# Responde localmente, a partir do censo gravado, as perguntas da sonda que o cluster
# não aguentou em 19/11/2026: duplicidade por número e grau, sigilo, trajetória do mesmo
# número entre classes, nomes de classes e assuntos, movimentos mais frequentes.
# Rodar sobre o arquivo local evita agregações pesadas no servidor e custa zero token.
import argparse, gzip, json, collections as C

p = argparse.ArgumentParser()
p.add_argument("--censo", required=True)
p.add_argument("--saida", required=True)
a = p.parse_args()
regs = [json.loads(l) for l in gzip.open(a.censo, "rt")]
nome_cl, nome_as, mov = {}, {}, C.Counter()
por_num = C.defaultdict(set); grau = C.Counter(); sig = C.Counter(); ano_cl = C.Counter()
for r in regs:
    cl = r.get("classe") or {}; nome_cl[cl.get("codigo")] = cl.get("nome")
    for s in r.get("assuntos") or []:
        for x in (s if isinstance(s, list) else [s]):
            nome_as[x.get("codigo")] = x.get("nome")
    por_num[r.get("numeroProcesso")].add((r.get("grau"), cl.get("codigo")))
    grau[r.get("grau")] += 1; sig[r.get("nivelSigilo")] += 1
    ano_cl[(str(r.get("dataAjuizamento"))[:4], cl.get("codigo"))] += 1
    for m in r.get("movimentos") or []:
        mov[(m.get("codigo"), m.get("nome"))] += 1
multi = {n: v for n, v in por_num.items() if len({c for _, c in v}) > 1}
combos = C.Counter(tuple(sorted({c for _, c in v})) for v in multi.values())
out = {"registros": len(regs), "numeros_distintos": len(por_num),
       "numeros_em_mais_de_uma_classe": len(multi),
       "combinacoes_de_classe": [[list(k), n] for k, n in combos.most_common(15)],
       "grau": dict(grau), "nivelSigilo": {str(k): v for k, v in sig.items()},
       "classes": {str(k): v for k, v in nome_cl.items()},
       "assuntos": {str(k): v for k, v in nome_as.items()},
       "movimentos_top80": [[c, n_, k] for (c, n_), k in mov.most_common(80)],
       "ano_classe": {f"{y}|{c}": n for (y, c), n in sorted(ano_cl.items())}}
json.dump(out, open(a.saida, "w"), ensure_ascii=False, indent=1)
print({k: out[k] for k in ("registros", "numeros_distintos", "numeros_em_mais_de_uma_classe", "grau", "nivelSigilo")})
print("combinações:", out["combinacoes_de_classe"][:6])
