#!/usr/bin/env python3
"""Lê pelo Codex (TecJustica MCP) a denúncia de cada processo da amostra e grava só o texto.

Roda no seu computador, fora do contexto do modelo, com a sua chave:
    export TECJUSTICA_API_KEY=...          (Windows: set TECJUSTICA_API_KEY=...)
    python scripts/codex_denuncias.py                  # processa a amostra
    python scripts/codex_denuncias.py --simular        # só mostra o plano
    python scripts/codex_denuncias.py --teste          # testa os parsers sem rede

Entrada: dados/cjpg/amostra_tjsp.csv (saída do sorteio, scripts/cjpg_sorteio.js).
Saídas:
    textos/tjsp/denuncias/<numero>/<ordem>_<documento_id>.txt   texto lido, com a linha de procedência
    textos/tjsp/manifesto.csv     numero, estrato, documento_id, parte, nome, procedencia, chars, sha256, lido_em
    dados/codex/status.csv        numero, estrato, status, docs, chamadas_estimadas, quando, detalhe

Rota por processo (medida em 20/11/2026, ver docs/RUNBOOK_TJSP.md):
    1. pdpj_mapa_documentos (1 chamada real)
    2. todas as partes da categoria "Peça Inicial" do 1º grau, numa só
       pdpj_read_documentos_batch (1 chamada real, mais 1 por parte sem texto indexado)
Não usa pdpj_perguntar_processo (30 por dia) nem pdpj_analise_essencial.

Cota (skill do conector): 20 chamadas reais por minuto e 300 por hora por chave;
para uso automatizado, metade. Este script fica abaixo disso: uma chamada a cada
6,5 s (até 9 por minuto) e no máximo 140 chamadas estimadas por hora corrida,
sempre em sequência. Em "aguarde Xs", espera X + 5 s; em limite da fonte, 60 s;
indisponibilidade repetida, para e registra. Nunca repete de imediato.

Cotas da amostra (decisão de 20/11/2026): invasão em censo; conta laranja 50;
fraude eletrônica completa 200 menos o obtido nos outros dois estratos.

O link "Original:" que o Codex devolve traz token de acesso: é descartado antes
de qualquer gravação e nunca vai para arquivo.

Só biblioteca padrão.
"""
import argparse
import csv
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from collections import deque
from datetime import datetime, timezone

ENDPOINT = os.environ.get("TECJUSTICA_MCP_URL", "https://mcp.tecjustica.com/mcp")
TOTAL_ALVO = 200
COTA_CL = 50
INTERVALO = 6.5          # segundos entre chamadas
TETO_HORA = 140          # chamadas reais estimadas por hora corrida

AMOSTRA = os.path.join("dados", "cjpg", "amostra_tjsp.csv")
STATUS = os.path.join("dados", "codex", "status.csv")
MANIFESTO = os.path.join("textos", "tjsp", "manifesto.csv")
DIR_TEXTOS = os.path.join("textos", "tjsp", "denuncias")

RE_UUID = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
RE_ENTRADA = re.compile(
    r"\[(\d+)\]\s+(\d{4}-\d{2}-\d{2})\s+\|\s+([^|\n]+?)\s+\|\s+([^\n]*)\n\s+ID:\s+(" + RE_UUID + r")\s+\|\s+PJe:\s+(\S+)")
RE_ORIGINAL = re.compile(r"^Original:\s+\S+.*$", re.M)
RE_AGUARDE = re.compile(r"limite de consultas.*?aguarde\s+(\d+)\s*s", re.I | re.S)


# ---------------------------------------------------------------- parsers

def pecas_iniciais(mapa):
    """Partes da denúncia (e aditamento) no mapa: categoria 'Peça Inicial', só 1º grau.

    O destaque 'PECA INICIAL (provavel)' pode listar só parte das páginas
    (no piloto, 3 de 5); por isso se usa a categoria inteira.
    """
    m = re.search(r"\nPe[çc]a Inicial \(\d+ docs?\):\n(.*?)(?:\n\n[^\n]+\(\d+ docs?\):|\n\n=== |\Z)", mapa, re.S)
    if not m:
        return []
    vistos, partes = set(), []
    for ordinal, data, nome, resto, uid, pje in RE_ENTRADA.findall(m.group(1) + "\n"):
        if pje.upper().startswith("SG"):          # dossiê de 2º grau
            continue
        chars = re.search(r"(\d+)\s+chars", resto)
        chave = (nome, chars.group(1) if chars else resto)   # cópia redistribuída (PG5REG) duplica a peça
        if chave in vistos and "REG" in pje.upper():
            continue
        vistos.add(chave)
        proto, _, n = pje.rpartition("_")
        partes.append({"ordinal": int(ordinal), "data": data, "nome": nome, "id": uid, "pje": pje,
                       "protocolo": proto, "parte": int(n) if n.isdigit() else 0,
                       "sem_texto": "sem texto indexado" in resto})
    # descarta a cópia REG quando a mesma peça existe no dossiê principal
    principais = {(p["nome"], p["parte"]) for p in partes if "REG" not in p["pje"].upper()}
    partes = [p for p in partes if "REG" not in p["pje"].upper() or (p["nome"], p["parte"]) not in principais]
    partes.sort(key=lambda p: (p["data"], p["protocolo"], p["parte"]))
    return partes


def separa_lote(texto):
    """Divide a saída do lote em {documento_id: texto}, sem a linha Original."""
    docs = {}
    for bloco in re.split(r"\n?--- [^\n]+ ---\n", "\n" + texto)[1:]:
        uid = re.search(r"/doc/[^/\s]+/(" + RE_UUID + r")", bloco)
        if not uid:
            continue
        corpo = RE_ORIGINAL.sub("", bloco)
        corpo = re.sub(r"\n*Ao responder, cite as pecas.*\Z", "", corpo, flags=re.S).strip("\n") + "\n"
        docs[uid.group(1)] = corpo
    return docs


def procedencia(corpo):
    m = re.search(r"\[(Texto nativo[^\]]*|OCR[^\]]*|[^\]]*parser[^\]]*)\]", corpo[:300], re.I)
    return m.group(1) if m else ""


# ---------------------------------------------------------------- cliente MCP

class Codex:
    def __init__(self, chave):
        self.chave = chave
        self.sessao = None
        self.ultimo = 0.0
        self.hora = deque()   # (instante, custo)
        self.n = 0

    def _post(self, corpo):
        h = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream",
             "Authorization": "Bearer " + self.chave}
        if self.sessao:
            h["Mcp-Session-Id"] = self.sessao
        req = urllib.request.Request(ENDPOINT, data=json.dumps(corpo).encode(), headers=h, method="POST")
        with urllib.request.urlopen(req, timeout=180) as r:
            self.sessao = r.headers.get("Mcp-Session-Id") or self.sessao
            bruto = r.read().decode("utf-8", "replace")
            tipo = r.headers.get("Content-Type", "")
        if not bruto.strip():
            return None
        if "text/event-stream" in tipo:
            msgs = [json.loads(l[5:]) for l in bruto.splitlines() if l.startswith("data:") and l[5:].strip()]
            return next((m for m in reversed(msgs) if "id" in m), msgs[-1] if msgs else None)
        return json.loads(bruto)

    def iniciar(self):
        self._post({"jsonrpc": "2.0", "id": 0, "method": "initialize", "params": {
            "protocolVersion": "2025-06-18", "capabilities": {},
            "clientInfo": {"name": "fgv-tjsp-denuncias", "version": "1.0"}}})
        self._post({"jsonrpc": "2.0", "method": "notifications/initialized"})

    def _ritmo(self, custo):
        espera = self.ultimo + INTERVALO - time.time()
        if espera > 0:
            time.sleep(espera)
        agora = time.time()
        while self.hora and agora - self.hora[0][0] > 3600:
            self.hora.popleft()
        while sum(c for _, c in self.hora) + custo > TETO_HORA:
            time.sleep(max(5, 3600 - (agora - self.hora[0][0]) + 1))
            agora = time.time()
            while self.hora and agora - self.hora[0][0] > 3600:
                self.hora.popleft()

    def chamar(self, ferramenta, argumentos, custo=1):
        for tentativa in range(4):
            self._ritmo(custo)
            self.n += 1
            try:
                r = self._post({"jsonrpc": "2.0", "id": self.n, "method": "tools/call",
                                "params": {"name": ferramenta, "arguments": argumentos}})
            except urllib.error.HTTPError as e:
                self.ultimo = time.time()
                if e.code == 429:
                    time.sleep(65)
                    continue
                if e.code >= 500:
                    time.sleep(120 * (tentativa + 1))
                    continue
                raise
            finally:
                self.ultimo = time.time()
            self.hora.append((time.time(), custo))
            if r is None or "error" in r:
                raise RuntimeError("erro MCP: %s" % (r or {}).get("error"))
            texto = "\n".join(c.get("text", "") for c in r["result"].get("content", []) if c.get("type") == "text")
            m = RE_AGUARDE.search(texto)
            if m:
                time.sleep(int(m.group(1)) + 5)
                continue
            if "Rate limit atingido na fonte" in texto:
                time.sleep(60)
                continue
            if "temporariamente indispon" in texto.lower():
                time.sleep(300)
                continue
            return texto
        raise RuntimeError("limite ou indisponibilidade persistente em %s" % ferramenta)


# ---------------------------------------------------------------- fluxo

def ler_csv(caminho):
    if not os.path.exists(caminho):
        return []
    with open(caminho, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def anexar(caminho, campos, linha):
    novo = not os.path.exists(caminho)
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        if novo:
            w.writeheader()
        w.writerow(linha)


def agora():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def processa(cx, alvo):
    numero, estrato = alvo["numero"], alvo["estrato"]
    mapa = cx.chamar("pdpj_mapa_documentos", {"numero_processo": numero})
    if "nao esta disponivel" in mapa.lower() or "sigilo" in mapa.lower()[:400]:
        return "sigilo", 0, 1, ""
    if "Nao foi possivel" in mapa[:200]:
        return "erro", 0, 1, mapa[:200].replace("\n", " ")
    partes = pecas_iniciais(mapa)
    if not partes:
        return "sem_peca_inicial", 0, 1, ""
    custo = 1 + sum(p["sem_texto"] for p in partes)
    lote = cx.chamar("pdpj_read_documentos_batch",
                     {"numero_processo": numero, "documento_ids": [p["id"] for p in partes]}, custo=custo)
    textos = separa_lote(lote)
    gravados = 0
    for k, p in enumerate(partes, 1):
        corpo = textos.get(p["id"])
        if not corpo or len(corpo.strip()) < 40:
            continue
        d = os.path.join(DIR_TEXTOS, numero)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "%02d_%s.txt" % (k, p["id"])), "w", encoding="utf-8") as f:
            f.write(corpo)
        anexar(MANIFESTO, ["numero", "estrato", "documento_id", "parte", "nome", "pje", "data", "procedencia", "chars", "sha256", "lido_em"],
               {"numero": numero, "estrato": estrato, "documento_id": p["id"], "parte": k, "nome": p["nome"],
                "pje": p["pje"], "data": p["data"], "procedencia": procedencia(corpo), "chars": len(corpo),
                "sha256": hashlib.sha256(corpo.encode()).hexdigest(), "lido_em": agora()})
        gravados += 1
    return ("ok" if gravados else "sem_texto"), gravados, 1 + custo, ""


def plano(amostra, feitos):
    """Ordem de trabalho: INV (censo), CL até 50, FE até completar 200."""
    por = {"INV": [], "CL": [], "FE": []}
    for a in sorted(amostra, key=lambda a: int(a.get("ordem_no_estrato") or 0)):
        if a["estrato"] in por:
            por[a["estrato"]].append(a)
    ok = {e: sum(1 for s in feitos.values() if s["estrato"] == e and s["status"] == "ok") for e in por}
    return por, ok


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--simular", action="store_true")
    ap.add_argument("--teste", action="store_true")
    ap.add_argument("--max", type=int, default=0, help="parar depois de N processos nesta execução")
    a = ap.parse_args()

    if a.teste:
        return testes()

    amostra = ler_csv(AMOSTRA)
    feitos = {s["numero"]: s for s in ler_csv(STATUS)}
    por, ok = plano(amostra, feitos)
    print("amostra:", {e: len(v) for e, v in por.items()}, "| já obtidos:", ok, file=sys.stderr)
    if a.simular:
        return

    chave = os.environ.get("TECJUSTICA_API_KEY")
    if not chave:
        sys.exit("defina TECJUSTICA_API_KEY")
    cx = Codex(chave)
    cx.iniciar()
    feitos_agora = 0
    for estrato in ("INV", "CL", "FE"):
        for alvo in por[estrato]:
            cota = None if estrato == "INV" else COTA_CL if estrato == "CL" else TOTAL_ALVO - ok["INV"] - ok["CL"]
            if cota is not None and ok[estrato] >= cota:
                break
            if alvo["numero"] in feitos:
                continue
            try:
                status, docs, custo, detalhe = processa(cx, alvo)
            except RuntimeError as e:
                print("parada:", e, file=sys.stderr)
                return
            linha = {"numero": alvo["numero"], "estrato": estrato, "status": status, "docs": docs,
                     "chamadas_estimadas": custo, "quando": agora(), "detalhe": detalhe}
            anexar(STATUS, list(linha), linha)
            feitos[alvo["numero"]] = linha
            ok[estrato] += status == "ok"
            feitos_agora += 1
            print(estrato, alvo["numero"], status, docs, "| obtidos:", ok, file=sys.stderr)
            if a.max and feitos_agora >= a.max:
                return


def testes():
    mapa = open(os.path.join("scripts", "testes", "codex_mapa_fixture.txt"), encoding="utf-8").read()
    partes = pecas_iniciais(mapa)
    assert [p["parte"] for p in partes] == [1, 2, 3, 4, 5], partes
    assert all(not p["pje"].startswith("SG") for p in partes)
    lote = open(os.path.join("scripts", "testes", "codex_lote_fixture.txt"), encoding="utf-8").read()
    docs = separa_lote(lote)
    assert len(docs) == 2, docs.keys()
    assert all("Original:" not in t and "?t=" not in t for t in docs.values())
    assert procedencia(next(iter(docs.values()))) == "Texto nativo do PJe"
    print("ok:", len(partes), "partes;", len(docs), "documentos no lote; sem links com token")


if __name__ == "__main__":
    main()
