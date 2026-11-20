"""Imprime, em forma compacta, o próximo lote de denúncias ainda não codificadas.

Uso (da raiz do repo):
    python3 scripts/lote_codificacao.py ESTRATO [N] [--todas] [--ordens 3,5,9]

Serve à codificação assistida de artifício, meio e papel do denunciado
(passo 1 do HANDOFF). Considera codificado todo número presente em
dados/extracao/codificacao_manual_r*.csv ou em codificacao_assistida.csv.

Decisões de compactação, para caber a leitura caso a caso no contexto:
- a narrativa até LIMITE caracteres vai inteira;
- acima disso, vão o início (CABECA), as frases do restante que tocam o papel
  do denunciado ou o meio de pagamento (até JANELAS caracteres) e o fim (CAUDA),
  porque é no fim que a denúncia costuma identificar a conta recebedora;
- a capitulação vai truncada, só para ver quem é denunciado e por quê;
- as colunas m_* da extração vão como pista, nunca como codificação.
"""
import csv
import glob
import json
import re
import sys

LIMITE, CABECA, JANELAS, CAUDA, CAP = 5000, 3000, 1800, 600, 450
CHAVES = re.compile(
    r"denunciad|titular|conta|chave pix|\bpix\b|cedeu|emprest|vendeu|abriu|"
    r"sacou|saque|transfer|recebe|benefici|whatsapp|boleto|invad|acess",
    re.I,
)
PISTAS = ["m_whatsapp", "m_pix", "m_boleto", "m_conta_laranja",
          "m_invasao_dispositivo", "vitima_idosa", "contexto_vd", "vitima_pj"]


def compacta(t):
    t = re.sub(r"\s+", " ", t or "").strip()
    if len(t) <= LIMITE:
        return t
    meio = t[CABECA:-CAUDA]
    frases = re.split(r"(?<=[.;])\s+", meio)
    sel, tam = [], 0
    for f in frases:
        if CHAVES.search(f) and tam + len(f) <= JANELAS:
            sel.append(f)
            tam += len(f)
    return f"{t[:CABECA]} [...] {' '.join(sel)} [...] {t[-CAUDA:]}"


def codificados():
    feitos = set()
    arqs = glob.glob("dados/extracao/codificacao_manual_r*.csv")
    arqs += glob.glob("dados/extracao/codificacao_assistida.csv")
    for a in arqs:
        with open(a, encoding="utf-8") as f:
            feitos |= {r["numero"] for r in csv.DictReader(f)}
    return feitos


def main():
    args = sys.argv[1:]
    estrato = args[0]
    n = int(args[1]) if len(args) > 1 and args[1].isdigit() else 10
    ordens = None
    if "--ordens" in args:
        ordens = set(args[args.index("--ordens") + 1].split(","))
    feitos = set() if "--todas" in args else codificados()
    with open("dados/extracao/denuncias_tjsp.csv", encoding="utf-8") as f:
        linhas = [r for r in csv.DictReader(f) if r["estrato"] == estrato]
    linhas.sort(key=lambda r: int(r["ordem"]))
    if ordens:
        linhas = [r for r in linhas if r["ordem"] in ordens]
    else:
        linhas = [r for r in linhas if r["numero"] not in feitos][:n]
    for r in linhas:
        with open(f"dados/extracao/segmentos/{r['numero']}.json", encoding="utf-8") as f:
            seg = json.load(f)
        pistas = " ".join(p.replace("m_", "") for p in PISTAS if r.get(p) in ("1", "True"))
        print(f"### {r['estrato']} {r['ordem']} {r['numero']} | {r['tipo_capitulacao']} "
              f"| den={r['n_denunciados_cap'] or '?'} | dup={r['duplicata_de'] or '-'} | {pistas}")
        print("NARR:", compacta(seg.get("narrativa")))
        print("CAP:", re.sub(r"\s+", " ", seg.get("capitulacao") or "")[:CAP])
        print()


if __name__ == "__main__":
    main()
