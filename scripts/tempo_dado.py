"""Leitura do tempo do dado nas denúncias (questão 5, linha 4.4): a data do fato, a data da
denúncia, as fontes de dado que a denúncia narra, agrupadas pelo custodiante, e os pedidos
de dado que a cota faz.

Uso:
  python3 scripts/tempo_dado.py valida       confere a data do fato contra a leitura à mão das
                                             29 denúncias da matriz e confere que todo achado
                                             das regras de operadora, plataforma, conexão e
                                             pedido na cota passou pela leitura manual
  python3 scripts/tempo_dado.py caso FE 13   imprime a leitura de uma denúncia

Decisões que não saltam aos olhos:
- A data do fato é a primeira data da narrativa depois da âncora ("Consta", "Apurou-se",
  "Relata", "1) "...). Ficam de fora as datas cujo contexto imediato (30 caracteres à
  esquerda, cortados no último parêntese) indica nascimento, documento (fls., boletim,
  ofício, relatório, portaria) ou assinatura ("Cidade, 9 de março de 2022"), as anteriores a
  2010 e as posteriores à denúncia. Sem data completa, vale mês e ano (dia 15). Num período
  ("entre janeiro de 2021 e outubro de 2022") vale o início, porque o dado mais antigo é o
  que primeiro vence; quando a denúncia só dá o limite ("até a data de 9 de novembro"), a
  data fica marcada como "até" e o intervalo é um mínimo.
- A data da denúncia é a da assinatura na própria peça (último "Cidade, DD de mês de AAAA"
  da cota ou do fecho) e, sem ela, a data do documento no PJe (manifesto.csv). As duas
  coincidem em até 7 dias em 94 das 98 denúncias que têm as duas; nas 4 que divergem (INV 17,
  CL 41, CL 11, INV 34) o documento do PJe é posterior à assinatura.
- As fontes de dado são triagem por termos, como os indícios da questão 1. As que dependem de
  custodiante que não seja banco (operadora, plataforma, provedor de conexão) são poucas e
  foram lidas uma a uma: o dicionário TERCEIRO registra o que cada denúncia diz ter obtido e
  o efeito, e FALSO_TERCEIRO, os achados da regra que não são dado obtido. O mesmo vale para
  os pedidos de dado na cota (PEDIDO_COTA e FALSO_PEDIDO).
"""
import csv
import datetime
import json
import os
import re
import sys

BASE = os.path.join(os.path.dirname(__file__), "..")
EXT = os.path.join(BASE, "dados/extracao")

MES = {"janeiro": 1, "fevereiro": 2, "marco": 3, "abril": 4, "maio": 5, "junho": 6, "julho": 7, "agosto": 8,
       "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12}
_M = r"(janeiro|fevereiro|mar[çc]o|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro)"
RX_EXT = re.compile(r"\b(\d{1,2})º?\s*(?:\(\w+\)\s*)?de\s+" + _M + r"\s+(?:de\s+)?(\d)\.?(\d{3})\b", re.I)
RX_NUM = re.compile(r"\b(\d{1,2})[/.](\d{1,2})[/.](\d{2,4})\b")
RX_MESANO = re.compile(r"\b(?:m[êe]s de )?" + _M + r"\s+de\s+(\d{4})", re.I)
FILTRO = re.compile(r"nascid|D\.N\.|boletim|B\.O\.|fls?\.|registrad[oa] (em|no dia)|lavrad|of[íi]cio|relat[óo]rio|datad"
                    r"|portaria (n|de)", re.I)
ASSINATURA = re.compile(r"\b[A-ZÀ-Ú][a-zà-ú]+(?:/[A-Z]{2})?, *$")  # "Tupã, " "Ribeirão Preto/SP, " (sem re.I)
LIMITE = re.compile(r"\b(até|anterior|antes)\b[^,;]{0,25}$", re.I)
ANCORA = re.compile(r"Consta|Segundo (o )?apurad|Apurou-se|Narra|Segundo consta|Restou apurado|Relata|noticiam"
                    r"|\bconsta\b|\b1\) ")
RX_FECHO = re.compile(r"\b[A-ZÀ-Ú][a-zà-ú]+(?:/[A-Z]{2})?, *(\d{1,2})º? de " + _M + r" de (\d)\.?(\d{3})")


def _mes(nome):
    return MES[nome.lower().replace("ç", "c")]


def _d(y, m, d):
    try:
        return datetime.date(int(y), int(m), int(d))
    except ValueError:
        return None


def datas(t):
    """Todas as datas do trecho, em ordem de posição: (posição, data, tipo)."""
    out = []
    for m in RX_EXT.finditer(t):
        out.append((m.start(), _d(m.group(3) + m.group(4), _mes(m.group(2)), m.group(1)), "dia"))
    for m in RX_NUM.finditer(t):
        y = m.group(3)
        out.append((m.start(), _d(("20" + y) if len(y) == 2 else y, m.group(2), m.group(1)), "dia"))
    dias = [(a, a + 40) for a, _, _ in out]
    for m in RX_MESANO.finditer(t):
        if any(a <= m.start() <= b for a, b in dias):
            continue  # "junho de 2022" dentro de "9 de junho de 2022"
        out.append((m.start(), _d(m.group(2), _mes(m.group(1)), 15), "mês"))
    return sorted([x for x in out if x[1]], key=lambda x: x[0])


def _primeira(t, limite):
    for pos, d, tipo in datas(t):
        ctx = t[max(0, pos - 30):pos].split(")")[-1]
        if FILTRO.search(ctx) or ASSINATURA.search(ctx):
            continue
        if not (2010 <= d.year <= 2026) or (limite and d > limite):
            continue
        return d, ("até" if LIMITE.search(t[max(0, pos - 40):pos]) else tipo)
    return None


def data_fato_regra(narr, limite=None):
    i = 0
    m = ANCORA.search(narr)
    if m:
        i = m.start()
    r = _primeira(narr[i:i + 3000], limite)
    if not r and i:
        r = _primeira(narr, limite)
    return r or (None, "")


# Correções da leitura manual. O CL 49 diz só "no dia dos fatos" e fica sem data.
DATA_MANUAL = {
    "INV 36": (datetime.date(2020, 7, 15), "mês", "a organização é narrada a partir de julho de 2020; a regra pegava o emprego anterior de um denunciado, em 2016"),
    "INV 27": (datetime.date(2025, 3, 15), "mês", "entre março e setembro do corrente ano, numa denúncia de novembro de 2025"),
    "CL 1": (datetime.date(2013, 7, 9), "dia", "OCR degradado: 9 de julho legível, ano pelo número do inquérito (2013)"),
    "FE 86": (datetime.date(2023, 11, 26), "até", "a denúncia diz só 'na data dos fatos'; a venda dos ingressos é anterior ao show de 26 de novembro de 2023, que a regra lia como data do fato"),
}

# Leitura à mão das 29 denúncias da matriz (trecho depois da âncora). Nas duas marcadas com
# "até" a denúncia só dá o limite; no CL 56 o primeiro fato é de "data incerta" e vale o
# segundo; no INV 11 vale o início do período (janeiro de 2021 a outubro de 2022).
REF_DATA = {
    "FE 35": "2023-03-27", "CL 42": "2022-01-10", "FE 107": "2021-08-11", "FE 55": "2023-02-28", "FE 24": "2022-06-09",
    "CL 41": "2022-03-01", "FE 122": "2021-12-30", "FE 52": "2022-04", "FE 65": "2021-10-05", "FE 39": "2021-09-21",
    "FE 54": "2024-02-02", "FE 79": "2021-08-26", "FE 84": "2022-03-23", "CL 1": "2013-07-09", "CL 11": "2024-07-24",
    "CL 18": "2024-11-20", "CL 7": "2026-03-10", "INV 39": "2024-01-24", "INV 20": "2024-04-26", "FE 50": "2023-03-14",
    "INV 14": "2023-12-26", "INV 30": "2023-09-07", "INV 11": "2021-01", "INV 21": "2023-11-09", "CL 56": "2023-07-24",
    "FE 105": "2023-08-18", "FE 115": "2023-01-02", "FE 77": "2022-06-24", "FE 96": "2025-06-09",
}

_MANIFESTO = None


def data_documento(numero):
    global _MANIFESTO
    if _MANIFESTO is None:
        _MANIFESTO = {}
        for r in csv.DictReader(open(os.path.join(BASE, "textos/tjsp/manifesto.csv"), encoding="utf-8")):
            _MANIFESTO[r["numero"]] = min(_MANIFESTO.get(r["numero"], "9999"), r["data"])
    v = _MANIFESTO.get(numero)
    return datetime.date.fromisoformat(v) if v else None


def data_assinatura(seg):
    t = re.sub(r"\s+", " ", seg.get("cota", "") + " " + seg.get("capitulacao", ""))
    ms = list(RX_FECHO.finditer(t))
    if not ms:
        return None
    m = ms[-1]
    return _d(m.group(3) + m.group(4), _mes(m.group(2)), m.group(1))


# Fontes de dado narradas, agrupadas pelo custodiante (triagem por termos na narrativa e na cota).
BANCOS = (r"(banco|institui[çc][ãa]o (financeira|banc[áa]ria|de pagamento)|Caixa Econ|Ita[úu]|Bradesco|Santander|Nu ?[Bb]ank"
          r"|Nu Pagamentos|Inter\b|PicPay|Mercado Pago|C6|PagSeguro|PagBank|Neon|Sicoob|Sicredi|BTG|Banco do Brasil"
          r"|Stone|Cielo|Companhia Global)")
EMP = r"(Meta|Facebook|Google|WhatsApp|Instagram|Mercado Livre|OLX|Telegram|Microsoft|Apple|Shopee|Webmotors|Yahoo|Uber|iFood)"
FONTES = {
    # dado que o banco guarda e entrega: quebra, resposta a ofício, cadastro e documentos da abertura, extrato da conta do investigado
    "banco": r"quebra (do|de) sigilo banc|sigilo banc[áa]rio|(informa[çc][õo]es|documentos|dados) (prestad|encaminhad|fornecid|enviad|remetid|apresentad)[oa]s? pel[oa]s? "
             + BANCOS + r"|of[íi]cio (d[oa]|ao|à) " + BANCOS + r"|resposta (d[oa]|ao) " + BANCOS
             + r"|(documenta[çc][ãa]o|ficha|proposta|dados|informa[çc][õo]es) (cadastra(l|is)|de abertura)|abertura (da|de) conta|apresentad[oa] pel[oa] "
             + BANCOS + r"|extratos? (banc[áa]ri[oa]s? )?(da conta )?(do|da|de titularidade d[oa]|em nome d[oa]|pertencente) (denunciad|acusad|investigad|indiciad)"
             + r"|biometri|selfie",
    # o que a vítima traz: comprovante, extrato próprio, print da conversa
    "vitima": r"\bprints?\b|captura(s)? de tela|screenshot|comprovantes?|extratos? (banc[áa]ri[oa]s? )?(do|da) (ofendid|v[íi]tima)|conversas? (apresentad|fornecid|juntad)",
    "operadora": r"\bERBs?\b|esta[çc][ãa]o r[áa]dio|(operadora|empresa) (Vivo|Claro|TIM|Oi)\b|operadora de telefonia|(Vivo|Claro|TIM)\b,? (informou|respondeu|forneceu)"
                 r"|extrato de liga|registros? de (chamadas|liga)|bilhetagem|linha (?!digit)(telef[ôo]nica |m[óo]vel |celular )?[^.]{0,60}(cadastrad|habilitad|registrad|em nome d|pertencia)"
                 r"|titular da linha (?!digit)|habilitou a linha",
    "plataforma": r"(of[íi]cio|respost|informa[çc][õo]es|dados cadastrais|registros)[^.]{0,50}(d[oa]|pel[oa]) (empresa )?" + EMP
                  + r"|Oficiad[oa],? (a empresa |o )?" + EMP + r"|" + EMP + r"( Inc\.?| Ltda\.?| Brasil| Platforms)?,? (informou|respondeu|forneceu|encaminhou|esclareceu)"
                  + r"|registros de acesso|provedor de aplica|dados cadastrais (da|do) (conta|perfil|e-mail)",
    "conexao": r"endere[çc]os? (de )?IPs?\b|n[úu]mero (de )?IP\b|\bIPs? (de origem|utilizad)|\bIP\b.{0,40}(administrad|operadora|provedor|vinculad)"
               r"|\bIP \d{1,3}\.\d|protocolo de internet|provedor de (conex|acesso)|porta l[óo]gica|modem",
    "dispositivo": r"(per[íi]cia|laudo|extra[çc][ãa]o|an[áa]lise|exame).{0,40}(celular|aparelho|telefone|dispositivo|smartphone)|(celular|aparelho|smartphone)s? (apreendid|periciad|examinad)|Cellebrite",
    "camera": r"c[âa]meras? de (segurança|monitoramento|vigil[âa]ncia)|CFTV|imagens (das|de|captadas por) c[âa]meras|circuito (interno|fechado)|filmagens? (de|das) (segurança|c[âa]meras)",
}
RX_FONTES = {k: re.compile(v, re.I) for k, v in FONTES.items()}
TERCEIROS = ("operadora", "plataforma", "conexao")

# Leitura manual de cada denúncia em que a narrativa ou a cota diz ter obtido dado de operadora,
# plataforma ou provedor de conexão: (custodiante, o que veio, efeito sobre a autoria).
TERCEIRO = {
    "INV 2": ("provedor de conexão, plataforma e operadora", "a Vivo vinculou o IP da criação de uma conta Google a uma linha usada com 12 IMEIs; Facebook e Google forneceram dados das contas do denunciado", "identificou o denunciado"),
    "INV 11": ("provedor de conexão", "as consultas indevidas saíram de modem da Vivo cadastrado em nome da mãe do denunciado, no endereço dele", "identificou o denunciado"),
    "INV 30": ("provedor de conexão", "o IP do acesso ao servidor, administrado pela Claro, tinha cadastro em nome da esposa do acusado", "identificou o denunciado"),
    "INV 42": ("plataforma e operadora", "a Meta informou o celular cadastrado na conta invadida e a TIM, o titular da linha, denunciado", "identificou o denunciado"),
    "FE 13": ("operadora", "a Claro informou que a linha do falso vendedor estava em nome do correntista denunciado", "identificou o denunciado"),
    "FE 25": ("operadora", "a linha que falou com a vítima estava em nome da denunciada; a da chave Pix, em nome de terceira, cujo inquérito foi arquivado", "identificou o denunciado"),
    "FE 55": ("operadora", "a Vivo identificou o denunciado como titular da linha usada no golpe", "identificou o denunciado"),
    "FE 61": ("operadora", "a linha TIM usada no contato foi habilitada por um dos denunciados", "identificou o denunciado"),
    "FE 108": ("operadora", "a TIM informou que a linha pertencia à denunciada no período do fato", "identificou o denunciado"),
    "FE 14": ("operadora", "a linha da falsa leiloeira estava em nome de terceiro, com o endereço da empresa da denunciada", "corroborou"),
    "INV 36": ("operadora", "a funcionária usava linha cadastrada em nome de outra denunciada", "corroborou"),
    "FE 5": ("operadora", "a linha que recebeu os comprovantes estava em nome de terceiro não denunciado (relatório de investigação)", "apontou terceiro não denunciado"),
    "CL 22": ("operadora", "a Vivo informou que a linha pré-paga do golpe estava em nome de terceiro, arquivado por ser linha 'facilmente habilitada em nome de terceiros'", "apontou terceiro não denunciado"),
    "CL 54": ("operadora", "a linha usada estava em nome de terceiro, arquivado porque negou a titularidade e não aparece nos extratos", "apontou terceiro não denunciado"),
    "FE 66": ("operadora", "os titulares das linhas usadas, não indiciados, ficaram fora da denúncia por falta de indícios", "apontou terceiro não denunciado"),
    "FE 16": ("operadora", "a Vivo informou que a linha pré-paga do golpe fora cancelada e desprogramada, sem dado de titular", "sem resultado"),
}
# Achados da regra que não são dado obtido de terceiro custodiante.
FALSO_TERCEIRO = {
    "CL 15": "o golpista ligou para a operadora da vítima; nenhum dado veio dela",
    "FE 41": "linha digitável do boleto",
    "INV 34": "o IP do invasor veio da auditoria da própria empresa vítima, confirmada por perícia, sem provedor de conexão",
}

# Pedidos de dado na cota (triagem por termos, lida uma a uma): (tipo, modo, alvo e finalidade).
PEDIDOS = {
    "bancario": r"(quebra|afastamento).{0,30}sigilo banc|(of[íi]cie-se|oficiad[oa]|of[íi]cio|requisit)[^.;]{0,40}" + BANCOS + r"|BACEN|SISBAJUD",
    "telefonico_telematico": r"sigilo (telef[ôo]nico|telem[áa]tico)|dados (telef[ôo]nicos|telem[áa]ticos)|operadoras?\b|intercepta",
    "pericia": r"per[íi]cia|laudos?",
    "preservacao": r"preserva[çc][ãa]o|guarda dos registros|congelamento",
}
RX_PEDIDOS = {k: re.compile(v, re.I) for k, v in PEDIDOS.items()}
PEDIDO_COTA = {
    "CL 7": [("bancário", "requer", "quebra das contas de destino, com cadastro, selfies e extratos, para rastrear o dinheiro")],
    "FE 5": [("bancário", "requer", "quebra do sigilo bancário do denunciado, com cadastro e extratos")],
    "FE 14": [("bancário", "requer", "documentação da abertura da conta e fotografia do titular")],
    "FE 113": [("bancário", "requer", "extrato da conta do indiciado")],
    "INV 32": [("bancário", "apoia representação policial", "quebra bancária e fiscal das contas dos denunciados, via BACEN")],
    "FE 122": [("bancário e telefônico ou telemático", "apoia representação policial", "quebras e bloqueio pedidos pela polícia depois da prisão, para alcançar comparsas")],
    "FE 17": [("telemático em aparelho apreendido", "requer", "extração dos dados do celular apreendido, para apurar a associação")],
    "FE 103": [("telefônico e telemático em aparelho apreendido", "indica representação futura", "celular apreendido, para apurar a participação dos demais")],
    "INV 8": [("telefônico", "aguarda resultado", "conteúdo da quebra já autorizada")],
    "FE 74": [("bancário", "junta resultado", "resultado da quebra do sigilo bancário da denunciada")],
    "INV 13": [("perícia em dispositivo", "requer", "celular da vítima, para provar o fato")],
    "INV 28": [("perícia em objetos apreendidos", "requer", "objetos apreendidos na casa de um denunciado")],
    "INV 21": [("perícia em dispositivo", "aguarda resultado", "laudos dos aparelhos eletrônicos apreendidos")],
    "CL 56": [("perícia em objetos apreendidos", "aguarda resultado", "laudos do material apreendido")],
}
FALSO_PEDIDO = {
    "FE 51": "ofícios de praxe a bancos e operadoras para localizar o réu, não para provar",
    "FE 109": "relata o resultado da quebra já feita, ao justificar o ANPP",
    "CL 43": "bloqueio BACENJUD para reparação", "CL 22": "bloqueio BACENJUD para reparação",
    "FE 55": "bloqueio BACENJUD para reparação", "CL 28": "bloqueio BACENJUD para reparação",
    "CL 14": "ofício à instituição de pagamento para encerrar a conta usada no golpe",
    "CL 25": "destruição de substâncias depois dos laudos", "INV 22": "compartilhamento dos laudos já juntados",
    "CL 4": "laudos periciais em geral", "FE 115": "cobrança das perícias em geral", "FE 128": "laudo de corpo de delito",
    "FE 50": "lista o laudo dos dispositivos apreendidos entre as provas",
}


def le(caso, numero):
    seg = json.load(open(os.path.join(EXT, "segmentos", f"{numero}.json"), encoding="utf-8"))
    narr = re.sub(r"\s+", " ", seg.get("narrativa", ""))
    cota = re.sub(r"\s+", " ", seg.get("cota", ""))
    doc, ass = data_documento(numero), data_assinatura(seg)
    den = ass or doc
    if caso in DATA_MANUAL:
        fato, prec, fonte = DATA_MANUAL[caso][0], DATA_MANUAL[caso][1], "manual"
    else:
        fato, prec = data_fato_regra(narr, den)
        fonte = "regra" if fato else ""
    x = dict(data_fato=fato, precisao=prec, fonte_data=fonte, data_denuncia=den,
             fonte_data_denuncia="assinatura" if ass else "PJe", data_documento_pje=doc)
    x["dias"] = (den - fato).days if fato and den else None
    texto = narr + " " + cota
    for k, rx in RX_FONTES.items():
        x["fonte_" + k] = bool(rx.search(texto))
    t = TERCEIRO.get(caso)
    for k in TERCEIROS:  # a leitura manual substitui a triagem nos custodiantes não bancários
        x["fonte_" + k] = bool(t) and {"operadora": "operadora", "plataforma": "plataforma", "conexao": "conexão"}[k] in t[0]
    x["terceiro"] = t[0] if t else ""
    x["terceiro_dado"] = t[1] if t else ""
    x["terceiro_efeito"] = t[2] if t else ""
    p = PEDIDO_COTA.get(caso, [])
    x["pedido_cota"] = "; ".join(f"{a} ({b})" for a, b, _ in p)
    x["pedido_cota_alvo"] = "; ".join(c for _, _, c in p)
    x["pedido_preservacao"] = bool(RX_PEDIDOS["preservacao"].search(cota))
    return x


def _den():
    return {f'{d["estrato"]} {d["ordem"]}': d for d in csv.DictReader(open(os.path.join(EXT, "denuncias_tjsp.csv"), encoding="utf-8"))
            if not d["duplicata_de"]}


def valida():
    D = _den()
    ok = 0
    for caso, ref in REF_DATA.items():
        x = le(caso, D[caso]["numero"])
        regra = x["data_fato"].isoformat() if x["data_fato"] else ""
        bate = regra.startswith(ref) if len(ref) == 7 else regra == ref
        ok += bate
        if not bate:
            print(f"  {caso}: regra {regra} ({x['precisao']}, {x['fonte_data']}), mão {ref}")
    print(f"data do fato em {len(REF_DATA)} denúncias da matriz: {ok} batem")
    # todo achado das regras de terceiro custodiante e de pedido na cota passou pela leitura manual
    falta = []
    for caso, d in D.items():
        seg = json.load(open(os.path.join(EXT, "segmentos", f'{d["numero"]}.json'), encoding="utf-8"))
        narr, cota = (re.sub(r"\s+", " ", seg.get(k, "")) for k in ("narrativa", "cota"))
        if any(RX_FONTES[k].search(narr + " " + cota) for k in TERCEIROS) and caso not in TERCEIRO and caso not in FALSO_TERCEIRO:
            falta.append(("terceiro", caso))
        if any(RX_PEDIDOS[k].search(cota) for k in ("bancario", "telefonico_telematico", "pericia")) \
                and caso not in PEDIDO_COTA and caso not in FALSO_PEDIDO:
            falta.append(("pedido", caso))
    print("achados sem leitura manual:", falta or "nenhum")
    sem = [c for c, d in D.items() if not le(c, d["numero"])["data_fato"]]
    print("sem data do fato:", sem)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "valida":
        valida()
    elif len(sys.argv) > 2 and sys.argv[1] == "caso":
        caso = " ".join(sys.argv[2:])
        for k, v in le(caso, _den()[caso]["numero"]).items():
            print(f"{k}: {v}")
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
