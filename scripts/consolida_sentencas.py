"""Consolida as sentenças da amostra do TJSP.

Lê dados/extracao/sentencas_amostra.csv (uma linha por processo) e cruza com
dados/extracao/denuncias_tjsp.csv (capitulação da denúncia, duplicatas) e
dados/codex/status_sentencas.csv (cobertura). Imprime as tabelas em texto e grava
dados/extracao/resumo_sentencas.json, que o LEIAME e o HANDOFF citam.

Decisões que não saltam aos olhos:
- A unidade é a denúncia sem duplicatas, com o peso amostral do processo, e os
  percentuais são ponderados dentro do estrato, como na distribuição da capitulação.
  As duplicatas (INV 7 e INV 3) saem das contagens; os 29 casos da matriz entram,
  porque foram tirados da própria amostra.
- "Ao menos um réu condenado" soma condenação e procedência parcial. A procedência
  parcial do leitor por regras cobre tanto o réu condenado em parte das imputações
  quanto o corréu absolvido; a distinção fica na nota.
- A variável da Lei 15.397/2026 (DOU de 04/05/2026) é codificada aqui, à mão, para
  as sentenças que mencionam a lei sem aplicar o 171 §2º, VII, porque o motivo da
  recusa só se lê no texto. As demais saem da capitulação acolhida e da menção.
"""
import csv
import json
import os
import sys
from collections import Counter, defaultdict
from statistics import median

BASE = os.path.join(os.path.dirname(__file__), "..")
SENT = os.path.join(BASE, "dados/extracao/sentencas_amostra.csv")
DEN = os.path.join(BASE, "dados/extracao/denuncias_tjsp.csv")
STATUS = os.path.join(BASE, "dados/codex/status_sentencas.csv")
SAIDA = os.path.join(BASE, "dados/extracao/resumo_sentencas.json")
VIGENCIA = "2026-05-04"  # publicação da Lei 15.397/2026 no DOU
ESTRATOS = ["INV", "CL", "FE"]

# Sentenças posteriores à lei que a mencionam sem aplicar o §2º, VII (lidas no texto).
# recusa: afasta o inciso para o réu condenado; absolve: o fundamento da absolvição
# alcança também o inciso; reforço: cita a lei só como argumento sobre o dolo.
LEI_MANUAL = {
    "CL 10": "recusa", "CL 16": "recusa", "CL 28": "recusa", "CL 48": "recusa", "CL 49": "recusa", "CL 33": "recusa", "CL 36": "recusa",
    "CL 57": "recusa", "FE 77": "recusa", "FE 72": "recusa", "CL 31": "absolve", "CL 37": "reforço",
}


def carrega():
    den = {x["numero"]: x for x in csv.DictReader(open(DEN, encoding="utf-8"))}
    sent = list(csv.DictReader(open(SENT, encoding="utf-8")))
    st = {x["numero"]: x for x in csv.DictReader(open(STATUS, encoding="utf-8"))}
    return den, sent, st


def pct(c, tot):
    return round(100 * c / tot, 1) if tot else 0.0


def ponderada(linhas, chave):
    """Distribuição ponderada pelo peso: {categoria: (n, %)}."""
    soma, n = defaultdict(float), Counter()
    for x in linhas:
        k = chave(x)
        soma[k] += float(x["peso"])
        n[k] += 1
    tot = sum(soma.values())
    return {k: (n[k], pct(soma[k], tot)) for k in sorted(soma, key=lambda k: -soma[k])}


def lei_15397(x):
    data = x["data_mov"] or ""
    if not data or data < VIGENCIA:
        return "anterior à lei"
    if x["tipo_acolhido"] == "171 §2º VII":
        return "aplica"
    if x["caso"] in LEI_MANUAL:
        return LEI_MANUAL[x["caso"]]
    if x["documentos"] == "0":  # só o dispositivo do DJEN: a fundamentação não foi lida
        return "só dispositivo"
    if x["menciona_lei_15397"] in ("True", "1"):
        return "menciona, sem codificar"  # aparece se uma sentença nova não entrou no dicionário
    return "sem menção"


def mudanca(cap, aco, res):
    if res not in ("condenação", "procedência parcial") or not aco:
        return None
    if aco == cap:
        return "mantém"
    if aco == "171 §2º VII":
        return "para 171 §2º VII"
    if cap == "171 §2º-A" and aco.startswith("171"):
        return "afasta o §2º-A"
    if cap == "171 outro" and aco == "171 §2º-A":
        return "acrescenta o §2º-A"
    return f"{cap} → {aco}"


def main():
    den, sent, st = carrega()
    dup = {n for n, x in den.items() if x.get("duplicata_de")}
    base = [x for x in sent if x["numero"] not in dup]
    for x in base:
        x["cap"] = den[x["numero"]]["tipo_capitulacao"]
    amostra = {e: [n for n, x in den.items() if x["estrato"] == e and n not in dup] for e in ESTRATOS}
    out = {"vigencia_lei_15397": VIGENCIA, "estratos": {}}

    for e in ESTRATOS:
        L = [x for x in base if x["estrato"] == e]
        lidas = [x for x in L if x["resultado"] and x["resultado"] != "indeterminado"]
        cobertura = Counter()
        for n in amostra[e]:
            x = next((y for y in L if y["numero"] == n), None)
            s = st.get(n, {}).get("status", "")
            if x is None:
                cobertura["sem sentença lida (" + (s or "pendente") + ")"] += 1
            elif x["conferido"] == "matriz":
                cobertura["matriz (lida à mão)"] += 1
            elif s == "ok_djen":
                cobertura["dispositivo pelo DJEN"] += 1
            else:
                cobertura["texto pelo Codex"] += 1
        res = ponderada(lidas, lambda x: x["resultado"])
        cond = [x for x in lidas if x["resultado"] in ("condenação", "procedência parcial")]
        acolhido = ponderada([x for x in cond if x["tipo_acolhido"]], lambda x: x["tipo_acolhido"])
        mud = ponderada([x for x in cond if mudanca(x["cap"], x["tipo_acolhido"], x["resultado"])],
                        lambda x: mudanca(x["cap"], x["tipo_acolhido"], x["resultado"]))
        cruz = defaultdict(Counter)
        for x in cond:
            cruz[x["cap"]][x["tipo_acolhido"] or "(não lido)"] += 1
        penas = defaultdict(list)
        for x in cond:
            if x["pena_meses"]:
                penas[x["tipo_acolhido"] or "(não lido)"].append(float(x["pena_meses"]))
        regime = ponderada([x for x in cond if x["regime"]], lambda x: x["regime"])
        lei = Counter(lei_15397(x) for x in lidas)
        # Divergência de polaridade: o movimento diz procedência e o texto absolve, ou o
        # contrário. Procedência contra procedência parcial não conta como erro, porque o
        # leitor chama de parcial também a sentença que absolve um corréu; fica só a contagem.
        mov, parcial_trocada = [], 0
        for x in lidas:
            m, r = x["movimento"], x["resultado"]
            if not m:
                continue
            condena = r in ("condenação", "procedência parcial")
            if (m.startswith("Procedência") and not condena) or (m == "Improcedência" and condena):
                mov.append(f'{x["caso"]}: movimento {m}, texto {r}')
            elif condena and (m == "Procedência") != (r == "condenação"):
                parcial_trocada += 1
        out["estratos"][e] = dict(
            denuncias=len(amostra[e]), sentencas_lidas=len(lidas), cobertura=dict(cobertura),
            resultado=res, ao_menos_um_condenado=pct(sum(v[1] for k, v in res.items()
                                                       if k in ("condenação", "procedência parcial")), 100),
            tipo_acolhido=acolhido, mudanca_capitulacao=mud,
            cruzamento={k: dict(v) for k, v in cruz.items()},
            pena_mediana_meses={k: (len(v), median(v)) for k, v in penas.items() if v},
            regime=regime, lei_15397=dict(lei), movimento_diverge=mov,
            movimento_parcial_trocada=parcial_trocada)

    json.dump(out, open(SAIDA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if "-q" in sys.argv:
        return
    for e, o in out["estratos"].items():
        print(f"\n== {e}: {o['sentencas_lidas']} sentenças lidas de {o['denuncias']} denúncias")
        print("cobertura:", o["cobertura"])
        print("resultado:", {k: f"{n} ({p}%)" for k, (n, p) in o["resultado"].items()},
              "| ao menos um condenado", o["ao_menos_um_condenado"], "%")
        print("acolhido:", {k: f"{n} ({p}%)" for k, (n, p) in o["tipo_acolhido"].items()})
        print("mudança:", {k: f"{n} ({p}%)" for k, (n, p) in o["mudanca_capitulacao"].items()})
        print("pena mediana:", o["pena_mediana_meses"])
        print("regime:", {k: f"{n} ({p}%)" for k, (n, p) in o["regime"].items()})
        print("Lei 15.397:", o["lei_15397"])
        print("movimento x texto:", o["movimento_diverge"], "| parcial trocada", o["movimento_parcial_trocada"])


if __name__ == "__main__":
    main()
