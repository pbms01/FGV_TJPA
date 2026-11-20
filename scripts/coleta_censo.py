# Censo de metadados (com movimentos) de um recorte por assunto, paginado por search_after.
# Retoma de onde parou: o cursor da última página gravada fica em <saida>.cursor,
# o que importa numa execução noturna sujeita a 429/504 e a reinício do contêiner.
import argparse, gzip, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from datajud import q

p = argparse.ArgumentParser()
p.add_argument("--tribunal", required=True)
p.add_argument("--assuntos", required=True, help="códigos separados por vírgula")
p.add_argument("--saida", required=True)
p.add_argument("--pagina", type=int, default=500)
p.add_argument("--max", type=int, default=10**9, help="teto, para teste")
a = p.parse_args()
cods = [int(x) for x in a.assuntos.split(",")]
query = {"bool": {"filter": [{"terms": {"assuntos.codigo": cods}}]}}
cur_f = a.saida + ".cursor"
depois = json.load(open(cur_f)) if os.path.exists(cur_f) else None
total = q(a.tribunal, {"size": 0, "track_total_hits": True, "query": query})["hits"]["total"]["value"]
n = sum(1 for _ in gzip.open(a.saida, "rt")) if (depois and os.path.exists(a.saida)) else 0
print(f"{a.tribunal}: universo {total}, já gravados {n}", flush=True)
with gzip.open(a.saida, "at") as out:
    while True:
        body = {"size": a.pagina, "query": query,
                "sort": [{"dataAjuizamento": {"order": "desc"}}, {"_id": {"order": "asc"}}]}
        if depois:
            body["search_after"] = depois
        hits = q(a.tribunal, body)["hits"]["hits"]
        if not hits or n >= a.max:
            break
        for h in hits:
            out.write(json.dumps({"_id": h["_id"], **h["_source"]}, ensure_ascii=False) + "\n")
        n += len(hits)
        depois = hits[-1]["sort"]
        out.flush(); json.dump(depois, open(cur_f, "w"))
        print(f"  {n}/{total}", flush=True)
print(f"concluído: {n} registros (universo {total})")
