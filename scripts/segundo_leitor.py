"""Segundo leitor: compara a codificação independente com a primeira leitura e mede a
concordância.

O segundo leitor recebeu, às cegas, os textos de 34 denúncias (codificação de artifício,
meio, papel e indicadores) e de 50 sentenças (dispositivo, reparação do art. 387, IV,
consequências do crime e pedido na denúncia), com identificadores neutros e o livro de
códigos de dados/conferencia/livro_codigos_*.md, sem acesso às codificações da primeira
leitura. A amostra e a correspondência entre identificador e caso estão em
dados/conferencia/mapa_segundo_leitor.json; as respostas, em dados/conferencia/segundo_leitor_*.csv.

Uso (da raiz do repo):

    python3 scripts/segundo_leitor.py          # grava dados/conferencia/concordancia.csv e resumo, imprime
    python3 scripts/segundo_leitor.py -q

Decisões que não saltam aos olhos:
- A amostra das denúncias soma 24 sorteadas da codificação assistida (8 por estrato,
  semente 20261122) e os 10 casos de fronteira do LEIAME. A das sentenças soma 24 sorteadas
  entre as lidas só pelo leitor de regras (conferido=auto; no INV, todas as 8), os 14 casos
  de que a questão 3 depende mais (correções à mão, dano não econômico, dano moral) e 15
  condenações sorteadas (5 por estrato). Os casos forçados entram na concordância, mas são
  mais difíceis que a média; o resumo dá a concordância também só nos sorteados.
- A concordância é a proporção de casos iguais e, nos campos categóricos, o kappa de Cohen.
  Valores em reais concordam quando diferem em até R$ 1 ou 1%; a pena, em até meio mês.
- Os campos de múltipla escolha (fundamentos da negativa, danos nas consequências) são
  comparados como conjuntos.
- A primeira leitura das sentenças vem de sentencas_amostra.csv (dispositivo) e de
  dados/analise/q3_dano.csv (reparação, consequências, pedido); a da codificação, das três
  rodadas de codificação (manual r1 e r2 e assistida). Ela foi congelada em
  dados/conferencia/primeira_leitura.csv antes da adjudicação, e a concordância é sempre
  medida contra esse retrato; apagar o arquivo refaz o retrato pelos dados vigentes, que já
  trazem as correções, e a concordância deixaria de medir a primeira leitura.
- Cada divergência tem decisão em dados/conferencia/adjudicacao.csv (final, decisão, motivo).
  O script confere se os dados vigentes trazem o valor decidido e lista o que faltar.
"""
import csv
import glob
import json
import os
import sys
from collections import Counter, defaultdict

BASE = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.dirname(__file__))
from consolida_sentencas import lei_15397  # noqa: E402
from eixos_mediacao import le_codificacao  # noqa: E402
from analise_q1_alcance import SUBSTITUIDA  # noqa: E402

CONF = os.path.join(BASE, "dados/conferencia")
PRIMEIRA = os.path.join(CONF, "primeira_leitura.csv")
ADJ = os.path.join(CONF, "adjudicacao.csv")
CAMPOS_D = ["contexto", "meio_contato", "artificio", "papel_denunciado", "whatsapp", "pix_pagamento", "boleto",
            "falso_parente", "falsa_central", "venda_falsa", "investimento", "conta_do_denunciado", "invasao"]
CAMPOS_S = ["resultado", "tipo_acolhido", "pena_meses", "regime", "substituida", "lei_15397", "rep_status",
            "rep_material", "rep_moral", "rep_fundamentos", "rep_moral_negado", "rep_individualizada", "rep_solidaria",
            "intermediario_ressarciu", "conseq_valoracao", "conseq_danos", "pedido_reparacao", "pedido_moral"]
NUMERICOS = {"pena_meses": 0.5, "rep_material": None, "rep_moral": None}
CONJUNTOS = {"rep_fundamentos", "conseq_danos"}


def sim(v):
    return "sim" if str(v).strip().lower() in ("true", "1", "sim") else "não"


def num(v):
    v = str(v or "").strip().replace("R$", "").strip()
    if not v or v.lower() in ("sem valor", "n/a"):
        return v.lower()
    try:
        return float(v)
    except ValueError:
        return v


def primeira_sentenca(caso, s, q):
    """Primeira leitura de uma sentença, no vocabulário do livro de códigos."""
    cond = s["resultado"] in ("condenação", "procedência parcial")
    lei = lei_15397(s)
    lei = {"anterior à lei": "anterior", "absolve": "menciona", "reforço": "menciona",
           "menciona, sem codificar": "menciona", "só dispositivo": ""}.get(lei, lei)
    rep = q["rep_status"] if cond else "n/a"
    conseq = {"não lida": "não examinada", "não conferida": "não examinada"}.get(q["conseq_valoracao"], q["conseq_valoracao"])
    pedido = "sim" if q["pedido_denuncia"] == "True" else "não"
    return dict(
        resultado=s["resultado"], tipo_acolhido=s["tipo_acolhido"] if cond else "",
        pena_meses=s["pena_meses"] if cond else "", regime=s["regime"] if cond else "",
        substituida=sim(SUBSTITUIDA.get(caso, s["substituida_auto"])) if cond else "", lei_15397=lei, rep_status=rep,
        rep_material=("sem valor" if rep == "fixa" and not q["rep_total"] else (q["rep_material"] or "0")) if rep == "fixa" else "0",
        rep_moral=q["rep_moral"] or "0", rep_fundamentos=q["fundamentos"],
        rep_moral_negado=sim(q["nega_moral"]), rep_individualizada=sim(q["rep_limitada_conta"]),
        rep_solidaria=sim(q["solidaria"]), intermediario_ressarciu="sim" if q["intermediario_ressarciu"] else "não",
        conseq_valoracao=conseq if cond else "n/a", conseq_danos=q["conseq_danos"], pedido_reparacao=pedido,
        pedido_moral=sim(q["pedido_moral"]))


def igual(campo, a, b):
    if campo in NUMERICOS:
        x, y = num(a), num(b)
        if isinstance(x, float) and isinstance(y, float):
            tol = NUMERICOS[campo]
            return abs(x - y) <= (tol if tol is not None else max(1.0, 0.01 * max(abs(x), abs(y))))
        return str(x) == str(y) or (x in ("", 0.0) and y in ("", 0.0))
    if campo in CONJUNTOS:
        return set(filter(None, str(a).split("|"))) == set(filter(None, str(b).split("|")))
    return str(a).strip().lower() == str(b).strip().lower()


def kappa(pares):
    n = len(pares)
    if not n:
        return None
    po = sum(a == b for a, b in pares) / n
    ca, cb = Counter(a for a, _ in pares), Counter(b for _, b in pares)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    return round((po - pe) / (1 - pe), 2) if pe < 1 else None


def carrega():
    mapa = json.load(open(os.path.join(CONF, "mapa_segundo_leitor.json"), encoding="utf-8"))
    seg = {}
    for f in sorted(glob.glob(os.path.join(CONF, "segundo_leitor_*.csv"))):
        for r in csv.DictReader(open(f, encoding="utf-8")):
            seg[r["id"].strip()] = r
    return mapa, seg


def atual(m, cod, sent, q3):
    """Leitura vigente de um caso (depois das correções gravadas), no vocabulário do livro de códigos."""
    if m["bloco"] == "codificacao":
        r1 = dict(cod[m["numero"]])
        return r1, r1["fonte_codificacao"]
    caso = m["caso"]
    return primeira_sentenca(caso, sent[caso], q3[caso]), sent[caso]["conferido"]


def vigentes():
    cod = le_codificacao()
    sent = {x["caso"]: x for x in csv.DictReader(open(os.path.join(BASE, "dados/extracao/sentencas_amostra.csv"), encoding="utf-8"))}
    q3 = {x["caso"]: x for x in csv.DictReader(open(os.path.join(BASE, "dados/analise/q3_dano.csv"), encoding="utf-8"))}
    return cod, sent, q3


def congela(mapa):
    """Grava a primeira leitura como estava ao ser comparada (primeira_leitura.csv), para que a
    concordância continue reproduzível depois que a adjudicação corrigir os dados."""
    cod, sent, q3 = vigentes()
    with open(PRIMEIRA, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id", "caso", "bloco", "fonte", "campo", "valor"])
        w.writeheader()
        for bid, m in sorted(mapa.items()):
            r1, fonte = atual(m, cod, sent, q3)
            for c in (CAMPOS_D if m["bloco"] == "codificacao" else CAMPOS_S):
                w.writerow(dict(id=bid, caso=m["caso"], bloco=m["bloco"], fonte=fonte, campo=c, valor=r1.get(c, "")))


def primeira_congelada():
    out = defaultdict(dict)
    for x in csv.DictReader(open(PRIMEIRA, encoding="utf-8")):
        out[x["id"]][x["campo"]] = x["valor"]
        out[x["id"]]["_fonte"] = x["fonte"]
    return out


def compara():
    mapa, seg = carrega()
    if not os.path.exists(PRIMEIRA):
        congela(mapa)
    p1 = primeira_congelada()
    linhas = []
    for bid, m in sorted(mapa.items()):
        r2 = seg.get(bid)
        if r2 is None:
            continue
        caso = m["caso"]
        r1, fonte = p1[bid], p1[bid]["_fonte"]
        campos = CAMPOS_D if m["bloco"] == "codificacao" else CAMPOS_S
        for c in campos:
            a, b = r1.get(c, ""), r2.get(c, "")
            if m["bloco"] == "sentenca" and c in ("rep_fundamentos",) and r1["rep_status"] != "nega" and r2.get("rep_status") != "nega":
                continue
            if m["bloco"] == "sentenca" and c == "conseq_danos" and "negativa" not in (r1["conseq_valoracao"], r2.get("conseq_valoracao")):
                continue
            if m["bloco"] == "sentenca" and c in ("tipo_acolhido", "pena_meses", "regime", "substituida") and not m.get("auto") \
                    and r1["resultado"] not in ("condenação", "procedência parcial"):
                continue
            linhas.append(dict(id=bid, caso=caso, bloco=m["bloco"], sorteado=not m.get("forcado") and caso not in FRONTEIRA,
                               conferido_primeira=fonte, auto=m.get("auto", ""), campo=c, primeira=a, segunda=b,
                               concorda=igual(c, a, b), confianca=r2.get("confianca", ""), nota_segunda=r2.get("nota", "")))
    return linhas


def confere_adjudicacao(L):
    """Toda divergência precisa de decisão em adjudicacao.csv, e os dados vigentes precisam
    trazer o valor decidido. Devolve as falhas (vazio = adjudicação aplicada)."""
    if not os.path.exists(ADJ):
        return ["adjudicacao.csv ausente"]
    adj = {(x["caso"], x["campo"]): x for x in csv.DictReader(open(ADJ, encoding="utf-8"))}
    mapa, _ = carrega()
    cod, sent, q3 = vigentes()
    por_caso = {(m["caso"], m["bloco"]): m for m in mapa.values()}
    falhas = []
    for x in L:
        if x["concorda"]:
            continue
        a = adj.get((x["caso"], x["campo"]))
        if a is None:
            falhas.append(f'{x["caso"]} {x["campo"]}: divergência sem decisão')
            continue
        r1, _ = atual(por_caso[(x["caso"], x["bloco"])], cod, sent, q3)
        if not igual(x["campo"], r1.get(x["campo"], ""), a["final"]):
            falhas.append(f'{x["caso"]} {x["campo"]}: decidido {a["final"]!r}, vigente {r1.get(x["campo"], "")!r}')
    return falhas


FRONTEIRA = {"INV 6", "INV 27", "INV 41", "INV 32", "INV 36", "CL 25", "FE 23", "FE 31", "FE 67", "FE 97"}


def resumo(L):
    out = {}
    for bloco, campos in (("codificacao", CAMPOS_D), ("sentenca", CAMPOS_S)):
        o = out[bloco] = {}
        for c in campos:
            X = [x for x in L if x["bloco"] == bloco and x["campo"] == c]
            if not X:
                continue
            S = [x for x in X if x["sorteado"]]
            d = dict(n=len(X), concordancia=round(sum(x["concorda"] for x in X) / len(X), 2),
                     n_sorteados=len(S), concordancia_sorteados=round(sum(x["concorda"] for x in S) / len(S), 2) if S else None)
            if c not in NUMERICOS and c not in CONJUNTOS:
                d["kappa"] = kappa([(str(x["primeira"]).lower(), str(x["segunda"]).lower()) for x in X])
            if bloco == "sentenca" and c in ("resultado", "tipo_acolhido", "pena_meses", "regime", "substituida", "lei_15397"):
                A = [x for x in X if x["auto"] is True]
                d["n_auto"] = len(A)
                d["concordancia_auto"] = round(sum(x["concorda"] for x in A) / len(A), 2) if A else None
            d["divergencias"] = [x["caso"] for x in X if not x["concorda"]]
            o[c] = d
    return out


def main():
    L = compara()
    os.makedirs(CONF, exist_ok=True)
    with open(os.path.join(CONF, "concordancia.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(L[0].keys()))
        w.writeheader()
        w.writerows(L)
    out = resumo(L)
    json.dump(out, open(os.path.join(CONF, "concordancia_resumo.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    falhas = confere_adjudicacao(L)
    print("adjudicação aplicada em todas as divergências" if not falhas else "adjudicação pendente:\n  " + "\n  ".join(falhas))
    if "-q" in sys.argv:
        return
    for bloco, o in out.items():
        print(f"\n===== {bloco}")
        for c, d in o.items():
            extra = f" kappa {d['kappa']}" if d.get("kappa") is not None else ""
            auto = f" | auto {d['concordancia_auto']} (n={d['n_auto']})" if d.get("n_auto") else ""
            print(f"{c:24} {d['concordancia']:.2f} (n={d['n']}){extra} | sorteados {d['concordancia_sorteados']} (n={d['n_sorteados']}){auto}"
                  f" | divergem: {', '.join(d['divergencias'])}")


if __name__ == "__main__":
    main()
