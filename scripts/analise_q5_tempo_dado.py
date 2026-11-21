"""Questão 5 da análise criminológica (linha 4.4): quanto tempo separa o fato da denúncia,
de que custodiante vem o dado que a denúncia narra, o que a cota ainda pede, e como isso se
compara aos prazos legais de guarda (6 meses para os registros de acesso a aplicações e 1
ano para os de conexão, no Marco Civil; 5 anos para os registros de ligações, na Lei
12.850, e para cadastros e transações das instituições do art. 9º da Lei 9.613).

Lê as denúncias com scripts/tempo_dado.py (validação: `python3 scripts/tempo_dado.py
valida`), cruza com a codificação, os eixos e o nível da questão 1, e grava
dados/analise/q5_tempo_dado.csv (uma linha por denúncia) e q5_resumo.json. `-q` grava sem
imprimir.

Decisões que não saltam aos olhos:
- O intervalo medido é o do fato à denúncia. Ele não é o tempo até o pedido de dado, que
  corre dentro do inquérito e a denúncia raramente data; é o teto desse tempo e é,
  exatamente, a idade do dado no dia em que a cota pede alguma coisa.
- Faixas e percentuais são ponderados dentro do estrato, como nas questões anteriores. Por
  canal, nível e prisão no ato os números são contagens simples das três camadas somadas,
  com mediana e quartis em meses de 30,44 dias, porque o canal atravessa os estratos.
- "Preso no ato" é a triagem de termos da questão 1 (flagrante, foi preso, abordado,
  surpreendido), não uma codificação, corrigida em PRESO_MANUAL nos casos lidos por inteiro.
"""
import csv
import json
import os
import re
import statistics
import sys
from collections import Counter

BASE = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.dirname(__file__))
from analise_q1_alcance import INDICIOS, NIVEL  # noqa: E402
from eixos_mediacao import eixos, le_codificacao, ponderada  # noqa: E402
import tempo_dado as td  # noqa: E402

EXT = os.path.join(BASE, "dados/extracao")
SAIDA = os.path.join(BASE, "dados/analise")
ESTRATOS = ["INV", "CL", "FE"]
FAIXAS = ["até 6 meses", "6 a 12 meses", "12 a 24 meses", "24 a 60 meses", "mais de 60 meses"]
CANAIS = ["internet", "telefonia", "presencial", "correio", "sem contato", "sistema-objeto"]
FONTES = ["banco", "vitima", "operadora", "plataforma", "conexao", "dispositivo", "camera"]
MES = 30.44

# Correções da triagem "preso no ato" lidas no exame em aula (dados/aula/divergencias.csv).
# CL 56: o "flagrante" da denúncia é o de receptação e de arma, na busca, dois meses depois
# do golpe. FE 105: a denúncia narra a parada do carro pela PM logo depois do golpe sem usar
# nenhum dos termos da triagem.
PRESO_MANUAL = {"CL 56": False, "FE 105": True}


def faixa(dias):
    if dias is None:
        return "sem data"
    m = dias / MES
    return FAIXAS[0] if m <= 6 else FAIXAS[1] if m <= 12 else FAIXAS[2] if m <= 24 else FAIXAS[3] if m <= 60 else FAIXAS[4]


def base():
    den = [d for d in csv.DictReader(open(os.path.join(EXT, "denuncias_tjsp.csv"), encoding="utf-8")) if not d["duplicata_de"]]
    sent = {x["numero"]: x for x in csv.DictReader(open(os.path.join(EXT, "sentencas_amostra.csv"), encoding="utf-8"))}
    cod = le_codificacao()
    L = []
    for d in den:
        caso, n_ = f'{d["estrato"]} {d["ordem"]}', d["numero"]
        c, s = cod[n_], sent.get(n_)
        ex = eixos(caso, c)
        if d["estrato"] == "INV":
            nivel = c["papel_denunciado"]
        elif c["papel_denunciado"] == "titular_conta":
            nivel = "só conta"
        else:
            nivel = NIVEL[caso][0]
        seg = json.load(open(os.path.join(EXT, "segmentos", f"{n_}.json"), encoding="utf-8"))
        texto = re.sub(r"\s+", " ", seg.get("narrativa", "") + " " + seg.get("cota", ""))
        x = td.le(caso, n_)
        dias = x["dias"]
        L.append(dict(
            caso=caso, numero=n_, estrato=d["estrato"], peso=float(d["peso"]), fora=ex["classe"] == "fora",
            sistema=ex["sistema"], canal="sistema-objeto" if ex["sistema"] == "objeto" else ex["canal_eixo"],
            acesso=ex["canal_eixo"] if ex["sistema"] == "objeto" else "", meio=c["meio_contato"], artificio=c["artificio"],
            papel=c["papel_denunciado"], nivel=nivel, preso_no_ato=PRESO_MANUAL.get(caso, bool(re.search(INDICIOS["flagrante"], texto, re.I))),
            data_fato=x["data_fato"].isoformat() if x["data_fato"] else "", precisao=x["precisao"], fonte_data=x["fonte_data"],
            data_denuncia=x["data_denuncia"].isoformat() if x["data_denuncia"] else "", fonte_data_denuncia=x["fonte_data_denuncia"],
            dias=dias, meses=round(dias / MES, 1) if dias is not None else None, faixa=faixa(dias),
            alem_6m=dias is not None and dias > 6 * MES, alem_12m=dias is not None and dias > 12 * MES,
            alem_5a=dias is not None and dias > 60 * MES,
            **{"fonte_" + k: x["fonte_" + k] for k in FONTES},
            terceiro=x["terceiro"], terceiro_dado=x["terceiro_dado"], terceiro_efeito=x["terceiro_efeito"],
            pedido_cota=x["pedido_cota"], pedido_cota_alvo=x["pedido_cota_alvo"], pedido_preservacao=x["pedido_preservacao"],
            resultado=s["resultado"] if s else "sem sentença",
        ))
    return L


def tempo(linhas):
    v = sorted(x["dias"] / MES for x in linhas if x["dias"] is not None)
    if not v:
        return {}
    q = statistics.quantiles(v, n=4) if len(v) >= 4 else [v[0], statistics.median(v), v[-1]]
    return dict(n=len(v), mediana=round(statistics.median(v), 1), q1=round(q[0], 1), q3=round(q[2], 1),
                alem_6m=sum(m > 6 for m in v), alem_12m=sum(m > 12 for m in v), alem_24m=sum(m > 24 for m in v),
                alem_5a=sum(m > 60 for m in v))


def resumo(L):
    out = {}
    T = [x for x in L if not x["fora"]]
    for e in ESTRATOS:
        E = [x for x in T if x["estrato"] == e]
        C = [x for x in E if x["dias"] is not None]
        o = out[e] = {"denuncias": len(E), "com_data": len(C)}
        o["tempo"] = tempo(C)
        o["faixa"] = ponderada(C, lambda x: x["faixa"], FAIXAS)
        o["alem_6m"] = ponderada(C, lambda x: x["alem_6m"])
        o["alem_12m"] = ponderada(C, lambda x: x["alem_12m"])
        o["precisao"] = dict(Counter(x["precisao"] for x in C))
        o["fontes"] = {k: ponderada(E, lambda x, k=k: x["fonte_" + k]).get(True, (0, 0.0)) for k in FONTES}
    out["por_canal"] = {k: tempo([x for x in T if x["canal"] == k]) for k in CANAIS}
    out["por_nivel"] = {k: tempo([x for x in T if x["nivel"] == k and x["estrato"] != "INV"])
                        for k in ["só conta", "elo logístico", "autor remoto", "autor presencial"]}
    out["preso_no_ato"] = {str(k): tempo([x for x in T if x["preso_no_ato"] == k]) for k in (True, False)}
    out["fontes_por_canal"] = {k: {f: sum(x["fonte_" + f] for x in T if x["canal"] == k) for f in FONTES} | {"n": sum(x["canal"] == k for x in T)}
                               for k in CANAIS}
    out["terceiro"] = {x["caso"]: f'{x["terceiro"]} | {x["terceiro_efeito"]} | canal {x["canal"]} | {x["meses"]} meses | {x["terceiro_dado"]}'
                       for x in T if x["terceiro"]}
    out["terceiro_efeito"] = dict(Counter(x["terceiro_efeito"] for x in T if x["terceiro"]))
    out["terceiro_por_canal"] = dict(Counter(x["canal"] for x in T if x["terceiro"]))
    out["pedido_cota"] = {x["caso"]: f'{x["pedido_cota"]} | {x["meses"]} meses | {x["pedido_cota_alvo"]}' for x in T if x["pedido_cota"]}
    out["pedido_preservacao"] = [x["caso"] for x in T if x["pedido_preservacao"]]
    so = [x for x in T if x["nivel"] == "só conta"]
    out["so_conta"] = dict(n=len(so), banco=sum(x["fonte_banco"] for x in so),
                           so_vitima=sum(x["fonte_vitima"] and not x["fonte_banco"] for x in so),
                           nenhum=sum(not x["fonte_vitima"] and not x["fonte_banco"] for x in so))
    internet_meio = [x for x in T if x["canal"] == "internet"]
    out["internet_meio"] = dict(n=len(internet_meio), plataforma=sum(x["fonte_plataforma"] for x in internet_meio),
                                conexao=sum(x["fonte_conexao"] for x in internet_meio),
                                operadora=sum(x["fonte_operadora"] for x in internet_meio),
                                meio=dict(Counter(x["meio"] for x in internet_meio)),
                                alem_6m=sum(x["alem_6m"] for x in internet_meio), alem_12m=sum(x["alem_12m"] for x in internet_meio),
                                com_data=sum(x["dias"] is not None for x in internet_meio))
    out["total"] = dict(denuncias=len(T), com_data=sum(x["dias"] is not None for x in T), tempo=tempo(T),
                        sem_data=[x["caso"] for x in T if x["dias"] is None],
                        data_manual=[x["caso"] for x in T if x["fonte_data"] == "manual"],
                        precisao=dict(Counter(x["precisao"] for x in T if x["dias"] is not None)),
                        data_denuncia=dict(Counter(x["fonte_data_denuncia"] for x in T)))
    return out


def main():
    L = base()
    os.makedirs(SAIDA, exist_ok=True)
    with open(os.path.join(SAIDA, "q5_tempo_dado.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(L[0].keys()))
        w.writeheader()
        w.writerows(L)
    R = resumo(L)
    json.dump(R, open(os.path.join(SAIDA, "q5_resumo.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if "-q" in sys.argv:
        return
    for k, v in R.items():
        print(f"\n===== {k}")
        if isinstance(v, dict):
            for a, b in v.items():
                print(f"   {a}: {b}")
        else:
            print(f"   {v}")


if __name__ == "__main__":
    main()
