"""Registra o andamento em segundo grau das sentenças da amostra que trataram da Lei 15.397/2026.

Uso: python3 scripts/registra_apelacao.py NUMERO campo=valor [campo=valor ...]
Uma linha por processo em dados/tjsp2/apelacoes_amostra.csv; chamar de novo com o
mesmo número atualiza os campos dados e preserva os demais. Fonte das linhas: DJEN pelo
Codex (pdpj_buscar_comunicacoes) e, quando houver, o texto do acórdão.
"""
import csv
import os
import sys

BASE = os.path.join(os.path.dirname(__file__), "..")
ARQ = os.path.join(BASE, "dados/tjsp2/apelacoes_amostra.csv")
CAMPOS = ["caso", "numero", "data_sentenca", "lei_15397_sentenca", "recorrente",
          "distribuicao", "camara", "relator", "julgamento", "resultado_acordao",
          "trata_inciso_vii", "leitura_acordao", "fonte", "nota"]


def main():
    num, pares = sys.argv[1], sys.argv[2:]
    linhas = list(csv.DictReader(open(ARQ, encoding="utf-8"))) if os.path.exists(ARQ) else []
    alvo = next((x for x in linhas if x["numero"] == num), None)
    if alvo is None:
        alvo = {c: "" for c in CAMPOS}
        alvo["numero"] = num
        linhas.append(alvo)
    for p in pares:
        k, v = p.split("=", 1)
        if k not in CAMPOS:
            sys.exit(f"campo desconhecido: {k}")
        alvo[k] = v
    with open(ARQ, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        w.writeheader()
        w.writerows(linhas)
    print(alvo["caso"] or num, {k: v for k, v in alvo.items() if v and k not in ("numero",)})


if __name__ == "__main__":
    main()
