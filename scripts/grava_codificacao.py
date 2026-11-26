"""Acrescenta linhas a dados/extracao/codificacao_assistida.csv a partir da entrada padrão.

Uso (da raiz do repo):
    python3 scripts/grava_codificacao.py <<'FIM'
    INV 6|relacional|rede_social|controle_parceira|invasor|000000001|nota livre
    FIM

Cada linha traz: "ESTRATO ORDEM|contexto|meio_contato|artificio|papel_denunciado|
nove dígitos 0/1|nota". Os nove dígitos seguem a ordem das colunas da r1:
whatsapp, pix_pagamento, boleto, falso_parente, falsa_central, venda_falsa,
investimento, conta_do_denunciado, invasao.

O número do processo vem de denuncias_tjsp.csv pelo par estrato e ordem, para
evitar erro de digitação. Uma linha com número já gravado substitui a anterior,
o que permite corrigir sem editar o CSV à mão. Valores fora do vocabulário
abortam a gravação, a menos que estejam em NOVOS (categorias acrescentadas na
codificação assistida e documentadas no LEIAME).

Com TRIB=tjpa grava em dados/extracao/codificacao_assistida_tjpa.csv, com as
mesmas colunas, e tira o número de denuncias_tjpa.csv. O artifício do TJPA já
foi codificado e conferido por segundo leitor (codificacao_artificio_tjpa.csv):
na linha de entrada ele vai como "=", que copia o valor de lá; um valor escrito
por extenso tem de ser igual ao de lá, senão a gravação aborta (para mudar o
artifício, o caminho é scripts/artificio_tjpa.py). Duplicata não é codificada.
"""
import csv
import glob
import os
import sys

TRIB = os.environ.get("TRIB", "tjsp")
ARQ = {"tjsp": "dados/extracao/codificacao_assistida.csv",
       "tjpa": "dados/extracao/codificacao_assistida_tjpa.csv"}[TRIB]
ARQ_DEN = {"tjsp": "dados/extracao/denuncias_tjsp.csv", "tjpa": "dados/extracao/denuncias_tjpa.csv"}[TRIB]
ARQ_ARTIFICIO_TJPA = "dados/extracao/codificacao_artificio_tjpa.csv"
COLS = ["numero", "estrato", "ordem", "contexto", "meio_contato", "artificio",
        "papel_denunciado", "whatsapp", "pix_pagamento", "boleto", "falso_parente",
        "falsa_central", "venda_falsa", "investimento", "conta_do_denunciado",
        "invasao", "nota"]
BIN = COLS[7:16]

# Categorias novas da codificação assistida; cada uma precisa de nota no LEIAME.
NOVOS = {
    "contexto": {"relacional", "outro"},
    "meio_contato": {"outro"},
    "artificio": {"devassa_privacidade", "taxa_antecipada", "extorsao_transferencia", "falso_relacionamento", "outro"},
    "papel_denunciado": set(),
}


def vocabulario():
    voc = {k: set() for k in NOVOS}
    for a in glob.glob("dados/extracao/codificacao_manual_r*.csv"):
        with open(a, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                for k in voc:
                    voc[k].add(r[k])
    for k in voc:
        voc[k] |= NOVOS[k]
    return voc


def main():
    with open(ARQ_DEN, encoding="utf-8") as f:
        den = list(csv.DictReader(f))
    numeros = {(r["estrato"], r["ordem"]): r["numero"] for r in den}
    duplicatas = {r["numero"] for r in den if r.get("duplicata_de")} if TRIB == "tjpa" else set()
    artificio_tjpa = {}
    if TRIB == "tjpa":
        with open(ARQ_ARTIFICIO_TJPA, encoding="utf-8") as f:
            artificio_tjpa = {r["numero"]: r["artificio"] for r in csv.DictReader(f)}
    voc = vocabulario()
    try:
        with open(ARQ, encoding="utf-8") as f:
            atuais = {r["numero"]: r for r in csv.DictReader(f)}
    except FileNotFoundError:
        atuais = {}
    novos = []
    for linha in sys.stdin:
        linha = linha.strip()
        if not linha or linha.startswith("#"):
            continue
        chave, contexto, meio, artificio, papel, bits, nota = linha.split("|", 6)
        estrato, ordem = chave.split()
        if len(bits) != 9 or set(bits) - {"0", "1"}:
            sys.exit(f"bits inválidos em {chave}: {bits}")
        if TRIB == "tjpa":
            numero = numeros[(estrato, ordem)]
            if numero in duplicatas:
                sys.exit(f"{chave}: duplicata, não se codifica")
            if artificio not in ("=", artificio_tjpa[numero]):
                sys.exit(f"{chave}: artificio={artificio} difere do codificado ({artificio_tjpa[numero]})")
            artificio = artificio_tjpa[numero]
        valores = {"contexto": contexto, "meio_contato": meio,
                   "artificio": artificio, "papel_denunciado": papel}
        for k, v in valores.items():
            if TRIB == "tjpa" and k == "artificio":
                continue
            if v not in voc[k]:
                sys.exit(f"{chave}: {k}={v} fora do vocabulário {sorted(voc[k])}")
        r = {"numero": numeros[(estrato, ordem)], "estrato": estrato, "ordem": ordem,
             **valores, **dict(zip(BIN, bits)), "nota": nota.strip()}
        novos.append(r)
    for r in novos:
        atuais[r["numero"]] = r
    with open(ARQ, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        ordem_estrato = {"INV": 0, "CL": 1, "FE": 2}
        for r in sorted(atuais.values(),
                        key=lambda r: (ordem_estrato[r["estrato"]], int(r["ordem"]))):
            w.writerow(r)
    print(f"{len(novos)} gravadas; {len(atuais)} no arquivo")


if __name__ == "__main__":
    main()
