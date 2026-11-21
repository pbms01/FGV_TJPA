"""Leitura da entrada do titular da conta na fraude (questão 7, linha 2.3): a versão que ele
dá na denúncia e na sentença, os antecedentes e a idade que a sentença registra, e o pedido
e a remuneração da conta que a questão 4 já leu.

Uso:
  python3 scripts/titular_conta.py valida      imprime a versão e o trecho que a sustenta em
                                               todas as denúncias de só conta, para conferência
  python3 scripts/titular_conta.py caso CL 26  imprime a leitura de uma denúncia

Decisões que não saltam aos olhos:
- A versão é procurada frase a frase, na narrativa e na cota da denúncia e no texto da
  sentença, só nas frases com verbo de declaração (alegou, afirmou, negou, admitiu, disse...),
  interrogatório, versão, álibi, silêncio ou revelia, para não tomar a descrição da conduta
  pela acusação ("cedeu sua conta") como versão do titular. O verbo de cessão precedido de
  negação ("nunca vendeu", "não emprestou") conta como negativa. A categoria mais específica vence, nesta
  ordem: cedeu mediante pagamento (venda, aluguel, porcentagem); aceitou proposta de trabalho
  ou renda; emprestou a alguém; perdeu
  o controle dos dados ou não reconhece a conta; nega; silêncio; não localizado ou revel.
- As leituras corrigidas à mão, depois de conferidos todos os trechos, estão em
  VERSAO_MANUAL, com o motivo.
- Antecedentes e idade vêm da dosimetria da sentença: reincidência ou maus antecedentes
  vencem primariedade; "menor de 21" ou o art. 65, I, do CP marcam o titular jovem.
"""
import csv
import glob
import json
import os
import re
import sys

BASE = os.path.join(os.path.dirname(__file__), "..")
EXT = os.path.join(BASE, "dados/extracao")

# só frases de declaração do titular, e não a descrição da conduta pela acusação ou pelo juiz
SUJEITO = re.compile(r"\b(alegou|alega|afirmou|afirma|negou|nega|admitiu|admite|confessou|declarou|disse|sustentou|aduziu|relatou|explicou|esclareceu|justificou|asseverou|informou|contou|suscitou)\b"
                     r"|interrogad|ouvid[oa] (em ju[íi]zo|na delegacia|em sede|perante)|em (seu )?interrogat[óo]rio|\bvers[ãa]o\b|\bálibi|silêncio|sil[êe]ncio|\brevel|revelia|n[ãa]o (foi )?(localizad|encontrad)", re.I)
NEGACAO = re.compile(r"((nunca|jamais|\bn[ãa]o)\s+([\w,/]+\s+){0,3}|\bneg(ou|a|ando)\s+(ter\s+|que\s+)?)$", re.I)
VERSOES = [
    ("cedeu mediante pagamento", r"\bvend(eu|ido|ida|ia|er|endo)\b[^.]{0,50}\b(sua |a |as |seus? )?(conta|cart[ãa]o|cart[õo]es|dados banc|chave)|\balug(ou|ado|ada|ar|uel)\b[^.]{0,40}(conta|cart)"
                                 r"|(conta|cart[ãa]o)[^.]{0,40}\b(vendid|alugad)|em troca de (R\$|valor|dinheiro|pagamento|uma quantia)|mediante (a |o )?(contrapresta[çc][ãa]o|pagamento|remunera|recebimento de R)"
                                 r"|\b(porcentagem|comiss[ãa]o)\b[^.]{0,80}(conta|valor|dinheiro|parte)|(tira|tirar|ficar|ficava|receberia|recebia) (com )?(a |uma )?(sua )?(parte|porcentagem)"),
    ("aceitou proposta de trabalho, renda ou crédito", r"(vaga de|vaga|oferta de (trabalho|emprego)|proposta de (trabalho|emprego)|renda extra|grupo de empregos|an[úu]ncio de (emprego|empr[ée]stimo|trabalho|vaga))[^.]{0,120}(conta|cart|pix)"
                                      r"|(conta|cart|pix)[^.]{0,120}(vaga de|oferta de (trabalho|emprego)|proposta de (trabalho|emprego)|renda extra)"),
    ("emprestou a alguém", r"\bemprest(ou|ado|ada|ar|ei|ava|ou-a|ado-a)\b[^.]{0,60}(conta|cart|dados|senha|celular|chave)|(conta|cart[ãa]o)[^.]{0,40}\bemprestad"
                           r"|(cedeu|ceder|cedido|cedida|cess[ãa]o)[^.]{0,40}(conta|cart)|solicit\w+ (o uso|a cess[ãa]o) d[ea] (sua )?conta|pediu (a |sua )?conta"
                           r"|a pedido d[eoa] (seu |sua |um |uma )?(amig|prim|namorad|irm|vizinh|conhecid|colega|cunhad|companheir|marido|esposa|filh|tio|tia|sobrinh)"),
    ("perdeu o controle ou não reconhece a conta", r"(perdeu|perdid|furtad|roubad|extraviad|clonad)[^.]{0,60}(document|celular|cart|RG|CNH|dados)|n[ãa]o (abriu|reconhece|reconheceu|tinha conhecimento d[ae]|sabia d[ae]|possu[ií]a) (a |essa |aquela |da |tal |qualquer )?conta"
                                                  r"|desconhec\w*[^.]{0,20}(a |da |aquela |tal |qualquer )?conta|conta (foi )?aberta (por terceir|sem (seu|o seu) conhecimento|com (os )?seus dados)|(utiliza(ram|do|da|ção indevida)|uso indevido) (de )?seus (dados|documentos)|tirado foto de seus documentos"),
    ("nega", r"\bneg(ou|a|ando)\b[^.]{0,40}(a prática|os fatos|participa|envolvimento|as acusa|a autoria|ter recebido|qualquer)|negativa de autoria"),
    ("silêncio", r"(direito (constitucional )?a?o sil[êe]ncio|permaneceu em sil[êe]ncio|manteve-se em sil[êe]ncio|optou por (permanecer em )?sil[êe]ncio|preferiu (permanecer em |o )?sil[êe]ncio|silenciou)"),
    ("não localizado ou revel", r"\brevel\b|revelia|n[ãa]o (foi )?(localizad|encontrad)|n[ãa]o compareceu"),
]
RX_VERSAO = [(k, re.compile(v, re.I)) for k, v in VERSOES]
CONFISSAO = re.compile(r"\bconfess(ou|a|ando|ada|ado)\b|confiss[ãa]o", re.I)
REINCIDENTE = re.compile(r"\breincid[êe]n|\breincidente|maus antecedentes|antecedentes (criminais )?(desfavor|negativ|maculad)", re.I)
PRIMARIO = re.compile(r"\bprim[áa]ri[oa]|bons antecedentes|sem antecedentes|tecnicamente prim", re.I)
QUEM = [
    ("parente ou companheiro", re.compile(r"\b(prim[oa]|namorad[oa]|companheir[oa]|cunhad[oa]|sobrinh[oa]|irm[ãa]o?|marido|esposa|filh[oa]|tio|tia|genro|padrasto)\b", re.I)),
    ("amigo, vizinho ou colega", re.compile(r"\b(amig[oa]|vizinh[oa]|colega)", re.I)),
    ("conhecido ou cliente", re.compile(r"\b(conhecid[oa]|cliente)\b", re.I)),
    ("credor", re.compile(r"\bagiota|d[íi]vida", re.I)),
    ("anúncio ou proposta", re.compile(r"an[úu]ncio|Facebook|grupo de|vaga", re.I)),
    ("desconhecido", re.compile(r"desconhecid|terceir|pessoa (que n[ãa]o|identificada apenas)", re.I)),
]
JOVEM = re.compile(r"menor de (21|vinte e um)|menoridade relativa|\b(18|19|20|dezoito|dezenove|vinte) anos( de idade)?,? (à época|na data|quando)", re.I)

# Correções da conferência dos trechos (python3 scripts/titular_conta.py valida).
VERSAO_MANUAL = {
    "CL 57": ("não localizado ou revel", "o réu é revel; a regra pegava a discussão da sentença sobre o inciso VII"),
    "FE 44": ("não localizado ou revel", "o titular não foi localizado e foi declarado revel; a regra pegava o depoimento da vítima"),
    "CL 54": ("não localizado ou revel", "a ré foi declarada revel; a regra pegava a negativa do titular da linha"),
    "FE 70": ("nega", "a ré negou o ardil e disse ser amiga da vítima; a regra pegava a negativa do titular da linha"),
    "FE 91": ("emprestou a alguém", "a ré admitiu ter fornecido os dados da conta ao então companheiro, preso, e sacado e repassado os valores"),
    "CL 31": ("emprestou a alguém", "interrogado, o réu disse que emprestava o cartão a um cliente, que se comprometera a fazer os pagamentos"),
    "FE 56": ("cedeu mediante pagamento", "admitiu ter fornecido a conta a um conhecido e recebido quantia em contrapartida"),
    "CL 23": ("cedeu mediante pagamento", "na polícia disse ter vendido o CPF; em juízo, que o emprestou a colega para abrir conta de jogo, com promessa de parte do lucro"),
    "CL 13": ("cedeu mediante pagamento", "um conhecido de infância pediu a conta emprestada e daria R$ 500"),
    "CL 8": ("cedeu mediante pagamento", "em juízo, disse ter emprestado o nome a um conhecido, para abrir uma empresa, e recebido R$ 200; na polícia negara"),
    "CL 44": ("emprestou a alguém", "na polícia negou usar a conta; em juízo, disse tê-la cedido a uma amiga que prometera trabalhar com aplicativo de transporte"),
}


def frases(t):
    return [f for f in re.split(r"(?<=[.;!?])\s+", t) if SUJEITO.search(f)]


# ementas de acórdãos citadas na sentença falam de outro réu (o "alugado" do caso Kevin Brian
# Russo aparece em três sentenças); saem antes da leitura
EMENTA = re.compile(r"(Caso em Exame|EMENTA)[\s\S]{0,6000}?(Tese de julgamento[^.]*\.([^.]*\.){0,3}|Dispositivo[^.]*\.)|\b(Apela[çc][ãa]o (Criminal|n)|AgRg|HC|REsp)[^()]{0,600}\((TJSP|STJ)[^)]*\)", re.I)


def versao(t):
    t = EMENTA.sub(" ", t)
    fs = frases(t)
    negou = None
    for k, rx in RX_VERSAO:
        for f in fs:
            for m in rx.finditer(f):
                if k in ("cedeu mediante pagamento", "aceitou proposta de trabalho, renda ou crédito", "emprestou a alguém") and NEGACAO.search(f[max(0, m.start() - 25):m.start()]):
                    negou = negou or f[max(0, m.start() - 120):m.end() + 80]  # "nunca vendeu", "não emprestou": é negativa
                    continue
                if k == "nega" and negou is None:
                    pass
                return k, f[max(0, m.start() - 120):m.end() + 80]
        if k == "emprestou a alguém" and negou:
            return "nega", negou
    return "sem versão", ""


def texto_sentenca(numero):
    fs = sorted(glob.glob(os.path.join(BASE, "textos/tjsp/sentencas", numero, "*")))
    return re.sub(r"\s+", " ", " ".join(open(f, encoding="utf-8", errors="ignore").read() for f in fs)) if fs else ""


def le(caso, numero):
    seg = json.load(open(os.path.join(EXT, "segmentos", f"{numero}.json"), encoding="utf-8"))
    den = re.sub(r"\s+", " ", seg.get("narrativa", "") + " " + seg.get("cota", ""))
    sen = texto_sentenca(numero)
    vd, td = versao(den)
    vs, ts = versao(sen)
    ordem = [k for k, _ in VERSOES] + ["sem versão"]
    # vence a mais específica das duas leituras
    final, fonte, trecho = (vd, "denúncia", td) if ordem.index(vd) <= ordem.index(vs) else (vs, "sentença", ts)
    if caso in VERSAO_MANUAL:
        final, fonte, trecho = VERSAO_MANUAL[caso][0], "manual", VERSAO_MANUAL[caso][1]
    alvo = trecho if final in ("cedeu mediante pagamento", "aceitou proposta de trabalho, renda ou crédito", "emprestou a alguém") else ""
    quem = ""
    for rotulo, rx_quem in QUEM:  # o vínculo mais próximo vence o genérico ("terceira pessoa ... sua sobrinha")
        if rx_quem.search(alvo):
            quem = rotulo
            break
    v = re.search(r"R\$ ?(\d[\d.]*(?:,\d{2})?)(?!\d)|\b(\d+) reais", alvo) if final == "cedeu mediante pagamento" else None
    valor = (v.group(1) or v.group(2)).rstrip(".") if v else ""
    # reincidência ou maus antecedentes afirmados, não negados ("não ostenta maus antecedentes")
    afirmados = [m for m in REINCIDENTE.finditer(sen)
                 if not re.search(r"(\bn[ãa]o|\bsem\b|inexist|ausent|aus[êe]ncia|\bnem\b|eventuais)[^.;]{0,60}$", sen[max(0, m.start() - 70):m.start()], re.I)]
    ant = "reincidente ou maus antecedentes" if afirmados else "primário" if PRIMARIO.search(sen) else ("sem sentença" if not sen else "não dito")
    trecho_ant = sen[max(0, afirmados[0].start() - 100):afirmados[0].end() + 60] if afirmados else ""
    return dict(versao=final, fonte_versao=fonte, trecho_versao=trecho, versao_denuncia=vd, versao_sentenca=vs, a_quem=quem, valor_cessao=valor,
                confissao=bool(CONFISSAO.search(" ".join(frases(den)) + " " + " ".join(frases(sen)))),
                antecedentes=ant, trecho_antecedentes=trecho_ant, jovem=bool(JOVEM.search(sen)), tem_sentenca=bool(sen))


def _so_conta():
    q5 = [x for x in csv.DictReader(open(os.path.join(BASE, "dados/analise/q5_tempo_dado.csv"), encoding="utf-8"))
          if x["nivel"] == "só conta" and x["fora"] == "False"]
    return [(x["caso"], x["numero"]) for x in q5]


def valida():
    from collections import Counter
    c = Counter()
    for caso, n in _so_conta():
        x = le(caso, n)
        c[x["versao"]] += 1
        print(f"{caso}: {x['versao']} ({x['fonte_versao']}) | den {x['versao_denuncia']} | sen {x['versao_sentenca']} | {x['trecho_versao'][:230]}")
    print(dict(c))


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "valida":
        valida()
    elif len(sys.argv) > 2 and sys.argv[1] == "caso":
        caso = " ".join(sys.argv[2:])
        n = dict(_so_conta())[caso]
        for k, v in le(caso, n).items():
            print(f"{k}: {v}")
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
