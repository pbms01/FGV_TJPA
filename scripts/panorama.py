# Panorama comparativo por metadados (sem leitura de autos) para vários tribunais.
# Passo 1 ranqueia os candidatos pelo volume de registros ajuizados em 2025, porque
# "maiores tribunais" precisa de critério verificável na própria fonte; o índice conta
# registros (um por grau/classe), não processos, o que basta para ordenar.
# Passo 2 mede, por ano, os assuntos de estelionato e crime informático, as classes
# que representam etapa do funil e a adoção mensal do código 15623 desde set/2025.
import argparse, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from datajud import q, ano

p = argparse.ArgumentParser()
p.add_argument("--candidatos", default="tjsp,tjmg,tjrj,tjrs,tjpr,tjba")
p.add_argument("--fixos", default="tjpa", help="sempre medidos, além dos 3 maiores")
p.add_argument("--saida", default="/home/claude/dados/panorama.json")
# --alvos fixa os tribunais de comparação e dispensa o ranqueamento (escolha do Pedro em 19/11: tjsp,tjmg,tjba)
p.add_argument("--alvos", default=None)
a = p.parse_args()
res = json.load(open(a.saida)) if os.path.exists(a.saida) else {}

rank = res.setdefault("ranking_2025", {})
for t in ([] if a.alvos else a.candidatos.split(",")):
    if t in rank: continue
    d = q(t, {"size": 0, "track_total_hits": True,
              "query": {"range": {"dataAjuizamento": {"gte": ano(2025), "lt": ano(2026)}}}})
    rank[t] = d["hits"]["total"]["value"]; json.dump(res, open(a.saida, "w"), indent=1)
    print("2025", t, rank[t], flush=True)
top3 = a.alvos.split(",") if a.alvos else sorted(rank, key=rank.get, reverse=True)[:3]
res["top3"] = top3
alvos = top3 + [t for t in a.fixos.split(",") if t and t not in top3]

COD = [3431, 15623, 11978, 14692, 14693]
anos = [{"key": str(y), "from": ano(y), "to": ano(y + 1)} for y in range(2016, 2027)]
meses = [{"key": f"{y}-{m:02d}", "from": int(f"{y}{m:02d}01000000"),
          "to": int(f"{y + (m == 12)}{(m % 12) + 1:02d}01000000")}
         for y, m in [(2025, 9), (2025, 10), (2025, 11), (2025, 12)] + [(2026, k) for k in range(1, 12)]]
for t in alvos:
    if t in res.get("trib", {}): continue
    body = {"size": 0, "track_total_hits": True,
            "query": {"bool": {"filter": [{"terms": {"assuntos.codigo": COD}}]}},
            "aggs": {"ano": {"range": {"field": "dataAjuizamento", "ranges": anos},
                             "aggs": {"assunto": {"terms": {"field": "assuntos.codigo", "include": COD}},
                                      "classe": {"terms": {"field": "classe.codigo", "size": 12}}}},
                     "sigilo": {"terms": {"field": "nivelSigilo"}},
                     "mes15623": {"filter": {"term": {"assuntos.codigo": 15623}},
                                  "aggs": {"m": {"range": {"field": "dataAjuizamento", "ranges": meses}}}}}}
    d = q(t, body)
    ag = d["aggregations"]
    res.setdefault("trib", {})[t] = {
        "total": d["hits"]["total"]["value"],
        "por_ano": {b["key"]: {"n": b["doc_count"],
                               "assunto": {str(x["key"]): x["doc_count"] for x in b["assunto"]["buckets"]},
                               "classe": {str(x["key"]): x["doc_count"] for x in b["classe"]["buckets"]}}
                    for b in ag["ano"]["buckets"]},
        "sigilo": {str(b["key"]): b["doc_count"] for b in ag["sigilo"]["buckets"]},
        "mes15623": {b["key"]: b["doc_count"] for b in ag["mes15623"]["m"]["buckets"]}}
    json.dump(res, open(a.saida, "w"), indent=1)
    print("ok", t, res["trib"][t]["total"], flush=True)
print("top3:", top3)
