#!/usr/bin/env python3
"""Números-alvo pela API pública do DJEN, para tribunais sem consulta de sentenças de 1º grau.

Por que o DJEN (sondagem de 21/11/2026, ver docs/RUNBOOK_TJPA.md):
  - O TJPA não tem o equivalente ao cjpg do TJSP. O Banco de Jurisprudência
    (jurisprudencia.tjpa.jus.br) indexa só acórdãos e decisões monocráticas.
  - A API que alimenta o comunica.pje.jus.br faz busca textual por tribunal e
    período e devolve o inteiro teor de cada ato publicado, com classe, tipo de
    documento e órgão. No TJPA a apelação mantém o número de origem.

Semântica medida:
  - Cada consulta é UMA frase: aspas são indiferentes e várias palavras formam a
    frase, não a interseção. Não há OU nem E; cada variante é uma consulta, e a
    união se faz pelo id da publicação.
  - Não há filtro de classe na API; o filtro é aplicado aqui pelo codigoClasse.
  - O número do artigo sozinho não serve ("154-A" devolve 340 publicações no TJPA).

O que o script grava:
  dados/djen/bruto/<TRIB>_<rotulo>.jsonl   uma linha por publicação e frase: metadados e
                                           indicadores, sem nomes de partes ou advogados
  dados/djen/alvos_djen_<trib>.csv          uma linha por processo das classes-alvo
  dados/djen/totais_<trib>.json             totais por frase, rótulo e classe
  textos/<trib>/djen/<id>.txt               inteiro teor, só com --texto

Limites conhecidos:
  - Só entra o que foi publicado no DJEN. Processo em que só MP e Defensoria são
    intimados pelo sistema pode não ter publicação nenhuma; medir a cobertura
    contra o DataJud ou o Codex antes de tratar a lista como censo.
  - Do workspace da sessão a API devolve 403 (CloudFront); rode no seu computador
    ou use scripts/djen_navegador.js numa aba do comunica.pje.jus.br.

Conduta de acesso: um único fluxo, pausa fixa (--pausa, padrão 1,5 s), sem
disfarce de navegador. Em 403 o script para e registra; em 429 ou 5xx espera e
tenta no máximo três vezes.

Uso:
  python scripts/djen_alvos.py                         # TJPA, 2020-01-01 até hoje
  python scripts/djen_alvos.py --so FE INV             # só alguns rótulos
  python scripts/djen_alvos.py --fim 2026-11-20        # janela fixa (a da sondagem)
  python scripts/djen_alvos.py --texto                 # grava também o inteiro teor
  python scripts/djen_alvos.py --controle estelionato  # série de cobertura por ano
  python scripts/djen_alvos.py --teste                 # testa sem rede, com a fixture

Só biblioteca padrão.
"""
import argparse
import csv
import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from datetime import date

API = "https://comunicaapi.pje.jus.br/api/v1/comunicacao"
POR_PAGINA = 100

CONSULTAS = {
    "FE": ["fraude eletrônica"],
    "FE_amp": ["171, § 2º-A", "art. 171, § 2º-A"],
    "INV": ["invasão de dispositivo informático"],
    "CL": ["conta laranja", "contas laranja", "contas laranjas", "cessão de conta", "cessão de contas"],
    "EE": ["estelionato eletrônico"],
}

# Classes que entram na lista de alvos. O habeas corpus (307) fica fora: tem
# número próprio de 2º grau.
CLASSES = {"283": "AP", "10943": "AP", "10944": "AP", "417": "APEL", "279": "IP", "280": "APF"}

CAMPOS_CSV = ["numero", "acao_penal", "apelacao", "inquerito", "flagrante", "data_sentenca_djen",
              "primeira_pub", "ultima_pub", "consultas", "m_fraude_eletronica", "m_171_2A", "m_154A",
              "m_laranja", "n_pubs", "n_pubs_sem_advogado", "orgao_1g"]


def norm(s):
    s = unicodedata.normalize("NFD", s or "")
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def indicadores(texto, tipo_doc):
    t = norm(texto)
    fim = t[-4000:]
    return {
        "m_fraude_eletronica": bool(re.search(r"fraude eletronica", t)),
        "m_171_2A": bool(re.search(r"171[^.;]{0,40}2[ºo°]?\s*-\s*a\b", t)),
        "m_154A": bool(re.search(r"154\s*-\s*a\b", t)),
        "m_laranja": bool(re.search(r"laranja|cessao de conta", t)),
        "sentenca": tipo_doc == "Sentença" or bool(
            re.search(r"(condeno|absolvo|julgo (parcialmente )?procedente|julgo improcedente)", t)
            and re.search(r"dispositivo|ante o exposto|isto posto|diante do exposto", t)),
        "condena": bool(re.search(r"\bcondeno\b|julgo (parcialmente )?procedente", fim)),
        "absolve": bool(re.search(r"\babsolvo\b|julgo improcedente", fim)),
    }


def registro(item):
    """Metadados e indicadores de uma publicação; nomes de pessoas não entram."""
    r = {
        "id": item["id"],
        "numero": item.get("numeroprocessocommascara") or item.get("numero_processo"),
        "data": item.get("data_disponibilizacao"),
        "codigoClasse": str(item.get("codigoClasse")),
        "nomeClasse": item.get("nomeClasse"),
        "tipoDocumento": item.get("tipoDocumento"),
        "tipoComunicacao": item.get("tipoComunicacao"),
        "orgao": item.get("nomeOrgao"),
        "n_advogados": len(item.get("destinatarioadvogados") or []),
        "chars": len(item.get("texto") or ""),
    }
    r.update(indicadores(item.get("texto"), item.get("tipoDocumento")))
    return r


class Cliente:
    def __init__(self, tribunal, inicio, fim, pausa):
        self.tribunal, self.inicio, self.fim, self.pausa = tribunal, inicio, fim, pausa

    def url(self, frase, pagina, por_pagina=POR_PAGINA, inicio=None, fim=None):
        q = {"texto": frase, "siglaTribunal": self.tribunal,
             "dataDisponibilizacaoInicio": inicio or self.inicio,
             "dataDisponibilizacaoFim": fim or self.fim,
             "pagina": pagina, "itensPorPagina": por_pagina}
        return API + "?" + urllib.parse.urlencode(q, quote_via=urllib.parse.quote)

    def get(self, url):
        for tentativa in range(3):
            req = urllib.request.Request(url, headers={"Accept": "application/json"})
            try:
                with urllib.request.urlopen(req, timeout=60) as r:
                    dados = json.loads(r.read().decode("utf-8"))
                time.sleep(self.pausa)
                return dados
            except urllib.error.HTTPError as e:
                if e.code == 403:
                    sys.exit("403: a API recusou esta origem (no workspace da sessão isso é esperado); "
                             "rode no seu computador ou use scripts/djen_navegador.js")
                if e.code == 429 or e.code >= 500:
                    time.sleep(30 * (tentativa + 1))
                    continue
                raise
        sys.exit("falha repetida em " + url)

    def todas(self, frase):
        pagina, itens, total = 1, [], None
        while True:
            j = self.get(self.url(frase, pagina))
            total = j.get("count", 0) if total is None else total
            lote = j.get("items") or []
            itens += lote
            if len(lote) < POR_PAGINA or len(itens) >= total:
                return total, itens
            pagina += 1


def consolida(publicacoes):
    """publicacoes: {id: registro com 'rotulos'} -> lista de processos das classes-alvo."""
    P = {}
    for x in publicacoes.values():
        tipo = CLASSES.get(x["codigoClasse"])
        if not tipo:
            continue
        p = P.setdefault(x["numero"], {
            "numero": x["numero"], "AP": 0, "APEL": 0, "IP": 0, "APF": 0, "data_sentenca": "",
            "primeira_pub": x["data"], "ultima_pub": x["data"], "consultas": set(),
            "m_fraude_eletronica": 0, "m_171_2A": 0, "m_154A": 0, "m_laranja": 0,
            "n_pubs": 0, "n_pubs_sem_advogado": 0, "orgao_1g": ""})
        p[tipo] = 1
        p["n_pubs"] += 1
        p["n_pubs_sem_advogado"] += not x["n_advogados"]
        p["consultas"].update(x["rotulos"])
        p["primeira_pub"] = min(p["primeira_pub"], x["data"])
        p["ultima_pub"] = max(p["ultima_pub"], x["data"])
        for m in ("m_fraude_eletronica", "m_171_2A", "m_154A", "m_laranja"):
            if x[m]:
                p[m] = 1
        if tipo != "APEL" and not p["orgao_1g"]:
            p["orgao_1g"] = x["orgao"] or ""
        if tipo == "AP" and x["sentenca"] and x["data"] > p["data_sentenca"]:
            p["data_sentenca"] = x["data"]
    return [P[n] for n in sorted(P)]


def linha_csv(p):
    return {"numero": p["numero"], "acao_penal": p["AP"], "apelacao": p["APEL"], "inquerito": p["IP"],
            "flagrante": p["APF"], "data_sentenca_djen": p["data_sentenca"],
            "primeira_pub": p["primeira_pub"], "ultima_pub": p["ultima_pub"],
            "consultas": "+".join(sorted(p["consultas"])), "m_fraude_eletronica": p["m_fraude_eletronica"],
            "m_171_2A": p["m_171_2A"], "m_154A": p["m_154A"], "m_laranja": p["m_laranja"],
            "n_pubs": p["n_pubs"], "n_pubs_sem_advogado": p["n_pubs_sem_advogado"], "orgao_1g": p["orgao_1g"]}


def totais(publicacoes, frases, processos, parametros):
    por_rotulo = {}
    for x in publicacoes.values():
        tipo = CLASSES.get(x["codigoClasse"])
        for r in x["rotulos"]:
            o = por_rotulo.setdefault(r, {"publicacoes": 0, "AP": set(), "sentenca": set(), "APEL": set()})
            o["publicacoes"] += 1
            if tipo == "AP":
                o["AP"].add(x["numero"])
                if x["sentenca"]:
                    o["sentenca"].add(x["numero"])
            if tipo == "APEL":
                o["APEL"].add(x["numero"])
    por_classe = {}
    for x in publicacoes.values():
        por_classe.setdefault("%s %s" % (x["codigoClasse"], x["nomeClasse"]), set()).add(x["numero"])
    ps = processos
    return {
        "parametros": parametros, "frases": frases,
        "por_rotulo": {r: {"publicacoes": o["publicacoes"], "acoes_penais": len(o["AP"]),
                           "com_sentenca": len(o["sentenca"]), "apelacoes": len(o["APEL"])}
                       for r, o in por_rotulo.items()},
        "publicacoes_distintas": len(publicacoes),
        "processos_por_classe": {k: len(v) for k, v in sorted(por_classe.items())},
        "alvos": {
            "processos": len(ps), "acao_penal": sum(p["AP"] for p in ps), "apelacao": sum(p["APEL"] for p in ps),
            "acao_penal_ou_apelacao": sum(1 for p in ps if p["AP"] or p["APEL"]),
            "so_apelacao": sum(1 for p in ps if p["APEL"] and not p["AP"]),
            "com_sentenca_djen": sum(1 for p in ps if p["data_sentenca"]),
            "sentenca_ou_apelacao": sum(1 for p in ps if p["data_sentenca"] or p["APEL"]),
            "inquerito": sum(p["IP"] for p in ps), "flagrante": sum(p["APF"] for p in ps)},
    }


def grava(processos, tot, tribunal, pasta):
    os.makedirs(pasta, exist_ok=True)
    trib = tribunal.lower()
    with open(os.path.join(pasta, "alvos_djen_%s.csv" % trib), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS_CSV)
        w.writeheader()
        for p in processos:
            w.writerow(linha_csv(p))
    with open(os.path.join(pasta, "totais_%s.json" % trib), "w", encoding="utf-8") as f:
        json.dump(tot, f, ensure_ascii=False, indent=1)


def coleta(cli, rotulos, guardar_texto, pasta):
    publicacoes, frases = {}, {}
    os.makedirs(os.path.join(pasta, "bruto"), exist_ok=True)
    for rotulo in rotulos:
        caminho = os.path.join(pasta, "bruto", "%s_%s.jsonl" % (cli.tribunal, rotulo))
        with open(caminho, "w", encoding="utf-8") as f:
            for frase in CONSULTAS[rotulo]:
                total, itens = cli.todas(frase)
                frases[frase] = {"rotulo": rotulo, "publicacoes": total}
                print("%s | %s: %d publicações" % (rotulo, frase, total), file=sys.stderr)
                for it in itens:
                    r = publicacoes.get(it["id"])
                    if r is None:
                        r = registro(it)
                        r["rotulos"] = []
                        publicacoes[it["id"]] = r
                        if guardar_texto:
                            d = os.path.join("textos", cli.tribunal.lower(), "djen")
                            os.makedirs(d, exist_ok=True)
                            with open(os.path.join(d, "%s.txt" % it["id"]), "w", encoding="utf-8") as g:
                                g.write(it.get("texto") or "")
                    if rotulo not in r["rotulos"]:
                        r["rotulos"].append(rotulo)
                    f.write(json.dumps(dict(r, frase=frase), ensure_ascii=False) + "\n")
    return publicacoes, frases


def controle(cli, termo, anos):
    out = {}
    for a in anos:
        fim = cli.fim if a == cli.fim[:4] else a + "-12-31"
        out[a] = cli.get(cli.url(termo, 1, por_pagina=1, inicio=a + "-01-01", fim=fim)).get("count")
    return out


def testes():
    fixture = os.path.join(os.path.dirname(__file__), "testes", "djen_fixture.json")
    j = json.load(open(fixture, encoding="utf-8"))
    publicacoes = {}
    for rotulo, its in (("FE", j["items"]), ("FE_amp", j["items"][:1])):
        for it in its:
            r = publicacoes.setdefault(it["id"], dict(registro(it), rotulos=[]))
            if rotulo not in r["rotulos"]:
                r["rotulos"].append(rotulo)
    ps = consolida(publicacoes)
    por = {p["numero"]: p for p in ps}
    assert len(ps) == 2, [p["numero"] for p in ps]                 # o HC fica fora
    ap = por["0800001-11.2024.8.14.0401"]
    assert ap["AP"] == 1 and ap["APEL"] == 1 and ap["data_sentenca"] == "2026-03-10", ap
    assert ap["m_171_2A"] == 1 and ap["consultas"] == {"FE", "FE_amp"} and ap["n_pubs_sem_advogado"] == 1, ap
    assert ap["orgao_1g"] == "1ª Vara Criminal de Belém", ap
    ip = por["0800002-22.2025.8.14.0006"]
    assert ip["IP"] == 1 and ip["data_sentenca"] == "", ip
    saida = json.dumps([linha_csv(p) for p in ps], ensure_ascii=False) + json.dumps(list(publicacoes.values()), ensure_ascii=False)
    assert "FULANO" not in saida and "BELTRANO" not in saida, "nome de pessoa vazou"
    tot = totais(publicacoes, {}, ps, {})
    assert tot["alvos"]["sentenca_ou_apelacao"] == 1 and tot["alvos"]["inquerito"] == 1, tot["alvos"]
    print("ok: %d publicações, %d processos, sem nomes de pessoas" % (len(publicacoes), len(ps)))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tribunal", default="TJPA")
    ap.add_argument("--inicio", default="2020-01-01")
    ap.add_argument("--fim", default=date.today().isoformat())
    ap.add_argument("--so", nargs="*", choices=list(CONSULTAS))
    ap.add_argument("--pausa", type=float, default=1.5)
    ap.add_argument("--texto", action="store_true")
    ap.add_argument("--controle", metavar="TERMO")
    ap.add_argument("--pasta", default=os.path.join("dados", "djen"))
    ap.add_argument("--teste", action="store_true")
    a = ap.parse_args()
    if a.teste:
        return testes()
    cli = Cliente(a.tribunal, a.inicio, a.fim, a.pausa)
    if a.controle:
        anos = [str(y) for y in range(int(a.inicio[:4]), int(a.fim[:4]) + 1)]
        print(json.dumps(controle(cli, a.controle, anos), ensure_ascii=False))
        return
    rotulos = a.so or list(CONSULTAS)
    publicacoes, frases = coleta(cli, rotulos, a.texto, a.pasta)
    processos = consolida(publicacoes)
    par = {"tribunal": a.tribunal, "inicio": a.inicio, "fim": a.fim, "rotulos": rotulos}
    tot = totais(publicacoes, frases, processos, par)
    grava(processos, tot, a.tribunal, a.pasta)
    print(json.dumps(tot["alvos"], ensure_ascii=False), file=sys.stderr)


if __name__ == "__main__":
    main()
