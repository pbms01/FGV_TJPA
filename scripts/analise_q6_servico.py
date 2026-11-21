"""Questão 6 da análise criminológica (linhas 3.4 e 4.1): a fraude explora a vulnerabilidade
da pessoa ou a do serviço? Quem é a vítima por família de artifício, por quais pontos do
serviço financeiro o golpe passou, o que o banco fez segundo a denúncia e a sentença, e
que deveres de cuidado isso põe em jogo.

Lê as denúncias com scripts/servico_banco.py (`python3 scripts/servico_banco.py valida`
imprime os trechos que acionam cada indicador nas 29 da matriz), cruza com a codificação, os
eixos, a questão 1 (nível), a questão 3 (valor do fato e ressarcimento pelo intermediário) e
a questão 5 (data do fato), e grava dados/analise/q6_servico.csv e q6_resumo.json. `-q`
grava sem imprimir.

Decisões que não saltam aos olhos:
- Entram as denúncias da tipologia em que o dinheiro passou pelo serviço financeiro (as cinco
  famílias de servico_banco.py); controle da parceira, devassa, venda de dados, insider e
  inserção de dados em sistema público ficam fora.
- Por estrato, percentuais ponderados; por família e por ponto do serviço, contagens simples
  das três camadas, porque a família atravessa os estratos.
- O valor do fato é o da questão 3 (prejuízo narrado, em reais), comparado por mediana.
"""
import csv
import datetime
import json
import os
import statistics
import sys
from collections import Counter

BASE = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.dirname(__file__))
from analise_q1_alcance import NIVEL  # noqa: E402
from eixos_mediacao import eixos, le_codificacao, ponderada  # noqa: E402
import servico_banco as sb  # noqa: E402

EXT = os.path.join(BASE, "dados/extracao")
SAIDA = os.path.join(BASE, "dados/analise")
ESTRATOS = ["INV", "CL", "FE"]
PONTOS = ["credencial", "acesso_remoto", "credito_vitima", "varias_operacoes", "repasse_imediato"]
RES_CONJ_6 = datetime.date(2023, 11, 1)  # vigência da Resolução Conjunta CMN/BCB nº 6/2023


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def base():
    den = [d for d in csv.DictReader(open(os.path.join(EXT, "denuncias_tjsp.csv"), encoding="utf-8")) if not d["duplicata_de"]]
    sent = {x["numero"]: x for x in csv.DictReader(open(os.path.join(EXT, "sentencas_amostra.csv"), encoding="utf-8"))}
    q3 = {x["caso"]: x for x in csv.DictReader(open(os.path.join(SAIDA, "q3_dano.csv"), encoding="utf-8"))}
    q5 = {x["caso"]: x for x in csv.DictReader(open(os.path.join(SAIDA, "q5_tempo_dado.csv"), encoding="utf-8"))}
    cod = le_codificacao()
    L = []
    for d in den:
        caso, n_ = f'{d["estrato"]} {d["ordem"]}', d["numero"]
        c, s = cod[n_], sent.get(n_)
        ex = eixos(caso, c)
        x = sb.le(caso, d, c)
        if d["estrato"] == "INV":
            nivel = c["papel_denunciado"]
        elif c["papel_denunciado"] == "titular_conta":
            nivel = "só conta"
        else:
            nivel = NIVEL[caso][0]
        fato = q5[caso]["data_fato"]
        L.append(dict(
            caso=caso, numero=n_, estrato=d["estrato"], peso=float(d["peso"]), fora=ex["classe"] == "fora" or not x["familia"],
            familia=x["familia"], artificio=c["artificio"], canal="sistema-objeto" if ex["sistema"] == "objeto" else ex["canal_eixo"],
            meio=c["meio_contato"], nivel=nivel, idosa=x["idosa"], majorante_4=x["majorante_4"], aumento_idade=x["aumento_idade"], pj=x["pj"],
            **{k: x[k] for k in PONTOS}, nota_credito=x["nota_credito"], reacao_banco=x["reacao_banco"], nota_reacao=x["nota_reacao"],
            valor_fato=num(q3[caso]["valor_fato"]) if caso in q3 else None,
            ressarciu_sentenca=q3[caso]["intermediario_ressarciu"] if caso in q3 else "",
            data_fato=fato, apos_res_conj_6=bool(fato) and datetime.date.fromisoformat(fato) >= RES_CONJ_6,
            resultado=s["resultado"] if s else "sem sentença",
        ))
    return L


def mediana(v):
    v = [x for x in v if x]
    return round(statistics.median(v), 2) if v else None


def resumo(L):
    out = {}
    T = [x for x in L if not x["fora"]]
    for e in ESTRATOS:
        E = [x for x in T if x["estrato"] == e]
        o = out[e] = {"denuncias": len(E)}
        o["familia"] = ponderada(E, lambda x: x["familia"], sb.FAMILIAS)
        o["idosa"] = ponderada(E, lambda x: x["idosa"]).get(True, (0, 0.0))
        o["pj"] = ponderada(E, lambda x: x["pj"]).get(True, (0, 0.0))
    out["por_familia"] = {}
    for f in sb.FAMILIAS:
        F = [x for x in T if x["familia"] == f]
        pessoa = [x for x in F if not x["pj"]]
        out["por_familia"][f] = dict(
            n=len(F), pj=sum(x["pj"] for x in F), idosa=sum(x["idosa"] for x in F),
            idosa_pct_pessoa_fisica=round(100 * sum(x["idosa"] for x in pessoa) / len(pessoa), 1) if pessoa else None,
            canal=dict(Counter(x["canal"] for x in F)), artificio=dict(Counter(x["artificio"] for x in F)),
            valor_mediano=mediana([x["valor_fato"] for x in F]),
            **{p: sum(x[p] for x in F) for p in PONTOS},
            reacao=dict(Counter(x["reacao_banco"] for x in F if x["reacao_banco"])),
            ressarciu_sentenca=sum(bool(x["ressarciu_sentenca"]) for x in F))
    pf = [x for x in T if not x["pj"]]
    out["idosa"] = dict(
        pessoa_fisica=len(pf), idosas=sum(x["idosa"] for x in pf),
        artificio_idosa=dict(Counter(x["artificio"] for x in pf if x["idosa"]).most_common()),
        canal_idosa=dict(Counter(x["canal"] for x in pf if x["idosa"])), canal_nao=dict(Counter(x["canal"] for x in pf if not x["idosa"])),
        valor_mediano_idosa=mediana([x["valor_fato"] for x in pf if x["idosa"]]),
        valor_mediano_nao=mediana([x["valor_fato"] for x in pf if not x["idosa"]]),
        aumento_idade=dict(Counter(x["aumento_idade"] or "nenhum" for x in pf if x["idosa"])),
        idosa_sem_aumento=[f'{x["caso"]} ({x["artificio"]})' for x in pf if x["idosa"] and not x["aumento_idade"]],
        nivel_idosa=dict(Counter(x["nivel"] for x in pf if x["idosa"])),
        pontos_idosa={p: sum(x[p] for x in pf if x["idosa"]) for p in PONTOS},
        pontos_nao={p: sum(x[p] for x in pf if not x["idosa"]) for p in PONTOS},
    )
    out["credito"] = {x["caso"]: f'{x["familia"]} | idosa {x["idosa"]} | {x["nota_credito"]}' for x in T if x["credito_vitima"]}
    out["reacao"] = {x["caso"]: f'{x["reacao_banco"]} | {x["familia"]} | {x["nota_reacao"]}' for x in T if x["reacao_banco"]}
    out["ressarciu_sentenca"] = {x["caso"]: f'{x["familia"]} | {x["artificio"]} | {x["ressarciu_sentenca"]}' for x in T if x["ressarciu_sentenca"]}
    so = [x for x in T if x["nivel"] == "só conta"]
    out["res_conj_6"] = dict(total=len(T), apos=sum(x["apos_res_conj_6"] for x in T), so_conta=len(so),
                             so_conta_apos=sum(x["apos_res_conj_6"] for x in so))
    out["total"] = dict(denuncias=len(T), familia=dict(Counter(x["familia"] for x in T)),
                        pontos={p: sum(x[p] for x in T) for p in PONTOS}, idosa=sum(x["idosa"] for x in T),
                        pj=sum(x["pj"] for x in T), fora_servico=sum(1 for x in L if x["fora"]))
    return out


def main():
    L = base()
    os.makedirs(SAIDA, exist_ok=True)
    with open(os.path.join(SAIDA, "q6_servico.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(L[0].keys()))
        w.writeheader()
        w.writerows(L)
    R = resumo(L)
    json.dump(R, open(os.path.join(SAIDA, "q6_resumo.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if "-q" in sys.argv:
        return
    for k, v in R.items():
        print(f"\n===== {k}")
        for a, b in v.items():
            print(f"   {a}: {b}")


if __name__ == "__main__":
    main()
