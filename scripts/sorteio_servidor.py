# Sorteio estratificado feito no próprio servidor (random_score com semente), uma consulta por célula.
# Motivo: com o DataJud saturado, baixar o censo inteiro para sortear localmente exige dezenas de
# pedidos aceitos; aqui bastam 6. O censo continua necessário para o funil, mas não para a amostra.
# Pede-se o dobro do necessário por célula para absorver exclusões (violência doméstica, duplicados
# por número) sem nova consulta. A semente fixa torna o sorteio reproduzível enquanto o índice não mudar;
# por isso o resultado bruto de cada célula é gravado com data e hora.
import argparse, csv, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from datajud import q

p = argparse.ArgumentParser()
p.add_argument("--tribunal", default="tjpa")
p.add_argument("--por-celula", type=int, default=20)
p.add_argument("--semente", type=int, default=20261120)
p.add_argument("--saida", default="/home/claude/dados/amostra_tjpa.csv")
a = p.parse_args()
COD = [3431, 15623, 11978, 14692, 14693]
PER = [("P1", 20190101000000, 20200123000000), ("P2", 20200123000000, 20210528000000),
       ("P3", 20210528000000, 20250101000000)]
ETAPA = {"inquerito": [279], "acao_penal": [283, 10943]}
BRUTO = "/home/claude/dados/sorteio_bruto"
os.makedirs(BRUTO, exist_ok=True)

def excluido(r):
    nomes = " ".join(str(x.get("nome", "")) for s in r.get("assuntos") or [] for x in (s if isinstance(s, list) else [s]))
    alvo = (nomes + " " + str((r.get("orgaoJulgador") or {}).get("nome", ""))).upper()
    return any(t in alvo for t in ("MULHER", "DOMESTICA", "DOMÉSTICA", "MARIA DA PENHA"))

linhas = []
for et, classes in ETAPA.items():
    for per, i, f in PER:
        arq = f"{BRUTO}/{et}_{per}.json"
        if os.path.exists(arq):
            d = json.load(open(arq))
        else:
            # _source enxuto: sob fila cheia, resposta menor reduz o risco de 504 no balanceador
            body = {"size": a.por_celula * 2, "track_total_hits": True,
                    "_source": ["numeroProcesso", "classe", "dataAjuizamento", "orgaoJulgador", "assuntos", "grau", "nivelSigilo"],
                    "query": {"function_score": {
                        "query": {"bool": {"filter": [
                            {"terms": {"assuntos.codigo": COD}}, {"terms": {"classe.codigo": classes}},
                            {"term": {"nivelSigilo": 0}}, {"match": {"grau": "G1"}},
                            {"range": {"dataAjuizamento": {"gte": i, "lt": f}}}]}},
                        "random_score": {"seed": a.semente, "field": "_seq_no"}, "boost_mode": "replace"}}}
            d = q(a.tribunal, body, tries=25, espera=3)
            d["_coletado_em"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            json.dump(d, open(arq, "w"), ensure_ascii=False)
        univ = d["hits"]["total"]["value"]
        vistos, k = set(), 0
        for h in d["hits"]["hits"]:
            r = h["_source"]
            if k >= a.por_celula: break
            if r.get("numeroProcesso") in vistos or excluido(r): continue
            vistos.add(r.get("numeroProcesso")); k += 1
            linhas.append([r.get("numeroProcesso"), et, per, (r.get("classe") or {}).get("codigo"),
                           str(r.get("dataAjuizamento"))[:8], (r.get("orgaoJulgador") or {}).get("nome"), univ,
                           len(r.get("movimentos") or [])])
        print(et, per, "universo", univ, "sorteados", k, flush=True)
import random
random.Random(a.semente).shuffle(linhas)  # ordem aleatória: se a triagem parar, o já triado segue amostra
with open(a.saida, "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["ordem", "numero", "etapa", "periodo", "classe", "ajuizamento", "orgao", "n_universo_celula", "n_movimentos"])
    for n, l in enumerate(linhas, 1): w.writerow([n] + l)
print("total sorteado:", len(linhas))
