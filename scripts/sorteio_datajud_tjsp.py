#!/usr/bin/env python3
"""Seleciona no DataJud (API pública do CNJ) os números de processo-alvo do TJSP para download posterior.

Recorte (decisão de 20/11/2026): só os assuntos da TPU que nomeiam o próprio tipo cibernético,
conferidos no SGT versão 05/11/2026: 15623 Fraude Eletrônica (art. 171, § 2º-A, CP), 11978 Invasão de
Dispositivo Informático (art. 154-A, CP) e 15755 Estelionato Mediante Cessão de Conta Laranja
(art. 171, § 2º, VII, CP). Ficam fora o furto informático (art. 155, § 4º-B), que não tem código e cai
no genérico 3417 Furto Qualificado, e os códigos genéricos de estelionato (3431, 3432, 14692), que não
separam o meio digital. 14693, 15624 e 15756 são da árvore de ato infracional e não entram.
1º grau, sigilo 0, inquérito policial (279) e ação penal (283, 10943).
Saída: CSV com um número por linha, pronto para a sessão de download.

Uso:
    python sorteio_datajud_tjsp.py                    # até 20 por célula (10 células) em alvos_tjsp.csv
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
- A janela de cada código começa na vigência do tipo, e não na criação do código: um processo
  anterior ao código pode tê-lo recebido por reclassificação, e isso é dado a medir. Por isso o 15623
  tem uma célula antes e outra depois de 19/09/2025, data em que o código foi criado no SGT.
- Célula com universo menor que o pedido vira censo (o servidor devolve todos).
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
ETAPAS = {"inquerito": [279], "acao_penal": [283, 10943]}
FIM = 20261120000000  # data da decisão do recorte; ajustar ao rodar mais tarde
CELULAS = [  # (código TPU, tipo, rótulo do período, início inclusive, fim exclusivo), em yyyyMMddHHmmss
    (11978, "invasao_dispositivo_154A", "ate_14155", 20161119000000, 20210528000000),   # redação da Lei 12.737/2012
    (11978, "invasao_dispositivo_154A", "pos_14155", 20210528000000, FIM),              # redação da Lei 14.155/2021
    (15623, "fraude_eletronica_171_2A", "antes_do_codigo", 20210528000000, 20250919000000),  # só por reclassificação
    (15623, "fraude_eletronica_171_2A", "codigo_vigente", 20250919000000, FIM),
    (15755, "conta_laranja_171_2_VII", "pos_15397", 20260504000000, FIM),               # tipo desde 04/05/2026
]
CAMPOS = ["numeroProcesso", "classe", "dataAjuizamento", "orgaoJulgador", "assuntos", "grau", "nivelSigilo"]


def consulta(assunto, classes, inicio, fim, tamanho, semente, campo_aleatorio):
    return {
        "size": tamanho,
        "track_total_hits": True,
        "_source": CAMPOS,
        "query": {"function_score": {
            "query": {"bool": {"filter": [
                {"term": {"assuntos.codigo": assunto}},
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
        todas = {f"{cod}_{et}_{per}": consulta(cod, cl, i, f, a.por_celula * 2, a.semente, "_seq_no")
                 for cod, tipo, per, i, f in CELULAS for et, cl in ETAPAS.items()}
        print(json.dumps({"endpoint": url, "consultas": todas}, ensure_ascii=False, indent=2))
        return 0

    os.makedirs(a.bruto, exist_ok=True)
    linhas, faltaram = [], []
    for cod, tipo, per, i, f in CELULAS:
        for et, classes in ETAPAS.items():
            arq = os.path.join(a.bruto, f"{a.tribunal}_{cod}_{et}_{per}.json")
            if os.path.exists(arq):  # retomada: célula já sorteada não é refeita
                d = json.load(open(arq, encoding="utf-8"))
            else:
                print(f"{cod} {et} {per}: consultando", flush=True)
                d, motivo = busca(url, a.chave, consulta(cod, classes, i, f, a.por_celula * 2, a.semente, "_seq_no"),
                                  a.tentativas, a.espera)
                sobrecarga = motivo and any(x in motivo for x in ("HTTP 0", "HTTP 429", "HTTP 50", "rejected"))
                if d is None and not sobrecarga:  # erro de consulta, provavelmente o campo do sorteio
                    d, motivo = busca(url, a.chave, consulta(cod, classes, i, f, a.por_celula * 2, a.semente, "dataAjuizamento"),
                                      a.tentativas, a.espera)
                if d is None:
                    print(f"{cod} {et} {per}: FALHOU ({motivo})", flush=True)
                    faltaram.append(f"{cod}_{et}_{per}")
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
                linhas.append([r.get("numeroProcesso"), cod, tipo, et, per, (r.get("classe") or {}).get("codigo"),
                               str(r.get("dataAjuizamento"))[:8], (r.get("orgaoJulgador") or {}).get("nome"), universo])
            print(f"{cod} {et} {per}: universo {universo}, sorteados {k}", flush=True)

    random.Random(a.semente).shuffle(linhas)  # ordem aleatória: o que for baixado primeiro continua amostra
    with open(a.saida, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["ordem", "numero", "assunto", "tipo", "etapa", "periodo", "classe", "ajuizamento", "orgao", "n_universo_celula"])
        for n, l in enumerate(linhas, 1):
            w.writerow([n] + l)
    print(f"{len(linhas)} alvos gravados em {a.saida}" + (f"; células sem resposta: {', '.join(faltaram)}" if faltaram else ""))
    return 1 if faltaram else 0


if __name__ == "__main__":
    sys.exit(main())
