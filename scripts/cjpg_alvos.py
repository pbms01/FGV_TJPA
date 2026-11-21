#!/usr/bin/env python3
"""Números-alvo do TJSP pela Consulta de Julgados de 1º Grau (cjpg), sem DataJud.

Por que o cjpg (decisão de 20/11/2026, ver docs/RUNBOOK_TJSP.md):
  - O DataJud ficou saturado de 19 a 20/11/2026.
  - O piloto mostrou que o assunto TPU não serve de porta de entrada no TJSP:
    com filtro de ação penal, o assunto 15623 (código interno 5397 no cjpg)
    devolve 0 julgados e o 11978 (interno 3719) devolve 2, enquanto a busca
    textual devolve 1.702 ("fraude eletrônica") e 80 ("invasão de dispositivo
    informático"). As denúncias por art. 171, § 2º-A vêm cadastradas como
    Estelionato (3431). O 15755 nem existe na árvore de assuntos do cjpg.

O que o script faz:
  1. Abre a página do cjpg para obter a sessão (o servidor guarda a consulta na
     sessão e a paginação é GET /cjpg/trocarDePagina.do?pagina=N, o mesmo que o
     botão da página faz).
  2. Para cada consulta, percorre todas as páginas (10 resultados cada), com
     pausa fixa entre requisições.
  3. De cada resultado extrai metadados e, do inteiro teor da sentença que a
     própria listagem já traz oculto, calcula indicadores de precisão e um
     recorte da imputação. O texto integral só é gravado com --texto.
  4. Consolida por número em alvos_cjpg_tjsp.csv.

Limites conhecidos:
  - Só entra processo com sentença publicada no 1º grau; ficam fora feitos em
    curso e em segredo de justiça. É outro universo, não o das denúncias
    ajuizadas.
  - O índice quebra o número do artigo ("154-A" casa "pág. 154"); por isso as
    consultas usam o nome do tipo e expressões da narrativa.
  - O operador NÃO não excluiu a frase no piloto; a consulta ampliada da fraude
    eletrônica se sobrepõe à principal e a deduplicação é feita aqui.

Conduta de acesso: ritmo baixo (--pausa, padrão 3 s), um único fluxo, sem
disfarce de navegador. Se a página pedir CAPTCHA ou devolver erro repetido, o
script para e registra o motivo; não há tentativa de contornar barreira.

Uso:
  python scripts/cjpg_alvos.py                 # todas as consultas
  python scripts/cjpg_alvos.py --so FE INV     # só algumas
  python scripts/cjpg_alvos.py --max-paginas 3 # piloto
  python scripts/cjpg_alvos.py --texto         # grava também o inteiro teor
  python scripts/cjpg_alvos.py --teste FIXTURE # só testa o parser num HTML salvo

Só biblioteca padrão.
"""
import argparse
import csv
import html
import http.cookiejar
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone

BASE = "https://esaj.tjsp.jus.br/cjpg/"

# Classes no código interno do cjpg. A cadeia de cada nó traz o código TPU:
# 8657 = 283 Ação Penal - Procedimento Ordinário; 8803 = 10943 Sumário;
# 8804 = 10944 Sumaríssimo (a invasão anterior à Lei 14.155/2021 era de menor
# potencial ofensivo).
CLASSES_ACAO_PENAL = "8657,8803,8804"

CONSULTAS = {
    "FE": '"fraude eletrônica"',
    "FE_amp": '"2º-A" E estelionato',
    "INV": '"invasão de dispositivo informático"',
    "CL": '"conta laranja" OU "contas laranja" OU "contas laranjas" '
          'OU "cessão de conta" OU "cessão de contas"',
}

RE_TOTAL = re.compile(r"Resultados\s+\d+\s+a\s+\d+\s+de\s+(\d+)")
RE_LINHA = re.compile(r'<tr class="fundocinza1">(.*?)(?=<tr class="fundocinza1">|<div class="trocaDePagina"|\Z)', re.S)
RE_NUMERO = re.compile(r'<span class="fonteNegrito">\s*([\d.\-]+)\s*</span>')
RE_CDDOC = re.compile(r'title="Visualizar Inteiro Teor" name="([^"]+)"')
RE_CAMPO = re.compile(r"<strong>\s*([^<:]{2,40}):\s*</strong>\s*([^<]*)")
RE_DIV = re.compile(r'<div align="justify"[^>]*>(.*?)</div>', re.S)
RE_TAG = re.compile(r"<[^>]+>")

# Indicadores sobre o inteiro teor (mesmas regras do piloto no navegador).
IND = {
    "m_171_2A": re.compile(r"171[^.;]{0,25}(§|par\.?|parágrafo)\s*2º?\s*-?\s*A\b", re.I),
    "m_fraude_eletronica": re.compile(r"fraude eletr[ôo]nica", re.I),
    "m_154A": re.compile(r"154\s*-\s*A", re.I),
    "m_laranja": re.compile(r"laranja|cess[ãa]o de conta", re.I),
}
RE_IMPUTACAO = re.compile(r"foi denunciad|foram denunciad|ofereceu den[úu]ncia|denunciou|incurs[oa]s? n", re.I)
RE_CONDENA = re.compile(r"\bcondeno\b|julgo procedente", re.I)
RE_ABSOLVE = re.compile(r"\babsolvo\b|julgo improcedente", re.I)
RE_BARREIRA = re.compile(r"captcha|recaptcha|acesso negado|too many requests", re.I)

CAMPOS = ["numero", "consultas", "classe", "assunto", "comarca", "foro", "vara",
          "data_disponibilizacao", "cd_doc_cjpg", "chars_sentenca", "m_171_2A",
          "m_fraude_eletronica", "m_154A", "m_laranja", "m_imputacao", "condena",
          "absolve", "imputacao"]


RE_TAG_INLINE = re.compile(r"</?(em|strong|span|b|i)\b[^>]*>", re.I)


def texto_limpo(fragmento):
    # marcação inline (o realce <em> dos termos) some sem espaço; o resto vira espaço
    sem_inline = RE_TAG_INLINE.sub("", fragmento)
    return re.sub(r"\s+", " ", html.unescape(RE_TAG.sub(" ", sem_inline))).strip()


def dv_ok(numero):
    """Dígito verificador do número CNJ (Res. CNJ 65/2008, módulo 97)."""
    m = re.fullmatch(r"(\d{7})-(\d{2})\.(\d{4})\.(\d)\.(\d{2})\.(\d{4})", numero or "")
    if not m:
        return False
    n, d, a, j, t, o = m.groups()
    return 98 - (int(n + a + j + t + o) * 100) % 97 == int(d)


def parse_pagina(pagina_html):
    """Devolve (total, linhas). Cada linha traz metadados, indicadores e o texto."""
    plano = texto_limpo(pagina_html)
    m = RE_TOTAL.search(plano)
    total = int(m.group(1)) if m else 0
    linhas = []
    for bloco in RE_LINHA.findall(pagina_html):
        num = RE_NUMERO.search(bloco)
        if not num:
            continue
        campos = {k.strip(): html.unescape(v).strip() for k, v in RE_CAMPO.findall(bloco)}
        divs = [texto_limpo(x) for x in RE_DIV.findall(bloco)]
        inteiro = max(divs, key=len) if divs else ""   # o oculto é o integral
        i = RE_IMPUTACAO.search(inteiro)
        fim = inteiro[-4000:]
        cd = RE_CDDOC.search(bloco)
        linha = {
            "numero": num.group(1),
            "classe": campos.get("Classe", ""),
            "assunto": campos.get("Assunto", ""),
            "comarca": campos.get("Comarca", ""),
            "foro": campos.get("Foro", ""),
            "vara": campos.get("Vara", ""),
            "data_disponibilizacao": campos.get("Data de Disponibilização", ""),
            "cd_doc_cjpg": cd.group(1) if cd else "",
            "chars_sentenca": len(inteiro),
            "m_imputacao": bool(i),
            "condena": bool(RE_CONDENA.search(fim)),
            "absolve": bool(RE_ABSOLVE.search(fim)),
            "imputacao": inteiro[i.start():i.start() + 420] if i else "",
            "_texto": inteiro,
        }
        for k, rx in IND.items():
            linha[k] = bool(rx.search(inteiro))
        linhas.append(linha)
    return total, linhas


class Sessao:
    def __init__(self, pausa, tentativas=3):
        self.pausa = pausa
        self.tentativas = tentativas
        self.op = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))

    def get(self, url):
        ultimo = None
        for k in range(self.tentativas):
            try:
                with self.op.open(url, timeout=120) as r:
                    corpo = r.read().decode("utf-8", "replace")
                if RE_BARREIRA.search(corpo[:20000]) and "fundocinza1" not in corpo:
                    raise RuntimeError("barreira de acesso na resposta; coleta interrompida")
                return corpo
            except RuntimeError:
                raise
            except Exception as e:  # rede ou 5xx: espera e repete
                ultimo = e
                time.sleep(self.pausa * (k + 2))
        raise RuntimeError(f"falha repetida em {url}: {ultimo}")

    def abrir(self):
        self.get(BASE)

    def pesquisar(self, livre, classes=CLASSES_ACAO_PENAL, assuntos=""):
        p = {"dadosConsulta.pesquisaLivre": livre, "tipoNumero": "UNIFICADO",
             "classeTreeSelection.values": classes,
             "assuntoTreeSelection.values": assuntos,
             "dadosConsulta.ordenacao": "DESC"}
        return self.get(BASE + "pesquisar.do?" + urllib.parse.urlencode(p))

    def pagina(self, n):
        return self.get(BASE + "trocarDePagina.do?pagina=%d" % n)


def coleta(rotulo, livre, s, saida, max_paginas, gravar_texto, log):
    """Percorre uma consulta e grava uma linha JSON por resultado (retomável)."""
    feitas_path = os.path.join(saida, rotulo + ".feitas")
    feitas = set()
    if os.path.exists(feitas_path):
        feitas = {int(x) for x in open(feitas_path).read().split()}
    jl = open(os.path.join(saida, rotulo + ".jsonl"), "a", encoding="utf-8")
    pf = open(feitas_path, "a")

    total, linhas = parse_pagina(s.pesquisar(livre))
    paginas = (total + 9) // 10
    if max_paginas:
        paginas = min(paginas, max_paginas)
    log({"consulta": rotulo, "pesquisa_livre": livre, "total": total, "paginas": paginas})

    for n in range(1, paginas + 1):
        if n in feitas:
            continue
        if n > 1:
            time.sleep(s.pausa)
            _, linhas = parse_pagina(s.pagina(n))
            if not linhas:  # sessão perdida: refaz a consulta uma vez e tenta de novo
                time.sleep(s.pausa)
                s.pesquisar(livre)
                time.sleep(s.pausa)
                _, linhas = parse_pagina(s.pagina(n))
        if not linhas:
            log({"consulta": rotulo, "pagina": n, "erro": "pagina vazia"})
            continue
        for x in linhas:
            texto = x.pop("_texto")
            x.update(consulta=rotulo, pagina=n, coletado=datetime.now(timezone.utc).isoformat(timespec="seconds"))
            if gravar_texto and texto:
                dirt = os.path.join("textos", "tjsp", "sentencas_cjpg")
                os.makedirs(dirt, exist_ok=True)
                nome = x["numero"] + "__" + re.sub(r"[^\w\-]", "_", x["cd_doc_cjpg"]) + ".txt"
                with open(os.path.join(dirt, nome), "w", encoding="utf-8") as f:
                    f.write(texto)
            jl.write(json.dumps(x, ensure_ascii=False) + "\n")
        jl.flush()
        pf.write("%d\n" % n)
        pf.flush()
    jl.close()
    pf.close()


def consolida(saida, destino):
    por_num = {}
    for arq in sorted(os.listdir(saida)):
        if not arq.endswith(".jsonl"):
            continue
        for ln in open(os.path.join(saida, arq), encoding="utf-8"):
            x = json.loads(ln)
            r = por_num.setdefault(x["numero"], dict(x, consultas=set()))
            r["consultas"].add(x["consulta"])
            for k in IND:
                r[k] = r[k] or x[k]
    with open(destino, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS + ["dv_ok"], extrasaction="ignore")
        w.writeheader()
        def data_iso(r):  # dd/mm/aaaa -> aaaammdd, para ordenar do mais recente
            d = r["data_disponibilizacao"].split("/")
            return "".join(reversed(d)) if len(d) == 3 else ""
        for num, r in sorted(por_num.items(), key=lambda kv: data_iso(kv[1]), reverse=True):
            r = dict(r, consultas="|".join(sorted(r["consultas"])), dv_ok=dv_ok(num))
            w.writerow(r)
    return len(por_num)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--so", nargs="*", choices=list(CONSULTAS), help="rodar só estas consultas")
    ap.add_argument("--max-paginas", type=int, default=0, help="limite de páginas por consulta (0 = todas)")
    ap.add_argument("--pausa", type=float, default=3.0, help="segundos entre requisições")
    ap.add_argument("--saida", default=os.path.join("dados", "cjpg", "bruto"))
    ap.add_argument("--destino", default="alvos_cjpg_tjsp.csv")
    ap.add_argument("--texto", action="store_true", help="grava o inteiro teor de cada sentença em textos/tjsp/sentencas_cjpg/")
    ap.add_argument("--teste", metavar="HTML", help="só aplica o parser a um HTML salvo e imprime o resultado")
    a = ap.parse_args()

    if a.teste:
        total, linhas = parse_pagina(open(a.teste, encoding="utf-8").read())
        for x in linhas:
            x["_texto"] = len(x["_texto"])
        print(json.dumps({"total": total, "linhas": linhas}, ensure_ascii=False, indent=1))
        return

    os.makedirs(a.saida, exist_ok=True)
    logf = open(os.path.join(a.saida, "log.jsonl"), "a", encoding="utf-8")

    def log(ev):
        ev["t"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        logf.write(json.dumps(ev, ensure_ascii=False) + "\n")
        logf.flush()
        print(ev, file=sys.stderr)

    s = Sessao(a.pausa)
    s.abrir()
    for rot in (a.so or list(CONSULTAS)):
        try:
            coleta(rot, CONSULTAS[rot], s, a.saida, a.max_paginas, a.texto, log)
        except RuntimeError as e:
            log({"consulta": rot, "parada": str(e)})
            break
        time.sleep(a.pausa)
    n = consolida(a.saida, a.destino)
    log({"consolidado": a.destino, "numeros": n})


if __name__ == "__main__":
    main()
