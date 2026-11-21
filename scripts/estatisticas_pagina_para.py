"""Gera a página do Pará: registros da Polícia Civil (censo SIAC/SEGUP-PA publicado por Silva, Ramos e
Reis Netto, Revista Tópicos, 2026) contra o que o Anuário FBSP conta como "estelionato por meio eletrônico".

Decisões não óbvias:
- A Tabela 1 do artigo é lida do HTML do próprio artigo (versão web), não digitada; o script confere as somas.
- A série do Anuário para o Pará vem do CSV do painel (valor da edição mais recente por ano). A partir de
  2023 a SSP/PA passou a filtrar só os §§ 2º-A, 2º-B e 3º (nota 4 da 19ª edição); 2022 ainda usa o filtro antigo.
Grava também dados/estatisticas/para_artigo_tabelas.csv, com as Tabelas 1 e 2 do artigo como lidas.
Uso, da raiz do repo, depois de estatisticas_baixa.py e estatisticas_painel.py:
  python3 scripts/estatisticas_pagina_para.py
(saída: docs/estatisticas/paginas/para_crime_eletronico.html, publicada no claude.ai como artefato
 "Crime patrimonial eletrônico no Pará", e dados/estatisticas/para_registros_2022_2025.csv)
"""
import csv
import html as h
import json
import re
import sys

ANOS = [2022, 2023, 2024, 2025]


def num(s):
    return int(s.replace(".", ""))


def tabelas_como_lidas(path, saida):
    """Grava as Tabelas 1 (estado) e 2 (DECCC) do artigo como estão no HTML. A coluna Total das linhas
    da Tabela 2 repete a da Tabela 1 por erro do artigo; fica como lida, e a soma correta vai na
    coluna total_recalculado."""
    s = open(path, encoding="utf-8", errors="replace").read()
    linhas = []
    for n, t in enumerate(re.findall(r"<table.*?</table>", s, flags=re.S | re.I), start=1):
        for r in re.findall(r"<tr.*?</tr>", t, flags=re.S | re.I):
            cells = [h.unescape(re.sub(r"<[^>]+>", "", c)).strip()
                     for c in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", r, flags=re.S | re.I)]
            if cells and cells[0] in ("Estelionato", "Fraude Eletrônica", "Furto", "Total"):
                anos = [num(x) for x in cells[1:5]]
                linhas.append({"tabela": n, "unidade": "estado" if n == 1 else "DECCC", "categoria": cells[0],
                               "a2022": anos[0], "a2023": anos[1], "a2024": anos[2], "a2025": anos[3],
                               "total_como_lido": num(cells[5]), "total_recalculado": sum(anos),
                               "var_22_23": cells[6], "var_23_24": cells[7], "var_24_25": cells[8]})
    with open(saida, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0].keys()))
        w.writeheader()
        w.writerows(linhas)


def tabela1(path):
    s = open(path, encoding="utf-8", errors="replace").read()
    t = re.findall(r"<table.*?</table>", s, flags=re.S | re.I)[0]
    out = {}
    for r in re.findall(r"<tr.*?</tr>", t, flags=re.S | re.I):
        cells = [h.unescape(re.sub(r"<[^>]+>", "", c)).strip()
                 for c in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", r, flags=re.S | re.I)]
        if cells and cells[0] in ("Estelionato", "Fraude Eletrônica", "Furto", "Total"):
            out[cells[0]] = [num(x) for x in cells[1:5]]
    # conferência das somas: categorias somam o total de cada ano
    for i in range(4):
        assert out["Estelionato"][i] + out["Fraude Eletrônica"][i] + out["Furto"][i] == out["Total"][i], i
    return out


def main(art, anu_csv, tpl, out_html, out_csv):
    tabelas_como_lidas(art, "dados/estatisticas/para_artigo_tabelas.csv")
    t1 = tabela1(art)
    anu = {int(r["ano"]): r for r in csv.DictReader(open(anu_csv, encoding="utf-8")) if r["uf"] == "Pará"}
    serie = []
    for i, a in enumerate(ANOS):
        serie.append({
            "ano": a,
            "caput": t1["Estelionato"][i],          # art. 171, caput, por meio eletrônico
            "qualif": t1["Fraude Eletrônica"][i],    # art. 171, § 2º-A
            "furto": t1["Furto"][i],                 # art. 155, § 4º-B
            "total": t1["Total"][i],
            "anuario_eletr": int(anu[a]["estelionato_eletronico"]),
            "anuario_eletr_ed": int(anu[a]["edicao_fonte"]),
            "anuario_estel_total": int(anu[a]["estelionato_total"]),
        })
    s = {x["ano"]: x for x in serie}
    R = {
        "tot22": s[2022]["total"], "tot25": s[2025]["total"],
        "cresc_22_25": s[2025]["total"] / s[2022]["total"] - 1,
        "cresc_22_23": s[2023]["total"] / s[2022]["total"] - 1,
        "anu22": s[2022]["anuario_eletr"], "anu23": s[2023]["anuario_eletr"], "anu25": s[2025]["anuario_eletr"],
        "queda_anu_22_23": s[2023]["anuario_eletr"] / s[2022]["anuario_eletr"] - 1,
        "cob = anu/total": None,
        "cob23": s[2023]["anuario_eletr"] / s[2023]["total"],
        "cob24": s[2024]["anuario_eletr"] / s[2024]["total"],
        "cob25": s[2025]["anuario_eletr"] / s[2025]["total"],
        "furto25": s[2025]["furto"], "furto_sh25": s[2025]["furto"] / s[2025]["total"],
        "furto_tot": sum(x["furto"] for x in serie), "geral_tot": sum(x["total"] for x in serie),
        "caput_sh_estel25": s[2025]["caput"] / (s[2025]["caput"] + s[2025]["qualif"]),
        "caput_mais_qualif22": s[2022]["caput"] + s[2022]["qualif"],
        "qualif25": s[2025]["qualif"],
        "eletr_sobre_estel_total25": (s[2025]["caput"] + s[2025]["qualif"]) / s[2025]["anuario_estel_total"],
    }
    del R["cob = anu/total"]
    data = {"serie": serie, "resumo": R}
    page = open(tpl, encoding="utf-8").read().replace("/*__DATA__*/null", json.dumps(data, ensure_ascii=False))
    assert "—" not in page and "–" not in page, "travessão na página"
    open(out_html, "w", encoding="utf-8").write(page)
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(serie[0].keys()))
        w.writeheader()
        w.writerows(serie)
    print(json.dumps(R, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main(*(sys.argv[1:6] or ["dados/bruto/para/artigo_revista_topicos.html",
                             "dados/estatisticas/estelionato_uf_2021_2025.csv",
                             "scripts/templates/para.html",
                             "docs/estatisticas/paginas/para_crime_eletronico.html",
                             "dados/estatisticas/para_registros_2022_2025.csv"]))
