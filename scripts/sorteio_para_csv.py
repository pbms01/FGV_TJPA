#!/usr/bin/env python3
"""Converte o resultado do sorteio (JSON de scripts/cjpg_sorteio.js) em dados/cjpg/amostra_tjsp.csv.

Uso:
    python scripts/sorteio_para_csv.py resultado.json

Aceita o JSON puro de sorteio.resultado() ou a saída da ferramenta de JavaScript
do navegador gravada em arquivo (lista de blocos com o texto JSON dentro).
Grava também dados/cjpg/sorteio_listas.json com totais, páginas sorteadas e
frações, para refazer os pesos.
"""
import csv
import json
import os
import re
import sys

CAMPOS = ["estrato", "ordem_no_estrato", "numero", "lista", "pagina", "elegiveis_na_pagina", "peso",
          "classe", "assunto", "comarca", "foro", "vara", "data_disponibilizacao", "cd_doc_cjpg",
          "chars_sentenca", "m_171_2A", "m_fraude_eletronica", "m_154A", "m_conta_laranja",
          "m_imputacao", "condena", "absolve", "imputacao", "dv_ok"]


def dv_ok(numero):
    m = re.fullmatch(r"(\d{7})-(\d{2})\.(\d{4})\.(\d)\.(\d{2})\.(\d{4})", numero or "")
    if not m:
        return False
    n, d, a, j, t, o = m.groups()
    return 98 - (int(n + a + j + t + o) * 100) % 97 == int(d)


def carrega(caminho):
    s = open(caminho, encoding="utf-8").read()
    v, _ = json.JSONDecoder().raw_decode(s.lstrip())
    while True:
        if isinstance(v, list) and v and isinstance(v[0], dict) and "text" in v[0]:
            v, _ = json.JSONDecoder().raw_decode(v[0]["text"])
        elif isinstance(v, str):
            v, _ = json.JSONDecoder().raw_decode(v)
        else:
            return v


def main():
    r = carrega(sys.argv[1])
    os.makedirs(os.path.join("dados", "cjpg"), exist_ok=True)
    with open(os.path.join("dados", "cjpg", "amostra_tjsp.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS, extrasaction="ignore")
        w.writeheader()
        for a in sorted(r["amostra"], key=lambda a: (a["estrato"], a["ordem_no_estrato"])):
            w.writerow(dict(a, dv_ok=dv_ok(a["numero"])))
    meta = {k: r[k] for k in ("semente", "por_pagina", "inicio", "fim", "listas")}
    json.dump(meta, open(os.path.join("dados", "cjpg", "sorteio_listas.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    por = {}
    for a in r["amostra"]:
        por[a["estrato"]] = por.get(a["estrato"], 0) + 1
    print("sorteados por estrato:", por, "| total:", len(r["amostra"]),
          "| dv inválido:", sum(not dv_ok(a["numero"]) for a in r["amostra"]))


if __name__ == "__main__":
    main()
