"""Coleta, na conversa, das sentenças dos casos da matriz de seleção. Rodar da raiz do repo.

    python3 scripts/pipe_sentencas.py next
        próximo caso de dados/extracao/matriz_casos.csv sem status
    python3 scripts/pipe_sentencas.py ids NUM ID:CHARS [ID:CHARS ...]
        guarda o processo corrente em /tmp/sent_cur.json e imprime a lista de IDs
        repetidos até a saída do lote passar de cerca de 75 KB, o que força a
        gravação do resultado em arquivo e mantém o texto fora da conversa
    python3 scripts/pipe_sentencas.py grava ARQUIVO_DO_LOTE
        grava o texto (sem a linha Original), o manifesto e o status, e imprime
        só o dispositivo, para a extração do resultado
    python3 scripts/pipe_sentencas.py status NUM STATUS "detalhe"

Roteiro por caso, com o Codex: pdpj_list_movimentos(NUM, tipo_filter="cedência")
acha o movimento de procedência ou improcedência e o documento da sentença; sem
ele, tentar "Extin", "Julgamento" ou o mapa. A data do movimento deve bater com a
data de disponibilização no cjpg (matriz_casos.csv). Depois, o lote com os IDs
impressos por `ids` e, por fim, `grava`.
"""
import csv
import hashlib
import json
import math
import os
import re
import sys
from datetime import datetime, timezone

sys.path.insert(0, "scripts")
import codex_denuncias as c  # noqa: E402  (separa_lote, normaliza, procedencia, anexar)

CUR = "/tmp/sent_cur.json"
MATRIZ = os.path.join("dados", "extracao", "matriz_casos.csv")
STATUS = os.path.join("dados", "codex", "status_sentencas.csv")
MANIFESTO = os.path.join("textos", "tjsp", "manifesto_sentencas.csv")
DIR = os.path.join("textos", "tjsp", "sentencas")
CAMPOS_MAN = ["numero", "caso", "documento_id", "parte", "data_mov", "procedencia", "chars", "sha256", "lido_em"]
# fecho do relatório e da fundamentação: o dispositivo começa no último destes
RE_DISP = re.compile(r"(ante o exposto|diante do exposto|posto isso|isto posto|pelo exposto|em face do exposto|"
                     r"diante disso|ante o acima exposto|em raz[aã]o do exposto|julgo (parcialmente )?(im)?procedente)", re.I)

agora = lambda: datetime.now(timezone.utc).isoformat(timespec="seconds")


def matriz():
    with open(MATRIZ, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def caso_de(num):
    return next((m["caso"] for m in matriz() if m["numero"] == num), "")


def status(num, st, docs=0, det=""):
    linha = dict(numero=num, caso=caso_de(num), status=st, docs=docs, quando=agora(), detalhe=det)
    c.anexar(STATUS, list(linha), linha)


def ler(arq):
    s = open(arq, encoding="utf-8").read()
    if s.lstrip().startswith("["):  # resultado de MCP salvo como lista de blocos de texto
        v, _ = json.JSONDecoder().raw_decode(s.lstrip())
        s = "\n".join(b.get("text", "") for b in v)
    return s


def dispositivo(t, n=2600):
    # o "julgo ... procedente" é o melhor marco; o fecho genérico às vezes cai na parte sobre a prisão
    ms = list(re.finditer(r"julgo[^.]{0,40}procedente|absolvo|declaro extinta", t, re.I)) or list(RE_DISP.finditer(t))
    ini = ms[-1].start() if ms else max(0, len(t) - n)
    return re.sub(r"\s+", " ", t[ini:ini + n])


cmd = sys.argv[1]
if cmd == "next":
    feitos = {s["numero"] for s in c.ler_csv(STATUS)} if os.path.exists(STATUS) else set()
    pend = [m for m in matriz() if m["numero"] not in feitos]
    print(f"{pend[0]['caso']} {pend[0]['numero']} cjpg {pend[0]['data_disponibilizacao_cjpg']} | faltam {len(pend)}"
          if pend else "FIM")
elif cmd == "ids":
    num, docs = sys.argv[2], []
    for a in sys.argv[3:]:
        uid, _, ch = a.partition(":")
        docs.append({"id": uid, "chars": int(ch or 0)})
    json.dump({"numero": num, "docs": docs}, open(CUR, "w"))
    tot = sum(d["chars"] or 5000 for d in docs)  # tamanho desconhecido: supõe 5 mil e repete mais
    rep = max(1, min(50 // len(docs), math.ceil(75000 / max(tot, 1))))
    print(json.dumps([d["id"] for d in docs] * rep))
elif cmd == "grava":
    cur = json.load(open(CUR))
    num = cur["numero"]
    textos = c.separa_lote(ler(sys.argv[2]))
    d = os.path.join(DIR, num)
    n, todo = 0, []
    for k, doc in enumerate(cur["docs"], 1):
        corpo = textos.get(doc["id"])
        if not corpo or len(corpo.strip()) < 40:
            continue
        assert "?t=" not in corpo  # o link Original traz token e nunca é gravado
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, f"{k:02d}_{doc['id']}.txt"), "w", encoding="utf-8").write(corpo)
        c.anexar(MANIFESTO, CAMPOS_MAN, dict(numero=num, caso=caso_de(num), documento_id=doc["id"], parte=k,
                 data_mov=doc.get("data", ""), procedencia=c.procedencia(corpo), chars=len(corpo),
                 sha256=hashlib.sha256(corpo.encode()).hexdigest(), lido_em=agora()))
        n += 1
        todo.append(corpo)
    status(num, "ok" if n else "sem_texto", n)
    t = "\n".join(todo)
    print(f"gravado {caso_de(num)} {num}: {n} doc(s), {len(t)} chars")
    if t:
        print("DISPOSITIVO:", dispositivo(t))
elif cmd == "status":
    status(sys.argv[2], sys.argv[3], 0, sys.argv[4] if len(sys.argv) > 4 else "")
    print("status", sys.argv[2], sys.argv[3])
