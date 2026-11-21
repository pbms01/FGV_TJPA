"""Classificação dos acórdãos do TJSP sobre o 171 §2º, VII (Lei 15.397/2026) pela ementa.

Lê as duas buscas do cjsg gravadas em dados/tjsp2/ (cjsg_cessao_conta_laranja.json e
cjsg_15397_inciso_vii.json), junta por cdacordao, guarda só os que tratam do inciso ou da
cessão de conta e classifica a decisão e o fundamento por regras sobre a ementa. As regras
são um primeiro corte: a coluna `revisao` marca o que precisa de leitura, e o dicionário
MANUAL, preenchido pela leitura da ementa, prevalece sobre a regra.
Grava dados/tjsp2/acordaos_inciso_vii.csv.
"""
import csv
import json
import os
import re

BASE = os.path.join(os.path.dirname(__file__), "..")
D = os.path.join(BASE, "dados/tjsp2")
N = lambda s: re.sub(r"\s+", " ", s or "")
VII = r"(?:171,?\s*(?:§|par[áa]grafo)\s*2º,?\s*(?:inciso\s*)?VII|cess[ãa]o (?:onerosa )?de conta(?: banc[áa]ria| laranja| de laranja)?|conta laranja|novel figura|nov[oa] (?:tipo|figura))"
RE_TRATA = re.compile(r"(?i)" + VII + r"|15\.?397")
RE_APLICA = re.compile(r"(?i)(?:desclassific\w*|adequ\w*|readequ\w*|subsume-se|amolda-se|se amolda|se ajusta|condena\w*|enquadr\w*)[^.;]{0,120}" + VII
                       + r"|desclassifica[çc][ãa]o (?:para o delito de cess[ãa]o de conta laranja )?operada|conduta readequada")
RE_RECUSA = re.compile(r"(?i)(?:invi[áa]vel|n[ãa]o [ée] o caso de|impossibilidade de|n[ãa]o h[áa] espa[çc]o para|incab[íi]vel|n[ãa]o se sustenta\w*|"
                       r"n[ãa]o se aplica|inaplicabilidade|afasta\w*|n[ãa]o comporta|descabid\w*|rejeitad\w*|incompat[íi]ve\w*)[^.;]{0,140}"
                       r"(?:" + VII + r"|lei (?:penal )?(?:nova|mais ben[ée]fica|posterior)|novatio)")
FUND = {
    "retroatividade benigna": r"retroa|in mellius|mais ben[ée]fica|mais favor[áa]vel|lex mitior|benigna",
    "especialidade": r"especialidade|especial\b",
    "exceção pluralista": r"pluralista",
    "participação ou adesão": r"part[íi]cipe|participa[çc][ãa]o (?:ativa|criminosa|no|na|consciente|nos)|coautoria|art\.? ?29|ades[ãa]o consciente|v[íi]nculo subjetivo|iter criminis|integr\w* (?:a|de forma)[^.]{0,30}execu|dom[íi]nio funcional",
    "irretroatividade": r"irretroativ|n[ãa]o (?:pode )?retroag|incriminadora",
    "tipicidade anterior": r"j[áa] era poss[íi]vel|antes da edi[çc][ãa]o|j[áa] se subsumia",
    "via inadequada": r"preclus|ju[íi]zo das? execu|s[úu]mula 611|art(?:igo)?\.? 619|n[ãa]o (?:foi )?submetid|n[ãa]o deduzid|via estreita|n[ãa]o conhecid",
    "suspensão ou ANPP": r"suspens[ãa]o condicional|art\.? 89|s[úu]mula 337|n[ãa]o persecu|anpp",
}

# Leitura da ementa, caso a caso (21/11/2026). Chave: (número, primeira palavra da classe),
# porque o mesmo número tem apelação e embargos. Valor: (decisão, fundamento principal, nota).
# Decisões: aplica | recusa | condena no VII (apelo do MP) | mantém o VII da sentença |
# troca o VII por 171 caput | não enfrenta (via) | não decide sobre o inciso |
# ementa não trata | ementa indisponível | fora do tema (outro inciso VII ou outro crime).
A, R, V = "aplica", "recusa", "não enfrenta (via)"
RB, ESP, PLU = "retroatividade benigna", "especialidade", "exceção pluralista à teoria monista"
PART, IRR, TIP, VIOL = "participação ou adesão à fraude", "irretroatividade", "tipicidade anterior", "crime violento"
MANUAL = {
    ("1500120-91.2023.8.26.0412", "Apelação"): (R, PART, "o inciso não é nomeado; tese: conta de uso pessoal com recebimento consciente é coautoria"),
    ("1506897-81.2025.8.26.0393", "Apelação"): (A, RB, "a lei mais favorável incide sobre a contribuição já descrita na imputação"),
    ("1529998-85.2020.8.26.0050", "Apelação"): (A, ESP, "de ofício"),
    ("1502838-89.2022.8.26.0220", "Apelação"): (A, ESP, "devolve à origem para a suspensão condicional do processo (Súmula 337 STJ)"),
    ("1504642-82.2022.8.26.0482", "Apelação"): ("ementa não trata", "", ""),
    ("1500254-58.2022.8.26.0411", "Apelação"): ("ementa não trata", "", ""),
    ("1502402-29.2022.8.26.0577", "Apelação"): ("troca o VII por 171 caput", "", "a sentença condenara no VII; o acórdão readequa ao 171 caput e §4º sem dizer por quê na ementa"),
    ("1509103-91.2023.8.26.0602", "Embargos"): (R, PART, "o VII alcança quem cede ciente do uso criminoso, não quem adere à execução"),
    ("1503302-12.2022.8.26.0577", "Apelação"): ("mantém o VII da sentença", "", ""),
    ("2158580-89.2026.8.26.0000", "Revisão"): (R, VIOL, "domínio funcional no roubo majorado"),
    ("1501603-80.2023.8.26.0405", "Apelação"): (A, RB, ""),
    ("2200316-87.2026.8.26.0000", "Revisão"): (V, "", "lavagem; não reaprecia a prova"),
    ("1500922-21.2025.8.26.0606", "Apelação"): (A, RB, "para três réus que só viabilizaram a circulação, distintos dos executores"),
    ("1507761-57.2022.8.26.0577", "Apelação"): ("ementa indisponível", "", ""),
    ("0013595-08.2026.8.26.0050", "Apelação"): (R, PART, "conta usada diretamente na execução"),
    ("1500440-50.2022.8.26.0292", "Apelação"): (R, PART, "apelo do MP contra absolvição; o VII alcança o cedente alheio ao delito de origem"),
    ("1501398-89.2023.8.26.0554", "Apelação"): (A, RB, ""),
    ("1505768-32.2023.8.26.0451", "Apelação"): (A, PLU, "rés partícipes; retroatividade benigna"),
    ("1502404-69.2024.8.26.0628", "Apelação"): ("ementa indisponível", "", ""),
    ("1501016-22.2024.8.26.0438", "Apelação"): (A, ESP, "mesmo com adesão consciente demonstrada"),
    ("1503105-24.2021.8.26.0664", "Apelação"): ("condena no VII (apelo do MP)", RB, "absolvição reformada para condenar no VII"),
    ("1512749-87.2023.8.26.0577", "Apelação"): (A, ESP, "de ofício"),
    ("1508421-62.2023.8.26.0562", "Apelação"): ("condena no VII (apelo do MP)", "", "o MP recorreu da desclassificação para receptação"),
    ("1509632-27.2020.8.26.0114", "Apelação"): ("ementa indisponível", "", ""),
    ("1508354-23.2021.8.26.0577", "Embargos"): (V, "", "preclusão; a lei mais benéfica cabe ao juízo da execução"),
    ("1501176-86.2022.8.26.0577", "Embargos"): (A, RB, "em embargos, com efeitos infringentes"),
    ("1504338-55.2023.8.26.0577", "Apelação"): ("ementa indisponível", "", ""),
    ("2186647-64.2026.8.26.0000", "Agravo"): ("ementa não trata", "", ""),
    ("1511359-53.2021.8.26.0577", "Apelação"): (A, RB, ""),
    ("1503515-52.2021.8.26.0577", "Apelação"): (R, PART, "titular partícipe quando há adesão consciente e contribuição essencial"),
    ("1535151-94.2023.8.26.0050", "Apelação"): (R, PART, "conta disponibilizada como destino das transferências no curso da fraude"),
    ("1500625-30.2023.8.26.0300", "Apelação"): ("ementa não trata", "", ""),
    ("1507101-24.2024.8.26.0050", "Embargos"): (R, PART, "tese não deduzida na apelação; dolo direto incompatível com o tipo subsidiário"),
    ("1500375-84.2022.8.26.0638", "Apelação"): ("ementa indisponível", "", ""),
    ("1515957-11.2023.8.26.0050", "Embargos"): (V, "", "rediscussão"),
    ("1515957-11.2023.8.26.0050", "Apelação"): ("ementa não trata", "", ""),
    ("1501491-38.2020.8.26.0625", "Apelação"): (A, ESP, ""),
    ("2163935-80.2026.8.26.0000", "Revisão"): ("ementa não trata", "", ""),
    ("1509023-03.2024.8.26.0050", "Embargos"): (R, PART, "tese: o VII não se aplica com participação ativa"),
    ("1503076-37.2022.8.26.0664", "Apelação"): (A, RB, "o acórdão citado pelas sentenças do CL 29 e do CL 34"),
    ("1529551-58.2024.8.26.0050", "Apelação"): ("ementa indisponível", "", ""),
    ("1533261-91.2021.8.26.0050", "Apelação"): (A, RB, "do 155 §4º-B para o VII; afasta a receptação pela especialidade"),
    ("1519635-63.2025.8.26.0050", "Apelação"): (R, "", "sem fundamento na ementa"),
    ("1507168-36.2024.8.26.0196", "Apelação"): (A, RB, "sem prova de que conhecia o modus operandi"),
    ("1500057-22.2024.8.26.0480", "Apelação"): ("ementa não trata", "", ""),
    ("1537537-97.2023.8.26.0050", "Apelação"): (R, PART, "conta aberta dias antes e triangulação: coautoria"),
    ("2165890-49.2026.8.26.0000", "Habeas"): (V, "", "após o trânsito, não conhecido"),
    ("1513891-58.2023.8.26.0050", "Apelação"): (A, "", "readequa ao VII; cessão confessada sem prova de participação no golpe"),
    ("1501075-69.2021.8.26.0032", "Apelação"): ("ementa não trata", "", ""),
    ("1501082-02.2024.8.26.0050", "Apelação"): ("ementa não trata", "", ""),
    ("0004925-83.2023.8.26.0050", "Embargos"): (R, TIP, "a cessão para fraude já era participação no 171 antes da lei; o VII não torna atípicos os fatos anteriores"),
    ("1540078-74.2021.8.26.0050", "Embargos"): (V, "", "rediscussão"),
    ("2121543-28.2026.8.26.0000", "Habeas"): ("ementa não trata", "", "prisão preventiva"),
    ("0012896-44.2025.8.26.0602", "Embargos"): ("ementa indisponível", "", ""),
    ("1505778-51.2021.8.26.0482", "Apelação"): (R, PART, "vínculo subjetivo; partícipe do furto qualificado"),
    ("1508665-83.2021.8.26.0554", "Apelação"): (A, RB, "do 155 §4º-B para o VII"),
    ("1501168-06.2022.8.26.0482", "Embargos"): (V, "", "matéria nova; a execução aplica a lei mais benéfica (Súmula 611 STF)"),
    ("1522945-14.2024.8.26.0050", "Embargos"): (V, "", "não conhecidos"),
    ("0002395-39.2025.8.26.0664", "Apelação"): ("ementa não trata", "", ""),
    ("1509801-22.2025.8.26.0378", "Apelação"): (A, RB, ""),
    ("1506886-59.2022.8.26.0554", "Embargos"): (R, PART, "coautor do §2º-A"),
    ("1545200-63.2024.8.26.0050", "Apelação"): (R, IRR, "de ofício: o VII não se aplica a fatos anteriores à vigência; readequa ao 171 caput com art. 29"),
    ("0012451-26.2026.8.26.0041", "Agravo"): (V, "", "execução: desclassificar exigiria reexame de fatos"),
    ("1500701-14.2022.8.26.0648", "Apelação"): (A, RB, ""),
    ("1503086-90.2026.8.26.0454", "Apelação"): (R, VIOL, "quem recruta, abre ou cede conta para extorsão em curso é partícipe da extorsão"),
    ("1526366-80.2022.8.26.0050", "Apelação"): (R, VIOL, "participação dolosa na extorsão"),
    ("1503721-54.2022.8.26.0408", "Apelação"): (R, "", "invocação genérica da lei nova"),
    ("1510917-19.2023.8.26.0577", "Embargos"): (R, PART, "condutas que transcendem a mera cessão"),
    ("2188126-92.2026.8.26.0000", "Revisão"): (V, "", "a retroatividade não substitui a moldura fática assentada; extorsão"),
    ("1530271-25.2024.8.26.0050", "Apelação"): (A, RB, ""),
    ("1508759-88.2023.8.26.0577", "Apelação"): (R, PART, "concurso de pessoas, não a figura autônoma e residual"),
    ("1516149-07.2024.8.26.0050", "Apelação"): (R, PART, "figura reservada ao cedente de atuação neutra"),
    ("1503645-16.2024.8.26.0196", "Apelação"): (R, PART, "coautoria funcional"),
    ("1505032-84.2025.8.26.0114", "Apelação"): (R, VIOL, "natureza violenta da extorsão incompatível com o tipo fraudulento"),
    ("1512831-44.2025.8.26.0385", "Apelação"): (A, RB, "aplicação direta antes do trânsito; afasta a Súmula 611"),
    ("1524175-96.2021.8.26.0050", "Apelação"): (R, "", "sem fundamento na ementa"),
    ("1510449-83.2023.8.26.0309", "Embargos"): (R, PART, "o VII não afasta o §2º-A quando a cessão é inerente à execução"),
    ("1500765-66.2024.8.26.0482", "Apelação"): (R, PART, "coautoria"),
    ("1503349-83.2022.8.26.0577", "Apelação"): (A, RB, ""),
    ("1501285-14.2023.8.26.0077", "Embargos"): (R, PART, "coautoria e divisão de tarefas"),
    ("1503508-55.2024.8.26.0577", "Embargos"): (R, PART, "a conduta não se limitou à da lei nova"),
    ("2135942-62.2026.8.26.0000", "Habeas"): (R, TIP, "não reconhece atipicidade do empréstimo de conta antes da lei"),
    ("1513440-33.2023.8.26.0050", "Embargos"): (R, PART, "tese: não retroage quando há participação ativa e consciente"),
    ("1507223-32.2023.8.26.0451", "Apelação"): ("não decide sobre o inciso", "", "absolve por falta de prova da adesão"),
    ("0005737-25.2017.8.26.0604", "Apelação"): ("não decide sobre o inciso", "", "absolve: ilícito civil"),
    ("1503073-55.2025.8.26.0542", "Apelação"): ("fora do tema", "", "roubo"),
    ("1517242-83.2026.8.26.0454", "Apelação"): ("fora do tema", "", "furto §4º-B: a lei nova, mais grave, não retroage"),
    ("1501034-69.2026.8.26.0536", "Apelação"): ("fora do tema", "", "roubo §2º, VII"),
    ("1522946-72.2023.8.26.0037", "Apelação"): ("fora do tema", "", "furto"),
}


def carrega():
    vistos = {}
    for nome in ("cjsg_cessao_conta_laranja.json", "cjsg_15397_inciso_vii.json"):
        for x in json.load(open(os.path.join(D, nome), encoding="utf-8")):
            y = vistos.setdefault(x["cdacordao"], dict(x, buscas=[]))
            y["buscas"].append(nome.split("_", 1)[1].rsplit(".", 1)[0])
    return list(vistos.values())


def classifica(x):
    e = N(x["ementa"])
    if not RE_TRATA.search(e):
        return "ementa não trata", [], True
    cl = x.get("Classe/Assunto", "").split(" / ")[0]
    a, r = bool(RE_APLICA.search(e)), bool(RE_RECUSA.search(e))
    fund = [k for k, p in FUND.items() if re.search(p, e, re.I)]
    if a and not r:
        dec = "aplica"
    elif r and not a:
        dec = "recusa"
    elif "via inadequada" in fund and cl != "Apelação Criminal":
        dec = "não enfrenta (via)"
    else:
        dec = "indefinido"
    return dec, fund, dec == "indefinido" or (a and r)


def main():
    linhas = []
    for x in carrega():
        dec, fund, rev = classifica(x)
        nota, principal = "", ""
        chave = (x["numero"], x.get("Classe/Assunto", "").split(" ")[0])
        if chave in MANUAL:
            dec, principal, nota = MANUAL[chave]
            rev = False
        elif dec == "ementa não trata":
            dec, rev = "fora do tema", False
        linhas.append({
            "numero": x["numero"], "cdacordao": x["cdacordao"],
            "classe": x.get("Classe/Assunto", ""), "orgao": x.get("Órgão julgador", ""),
            "relator": x.get("Relator(a)", ""), "comarca": x.get("Comarca", ""),
            "julgamento": x.get("Data do julgamento", ""), "buscas": "+".join(x["buscas"]),
            "decisao_inciso_vii": dec, "fundamento_principal": principal,
            "fundamentos_regex": "; ".join(fund), "revisao": "sim" if rev else "",
            "nota": nota})
    linhas.sort(key=lambda l: l["julgamento"][6:] + l["julgamento"][3:5] + l["julgamento"][:2])
    with open(os.path.join(D, "acordaos_inciso_vii.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0].keys()))
        w.writeheader()
        w.writerows(linhas)
    return linhas


if __name__ == "__main__":
    from collections import Counter
    L = main()
    print(len(L), Counter(l["decisao_inciso_vii"] for l in L))
    print("revisar:", sum(1 for l in L if l["revisao"]))
