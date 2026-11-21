"""Questão 4 da análise criminológica (linha 2.1): o que a denúncia e a sentença tratam
como organização (art. 288 do CP e Lei 12.850/2013) corresponde a uma estrutura ordenada
ou à cooperação frouxa descrita por Leukfeldt, Lavorgna e Kleemans (2017)? E como a
estrutura narrada se distribui pelos eixos, pelo nível alcançado da questão 1 e pelo
enquadramento?

Lê as denúncias com scripts/organizacao.py (validação: `python3 scripts/organizacao.py
valida`), cruza com a codificação, os eixos e o nível da questão 1, e grava
dados/analise/q4_organizacao.csv (uma linha por denúncia) e q4_resumo.json. `-q` grava sem
imprimir.

Decisões que não saltam aos olhos:
- A unidade é a denúncia sem duplicatas, com o peso do processo e percentuais ponderados
  dentro do estrato; as quatro denúncias fora da tipologia (classe "fora" dos eixos) ficam
  no CSV e fora do resumo.
- A estrutura narrada combina o número de denunciados, os coautores não identificados
  (coluna coautores_desconhecidos da extração) e a leitura de ESTRUTURA em organizacao.py:
  autor isolado; nó isolado de rede não identificada (um denunciado com coautores não
  identificados, ou titular de conta ou elo logístico, que a codificação já define como peça
  de esquema executado por outro); pluralidade sem divisão de papéis
  (todos titulares de conta, ou execução conjunta do mesmo ato); papéis complementares;
  papéis complementares com coordenação narrada (por denunciado ou por terceiro).
- O critério formal da Lei 12.850 (art. 1º, §1º) é lido de modo conservador: quatro ou
  mais denunciados e papéis complementares. Pessoas não identificadas não entram na
  contagem, porque a denúncia raramente diz quantas são.
"""
import csv
import json
import os
import sys
from collections import Counter

BASE = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.dirname(__file__))
from analise_q1_alcance import NIVEL  # noqa: E402
from eixos_mediacao import eixos, le_codificacao, ponderada  # noqa: E402
import organizacao as org  # noqa: E402

EXT = os.path.join(BASE, "dados/extracao")
SAIDA = os.path.join(BASE, "dados/analise")
ESTRATOS = ["INV", "CL", "FE"]
TIPOS = ["autor isolado", "nó isolado de rede não identificada", "pluralidade sem divisão de papéis",
         "papéis complementares", "papéis complementares com coordenação", "indeterminada"]
ENQ = ["organização criminosa", "associação criminosa", "concurso de pessoas", "autoria singular"]

# Remuneração do titular pela conta, lida nos trechos que a regra RE_PAGA aponta (INV 36 e CL 32
# são falsos positivos) e na nota da codificação (FE 88).
PAGA_CONTA = {
    "FE 55": "R$ 50 prometidos pelo primo à titular",
    "FE 35": "cerca de 10% do valor transferidos a outra conta própria",
    "FE 24": "de 10 a 30% dos valores, como captador de contas",
    "INV 32": "20% dos valores",
    "FE 45": "5% por operação",
    "FE 88": "retêm 10%",
}


def grupo(n):
    return "4 ou mais" if n >= 4 else str(n)


def tipo(n, desconhecidos, est, papel, nivel):
    if n <= 1:
        # o titular de conta e o elo logístico são, pela própria codificação, peças de um
        # esquema que outra pessoa executou, mesmo quando a denúncia não fala em coautores
        rede = desconhecidos or (est and est[0] == "nó único") or papel == "titular_conta" or nivel == "elo logístico"
        return "nó isolado de rede não identificada" if rede else "autor isolado"
    div, coord = est[0], est[1]
    if div in ("contas", "execução conjunta"):
        return "pluralidade sem divisão de papéis"
    if div == "complementar":
        return "papéis complementares com coordenação" if coord != "não narrada" else "papéis complementares"
    return "indeterminada"


def base():
    den = [d for d in csv.DictReader(open(os.path.join(EXT, "denuncias_tjsp.csv"), encoding="utf-8")) if not d["duplicata_de"]]
    sent = {x["numero"]: x for x in csv.DictReader(open(os.path.join(EXT, "sentencas_amostra.csv"), encoding="utf-8"))}
    cod = le_codificacao()
    L = []
    for d in den:
        caso, n_ = f'{d["estrato"]} {d["ordem"]}', d["numero"]
        c, s = cod[n_], sent.get(n_)
        ex = eixos(caso, c)
        x = org.le(caso, n_)
        est = org.ESTRUTURA.get(caso)
        desc = d["coautores_desconhecidos"] == "True"
        if d["estrato"] == "INV":
            nivel = c["papel_denunciado"]
        elif c["papel_denunciado"] == "titular_conta":
            nivel = "só conta"
        else:
            nivel = NIVEL[caso][0]
        so = org.SENTENCA_ORG.get(caso, ("", ""))
        L.append(dict(
            caso=caso, numero=n_, estrato=d["estrato"], peso=float(d["peso"]), fora=ex["classe"] == "fora",
            n_denunciados=x["n_denunciados"], grupo=grupo(x["n_denunciados"]), coautores_desconhecidos=desc,
            enquadramento=x["enquadramento"], divisao=est[0] if est else "", coordenacao=est[1] if est else "",
            vinculo=est[2] if est else "", reiteracao=est[3] if est else "", nota_estrutura=est[4] if est else "",
            tipo_estrutura=tipo(x["n_denunciados"], desc, est, c["papel_denunciado"], nivel), papel=c["papel_denunciado"], nivel=nivel,
            artificio=c["artificio"], sistema=ex["sistema"], canal=ex["canal_eixo"], distancia=ex["distancia"],
            classe=ex["classe"], cap=d["tipo_capitulacao"], resultado=s["resultado"] if s else "sem sentença",
            sentenca_org=so[0], nota_sentenca_org=so[1], pedido_conta=x["pedido_conta"], trecho_pedido=x["trecho_pedido"],
            paga_conta=PAGA_CONTA.get(caso, ""),
            formal_12850=x["n_denunciados"] >= 4 and bool(est) and est[0] == "complementar",
        ))
    return L


def resumo(L):
    out = {}
    for e in ESTRATOS:
        E = [x for x in L if x["estrato"] == e and not x["fora"]]
        P = [x for x in E if x["n_denunciados"] >= 2]
        o = out[e] = {"denuncias": len(E), "plurais": len(P)}
        o["grupo"] = ponderada(E, lambda x: x["grupo"], ["1", "2", "3", "4 ou mais"])
        o["um_denunciado_com_desconhecidos"] = ponderada([x for x in E if x["n_denunciados"] <= 1], lambda x: x["coautores_desconhecidos"])
        o["enquadramento"] = ponderada(E, lambda x: x["enquadramento"], ENQ)
        o["tipo_estrutura"] = ponderada(E, lambda x: x["tipo_estrutura"], TIPOS)
        o["divisao_plurais"] = ponderada(P, lambda x: x["divisao"])
        o["coordenacao_plurais"] = ponderada(P, lambda x: x["coordenacao"])
        o["vinculo_plurais"] = ponderada(P, lambda x: x["vinculo"] or "não narrado")
        o["reiteracao_plurais"] = ponderada(P, lambda x: x["reiteracao"])
        o["enquadramento_por_tipo"] = {t: dict(Counter(x["enquadramento"] for x in E if x["tipo_estrutura"] == t)) for t in TIPOS
                                       if any(x["tipo_estrutura"] == t for x in E)}
        o["tipo_por_enquadramento"] = {q: dict(Counter(x["tipo_estrutura"] for x in E if x["enquadramento"] == q)) for q in ENQ
                                       if any(x["enquadramento"] == q for x in E)}
        o["org_assoc"] = {x["caso"]: f'{x["enquadramento"]} | {x["n_denunciados"]} denunciado(s) | {x["tipo_estrutura"]} | '
                                     f'{x["coordenacao"] or "-"} | sentença: {x["sentenca_org"]}' for x in E
                          if x["enquadramento"] in ("organização criminosa", "associação criminosa")}
        o["formal_12850"] = {x["caso"]: f'{x["n_denunciados"]} | {x["enquadramento"]} | {x["coordenacao"]} | {x["nota_estrutura"]}'
                             for x in E if x["formal_12850"]}
        o["coordenacao_detalhe"] = {x["caso"]: f'{x["coordenacao"]} | {x["enquadramento"]} | {x["nota_estrutura"]}' for x in P
                                    if x["coordenacao"] in ("denunciado", "terceiro")}
        o["vinculo_detalhe"] = {x["caso"]: f'{x["vinculo"]} | {x["nota_estrutura"]}' for x in P if x["vinculo"]}
        o["tipo_por_nivel"] = {v: ponderada([x for x in E if x["nivel"] == v], lambda x: x["tipo_estrutura"], TIPOS)
                               for v in sorted({x["nivel"] for x in E})}
        o["tipo_por_sistema"] = {v: ponderada([x for x in E if x["sistema"] == v], lambda x: x["tipo_estrutura"], TIPOS)
                                 for v in sorted({x["sistema"] for x in E})}
        o["tipo_por_distancia"] = {v: ponderada([x for x in E if x["distancia"] == v], lambda x: x["tipo_estrutura"], TIPOS)
                                   for v in sorted({x["distancia"] for x in E})}
        o["grupo_por_distancia"] = {v: ponderada([x for x in E if x["distancia"] == v], lambda x: x["grupo"], ["1", "2", "3", "4 ou mais"])
                                    for v in sorted({x["distancia"] for x in E})}
        o["pedido_conta"] = {x["caso"]: f'{x["pedido_conta"]} | {x["trecho_pedido"][40:170]}' for x in E if x["pedido_conta"]}
        o["paga_conta"] = {x["caso"]: x["paga_conta"] for x in E if x["paga_conta"]}
    T = [x for x in L if not x["fora"]]
    out["total"] = dict(
        denuncias=len(T), plurais=sum(x["n_denunciados"] >= 2 for x in T), tres_ou_mais=sum(x["n_denunciados"] >= 3 for x in T),
        quatro_ou_mais=sum(x["n_denunciados"] >= 4 for x in T),
        enquadramento=dict(Counter(x["enquadramento"] for x in T)),
        tipo=dict(Counter(x["tipo_estrutura"] for x in T)),
        sentenca_org=dict(Counter(x["sentenca_org"] for x in T if x["sentenca_org"])),
        formal_12850=[x["caso"] for x in T if x["formal_12850"]],
        formal_12850_denunciada_org=[x["caso"] for x in T if x["formal_12850"] and x["enquadramento"] == "organização criminosa"],
        formal_12850_denunciada_288=[x["caso"] for x in T if x["formal_12850"] and x["enquadramento"] == "associação criminosa"],
        complementar_com_coordenacao=[x["caso"] for x in T if x["tipo_estrutura"] == "papéis complementares com coordenação"],
    )
    return out


def fmt(d):
    return "; ".join(f"{k} {v[0]} ({v[1]}%)" for k, v in d.items())


def main():
    L = base()
    os.makedirs(SAIDA, exist_ok=True)
    with open(os.path.join(SAIDA, "q4_organizacao.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(L[0].keys()))
        w.writeheader()
        w.writerows(L)
    R = resumo(L)
    json.dump(R, open(os.path.join(SAIDA, "q4_resumo.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if "-q" in sys.argv:
        return
    for e in ESTRATOS:
        print(f"\n===== {e}")
        for k, v in R[e].items():
            if isinstance(v, dict) and v and all(isinstance(z, tuple) or isinstance(z, list) for z in v.values()):
                print(f"{k}: {fmt(v)}")
            elif isinstance(v, dict):
                print(f"{k}:")
                for a, b in v.items():
                    print(f"   {a}: {fmt(b) if isinstance(b, dict) and b and isinstance(next(iter(b.values())), (tuple, list)) else b}")
            else:
                print(f"{k}: {v}")
    print("\n===== total")
    for k, v in R["total"].items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
