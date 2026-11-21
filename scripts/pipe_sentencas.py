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

Amostra inteira (as 200 denúncias com texto, na ordem CL, INV, FE):

    python3 scripts/pipe_sentencas.py prox
        próximo processo da amostra sem status de sentença
    python3 scripts/pipe_sentencas.py lote ARQUIVO "AAAA-MM-DD|movimento|complemento"
        grava o lote, inferindo número e documentos pelo próprio arquivo, lê o resultado
        por regras (scripts/resultado_sentenca.py), acrescenta a linha em
        dados/extracao/sentencas_amostra.csv e imprime o resumo, o dispositivo quando a
        leitura pede revisão, e o próximo processo
    python3 scripts/pipe_sentencas.py sem NUM STATUS "detalhe"
        sem sentença, sigilo ou sentença sem texto
    python3 scripts/pipe_sentencas.py corrige NUM campo=valor [campo=valor ...]
        corrige os campos finais (resultado, tipo_acolhido, pena_meses, regime, nota) e marca conferido=lido
    python3 scripts/pipe_sentencas.py importa_matriz
        põe em sentencas_amostra.csv as 29 sentenças da matriz, já lidas à mão

Roteiro por caso, com o Codex: pdpj_list_movimentos(NUM, tipo_filter="cedência")
acha o movimento de procedência ou improcedência e o documento da sentença; sem
ele, tentar "Extin", "Julgamento" ou o mapa. A data do movimento deve bater com a
data de disponibilização no cjpg (matriz_casos.csv). Depois, o lote com os IDs
impressos por `ids` e, por fim, `grava`.
"""
import csv
import glob
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


AMOSTRA = os.path.join("dados", "cjpg", "amostra_tjsp.csv")
STATUS_DEN = os.path.join("dados", "codex", "status.csv")
SAIDA = os.path.join("dados", "extracao", "sentencas_amostra.csv")
ORDEM_ESTRATO = {"CL": 0, "INV": 1, "FE": 2}
CAMPOS_AUTO = ["resultado_auto", "condena_auto", "absolve_auto", "extingue_auto", "parcial_dito", "tipo_acolhido_auto",
               "acolhe_171_2A", "acolhe_171_2_VII", "acolhe_154A", "acolhe_155_4B", "acolhe_158", "acolhe_288",
               "acolhe_tentativa", "pena_meses_auto", "pena_texto_auto", "n_penas_auto", "regime_auto",
               "substituida_auto", "menciona_desclassificacao", "menciona_lei_15397", "desclassifica_disp", "fundamento_abs_auto", "revisar"]
CAMPOS_SAIDA = (["caso", "estrato", "ordem", "numero", "peso", "data_disp_cjpg", "data_mov", "movimento", "complemento_mov",
                 "documentos", "chars"] + CAMPOS_AUTO +
                ["resultado", "tipo_acolhido", "pena_meses", "regime", "conferido", "nota"])


def amostra():
    """As 200 denúncias com texto, com rótulo de caso, na ordem CL, INV, FE e pela ordem no estrato."""
    st = {}
    for r in c.ler_csv(STATUS_DEN):
        st[r["numero"]] = r["status"]
    lin = [r for r in csv.DictReader(open(AMOSTRA, encoding="utf-8")) if st.get(r["numero"]) == "ok"]
    for r in lin:
        r["caso"] = f"{r['estrato']} {r['ordem_no_estrato']}"
    return sorted(lin, key=lambda r: (ORDEM_ESTRATO[r["estrato"]], int(r["ordem_no_estrato"])))


def pendentes():
    feitos = {s["numero"] for s in c.ler_csv(STATUS)} if os.path.exists(STATUS) else set()
    return [r for r in amostra() if r["numero"] not in feitos]


def linha_saida(r, docs, chars, auto, mov="", conferido="auto", nota=""):
    data_mov, movimento, compl = (mov.split("|") + ["", "", ""])[:3]
    out = dict(caso=r["caso"], estrato=r["estrato"], ordem=r["ordem_no_estrato"], numero=r["numero"], peso=r["peso"],
               data_disp_cjpg=r["data_disponibilizacao"], data_mov=data_mov, movimento=movimento,
               complemento_mov=compl, documentos=docs, chars=chars, conferido=conferido, nota=nota)
    out.update({k: auto.get(k, "") for k in CAMPOS_AUTO})
    out.update(resultado=auto["resultado_auto"], tipo_acolhido=auto["tipo_acolhido_auto"],
               pena_meses=auto["pena_meses_auto"], regime=auto["regime_auto"])
    return out


def resumo(o):
    return (f"{o['resultado_auto']} | tipo {o['tipo_acolhido_auto'] or '-'} | pena {o['pena_meses_auto'] or '-'} m "
            f"({o['n_penas_auto']} penas) | regime {o['regime_auto'] or '-'} | subst {int(o['substituida_auto'])} | "
            f"descl {int(o['menciona_desclassificacao'])} | lei nova {int(o['menciona_lei_15397'])} | "
            f"descl no disp {int(o['desclassifica_disp'])} | 386 {o['fundamento_abs_auto'] or '-'} | revisar {int(o['revisar'])}")


def prox_txt():
    pend = pendentes()
    if not pend:
        return "FIM"
    r = pend[0]
    return f"PRÓXIMO {r['caso']} {r['numero']} cjpg {r['data_disponibilizacao']} | faltam {len(pend)}"


cmd = sys.argv[1]
if cmd == "prox":
    print(prox_txt())
elif cmd == "lote":
    import resultado_sentenca as rs
    bruto = ler(sys.argv[2])
    mov = sys.argv[3] if len(sys.argv) > 3 else ""
    urls = re.findall(r"mcp\.tecjustica\.com/doc/([\d.\-]+)/([0-9a-f\-]{36})", bruto)
    assert urls, "arquivo sem a linha Original: não dá para inferir o processo"
    num = urls[0][0]
    assert all(u[0] == num for u in urls), "lote com mais de um processo"
    ids = list(dict.fromkeys(u[1] for u in urls))
    r = next(x for x in amostra() if x["numero"] == num)
    textos = c.separa_lote(bruto)
    d = os.path.join(DIR, num)
    todo = []
    for k, uid in enumerate(ids, 1):
        corpo = textos.get(uid)
        if not corpo or len(corpo.strip()) < 40:
            continue
        assert "?t=" not in corpo  # o link Original traz token e nunca é gravado
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, f"{k:02d}_{uid}.txt"), "w", encoding="utf-8").write(corpo)
        c.anexar(MANIFESTO, CAMPOS_MAN, dict(numero=num, caso=r["caso"], documento_id=uid, parte=k,
                 data_mov=mov.split("|")[0], procedencia=c.procedencia(corpo), chars=len(corpo),
                 sha256=hashlib.sha256(corpo.encode()).hexdigest(), lido_em=agora()))
        todo.append(corpo)
    linha = dict(numero=num, caso=r["caso"], status="ok" if todo else "sem_texto", docs=len(todo), quando=agora(),
                 detalhe=mov)
    c.anexar(STATUS, list(linha), linha)
    t = "\n".join(todo)
    if t:
        o = rs.le(t)
        c.anexar(SAIDA, CAMPOS_SAIDA, linha_saida(r, len(todo), len(t), o, mov))
        print(f"{r['caso']} {num}: {len(todo)} doc(s), {len(t)} chars | {resumo(o)}")
        if o["revisar"]:
            print("DISPOSITIVO:", rs.dispositivo(t, 1100))
            if o["menciona_lei_15397"]:
                tt = re.sub(r"\s+", " ", t)
                ms = list(re.finditer(r"desclassific|emendatio|15\.?397", tt, re.I))
                print("TRECHO:", tt[max(0, ms[-1].start() - 300): ms[-1].start() + 300])
    else:
        print(f"{r['caso']} {num}: sem texto")
    print(prox_txt())
elif cmd == "sem":
    num = sys.argv[2]
    r = next(x for x in amostra() if x["numero"] == num)
    linha = dict(numero=num, caso=r["caso"], status=sys.argv[3], docs=0, quando=agora(),
                 detalhe=sys.argv[4] if len(sys.argv) > 4 else "")
    c.anexar(STATUS, list(linha), linha)
    print("status", r["caso"], num, sys.argv[3])
    print(prox_txt())
elif cmd == "corrige":
    num, pares = sys.argv[2], dict(a.split("=", 1) for a in sys.argv[3:])
    lin = list(csv.DictReader(open(SAIDA, encoding="utf-8")))
    alvo = [x for x in lin if x["numero"] == num]
    assert alvo, "número sem linha em sentencas_amostra.csv"
    for k in pares:
        assert k in ("resultado", "tipo_acolhido", "pena_meses", "regime", "nota"), k
    alvo[-1].update(pares, conferido="lido")
    with open(SAIDA, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, CAMPOS_SAIDA)
        w.writeheader()
        w.writerows(lin)
    print("corrigido", alvo[-1]["caso"], pares)
elif cmd == "recalcula":
    # refaz os campos automáticos de todas as linhas pelo texto gravado, sem tocar nos finais
    import resultado_sentenca as rs
    lin = list(csv.DictReader(open(SAIDA, encoding="utf-8")))
    for x in lin:
        caso = x["caso"]
        o = rs.le(rs.texto_do_caso(x["numero"], caso))
        x.update({k: o.get(k, "") for k in CAMPOS_AUTO})
        if x["conferido"] == "auto":
            x.update(resultado=o["resultado_auto"], tipo_acolhido=o["tipo_acolhido_auto"],
                     pena_meses=o["pena_meses_auto"], regime=o["regime_auto"])
    with open(SAIDA, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, CAMPOS_SAIDA)
        w.writeheader()
        w.writerows(lin)
    print("recalculadas", len(lin))
elif cmd == "importa_matriz":
    import resultado_sentenca as rs
    feitos = {x["numero"] for x in csv.DictReader(open(SAIDA, encoding="utf-8"))} if os.path.exists(SAIDA) else set()
    man = {x["caso"]: x for x in csv.DictReader(open(os.path.join("dados", "extracao", "sentencas_matriz.csv"), encoding="utf-8"))}
    am = {x["numero"]: x for x in amostra()}
    n = 0
    for m in matriz():
        if m["numero"] in feitos:
            continue
        t = rs.texto_do_caso(m["numero"], m["caso"])
        o = rs.le(t)
        cond, abs_, tipo = rs.REF[m["caso"]]
        res = o["resultado_auto"]
        if cond and not abs_ and res == "procedência parcial" and not o["parcial_dito"]:
            res = "condenação"
        lin = linha_saida(am[m["numero"]], len(glob.glob(os.path.join(DIR, m["numero"], "*.txt"))), len(t), o,
                          mov=man[m["caso"]]["data_sentenca"] + "||", conferido="matriz",
                          nota="lida à mão; ver sentencas_matriz.csv")
        lin.update(resultado=res, tipo_acolhido=tipo)
        c.anexar(SAIDA, CAMPOS_SAIDA, lin)
        n += 1
    print("importadas", n)
elif cmd == "next":
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
