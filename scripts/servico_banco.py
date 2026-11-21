"""Leitura da vulnerabilidade da vítima e dos pontos do serviço financeiro por onde a fraude
passou (questão 6, linhas 3.4 e 4.1): família do artifício, vítima idosa e pessoa jurídica,
credencial ou cartão entregue, acesso remoto, crédito contratado em nome da vítima, mais de
uma operação da vítima, repasse ou saque imediato pela conta de destino, e o que a denúncia
diz que o banco fez.

Uso:
  python3 scripts/servico_banco.py valida      imprime, nas 29 denúncias da matriz, o trecho
                                               que acionou cada indicador por termos
  python3 scripts/servico_banco.py caso CL 48  imprime a leitura de uma denúncia

Decisões que não saltam aos olhos:
- A família do artifício agrupa a codificação pelo que a fraude imita. A taxa antecipada se
  divide: o falso empréstimo imita instituição financeira; a falsa vaga e o falso editor
  (CL 44, FE 9, FE 117) imitam oferta. O sequestro de conta fica com os ataques à conta,
  porque o ato que abre o golpe é a tomada da conta. As famílias fora do serviço financeiro
  (controle da parceira, devassa, venda de dados, insider, inserção de dados em sistema
  público) ficam fora da análise.
- Vítima idosa é a da extração (idade, "idoso", Estatuto) ou o §4º do 171 na capitulação; as
  44 denúncias foram lidas e só o FE 29, em que a denúncia fala das vítimas do grupo em geral,
  sai.
- Crédito em nome da vítima e reação do banco foram lidos um a um (CREDITO e REACAO); os
  demais pontos do serviço são triagem por termos.
"""
import csv
import json
import os
import re
import sys

BASE = os.path.join(os.path.dirname(__file__), "..")
EXT = os.path.join(BASE, "dados/extracao")

FAMILIA = {
    "falsa_central": "imita instituição", "boleto_falso": "imita instituição", "falso_advogado": "imita instituição",
    "falsa_taxa_plataforma": "imita instituição", "taxa_antecipada": "imita instituição",
    "venda_falsa": "imita oferta", "investimento_falso": "imita oferta",
    "falso_parente": "imita relação pessoal", "falso_conhecido": "imita relação pessoal", "falso_relacionamento": "imita relação pessoal",
    "maquininha": "manipula o pagamento", "compra_fraudulenta_empresa": "manipula o pagamento",
    "invasao_sistema_bancario": "ataca a conta ou o aparelho", "sequestro_conta": "ataca a conta ou o aparelho",
    "roubo_celular_invasao": "ataca a conta ou o aparelho", "extorsao_transferencia": "ataca a conta ou o aparelho",
    "insercao_dados_falsos": "ataca a conta ou o aparelho",
}
FAMILIAS = ["imita instituição", "imita oferta", "imita relação pessoal", "manipula o pagamento", "ataca a conta ou o aparelho"]
OFERTA = {"CL 44", "FE 9", "FE 117"}             # taxa antecipada que não imita instituição
FORA_SERVICO = {"INV 10", "INV 4"}               # inserção de dados em sistema público, sem conta da vítima
NAO_IDOSA = {"FE 29": "a denúncia fala das vítimas do grupo em geral, não da vítima do fato"}
# Aumento pela idade na capitulação que a coluna a_171_4 da extração não lê (lido nas 7
# denúncias de vítima idosa sem o §4º do 171): o §4º-C, II, do 155, o §4º do 171 escrito como
# "c.c. §4º" e a agravante do art. 61, II, h. Sem aumento ficam FE 3 (171 §2º-A c.c. §3º),
# INV 36 (organização criminosa e lavagem) e CL 36 (receptação do produto do golpe).
AUMENTO_MANUAL = {"FE 84": "155, §4º-C, II", "CL 24": "155, §4º-C, II", "CL 39": "171, §4º", "CL 10": "agravante do art. 61, II, h"}
PJ = {"CL 28", "CL 41", "FE 124", "FE 97"}  # pessoa jurídica lida na nota da codificação, além da compra fraudulenta contra empresa

# Crédito contratado ou alterado em nome da vítima, lido na narrativa.
CREDITO = {
    "CL 48": "acesso à conta pela falsa central e empréstimo de R$ 8.630,04 em nome da vítima, transferido em seguida",
    "FE 88": "comparsas acessam a conta do aposentado e contratam consignado de R$ 6.300, repassado aos denunciados",
    "CL 41": "com o celular roubado, empréstimo de R$ 26.000 pelo aplicativo do banco e Pix para as contas dos denunciados",
    "CL 18": "sob ameaça, senha dos aplicativos e empréstimo de R$ 15.600, retirado rapidamente para terceiros",
    "FE 54": "depois de entregar os cartões ao motoboy, transferências e empréstimos na conta da vítima",
    "FE 58": "falso funcionário do banco altera o valor do consignado pedido, contrata outro e abre conta em nome da vítima",
    "FE 70": "empréstimo contratado na conta da vítima pela falsa central e não cancelado pelo banco: 84 parcelas na aposentadoria",
    "INV 36": "consignados montados por correspondentes bancários em nome de aposentados do INSS",
}
# O que a narrativa diz que o banco, a plataforma de pagamento ou a credenciadora fez.
REACAO = {
    "INV 35": ("bloqueou a conta de destino", "o banco levantou a fraude e bloqueou a conta do denunciado"),
    "FE 16": ("bloqueou a conta de destino", "a instituição bloqueou e encerrou a conta da titular meses depois, por suspeita de golpe"),
    "CL 43": ("bloqueou a conta de destino", "o titular diz ter sofrido prejuízo com o bloqueio da conta"),
    "CL 28": ("aviso sem reversão", "a empresa avisou o banco logo, mas o dinheiro já fora repassado minutos depois a outras contas"),
    "FE 88": ("manteve a cobrança", "apesar da impugnação, o banco não cancelou o empréstimo"),
    "FE 70": ("manteve a cobrança", "o banco não cancelou o empréstimo, descontado em 84 parcelas da aposentadoria"),
    "CL 48": ("ressarcimento parcial", "o mútuo foi cancelado, mas os valores transferidos não foram ressarcidos"),
    "FE 47": ("recusou responsabilidade", "o Mercado Pago disse não responder porque a compra não foi feita no Mercado Livre"),
    "CL 34": ("ressarciu a vítima", "a vítima buscou o banco e foi ressarcida"),
    "CL 41": ("ressarciu a vítima", "o PagSeguro ressarciu o mercado e assumiu o prejuízo"),
    "FE 17": ("estornou contra o lojista", "as compras foram contestadas pelos titulares dos cartões e os pagamentos ao lojista, frustrados"),
}

TERMOS = {
    # a vítima entrega senha, código ou cartão, ou o golpista a obtém
    "credencial": r"\bsenhas?\b|\btoken\b|c[óo]digos? (de )?(verifica|seguran|acesso|valida|sms|recebid)|cart(ão|ões)[^.]{0,60}(entreg|recolh|retir|busc)"
                  r"|recolh\w+ (o|os) cart|motoboy|c[óo]digo (que|enviado)",
    "acesso_remoto": r"acesso remoto|anydesk|teamviewer|malware|instal\w+ (de )?(um |o )?(aplicativo|programa|app)|aplicativo (de acesso|malicioso|falso)|tela falsa",
    # a própria vítima faz mais de uma operação
    "varias_operacoes": r"(v[íi]tima|ofendid[oa]|lesad[oa])[^.]{0,120}(fez|efetuou|realizou|transferiu|depositou|pagou)[^.]{0,40}"
                        r"\b(duas|tr[êe]s|quatro|cinco|seis|sete|oito|nove|dez|[2-9]|\d{2}|diversas|v[áa]rias|sucessivas)\b[^.]{0,15}"
                        r"(transfer[êe]ncias|opera[çc][õo]es|transa[çc][õo]es|pix|dep[óo]sitos|pagamentos|boletos)"
                        r"|(duas|tr[êe]s|quatro|cinco|seis|sete|oito|nove|dez|diversas|v[áa]rias|sucessivas) (transfer[êe]ncias|transa[çc][õo]es|dep[óo]sitos|pagamentos)[^.]{0,60}(d[ao] v[íi]tima|d[ao] ofendid|pela v[íi]tima|pel[ao] ofendid)",
    # a conta de destino repassa ou saca logo
    "repasse_imediato": r"repass\w*[^.]{0,30}\b(valor|valores|quantia|quantias|dinheiro|import[âa]ncia|produto|montante|parte)\b"
                        r"|\b(valor|valores|quantia|dinheiro|import[âa]ncia)[^.]{0,40}repassad|pulveriz|transferi(u|ram|do)[^.]{0,80}(outra|outras|terceir|diversas) contas?"
                        r"|sac(ou|aram|ado|ados|ada|adas)[^.]{0,80}(imediat|logo|mesmo dia|em seguida|minutos|para (evitar|impedir))"
                        r"|(imediatamente|logo em seguida|minutos depois)[^.]{0,40}(sac|transferi|repass)",
}
RX = {k: re.compile(v, re.I) for k, v in TERMOS.items()}


def familia(caso, artificio):
    if caso in FORA_SERVICO:
        return ""
    if artificio == "taxa_antecipada" and caso in OFERTA:
        return "imita oferta"
    return FAMILIA.get(artificio, "")


def le(caso, d, c):
    """d: linha de denuncias_tjsp.csv; c: codificação."""
    seg = json.load(open(os.path.join(EXT, "segmentos", f'{d["numero"]}.json'), encoding="utf-8"))
    narr = re.sub(r"\s+", " ", seg.get("narrativa", ""))
    x = dict(familia=familia(caso, c["artificio"]),
             idosa=(d["vitima_idosa"] == "True" or d["a_171_4"] == "True") and caso not in NAO_IDOSA,
             majorante_4=d["a_171_4"] == "True",
             aumento_idade=("171, §4º" if d["a_171_4"] == "True" else AUMENTO_MANUAL.get(caso, "")),
             pj=caso in PJ or c["artificio"] == "compra_fraudulenta_empresa")
    for k, rx in RX.items():
        m = rx.search(narr)
        x[k] = bool(m)
        x["trecho_" + k] = narr[max(0, m.start() - 60):m.end() + 40] if m else ""
    x["credito_vitima"] = caso in CREDITO
    x["nota_credito"] = CREDITO.get(caso, "")
    r = REACAO.get(caso)
    x["reacao_banco"] = r[0] if r else ""
    x["nota_reacao"] = r[1] if r else ""
    return x


def _base():
    sys.path.insert(0, os.path.dirname(__file__))
    from eixos_mediacao import le_codificacao
    cod = le_codificacao()
    D = {f'{d["estrato"]} {d["ordem"]}': d for d in csv.DictReader(open(os.path.join(EXT, "denuncias_tjsp.csv"), encoding="utf-8"))
         if not d["duplicata_de"]}
    return D, cod


def valida():
    from organizacao import REF_N  # as 29 denúncias da matriz
    D, cod = _base()
    for caso in REF_N:
        x = le(caso, D[caso], cod[D[caso]["numero"]])
        print(f"== {caso} | {cod[D[caso]['numero']]['artificio']} | família {x['familia'] or '-'} | idosa {x['idosa']}")
        for k in TERMOS:
            if x[k]:
                print(f"   {k}: {x['trecho_' + k]}")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "valida":
        valida()
    elif len(sys.argv) > 2 and sys.argv[1] == "caso":
        D, cod = _base()
        caso = " ".join(sys.argv[2:])
        for k, v in le(caso, D[caso], cod[D[caso]["numero"]]).items():
            print(f"{k}: {v}")
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
