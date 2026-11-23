"""Aula de segurança da informação e criptografia, perguntas 1, 2 e 4 (linhas 1.1, 3.4, 4.1 e 2.3).

1. Como a barreira cai: em cada denúncia em que um mecanismo de acesso (senha, código,
   token, sessão, aparelho) estava entre o agente e o sistema, por onde ele passou.
2. A barreira no processo: depois da Lei 14.155/2021, que suprimiu do art. 154-A a
   "violação indevida de mecanismo de segurança", a denúncia ainda a narra, a sentença a
   exige e a técnica do agente pesa na pena?
4. Quem tem a chave: o acesso interno (credencial própria ou de colega) como oportunidade e
   como prova da autoria.

A pergunta 3 (quem paga pela barreira fraca) não tem script: reorganiza os números das
questões 3 e 6 (docs/analise/q3-tipologia-dano.md e q6-servico-vulnerabilidade.md).

Grava dados/analise/s_barreira.csv (uma linha por denúncia do universo) e s_resumo.json.
`valida` imprime os trechos das sentenças que acionam a valoração da técnica. `-q` grava
sem imprimir.

Decisões que não saltam aos olhos:
- Universo: as denúncias sem duplicata com o sistema como objeto (eixo da questão 2), mais
  as de sistema-meio em que a credencial saiu da vítima (indicador da questão 6) ou foi
  fornecida por quem tinha acesso legítimo (INV 10). Fora da tipologia ficam fora.
- A via de passagem do sistema-objeto é leitura à mão das narrativas (dicionário BARREIRA,
  com o trecho que a sustenta); a do sistema-meio vem do indicador da questão 6, que é
  triagem por termos, e por isso é piso.
- Regime legal pela data do fato contra 28/05/2021, data de publicação e vigência da Lei
  14.155/2021. A posição da sentença sobre a elementar vem de dados/aula/inv_elementar_seguranca.csv.
- A elementar na denúncia separa a imputação com a redação revogada ("mediante violação
  indevida de mecanismo de segurança") da violação narrada como fato; a transcrição do § 4º-B
  do art. 155 ("com ou sem violação de mecanismo de segurança") não conta.
- A valoração da técnica é triagem por termos no texto da sentença, conferida pela leitura
  dos trechos (`valida`); o texto do INV 2 está cortado em 100 mil caracteres pelo Codex e
  não traz a dosimetria.
"""
import csv
import glob
import json
import os
import re
import sys
from collections import Counter

BASE = os.path.join(os.path.dirname(__file__), "..")
AN = os.path.join(BASE, "dados/analise")
LEI_14155 = "2021-05-28"

INTERNO = "credencial própria de quem tinha acesso legítimo"
TERCEIRO = "credencial de quem tinha acesso legítimo, comprada ou cedida"
ENGANO = "credencial obtida da vítima por engano"
COACAO = "credencial obtida da vítima por relação ou coação"
ABERTO = "aparelho ou sessão em mãos, sem barreira narrada"
TECNICA = "técnica (falha explorada, programa malicioso, força bruta)"
RESISTIU = "a barreira resistiu"
INDET = "via não narrada"
SEM = "sem barreira: a vítima pagou ou autorizou, sem entregar credencial"
ORDEM = [INTERNO, TERCEIRO, ENGANO, COACAO, ABERTO, TECNICA, RESISTIU, INDET, SEM]

# Leitura à mão das narrativas (segmentos da extração), 22/11/2026. Trecho curto que decide.
BARREIRA = {
    "INV 1": (ABERTO, "na posse do celular da vítima, o denunciado invadiu o dispositivo"),
    "INV 2": (INTERNO, "colaboradores que agiam de dentro das empresas de telefonia celular e possuíam senhas de acesso"),
    "INV 4": (INDET, "ingressou na conta gov.br do ofendido, violando inclusive o modo de segurança em duas etapas"),  # segundo leitor
    "INV 6": (INDET, "invadiu as redes sociais da vítima"),
    "INV 8": (INTERNO, "responsáveis pelo desenvolvimento e manutenção do sistema, tinham acesso às senhas internas"),
    "INV 11": (TERCEIRO, "registros de usuários e senhas de acesso de policiais militares; adquiriu os acessos"),
    "INV 13": (INDET, "na posse do celular, os denunciados violaram o sistema de segurança"),
    "INV 14": (ABERTO, "subtraiu seu telefone celular, certamente com o objetivo de vasculhar"),
    "INV 17": (ENGANO, "mediante o envio de um link conseguiu se apoderar da aludida conta"),
    "INV 19": (TECNICA, "valendo-se de softwares maliciosos denominados JADX e FRIDA"),
    "INV 20": (ABERTO, "aproveitando-se da confiança da vítima, acessou o computador de uso de Leonardo"),
    "INV 21": (TERCEIRO, "listagem com números de CPFs pertencentes a policiais militares e respectivas senhas"),
    "INV 22": (INDET,  # segundo leitor; a perícia lista ferramentas, a denúncia não diz como entrou
               "invadiu dispositivo pertencente à Polícia Civil, mediante violação indevida de mecanismo de segurança"),
    "INV 24": (COACAO, "constrangeram a revelar a senha de desbloqueio dos telefones celulares"),
    "INV 26": (INDET, "invadiu dispositivo informático de uso alheio"),
    "INV 27": (COACAO, "continuou a acessar as contas da vítima e alterou o e-mail de recuperação"),
    "INV 28": (COACAO, "constrangeram a vítima a fornecer a senha de acesso ao aparelho"),
    "INV 29": (INDET, "violação da senha de acesso"),
    "INV 30": (INTERNO, "ex-funcionário da área de T.I., valendo-se de seus conhecimentos acerca dos dispositivos"),
    "INV 32": (INDET, "invadiram o aparelho de telefone celular da vítima"),
    "INV 33": (TECNICA, "aproveitando-se de uma vulnerabilidade do sistema da empresa vítima"),
    "INV 34": (TECNICA, "ataques de negação de serviço e de força bruta contra o sistema da INFOCAR"),  # segundo leitor
    "INV 35": (TECNICA, "fazendo uso de programas maliciosos (mikrotik e keylogger)"),
    "INV 36": (INDET, "invadiu e explorou a base de arquivos do INSS, por meios próprios ou com auxílio de terceiros"),  # segundo leitor
    "INV 38": (RESISTIU, "o dispositivo era provido de senha que ele não conseguiu descobrir nem violar"),
    "INV 39": (ABERTO, "por descuido, manteve a sessão do aplicativo WhatsApp Web aberta"),
    "INV 41": (INDET, "após ter invadido conta da plataforma Google, de titularidade da vítima"),
    "INV 42": (ENGANO, "solicitaram alguns dados e um código de segurança do Facebook, fornecidos pela vítima"),
    "INV 43": (ENGANO, "recebeu um link malicioso e dissimulado que, ao clicar, permitiu assumir o controle"),
    "INV 44": (INDET, "se apossou do aparelho celular da vítima, desbloqueou o dispositivo"),  # segundo leitor
    "INV 45": (INTERNO, "funcionário da empresa, adulterou e destruiu informações do sistema"),
    "CL 10": (INDET, "após burlarem o sistema de segurança do Banco do Brasil"),
    "CL 15": (INDET, "violaram os mecanismos de segurança do aplicativo do Banco do Brasil"),
    "CL 28": (TECNICA, "valendo-se do fato de que a máquina estava sem o antivírus instalado"),
    "CL 41": (INDET,  # segundo leitor
               "acessaram as contas através dos aplicativos instalados no celular roubado"),
    "FE 73": (INDET, "o comparsa desconhecido invadiu um perfil da rede social Instagram"),
    "FE 88": (INDET, "acessaram indevidamente a conta corrente da vítima"),
    "FE 97": (INDET, "através de meios não esclarecidos, acessaram o sistema de pedidos com a senha do cliente"),  # segundo leitor
    "INV 10": (TERCEIRO, "tinha livre acesso ao sistema, haja vista o fornecimento da senha pelas servidoras"),
}

# Sistema-meio em que o segundo leitor recusou a premissa da triagem da questão 6
# (dados/conferencia/seguranca/adjudicacao.csv): a maquininha e o pagamento feito pela vítima
# não passam por credencial entregue ao agente.
VIA_MEIO = {c: SEM for c in ("FE 105", "FE 18", "FE 29", "CL 24", "FE 50", "FE 110", "FE 16", "CL 49")}
VIA_MEIO.update({c: INDET for c in ("FE 10", "FE 102", "FE 17")})

# Elementar narrada como fato que a regex não pega (segundo leitor).
ELEM_DEN_MANUAL = {"INV 4"}

# Posição da sentença sobre a elementar, valoração na pena e prova da autoria, pela leitura
# integral do segundo leitor (dados/conferencia/seguranca/segundo_leitor_S*.csv), adjudicada.
def le_sentencas():
    mapa = json.load(open(os.path.join(BASE, "dados/conferencia/seguranca/mapa.json"), encoding="utf-8"))["S"]
    adj = {(x["campo"], x["caso"]): x["final"] for x in le(os.path.join(BASE, "dados/conferencia/seguranca/adjudicacao.csv"))}
    out = {}
    for a in glob.glob(os.path.join(BASE, "dados/conferencia/seguranca/segundo_leitor_S*.csv")):
        for x in le(a):
            c = mapa[x["id"].strip()]
            x["elementar_sentenca"] = adj.get(("elementar_sentenca", c), x["elementar_sentenca"])
            out[c] = x
    return out


# Prova da autoria no acesso interno, só onde a peça foi lida neste ponto.
PROVA = {
    "INV 2": "registro de login e token da operadora (token trocado a cada 30 segundos), horários fora do expediente e DDDs fora da região de trabalho (sentença)",
    "INV 11": "auditoria da Polícia Militar e IP do modem cadastrado em nome da mãe do denunciado (denúncia; questão 5)",
    "INV 21": "aparelho apreendido com o aplicativo do Detecta e a lista de CPFs e senhas (denúncia)",
    "INV 30": "IP do acesso ao servidor da empresa, administrado pela operadora (denúncia)",
    "INV 34": "IP do invasor obtido pela auditoria da própria empresa (questão 5)",
}

TERMO_ELEMENTAR = re.compile(r"(?<!com ou sem )(?<!com ou sem a )(viola\w*|burla\w*|atua[çc][ãa]o do) (indevid\w+ )?(de |a |à |os? |d[oa]s? )?(mecanismos? de seguran[çc]a|sistemas? de seguran[çc]a|barreiras? de seguran[çc]a)", re.I)
REDACAO_REVOGADA = re.compile(r"(mediante viola[çc][ãa]o indevida de|violando indevidamente) mecanismos? de seguran[çc]a", re.I)
TERMO_TECNICA = re.compile(r"(conhecimentos? t[ée]cnicos?|aptid[ãa]o t[ée]cnica|habilidade t[ée]cnica|sofistica[çd]|expertise|especialista em)", re.I)
TERMO_PENA = re.compile(r"(culpabilidade|circunst[âa]ncias (do crime|judiciais)|art(igo)?\.? 59|pena-base|pena base)", re.I)


def le(path):
    return list(csv.DictReader(open(path, encoding="utf-8")))


def texto(pasta, numero):
    arqs = sorted(glob.glob(os.path.join(BASE, "textos/tjsp", pasta, numero, "*.txt")))
    return re.sub(r"\s+", " ", " ".join(open(a, encoding="utf-8").read() for a in arqs))


def tecnica_na_pena(numero):
    """Trechos em que a sentença liga a técnica do agente à dosimetria (janela de 600 caracteres)."""
    t = texto("sentencas", numero)
    achados = []
    for m in TERMO_TECNICA.finditer(t):
        jan = t[max(0, m.start() - 600): m.end() + 600]
        if TERMO_PENA.search(jan):
            achados.append(t[max(0, m.start() - 200): m.end() + 200])
    return achados


def monta():
    q2 = {x["caso"]: x for x in le(os.path.join(AN, "q2_eliminacao.csv"))}
    q6 = {x["caso"]: x for x in le(os.path.join(AN, "q6_servico.csv"))}
    q5 = {x["caso"]: x for x in le(os.path.join(AN, "q5_tempo_dado.csv"))}
    elem = {x["caso"]: x for x in le(os.path.join(BASE, "dados/aula/inv_elementar_seguranca.csv"))}
    s2 = le_sentencas()
    L = []
    for caso, x in q2.items():
        if x["eixo_sistema"] == "fora":
            continue
        if caso in BARREIRA:
            via, trecho = BARREIRA[caso]
            origem = "leitura"
        elif caso in VIA_MEIO:
            via, trecho, origem = VIA_MEIO[caso], "", "segundo leitor"
        elif q6.get(caso, {}).get("credencial") == "True":
            via = COACAO if q6[caso]["artificio"] == "extorsao_transferencia" else ENGANO
            trecho, origem = "", "triagem q6"
        else:
            continue
        seg = os.path.join(BASE, "dados/extracao/segmentos", x["numero"] + ".json")
        narr = re.sub(r"\s+", " ", json.load(open(seg, encoding="utf-8"))["narrativa"]) if os.path.exists(seg) else ""
        fato = q5.get(caso, {}).get("data_fato", "")
        regime = "" if not fato else ("Lei 14.155/2021" if fato >= LEI_14155 else "Lei 12.737/2012")
        tec = tecnica_na_pena(x["numero"]) if x["eixo_sistema"] == "objeto" else []
        L.append({
            "caso": caso, "numero": x["numero"], "estrato": x["estrato"], "sistema": x["eixo_sistema"],
            "canal": x["eixo_canal"], "artificio": x["artificio"], "via": via, "origem_via": origem,
            "trecho": trecho, "data_fato": fato, "regime": regime,
            "denuncia_narra_elementar": bool(TERMO_ELEMENTAR.search(narr)) or caso in ELEM_DEN_MANUAL,
            "denuncia_redacao_revogada": bool(REDACAO_REVOGADA.search(narr)),
            "sentenca_elementar": elem.get(caso, {}).get("posicao", ""),
            "efeito_154A": elem.get(caso, {}).get("efeito_no_154A", ""),
            "tecnica_na_pena": bool(tec),
            "elementar_sentenca_2l": s2.get(caso, {}).get("elementar_sentenca", ""),
            "confianca_na_pena": s2.get(caso, {}).get("confianca_na_pena", "").strip() == "1",
            "prova_autoria_sentenca": s2.get(caso, {}).get("prova_autoria", "").strip(),
            "resultado": x["resultado"], "tipo_acolhido": x["tipo_acolhido"],
            "a_154A_denuncia": x["a_154A"], "prova_interna": PROVA.get(caso, ""),
        })
    return L


def resumo(L):
    obj = [r for r in L if r["sistema"] == "objeto"]
    pos = [r for r in obj if r["regime"] == "Lei 14.155/2021"]
    ante = [r for r in obj if r["regime"] == "Lei 12.737/2012"]
    chave = [r for r in L if r["via"] in (INTERNO, TERCEIRO)]
    R = {
        "universo": len(L),
        "via_sistema_objeto": {v: sum(r["via"] == v for r in obj) for v in ORDEM},
        "via_sistema_meio_triagem": {v: sum(r["via"] == v and r["sistema"] == "meio" for r in L) for v in ORDEM},
        "objeto_total": len(obj),
        "denuncia_narra_elementar": {
            "fato_posterior_14155": f'{sum(r["denuncia_narra_elementar"] for r in pos)} de {len(pos)}',
            "fato_anterior_14155": f'{sum(r["denuncia_narra_elementar"] for r in ante)} de {len(ante)}',
            "posterior_com_redacao_revogada": [r["caso"] for r in pos if r["denuncia_redacao_revogada"]],
            "posterior_narra_como_fato": [r["caso"] for r in pos if r["denuncia_narra_elementar"] and not r["denuncia_redacao_revogada"]],
        },
        "sentenca_elementar_pos_14155": dict(Counter(r["sentenca_elementar"] for r in pos if r["sentenca_elementar"])),
        "sentenca_elementar_pos_14155_2l": {k: [r["caso"] for r in pos if r["elementar_sentenca_2l"] == k] for k in ("exige_e_afasta", "exige_e_encontra", "dispensa", "nao_trata")},
        "confianca_na_pena": [r["caso"] for r in obj if r["confianca_na_pena"]],
        "vias_narradas": sum(r["via"] not in (INDET, SEM) for r in L),
        "via_total": {v: sum(r["via"] == v for r in L) for v in ORDEM},
        "tecnica_na_pena": [r["caso"] for r in obj if r["tecnica_na_pena"]],
        "acesso_interno": {
            "casos": [r["caso"] for r in chave],
            "por_via": dict(Counter(r["via"] for r in chave)),
            "resultado": dict(Counter(r["resultado"] for r in chave)),
            "com_prova_lida": [r["caso"] for r in chave if r["prova_interna"]],
            "prova_na_sentenca": {r["caso"]: r["prova_autoria_sentenca"] for r in chave},
        },
    }
    return R


def main():
    L = monta()
    os.makedirs(AN, exist_ok=True)
    with open(os.path.join(AN, "s_barreira.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(L[0]))
        w.writeheader()
        w.writerows(L)
    R = resumo(L)
    json.dump(R, open(os.path.join(AN, "s_resumo.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if "valida" in sys.argv:
        for r in L:
            if r["sistema"] == "objeto":
                for tr in tecnica_na_pena(r["numero"]):
                    print(f'== {r["caso"]}: {tr}\n')
    elif "-q" not in sys.argv:
        print(json.dumps(R, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
