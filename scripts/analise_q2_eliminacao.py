"""Questão 2 da análise criminológica: o que o teste de eliminação separa na amostra, e
se a capitulação acompanha a separação.

Para cada denúncia sem duplicata (198), aplica dois testes de eliminação e cruza o
resultado com a capitulação da denúncia e com o tipo acolhido na sentença. Grava
dados/analise/q2_eliminacao.csv e dados/analise/q2_resumo.json e imprime as tabelas.

A conduta é descrita nos dois eixos de scripts/eixos_mediacao.py (sistema e canal), com a
distância como agrupamento dos canais. Os dois testes derivam deles:
- sem o sistema informático, conectado ou não, inclusive rede interna: é o teste da
  mediação técnica relevante, que separa o crime informático próprio (desaparece) do
  impróprio (continua por outros meios);
- sem a internet (o teste de Wall): a coluna `wall` mostra onde ele classifica mal (os
  crimes próprios por contato físico ou por rede interna).

Decisões que não saltam aos olhos:
- A unidade de classificação é a conduta narrada na denúncia, não a do denunciado. A
  invasão feita por comparsa desconhecido conta como sistema-objeto mesmo quando a
  denúncia alcança só o titular da conta, porque a pergunta aqui é sobre o delito e não
  sobre o infrator. A separação entre as duas coisas é um dos resultados.
- Sistema-objeto: o dispositivo, a conta, a base de dados ou o sistema é o alvo da
  conduta (acesso, tomada, extração, alteração, destruição). A engenharia social em que a
  própria vítima entrega senha ou valida o aparelho do golpista não é sistema-objeto,
  como na codificação de base; esses casos vão para a lista de fronteira.
- Canal do ardil: internet quando o engano trafega por WhatsApp, rede social, site ou
  e-mail, e sempre na venda falsa, no falso investimento, na taxa de plataforma e no
  falso relacionamento, que nascem de anúncio ou perfil online mesmo quando a conversa
  segue por telefone; telefonia quando o contato descrito é só ligação ou SMS (o código
  "telefone" da base inclui aplicativo de mensagens não nomeado, o que pode puxar casos
  de internet para cá); presencial; postal (boleto sem canal descrito).
- Os percentuais são ponderados dentro do estrato. INV é censo (peso 1).
"""
import csv
import json
import os
import sys
from collections import Counter, defaultdict
from statistics import median

BASE = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.dirname(__file__))
from eixos_mediacao import CLASSES, OBJETO, eixos, le_codificacao, ponderada  # eixos comuns às questões 1 e 2

EXT = os.path.join(BASE, "dados/extracao")
SAIDA = os.path.join(BASE, "dados/analise")
ESTRATOS = ["INV", "CL", "FE"]

# Engenharia social que leva a vítima a ceder o acesso ao próprio sistema (fronteira entre
# estelionato e furto mediante fraude), lida nas notas.
FRONTEIRA_ACESSO = {"CL 33", "FE 115", "FE 36", "FE 51", "CL 48", "FE 84"}
# Denúncias INV com 154-A que imputam também outro crime, conferidas na capitulação (a
# coluna a_155 da extração dá falso positivo no INV 39). O INV 22 entra pelo art. 12 da
# Lei 9.609/98.
INV_154A_COM_OUTRO = {"INV 1", "INV 2", "INV 4", "INV 8", "INV 13", "INV 17", "INV 21", "INV 22", "INV 24",
                      "INV 26", "INV 28", "INV 32", "INV 33", "INV 34", "INV 35", "INV 41", "INV 45"}
def base():
    den = {x["numero"]: x for x in csv.DictReader(open(os.path.join(EXT, "denuncias_tjsp.csv"), encoding="utf-8"))}
    sent = {x["numero"]: x for x in csv.DictReader(open(os.path.join(EXT, "sentencas_amostra.csv"), encoding="utf-8"))}
    cod = le_codificacao()
    L = []
    for n, d in den.items():
        if d["duplicata_de"]:
            continue
        c, s = cod[n], sent.get(n, {})
        caso = f'{d["estrato"]} {d["ordem"]}'
        ex = eixos(caso, c)
        L.append(dict(
            caso=caso, numero=n, estrato=d["estrato"], peso=float(d["peso"]), artificio=c["artificio"],
            meio=c["meio_contato"], canal=ex["canal"], acesso=ex["acesso"],
            eixo_sistema=ex["sistema"], eixo_canal=ex["canal_eixo"], eixo_distancia=ex["distancia"],
            classe=ex["classe"], wall=ex["wall"], sem_internet=ex["sem_internet"], sem_sistema=ex["sem_sistema"],
            fronteira_acesso=caso in FRONTEIRA_ACESSO, papel=c["papel_denunciado"], contexto=c["contexto"],
            cap=d["tipo_capitulacao"], a_154A=d["a_154A"] == "True",
            resultado=s.get("resultado", ""), tipo_acolhido=s.get("tipo_acolhido", ""),
            pena_meses=float(s["pena_meses"]) if s.get("pena_meses") else None,
            condena=s.get("resultado", "") in ("condenação", "procedência parcial"),
        ))
    return L


def dispersao(linhas, campo):
    """Por artifício com 4 casos ou mais: tipo modal e sua participação, sem peso."""
    g = defaultdict(Counter)
    for x in linhas:
        if x[campo]:
            g[x["artificio"]][x[campo]] += 1
    out = {}
    for a, c in sorted(g.items(), key=lambda kv: -sum(kv[1].values())):
        tot = sum(c.values())
        if tot >= 4:
            modal, n = c.most_common(1)[0]
            out[a] = {"n": tot, "modal": modal, "participação do modal": round(100 * n / tot, 1),
                      "tipos distintos": len(c), "distribuição": dict(c.most_common())}
    return out


def main():
    L = base()
    os.makedirs(SAIDA, exist_ok=True)
    with open(os.path.join(SAIDA, "q2_eliminacao.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(L[0]))
        w.writeheader()
        for x in sorted(L, key=lambda x: (ESTRATOS.index(x["estrato"]), int(x["caso"].split()[1]))):
            w.writerow(x)
    dentro = [x for x in L if x["classe"] != "fora"]
    out = {"classe_por_estrato": {}, "testes_por_estrato": {}}
    for e in ESTRATOS:
        E = [x for x in dentro if x["estrato"] == e]
        out["classe_por_estrato"][e] = ponderada(E, lambda x: x["classe"], CLASSES)
        out["testes_por_estrato"][e] = {
            "sem internet": ponderada(E, lambda x: x["sem_internet"]),
            "sem sistema": ponderada(E, lambda x: x["sem_sistema"])}
    # Classe × capitulação (sem peso, porque cruza estratos)
    cruz = defaultdict(Counter)
    cruz_s = defaultdict(Counter)
    for x in dentro:
        cruz[x["classe"]][x["cap"]] += 1
        if x["condena"] and x["tipo_acolhido"]:
            cruz_s[x["classe"]][x["tipo_acolhido"]] += 1
    out["classe_x_capitulacao_denuncia"] = {k: dict(v.most_common()) for k, v in cruz.items()}
    out["classe_x_tipo_acolhido"] = {k: dict(v.most_common()) for k, v in cruz_s.items()}
    # Para onde vai o crime informático próprio, por papel do denunciado
    obj = [x for x in dentro if x["eixo_sistema"] == "objeto"]
    out["objeto_papel_acesso"] = {f'{a}': dict(Counter(x["papel"] for x in obj if x["acesso"] == a))
                                  for a in ("remoto", "local", "rede interna")}
    out["objeto_contexto_acesso"] = {a: dict(Counter(x["contexto"] for x in obj if x["acesso"] == a))
                                     for a in ("remoto", "local", "rede interna")}
    out["objeto_154A_por_papel"] = {p: f'{sum(x["cap"] == "154-A" for x in obj if x["papel"] == p)} de {sum(x["papel"] == p for x in obj)}'
                                    for p in sorted({x["papel"] for x in obj})}
    out["objeto_titular_cap"] = {x["caso"]: f'{x["cap"]} > {x["tipo_acolhido"] or x["resultado"]}'
                                 for x in obj if x["papel"] in ("titular_conta",)}
    # A qualificadora do meio em conduta presencial ou telefônica
    q = [x for x in dentro if x["cap"] == "171 §2º-A"]
    out["2A_denuncia_por_canal"] = dict(Counter(x["canal"] or ("objeto " + x["acesso"]) for x in q))
    # O critério do §2º-A é a distância (canal de comunicação), não a internet nem o sistema:
    # o desencontro com o próprio texto legal é a conduta próxima e o sistema-objeto.
    out["2A_denuncia_por_eixos"] = dict(Counter(f'{x["eixo_sistema"]} | {x["eixo_distancia"]}' for x in q))
    out["eixos_por_estrato"] = {e: {
        "sistema": ponderada([x for x in dentro if x["estrato"] == e], lambda x: x["eixo_sistema"]),
        "canal": ponderada([x for x in dentro if x["estrato"] == e], lambda x: x["eixo_canal"]),
        "distância": ponderada([x for x in dentro if x["estrato"] == e], lambda x: x["eixo_distancia"]),
        "Wall": ponderada([x for x in dentro if x["estrato"] == e], lambda x: x["wall"])} for e in ESTRATOS}
    out["2A_presencial"] = {x["caso"]: f'{x["artificio"]} > {x["tipo_acolhido"] or x["resultado"]}'
                            for x in q if x["canal"] == "presencial"}
    out["2A_telefonia"] = {x["caso"]: f'{x["artificio"]} > {x["tipo_acolhido"] or x["resultado"]}'
                           for x in q if x["canal"] == "telefonia"}
    # Dispersão da capitulação por artifício
    out["dispersao_denuncia"] = dispersao(dentro, "cap")
    out["dispersao_sentenca"] = dispersao([x for x in dentro if x["condena"]], "tipo_acolhido")
    # Fronteira furto × estelionato na subtração por sistema
    fr = [x for x in dentro if x["fronteira_acesso"] or x["artificio"] in ("invasao_sistema_bancario", "roubo_celular_invasao", "maquininha")]
    out["fronteira_furto_estelionato"] = {x["caso"]: f'{x["artificio"]} | {x["cap"]} > {x["tipo_acolhido"] or x["resultado"]}' for x in fr}
    # O 154-A na sentença: imputação única ou ao lado de outro crime
    sent = {x["caso"]: x for x in csv.DictReader(open(os.path.join(EXT, "sentencas_amostra.csv"), encoding="utf-8"))}
    r154 = defaultdict(Counter)
    det = defaultdict(list)
    for x in L:
        if x["estrato"] != "INV" or not x["a_154A"]:
            continue
        s = sent[x["caso"]]
        if s["acolhe_154A"] == "True" or s["tipo_acolhido"] == "154-A":
            r = "154-A acolhido"
        elif x["condena"] and not s["tipo_acolhido"]:
            r = "indeterminado"  # INV 8: só o movimento
        elif x["condena"]:
            r = "condena pelo outro crime e não pelo 154-A"
        else:
            r = "absolvição integral"
        k = "com outro crime" if x["caso"] in INV_154A_COM_OUTRO else "154-A sozinho"
        r154[k][r] += 1
        det[f"{k} | {r}"].append(x["caso"])
    out["154A_na_sentenca"] = {k: dict(v) for k, v in r154.items()}
    out["154A_na_sentenca_casos"] = dict(det)
    # Pena por tipo acolhido (sem peso), para comparar o crime novo com o antigo qualificado pelo meio
    pen = defaultdict(list)
    for x in dentro:
        if x["condena"] and x["pena_meses"] and x["tipo_acolhido"] in ("154-A", "171 §2º-A", "155 §4º-B", "171 outro"):
            pen[x["tipo_acolhido"]].append(x["pena_meses"])
    out["pena_mediana_por_tipo"] = {k: f"n={len(v)}, mediana {median(v)} meses" for k, v in pen.items()}
    json.dump(out, open(os.path.join(SAIDA, "q2_resumo.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if "-q" in sys.argv:
        return
    for k, v in out.items():
        print(f"\n== {k}")
        if isinstance(v, dict):
            for k2, v2 in v.items():
                print(f"   {k2}: {v2}")
        else:
            print("  ", v)


if __name__ == "__main__":
    main()
