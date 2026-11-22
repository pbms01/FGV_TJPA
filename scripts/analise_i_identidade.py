"""Aula de identidade digital e anonimato: quatro questões respondidas com a base da fase 1
(TJSP), sem coleta nova.

  I1  identidade usurpada narrada e capitulação: quantas denúncias narram o uso da
      identidade de outra pessoa (parente, funcionário, perfil clonado, dados ou conta de
      terceiro) e quantas imputam o art. 307 ou o 299/298 do CP.
  I2  cessão de identidade: quantas denúncias e sentenças narram a cessão de documentos,
      dados pessoais, selfie ou linha, e não só da conta; quantas imputam o art. 308.
  I3  nas 101 denúncias de só conta, o que os autos trazem sobre a abertura da conta.
  I4  o cruzamento de I3 com a versão do titular (questão 7) e o desfecho.

Uso:
  python3 -I scripts/analise_i_identidade.py          grava dados/analise/i_identidade.csv e i_resumo.json
  python3 -I scripts/analise_i_identidade.py trechos  imprime os trechos achados, para conferência

Decisões que não saltam aos olhos:
- Ementas e citações de julgados (texto entre aspas seguido de "(TJSP" ou "(STJ") saem antes
  da leitura, porque falam de outro caso: a selfie e o deepfake do FE 114 estão numa
  apelação cível citada, não nos autos.
- I3 é ordenada da evidência mais forte para a mais fraca e vence a primeira que aparece:
  resposta da instituição de que não colheu documento ou foto; selfie, biometria ou
  reconhecimento facial nos autos; documentos ou ficha de abertura; dado cadastral (nome,
  CPF, endereço) ou titularidade e extrato; nada. A leitura das 38 negativas foi conferida
  à mão (MANUAL_I3).
- A unidade é a denúncia; os números são contagens simples por estrato, como nas questões 1
  a 7, porque a pergunta é sobre o que os autos trazem, não sobre a prevalência no TJSP.
"""
import csv
import glob
import json
import os
import re
import sys
from collections import Counter, defaultdict

BASE = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.dirname(__file__))
import titular_conta as tc  # noqa: E402

EXT = os.path.join(BASE, "dados/extracao")
SAIDA = os.path.join(BASE, "dados/analise")

CITACAO = re.compile(r"[“\"][^”\"]{20,4000}[”\"]\s*\((TJ\w{2}|STJ|STF)[^)]*\)", re.S)

USURPA = {
    # identidade de pessoa usada diante da vítima (meio do engano)
    "parente": r"(se passando|passando-se|fazendo-se passar|fingindo ser|como se fosse)[^.]{0,30}\b(filh|net|sobrinh|irm|m[ãa]e\b|pai\b|parente|tia\b|tio\b|primo|prima|cunhad|genro|nora|esposa|marido|companheir)",
    "funcionario": r"(se passando|passando-se|fazendo-se passar|identificando-se|apresentando-se|fingindo ser)[^.]{0,25}\b(como |por )?(um |uma )?(funcion[áa]ri|atendente|gerente|preposto|representante|agente|empregad|colaborador|operador|t[ée]cnico|policial|delegad|advogad|servidor)",
    "perfil": r"clonad[oa]|perfil (falso|fake|fraudulento)|conta (hackeada|invadida|sequestrada|clonada)|n[úu]mero (falso|clonado)|whatsapp (falso|clonado)|foto (de perfil )?(d[oa] |de )(filh|parente|v[íi]tima|irm)",
    "generica": r"(se passando|passando-se|fazendo-se passar|fingindo ser) por|falsa identidade|identidade falsa|nome falso|nome fict[íi]cio|identidade de terceir",
    # identidade de pessoa usada como instrumento (conta, linha, cadastro)
    "terceiro": r"dados (pessoais )?(de|da|do|das|dos) (terceir|v[íi]timas)|documentos? (de|da|do) terceir|em nome de terceir|abert[ao]s? (fraudulentamente |indevidamente )?em (seu |nome d)|conta (aberta )?(fraudulenta|fantasma)|documentos? (falso|falsificad|adulterad)",
}
RX_USURPA = {k: re.compile(v, re.I) for k, v in USURPA.items()}
MEIO = ("parente", "funcionario", "perfil", "generica")

CESSAO_ID = re.compile(
    r"(emprest|ced|cedeu|vend|alug|entreg|fornec|repass|forneceu|disponibiliz)\w*[^.]{0,50}\b(seus documentos|documentos pessoais|documento de identidade|\bRG\b|\bCPF\b|dados pessoais|seus dados|selfie|foto(grafia)? (do|de seu|d[oa]) rosto|chip|linha telef)"
    r"|(documentos|dados pessoais|chip)[^.]{0,30}(emprestad|cedid|vendid|entregu|alugad)"
    r"|abri[ru][^.]{0,40}conta[^.]{0,40}(a pedido|para (um|uma|terceir|outra pessoa)|em troca|mediante (pagamento|remunera))", re.I)

ABERTURA = [
    ("instituição diz não ter colhido documento ou foto",
     r"n[ãa]o (ter |teria |havia |houve )?(solicitad|exigid|colhid|realizad|requisitad|feit)\w*[^.]{0,50}(fotografia|foto|selfie|documento|biometria|reconhecimento)"),
    ("selfie, biometria ou reconhecimento facial",
     r"selfie|biometri|reconhecimento facial|prova de vida|valida[çc][ãa]o facial|foto(grafia)? (d[oa] |de )?(rosto|face|titular)"),
    ("documentos ou ficha de abertura",
     r"(documentos?|documenta[çc][ãa]o) (pessoa(l|is) )?(apresentad|utilizad|fornecid|enviad)\w*[^.]{0,60}(abertura|institui|banco|cadastro)|ficha cadastral|proposta de abertura|documenta[çc][ãa]o (de abertura|cadastral)|documentos (da|de) abertura|(c[óo]pia|imagem) d[oa]s? documento|contrato de abertura"),
    ("dado cadastral, titularidade ou extrato",
     r"dados cadastrais|informa[çc][õo]es cadastrais|cadastro|qualifica[çc][ãa]o d[oa] titular|titular(idade)? da conta|extrato|conta (de|em nome d|pertencente)"),
]
RX_ABERTURA = [(k, re.compile(v, re.I)) for k, v in ABERTURA]

# I1: de quem é a identidade que o golpe usa diante da vítima, pela codificação validada do
# artifício (questão 1), completada pelos perfis clonados de pessoa real lidos à mão
REAL = {"falso_parente", "falso_conhecido", "falso_advogado", "sequestro_conta"}
INSTITUCIONAL = {"falsa_central", "falsa_taxa_plataforma", "boleto_falso"}
FICTICIA = {"venda_falsa", "investimento_falso", "taxa_antecipada", "falso_relacionamento"}
PERFIL_REAL = {"FE 76": "WhatsApp de conhecido clonado", "FE 98": "linha de conhecida clonada",
               "CL 14": "WhatsApp de conhecida clonado", "FE 101": "WhatsApp da filha clonado",
               "FE 114": "Instagram de amiga clonado", "FE 89": "foto do filho em perfil falso"}
# correções da amostra do segundo leitor (22 de 24 concordantes): a vendedora de uma agência
# de veículos real, com CNPJ (CL 57), e o anúncio de ingressos no próprio perfil (FE 86)
IDENT_MANUAL = {"CL 57": "instituição", "FE 86": "não usa identidade alheia"}
# identidade de terceiro usada como instrumento (linha, cartão, cadastro), lida à mão entre os
# achados da regra "terceiro"; ficaram fora a conta do próprio denunciado chamada de
# "fraudulenta" (CL 39, FE 120), a dissipação para conta de terceiro (CL 28) e a negativa de
# documento falso (FE 35)
INSTRUMENTO = {"CL 42": "linha habilitada com dados de terceiro para o perfil da falsa filha",
               "CL 22": "linha pré-paga habilitada em nome de terceiro",
               "FE 66": "dois números cadastrados em nome de terceiros",
               "FE 7": "linha habilitada com dados de terceiro",
               "CL 15": "cartões bancários em nome de terceiros apreendidos",
               "FE 29": "cartão bancário em nome de terceira pessoa apreendido",
               "FE 6": "dados de terceiros e de empresas para compras fraudulentas",
               "FE 102": "dados pessoais de terceiros obtidos na internet para compras"}
# imputação autônoma de crime de identidade ou falso ligado à identidade, e o que a sentença fez
IMPUTACAO = {"INV 4": "denúncia capitulou 304 c/c 297 a falsa identidade da locação; a sentença deu ao fato a definição do art. 307 (art. 383 do CPP) e absolveu por consunção, como etapa necessária do estelionato; condenou pelo 297, §1º, do holerite falso, como falso autônomo com potencialidade além da locação; absolveu do 299 (386, III)",
             "FE 122": "falsa central presencial: denúncia imputou também o 328, p. ú., e o 304 c/c 297; absolvição nesses dois, porque o réu só se apresentou verbalmente como funcionário; condenação no 171, §2º-A"}

# I2: cessão de identidade, lida à mão entre os achados da regra CESSAO_ID
CESSAO_MANUAL = {
    "titular cedeu documentos, dados pessoais ou selfie, ou abriu conta a pedido": {
        "CL 39": "forneceu documentos pessoais e fotografia de face para abrir conta digital no Bradesco e cedeu o acesso",
        "FE 14": "disponibilizou seus dados e documentos (sentença)",
        "CL 23": "concorreu ao fornecer os dados pessoais para o delito (denúncia)",
        "FE 41": "abriu a conta no Mercado Pago a pedido do companheiro (versão da ré; absolvida)"},
    "vítima entregou documentos, dados pessoais ou selfie ao golpista": {
        "FE 70": "cópia dos documentos pessoais e fotografia do rosto", "FE 24": "cópias de CNH e comprovante de residência",
        "CL 45": "dados pessoais, inclusive RG, para cadastro em leilão falso", "FE 90": "cadastro em site fraudulento",
        "FE 127": "dados pessoais por WhatsApp", "CL 21": "dados pessoais e do contrato", "CL 36": "dados pessoais e bancários",
        "FE 126": "dados pessoais a falso gerente", "CL 48": "dados bancários e contratação de empréstimo"},
    "mercado de dados de terceiros narrado": {
        "INV 36": "planilhas de CPF vendidas por consulta", "INV 4": "vítima acreditava que empresa vendera seus dados"},
}
# "dados bancários" emprestados é a cessão da conta descrita como dado (FE 53, FE 73, FE 99,
# CL 52, FE 21, FE 77, INV 35, INV 5): fica na questão 7

# I3: leitura à mão das 38 negativas (nega ou não reconhece a conta); (categoria, nota)
A, B, C, D, N = ("selfie ou biometria da abertura nos autos", "documentos ou ficha de abertura, sem selfie",
                 "instituição não colheu ou não achou foto ou documento", "só titularidade, extrato ou cadastro", "nada sobre a conta")
MANUAL_I3 = {
    "FE 47": (A, "selfie da abertura juntada depois; MP pediu absolvição"), "FE 98": (A, "documento e selfie segurando o documento"),
    "CL 27": (A, "Banco Inter: dados pessoais e fotografia da abertura"), "CL 58": (A, "selfie e documento de identidade da abertura"),
    "CL 22": (A, "réu admite ter aberto com documentos e selfie"), "FE 74": (A, "selfie em tempo real e geolocalização"),
    "CL 33": (A, "documentação, selfies e assinaturas"), "CL 47": (A, "biometria facial e documentos"),
    "CL 19": (A, "exame de comparação de biometria facial"), "FE 45": (A, "documentos, foto e selfie; endereço e telefone iguais aos informados à polícia"),
    "FE 119": (A, "ficha cadastral, selfie e documento"),
    "CL 43": (B, "documentos apresentados à polícia e ao banco idênticos"), "FE 124": (B, "documentos da abertura eram os da ré"),
    "FE 77": (B, "ficha cadastral e extratos"), "CL 28": (B, "proposta de abertura e documento de identidade"),
    # adjudicação com o segundo leitor cego (22/11/2026): acolhidos FE 75, FE 96, FE 36, CL 50,
    # FE 41 e FE 26; mantido FE 124 (a falta de imagem é a leitura da defesa; a sentença lê nos
    # ofícios a abertura com documento pessoal, e uma testemunha cita resposta posterior com foto)
    "FE 75": (A, "identificação facial e documento no Mercado Pago (fl. 49)"),
    "FE 96": (A, "cadastro com fotografia e foto do RG (fl. 33)"),
    "FE 36": (B, "fichas cadastrais que atestam a abertura (fls. 10/11)"),
    "CL 50": (N, "só o comprovante da transferência"), "FE 41": (N, "só o comprovante do depósito"),
    "FE 26": (D, "banco confirmou o encerramento da conta a pedido do réu"),
    "FE 4": (C, "Bradesco não localizou selfie; conta com assinatura digital"),
    "FE 114": (C, "PagSeguro informou não ter solicitado foto nem documento"),
    "FE 92": (N, ""),
}
for c in ("FE 76", "FE 16", "CL 6", "FE 90", "CL 42", "FE 70", "FE 94", "FE 113",
          "CL 4", "FE 89", "CL 41", "FE 106", "FE 64", "CL 38"):
    MANUAL_I3[c] = (D, "")
# CL 6 e CL 41: a biometria dos autos é do saque e do acesso ao aplicativo, não da abertura;
# FE 113: a cota pede os documentos da abertura, que ainda não estão nos autos


def limpa(t):
    return CITACAO.sub(" ", tc.EMENTA.sub(" ", t))


def textos(numero):
    seg = json.load(open(os.path.join(EXT, "segmentos", f"{numero}.json"), encoding="utf-8"))
    den = re.sub(r"\s+", " ", seg.get("narrativa", "") + " " + seg.get("cota", ""))
    return limpa(den), limpa(tc.texto_sentenca(numero)), seg.get("capitulacao", "")


def achado(rx, t, larg=110):
    m = rx.search(t)
    return t[max(0, m.start() - larg):m.end() + larg] if m else ""


def le(caso, numero):
    den, sen, cap = textos(numero)
    x = dict(caso=caso, numero=numero)
    for k, rx in RX_USURPA.items():
        tr = achado(rx, den)
        x[f"u_{k}"] = bool(tr)
        x[f"tr_u_{k}"] = tr
    x["usurpa_meio"] = any(x[f"u_{k}"] for k in MEIO)
    x["usurpa_instrumento"] = x["u_terceiro"]
    x["usurpa"] = x["usurpa_meio"] or x["usurpa_instrumento"]
    x["usurpa_so_sentenca"] = (not x["usurpa"]) and any(rx.search(sen) for rx in RX_USURPA.values())
    x["cap_307"] = bool(re.search(r"\b307\b", cap))
    x["cap_308"] = bool(re.search(r"\b308\b", cap))
    x["cap_298_299"] = bool(re.search(r"\b29[89]\b", cap))
    x["sen_307_308"] = bool(re.search(r"art(igo|\.)?\s*30[78]\b", sen, re.I))
    tr_c = achado(CESSAO_ID, den) or achado(CESSAO_ID, sen)
    x["cessao_identidade"] = bool(tr_c)
    x["tr_cessao"] = tr_c
    cat, tr = "nada sobre a abertura", ""
    for k, rx in RX_ABERTURA:
        tr = achado(rx, den + " || " + sen)
        if tr:
            cat = k
            break
    if caso in MANUAL_I3:
        cat, tr = MANUAL_I3[caso][0], "manual: " + MANUAL_I3[caso][1]
    else:
        cat = "triagem: " + cat
    x["abertura"] = cat
    x["tr_abertura"] = tr
    return x


def base():
    den = {f'{d["estrato"]} {d["ordem"]}': d for d in csv.DictReader(open(os.path.join(EXT, "denuncias_tjsp.csv"), encoding="utf-8"))
           if not d["duplicata_de"]}
    q1 = {x["caso"]: x for x in csv.DictReader(open(os.path.join(SAIDA, "q1_alcance.csv"), encoding="utf-8"))}
    q7 = {x["caso"]: x for x in csv.DictReader(open(os.path.join(SAIDA, "q7_titular.csv"), encoding="utf-8"))}
    L = []
    for caso, d in den.items():
        x = le(caso, d["numero"])
        a = q1.get(caso, {})
        x.update(estrato=d["estrato"], comarca=d["comarca"], tipo_capitulacao=d["tipo_capitulacao"],
                 a_307=d["a_307"] == "True", a_298_299=d["a_298_299"] == "True",
                 falso_parente=d["m_falso_parente"] == "True", falsa_central=d["m_falsa_central"] == "True",
                 papel=a.get("papel", ""), nivel=a.get("nivel", ""), artificio=a.get("artificio", ""),
                 resultado=a.get("resultado", ""), tipo_acolhido=a.get("tipo_acolhido", ""), condena=a.get("condena", ""),
                 so_conta=caso in q7, versao=q7.get(caso, {}).get("versao", ""), grupo_versao=q7.get(caso, {}).get("grupo_versao", ""))
        art = x["artificio"]
        x["identidade_meio"] = ("pessoa real" if art in REAL or caso in PERFIL_REAL else "instituição" if art in INSTITUCIONAL
                                else "fictícia" if art in FICTICIA else "não usa identidade alheia" if art else "")
        x["identidade_meio"] = IDENT_MANUAL.get(caso, x["identidade_meio"])
        x["identidade_instrumento"] = INSTRUMENTO.get(caso, "")
        x["imputacao_identidade"] = IMPUTACAO.get(caso, "")
        x["cessao_manual"] = next((k for k, v in CESSAO_MANUAL.items() if caso in v), "")
        L.append(x)
    return L


def taxa(xs):
    c = [x for x in xs if x["resultado"] not in ("", "sem sentença")]
    k = sum(x["condena"] == "True" for x in c)
    return dict(n=len(xs), com_sentenca=len(c), condena=k, absolve=sum(x["resultado"] == "absolvição" for x in c),
                casos=sorted(x["caso"] for x in xs))


def resumo(L):
    out = {}
    fraude = [x for x in L if x["estrato"] in ("CL", "FE")]
    out["I1"] = dict(
        fraude=len(fraude),
        identidade_meio={e: dict(Counter(x["identidade_meio"] for x in fraude if x["estrato"] == e)) for e in ("CL", "FE")},
        identidade_meio_total=dict(Counter(x["identidade_meio"] for x in fraude)),
        capitulacao_por_identidade={k: dict(Counter(x["tipo_capitulacao"] for x in fraude if x["identidade_meio"] == k))
                                    for k in ("pessoa real", "instituição", "fictícia")},
        instrumento=INSTRUMENTO, cap_307_na_denuncia=[x["caso"] for x in L if x["cap_307"] or x["a_307"]],
        imputacao_autonoma=IMPUTACAO,
    )
    out["I2"] = dict(cessao={k: sorted(v) for k, v in CESSAO_MANUAL.items()}, cap_308=[x["caso"] for x in L if x["cap_308"]])
    sc = [x for x in L if x["so_conta"]]
    neg = [x for x in sc if x["grupo_versao"] == "nega ou não reconhece"]
    out["I3"] = dict(so_conta=len(sc), negativas=len(neg), abertura_negativas=dict(Counter(x["abertura"] for x in neg)),
                     abertura_demais_triagem=dict(Counter(x["abertura"] for x in sc if x not in neg)))
    out["I4"] = {k: taxa([x for x in neg if x["abertura"] == k]) for k in (A, B, C, D, N)}
    out["I4"]["abertura documentada (A+B)"] = taxa([x for x in neg if x["abertura"] in (A, B)])
    return out


def main():
    L = base()
    if len(sys.argv) > 1 and sys.argv[1] == "trechos":
        for x in L:
            if x["usurpa"] or x["cessao_identidade"] or x["so_conta"]:
                print(f"== {x['caso']} {x['numero']} | usurpa={x['usurpa']} cessao={x['cessao_identidade']} | abertura={x['abertura']} | versao={x['versao']} | {x['resultado']}")
                for k in USURPA:
                    if x[f"tr_u_{k}"]:
                        print(f"   U[{k}] {x[f'tr_u_{k}'][:260]}")
                if x["tr_cessao"]:
                    print(f"   C {x['tr_cessao'][:260]}")
                if x["so_conta"]:
                    print(f"   A {x['tr_abertura'][:260]}")
        return
    campos = [k for k in L[0] if not k.startswith("tr_u_")]
    with open(os.path.join(SAIDA, "i_identidade.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos, extrasaction="ignore")
        w.writeheader()
        w.writerows(L)
    R = resumo(L)
    json.dump(R, open(os.path.join(SAIDA, "i_resumo.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if "-q" not in sys.argv:
        print(json.dumps(R, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
