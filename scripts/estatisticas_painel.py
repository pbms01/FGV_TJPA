"""Série de estelionato (total) e estelionato por meio eletrônico por UF, 2021 a 2025, a partir das
tabelas de quatro edições do Anuário Brasileiro de Segurança Pública (FBSP), e painel balanceado.

Grava, da raiz do repo (depois de scripts/estatisticas_baixa.py):
- dados/estatisticas/anuario_estelionato_por_edicao.csv: o que cada edição publicou para cada UF e
  ano, inclusive o ano revisto (serve para medir as revisões entre edições);
- dados/estatisticas/estelionato_uf_2021_2025.csv: um valor por UF e ano, o da edição mais recente.

Decisões não óbvias:
- Cada edição traz dois anos; o primeiro é "atualização" da edição anterior. Fica o valor da edição
  mais recente, porque o FBSP revisa para trás (ex.: Pará 2023, de 16.884 para 1.686).
- A numeração da tabela muda entre edições (T15 em 2023 e 2024, aba T19 com título "Tabela 15" em
  2025, T17 em 2026); as abas estão fixadas abaixo e conferidas pelo título.
- O total "Brasil" do meio eletrônico soma só as UFs que informaram no ano; o painel balanceado é
  montado depois, em scripts/estatisticas_pagina_18uf.py.
Uso: python3 scripts/estatisticas_painel.py
"""
import csv
import pathlib

import openpyxl

BRUTO = pathlib.Path("dados/bruto/anuario")
SAIDA = pathlib.Path("dados/estatisticas")
FONTES = [  # (arquivo, aba, edição, anos da tabela)
    ("anuario2023.xlsx", "T15", 17, (2021, 2022)),
    ("anuario2024.xlsx", "T15", 18, (2022, 2023)),
    ("anuario2025.xlsx", "T19", 19, (2023, 2024)),
    ("anuario2026.xlsx", "T17", 20, (2024, 2025)),
]


def num(v):
    return None if v in (None, "...", "-") else int(round(float(v)))


def limpa_uf(s):
    return s.split(" (")[0].strip()  # remove marcador de nota, ex. "Pernambuco (4)"


def le_edicoes():
    linhas = []
    for arq, aba, ed, anos in FONTES:
        ws = openpyxl.load_workbook(BRUTO / arq, read_only=True, data_only=True)[aba]
        titulo = " ".join(str(c) for r in ws.iter_rows(min_row=1, max_row=3, values_only=True) for c in r if c)
        assert "Estelionato por meio eletr" in titulo, (arq, aba, titulo)
        for r in ws.iter_rows(values_only=True):
            if not r or not isinstance(r[0], str):
                continue
            nome = r[0].strip()
            if nome.startswith(("(", "Fonte", "Brasil e", "Ns.", "TABELA", "Estelionato")):
                continue
            vals = [c for c in r[1:] if c is not None]
            if len(vals) < 10:
                continue
            # colunas: total a1, total a2, taxa a1, taxa a2, var, eletr a1, eletr a2, taxa, taxa, var
            for i, ano in enumerate(anos):
                linhas.append({"uf": limpa_uf(nome), "ano": ano, "edicao": ed, "aba": aba,
                               "estelionato_total": num(vals[i]), "estelionato_eletronico": num(vals[5 + i])})
    return linhas


def main():
    SAIDA.mkdir(parents=True, exist_ok=True)
    linhas = le_edicoes()
    campos = ["uf", "ano", "edicao", "aba", "estelionato_total", "estelionato_eletronico"]
    with open(SAIDA / "anuario_estelionato_por_edicao.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        for l in sorted(linhas, key=lambda x: (x["uf"], x["ano"], x["edicao"])):
            w.writerow({k: ("" if l[k] is None else l[k]) for k in campos})
    ultimo = {}
    for l in linhas:
        k = (l["uf"], l["ano"])
        if k not in ultimo or ultimo[k]["edicao"] < l["edicao"]:
            ultimo[k] = l
    with open(SAIDA / "estelionato_uf_2021_2025.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["uf", "ano", "edicao_fonte", "estelionato_total", "estelionato_eletronico"])
        for (uf, ano), l in sorted(ultimo.items()):
            w.writerow([uf, ano, l["edicao"], "" if l["estelionato_total"] is None else l["estelionato_total"],
                        "" if l["estelionato_eletronico"] is None else l["estelionato_eletronico"]])
    print(f"{len(linhas)} linhas por edição; {len(ultimo)} pares UF e ano")


if __name__ == "__main__":
    main()
