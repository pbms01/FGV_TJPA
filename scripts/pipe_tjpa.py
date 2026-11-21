#!/usr/bin/env python3
"""Coleta da fase 2 (TJPA) na conversa: denúncia e sentença pelo Codex, gravadas sem passar pelo contexto.

Rodar da raiz do repositório. Roteiro por processo (docs/RUNBOOK_TJPA.md):
  1. python3 scripts/pipe_tjpa.py prox
  2. pdpj_visao_geral_processo(NUM)                    -> total de documentos, grau, sigilo
     pdpj_list_movimentos(NUM, tipo_filter="cedência") -> documento da sentença (procedência ou improcedência)
     pdpj_list_documentos(NUM, limit=40, offset=total-40) -> primeiras peças; denúncia do tipo "Denúncia"
     (sem ela: pdpj_list_movimentos(NUM, tipo_filter="Denúncia") dá a data do recebimento, e as petições
      juntadas antes dela entram como candidatas, papel "cand")
  3. python3 scripts/pipe_tjpa.py sel NUM "den:ID|nome|data|chars" "sent:ID|nome|data|chars" "cand:ID|nome|data|chars"
     -> imprime a lista de IDs repetida para a leitura em lote passar de cerca de 75 KB e ir para arquivo
  4. pdpj_read_documentos_batch(NUM, ids)  (o resultado vai para arquivo)
  5. python3 scripts/pipe_tjpa.py grava ARQUIVO
     -> grava o texto de cada peça (sem a linha Original:), o manifesto e o status; candidata só entra se
        o texto for de denúncia; imprime a capitulação e o dispositivo, para conferência
  Perdas: python3 scripts/pipe_tjpa.py status NUM sigilo|nao_encontrado|sem_denuncia|sem_texto "detalhe"
  Andamento: python3 scripts/pipe_tjpa.py resumo

Fila (dados/codex_tjpa/fila.csv, criada no primeiro uso a partir de dados/djen/alvos_djen_tjpa.csv):
  grupo 1 = ação penal ou apelação com sentença conhecida (publicada no DJEN ou apelada);
  grupo 2 = demais ações penais da lista. Ordem aleatória dentro do grupo, semente 20261121, para que
  parar no meio deixe uma subamostra aleatória. Inquéritos e flagrantes sem ação penal ficam fora.

Saídas:
  textos/tjpa/denuncias/<numero>/NN_<id>.txt e textos/tjpa/sentencas/<numero>/NN_<id>.txt
  textos/tjpa/manifesto.csv    numero, papel, documento_id, parte, nome, data, procedencia, chars, sha256, lido_em
  dados/codex_tjpa/status.csv  numero, grupo, status, denuncia, sentenca, chamadas, quando, detalhe (vale a última linha)
"""
import csv
import hashlib
import json
import os
import random
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
import codex_denuncias as c  # noqa: E402  (reusa separa_lote, procedencia, anexar, ler_csv, agora)

ALVOS = os.path.join("dados", "djen", "alvos_djen_tjpa.csv")
FILA = os.path.join("dados", "codex_tjpa", "fila.csv")
STATUS = os.path.join("dados", "codex_tjpa", "status.csv")
MANIFESTO = os.path.join("textos", "tjpa", "manifesto.csv")
DIR = {"den": os.path.join("textos", "tjpa", "denuncias"), "sent": os.path.join("textos", "tjpa", "sentencas")}
CUR = "/tmp/tjpa_cur.json"
SEMENTE = 20261121
CAMPOS_STATUS = ["numero", "grupo", "status", "denuncia", "sentenca", "chamadas", "quando", "detalhe"]
CAMPOS_MANIFESTO = ["numero", "papel", "documento_id", "parte", "nome", "data", "procedencia", "chars", "sha256", "lido_em"]

RE_DEN = re.compile(r"(?:ofere[cç]|ofert)\w*\s+(a\s+presente\s+|a\s+)?den[úu]ncia|vem\s+[^.]{0,200}den[úu]ncia|"
                    r"\bdenuncia[r]?\s+(o|a|os|as)\b|incurs[oa]s?\s+n", re.I)
RE_NAO_DEN = re.compile(r"resposta\s+[àa]\s+acusa|alega[çc][õo]es\s+finais|defesa\s+pr[ée]via|"
                        r"habilita[çc][ãa]o|procura[çc][ãa]o|arquivamento", re.I)


def fila():
    if not os.path.exists(FILA):
        alvos = c.ler_csv(ALVOS)
        g1 = [a["numero"] for a in alvos if (a["acao_penal"] == "1" or a["apelacao"] == "1")
              and (a["data_sentenca_djen"] or a["apelacao"] == "1")]
        g2 = [a["numero"] for a in alvos if a["acao_penal"] == "1" and a["numero"] not in g1]
        rnd = random.Random(SEMENTE)
        rnd.shuffle(g1)
        rnd.shuffle(g2)
        os.makedirs(os.path.dirname(FILA), exist_ok=True)
        with open(FILA, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["ordem", "grupo", "numero"])
            for k, n in enumerate(g1, 1):
                w.writerow([k, 1, n])
            for k, n in enumerate(g2, len(g1) + 1):
                w.writerow([k, 2, n])
    return c.ler_csv(FILA)


def feitos():
    return {s["numero"]: s for s in c.ler_csv(STATUS)}


def grupo(num):
    return next((f["grupo"] for f in fila() if f["numero"] == num), "")


def status(num, st, den=0, sent=0, chamadas=0, det=""):
    linha = dict(numero=num, grupo=grupo(num), status=st, denuncia=den, sentenca=sent, chamadas=chamadas,
                 quando=c.agora(), detalhe=det)
    c.anexar(STATUS, CAMPOS_STATUS, linha)


def ultimo():
    """Arquivo mais recente gravado pela sessão com resultado de ferramenta."""
    import glob
    fs = glob.glob("/tmp/claude-tool-results/**/*", recursive=True)
    return max((f for f in fs if os.path.isfile(f)), key=os.path.getmtime)


def ler(arq):
    if arq == "ultimo":
        arq = ultimo()
    s = open(arq, encoding="utf-8").read()
    if s.lstrip().startswith("["):
        v, _ = json.JSONDecoder().raw_decode(s.lstrip())
        s = "\n".join(b.get("text", "") for b in v if isinstance(b, dict))
    return s


def cmd_prox():
    fs, fe = fila(), feitos()
    pend = [f for f in fs if f["numero"] not in fe]
    ok = {g: sum(1 for f in fs if f["grupo"] == g and fe.get(f["numero"], {}).get("status") == "ok") for g in ("1", "2")}
    tot = {g: sum(1 for f in fs if f["grupo"] == g) for g in ("1", "2")}
    if not pend:
        print("FIM", ok)
        return
    p = pend[0]
    print(p["numero"], "grupo", p["grupo"], "ordem", p["ordem"], "| ok g1 %d/%d, g2 %d/%d | tratados %d" %
          (ok["1"], tot["1"], ok["2"], tot["2"], len(fe)))


def cmd_sel(num, specs):
    pecas = []
    for s in specs:
        papel, _, resto = s.partition(":")
        assert papel in ("den", "sent", "cand"), s
        uid, nome, data, chars = (resto.split("|") + ["", "", ""])[:4]
        assert re.fullmatch(c.RE_UUID, uid), uid
        pecas.append({"papel": papel, "id": uid, "nome": nome, "data": data, "chars": int(chars or 0)})
    json.dump({"numero": num, "pecas": pecas}, open(CUR, "w"))
    # acima de ~100 mil caracteres o resultado vai a arquivo sem prévia; de ~50 a 100 mil, a arquivo com prévia
    # de 2 KB; abaixo, entra inteiro no contexto. Tamanho desconhecido (sentença vinda do movimento): 30 IDs.
    if any(not p["chars"] for p in pecas):
        tot, rep = 0, max(1, 30 // len(pecas))
    else:
        tot = sum(p["chars"] for p in pecas)
        rep = max(1, min(50 // len(pecas), -(-115000 // max(tot, 1))))
    print(num, len(pecas), "peças", tot, "chars, rep", rep, file=sys.stderr)
    print(json.dumps([p["id"] for p in pecas] * rep))


def e_denuncia(texto):
    cab = texto[:4000]
    return bool(RE_DEN.search(cab)) and not RE_NAO_DEN.search(cab[:700])


def cmd_grava(arq, chamadas, extra=""):
    cur = json.load(open(CUR))
    num = cur["numero"]
    textos = c.separa_lote(ler(arq))
    n = {"den": 0, "sent": 0}
    notas, cap, disp = [], "", ""
    cands = [p for p in cur["pecas"] if p["papel"] == "cand"]
    tem_den = any(p["papel"] == "den" for p in cur["pecas"])
    for p in cur["pecas"]:
        corpo = textos.get(p["id"])
        if not corpo or len(corpo.strip()) < 40:
            notas.append("sem texto: %s %s" % (p["papel"], p["id"]))
            continue
        assert "?t=" not in corpo and "Original:" not in corpo
        papel = p["papel"]
        if papel == "cand":
            if tem_den or not e_denuncia(corpo):
                continue
            papel = "den"
            tem_den = True
            notas.append("denúncia juntada como " + (p["nome"] or "petição"))
        n[papel] += 1
        d = os.path.join(DIR[papel], num)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "%02d_%s.txt" % (n[papel], p["id"])), "w", encoding="utf-8").write(corpo)
        c.anexar(MANIFESTO, CAMPOS_MANIFESTO, dict(
            numero=num, papel="denuncia" if papel == "den" else "sentenca", documento_id=p["id"], parte=n[papel],
            nome=p["nome"], data=p["data"], procedencia=c.procedencia(corpo), chars=len(corpo),
            sha256=hashlib.sha256(corpo.encode()).hexdigest(), lido_em=c.agora()))
        plano = corpo.replace("\n", " ")
        if papel == "den":
            m = (re.findall(r"(?:incurs\w*|viol\w+ (?:as )?disposi\w+|capitula\w*|pr[áa]tica d[oa]s? (?:crimes?|delitos?)|"
                            r"pela pr[áa]tica d[oa]s?)[^.;]{0,40}art[^;]{0,150}", plano, re.I)
                 or re.findall(r"art\.?\s?\d{3}[^;]{0,120}(?:C[óo]digo Penal|CPB?\b)", plano, re.I))
            cap = cap or (re.sub(r"\s+", " ", m[0])[:170] if m else "capitulação não localizada")
        else:
            m = re.findall(r"(?:condeno|conden[áa]-l[oa]s?|absolvo|absolv[êe]-l[oa]s?|julg\w+\s+(?:parcialmente\s+)?"
                           r"(?:im)?procedente|extin\w+ a punibilidade)[^.]{0,140}", plano, re.I)
            disp = re.sub(r"\s+", " ", m[-1])[:150] if m else "dispositivo não localizado"
    if cands and not n["den"]:
        notas.append("nenhuma das %d candidatas era denúncia" % len(cands))
    st = "ok" if n["den"] else ("so_sentenca" if n["sent"] else "sem_texto")
    status(num, st, n["den"], n["sent"], chamadas, "; ".join([x for x in [extra] + notas if x]))
    print("gravado", num, st, "| den", n["den"], "sent", n["sent"], "|", cap or "-", "|", disp or "-")


RE_MAPA = re.compile(r"\[(\d+)\] (\d{4}-\d{2}-\d{2}) \| ([^|\n]+?) \| ([^\n]*)\n\s+ID: (" + c.RE_UUID +
                     r") \| PJe: (\S+)(?:\n\s+Mov: ([^\n]*))?")


def cmd_mapa(arq):
    """Mapa grande (gravado em arquivo): imprime só denúncia, sentença, recebimento e candidatas."""
    s = ler(arq)
    vis, ent = set(), []
    for m in RE_MAPA.finditer(s):
        o, data, nome, resto, uid, pje, mov = m.groups()
        ch = re.search(r"(\d+) chars", resto)
        ch = int(ch.group(1)) if ch else 0
        chave = (nome, ch)
        if uid in {e["id"] for e in ent}:
            continue
        e = {"o": int(o), "data": data, "nome": nome.strip(), "chars": ch, "id": uid, "pje": pje, "mov": mov or "",
             "sem_texto": "sem texto" in resto, "dup": chave in vis}
        vis.add(chave)
        ent.append(e)
    fmt = lambda e: "%s:%s|%s|%s|%d%s%s" % (e["papel"], e["id"], e["nome"][:60], e["data"], e["chars"],
                                             " SEM_TEXTO" if e["sem_texto"] else "", " (dup)" if e["dup"] else "")
    rec = sorted({e["data"] for e in ent if "Recebida a den" in e["mov"]})
    print("recebimento da denúncia:", ", ".join(rec) or "não aparece no mapa")
    for e in ent:
        if re.search(r"den[úu]ncia", e["nome"], re.I) and not re.search(r"recebi|rejei", e["nome"], re.I) and not e["dup"]:
            e["papel"] = "den"
            print(fmt(e))
    for e in ent:
        if re.match(r"senten[çc]a", e["nome"], re.I) and not e["dup"]:
            e["papel"] = "sent"
            print(fmt(e))
    if rec:
        r0 = rec[0]
        cs = [e for e in ent if e["data"] <= r0 and re.search(r"peti|manifesta|cota|parecer|outros", e["nome"], re.I)
              and e["chars"] >= 1000 and not e["dup"] and not re.search(r"den[úu]ncia", e["nome"], re.I)]
        for e in sorted(cs, key=lambda e: e["data"], reverse=True)[:6]:
            e["papel"] = "cand"
            print(fmt(e))
    print("documentos no mapa:", len(ent))


def cmd_resumo():
    fs, fe = fila(), feitos()
    por = {}
    for f in fs:
        st = fe.get(f["numero"], {}).get("status", "pendente")
        por.setdefault(f["grupo"], {}).setdefault(st, 0)
        por[f["grupo"]][st] += 1
    print(json.dumps(por, ensure_ascii=False), "| chamadas registradas:",
          sum(int(s["chamadas"] or 0) for s in fe.values()))


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    if a[0] == "prox":
        cmd_prox()
    elif a[0] == "sel":
        cmd_sel(a[1], a[2:])
    elif a[0] == "grava":
        cmd_grava(a[1], int(a[2]) if len(a) > 2 else 0, a[3] if len(a) > 3 else "")
    elif a[0] == "status":
        status(a[1], a[2], 0, 0, int(a[4]) if len(a) > 4 else 0, a[3] if len(a) > 3 else "")
        print("status", a[1], a[2])
    elif a[0] == "resumo":
        cmd_resumo()
    elif a[0] == "mapa":
        cmd_mapa(a[1])
    elif a[0] == "teste":
        assert e_denuncia("MINISTÉRIO PÚBLICO ... vem oferecer DENÚNCIA contra: FULANO")
        assert e_denuncia("O Ministério Público ... vem, perante V. Exa., oferecer a presente DENÚNCIA em face de")
        assert not e_denuncia("RESPOSTA À ACUSAÇÃO. O réu, nos autos da denúncia oferecida, vem apresentar")
        assert not e_denuncia("Requer a juntada de procuração e habilitação nos autos.")
        print("ok")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
