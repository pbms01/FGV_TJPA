"""Leitor da organização narrada nas denúncias (questão 4, linha 2.1).

Para cada denúncia sem duplicata, lê o número de denunciados, o enquadramento dado ao
concurso (organização criminosa da Lei 12.850/2013, associação criminosa do art. 288 do
CP, concurso de pessoas ou autoria singular) e, para o titular de conta, quem lhe pediu a
conta segundo a narrativa. A estrutura do grupo (divisão de papéis entre os denunciados,
coordenação, vínculo pessoal e reiteração) vem da leitura do assistente nas denúncias com
dois ou mais denunciados ou com 288 ou Lei 12.850 (dicionário ESTRUTURA), feita sobre a
nota da codificação e os trechos de contexto dos termos de coordenação, recrutamento e
parentesco.

Uso (da raiz do repo):

    python3 scripts/organizacao.py valida        # número de denunciados contra a leitura à mão da matriz
    python3 scripts/organizacao.py caso FE 55    # o que o leitor extrai de um caso

Decisões que não saltam aos olhos:
- O número de denunciados soma os nomes em maiúsculas da capitulação (até o pedido e o
  rol), os nomes do texto integral seguidos de qualificação ("qualificado", "qual.", RG,
  CPF, "vulgo"), e, se nada houver, os nomes em caixa mista entre "denuncio" e "como
  incurso" (FE 24). O texto integral entra porque, nas denúncias de São José dos Campos, a
  primeira frase, onde estão os nomes, ficou fora do segmento da narrativa (CL 10, FE 100).
  Nomes seguidos de "Promotor", "Analista" ou "Estagiário" são de quem assina (FE 26, FE 78).
  A deduplicação usa as quatro primeiras letras do primeiro e do último nome, sem acento,
  o que junta grafias variantes (RONALD/RONALDO, no FE 39) e mantém irmãos (FE 31).
  Os casos que a regra erra, achados na revisão das denúncias plurais e das com contagem
  duvidosa, estão em N_MANUAL.
- "Concurso de pessoas" é a capitulação com art. 29 ou a narrativa de ajuste, unidade de
  desígnios, comparsas ou coautores não identificados. A capitulação de 288 e de Lei 12.850
  é lida na capitulação, e a organização criminosa prevalece sobre o 288.
"""
import csv
import json
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(__file__))
from reparacao_387 import texto_denuncia  # noqa: E402

BASE = os.path.join(os.path.dirname(__file__), "..")
EXT = os.path.join(BASE, "dados/extracao")

UP = "A-ZÁÉÍÓÚÂÊÔÃÕÇÜ"
LO = "a-zà-ü"
PART = {"DA", "DE", "DO", "DAS", "DOS", "E", "DI", "DU"}
NOME = re.compile(rf"(?<![{UP}{LO}])([{UP}][{UP}']+(?:\s+(?:D[AEO]S?\s+|E\s+|DI\s+|DU\s+)?[{UP}][{UP}']+){{1,7}})(?![{UP}{LO}])")
NOME_MISTO = re.compile(rf"\b([{UP}][{LO}]+(?:\s+(?:d[aeo]s?\s+|e\s+)?[{UP}][{LO}]+){{1,6}})\b")
BL = re.compile(r"MINIST|PÚBLICO|PUBLICO|ESTADO|S[ÃA]O PAULO|PROMOTOR|JUSTI|VARA\b|CRIMINAL|COMARCA|CÓDIGO|CODIGO|PENAL|EXCEL|"
                r"BANCO|CAIXA|ECON|FEDERAL|LTDA|WHATSAPP|INSTAGRAM|POL[IÍ]CIA|DELEGACIA|DENUNC|INQU|AUTOS|\bPIX\b|BRADESCO|"
                r"ITA[UÚ]|SANTANDER|NUBANK|MERCADO|PAGSEGURO|PICPAY|FACEBOOK|\bOLX\b|\bRUA\b|AVENIDA|CIDADE|FORO|TRIBUNAL|JUIZ|"
                r"MERIT|SENHOR|DOUTOR|\bART|\bLEI\b|BRASIL|CENTRAL|GAECO|OPERA[ÇC]|SECCIONAL|DISTRITO|CART[ÓO]RIO|AG[ÊE]NCIA|"
                r"\bCONTA|\bCPF\b|\bRG\b|BOLETIM|OCORR|\bFLS\b|PROCESSO|DIGITAL|RECEBIMENTO|\bROL\b|TESTEMUNHA|V[ÍI]TIMA|CONSTA|"
                r"\bFATO|CONCLUS|AUDI[ÊE]NCIA|PEDIDO|EXPOSTO|DEN[ÚU]NCIA|REQUER|QUALIFICA|IMPUTA|ORGANIZA|MODUS|OPERANDI|LAVAGEM|"
                r"ESTELIONATO|INDIVIDUALIZA|CAPITAIS|PAGAMENTOS|DIREITO|EXMO|ASSOCIA|FURTO|ROUBO|RECEPTA|INVAS|DOS FATOS|"
                r"DO CRIME|CRIMES|LIMINAR|PRELIMINAR|RESPOSTA|ACUSA|MEDIDA|CAUTELAR|PRIS|PREVENTIVA|SIGILO|SUBSTITUT|ESTAGI|"
                r"ANALISTA|TELEFONIA|EMPRESA|LOJA|SHOPPING|MAGAZINE|CASAS|BAHIA|AMERICANAS|SHOPEE|AMAZON|CLARO\b|VIVO\b|\bTIM\b|"
                r"\bOI\b|CONSELHO|ESCRIT|MENSAGENS|ORDIN[ÁA]RIO|VEZSES|VEZES|ANOS DE IDADE|RIBEIR[ÃA]|ARARAQUARA|S[ÃA]O CARLOS", re.I)
QUAL = re.compile(r"^.{0,12}(\(?\s*qualificad|\(?\s*qual\. |\(?\s*identificad[oa] (na|nas|a|à) fl|\(?\s*com dados qualificativos|"
                  r"\(?\s*vulgo|,? (brasileir|nascid|portador|RG|CPF|filh[oa] de|natural de|solteir|casad|convivente|desempregad))", re.I)
ASSINA = re.compile(r"Promotor|Promotora|Analista|Estagi|Oficial de Promotoria|Assistente|Procurador", re.I)
FIM_CAP = re.compile(r"\b(Requer|REQUER|Rol\b|ROL\b|testemunhas|TESTEMUNHAS|Pede deferimento|Termos em que|ROL DE)")
ROL = re.compile(r"\bR\s?O\s?L\b|\bRol\b|ROL DE|TESTEMUNHAS:|Testemunhas:")

# Contagem à mão onde a regra erra (revisão das denúncias plurais e das com contagem duvidosa).
N_MANUAL = {
    "CL 1": 2,    # OCR degradado; Lindomar e Jaqueline
    "CL 18": 2,   # Paulo Antonio e Ronaldo
    "CL 25": 9,   # anabolizantes; nove réus (fora da tipologia)
    "FE 27": 2, "FE 126": 2, "FE 76": 2, "FE 81": 2,  # o segundo nome ficou fora da regra
    "FE 79": 1,   # Silvia Aparecida é vítima
    "FE 89": 1, "FE 123": 1, "CL 39": 1, "FE 25": 1, "CL 40": 1, "INV 4": 1,  # ruído de cabeçalho ou de rodapé
    "CL 8": 1, "CL 23": 1, "FE 71": 1, "FE 99": 1,  # nome em caixa mista ou fora do padrão
    "INV 2": 7,   # sete na capitulação; os demais nomes qualificados não foram denunciados
    "INV 36": 9,  # GAECO; contagem da capitulação, com ruído de OCR
    "CL 56": 7,   # JONNATHAS e "ONNATHAS" (o "J" colado à vírgula) são a mesma pessoa
}

# Leitura do assistente nas denúncias com dois ou mais denunciados ou com 288 ou Lei 12.850:
# (divisão de papéis entre os denunciados, coordenação, vínculo entre denunciados, reiteração, nota).
# divisão: "contas" (todos são titulares que recebem, em paralelo ou em cadeia), "execução
# conjunta" (fazem juntos o mesmo ato), "complementar" (ao menos dois papéis distintos entre
# captação ou execução, conta, saque ou recolha, insumo, recrutamento ou coordenação), "nó único"
# (um denunciado com 288 ou Lei 12.850), "indeterminada". coordenação: "denunciado" (a denúncia
# atribui a um denunciado organizar, recrutar ou dirigir), "terceiro" (atribui a pessoa não
# denunciada), "não narrada". vínculo: parentesco, conjugal, trabalho, amizade, ou "" (não narrado).
ESTRUTURA = {
    "CL 1": ("complementar", "não narrada", "", False, "um rende a vítima no caixa, a corré fornece a conta e saca"),
    "CL 53": ("complementar", "não narrada", "conjugal", True, "auxiliar administrativa autoriza pagamentos ao companheiro e a terceira titular; 2015-2016, mais de 25 vezes"),
    "CL 25": ("complementar", "denunciado", "", True, "anabolizantes; mentor e braço direito; fora da tipologia"),
    "INV 8": ("execução conjunta", "não narrada", "trabalho", False, "ex-prestadores de TI da vítima"),
    "CL 57": ("contas", "não narrada", "", False, ""),
    "FE 76": ("contas", "não narrada", "", False, ""),
    "FE 53": ("contas", "não narrada", "", False, "depósito na conta de um e repasses aos demais"),
    "FE 44": ("contas", "não narrada", "", False, ""),
    "INV 2": ("complementar", "denunciado", "conjugal", True, "SIM swap com operadores de telefonia; 'atribuições e hierarquia definidas'; namorada e esposa"),
    "CL 14": ("contas", "não narrada", "", False, ""),
    "FE 107": ("complementar", "denunciado", "", False, "um organiza e recruta, dois cedem contas"),
    "CL 45": ("contas", "não narrada", "", False, ""),
    "INV 13": ("complementar", "não narrada", "", False, "receptação e acesso ao WhatsApp; conta de um"),
    "CL 49": ("contas", "não narrada", "", False, ""),
    "INV 28": ("complementar", "não narrada", "", False, "roubo armado e entrega do celular ao invasor; 288"),
    "FE 60": ("contas", "não narrada", "", False, "a titular recebe, saca e repassa ao corréu"),
    "INV 36": ("complementar", "denunciado", "conjugal|parentesco", True, "GAECO; empresária, marido e filho; digitadores cooptados; organização criminosa"),
    "FE 108": ("complementar", "não narrada", "", False, "um cede a conta, a outra é titular da linha"),
    "FE 1": ("complementar", "não narrada", "conjugal", False, "a denunciada negocia, o companheiro é titular da conta"),
    "CL 42": ("contas", "terceiro", "", True, "quatro contas; linha habilitada com dados de terceiro; dois fatos"),
    "CL 15": ("complementar", "terceiro", "", True, "'Lobo', líder não denunciado; dois denunciados cooptam e administram, os demais fornecem contas e sacam; quinze vezes"),
    "FE 8": ("contas", "não narrada", "", False, ""),
    "FE 84": ("execução conjunta", "não narrada", "", False, "dupla que recolhe os cartões com maquininhas"),
    "FE 51": ("contas", "não narrada", "", False, ""),
    "FE 52": ("nó único", "não narrada", "", False, "falsa policial com sete maquininhas; 288 com não identificados"),
    "CL 58": ("contas", "não narrada", "", False, ""),
    "FE 127": ("complementar", "não narrada", "", False, "terceira recebe a taxa e repassa ao denunciado"),
    "CL 43": ("contas", "não narrada", "", False, ""),
    "FE 87": ("complementar", "não narrada", "", False, "um negocia, o outro saca da conta da irmã"),
    "FE 61": ("complementar", "não narrada", "", False, "um habilita a linha, o outro abre a conta"),
    "FE 91": ("complementar", "não narrada", "conjugal", False, "empresta a conta ao companheiro preso"),
    "CL 10": ("contas", "terceiro", "", False, "comparsas burlam a segurança do banco"),
    "CL 16": ("contas", "não narrada", "", False, ""),
    "INV 32": ("complementar", "denunciado", "parentesco", True, "a prima orienta os repasses; 'já há alguns meses'"),
    "FE 24": ("complementar", "denunciado", "", True, "um entrega os cartões, o outro, 'consultor', capta contas para golpes"),
    "INV 11": ("nó único", "terceiro", "", True, "integra organização de pelo menos quinze não identificados"),
    "FE 19": ("complementar", "não narrada", "", False, "passa-se por funcionário, recebe e repassa ao corréu"),
    "FE 66": ("contas", "não narrada", "", False, "os dois tidos como anunciantes"),
    "CL 52": ("contas", "não narrada", "", False, "seis titulares, oito transferências"),
    "INV 24": ("execução conjunta", "não narrada", "", False, "roubo armado com corrupção de menor"),
    "FE 100": ("contas", "não narrada", "", False, ""),
    "FE 55": ("complementar", "denunciado", "parentesco", False, "Carlos recruta, divide as tarefas e engana a vítima; Álvaro arregimenta a conta da prima Carmelia por R$ 50"),
    "FE 105": ("complementar", "não narrada", "", True, "dois executam e o terceiro fornece a conta; os mesmos do CL 56"),
    "INV 42": ("indeterminada", "não narrada", "", False, ""),
    "CL 33": ("contas", "não narrada", "parentesco", False, "conta da mãe, que repassa ao filho"),
    "CL 56": ("complementar", "não narrada", "", True, "dois executam e os demais fornecem contas; associação; os mesmos do FE 105"),
    "FE 88": ("contas", "terceiro", "", False, "repassam e retêm 10%"),
    "FE 81": ("complementar", "não narrada", "", False, "furto do carro e conta do resgate"),
    "CL 13": ("contas", "não narrada", "", False, ""),
    "FE 21": ("contas", "não narrada", "", False, "a conta de um repassa ao outro"),
    "CL 47": ("contas", "não narrada", "", False, ""),
    "CL 19": ("contas", "terceiro", "", False, "pessoa não denunciada veicula o anúncio; os três cedem contas"),
    "INV 21": ("nó único", "não narrada", "", True, "vende consultas a criminosos; 288"),
    "FE 125": ("complementar", "não narrada", "", False, "receptação e anúncio do carro; conta da corré, apresentada à vítima como mãe"),
    "CL 41": ("complementar", "não narrada", "", False, "contas de dois; a terceira saca e entrega a quem divide"),
    "FE 54": ("nó único", "não narrada", "", False, "recebe os cartões do motoboy; 288 com não identificados"),
    "FE 45": ("contas", "terceiro", "", False, "uma converte em bitcoin para 'Max' por 5%"),
    "FE 97": ("complementar", "denunciado", "trabalho", True, "a colega de trabalho pede, o outro retira os cartões; 'não foi a primeira vez'"),
    "FE 23": ("complementar", "não narrada", "", False, "uma vende, o outro recebe e repassa"),
    "FE 27": ("complementar", "não narrada", "", False, "um abre a conta, o outro a administra"),
    "FE 126": ("complementar", "não narrada", "", False, "um empresta a conta, o outro a usa"),
    "CL 18": ("contas", "não narrada", "", False, "roubo com cativeiro feito por terceiros; Pix para os dois"),
    "CL 11": ("complementar", "não narrada", "", False, "um executa, o outro fornece a conta"),
    "FE 29": ("execução conjunta", "não narrada", "", True, "falsos feirantes itinerantes"),
    "FE 31": ("execução conjunta", "não narrada", "", True, "oito flagrados com notebooks; lojas falsas no Mercado Livre"),
    "FE 6": ("execução conjunta", "não narrada", "", False, ""),
    "FE 17": ("complementar", "não narrada", "", True, "compras com cartões de terceiros e retirada na loja; 170 câmeras"),
    "CL 29": ("complementar", "não narrada", "", False, "uma aborda, o outro fornece a máquina e recebe"),
    "FE 102": ("complementar", "denunciado", "parentesco", True, "João Lucas coordena as compras com dados de terceiros; a sobrinha e outro denunciado; 'estável e permanente'"),
    "CL 7": ("complementar", "não narrada", "", False, "dois cedem contas, um recebe o saque em mãos"),
}

# Desfecho, na sentença, da imputação de associação ou organização criminosa (leitura do
# dispositivo; INV 2, FE 31 pelo DJEN; FE 54 e INV 11 pela leitura da matriz).
SENTENCA_ORG = {
    "INV 28": ("absolvição", "os três absolvidos do 288; dois condenados pelo roubo e pela extorsão"),
    "CL 15": ("condenação", "quatro dos seis condenados no 155 §4º-B c.c. 288"),
    "FE 52": ("condenação", "288 e 171 §2º-A tentado"),
    "INV 32": ("condenação", "dois condenados no 171 caput e no 288; absolvidos do 154-A"),
    "CL 56": ("condenação", "288 e 171 §2º-A e §4º para os que executaram"),
    "INV 21": ("condenação", "154-A tentado e 288"),
    "FE 54": ("absolvição", "absolvido do 288 a pedido do MP nas alegações finais"),
    "FE 97": ("absolvição", "a ré absolvida do 288 (386, V) e o corréu de tudo (386, VII)"),
    "FE 31": ("condenação", "oito condenados no 171 §2º-A tentado e no 288 (DJEN)"),
    "FE 102": ("absolvição", "os três absolvidos do 288 (386, VII)"),
    "INV 2": ("condenação", "três rés condenadas por organização criminosa e lavagem (DJEN); uma absolvida em parte"),
    "INV 36": ("indeterminado", "texto cortado antes do dispositivo; movimento de procedência em parte"),
    "INV 11": ("absolvição", "condenação só no 154-A §§3º e 4º"),
    "CL 25": ("condenação", "art. 2º da Lei 12.850 para parte dos réus; fora da tipologia"),
}

# Leitura à mão do número de denunciados nas 29 denúncias da matriz.
REF_N = {"FE 35": 1, "CL 42": 4, "FE 107": 3, "FE 55": 3, "FE 24": 2, "CL 41": 3, "FE 122": 1, "FE 52": 1, "FE 65": 1,
         "FE 39": 1, "FE 54": 1, "FE 79": 1, "FE 84": 2, "CL 1": 2, "CL 11": 2, "CL 18": 2, "CL 7": 3, "INV 39": 1,
         "INV 20": 1, "FE 50": 1, "INV 14": 1, "INV 30": 1, "INV 11": 1, "INV 21": 1, "CL 56": 7, "FE 105": 3,
         "FE 115": 1, "FE 77": 1, "FE 96": 1}


def _sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def _limpa(n):
    return re.sub(r"\s+", " ", n).strip(" ,.;:")


def corpo(texto):
    """Texto integral da denúncia até o rol."""
    t = re.sub(r"\s+", " ", texto)
    m = ROL.search(t, 400)
    return t[: m.start()] if m else t


def nomes(cap, texto):
    cap = re.sub(r"\s+", " ", cap)
    m = FIM_CAP.search(cap)
    cap = cap[: m.start()] if m else cap[:1500]
    cand = []
    for m in NOME.finditer(cap):
        n = _limpa(m.group(1))
        if len(n.split()) >= 2 and not BL.search(n) and not ASSINA.search(cap[m.end(): m.end() + 30]):
            cand.append(n)
    for m in NOME.finditer(texto):
        n = _limpa(m.group(1))
        depois = texto[m.end(): m.end() + 60]
        if len(n.split()) >= 2 and not BL.search(n) and QUAL.search(depois) and not ASSINA.search(depois[:30]):
            cand.append(n)
    if not cand:
        m = re.search(r"denunci\w*(?: a Vossa Excel[êe]ncia)?,? (.{0,400}?)(?:,)? com[oa] incurs", cap)
        if m:
            cand += [_limpa(x.group(1)).upper() for x in NOME_MISTO.finditer(m.group(1)) if not BL.search(x.group(1))]
    toks = lambda n: [t for t in re.sub(r"[^\w\s]", "", n).split() if t.upper() not in PART]
    cand = [n for n in cand if len([t for t in toks(n) if len(t) >= 3]) >= 2]
    u = list(dict.fromkeys(cand))
    u = [a for a in u if not any(b != a and set(toks(a)) < set(toks(b)) for b in u)]
    vistos, out = set(), []
    for n in u:
        t = [_sem_acento(x.upper()) for x in toks(n)]
        k = (t[0][:4], t[-1][:4])
        if k not in vistos:
            vistos.add(k)
            out.append(n)
    return out


def segmento(numero):
    return json.load(open(os.path.join(EXT, "segmentos", f"{numero}.json"), encoding="utf-8"))


CONCURSO = re.compile(r"previamente ajustad|unidade de des[íi]gnios?|identidade de des[íi]gnios?|concurso (de agentes|de pessoas|com|e )|"
                      r"em conluio|comparsa|coautor|terceir\w+ (ainda )?n[ãa]o identif ?icad|indiv[íi]duos? (ainda )?n[ãa]o identif ?icad|"
                      r"pessoas? (ainda )?n[ãa]o identif ?icad|desconhecid|concorreu (com|para)", re.I)


def enquadramento(cap, narr):
    cap = re.sub(r"\s+", " ", cap)
    if re.search(r"12\.?850|organiza[çc][ãa]o criminosa", cap, re.I):
        return "organização criminosa"
    if re.search(r"\b288\b", cap):
        return "associação criminosa"
    if re.search(r"art(igo|\.)?s?\s*29\b|c\.?\s?c\.?\s*(o )?(art\.?|artigo)?\s*29\b|\be 29\b", cap, re.I) or CONCURSO.search(narr):
        return "concurso de pessoas"
    return "autoria singular"


# Quem pediu a conta ao titular, segundo a narrativa (a versão do titular no inquérito, quase sempre).
RE_PEDIU = re.compile(r"(emprest|ced|vend|alug|forneceu|disponibiliz)\w*\s+(a |sua |a sua |essa |esta |referida )?conta"
                      r"(?: banc[áa]ria| corrente| digital| da [\w ]{2,20}?| do [\w ]{2,20}?)?,?\s+(?:para|a pedido d[eoa]|ao|à|a)\s+"
                      r"(?:um |uma |seu |sua |o |a |pessoa |seu ex-|sua ex-)?(?:conhecid[oa] |amig[oa] )?(?:de )?(?:prenome |vulgo |chamad[oa] )?"
                      r"(?P<q>amig\w*|vizinh\w*|conhecid\w*|colega\w*|prim[oa]|irm[ãa]o?|t[ií][oa]|pai|m[ãa]e|filh[oa]|sobrinh[oa]|"
                      r"cunhad[oa]|namorad[oa]|ex-namorad[oa]|companheir[oa]|marido|esposa|agiota|desconhecid[oa]|terceir[oa]|homem|"
                      r"mulher|rapaz|indiv[íi]duo|menor|[“\"][^”\"]{2,20}[”\"]|[A-ZÁÉÍÓÚÂÊÔ][a-zà-ü]{2,}|[A-ZÁÉÍÓÚÂÊÔ]{3,})")
TIPO_PEDIU = [("parentesco", r"^(prim|irm|t[ií]|pai|m[ãa]e|filh|sobrinh|cunhad)"),
              ("conjugal", r"^(namorad|ex-namorad|companheir|marido|esposa)"),
              ("amizade ou vizinhança", r"^(amig|vizinh|conhecid|colega)"),
              ("credor", r"^agiota"),
              ("desconhecido", r"^(desconhecid|terceir|homem|mulher|rapaz|indiv|menor)"),
              ("pessoa nomeada", r".")]
# Remuneração do titular pela conta narrada como parte ou paga (FE 55, R$ 50; FE 35, 10%; FE 24, 10 a 30%).
RE_PAGA = re.compile(r"prometendo a (ela|ele) R\$|como pagamento|em troca d[ea] (R\$|pagamento|dinheiro|valor)|"
                     r"rec(ebia|eberia|ebeu) (de )?\d+ ?(a \d+ ?)?%|\d+ ?(a \d+ ?)?% (dos|do) valor|dez por cento|"
                     r"ret(endo|iveram|inham|êm|em|ém) \d+ ?%|por ter emprestado|pela cess[ãa]o da conta|"
                     r"R\$ ?[\d.,]+ (?:\([^)]*\) )?(pela|por) (cess|empr[ée]stimo da conta|uso da conta|utiliza)", re.I)


def pedido_conta(narr):
    m = RE_PEDIU.search(narr)
    tipo = ""
    if m:
        q = m.group("q")
        for t, rx in TIPO_PEDIU:
            if re.search(rx, q, re.I):
                tipo = t
                break
    return tipo, bool(RE_PAGA.search(narr)), (narr[max(0, m.start() - 80): m.end() + 60] if m else "")


def le(caso, numero):
    seg = segmento(numero)
    cap = seg["capitulacao"]
    narr = re.sub(r"\s+", " ", seg["narrativa"])
    ns = nomes(cap, corpo(texto_denuncia(numero)))
    n = N_MANUAL.get(caso, len(ns))
    pedido, paga, trecho = pedido_conta(narr)
    return dict(n_denunciados=n, n_regra=len(ns), nomes="; ".join(ns), enquadramento=enquadramento(cap, narr),
                pedido_conta=pedido, pagamento_conta=paga, trecho_pedido=trecho)


def valida():
    den = {f'{r["estrato"]} {r["ordem"]}': r for r in csv.DictReader(open(os.path.join(EXT, "denuncias_tjsp.csv"), encoding="utf-8"))}
    ok_regra = ok_final = 0
    for caso, ref in REF_N.items():
        x = le(caso, den[caso]["numero"])
        ok_regra += x["n_regra"] == ref
        ok_final += x["n_denunciados"] == ref
        if x["n_regra"] != ref:
            print(f"{caso:7} regra {x['n_regra']} | final {x['n_denunciados']} | à mão {ref} | {x['nomes'][:90]}")
    print(f"número de denunciados em {len(REF_N)}: regra {ok_regra}, com N_MANUAL {ok_final}")


if __name__ == "__main__":
    if sys.argv[1:2] == ["valida"]:
        valida()
    elif sys.argv[1:2] == ["caso"]:
        caso = " ".join(sys.argv[2:4])
        den = {f'{r["estrato"]} {r["ordem"]}': r for r in csv.DictReader(open(os.path.join(EXT, "denuncias_tjsp.csv"), encoding="utf-8"))}
        print(json.dumps({**le(caso, den[caso]["numero"]), "estrutura": ESTRUTURA.get(caso)}, ensure_ascii=False, indent=1))
