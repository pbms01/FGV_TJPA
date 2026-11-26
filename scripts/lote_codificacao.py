"""Imprime, em forma compacta, o próximo lote de denúncias ainda não codificadas.

Uso (da raiz do repo):
    python3 scripts/lote_codificacao.py ESTRATO [N] [--todas] [--ordens 3,5,9]
    TRIB=tjpa python3 scripts/lote_codificacao.py ESTRATO [N] [--todas] [--ordens 3,5,9]

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

Com TRIB=tjpa lê a extração da fase 2 (denuncias_tjpa.csv, segmentos_tjpa/),
pula as duplicatas, considera codificado o que está em
codificacao_assistida_tjpa.csv e mostra, como pista, o artifício já codificado
em codificacao_artificio_tjpa.csv. A compactação é mais curta (as narrativas do
MPPA são mais longas e trazem cabeçalho de página repetido) e as frases
escolhidas incluem as que dizem o canal do contato.
"""
import csv
import glob
import json
import os
import re
import sys

TRIB = os.environ.get("TRIB", "tjsp")
LIMITE, CABECA, JANELAS, CAUDA, CAP = 5000, 3000, 1800, 600, 450
if TRIB == "tjpa":
    LIMITE, CABECA, JANELAS, CAUDA, CAP = 1250, 620, 480, 120, 150
ARQ_DEN = {"tjsp": "dados/extracao/denuncias_tjsp.csv", "tjpa": "dados/extracao/denuncias_tjpa.csv"}[TRIB]
DIR_SEG = {"tjsp": "dados/extracao/segmentos", "tjpa": "dados/extracao/segmentos_tjpa"}[TRIB]
ARQ_ARTIFICIO_TJPA = "dados/extracao/codificacao_artificio_tjpa.csv"
CHAVES = re.compile(
    r"denunciad|titular|conta|chave pix|\bpix\b|cedeu|emprest|vendeu|abriu|"
    r"sacou|saque|transfer|recebe|benefici|whatsapp|boleto|invad|acess",
    re.I,
)
if TRIB == "tjpa":
    CHAVES = re.compile(CHAVES.pattern + r"|olx|facebook|instagram|marketplace|\bsite\b|link|ligou|liga[çc][ãa]o|"
                        r"telefon|\bsms\b|e-?mail|pessoalmente|comparec|dirigiu-se|loja|ag[êe]ncia|caixa eletr", re.I)
PISTAS = ["m_whatsapp", "m_pix", "m_boleto", "m_conta_laranja",
          "m_invasao_dispositivo", "vitima_idosa", "contexto_vd", "vitima_pj"]


# cabeçalho de página do MPPA, repetido no meio da narrativa
RE_CABECALHO_MPPA = re.compile(
    r"(?:\d+\s+)?(?:Bel[ée]m\s+[IVX]+\s*-\s*)?[^.;]{0,60}?Den[úu]ncia\s+\d{7}-\d{2}\.\d{4}\.8\.14\.\d{4}\s*"
    r"|(?:Pra|Pro|niPras|mpPPA|PPA)?\s*MINIST[ÉE]RIO P[ÚU]BLICO DO ESTADO DO PAR[ÁA]")


def compacta(t):
    t = re.sub(r"\s+", " ", t or "").strip()
    if TRIB == "tjpa":
        t = re.sub(r"\s+", " ", RE_CABECALHO_MPPA.sub(" ", t)).strip()
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
    if TRIB == "tjpa":
        arqs = glob.glob("dados/extracao/codificacao_assistida_tjpa.csv")
    else:
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
    with open(ARQ_DEN, encoding="utf-8") as f:
        linhas = [r for r in csv.DictReader(f) if r["estrato"] == estrato]
    artificio = {}
    if TRIB == "tjpa":
        linhas = [r for r in linhas if not r["duplicata_de"]]
        with open(ARQ_ARTIFICIO_TJPA, encoding="utf-8") as f:
            artificio = {r["numero"]: r for r in csv.DictReader(f)}
    linhas.sort(key=lambda r: int(r["ordem"]))
    if ordens:
        linhas = [r for r in linhas if r["ordem"] in ordens]
    else:
        linhas = [r for r in linhas if r["numero"] not in feitos][:n]
    for r in linhas:
        with open(f"{DIR_SEG}/{r['numero']}.json", encoding="utf-8") as f:
            seg = json.load(f)
        pistas = " ".join(p.replace("m_", "") for p in PISTAS if r.get(p) in ("1", "True"))
        if r["numero"] in artificio:
            a = artificio[r["numero"]]
            pistas += f" | artificio={a['artificio']} ({a['nota'][:90]})"
        print(f"### {r['estrato']} {r['ordem']} {r['numero']} | {r['tipo_capitulacao']} "
              f"| den={r['n_denunciados_cap'] or '?'} | dup={r['duplicata_de'] or '-'} | {pistas}")
        print("NARR:", compacta(seg.get("narrativa")))
        print("CAP:", re.sub(r"\s+", " ", seg.get("capitulacao") or "")[:CAP])
        print()


if __name__ == "__main__":
    main()
