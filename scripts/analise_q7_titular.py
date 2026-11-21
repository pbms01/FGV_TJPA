"""Questão 7 da análise criminológica (linha 2.3, reduzida à entrada do titular da conta): o
que o titular diz de como a conta saiu das mãos dele, a quem e por quanto, que perfil a
sentença registra (antecedentes, idade), como a cota trata o acordo e como a versão se
relaciona com o desfecho.

Lê as 101 denúncias de só conta (FE e CL) com scripts/titular_conta.py (`python3
scripts/titular_conta.py valida` imprime a versão e o trecho de cada uma), cruza com a
questão 1 (desfecho), a questão 4 (pedido e remuneração da conta) e a extração da cota, e
grava dados/analise/q7_titular.csv e q7_resumo.json. `-q` grava sem imprimir.

Decisões que não saltam aos olhos:
- A unidade é a denúncia de só conta; quando há mais de um titular, a versão é a da primeira
  leitura que a regra acha, e os antecedentes, os de qualquer réu da sentença.
- Percentuais por versão são contagens simples das duas camadas somadas, com o CL e a FE
  também separados; a condenação inclui a procedência parcial, como na questão 1.
- O valor da cessão é o que o trecho da versão registra; a remuneração em percentual vem da
  questão 4 (PAGA_CONTA).
"""
import csv
import json
import os
import statistics
import sys
from collections import Counter

BASE = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.dirname(__file__))
import titular_conta as tc  # noqa: E402

EXT = os.path.join(BASE, "dados/extracao")
SAIDA = os.path.join(BASE, "dados/analise")
VERSOES = [k for k, _ in tc.VERSOES] + ["sem versão"]
CESSAO = {"cedeu mediante pagamento", "aceitou proposta de trabalho, renda ou crédito", "emprestou a alguém"}


def valor(v):
    try:
        return float(v.replace(".", "").replace(",", "."))
    except (AttributeError, ValueError):
        return None


def base():
    den = {f'{d["estrato"]} {d["ordem"]}': d for d in csv.DictReader(open(os.path.join(EXT, "denuncias_tjsp.csv"), encoding="utf-8"))
           if not d["duplicata_de"]}
    q1 = {x["caso"]: x for x in csv.DictReader(open(os.path.join(SAIDA, "q1_alcance.csv"), encoding="utf-8"))}
    q4 = {x["caso"]: x for x in csv.DictReader(open(os.path.join(SAIDA, "q4_organizacao.csv"), encoding="utf-8"))}
    L = []
    for caso, n in tc._so_conta():
        d, a, o = den[caso], q1[caso], q4[caso]
        x = tc.le(caso, n)
        grupo = ("cessão admitida" if x["versao"] in CESSAO else
                 "nega ou não reconhece" if x["versao"] in ("nega", "perdeu o controle ou não reconhece a conta") else
                 "ausente" if x["versao"] in ("silêncio", "não localizado ou revel") else "sem versão")
        L.append(dict(
            caso=caso, numero=n, estrato=d["estrato"], peso=float(d["peso"]), n_denunciados=o["n_denunciados"],
            versao=x["versao"], grupo_versao=grupo, fonte_versao=x["fonte_versao"], trecho_versao=x["trecho_versao"],
            a_quem=x["a_quem"], valor_cessao=x["valor_cessao"], paga_conta=o["paga_conta"], pedido_conta=o["pedido_conta"],
            confissao=x["confissao"], antecedentes=x["antecedentes"], jovem=x["jovem"],
            cota_anpp=d["cota_anpp"] == "True", anpp_pena=d["anpp_motivo_pena"] == "True", anpp_confissao=d["anpp_motivo_confissao"] == "True",
            anpp_antecedentes=d["anpp_motivo_antecedentes"] == "True", anpp_ausencia=d["anpp_motivo_ausencia"] == "True",
            cap=d["tipo_capitulacao"], resultado=a["resultado"], tipo_acolhido=a["tipo_acolhido"], pena_meses=a["pena_meses"],
            condena=a["condena"] == "True", lei=a["lei"],
        ))
    return L


def taxa(linhas):
    c = [x for x in linhas if x["resultado"] not in ("", "sem sentença")]
    k = sum(x["condena"] for x in c)
    return dict(n=len(linhas), com_sentenca=len(c), condena=k, pct=round(100 * k / len(c), 1) if c else None,
                acolhido=dict(Counter(x["tipo_acolhido"] for x in c if x["condena"])),
                absolve=sum(x["resultado"] == "absolvição" for x in c))


def resumo(L):
    out = {}
    for e in ("CL", "FE"):
        E = [x for x in L if x["estrato"] == e]
        out[e] = dict(n=len(E), versao=dict(Counter(x["versao"] for x in E)), grupo=dict(Counter(x["grupo_versao"] for x in E)),
                      antecedentes=dict(Counter(x["antecedentes"] for x in E)), jovem=sum(x["jovem"] for x in E))
    out["versao"] = {v: dict(n=sum(x["versao"] == v for x in L), fonte=dict(Counter(x["fonte_versao"] for x in L if x["versao"] == v)))
                     for v in VERSOES}
    out["desfecho_por_grupo"] = {g: taxa([x for x in L if x["grupo_versao"] == g])
                                 for g in ("cessão admitida", "nega ou não reconhece", "ausente", "sem versão")}
    out["desfecho_por_versao"] = {v: taxa([x for x in L if x["versao"] == v]) for v in VERSOES}
    out["desfecho_por_antecedentes"] = {a: taxa([x for x in L if x["antecedentes"] == a])
                                        for a in ("primário", "reincidente ou maus antecedentes", "não dito")}
    ce = [x for x in L if x["versao"] in CESSAO]
    out["a_quem"] = dict(Counter(x["a_quem"] or "não diz" for x in ce))
    vs = sorted(v for v in (valor(x["valor_cessao"]) for x in ce if x["versao"] == "cedeu mediante pagamento") if v)
    out["valor_cessao"] = dict(valores=vs, mediana=statistics.median(vs) if vs else None,
                               casos={x["caso"]: x["valor_cessao"] for x in ce if x["valor_cessao"]})
    out["paga_conta_q4"] = {x["caso"]: x["paga_conta"] for x in L if x["paga_conta"]}
    out["cessao_detalhe"] = {x["caso"]: f'{x["versao"]} | {x["a_quem"] or "-"} | {x["valor_cessao"] or "-"} | {x["resultado"]} | {x["tipo_acolhido"]} | {x["trecho_versao"][:160]}'
                             for x in ce}
    out["anpp"] = dict(tratado=sum(x["cota_anpp"] for x in L), pena=sum(x["anpp_pena"] for x in L),
                       confissao=sum(x["anpp_confissao"] for x in L), antecedentes=sum(x["anpp_antecedentes"] for x in L),
                       ausencia=sum(x["anpp_ausencia"] for x in L), cap=dict(Counter(x["cap"] for x in L)))
    out["anpp_por_grupo"] = {g: dict(n=sum(x["grupo_versao"] == g for x in L), pena=sum(x["anpp_pena"] for x in L if x["grupo_versao"] == g))
                             for g in ("cessão admitida", "nega ou não reconhece", "ausente", "sem versão")}
    out["jovem"] = [x["caso"] for x in L if x["jovem"]]
    cond = [x for x in L if x["condena"]]
    out["antecedentes_condenados"] = dict(Counter(x["antecedentes"] for x in cond))
    out["total"] = dict(n=len(L), grupo=dict(Counter(x["grupo_versao"] for x in L)), antecedentes=dict(Counter(x["antecedentes"] for x in L)),
                        condena=taxa(L), confissao=sum(x["confissao"] for x in L),
                        fonte_versao=dict(Counter(x["fonte_versao"] for x in L)))
    return out


def main():
    L = base()
    os.makedirs(SAIDA, exist_ok=True)
    with open(os.path.join(SAIDA, "q7_titular.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(L[0].keys()))
        w.writeheader()
        w.writerows(L)
    R = resumo(L)
    json.dump(R, open(os.path.join(SAIDA, "q7_resumo.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if "-q" in sys.argv:
        return
    for k, v in R.items():
        print(f"\n===== {k}")
        for a, b in (v.items() if isinstance(v, dict) else [("", v)]):
            print(f"   {a}: {b}")


if __name__ == "__main__":
    main()
