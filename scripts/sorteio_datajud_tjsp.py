#!/usr/bin/env python3
"""Seleciona no DataJud (API pública do CNJ) os números de processo-alvo do TJSP para download posterior.

Recorte: estelionato e crimes informáticos (assuntos TPU 3431, 15623, 11978, 14692, 14693),
1º grau, sigilo 0, inquérito policial (279) e ação penal (283, 10943), por período normativo.
Saída: CSV com um número por linha, pronto para a sessão de download.

Uso:
    python sorteio_datajud_tjsp.py                    # sorteia e grava alvos_tjsp.csv
    python sorteio_datajud_tjsp.py --por-celula 50    # amostra maior
    python sorteio_datajud_tjsp.py --so-consulta      # só imprime as consultas, sem rede

Decisões não óbvias:
- O sorteio é feito no próprio servidor (function_score + random_score com semente), uma consulta
  por célula. Com o cluster do DataJud saturado (19 e 20/11/2026), baixar o universo do TJSP para
  sortear localmente exigiria centenas de pedidos aceitos; aqui bastam seis.
- Pede-se o dobro do necessário por célula para absorver, sem nova consulta, duplicados por número
  e processos de violência doméstica, que saem do recorte por não serem objeto.
- random_score usa o campo _seq_no; se o cluster recusar o campo, cai para dataAjuizamento, que
  também é numérico com doc values. A semente fixa torna o sorteio reproduzível enquanto o índice
  não mudar; por isso a resposta bruta de cada célula é gravada com data e hora.
- Resposta com shard falho é tratada como falha: o Elasticsearch devolve contagem parcial sem erro
  quando parte dos shards rejeita a busca.
- dataAjuizamento é numérico (yyyyMMddHHmmss); data em formato ISO no range não filtra e não dá erro.
- O corte P1/P2 em 23/01/2020 (vigência da Lei 13.964/2019) é provisório, a conferir.
- Fonte obrigatória em qualquer publicação: CNJ, DataJud (Portaria CNJ 160/2020, art. 4º, na
  redação da Portaria 374/2026).
"""
import argparse
import csv
import json
import os
import random
import ssl
import sys
import time
import urllib.error
import urllib.request

CHAVE_PUBLICA = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="  # vigente em 20/11/2026
ASSUNTOS = [3431, 15623, 11978, 14692, 14693]
ETAPAS = {"inquerito": [279], "acao_penal": [283, 10943]}
PERIODOS = [  # (rótulo, início inclusive, fim exclusivo), em yyyyMMddHHmmss
    ("P1", 20190101000000, 20200123000000),  # ação incondicionada, antes da Lei 13.964/2019
    ("P2", 20200123000000, 20210528000000),  # representação exigida, competência antiga
    ("P3", 20210528000000, 20250101000000),  # representação e competência pelo domicílio da vítima (Lei 14.155/2021)
]
CAMPOS = ["numeroProcesso", "classe", "dataAjuizamento", "orgaoJulgador", "assuntos", "grau", "nivelSigilo"]


def consulta(classes, inicio, fim, tamanho, semente, campo_aleatorio):
    return {
        "size": tamanho,
        "track_total_hits": True,
        "_source": CAMPOS,
        "query": {"function_score": {
            "query": {"bool": {"filter": [
                {"terms": {"assuntos.codigo": ASSUNTOS}},
                {"terms": {"classe.codigo": classes}},
                {"term": {"nivelSigilo": 0}},
                {"match": {"grau": "G1"}},
                {"range": {"dataAjuizamento": {"gte": inicio, "lt": fim}}},
            ]}},
            "random_score": {"seed": semente, "field": campo_aleatorio},
            "boost_mode": "replace",
        }},
    }


def post(url, chave, corpo, timeout=180):
    req = urllib.request.Request(url, data=json.dumps(corpo).encode("utf-8"), method="POST",
                                 headers={"Content-Type": "application/json", "Authorization": f"APIKey {chave}"})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ssl.create_default_context()) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")
    except Exception as e:  # tempo esgotado, conexão recusada
        return 0, str(e)


def busca(url, chave, corpo, tentativas, espera):
    """Devolve (resposta, None) ou (None, motivo). Sobrecarga é repetida; erro de consulta não."""
    motivo = ""
    for i in range(tentativas):
        status, texto = post(url, chave, corpo)
        try:
            d = json.loads(texto)
        except ValueError:
            d = None
        if d and "error" not in d and d.get("_shards", {}).get("failed", 1) == 0:
            return d, None
        motivo = f"HTTP {status}: {texto[:200]}"
        sobrecarga = status in (0, 429, 502, 503, 504) or "rejected" in texto or (d and d.get("_shards", {}).get("failed"))
        if not sobrecarga:
            return None, motivo
        print(f"    sobrecarga (tentativa {i + 1}/{tentativas}), nova tentativa em {espera * (i + 1)} s", flush=True)
        time.sleep(espera * (i + 1))
    return None, motivo


def excluido(r):
    nomes = " ".join(str(x.get("nome", "")) for s in r.get("assuntos") or [] for x in (s if isinstance(s, list) else [s]))
    alvo = (nomes + " " + str((r.get("orgaoJulgador") or {}).get("nome", ""))).upper()
    return any(t in alvo for t in ("MULHER", "DOMESTICA", "DOMÉSTICA", "MARIA DA PENHA"))


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--tribunal", default="tjsp")
    p.add_argument("--por-celula", type=int, default=20)
    p.add_argument("--semente", type=int, default=20261120)
    p.add_argument("--saida", default="alvos_tjsp.csv")
    p.add_argument("--bruto", default="sorteio_bruto_tjsp", help="pasta das respostas brutas")
    p.add_argument("--tentativas", type=int, default=25)
    p.add_argument("--espera", type=int, default=3)
    p.add_argument("--chave", default=os.environ.get("DATAJUD_API_KEY", CHAVE_PUBLICA))
    p.add_argument("--so-consulta", action="store_true")
    a = p.parse_args()
    url = f"https://api-publica.datajud.cnj.jus.br/api_publica_{a.tribunal.lower()}/_search"

    if a.so_consulta:
        todas = {f"{et}_{per}": consulta(cl, i, f, a.por_celula * 2, a.semente, "_seq_no")
                 for et, cl in ETAPAS.items() for per, i, f in PERIODOS}
        print(json.dumps({"endpoint": url, "consultas": todas}, ensure_ascii=False, indent=2))
        return 0

    os.makedirs(a.bruto, exist_ok=True)
    linhas, faltaram = [], []
    for et, classes in ETAPAS.items():
        for per, i, f in PERIODOS:
            arq = os.path.join(a.bruto, f"{a.tribunal}_{et}_{per}.json")
            if os.path.exists(arq):  # retomada: célula já sorteada não é refeita
                d = json.load(open(arq, encoding="utf-8"))
            else:
                print(f"{et} {per}: consultando", flush=True)
                d, motivo = busca(url, a.chave, consulta(classes, i, f, a.por_celula * 2, a.semente, "_seq_no"),
                                  a.tentativas, a.espera)
                sobrecarga = motivo and any(x in motivo for x in ("HTTP 0", "HTTP 429", "HTTP 50", "rejected"))
                if d is None and not sobrecarga:  # erro de consulta, provavelmente o campo do sorteio
                    d, motivo = busca(url, a.chave, consulta(classes, i, f, a.por_celula * 2, a.semente, "dataAjuizamento"),
                                      a.tentativas, a.espera)
                if d is None:
                    print(f"{et} {per}: FALHOU ({motivo})", flush=True)
                    faltaram.append(f"{et}_{per}")
                    continue
                d["_coletado_em"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                json.dump(d, open(arq, "w", encoding="utf-8"), ensure_ascii=False)
            universo = d["hits"]["total"]["value"]
            vistos, k = set(), 0
            for h in d["hits"]["hits"]:
                r = h["_source"]
                if k >= a.por_celula:
                    break
                if r.get("numeroProcesso") in vistos or excluido(r):
                    continue
                vistos.add(r.get("numeroProcesso"))
                k += 1
                linhas.append([r.get("numeroProcesso"), et, per, (r.get("classe") or {}).get("codigo"),
                               str(r.get("dataAjuizamento"))[:8], (r.get("orgaoJulgador") or {}).get("nome"), universo])
            print(f"{et} {per}: universo {universo}, sorteados {k}", flush=True)

    random.Random(a.semente).shuffle(linhas)  # ordem aleatória: o que for baixado primeiro continua amostra
    with open(a.saida, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["ordem", "numero", "etapa", "periodo", "classe", "ajuizamento", "orgao", "n_universo_celula"])
        for n, l in enumerate(linhas, 1):
            w.writerow([n] + l)
    print(f"{len(linhas)} alvos gravados em {a.saida}" + (f"; células sem resposta: {', '.join(faltaram)}" if faltaram else ""))
    return 1 if faltaram else 0


if __name__ == "__main__":
    sys.exit(main())
