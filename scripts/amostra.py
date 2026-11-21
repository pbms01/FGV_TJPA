# Sorteio estratificado da amostra do TJPA para leitura no Codex.
# - deduplica por (número, grau), ficando com o registro de mais movimentos, porque o índice
#   guarda mais de um registro por número e o maior é o mais completo;
# - só 1º grau e sigilo 0, para não sortear porta que o conector não abre;
# - exclui violência doméstica e contra a mulher por assunto e por órgão julgador antes do
#   sorteio, porque não é objeto e concentra dado sensível;
# - o corte P1/P2 em 23/01/2020 é provisório: vigência da Lei 13.964/2019 a conferir.
import argparse, csv, gzip, json, random

p = argparse.ArgumentParser()
p.add_argument("--censo", required=True)
p.add_argument("--saida", required=True)
p.add_argument("--por-celula", type=int, default=20)
p.add_argument("--semente", type=int, default=20261120)
a = p.parse_args()
PER = [("P1", 20190101000000, 20200123000000), ("P2", 20200123000000, 20210528000000),
       ("P3", 20210528000000, 20250101000000)]
ETAPA = {279: "inquerito", 283: "acao_penal", 10943: "acao_penal"}
melhor = {}
for l in gzip.open(a.censo, "rt"):
    r = json.loads(l)
    k = (r.get("numeroProcesso"), r.get("grau"))
    if k not in melhor or len(r.get("movimentos") or []) > len(melhor[k].get("movimentos") or []):
        melhor[k] = r
def excluido(r):
    nomes = " ".join(str(x.get("nome", "")) for s in r.get("assuntos") or [] for x in (s if isinstance(s, list) else [s]))
    org = str((r.get("orgaoJulgador") or {}).get("nome", ""))
    alvo = (nomes + " " + org).upper()
    return any(t in alvo for t in ("MULHER", "DOMESTICA", "DOMÉSTICA", "MARIA DA PENHA"))
cel = {}
for (num, g), r in melhor.items():
    cl = (r.get("classe") or {}).get("codigo")
    if g != "G1" or r.get("nivelSigilo") != 0 or cl not in ETAPA or excluido(r):
        continue
    d = int(r.get("dataAjuizamento") or 0)
    per = next((n for n, i, f in PER if i <= d < f), None)
    if per:
        cel.setdefault((ETAPA[cl], per), []).append(r)
rnd = random.Random(a.semente)
with open(a.saida, "w", newline="") as f:
    w = csv.writer(f); w.writerow(["ordem", "numero", "etapa", "periodo", "classe", "ajuizamento", "orgao", "n_universo_celula"])
    linhas = []
    for (et, per), lst in sorted(cel.items()):
        pick = rnd.sample(lst, min(a.por_celula, len(lst)))
        for r in pick:
            linhas.append([r["numeroProcesso"], et, per, (r.get("classe") or {}).get("codigo"),
                           str(r.get("dataAjuizamento"))[:8], (r.get("orgaoJulgador") or {}).get("nome"), len(lst)])
    rnd.shuffle(linhas)  # ordem aleatória: se a leitura parar no meio, o que foi lido continua amostra
    for i, l in enumerate(linhas, 1):
        w.writerow([i] + l)
print({f"{k[0]}|{k[1]}": len(v) for k, v in sorted(cel.items())}, "sorteados:", len(linhas))
