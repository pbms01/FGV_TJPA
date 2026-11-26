"""Questão 7 no TJPA: a versão do titular da conta e o desfecho, com a posição do MP nas
alegações finais ao lado, e o confronto com o TJSP.

Uso (da raiz do repo): python3 scripts/analise_q7_titular_tjpa.py [-q]

Grava dados/analise/q7_titular_tjpa.csv (uma linha por denúncia sem duplicata da FE e do CL
codificada com papel de titular de conta ou misto) e q7_resumo_tjpa.json.

Decisões que não saltam aos olhos:
- Sem a tabela de nível da questão 1 no TJPA, a unidade é o papel da codificação assistida.
  O misto entra como segundo grupo, porque a codificação das denúncias e a das absolvições
  mostraram que parte dele é titular descrito como autor do ardil (atribuição sem prova além
  da conta). O TJSP, na questão 7, usa a unidade "só conta" da tabela de nível.
- A versão é a de scripts/titular_conta.py com TRIB=tjpa, conferida nos 67 casos com
  sentença (correções em VERSAO_MANUAL_TJPA). Nos casos sem sentença, a versão é só a da
  denúncia e não entra nas tabelas de desfecho.
- O desfecho é o da sentença por família (sentencas_tjpa.csv); a posição do MP é a de
  dados/analise/posicao_mp_fe.csv, que cobre a FE; no CL fica em branco.
"""
import csv
import json
import os
import sys
from collections import Counter, defaultdict

BASE = os.path.join(os.path.dirname(__file__), "..")
os.environ["TRIB"] = "tjpa"
sys.path.insert(0, os.path.dirname(__file__))
import titular_conta as tc  # noqa: E402

AN = os.path.join(BASE, "dados/analise")
CESSAO = {"cedeu mediante pagamento", "aceitou proposta de trabalho, renda ou crédito", "emprestou a alguém"}
GRUPOS = ("cessão admitida", "nega ou não reconhece", "ausente", "sem versão")
CONDENA = ("condenação", "procedência parcial")


def le(arq):
    with open(os.path.join(BASE, arq), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def grupo(v):
    return ("cessão admitida" if v in CESSAO else
            "nega ou não reconhece" if v in ("nega", "perdeu o controle ou não reconhece a conta") else
            "ausente" if v in ("silêncio", "não localizado ou revel") else "sem versão")


def base():
    cod = {r["numero"]: r for r in le("dados/extracao/codificacao_assistida_tjpa.csv")}
    sen = {r["numero"]: r for r in le("dados/extracao/sentencas_tjpa.csv") if not r["duplicata_de"]}
    mp = {r["numero"]: r["mp_posicao"] for r in le("dados/analise/posicao_mp_fe.csv") if r["tribunal"] == "TJPA"}
    fund = {r["numero"]: r["fundamento"] for r in le("dados/analise/fundamento_absolvicoes_fe.csv") if r["tribunal"] == "TJPA"}
    L = []
    for caso, n in tc._so_conta(("titular_conta", "misto")):
        x = tc.le(caso, n)
        s = sen.get(n, {})
        L.append(dict(caso=caso, numero=n, estrato=cod[n]["estrato"], papel=cod[n]["papel_denunciado"],
                      artificio=cod[n]["artificio"], versao=x["versao"], grupo_versao=grupo(x["versao"]),
                      fonte_versao=x["fonte_versao"], trecho_versao=x["trecho_versao"], a_quem=x["a_quem"],
                      valor_cessao=x["valor_cessao"], resultado=s.get("resultado", "") or "sem sentença",
                      mp_posicao=mp.get(n, ""), fundamento_absolvicao=fund.get(n, "")))
    return L


def taxa(g):
    c = [x for x in g if x["resultado"] in CONDENA + ("absolvição",)]
    k = sum(x["resultado"] in CONDENA for x in c)
    return f"{k} de {len(c)}" + (f" ({100 * k / len(c):.0f}%)".replace(".", ",") if c else "")


def tjsp():
    """A questão 7 do TJSP (só conta, FE e CL) com a posição do MP, que cobre a FE."""
    q7 = le("dados/analise/q7_titular.csv")
    mp = {r["numero"]: r["mp_posicao"] for r in le("dados/analise/posicao_mp_fe.csv") if r["tribunal"] == "TJSP"}
    for x in q7:
        x["mp_posicao"] = mp.get(x["numero"], "")
        x["resultado"] = x["resultado"] or "sem sentença"
    return q7


def resumo(L, S):
    out = {}
    for papel in ("titular_conta", "misto"):
        P = [x for x in L if x["papel"] == papel]
        com = [x for x in P if x["resultado"] in CONDENA + ("absolvição",)]
        out[papel] = dict(n=len(P), com_sentenca_de_merito=len(com), versao=dict(Counter(x["versao"] for x in P)),
                          desfecho_por_grupo={g: taxa([x for x in com if x["grupo_versao"] == g]) for g in GRUPOS})
    cess = [x for x in L if x["grupo_versao"] == "cessão admitida" and x["resultado"] in CONDENA + ("absolvição",)]
    out["cessao_admitida_detalhe"] = {x["caso"]: f'{x["papel"]} | {x["versao"]} | {x["resultado"]} | MP {x["mp_posicao"] or "-"} | {x["trecho_versao"][:140]}' for x in cess}
    fe = [x for x in L if x["estrato"] == "FE" and x["resultado"] in CONDENA + ("absolvição",)]
    tab = defaultdict(lambda: defaultdict(int))
    for x in fe:
        tab[x["grupo_versao"]][(x["mp_posicao"], x["resultado"] in CONDENA)] += 1
    out["fe_grupo_por_mp"] = {g: {f"MP {k[0]}, {'condena' if k[1] else 'absolve'}": v for k, v in d.items()} for g, d in tab.items()}
    sfe = [x for x in S if x["estrato"] == "FE" and x["resultado"] in CONDENA + ("absolvição",)]
    tab = defaultdict(lambda: defaultdict(int))
    for x in sfe:
        tab[x["grupo_versao"]][(x["mp_posicao"], x["resultado"] in CONDENA)] += 1
    out["tjsp_fe_grupo_por_mp"] = {g: {f"MP {k[0]}, {'condena' if k[1] else 'absolve'}": v for k, v in d.items()} for g, d in tab.items()}
    out["tjsp_desfecho_por_grupo"] = {g: taxa([x for x in S if x["grupo_versao"] == g]) for g in GRUPOS}
    return out


def imprime(L, S, R):
    print("Desfecho por versão do titular (condenação ou procedência parcial, entre sentenças de mérito)\n")
    print("| Versão | TJPA, titular | TJPA, misto | TJSP, só conta (q7) |")
    print("| --- | --- | --- | --- |")
    for g in GRUPOS:
        print(f"| {g} | {R['titular_conta']['desfecho_por_grupo'][g]} | {R['misto']['desfecho_por_grupo'][g]} | {R['tjsp_desfecho_por_grupo'][g]} |")
    print("\nFE: versão e posição do MP nas alegações finais (contagens de sentenças)\n")
    print("| Versão | TJPA: MP pede condenação (condena / absolve) | TJPA: MP pede absolvição | TJSP: MP pede condenação (condena / absolve) | TJSP: MP pede absolvição | TJSP: sem registro |")
    print("| --- | --- | --- | --- | --- | --- |")
    for g in GRUPOS:
        a = R["fe_grupo_por_mp"].get(g, {}); b = R["tjsp_fe_grupo_por_mp"].get(g, {})
        def c(d, mp, cond):
            return sum(v for k, v in d.items() if k.startswith(f"MP {mp},") and k.endswith("condena" if cond else "absolve"))
        pc = lambda d, m: f"{c(d, m, True) + c(d, 'parcial', True) * (m == 'condenacao')} / {c(d, m, False) + c(d, 'parcial', False) * (m == 'condenacao')}"
        print(f"| {g} | {pc(a, 'condenacao')} | {c(a, 'absolvicao', False)} | {pc(b, 'condenacao')} | {c(b, 'absolvicao', False)} | {c(b, 'nd', True)} / {c(b, 'nd', False)} |")
    print("\nCessão admitida no TJPA, com sentença de mérito:")
    for k, v in R["cessao_admitida_detalhe"].items():
        print(f"- {k}: {v}")


def main():
    L = base()
    S = tjsp()
    with open(os.path.join(AN, "q7_titular_tjpa.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(L[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(L)
    R = resumo(L, S)
    json.dump(R, open(os.path.join(AN, "q7_resumo_tjpa.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if "-q" not in sys.argv:
        imprime(L, S, R)


if __name__ == "__main__":
    main()
