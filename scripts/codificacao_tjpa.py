"""Confere e tabula a codificação assistida das denúncias do TJPA (fase 2).

Uso (da raiz do repo):
    python3 scripts/codificacao_tjpa.py            confere e imprime as tabelas
    python3 scripts/codificacao_tjpa.py tabelas    só as tabelas, em markdown

Lê dados/extracao/codificacao_assistida_tjpa.csv (contexto, meio, papel e nove
indicadores, gravados por TRIB=tjpa scripts/grava_codificacao.py), a extração
(denuncias_tjpa.csv) e o artifício já codificado (codificacao_artificio_tjpa.csv).

A conferência não lê as denúncias: verifica que a codificação cobre as denúncias
sem duplicata e só elas, que o artifício é o da codificação conferida por segundo
leitor, que os valores estão no vocabulário do livro de códigos e que os campos
são coerentes entre si. As incoerências aparentes que a leitura justificou estão
em EXCECOES, com o motivo; qualquer outra aborta.
"""
import csv
import sys
from collections import Counter

ARQ = "dados/extracao/codificacao_assistida_tjpa.csv"
ARQ_DEN = "dados/extracao/denuncias_tjpa.csv"
ARQ_ART = "dados/extracao/codificacao_artificio_tjpa.csv"
BIN = ["whatsapp", "pix_pagamento", "boleto", "falso_parente", "falsa_central", "venda_falsa",
       "investimento", "conta_do_denunciado", "invasao"]
VOC = {
    "contexto": {"patrimonial", "violencia_domestica", "relacional", "institucional", "outro"},
    "meio_contato": {"whatsapp", "rede_social", "site", "email", "telefone", "boleto", "presencial",
                     "sistema", "outro"},
    "papel_denunciado": {"titular_conta", "executor", "misto", "invasor"},
}
ART_INVASAO = {"invasao_sistema_bancario", "invasao_sistema_venda_dados", "roubo_celular_invasao",
               "sequestro_conta", "controle_parceira", "devassa_privacidade"}

# (caso, regra): motivo. Incoerências aparentes que a leitura da denúncia sustenta.
EXCECOES = {
    ("PA-FE 1", "artifício de invasão sem invasão"):
        "conta aberta em nome da vítima com documento falso e portabilidade do salário; não há acesso à conta dela",
    ("PA-FE 3", "invasão fora dos artifícios de invasão"):
        "falso conhecido pelo WhatsApp clonado de uma amiga da vítima",
    ("PA-FE 17", "invasão fora dos artifícios de invasão"):
        "falsa central que manda instalar falso antivírus; as transferências saem em minutos, sem ato da vítima",
    ("PA-FE 99", "invasão fora dos artifícios de invasão"):
        "acesso interno com alteração direta dos boletos no sistema e apagamento dos títulos",
    ("PA-FE 208", "invasão fora dos artifícios de invasão"):
        "falso investimento anunciado em perfil de Instagram invadido de terceira",
    ("PA-FE 218", "invasão fora dos artifícios de invasão"):
        "cartão corporativo movimentado por terceiros sem acesso autorizado",
    ("PA-FE 58", "boleto fora do boleto falso"): "venda falsa em site paga por boleto",
    ("PA-FE 99", "boleto fora do boleto falso"): "a empresa vítima pagou os boletos alterados",
    ("PA-FE 179", "misto sem conta"): "tentativa: a conta de um denunciado foi indicada e nada entrou",
}


def le(arq):
    with open(arq, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def caso(r):
    return f"PA-{r['estrato']} {r['ordem']}"


def confere(cod):
    den = [r for r in le(ARQ_DEN) if not r["duplicata_de"]]
    art = {r["numero"]: r["artificio"] for r in le(ARQ_ART)}
    erros = []
    if {r["numero"] for r in cod} != {r["numero"] for r in den}:
        erros.append("a codificação não cobre exatamente as denúncias sem duplicata")
    chaves = {r["numero"]: (r["estrato"], r["ordem"]) for r in den}
    achadas = set()
    for r in cod:
        c = caso(r)
        if chaves.get(r["numero"]) != (r["estrato"], r["ordem"]):
            erros.append(f"{c}: estrato ou ordem diferem da extração")
        if art.get(r["numero"]) != r["artificio"]:
            erros.append(f"{c}: artifício difere do codificado")
        for k, voc in VOC.items():
            if r[k] not in voc:
                erros.append(f"{c}: {k}={r[k]} fora do vocabulário")
        b = {k: r[k] == "1" for k in BIN}
        if any(r[k] not in ("0", "1") for k in BIN):
            erros.append(f"{c}: indicador fora de 0 e 1")
        a, p = r["artificio"], r["papel_denunciado"]
        regras = [
            ((a == "falso_parente") != b["falso_parente"], "falso parente difere do artifício"),
            ((a == "venda_falsa") != b["venda_falsa"], "venda falsa difere do artifício"),
            ((a == "investimento_falso") != b["investimento"], "investimento difere do artifício"),
            (a == "falsa_central" and not b["falsa_central"], "falsa central sem o indicador"),
            (p == "titular_conta" and not b["conta_do_denunciado"], "titular sem conta"),
            (p in ("executor", "invasor") and b["conta_do_denunciado"], "executor ou invasor com conta"),
            (p == "misto" and not b["conta_do_denunciado"], "misto sem conta"),
            (r["meio_contato"] == "whatsapp" and not b["whatsapp"], "meio WhatsApp sem o indicador"),
            (a in ART_INVASAO and not b["invasao"], "artifício de invasão sem invasão"),
            (a not in ART_INVASAO and b["invasao"], "invasão fora dos artifícios de invasão"),
            (b["boleto"] and a != "boleto_falso", "boleto fora do boleto falso"),
        ]
        for falha, regra in regras:
            if falha:
                if (c, regra) in EXCECOES:
                    achadas.add((c, regra))
                else:
                    erros.append(f"{c}: {regra}")
    for chave in set(EXCECOES) - achadas:
        erros.append(f"exceção sem uso: {chave}")
    return erros


def linha(rotulo, cod, campo, ordem):
    cels = []
    for e in ("INV", "CL", "FE"):
        sub = [r for r in cod if r["estrato"] == e]
        n = Counter(r[campo] for r in sub)
        cels.append("; ".join(f"{v.replace('_', ' ')} {n[v]} ({100 * n[v] / len(sub):.1f}%)".replace(".", ",")
                              for v in ordem if n[v]))
    return f"| {rotulo} | " + " | ".join(cels) + " |"


def tabelas(cod):
    n = Counter(r["estrato"] for r in cod)
    print(f"| Campo | INV ({n['INV']}) | CL ({n['CL']}) | FE ({n['FE']}) |")
    print("| --- | --- | --- | --- |")
    print(linha("Contexto", cod, "contexto",
                ["patrimonial", "violencia_domestica", "relacional", "institucional", "outro"]))
    print(linha("Meio de contato", cod, "meio_contato",
                ["whatsapp", "telefone", "sistema", "presencial", "site", "rede_social", "email", "boleto", "outro"]))
    print(linha("Papel do denunciado", cod, "papel_denunciado", ["titular_conta", "misto", "executor", "invasor"]))
    print()
    print(f"| Indicador | INV ({n['INV']}) | CL ({n['CL']}) | FE ({n['FE']}) |")
    print("| --- | --- | --- | --- |")
    for k in BIN:
        cels = []
        for e in ("INV", "CL", "FE"):
            sub = [r for r in cod if r["estrato"] == e]
            s = sum(r[k] == "1" for r in sub)
            cels.append(f"{s} ({100 * s / len(sub):.1f}%)".replace(".", ","))
        print(f"| {k} | " + " | ".join(cels) + " |")
    print()
    print("| Artifício (FE) | n | titular | misto | executor |")
    print("| --- | --- | --- | --- | --- |")
    fe = [r for r in cod if r["estrato"] == "FE"]
    for a, q in Counter(r["artificio"] for r in fe).most_common():
        p = Counter(r["papel_denunciado"] for r in fe if r["artificio"] == a)
        print(f"| {a.replace('_', ' ')} | {q} | {p['titular_conta']} | {p['misto']} | {p['executor']} |")


def main():
    cod = le(ARQ)
    if sys.argv[1:] != ["tabelas"]:
        erros = confere(cod)
        if erros:
            sys.exit("\n".join(erros))
        print(f"{len(cod)} denúncias codificadas; conferência sem divergência "
              f"({len(EXCECOES)} exceções justificadas)\n")
    tabelas(cod)


if __name__ == "__main__":
    main()
