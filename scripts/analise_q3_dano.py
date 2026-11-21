"""Questão 3 da análise criminológica (linha 3.3): que dano a sentença reconhece além do
financeiro, e como a reparação mínima do art. 387, IV, do CPP se distribui pelos eixos
(sistema e canal), pelo nível alcançado da questão 1 e pela vulnerabilidade da vítima.

Lê as sentenças com scripts/reparacao_387.py (validado contra a leitura à mão da matriz:
`python3 scripts/reparacao_387.py valida`), cruza com a denúncia (pedido de reparação,
valor do fato, vítima idosa, contexto de VD) e com os eixos e o nível das questões 1 e 2.
Grava dados/analise/q3_dano.csv (uma linha por denúncia) e dados/analise/q3_resumo.json,
e imprime as tabelas. `-q` grava sem imprimir.

Decisões que não saltam aos olhos:
- A unidade é a denúncia sem duplicatas, com o peso do processo, e os percentuais são
  ponderados dentro do estrato. As quatro denúncias fora da tipologia (classe "fora" dos
  eixos: INV 40, CL 12, CL 25, FE 123) ficam no CSV e fora do resumo, como na questão 1. O denominador da reparação é a sentença condenatória com
  texto lido; as seis lidas só pelo DJEN entram pela nota da coleta (CORRECAO), e as duas
  cujo dispositivo publicado não fala de reparação ficam como indeterminadas.
- "Silente" é a condenação sem palavra sobre a reparação. Não se confunde com a negativa
  fundamentada, porque o art. 387, IV, diz que o juiz "fixará" o valor mínimo.
- O valor do fato é o maior valor em reais da narrativa da denúncia (valor_max), que é o
  prejuízo na maioria dos casos, mas pode ser um item; a razão entre reparação e valor do
  fato é lida por faixas, não como medida exata.
- O nível alcançado vem da questão 1 (titular de conta = "só conta"; executores e mistos
  pelo dicionário NIVEL de analise_q1_alcance.py). No INV, o papel da codificação de base.
- As consequências do crime (art. 59 do CP) saem do leitor por termos e, nas que ele
  marca como valoradas ou em dúvida, da leitura à mão (CONSEQ_MANUAL), que prevalece.
- A tipologia do dano segue os cinco temas de Agrafiotis et al. (2018): físico ou digital,
  econômico, psicológico, reputacional, social e societal. "Digital" é o dano ao dado, à
  conta ou ao sistema da vítima (exposição, perda, uso indevido dos dados pessoais).
"""
import csv
import json
import os
import re
import sys
from collections import Counter, defaultdict
from statistics import median

BASE = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.dirname(__file__))
from analise_q1_alcance import NIVEL  # recodificação de nível dos executores e mistos
from eixos_mediacao import eixos, le_codificacao, ponderada
from reparacao_387 import (le_consequencias, le_reparacao, pedido_alegacoes, pedido_denuncia,
                           texto_denuncia, texto_sentenca)

EXT = os.path.join(BASE, "dados/extracao")
SAIDA = os.path.join(BASE, "dados/analise")
ESTRATOS = ["INV", "CL", "FE"]
CONDENA = ("condenação", "procedência parcial")

# Correções à mão da reparação: (status, valor material, valor moral, nota). None no valor
# quando a sentença fixa sem dizer quanto.
CORRECAO = {
    "FE 103": ("fixa", None, 0, "fixa como indenização mínima o valor recolhido como fiança, revertido à vítima; a sentença não diz o valor"),
    "FE 125": ("fixa", 92418.32, 0, "valor escrito sem R$ ('92.418,32'), prejuízo econômico comprovado"),
    # lidas só pelo dispositivo publicado no DJEN (sentencas_amostra.csv, coluna nota)
    "FE 8": ("fixa", None, 0, "DJEN: dois réus no 171 §2º-A 'com reparação'; o valor não foi anotado"),
    "FE 118": ("fixa", 558.90, 0, "DJEN: reparação de R$ 558,90"),
    "CL 20": ("fixa", 5343.76, 0, "DJEN: reparação de R$ 5.343,76"),
    "CL 32": ("fixa", 86000.0, 0, "DJEN: 'reparação de R$ 86 mil', valor arredondado na nota da coleta"),
    "INV 6": ("indeterminado", 0, 0, "DJEN: o dispositivo anotado não fala de reparação e a fundamentação não foi lida"),
    "CL 30": ("indeterminado", 0, 0, "DJEN: o dispositivo anotado não fala de reparação e a fundamentação não foi lida"),
}

# Leitura à mão das consequências do crime nas sentenças condenatórias em que o leitor por
# termos as marcou como valoradas, ou em dúvida: (valoração, danos, nota).
# valoração: negativa (pesou na pena-base), neutra, não examinada (a menção está fora da
# dosimetria, em ementa citada ou no pedido do MP). Entradas marcadas "(segundo leitor)" vêm
# da adjudicação de dados/conferencia/adjudicacao.csv.
CONSEQ_MANUAL = {
    "INV 39": ("negativa", ["psicológico", "social"], "relatório psicológico; hostilidade e falta de acolhimento no trabalho depois da divulgação"),
    "INV 20": ("não examinada", [], "a menção a consequências patrimoniais e morais está na recusa da insignificância"),
    "INV 30": ("negativa", ["econômico", "digital", "reputacional"], "perdeu projetos e clientes e contratou 15 pessoas para refazer o trabalho perdido; a perda de clientes é dano à reputação da empresa (segundo leitor)"),
    "INV 4": ("negativa", ["digital", "psicológico"], "uso ilícito de dados e documentos pessoais, abalo psíquico e receio de prejuízo; a reparação é negada porque 'não houve prejuízo financeiro' (segundo leitor)"),
    "INV 5": ("negativa", ["econômico"], "prejuízo significativo"),
    "INV 8": ("não examinada", [], "prejuízo financeiro e de imagem só no pedido do MP, no relatório"),
    "INV 22": ("negativa", ["digital", "social"], "invasão de computadores da Polícia Civil com informações sigilosas usadas no combate ao crime"),
    "INV 44": ("não examinada", [], "consequências da violência de gênero em tese, fora da dosimetria"),
    "CL 10": ("negativa", ["econômico"], "elevado prejuízo"),
    "CL 13": ("negativa", ["econômico", "social"], "prejuízo, encargos, empréstimos e reflexos pessoais e matrimoniais"),
    "CL 14": ("neutra", [], "não justificam a majoração"),
    "CL 25": ("negativa", ["social"], "anabolizantes: consequências à saúde pública na base dos demais réus; fato fora da tipologia (segundo leitor)"),
    "CL 37": ("negativa", ["econômico"], "R$ 27.185,00, acima do ordinário"),
    "CL 48": ("negativa", ["econômico"], "prejuízo experimentado pela vítima; a mesma sentença nega a reparação porque o banco ressarciu"),
    "CL 53": ("negativa", ["econômico"], "R$ 79.381,29 não recuperados"),
    "FE 10": ("não examinada", [], "só em ementas citadas"),
    "FE 15": ("negativa", ["econômico", "psicológico"], "R$ 24 mil e sentimento de insegurança"),
    "FE 27": ("negativa", ["econômico"], "R$ 21.725,00 não recuperados"),
    "FE 44": ("negativa", ["econômico"], "R$ 19.980,00 na parcela creditada na conta do réu"),
    "FE 53": ("negativa", ["econômico", "psicológico"], "R$ 25 mil e impacto emocional agravado pela condição de saúde, sem dano físico nomeado (segundo leitor)"),
    "FE 56": ("negativa", ["econômico"], "elevado prejuízo"),
    "FE 58": ("negativa", ["econômico"], "prejuízo da vítima"),
    "FE 59": ("neutra", [], "'aquelas ocorridas usualmente', na dosimetria (segundo leitor)"),
    "FE 67": ("negativa", ["econômico"], "grande prejuízo, veículo não restituído"),
    "FE 70": ("negativa", ["econômico"], "empréstimo de R$ 19,6 mil contraído em nome da vítima de 57 anos, aposentada"),
    "FE 71": ("negativa", ["econômico"], "prejuízo acima do esperado"),
    "FE 75": ("negativa", ["econômico"], "R$ 2.892,00 não ressarcidos"),
    "FE 91": ("neutra", [], "linha ordinária do delito patrimonial"),
    "FE 100": ("negativa", ["econômico"], "prejuízo experimentado pela vítima"),
    "FE 117": ("negativa", ["econômico", "psicológico"], "vítima com deficiência; livro e projeto de vida transformados em dívidas; desgaste emocional, frustração e desilusão"),
    "FE 121": ("negativa", ["econômico"], "prejuízo financeiro significativo"),
    "FE 125": ("negativa", ["econômico"], "prejuízo acima de R$ 92 mil e veículo em nome da vítima, com multas, pontos na habilitação e ação judicial para desfazer (segundo leitor: econômico, não social)"),
    "FE 128": ("não examinada", [], "transcrição genérica do art. 59"),
    "INV 26": ("neutra", [], "todas previstas no tipo"),
    "INV 34": ("não examinada", [], "a palavra está no relato da ameaça"),
    "INV 45": ("negativa", ["econômico"], "montante do prejuízo; a procura do medicamento na pandemia é circunstância (segundo leitor)"),
    "CL 1": ("não examinada", [], "citação doutrinária"),
    "CL 12": ("neutra", [], "'motivos e consequências do crime são neutros'; tráfico, fora da tipologia (segundo leitor)"),
    "CL 41": ("não examinada", [], "consequências do falso testemunho"),
    "FE 3": ("não examinada", [], "rótulo da lista do art. 59, sem valoração"),
    "FE 42": ("neutra", [], "neutras"),
    "FE 68": ("neutra", [], "não escapam à previsão típica"),
    "FE 98": ("neutra", [], "não destoam do previsto pelo legislador"),
    "FE 101": ("neutra", [], "pena-base no mínimo; lista do art. 59 sem valoração"),
    "FE 111": ("não examinada", [], "transcrição genérica do art. 59"),
    "FE 124": ("neutra", [], "nada a considerar"),
    # achadas pelo segundo leitor, fora do que o leitor por termos marcou
    "FE 21": ("negativa", ["econômico", "psicológico", "reputacional"], "pena-base +1/4: 'a vítima ficou muitíssimo abalada e temerosa' e dívidas 'que sujaram seu nome na praça'"),
    "INV 43": ("neutra", [], "as circunstâncias apontadas pelo MP 'não excedem a gravidade ordinária do crime'"),
}

# A sentença limita a reparação ao que entrou na conta do réu (lida no trecho da fixação).
LIMITADA_CONTA = {
    "CL 16": "soma das quantias nas contas cuja utilização o réu admitiu",
    "CL 19": "valor efetivamente recebido pela acusada em sua conta",
    "CL 43": "R$ 7.700,00 pela ré e R$ 200,00 pelo corréu, conforme o que entrou em cada conta",
    "CL 45": "o que ingressou na conta de cada uma das duas rés",
    "CL 47": "valores a serem quitados, respectivamente, por cada réu, desde as datas das transferências",
    "CL 57": "valor com que o réu foi favorecido",
    "FE 44": "montante carreado para a conta do réu e sob sua disponibilidade",
    "FE 100": "valor da transferência efetuada para a conta da acusada",
}
SOLIDARIA = {"CL 10", "CL 13", "CL 52", "FE 55"}  # CL 13: "reconhecida a responsabilidade solidária"

# O prejuízo foi coberto por intermediário (banco, instituição de pagamento, empresa) com recursos
# próprios, lido no texto da sentença: o dano mudou de titular antes dela. A varredura foi das
# condenatórias (CL 24, absolutória, veio do segundo leitor); a devolução do valor bloqueado na
# conta recebedora não conta (CL 13, CL 58).
INTERMEDIARIO_RESSARCIU = {
    "CL 15": "ressarcido pelo banco; reparação negada",
    "CL 18": "as instituições bancárias repararam os prejuízos; reparação negada",
    "CL 28": "ressarcida por empresa de informática; regresso da instituição na via própria",
    "CL 29": "ressarcida pelo banco, que não é parte; reparação negada",
    "CL 34": "reparada pelo Itaú; a instituição é estranha à relação processual",
    "CL 41": "o titular ressarcido pelo Santander; a reparação foi fixada a favor do PagSeguro",
    "CL 48": "ressarcida pelo banco; reparação negada e consequências valoradas pelo prejuízo",
    "FE 54": "ressarcimento parcial pelo Itaú; reparação fixada pelo restante",
    "FE 65": "ressarcido pelo banco; consequências normais por isso; sentença silente",
    "FE 122": "ressarcida em ação contra o banco; reparação negada",
    # segundo leitor
    "FE 70": "a vítima 'propôs ação cível contra o Banco e foram restituidas as parcelas'; sentença silente",
    "CL 24": "absolvição; os valores foram restituídos à vítima pela Caixa e pela Mastercard",
}

# Fundamentos da negativa corrigidos pela adjudicação do segundo leitor (adjudicacao.csv).
FUNDAMENTOS_ADJUDICADOS = {
    "CL 48": "vítima ressarcida|remete à via cível",   # "eventual dano moral deve ser buscado ... nas vias cíveis"
    "CL 58": "reparação por outro instrumento",        # valor bloqueado devolvido pelo PagSeguro ao juízo
}
DANOS = ["econômico", "psicológico", "digital", "reputacional", "social", "físico"]


def faixa_razao(rep, fato):
    if not rep or not fato:
        return ""
    r = rep / fato
    if abs(r - 1) <= 0.01:
        return "igual ao valor do fato"
    if r < 1:
        return "abaixo" if r >= 0.5 else "menos da metade"
    return "acima"


def base():
    den = {x["numero"]: x for x in csv.DictReader(open(os.path.join(EXT, "denuncias_tjsp.csv"), encoding="utf-8"))}
    sent = {x["numero"]: x for x in csv.DictReader(open(os.path.join(EXT, "sentencas_amostra.csv"), encoding="utf-8"))}
    cod = le_codificacao()
    linhas = []
    for n, d in den.items():
        if d["duplicata_de"]:
            continue
        caso = f'{d["estrato"]} {d["ordem"]}'
        c, s = cod[n], sent.get(n)
        ex = eixos(caso, c)
        if d["estrato"] == "INV":
            nivel = c["papel_denunciado"]
        elif c["papel_denunciado"] == "titular_conta":
            nivel = "só conta"
        else:
            nivel = NIVEL[caso][0]
        x = dict(caso=caso, numero=n, estrato=d["estrato"], peso=float(d["peso"]),
                 resultado=s["resultado"] if s else "sem sentença", data_sentenca=s["data_mov"] if s else "",
                 conferido_sentenca=s["conferido"] if s else "", tipo_acolhido=s["tipo_acolhido"] if s else "",
                 sistema=ex["sistema"], canal=ex["canal_eixo"], distancia=ex["distancia"], classe=ex["classe"],
                 fora=ex["classe"] == "fora",
                 nivel=nivel, artificio=c["artificio"], contexto=c.get("contexto", ""),
                 idosa=d["vitima_idosa"] == "True" or d["a_171_4"] == "True", vitima_pj=d["vitima_pj"] == "True",
                 vd=d["contexto_vd"] == "True", valor_fato=float(d["valor_max"]) if d["valor_max"] else None)
        x["condena"] = x["resultado"] in CONDENA
        td = texto_denuncia(n)
        x["pedido_denuncia"], x["valor_pedido"], x["pedido_moral"], _ = pedido_denuncia(td)
        ts = texto_sentenca(n, caso) if s else ""
        if ts:
            r = le_reparacao(ts)
            x["pedido_relatorio"] = pedido_alegacoes(ts)[0]
            val, danos, tr = le_consequencias(ts)
        else:
            r = dict(status="sem texto", valor_material=0, valor_moral=0, n_valores=0, valores="", nega_moral=False,
                     fundamentos="", solidaria=False, trechos=[])
            x["pedido_relatorio"] = False
            val, danos, tr = "sem texto", [], ""
        st = "fixa" if r["status"].startswith("fixa") else r["status"]
        x.update(rep_status=st, rep_material=r["valor_material"] or None, rep_moral=r["valor_moral"] or None,
                 rep_valores=r["valores"], nega_moral=r["nega_moral"], fundamentos=r["fundamentos"] if st == "nega" else "",
                 solidaria=caso in SOLIDARIA, fonte_reparacao="regras", nota_reparacao="")
        # a sentença limita a reparação ao que entrou na conta do réu ("valor efetivamente
        # recebido pela acusada em sua conta", CL 19; "valor da transferência efetuada para a
        # conta da acusada", FE 100)
        txt_fix = " ".join(r["trechos"])
        # a própria sentença diz que houve pedido ("Conforme pediu o Ministério Público em
        # alegações finais", FE 21; "acolho o pleito ministerial formulado na denúncia", FE 80)
        x["pedido_dito_na_sentenca"] = bool(st == "fixa" and re.search(r"\bpedi(u|do)\b|pleit|requer|requisi", txt_fix, re.I)) or \
            bool(st == "fixa" and re.search(r"conforme (pediu|requereu)|acolho o (pleito|pedido)", ts, re.I))
        if caso in FUNDAMENTOS_ADJUDICADOS and st == "nega":
            x["fundamentos"] = FUNDAMENTOS_ADJUDICADOS[caso]
        x["rep_limitada_conta"] = caso in LIMITADA_CONTA
        x["intermediario_ressarciu"] = INTERMEDIARIO_RESSARCIU.get(caso, "")
        if caso in CORRECAO:
            stc, vm, vmo, nota = CORRECAO[caso]
            x.update(rep_status=stc, rep_material=vm, rep_moral=vmo or None, fonte_reparacao="correção manual", nota_reparacao=nota)
        if not x["condena"]:
            x["rep_status"] = "sem condenação" if s else "sem sentença"
        x["rep_total"] = (x["rep_material"] or 0) + (x["rep_moral"] or 0) or None
        x["razao_fato"] = round(x["rep_total"] / x["valor_fato"], 3) if x["rep_total"] and x["valor_fato"] else None
        x["faixa_razao"] = faixa_razao(x["rep_total"], x["valor_fato"])
        if caso in CONSEQ_MANUAL:
            val, danos, nota = CONSEQ_MANUAL[caso]
            x["conseq_fonte"], x["conseq_nota"] = "leitura à mão", nota
        else:
            if val in ("negativa", "indefinida"):
                val = "não conferida"  # aparece se o leitor marcar caso novo sem leitura à mão
            x["conseq_fonte"], x["conseq_nota"] = "regras", ""
            danos = []
        x["conseq_valoracao"], x["conseq_danos"] = val, "|".join(danos)
        x["dano_extra"] = bool(x["rep_moral"]) or any(d_ != "econômico" for d_ in danos)
        linhas.append(x)
    return linhas


def pond_media(L, f):
    num = sum(x["peso"] * f(x) for x in L)
    den = sum(x["peso"] for x in L)
    return round(num / den, 1) if den else None


def resumo(L):
    out = {}
    for e in ESTRATOS:
        E = [x for x in L if x["estrato"] == e and not x["fora"]]
        cond = [x for x in E if x["condena"] and x["rep_status"] != "indeterminado"]
        fixa = [x for x in cond if x["rep_status"] == "fixa"]
        o = out[e] = {"denuncias": len(E), "condenacoes_lidas": len(cond)}
        o["status"] = ponderada(cond, lambda x: x["rep_status"], ["fixa", "nega", "silente"])
        nega = [x for x in cond if x["rep_status"] == "nega"]
        o["fundamentos_negativa"] = {k: sum(k in x["fundamentos"].split("|") for x in nega)
                                     for k in sorted({f for x in nega for f in x["fundamentos"].split("|") if f})}
        o["fundamentos_negativa"]["n"] = len(nega)
        # pedido na denúncia e fixação
        o["pedido_denuncia"] = ponderada(cond, lambda x: x["pedido_denuncia"])
        o["status_por_pedido"] = {str(p): ponderada([x for x in cond if x["pedido_denuncia"] == p], lambda x: x["rep_status"],
                                                    ["fixa", "nega", "silente"]) for p in (True, False)}
        o["nega_sem_pedido_com_pedido_na_denuncia"] = [x["caso"] for x in nega if "sem pedido" in x["fundamentos"] and x["pedido_denuncia"]]
        o["fixa_sem_pedido_na_denuncia"] = [x["caso"] for x in fixa if not x["pedido_denuncia"]]
        o["fixa_sem_pedido_algum"] = [x["caso"] for x in fixa if not x["pedido_denuncia"] and not x["pedido_relatorio"] and not x["pedido_dito_na_sentenca"]]
        o["pedido_denuncia_ou_alegacoes"] = ponderada(cond, lambda x: x["pedido_denuncia"] or x["pedido_relatorio"])
        o["status_por_pedido_qualquer"] = {str(p): ponderada([x for x in cond if (x["pedido_denuncia"] or x["pedido_relatorio"]) == p],
                                                             lambda x: x["rep_status"], ["fixa", "nega", "silente"]) for p in (True, False)}
        o["silente_com_pedido"] = [x["caso"] for x in cond if x["rep_status"] == "silente" and x["pedido_denuncia"]]
        # valores
        vals = [x["rep_total"] for x in fixa if x["rep_total"]]
        o["reparacao_mediana"] = median(vals) if vals else None
        o["reparacao_n_com_valor"] = len(vals)
        o["faixa_razao"] = ponderada([x for x in fixa if x["faixa_razao"]], lambda x: x["faixa_razao"])
        o["limitada_conta"] = [x["caso"] for x in fixa if x["rep_limitada_conta"]]
        o["solidaria"] = [x["caso"] for x in fixa if x["solidaria"]]
        o["moral_fixado"] = [f'{x["caso"]} ({x["rep_moral"]:.0f})' for x in fixa if x["rep_moral"]]
        o["moral_pedido_denuncia"] = [x["caso"] for x in E if x["pedido_moral"]]
        o["moral_pedido_e_desfecho"] = {x["caso"]: (x["rep_status"], x["rep_valores"] or "", x["nega_moral"]) for x in E if x["pedido_moral"]}
        o["moral_negado"] = [x["caso"] for x in cond if x["nega_moral"]]
        # por eixos
        for k in ("canal", "distancia", "sistema"):
            o["fixa_por_" + k] = {v: ponderada([x for x in cond if x[k] == v], lambda x: x["rep_status"] == "fixa")
                                  for v in sorted({x[k] for x in cond})}
        o["fixa_por_nivel"] = {v: ponderada([x for x in cond if x["nivel"] == v], lambda x: x["rep_status"], ["fixa", "nega", "silente"])
                               for v in sorted({x["nivel"] for x in cond})}
        o["valor_por_nivel"] = {v: f"n={len(w)}, mediana {median(w):.2f}" for v in sorted({x["nivel"] for x in fixa})
                                if (w := [x["rep_total"] for x in fixa if x["nivel"] == v and x["rep_total"]])}
        o["faixa_por_nivel"] = {v: ponderada([x for x in fixa if x["nivel"] == v and x["faixa_razao"]], lambda x: x["faixa_razao"])
                                for v in sorted({x["nivel"] for x in fixa})}
        o["fixa_por_idosa"] = {str(v): ponderada([x for x in cond if x["idosa"] == v], lambda x: x["rep_status"], ["fixa", "nega", "silente"])
                               for v in (True, False)}
        o["valor_por_idosa"] = {str(v): f"n={len(w)}, mediana {median(w):.2f}" for v in (True, False)
                                if (w := [x["rep_total"] for x in fixa if x["idosa"] == v and x["rep_total"]])}
        o["fixa_por_vitima_pj"] = {str(v): ponderada([x for x in cond if x["vitima_pj"] == v], lambda x: x["rep_status"], ["fixa", "nega", "silente"])
                                   for v in (True, False)}
        o["ressarcida_por_canal"] = Counter(x["canal"] for x in nega if "vítima ressarcida" in x["fundamentos"])
        o["intermediario_ressarciu"] = {x["caso"]: x["rep_status"] for x in cond if x["intermediario_ressarciu"]}
        o["limitada_conta_n"] = f'{sum(x["rep_limitada_conta"] for x in fixa)} de {len(fixa)}'
        so = [x for x in fixa if x["nivel"] == "só conta"]
        o["so_conta_fixa_igual_fato"] = f'{sum(x["faixa_razao"] == "igual ao valor do fato" for x in so)} de {sum(bool(x["faixa_razao"]) for x in so)}'
        o["so_conta_fixa_limitada"] = [x["caso"] for x in so if x["rep_limitada_conta"]]
        o["nega_por_nivel"] = {v: Counter(f for x in nega if x["nivel"] == v for f in x["fundamentos"].split("|") if f)
                               for v in sorted({x["nivel"] for x in nega})}
        o["status_por_canal"] = {v: ponderada([x for x in cond if x["canal"] == v], lambda x: x["rep_status"], ["fixa", "nega", "silente"])
                                 for v in sorted({x["canal"] for x in cond}) if v}
        o["pedido_por_canal"] = {v: ponderada([x for x in cond if x["canal"] == v], lambda x: x["pedido_denuncia"])
                                 for v in sorted({x["canal"] for x in cond}) if v}
        o["pedido_por_nivel"] = {v: ponderada([x for x in cond if x["nivel"] == v], lambda x: x["pedido_denuncia"])
                                 for v in sorted({x["nivel"] for x in cond})}
        o["ano_sentenca"] = {a: ponderada([x for x in cond if x["data_sentenca"][:4] == a], lambda x: x["rep_status"], ["fixa", "nega", "silente"])
                             for a in sorted({x["data_sentenca"][:4] for x in cond if x["data_sentenca"]})}
        # consequências do crime
        o["consequencias"] = ponderada(cond, lambda x: x["conseq_valoracao"])
        negs = [x for x in cond if x["conseq_valoracao"] == "negativa"]
        o["danos_consequencias"] = {d_: sum(d_ in x["conseq_danos"].split("|") for x in negs) for d_ in DANOS}
        o["danos_consequencias"]["n"] = len(negs)
        o["consequencias_alem_economico"] = [x["caso"] for x in negs if any(d_ != "econômico" for d_ in x["conseq_danos"].split("|"))]
        o["dano_extra_reconhecido"] = [x["caso"] for x in cond if x["dano_extra"]]
        o["conseq_negativa_e_reparacao"] = {x["caso"]: x["rep_status"] for x in negs}
    return out


def fmt(dist):
    return "; ".join(f"{k} {n} ({p}%)" for k, (n, p) in dist.items())


def main():
    L = base()
    os.makedirs(SAIDA, exist_ok=True)
    campos = list(L[0].keys())
    with open(os.path.join(SAIDA, "q3_dano.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        for x in sorted(L, key=lambda x: (ESTRATOS.index(x["estrato"]), int(x["caso"].split()[1]))):
            w.writerow(x)
    out = resumo(L)
    json.dump(out, open(os.path.join(SAIDA, "q3_resumo.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    if "-q" in sys.argv:
        return
    for e, o in out.items():
        print(f"\n===== {e}: {o['condenacoes_lidas']} condenações lidas de {o['denuncias']} denúncias")
        for k, v in o.items():
            if isinstance(v, dict) and v and all(isinstance(t, tuple) and len(t) == 2 and isinstance(t[1], float) for t in v.values()):
                print(f"{k}: {fmt(v)}")
            elif isinstance(v, dict):
                print(f"{k}:")
                for k2, v2 in v.items():
                    ok = isinstance(v2, dict) and v2 and all(isinstance(t, tuple) for t in v2.values())
                    print(f"   {k2}: {fmt(v2) if ok else v2}")
            else:
                print(f"{k}: {v}")


if __name__ == "__main__":
    main()
