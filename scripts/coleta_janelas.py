# Censo por janelas mensais de ajuizamento, sem search_after.
# Motivo: em 20/11/2026 o cluster passou a recusar ordenação por _id ("Fielddata access on the
# _id field is disallowed"), que era o desempate do search_after usado na skill de teses.
# Janela pequena (um mês tem ~100 registros no recorte do TJPA) cabe numa página só e dispensa
# desempate; se uma janela vier maior que a página, ela é partida em duas e refeita.
# Retoma: janelas concluídas ficam em <saida>.feitas.
import argparse, gzip, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from datajud import q

p = argparse.ArgumentParser()
p.add_argument("--tribunal", required=True)
p.add_argument("--assuntos", required=True)
p.add_argument("--saida", required=True)
p.add_argument("--de", default="201601"); p.add_argument("--ate", default="202612")
p.add_argument("--pagina", type=int, default=1000)
# --leve: sem movimentos. A fase de fetch é a que o cluster rejeita sob carga, e o sorteio não
# precisa dos movimentos; eles são buscados depois só para os 120 sorteados.
p.add_argument("--leve", action="store_true")
# --anual: uma janela por ano. Sob fila cheia o gargalo é ser aceito, não o tamanho da resposta:
# 11 pedidos grandes têm mais chance de passar que 130 pequenos.
p.add_argument("--anual", action="store_true")
a = p.parse_args()
cods = [int(x) for x in a.assuntos.split(",")]
feitas_f = a.saida + ".feitas"
feitas = set(open(feitas_f).read().split()) if os.path.exists(feitas_f) else set()

def meses(de, ate):
    y, m = int(de[:4]), int(de[4:])
    while (y, m) <= (int(ate[:4]), int(ate[4:])):
        yield y, m
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)

def janela(i, f, rotulo, out):
    body = {"size": a.pagina, "track_total_hits": True,
            **({"_source": ["numeroProcesso", "grau", "classe", "nivelSigilo", "dataAjuizamento",
                            "orgaoJulgador", "assuntos", "formato", "sistema"]} if a.leve else {}),
            "query": {"bool": {"filter": [{"terms": {"assuntos.codigo": cods}},
                                          {"range": {"dataAjuizamento": {"gte": i, "lt": f}}}]}}}
    d = q(a.tribunal, body)
    tot = d["hits"]["total"]["value"]
    if tot > a.pagina:
        meio = (i + f) // 2  # metade aritmética do inteiro yyyyMMddHHmmss: serve só como corte
        return janela(i, meio, rotulo + "a", out) + janela(meio, f, rotulo + "b", out)
    for h in d["hits"]["hits"]:
        out.write(json.dumps({"_id": h["_id"], **h["_source"]}, ensure_ascii=False) + "\n")
    return len(d["hits"]["hits"])

n = 0
with gzip.open(a.saida, "at") as out:
    jan = ([(str(y), int(f"{y}0101000000"), int(f"{y+1}0101000000")) for y in range(int(a.de[:4]), int(a.ate[:4]) + 1)]
           if a.anual else
           [(f"{y}{m:02d}", int(f"{y}{m:02d}01000000"),
             int(f"{y + (m == 12)}{(m % 12) + 1:02d}01000000")) for y, m in meses(a.de, a.ate)])
    for rot, i, f in jan:
        if rot in feitas or (len(rot) == 4 and all(f"{rot}{k:02d}" in feitas for k in range(1, 13))): continue
        if not a.anual and rot[:4] in feitas: continue
        k = janela(i, f, rot, out); out.flush(); n += k
        with open(feitas_f, "a") as ff: ff.write(rot + "\n")
        print(rot, k, flush=True)
print("concluído nesta execução:", n)
