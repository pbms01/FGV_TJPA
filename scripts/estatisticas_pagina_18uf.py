"""Gera a página do gráfico a partir do CSV montado por painel_estelionato.py.

Todos os números da página saem do CSV por este script; nenhum é digitado à mão.
Uso, da raiz do repo: python3 scripts/estatisticas_pagina_18uf.py
(entrada: dados/estatisticas/estelionato_uf_2021_2025.csv; saída: docs/estatisticas/paginas/estelionato_18uf.html,
 publicada no claude.ai como artefato "Estelionato eletrônico em 18 UFs")
"""
import csv
import json
import sys

ANOS = [2021, 2022, 2023, 2024, 2025]
# Painel balanceado: UFs com valor eletrônico nos cinco anos e sem quebra de registro declarada.
EXCLUIDAS = {
    "São Paulo": "nunca informou o meio eletrônico",
    "Rio de Janeiro": "nunca informou o meio eletrônico",
    "Ceará": "nunca informou o meio eletrônico",
    "Pernambuco": "natureza criada no sistema em dez/2024; 2023 retirado",
    "Pará": "mudou a metodologia em 2023 (antes contava todas as fraudes)",
    "Rio Grande do Sul": "registra desde 27/07/2023",
    "Bahia": "sem dado em 2021",
    "Rio Grande do Norte": "sem dado em 2021 e 2022",
    "Amazonas": "revisões sem nota (2023: 877 para 3.829; 2024: 6.035 para 972)",
}


def main(csv_path, tpl_path, out_path):
    rows = list(csv.DictReader(open(csv_path, encoding="utf-8")))
    m = {(r["uf"], int(r["ano"])): r for r in rows}
    ufs_all = sorted({r["uf"] for r in rows} - {"Brasil"})
    painel = [u for u in ufs_all if u not in EXCLUIDAS]
    # salvaguarda: o painel só aceita UF com os cinco valores presentes
    for u in painel:
        for a in ANOS:
            assert m[(u, a)]["estelionato_eletronico"] != "", (u, a)

    serie = []
    for a in ANOS:
        e = sum(int(m[(u, a)]["estelionato_eletronico"]) for u in painel)
        t = sum(int(m[(u, a)]["estelionato_total"]) for u in painel)
        br = int(m[("Brasil", a)]["estelionato_total"])
        br_e = int(m[("Brasil", a)]["estelionato_eletronico"])
        serie.append({"ano": a, "eletronico": e, "comum": t - e, "total": t,
                      "brasil_total": br, "brasil_eletronico_composicao_variavel": br_e})

    por_uf = []
    for u in ufs_all:
        vals = []
        for a in ANOS:
            v = m.get((u, a), {}).get("estelionato_eletronico", "")
            vals.append(None if v == "" else int(v))
        por_uf.append({"uf": u, "eletronico": vals, "painel": u not in EXCLUIDAS,
                       "motivo": EXCLUIDAS.get(u, "")})

    s = {x["ano"]: x for x in serie}
    resumo = {
        "n_ufs": len(painel),
        "e2021": s[2021]["eletronico"], "e2022": s[2022]["eletronico"], "e2025": s[2025]["eletronico"],
        "c2021": s[2021]["comum"], "c2022": s[2022]["comum"], "c2025": s[2025]["comum"],
        "mult_e_2021": s[2025]["eletronico"] / s[2021]["eletronico"],
        "mult_c_2021": s[2025]["comum"] / s[2021]["comum"],
        "mult_e_2022": s[2025]["eletronico"] / s[2022]["eletronico"],
        "mult_c_2022": s[2025]["comum"] / s[2022]["comum"],
        "aum_total_22_25": s[2025]["total"] - s[2022]["total"],
        "aum_e_22_25": s[2025]["eletronico"] - s[2022]["eletronico"],
        "share_e_2021": s[2021]["eletronico"] / s[2021]["total"],
        "share_e_2025": s[2025]["eletronico"] / s[2025]["total"],
        "painel_sobre_brasil_2025": s[2025]["total"] / s[2025]["brasil_total"],
        "go_t2022": int(m[("Goiás", 2022)]["estelionato_total"]),
        "go_t2025": int(m[("Goiás", 2025)]["estelionato_total"]),
        "go_e2022": int(m[("Goiás", 2022)]["estelionato_eletronico"]),
        "go_e2025": int(m[("Goiás", 2025)]["estelionato_eletronico"]),
    }
    resumo["parte_e_aumento"] = resumo["aum_e_22_25"] / resumo["aum_total_22_25"]

    data = {"serie": serie, "por_uf": por_uf, "resumo": resumo, "painel": painel}
    html = open(tpl_path, encoding="utf-8").read().replace("/*__DATA__*/null", json.dumps(data, ensure_ascii=False))
    assert "—" not in html and "–" not in html, "travessão na página"
    open(out_path, "w", encoding="utf-8").write(html)
    print(json.dumps(resumo, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main(*(sys.argv[1:4] or ["dados/estatisticas/estelionato_uf_2021_2025.csv",
                             "scripts/templates/estelionato_18uf.html",
                             "docs/estatisticas/paginas/estelionato_18uf.html"]))
