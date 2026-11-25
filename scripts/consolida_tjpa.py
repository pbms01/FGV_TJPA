"""Consolida a extração do TJPA (fase 2) e a põe lado a lado com o TJSP (fase 1).

    python3 scripts/consolida_tjpa.py        imprime as tabelas e grava dados/extracao/resumo_tjpa.json

Lê dados/extracao/denuncias_tjpa.csv e sentencas_tjpa.csv e, para o TJSP, denuncias_tjsp.csv,
sentencas_amostra.csv e as mesmas regras de scripts/consolida_sentencas.py.

Decisões que não saltam aos olhos:
- O TJPA é censo da lista do DJEN: percentuais simples, sem peso. O TJSP é amostra: percentuais
  ponderados dentro do estrato, como na fase 1. A comparação é de proporções, não de volumes.
- A unidade é a denúncia sem duplicatas: cada família de desmembramento conta uma vez, pela
  denúncia e pela sentença do processo originário (o mais antigo). As sentenças dos outros membros
  julgam réus distintos e ficam registradas em sentencas_tjpa.csv, fora desta conta; o número por
  processo vai junto, para mostrar o que a regra tira.
- As cinco sentenças sem denúncia gravada (status `so_sentenca`) entram nas tabelas de sentença e
  ficam fora das de capitulação e da mudança de capitulação.
- As decisões terminativas sem mérito (rejeição da denúncia, declinação de competência, extinção
  por decadência ou continência) entram na distribuição do resultado com rótulo próprio e não contam
  como absolvição; "ao menos um réu condenado" soma condenação e procedência parcial, como na fase 1.
- Ressalvas do TJPA que acompanham toda leitura destas tabelas: o corpus de denúncias inclui ações
  penais sem sentença (ao contrário do cjpg do TJSP, que só lista sentenciados), e a lista do DJEN
  subestima os julgados, porque 25 sentenças do grupo 2 não estavam classificadas como sentença no
  DJEN e foram achadas no Codex.
"""
import csv
import json
import os
import sys
from collections import Counter, defaultdict
from statistics import median

sys.path.insert(0, "scripts")
import consolida_sentencas as cs  # noqa: E402  (ponderada, pct, mudanca)

EXT = os.path.join("dados", "extracao")
SAIDA = os.path.join(EXT, "resumo_tjpa.json")
ESTRATOS = ["INV", "CL", "FE"]
VIGENCIA = cs.VIGENCIA
COND = ("condenação", "procedência parcial")


def ler(p):
    return list(csv.DictReader(open(os.path.join(EXT, p), encoding="utf-8")))


def dist(linhas, chave, peso=False):
    """{categoria: (n, %)}; com peso=False todos os pesos valem 1 (censo)."""
    if not peso:
        linhas = [dict(x, peso="1") for x in linhas]
    return cs.ponderada(linhas, chave)


def bloco_sentencas(L, cap_de, peso=False):
    lidas = [x for x in L if x["resultado"] and x["resultado"] != "indeterminado"]
    res = dist(lidas, lambda x: x["resultado"], peso)
    cond = [x for x in lidas if x["resultado"] in COND]
    acolhido = dist([x for x in cond if x["tipo_acolhido"]], lambda x: x["tipo_acolhido"], peso)
    com_cap = [x for x in cond if cap_de.get(x["numero"]) and cs.mudanca(cap_de[x["numero"]], x["tipo_acolhido"], x["resultado"])]
    mud = dist(com_cap, lambda x: cs.mudanca(cap_de[x["numero"]], x["tipo_acolhido"], x["resultado"]), peso)
    penas = defaultdict(list)
    for x in cond:
        if x["pena_meses"]:
            penas[x["tipo_acolhido"] or "(não lido)"].append(float(x["pena_meses"]))
    regime = dist([x for x in cond if x["regime"]], lambda x: x["regime"], peso)
    w = (lambda x: float(x["peso"])) if peso else (lambda x: 1.0)
    # percentual exato (a fase 1 somava os percentuais já arredondados; a diferença é de 0,1 ponto)
    ao_menos = cs.pct(sum(w(x) for x in cond), sum(w(x) for x in lidas))
    return dict(sentencas_lidas=len(lidas), resultado=res,
                ao_menos_um_condenado=ao_menos,
                tipo_acolhido=acolhido, mudanca_capitulacao=mud,
                pena_mediana_meses={k: (len(v), round(median(v), 1)) for k, v in sorted(penas.items(), key=lambda kv: -len(kv[1]))},
                regime=regime, sem_pena_lida=sum(1 for x in cond if not x["pena_meses"]))


def lei_tjpa(x):
    """Variável da Lei 15.397/2026 pela data do documento da sentença, como a fase 1 fez pela data
    do movimento; a codificação das menções sem aplicação fica para a leitura."""
    d = x.get("data_doc") or ""
    if not d or d < VIGENCIA:
        return "anterior à lei"
    if x["tipo_acolhido"] == "171 §2º VII":
        return "aplica"
    if x["menciona_lei_15397"] in ("True", "1"):
        return "menciona, sem codificar"
    return "sem menção"


def tjpa():
    den = ler("denuncias_tjpa.csv")
    sent = ler("sentencas_tjpa.csv")
    base_den = [x for x in den if not x["duplicata_de"]]
    dup = {x["numero"] for x in den if x["duplicata_de"]}
    cap_de = {x["numero"]: x["tipo_capitulacao"] for x in den}
    base_sent = [x for x in sent if x["numero"] not in dup]
    out = {"unidade": "denúncia sem duplicatas (família conta uma vez); censo, % simples", "estratos": {}}
    for e in ESTRATOS + ["total"]:
        D = [x for x in base_den if e == "total" or x["estrato"] == e]
        S = [x for x in base_sent if e == "total" or x["estrato"] == e]
        Sp = [x for x in sent if e == "total" or x["estrato"] == e]
        b = dict(denuncias=len(D), processos_com_denuncia=sum(1 for x in den if e == "total" or x["estrato"] == e),
                 capitulacao=dist(D, lambda x: x["tipo_capitulacao"]),
                 denuncias_com_sentenca=sum(1 for x in D if any(s["numero"] == x["numero"] for s in S)),
                 sentencas_por_processo=len(Sp), sentencas_so_sentenca=sum(1 for x in S if x["status_coleta"] == "so_sentenca"))
        b.update(bloco_sentencas(S, cap_de))
        b["lei_15397"] = dict(Counter(lei_tjpa(x) for x in S if x["resultado"] != "indeterminado"))
        b["operacoes"] = dict(Counter(x["operacao"] for x in D if x["operacao"]))
        out["estratos"][e] = b
    return out


def tjsp():
    den = ler("denuncias_tjsp.csv")
    sent = ler("sentencas_amostra.csv")
    dup = {x["numero"] for x in den if x["duplicata_de"]}
    base = [x for x in den if not x["duplicata_de"]]
    cap_de = {x["numero"]: x["tipo_capitulacao"] for x in den}
    out = {"unidade": "denúncia sem duplicatas, % ponderado dentro do estrato", "estratos": {}}
    for e in ESTRATOS:
        D = [x for x in base if x["estrato"] == e]
        S = [x for x in sent if x["estrato"] == e and x["numero"] not in dup]
        b = dict(denuncias=len(D), capitulacao=dist(D, lambda x: x["tipo_capitulacao"], peso=True))
        b.update(bloco_sentencas(S, cap_de, peso=True))
        out["estratos"][e] = b
    return out


def top(d, k=4):
    return "; ".join(f"{c} {v[1]}%" for c, v in list(d.items())[:k]) or "-"


def imprime(pa, sp):
    print("Capitulação da denúncia (sem duplicatas)")
    for e in ESTRATOS:
        a, b = pa["estratos"][e], sp["estratos"][e]
        print(f"  {e:4} TJPA {a['denuncias']:3}: {top(a['capitulacao'])}")
        print(f"       TJSP {b['denuncias']:3}: {top(b['capitulacao'])}")
    t = pa["estratos"]["total"]
    print(f"  total TJPA {t['denuncias']}: {top(t['capitulacao'], 6)}")
    print("\nSentenças (família uma vez; TJPA inclui as 5 sem denúncia gravada)")
    for e in ESTRATOS + ["total"]:
        a = pa["estratos"][e]
        print(f"  {e:5} TJPA {a['sentencas_lidas']:3} lidas ({a['sentencas_por_processo']} por processo): ao menos um condenado "
              f"{a['ao_menos_um_condenado']}% | resultado {top(a['resultado'], 6)}")
        print(f"        acolhido {top(a['tipo_acolhido'])} | mudança {top(a['mudanca_capitulacao'], 3)} | regime {top(a['regime'], 3)}")
        print(f"        pena mediana {dict(list(a['pena_mediana_meses'].items())[:4])} | sem pena lida {a['sem_pena_lida']}")
        if e in sp["estratos"]:
            b = sp["estratos"][e]
            print(f"        TJSP {b['sentencas_lidas']} lidas: ao menos um condenado {b['ao_menos_um_condenado']}% | acolhido {top(b['tipo_acolhido'])}")
            print(f"        TJSP mudança {top(b['mudanca_capitulacao'], 3)} | regime {top(b['regime'], 3)} | pena mediana {dict(list(b['pena_mediana_meses'].items())[:3])}")
    print("\nLei 15.397/2026 nas sentenças do TJPA:", pa["estratos"]["total"]["lei_15397"])
    print("Operações (denúncias distintas):", pa["estratos"]["total"]["operacoes"])


def main():
    pa, sp = tjpa(), tjsp()
    json.dump({"tjpa": pa, "tjsp": sp}, open(SAIDA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    imprime(pa, sp)


if __name__ == "__main__":
    main()
