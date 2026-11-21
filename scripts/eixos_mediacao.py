"""Eixos da mediação técnica, comuns às análises da fase 1 (questões 1 e 2).

Segue o critério do doc de linhas de pesquisa do Project (versão 0.3): o teste de
eliminação de Wall, reformulado em dois eixos. Retira-se o sistema informático, em rede ou
isolado, e observa-se se a conduta desaparece, perde escala ou continua por outros meios;
depois, identifica-se o canal pelo qual o agente chegou ao sistema (ou, na fraude, à
vítima que opera o sistema). A internet é um canal entre outros.

- sistema: "objeto" quando o dispositivo, a conta, a base ou o sistema é o alvo (crime
  informático próprio: desaparece sem o sistema); "meio" quando o sistema serve à conduta
  sem ser o alvo (crime informático impróprio: continua por outros meios); "fora" para o
  fato sem fraude nem invasão. A perda de escala não se mede na base, porque cada processo
  individualiza a vítima. A separação entre meio relevante e meio acessório (o sistema
  bancário que só registra o depósito de um golpe por telefone fixo) é pendência.
- canal: internet; telefonia; rede interna (sistema corporativo ou estatal acessado por
  quem está dentro); contato físico com o equipamento (o celular da parceira, o aparelho
  roubado); presencial (engano face a face); correio (boleto sem outro canal descrito);
  sem contato (o agente opera só sobre o sistema).
- distância: agrupamento dos canais, não terceiro eixo. "à distância" para internet,
  telefonia e correio; "próxima" para contato físico, rede interna e presencial. A
  questão 1 mostrou que é por esse agrupamento que varia a atribuição da autoria.

O teste de Wall, que retira só a internet, aparece na coluna `wall`, que mostra onde ele
classifica mal (os crimes próprios por contato físico ou rede interna).
"""
import csv
import os
from collections import Counter, defaultdict

BASE = os.path.join(os.path.dirname(__file__), "..")
EXT = os.path.join(BASE, "dados/extracao")

# Sistema-objeto, caso a caso, com o modo de acesso ao sistema atacado.
# remoto = pela internet; local = acesso físico ao aparelho ou ao terminal;
# rede interna = sistema corporativo ou estatal acessado por login, sem internet necessária.
OBJETO = {
    "INV 1": "local",        # celular tomado da ex-namorada
    "INV 2": "remoto",       # SIM swap e transferências bancárias
    "INV 4": "local",        # dispositivo de um juiz
    "INV 6": "remoto",       # Instagram e Booking da ex-parceira
    "INV 8": "remoto",       # ex-prestadores de TI com senhas retidas
    "INV 11": "rede interna",  # COPOM e DETECTA com logins de policiais
    "INV 13": "local",       # WhatsApp no celular furtado
    "INV 14": "local",       # celular furtado para vasculhar mensagens (sem invasão narrada)
    "INV 17": "remoto",
    "INV 19": "remoto",      # engenharia reversa do app do banco
    "INV 20": "rede interna",  # computador de colega na empresa
    "INV 21": "rede interna",
    "INV 22": "remoto",
    "INV 24": "local",       # devassa dos celulares roubados
    "INV 26": "remoto",
    "INV 27": "remoto",
    "INV 28": "local",
    "INV 29": "remoto",
    "INV 30": "remoto",      # servidor AWS
    "INV 32": "remoto",      # linha reabilitada em outro aparelho
    "INV 33": "remoto",
    "INV 34": "remoto",
    "INV 35": "remoto",
    "INV 36": "remoto",      # base invadida para montar consignados
    "INV 38": "local",
    "INV 39": "local",       # WhatsApp Web deixado aberto no posto de saúde
    "INV 41": "remoto",
    "INV 42": "remoto",
    "INV 43": "remoto",
    "INV 44": "local",
    "INV 45": "rede interna",  # sistema da empresa adulterado pelo empregado
    "CL 10": "remoto",
    "CL 15": "remoto",
    "CL 28": "remoto",       # tela falsa trava o computador e o comparsa transfere
    "CL 41": "local",        # apps bancários do celular roubado
    "FE 73": "remoto",       # Instagram invadido para anunciar venda falsa
    "FE 88": "remoto",
    "FE 97": "remoto",       # senha de cliente da VR Benefícios
}
# Canal do ardil corrigido à mão quando o código de meio engana.
CANAL_MANUAL = {
    "FE 17": "internet",     # compras pagas por link com cartões de terceiros
    "FE 10": "internet",     # cartões pedidos no sistema do banco com dados da vítima
}
ANUNCIO_ONLINE = {"venda_falsa", "investimento_falso", "falsa_taxa_plataforma", "falso_relacionamento"}
FORA = {"outro"}


def le_codificacao():
    """As três rodadas de codificação. A nota da r2 tem vírgula sem aspas (INV 45), por
    isso o que passa da 16ª coluna volta para a nota."""
    out = {}
    for f, fonte in [("codificacao_manual_r1.csv", "manual"), ("codificacao_manual_r2.csv", "manual"),
                     ("codificacao_assistida.csv", "assistida")]:
        linhas = list(csv.reader(open(os.path.join(EXT, f), encoding="utf-8")))
        cab = linhas[0]
        for r in linhas[1:]:
            d = dict(zip(cab, r[:16] + [",".join(r[16:])]))
            d["fonte_codificacao"] = fonte
            out[d["numero"]] = d
    return out


def ponderada(linhas, chave, ordem=None):
    """Distribuição ponderada pelo peso amostral: {categoria: (n, %)}."""
    soma, n = defaultdict(float), Counter()
    for x in linhas:
        k = chave(x)
        soma[k] += x["peso"]
        n[k] += 1
    tot = sum(soma.values())
    ks = ordem or sorted(soma, key=lambda k: -soma[k])
    return {k: (n[k], round(100 * soma[k] / tot, 1) if tot else 0.0) for k in ks if n[k]}


def canal(caso, c):
    """Canal do ardil, para as condutas em que o sistema não é o objeto."""
    if caso in CANAL_MANUAL:
        return CANAL_MANUAL[caso]
    m = c["meio_contato"]
    if c["artificio"] in ANUNCIO_ONLINE:
        return "internet"
    if m in ("whatsapp", "rede_social", "site", "email"):
        return "internet"
    if m == "telefone":
        return "telefonia"
    if m == "presencial":
        return "presencial"
    if m == "boleto":
        return "postal"
    if m == "sistema":
        return "sem contato"
    return "outro"


CLASSES = ["próprio, pela internet", "próprio, por rede interna", "próprio, por contato físico",
           "impróprio, pela internet", "impróprio, por telefonia", "impróprio, presencial",
           "impróprio, por correio ou sem contato", "fora"]
# Correspondência com as classes de Wall, que eliminam só a internet.
WALL = {"próprio, pela internet": "verdadeiro", "próprio, por rede interna": "tradicional (erro do teste)",
        "próprio, por contato físico": "tradicional (erro do teste)", "impróprio, pela internet": "híbrido",
        "impróprio, por telefonia": "tradicional", "impróprio, presencial": "tradicional",
        "impróprio, por correio ou sem contato": "tradicional", "fora": ""}


def eixos(caso, c):
    """Devolve os dois eixos, a distância, a classe, o resultado dos dois testes e a classe de Wall."""
    if c["artificio"] in FORA:
        return dict(sistema="fora", canal_eixo="", distancia="", classe="fora", sem_internet="", sem_sistema="",
                    wall="", canal="", acesso="")
    if caso in OBJETO:
        acesso = OBJETO[caso]
        ce = {"remoto": "internet", "rede interna": "rede interna", "local": "contato físico"}[acesso]
        classe = {"internet": "próprio, pela internet", "rede interna": "próprio, por rede interna",
                  "contato físico": "próprio, por contato físico"}[ce]
        return dict(sistema="objeto", canal_eixo=ce, distancia="à distância" if ce == "internet" else "próxima",
                    classe=classe, sem_internet="desaparece" if ce == "internet" else "persiste igual",
                    sem_sistema="desaparece", wall=WALL[classe], canal="", acesso=acesso)
    k = canal(caso, c)
    ce = {"postal": "correio"}.get(k, k)
    dist = {"internet": "à distância", "telefonia": "à distância", "correio": "à distância",
            "presencial": "próxima", "sem contato": "sem contato"}.get(ce, "")
    classe = {"internet": "impróprio, pela internet", "telefonia": "impróprio, por telefonia",
              "presencial": "impróprio, presencial"}.get(ce, "impróprio, por correio ou sem contato")
    return dict(sistema="meio", canal_eixo=ce, distancia=dist, classe=classe,
                sem_internet="continua por outros meios" if ce == "internet" else "persiste igual",
                sem_sistema="continua por outros meios", wall=WALL[classe], canal=k, acesso="")
