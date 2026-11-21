#!/usr/bin/env python3
"""Extração por regras das denúncias: TJSP (fase 1, padrão) e TJPA (fase 2).

Uso, da raiz do repositório:
    python3 scripts/extrai_denuncias.py          # TJSP, reprodução da fase 1
    python3 scripts/extrai_denuncias.py tjpa     # TJPA

TJSP. Entrada: textos/tjsp/denuncias/<numero>/NN_<id>.txt, dados/codex/status.csv e
dados/cjpg/amostra_tjsp.csv. Saída:
  dados/extracao/denuncias_tjsp.csv  (uma linha por processo, campos codificados)
  dados/extracao/segmentos/<numero>.json  (cota, narrativa e capitulação em texto)
TJPA. Entrada: textos/tjpa/denuncias/, dados/codex_tjpa/status.csv, dados/djen/alvos_djen_tjpa.csv
e dados/codex_tjpa/fila.csv. Saída: dados/extracao/denuncias_tjpa.csv e segmentos_tjpa/.

Decisões:
- A peça é a soma das partes na ordem gravada; o cabeçalho "[Texto nativo do PJe]" e as
  quebras de linha somem, porque o PJe parte o texto em linhas de diagramação.
- A cota (manifestação que acompanha a denúncia) é o trecho anterior ao endereçamento ao
  juízo ("EXCELENTÍSSIMO") quando esse endereçamento não abre o texto. Algumas peças vêm
  sem cota; outras trazem a cota depois da denúncia; o campo fica vazio nesse caso.
- Um segundo endereçamento seguido de número de autos diferente do processo indica peça
  de outro processo anexada (caso da ordem FE 105); o texto é cortado ali.
- A capitulação é a janela que começa no verbo "denuncio" (ou "incurso", na falta dele) e
  vai até 900 caracteres; os artigos são lidos só nessa janela, para não contar artigos
  citados na cota (art. 28-A do CPP, art. 89 da Lei 9.099) ou na narrativa.
- A narrativa vai do primeiro "Consta"/"Segundo"/"Relata"/"Apurou-se" (ou do fim do
  endereçamento) até o início da capitulação.
- Tudo é heurística; a coluna `alerta` marca o que precisa de leitura humana.

Uma regra só, dois tribunais. As regras da fase 1 valem para os dois, e o TJSP roda
exatamente como antes (a saída é idêntica byte a byte). O TJPA liga a camada `mppa`,
porque as denúncias do MPPA seguem outro molde: endereçamento abreviado ("EXMO. SR."),
seção "DOS FATOS" depois de uma qualificação longa, capitulação em seção própria ("DO
DIREITO", "TIPIFICAÇÃO", "DA IMPUTAÇÃO PENAL") com verbo de imputação ("praticou o
crime descrito no", "infringiu", "violou as disposições", "incorreu"), transcrição do
tipo penal logo depois do artigo, ANPP tratado no corpo da denúncia e OCR que troca o
"§" por "8" ou "$". A camada só age onde a regra da fase 1 não acha nada (âncora de
segundo nível) ou onde o molde do MPPA a contradiz (corte da transcrição e do pedido,
início da narrativa na seção dos fatos, cota no corpo), e está descrita em
`dados/extracao/LEIAME.md`, seção "Extração das denúncias do TJPA".
"""
import csv, glob, hashlib, json, os, re, sys, unicodedata

BASE = "textos/tjsp/denuncias"
OUT = "dados/extracao"
TRUNCADOS = set()  # 1503431-80.2021 foi relido pela cópia de 2025 (OCR), completa
# correções conferidas em outra peça do processo; valem sobre o parser
CORRECOES = {
    "1521208-63.2020.8.26.0228": ({"154A": True}, "capitulação diz 155-A; a sentença de 22/09/2022 lê 154-A e §2º"),
}
CNJ = r"\d{7}-\d{2}\.\d{4}\.8\.26\.\d{4}"

# TJPA: correções conferidas na peça; mesmo formato do TJSP
CORRECOES_TJPA = {
    "0046698-39.2015.8.14.0401": ({"171_2A": False, "171_caput": True},
                                  "aditamento de 03/11/2025 (parte 2) recapitula para o art. 171, caput, por fato anterior à Lei 14.155/2021; recebido em 14/05/2026"),
    "0809824-96.2022.8.14.0006": ({"155_4B": True},
                                  "o cabeçalho capitula o art. 155, §4º-B, e o corpo o §4º, II; a sentença lê o §4º-B"),
    "0000323-67.2021.8.14.0401": ({}, "aditamento de 01/04/2022 (parte 2) retira o art. 2º da Lei 12.850/13, rejeitado pela Vara de Combate ao Crime Organizado, e mantém o art. 1º, §1º, II, da Lei 9.613/98"),
    "0000533-21.2021.8.14.0401": ({}, "ratificação de 06/07/2022 (parte 2) mantém a denúncia sem o art. 2º da Lei 12.850/13, rejeitado pela Vara de Combate ao Crime Organizado"),
    "0000352-20.2021.8.14.0401": ({}, "a parte 1 (doc 014 da Operação Trojan, lavagem e Lei 12.850) foi substituída pela denúncia da 5ª PJ de 18/07/2022 (parte 2, art. 155, §4º, II, e art. 288), que é a julgada; só a parte 2 entra"),
    "0811772-81.2024.8.14.0401": ({}, "âncora manual: a automática caía no art. 2º da Lei 12.850 citado na narrativa; a capitulação por denunciado está no pedido"),
}
# partes gravadas junto com a denúncia que não são denúncia: saem do texto e vão para a cota
PARTES_COTA_TJPA = {
    "0825320-42.2025.8.14.0401": [3],  # manifestação do MP sobre a preventiva, no mesmo protocolo
}
# família de desmembramento que a deduplicação por texto não pega (aditamento só num membro)
DUPLICATA_MANUAL_TJPA = {
    "0817567-05.2023.8.14.0401": "0820198-53.2022.8.14.0401",  # 10ª Vara, IPL 592; aditamento de 17/10/2023 só neste
}
# partes gravadas que não valem como denúncia do processo (peça substituída por outra)
EXCLUI_PARTES_TJPA = {
    "0000352-20.2021.8.14.0401": [1],
}
# trecho literal que abre a capitulação, quando a âncora automática cai em outro lugar
ANCORA_MANUAL_TJPA = {
    "0811772-81.2024.8.14.0401": "CONDENAÇÃO dos réus: 1. FLÁVIO",
}
# denúncias distintas (réus e capitulação próprios) de uma mesma operação; contam cada uma,
# mas a análise precisa saber que vêm da mesma investigação
OPERACAO_TJPA = {
    **{n: "Trojan" for n in ("0000323-67.2021.8.14.0401", "0000352-20.2021.8.14.0401", "0000410-23.2021.8.14.0401",
                            "0000533-21.2021.8.14.0401", "0000548-87.2021.8.14.0401", "0000586-02.2021.8.14.0401",
                            "0000666-63.2021.8.14.0401")},
    **{n: "Arremate" for n in ("0803124-27.2024.8.14.0009", "0803125-12.2024.8.14.0009", "0803127-79.2024.8.14.0009")},
}

TRIBUNAIS = {
    "tjsp": {"base": "textos/tjsp/denuncias", "cnj": CNJ, "status": "dados/codex/status.csv",
             "saida": "denuncias_tjsp.csv", "segmentos": "segmentos", "correcoes": CORRECOES,
             "mppa": False},
    "tjpa": {"base": "textos/tjpa/denuncias", "cnj": r"\d{7}-\d{2}\.\d{4}\.8\.14\.\d{4}",
             "status": "dados/codex_tjpa/status.csv", "saida": "denuncias_tjpa.csv",
             "segmentos": "segmentos_tjpa", "correcoes": CORRECOES_TJPA, "mppa": True},
}


def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def le_partes(numero, base=None, so=None, exceto=()):
    """Texto das partes gravadas, na ordem; `so` e `exceto` filtram pelo número da parte (NN_)."""
    partes = []
    for f in sorted(glob.glob(f"{base or BASE}/{numero}/*.txt")):
        nn = int(os.path.basename(f)[:2])
        if (so is not None and nn not in so) or nn in exceto:
            continue
        t = open(f, encoding="utf-8").read()
        t = re.sub(r"\[Texto nativo do PJe\]|\[OCR[^\]]*\]", " ", t)
        partes.append(t)
    return partes


def carrega(numero, base=None, cnj=None, exceto=()):
    CNJ = cnj or globals()["CNJ"]
    partes = le_partes(numero, base, exceto=exceto)
    t = re.sub(r"\s+", " ", " ".join(partes)).strip()
    # rodapé de conferência do e-SAJ e carimbo do STJ, repetidos em cada página das cópias
    # digitalizadas; partem a capitulação ao meio quando ela cruza a página
    t = re.sub(r"Este documento é cópia do original, assinado digitalmente.{0,500}?fls\.\s*\d+", " ", t)
    t = re.sub(r"\(e-STJ Fl\.\s*\d+\)|Documento recebido eletronicamente da origem", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    # corte de peça de outro processo anexada
    # o número dos autos citado na abertura da peça vale como próprio: processos redistribuídos
    # ou renumerados trazem a denúncia com o número de origem (ex.: INV 3)
    proprios = {numero, *re.findall(CNJ, t[:2000])}
    for m in re.finditer(r"EXCELENT[ÍI]SSIM", t):
        if m.start() < 2000:
            continue
        janela = t[m.start(): m.start() + 600]
        outros = [n for n in re.findall(CNJ, janela) if n not in proprios]
        if outros and not proprios & set(re.findall(CNJ, janela)):
            return t[: m.start()].strip(), True
    return t, False


RX_ENDERECO = re.compile(r"EXCELENT[ÍI]SSIM[OA]S?\s*\(?A?\)?\s*SENHOR", re.I)
RX_INICIO_NARR = re.compile(
    r"\b(Consta|Segundo (?:se )?apur|Relata|Apurou-se|Narram|Noticiam|Conforme apurado|"
    r"Restou apurado|Depreende-se|Infere-se|Extrai-se|Segundo consta|Segundo restou|Consoante)", re.I)
RX_DENUNCIO = re.compile(r"\b(denuncio|denunciamos|denuncia(?:-se)?\s+(?:a|o)s?\s+(?:Vossa|V\.)|"
                         r"oferece(?:-se)?\s+den[úu]ncia\s+(?:contra|em face)|DENUNCI[OA])\b", re.I)
RX_ANCORA = re.compile(r"\bdenunci(?:o|amos|a-se|a|am)\b|oferec\w*(?:-se)?\s+(?:a\s+presente\s+)?den[úu]ncia|oferecida\s+a\s+presente\s+den[úu]ncia|\bincidi(?:u|ram)\b|\bincorre(?:u|ram)\b", re.I)
RX_ART_CRIME = re.compile(r"(art\.?|artigos?)\s*\d{1,3}|154\s*[-–]?\s*A\b|Lei\s*(n\.?\s*[º°o]?\s*)?\d{1,2}\.\d{3}", re.I)
RX_IMPUTA = re.compile(r"infra[çc]|viola[çc]|incurs|pr[áa]tica|tipificad|como autor|san[çc][õo]es|dispost", re.I)
RX_FIM_CAP = re.compile(r"\b(Requeiro|Requer-se|Requer|Requeremos|requeiro|requerendo|requer-se|ROL\b|Rol\b|Termos em que|Para tanto, requer)")
RX_INCURSO = re.compile(r"\bincurs[oa]s?\b|\bcomo (?:autor|autores|incurso)", re.I)
RX_FECHO = re.compile(r"[Aa]nte o exposto|[Dd]iante do exposto|[Ii]sto posto|[Pp]osto isso|[Pp]osto isto|[Ii]sso posto|"
                      r"[Dd]iante disso|[Aa]ssim agindo|[Aa]ssim procedendo|[Ee]m face do exposto|"
                      r"[Pp]elo exposto|ESTANDO")


# Camada MPPA (TJPA). Só entra com mppa=True; o TJSP não passa por nada daqui.
# endereçamento abreviado
RX_ENDERECO_MPPA = re.compile(r"\bEXM[OA]S?\b\.?\s*\(?[AO]?\)?\.?\s*S(?:R|ENHOR)|EXCELENT[ÍI]SSIM\s?[OA]", re.I)
# o que distingue uma cota de verdade do cabeçalho, carimbo de protocolo ou capa de migração
RX_MANIFESTA = re.compile(r"28-A|n[ãa]o persecu|\bANPP\b|\brequer|dilig[êe]ncia|Merit[íi]ssim|\bMM[ªa]?\.?\s*Ju|preventiva|\bcota\b", re.I)
# início da narrativa: a seção dos fatos, que no MPPA vem depois de uma qualificação longa
RX_FATOS_MPPA = re.compile(r"\b(?:\d{1,2}\s*[.)–-]\s*|[IVX]{1,3}\s*[.)–-]\s*)?(?:DOS? FATOS?|D[OA]S? FATOS? E|DA S[ÍI]NTESE F[ÁA]TICA|DA NARRATIVA)\b"
                           r"|\bFATOS?\s+DELITUOSOS?\b|\bCompulsando os autos|\bExtrai-se dos (?:presentes )?autos|\bDOS FATOS\b|\bDo[s]? [Ff]atos?\b")
# marcos de narrativa da fase 1 com fronteira de palavra e inicial maiúscula, isto é, em
# começo de frase ("Consta" não casa com "constante" nem com "conforme consta no relatório")
RX_INICIO_NARR_ESTRITO = re.compile(
    r"\b(?:Consta|Segundo (?:se )?apur\w*|Relata|Apurou-se|Narram|Noticiam|Conforme apurado|"
    r"Restou apurado|Depreende-se|Infere-se|Extrai-se|Segundo consta|Segundo restou|Consoante)\b")
# âncora de segundo nível: verbo ou fórmula de imputação seguida de artigo em até 250 caracteres
RX_ANCORA_MPPA = re.compile(
    r"\bpratic(?:ou|aram)\b|\bcomet(?:eu|eram)\b|\binfring(?:iu|iram|e|em)\b|\binfring[êe]ncia\b|"
    r"\bviol(?:ou|aram)\b|\bincorr(?:e|em|eu|eram|ido|idos|ida)\b(?!\s+nas?\s+mesmas?\s+penas?)|\bincid(?:e|em|iu|iram)\b|\bincurs[oa]s?\b|"
    r"\bcometimento\s+d[oa]s?\s+(?:crimes?|delitos?|il[íi]cit)|"
    r"\btransgredi(?:u|ram)\b|\bperpetr(?:ou|aram)\b|\bconsum(?:ou|aram)\s+os?\s+crimes?\b|"
    r"\bcaracteriza(?:m)?\s+(?:a\s+pr[áa]tica|o\s+crime|os\s+crimes)|\bamolda(?:m)?(?:-se)?\b|\bsubsume(?:m)?-se\b|"
    r"\badequa[çc][ãa]o\s+t[íi]pica\b|\bsujeit[oa]s?\s+[àa]s?\s+(?:reprimendas|san[çc][õo]es|penas)|"
    r"\bpela\s+pr[áa]tica\s+d[oa]s?\s+(?:crimes?|infra[çc]|il[íi]cit|delit|conduta)|"
    r"\b(?:apresenta|ofere[çc]o|oferece)\s+(?:a\s+presente\s+)?den[úu]ncia\b|\bimputa\s*:|"
    r"\bcapitula[çc][ãa]o(?:\s+penal)?(?:\s+provis[óo]ria)?\s*:", re.I)
# âncora fraca: a fórmula descritiva ("dos delitos descritos no art."), que também aparece na
# narrativa; só vence quando não há outra
RX_ANCORA_MPPA_FRACA = re.compile(r"\b(?:delitos?|crimes?|il[íi]citos?)\s+(?:descrit|tipificad|previst|capitulad)[oa]s?\s+n[oa]s?\s+art", re.I)
# seção ou fecho que anuncia a capitulação
RX_SECAO_DIREITO = re.compile(r"DO DIREITO|Do Direito|TIPIFICA[ÇC][ÃA]O|IM\s?PUTA[ÇC][ÃA]O\s+(?:PENAL|T[ÍI]PICA)|DA\s+IM\s?PUTA|"
                              r"CLASSIFICA[ÇC][ÃA]O\s+JUR[ÍI]DICA|ADEQUA[ÇC][ÃA]O\s+T[ÍI]PICA|ENQUADRAMENTO|FUNDAMENTO\s+JUR[ÍI]DICO|"
                              r"CAPITULA[ÇC][ÃA]O\s+T[ÍI]PICA|DA\s+CAPITULA|Assim agindo|Agindo (?:assim|desta forma|desse modo)")
# o artigo citado pela autoridade policial (indiciamento, relatório) não é a capitulação do MP
RX_POLICIA = re.compile(r"indici(?:ou|aram|ar|á-l|amento)|relat[óo]rio\s+(?:final|policial|conclusivo)|autoridade\s+policial|provis[óo]ria", re.I)
RX_PEDIDO = re.compile(r"\brequer|DOS?\s+PEDIDOS?|Do\s+Pedido|PEDIDO\s+DE\s+DILIG|REQUERIMENTO", re.I)
# fim da capitulação no molde do MPPA: seção do pedido, transcrição do tipo penal, seção de prova
RX_FIM_MPPA = re.compile(
    r"\b(?:\d{1,2}\s*[.)–-]\s*|[IVX]{1,3}\s*[.)–-]\s*)?(?:DOS?\s+PEDIDOS?|Do\s+Pedido|DOS\s+REQUERIM|PEDIDO\s+DE\s+DILIG|ROL\s+DE|"
    r"DA\s+MATERIALIDADE|DOS\s+IND[ÍI]CIOS|AUTORIA\s+E\s+MATERIALIDADE|MATERIALIDADE\s+E\s+AUTORIA|DO\s+ACORDO\s+DE\s+N[ÃA]O)\b|"
    r"\b(?:in verbis|nos seguintes termos|vazado nos|redigidos? nos)\b|[“\"]\s*Art\s*\.?\s*\d|"
    r"\bArt\s*\.?\s*\d{3}(?:\s*-\s*[A-Z])?\s*[-–.]?\s*(?:Obter|Subtrair|Constranger|Invadir|Vender|Falsificar|Fazer|Apropriar|Receber|Associarem)\b|"
    r"\brequer(?:-se)?\b|\bTermos em que\b")
RX_ANPP = re.compile(r"28-A|n[ãa]o persecu|\bANPP\b", re.I)
# data de nascimento na qualificação do denunciado, com a data
RX_NASC = re.compile(r"\bnascid[oa]s?\s+(?:em|a|aos|no dia|na data(?:\s+de)?)\s*[\d/.]+(?:\s*de\s+\w+\s+de\s+\d{4})?"
                     r"|\bd\.\s?n\.\s*[\d/.]+|data de nascimento\s*:?\s*[\d/.]+", re.I)


def capitulacao_mppa(corpo):
    """Âncora de segundo nível do MPPA: devolve (âncora, início) ou None.

    Ordem de preferência: fora do contexto policial e depois do início da narrativa; em seção
    ou fecho de capitulação e fora do pedido; a primeira no texto.
    """
    m_f = RX_FATOS_MPPA.search(corpo) or RX_INICIO_NARR.search(corpo)
    ini_fatos = m_f.start() if m_f else 0
    cands = []
    ancoras = [(m, 0) for m in RX_ANCORA_MPPA.finditer(corpo)] + [(m, 1) for m in RX_ANCORA_MPPA_FRACA.finditer(corpo)]
    for m, fraca in ancoras:
        if not RX_ART_CRIME.search(corpo[m.start(): m.start() + 250]):
            continue
        antes = corpo[max(0, m.start() - 300): m.start()]
        policia = bool(RX_POLICIA.search(antes + m.group(0)))
        inicio = m.start() < ini_fatos
        f = list(RX_FECHO.finditer(antes)) + list(RX_SECAO_DIREITO.finditer(antes))
        secao = bool(f)
        pedido = bool(RX_PEDIDO.search(antes[-250:]))
        cap_ini = m.start() - (len(antes) - max(x.start() for x in f)) if f else m.start()
        cands.append((policia + inicio, fraca, (not secao) + pedido, m.start(), cap_ini))
    if not cands:
        return None
    _, _, _, anc, cap_ini = sorted(cands)[0]
    return anc, cap_ini


def fim_capitulacao_mppa(corpo, anc, fim):
    """Corta no primeiro marco de fim depois da âncora que deixe algum artigo antes dele.

    A condição do artigo protege o caso em que o OCR desloca o "denuncia:" para antes do
    título "DOS PEDIDOS FINAIS" (Operação Trojan).
    """
    for rx in (RX_FIM_MPPA, RX_FATOS_MPPA):
        for m in rx.finditer(corpo, anc + 40, fim):
            if RX_ART_CRIME.search(corpo[anc: m.start()]):
                fim = m.start()
                break
    return fim


def segmenta(t, mppa=False, ancora_manual=None):
    """Cota, narrativa e capitulação. `ancora_manual` é um trecho literal do texto que abre a
    capitulação, para os casos conferidos na leitura em que a âncora automática erra."""
    seg = {"cota": "", "narrativa": "", "capitulacao": ""}
    m_end = RX_ENDERECO.search(t)
    if mppa and not m_end:
        m_end = RX_ENDERECO_MPPA.search(t)
    if m_end and m_end.start() > 150:
        # no MPPA o que vem antes do endereçamento quase sempre é cabeçalho, carimbo de
        # protocolo ou capa de migração; só vira cota se tiver cara de manifestação
        if not mppa or RX_MANIFESTA.search(t[: m_end.start()]):
            seg["cota"] = t[: m_end.start()].strip()
    corpo_ini = m_end.start() if m_end else 0
    corpo = t[corpo_ini:]
    # capitulação: âncora "denunci-/denúncia" seguida, em até 600 caracteres, de artigo de tipo
    # penal e de um verbo de imputação; preferir a âncora precedida de fecho ("Ante o exposto").
    cands = []
    for m in RX_ANCORA.finditer(corpo):
        jan = corpo[m.start(): m.start() + 600]
        if RX_ART_CRIME.search(jan) and RX_IMPUTA.search(jan):
            antes = corpo[max(0, m.start() - 400): m.start()]
            f = list(RX_FECHO.finditer(antes))
            ini = m.start() - (len(antes) - f[-1].start()) if f else m.start()
            forte = bool(re.search(r"incurs|infra[çc]|viola[çc]|san[çc][õo]es", jan))
            cands.append(((not f) + (not forte), m.start(), ini))
    if not cands and not mppa:  # último recurso: "incurso" com artigo de tipo penal
        for m in RX_INCURSO.finditer(corpo):
            if RX_ART_CRIME.search(corpo[m.start(): m.start() + 300]):
                cands.append((3, m.start(), m.start()))
    escolha = ""
    if ancora_manual and ancora_manual in corpo:
        anc = cap_ini = corpo.index(ancora_manual)
        escolha = "manual"
    elif cands:
        _, anc, cap_ini = sorted(cands)[0]
        escolha = "regra"
    elif mppa:  # no MPPA o "incurso" entra entre as âncoras de segundo nível
        r = capitulacao_mppa(corpo)
        if r:
            anc, cap_ini = r
            escolha = "mppa"
    cap_fim = None
    if escolha:
        # fim: primeiro pedido processual ("Requeiro", "Requer-se", "Rol") depois de 250
        # caracteres; teto de 6000 para as denúncias com lista de denunciados (GAECO)
        m_fim = RX_FIM_CAP.search(corpo, anc + 250)
        fim = min(m_fim.start() if m_fim else anc + 900, anc + 6000)
        if mppa:  # e, no MPPA, a seção do pedido ou a transcrição do tipo, se vierem antes
            fim = fim_capitulacao_mppa(corpo, anc, fim)
        seg["capitulacao"] = corpo[cap_ini: fim].strip()
        narr_fim, cap_fim = cap_ini, fim
    else:
        narr_fim = len(corpo)
    m_n = RX_INICIO_NARR.search(corpo[:narr_fim])
    # um "Consta" muito adiante costuma ser citação de documento; então a narrativa
    # começa no endereçamento
    narr_ini = m_n.start() if m_n and m_n.start() < 1500 else 0
    if mppa:
        # a seção dos fatos vence: a qualificação do MPPA é longa e traz datas de nascimento,
        # e "Consta" casa com "constante" na qualificação
        m_f = RX_FATOS_MPPA.search(corpo)
        if m_f and m_f.start() < narr_fim:
            narr_ini = m_f.start()
        elif m_f and cap_fim is not None:
            # capitulação no preâmbulo ("pela prática do crime previsto no art. ..."), antes
            # dos fatos: a narrativa vai da seção dos fatos até a seção de direito ou o pedido
            m_d = re.compile(RX_SECAO_DIREITO.pattern + r"|" + RX_PEDIDO.pattern).search(corpo, m_f.start() + 200)
            narr_ini, narr_fim = m_f.start(), (m_d.start() if m_d else len(corpo))
            seg["capitulacao_no_preambulo"] = True
        # sem seção dos fatos, a narrativa ainda pode abrir na qualificação ("com base no que
        # restou apurado ... oferecer DENÚNCIA em face de X, nascido em ..."): começa no primeiro
        # marco de narrativa depois da última data de nascimento, ou logo depois dela
        # A qualificação é a cadeia de datas de nascimento que começa nos primeiros 2.500
        # caracteres da narrativa, cada uma a menos de 1.500 da anterior; uma data de
        # nascimento solta mais adiante é de outra pessoa (titular da conta, vítima).
        q = None
        for m in RX_NASC.finditer(corpo, narr_ini, narr_fim):
            if (q is None and m.start() - narr_ini > 2500) or (q is not None and m.start() - q > 1500):
                break
            q = m.end()
        if q is not None:
            m2 = RX_FATOS_MPPA.search(corpo, q, narr_fim) or RX_INICIO_NARR_ESTRITO.search(corpo, q, narr_fim)
            narr_ini = m2.start() if m2 else q
    seg["narrativa"] = corpo[narr_ini:narr_fim].strip()
    # cota ao fim (quando não veio no início): trecho depois da capitulação com "ANPP"/"28-A"
    if not seg["cota"]:
        resto = corpo[(cap_ini if escolha else len(corpo)) + 900:] if mppa else corpo[narr_fim + 900:]
        if re.search(r"28-A|n[ãa]o persecu", resto, re.I):
            seg["cota"] = resto.strip()[:4000]
    if mppa and not seg["cota"]:
        # o MPPA trata o ANPP no corpo da denúncia, às vezes antes da capitulação
        for m in RX_ANPP.finditer(corpo):
            if cap_fim is not None and cap_ini <= m.start() < cap_fim:
                continue
            seg["cota"] = corpo[max(0, m.start() - 300): m.start() + 1500].strip()
            break
    if mppa:
        seg["ancora"] = escolha
    return seg


MENCAO_ARTIGO = re.compile(r"\b(?:artigos?|arts?)\b")


def do_171(c, m):
    """Diz se o parágrafo casado em m pertence ao art. 171.

    As alternativas soltas das regex do § 2º-A e do § 4º existem para pegar o
    parágrafo separado do artigo por cabeçalho de página. Sozinhas, também pegam
    o § 2º-A do roubo (art. 157) e os §§ 3º e 4º do art. 154-A. A regra: o trecho
    entre a última menção a "artigo" ou "art." e o parágrafo precisa citar o 171,
    o que cobre "artigos 155 e 171, § 2º-A" e o cabeçalho no meio do dispositivo.
    """
    antes = c[:m.start()]
    mencoes = list(MENCAO_ARTIGO.finditer(antes))
    trecho = antes[mencoes[-1].start():] if mencoes else antes
    return bool(re.search(r"\b171\b", trecho))


def normaliza_ocr(c):
    """Grafias de OCR e de digitação vistas nas denúncias do MPPA (texto já sem acento e minúsculo).

    O "§" lido como "8", "$", "$8" ou "&" depois do número do artigo ("171, 82º-A", "171, 8 2º-A",
    "155, 84º"); o § 2º-A sem hífen ("§ 2º A", "§2ºA"); travessão no lugar do hífen; o inciso
    II lido como "Il" e o I como "|"; "c/ c", "clc" e "Art ." com espaço.
    """
    c = c.replace("–", "-").replace("—", "-")
    c = re.sub(r"&\s*(?=\d)", "§ ", c)  # "171, & 2ºA" (0814514-45.2025, sentença)
    c = re.sub(r"\bart\s+\.", "art.", c)
    c = re.sub(r"\bc\s*/\s*c\b|\bc[l1]c\b", "c/c", c)
    c = re.sub(r"(\b(?:171|155|154\s*-?\s*a|157|158|180|288|297|299)\s*,?\s*)(?:\$\s*8|\$|8)\s*(?=\d)", r"\1§ ", c)
    c = re.sub(r"(§\s*o?\s*2\s*o)\s*a\b(?!\s*\d)", r"\1-a", c)
    # "§4.º-B": ponto entre o número e o ordinal
    c = re.sub(r"(§\s*\d)\.\s*(?=o\s*-?\s*[ab]\b)", r"\1", c)
    # cabeçalho de página do MPPA entre "§ 2º-" e o "A"
    c = re.sub(r"(§\s*2\s*o?\s*-)\s*[^§]{0,300}?(?:promotoria|ministerio publico)[^§]{0,200}?\s(a\b)", r"\1\2", c)
    c = re.sub(r"\b(inciso|inc\.)\s*i[l1|]\b", r"\1 ii", c)
    c = re.sub(r"(\b14\s*,\s*)i[l1|]\b", r"\1ii", c)
    c = re.sub(r"\b(inciso|inc\.)\s*\|", r"\1 i", c)
    return c


def artigos(cap, tolerante=False):
    """Lista de dispositivos do Código Penal e leis citados na capitulação.

    `tolerante` aplica antes `normaliza_ocr` (TJPA). O TJSP e o leitor de sentenças da fase 1
    chamam sem ele, e a leitura fica a mesma de antes.
    """
    c = sem_acento(cap).lower()
    c = c.replace("º", "o").replace("°", "o").replace("ª", "a")
    if tolerante:
        c = normaliza_ocr(c)
    f = {}
    f["171"] = bool(re.search(r"\b171\b", c))
    # variantes vistas: "§ 2º-A", "§ 2ª-A", "§2.º-A", "§ 2-Aº", "§ 2º- <cabeçalho de página> A"
    f["171_2A"] = bool(re.search(r"171[^0-9]{0,40}(§|par|paragrafo|\$|p\.)[^0-9]{0,15}2\s*[oa.]*\s*-\s*(endereco:.{0,300}?\s)?ao?\b", c)
                       or any(do_171(c, m) for m in re.finditer(r"\b2\s*[oa.]*\s*-\s*ao?\b", c)))
    f["171_2_VII"] = bool(re.search(r"171[^.;]{0,60}2\s*o?[^-a0-9][^.;]{0,25}\bvii\b", c))
    f["171_4"] = bool(re.search(r"171[^.;]{0,80}(§§?|par)[^.;]{0,30}\b4\s*o?\b|\b4\s*o?\s*\(?\s*(idos|vitima idos)", c)
                      or any(do_171(c, m) for m in re.finditer(r"e\s*(§\s*)?4\s*o?\s*,?\s*(do|ambos|todos|,|\()", c)))
    f["171_caput"] = bool(re.search(r"171\s*,?\s*(\"|“)?caput", c)) and not f["171_2A"]
    f["154A"] = bool(re.search(r"154\s*[-–]?\s*a\b", c))
    f["155"] = bool(re.search(r"\b155\b", c))
    f["155_4B"] = bool(re.search(r"155[^.;]{0,90}4\s*o?\s*-?\s*b\b", c))
    f["180"] = bool(re.search(r"\b180\b", c))
    f["147"] = bool(re.search(r"\b147\b", c))
    f["313A"] = bool(re.search(r"313\s*-\s*a", c))
    f["drogas"] = bool(re.search(r"11\.?343", c))
    f["158"] = bool(re.search(r"\b158\b", c))
    f["288"] = bool(re.search(r"\b288\b", c))
    f["307"] = bool(re.search(r"\b307\b", c))
    f["298_299"] = bool(re.search(r"\b29[789]\b", c))
    f["lavagem"] = bool(re.search(r"9\.?613|lavagem", c))
    f["art_29"] = bool(re.search(r"\b(artigo|art\.?)\s*29\b|c\.?\s*c\.?\s*(o\s*)?(artigo|art\.?)?\s*29\b|na forma do (artigo|art\.?) 29", c))
    f["art_69"] = bool(re.search(r"\b(artigo|art\.?)\s*69\b|concurso material", c))
    f["art_70"] = bool(re.search(r"\b(artigo|art\.?)\s*70\b|concurso formal", c))
    f["art_71"] = bool(re.search(r"\b(artigo|art\.?)\s*71\b|continuidade delitiva|crime continuado", c))
    f["tentativa"] = bool(re.search(r"14\s*,?\s*(inciso\s*)?ii\b|tentad", c))
    f["vezes"] = bool(re.search(r"por (duas|tres|quatro|cinco|seis|sete|oito|nove|dez|\d+|diversas|varias) vezes", c))
    return f


MEIOS = {
    "whatsapp": r"whats\s?app|zap\b",
    "instagram": r"instagram",
    "facebook": r"facebook|marketplace",
    "olx_site_venda": r"\bolx\b|mercado livre|webmotors|an[úu]ncio|site de vendas|loja virtual",
    "telefone": r"liga[çc][ãa]o|telefonema|contato telef[ôo]nico|telefonou|ligou para",
    "sms_email": r"\bsms\b|e-mail|correio eletr[ôo]nico|mensagem de texto",
    "pix": r"\bpix\b",
    "boleto": r"boleto",
    "transferencia_ted": r"transfer[êe]ncia|\bted\b|dep[óo]sito",
    "cartao": r"cart[ãa]o de cr[ée]dito|cart[ãa]o banc|cart[ãa]o de d[ée]bito",
    "link_phishing": r"\blink\b|phishing|site falso|p[áa]gina falsa",
    "acesso_remoto_app": r"acesso remoto|anydesk|teamviewer|malware|instal\w+ (de )?(um |o )?(aplicativo|programa|app)|aplicativo (de acesso|malicioso|falso)",
    "emprestimo_consignado": r"empr[ée]stimo|consignad",
    "falso_parente": r"(passando-se|se passando|se passou|se passar|fazendo-se passar|se fez passar|identific\w*-se como|se identific\w* como|apresent\w*-se como|se apresent\w* como|dissimul\w* ser|fing\w* ser|supostamente enviad\w* por|perfil[^.]{0,30}(foto|nome))[^.]{0,45}(filh|net[oa]|sobrinh|irm[ãa]|m[ãa]e\b|pai\b|parente|prim[oa]|tia\b|tio\b|genro|nora|afilhad|cunhad|sogr)|foto(grafia)? d[oa] (seu |sua )?(filh|net|sobrinh|irm)|(troc|mud)\w* (de |o |seu )?(n[úu]mero|numeral|celular|telefone)",
    "falsa_central": r"falsa central|central de atendimento|funcion[áa]ri[oa] d[oa] banco|setor de seguran[çc]a|central de seguran[çc]a|(passando-se|se passando|identific\w*-se) (como |por )?(representante|atendente|funcion[áa]ri)|em nome d[ao] (bv|banco|financeira|institui[çc][ãa]o)|acreditando tratar-se d[ao] (bv|banco|financeira|institui|empresa)",
    "venda_falsa": r"(anunci\w*|leil[ãa]o|site de vendas|marketplace|\bolx\b)[^.]{0,160}(ve[íi]culo|carro|caminh|moto|autom|im[óo]vel|celular|geladeira|m[óo]ve|eletro|produto|bem\b|bens\b)|(adquirir|compra d[eo]|comprar|negocia[çc][ãa]o d[eo])[^.]{0,80}(ve[íi]culo|carro|caminh|moto|autom|im[óo]vel|celular|geladeira|m[óo]ve|eletro)|n[ãa]o entreg|jamais recebeu o",
    "conta_laranja": r"(cedeu|cedid[oa]|emprest\w+|forne\w+|disponibiliz\w+|vend\w+|alug\w+|repass\w+)[^.]{0,40}(sua |seus? |a )?(conta|dados banc|cart[ãa]o)|conta (banc[áa]ria )?(de|em nome de) terceir|conta laranja|contas? de passagem",
    "invasao_dispositivo": r"invad|acesso (indevido|n[ãa]o autorizado)|sem autoriza[çc][ãa]o do titular",
    "senha_credencial_clonagem": r"senha|credenciais|clon(ou|agem|ad[oa])|token|c[óo]digo de (verifica|seguran|acesso)",
}


def campos(numero, t, seg):
    n = seg["narrativa"] or t
    # telefone/WhatsApp e e-mail institucionais do cabeçalho da Promotoria
    n = re.sub(r"(WhatsApp|Telefone|Tel\.?|Fone)\s*:\s*\(?\d{2}\)?\s*[\d\s-]{8,11}|[\w.]+@mp(?:sp|pa)\.mp\.br", " ", n)
    nl = n.lower()
    r = {}
    # valores em reais na narrativa
    vals = []
    for v in re.findall(r"R\$\s*([\d.]+(?:,\d{2})?)", n):
        try:
            vals.append(float(v.replace(".", "").replace(",", ".")))
        except ValueError:
            pass
    r["n_valores"] = len(vals)
    r["valor_max"] = max(vals) if vals else ""
    r["valor_soma_distintos"] = round(sum(set(vals)), 2) if vals else ""
    # data do fato: primeira data na narrativa
    MES = "janeiro|fevereiro|março|marco|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro"
    m = re.search(rf"\b(\d{{1,2}})(?:º|o)?\s+de\s+({MES})\s+de\s+(\d{{4}})", nl) or re.search(r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b", nl)
    r["ano_fato"] = m.group(3) if m else ""
    for k, rx in MEIOS.items():
        r["m_" + k] = bool(re.search(rx, nl))
    # titular da conta recebedora: o denunciado (a lista de MEIOS só pega a cessão narrada)
    r["m_conta_laranja"] = r["m_conta_laranja"] or bool(
        re.search(r"conta (banc[áa]ria |corrente )?(de |em nome d[oa] |pertencente (ao|[àa]) )?(titularidade d[oa] )?(denunciad|acusad|indiciad)", nl)
        or re.search(r"(em sua (pr[óo]pria )?conta|na conta d[oa] (denunciad|acusad))|benefici[áa]ri[oa][^.]{0,60}(denunciad|acusad)", nl)
        or re.search(r"(conta|chave pix)[^.]{0,80}(titularidade|em nome|pertencente|benefici[áa]ri[oa])[^.]{0,20}(d[aeo]s? )?(ora )?(denunciad[oa]|[A-ZÁÉÍÓÚÂÊÔÃÕÇ]{3,} [A-ZÁÉÍÓÚÂÊÔÃÕÇ]{2,})", n))
    # violência doméstica e familiar: no INV, boa parte do 154-A é controle da parceira ou ex-parceira.
    # Menção solta não basta (nome do Anexo de VD no cabeçalho, outro fato, "casa da ex-esposa")
    r["contexto_vd"] = bool(re.search(r"11\.?340", seg["capitulacao"]) or re.search(
        r"(contexto|cen[áa]rio|[âa]mbito)( configurador)? de viol[êe]ncia dom[ée]stica|prevalecendo-se de rela[çc][õo]es dom[ée]sticas"
        r"|rela[çc][ãa]o [íi]ntima de afeto|medidas protetivas|contra sua ex-?\s?\w+|(v[íi]tima|ofendida)[^.]{0,80}sua ex-?\s?(namorad|companheir|espos|mulher|convivente)"
        r"|sua ex-?\s?(namorad|companheir|espos|mulher|convivente)\w*[^.]{0,40}(v[íi]tima|ofendida)", nl))
    r["vitima_idosa"] = bool(re.search(r"idos[oa]|\b(6\d|7\d|8\d|9\d) anos de idade|estatuto do idoso", nl + seg["capitulacao"].lower()))
    r["coautores_desconhecidos"] = bool(re.search(r"(n[ãa]o|ainda n[ãa]o|at[ée] o momento n[ãa]o) identificad|desconhecid", nl))
    r["vitima_pj"] = bool(re.search(r"empresa|ltda|s\.a\.|s/a\b|pessoa jur[íi]dica", nl))
    # denunciados: nomes em caixa alta logo após "denuncio"
    cap = seg["capitulacao"]
    nomes = re.findall(r"\b([A-ZÁÉÍÓÚÂÊÔÃÕÇ]{2,}(?:\s+(?:D[AEO]S?|E)?\s*[A-ZÁÉÍÓÚÂÊÔÃÕÇ]{2,}){1,6})\b", cap[:600])
    nomes = [x for x in nomes if not re.match(r"(VOSSA|EXCEL|CODIGO|CÓDIGO|DENUNC|MINIST|PENAL|LEI|ART)", x)]
    r["n_denunciados_cap"] = len(dict.fromkeys(nomes)) or ""
    # cota
    cota = seg["cota"].lower()
    r["cota_anpp"] = bool(re.search(r"28-a|n[ãa]o persecu|anpp", cota))
    r["anpp_motivo_pena"] = bool(re.search(r"pena m[íi]nima|quatro anos|4 \(quatro\)|4 anos|requisito objetivo", cota))
    r["anpp_motivo_confissao"] = bool(re.search(r"confess", cota))
    r["anpp_motivo_antecedentes"] = bool(re.search(r"antecedente|reinciden|habitual|reitera", cota))
    r["anpp_motivo_ausencia"] = bool(re.search(r"n[ãa]o (foi )?localizad|n[ãa]o compareceu|deixou de se manifestar|n[ãa]o aceit|recus", cota))
    r["pede_preventiva"] = bool(re.search(r"preventiva", cota))
    r["pede_quebra_sigilo"] = bool(re.search(r"quebra|sigilo banc|extrato", cota))
    return r


def metadados(trib):
    """Desenho por processo: no TJSP, a amostra do cjpg; no TJPA, o censo da lista do DJEN."""
    if trib == "tjsp":
        amostra = {r["numero"]: r for r in csv.DictReader(open("dados/cjpg/amostra_tjsp.csv", encoding="utf-8"))}

        def meta(n):
            a = amostra.get(n, {})
            return {"estrato": a.get("estrato"), "ordem": a.get("ordem_no_estrato"), "lista": a.get("lista"),
                    "peso": a.get("peso"), "comarca": a.get("comarca")}
        return meta
    alvos = {r["numero"]: r for r in csv.DictReader(open("dados/djen/alvos_djen_tjpa.csv", encoding="utf-8"))}
    fila = {r["numero"]: r for r in csv.DictReader(open("dados/codex_tjpa/fila.csv", encoding="utf-8"))}

    def meta(n):
        a, q = alvos.get(n, {}), fila.get(n, {})
        rot = set(a.get("consultas", "").split("+"))
        # prioridade da fase 1: INV, depois CL, depois FE (FE, FE_amp ou EE)
        estrato = "INV" if "INV" in rot else "CL" if "CL" in rot else "FE"
        # ordem: posição na fila da coleta (estável); lista: grupo da fila; censo, peso 1
        return {"estrato": estrato, "ordem": q.get("ordem"), "lista": q.get("grupo"), "peso": "1",
                "comarca": a.get("orgao_1g", ""), "consultas": a.get("consultas", ""), "foro": n[-4:]}
    return meta


def main(trib="tjsp"):
    cfg = TRIBUNAIS[trib]
    base, mppa = cfg["base"], cfg["mppa"]
    os.makedirs(f"{OUT}/{cfg['segmentos']}", exist_ok=True)
    meta = metadados(trib)
    status = {r["numero"]: r for r in csv.DictReader(open(cfg["status"], encoding="utf-8"))}
    partes_cota = PARTES_COTA_TJPA if mppa else {}
    linhas = []
    # ordem cronológica do número CNJ (ano, depois sequencial) para que a duplicata
    # aponte para o processo originário
    for numero in sorted(os.listdir(base), key=lambda n: (n[11:15], n[:7])):
        if status.get(numero, {}).get("status") != "ok":
            continue
        a = meta(numero)
        exceto = tuple(partes_cota.get(numero, ())) + tuple((EXCLUI_PARTES_TJPA if mppa else {}).get(numero, ()))
        t, cortado = carrega(numero, base, cfg["cnj"], exceto=exceto)
        seg = segmenta(t, mppa, (ANCORA_MANUAL_TJPA if mppa else {}).get(numero))
        if numero in partes_cota:  # manifestação gravada como parte da denúncia: é cota
            extra = re.sub(r"\s+", " ", " ".join(le_partes(numero, base, so=partes_cota[numero]))).strip()
            seg["cota"] = (seg["cota"] + " " + extra).strip()
        f = artigos(seg["capitulacao"], tolerante=mppa)
        corr, nota_corr = cfg["correcoes"].get(numero, ({}, ""))
        f.update(corr)
        r = {"numero": numero, **a,
             "chars_total": len(t), "chars_cota": len(seg["cota"]), "chars_narrativa": len(seg["narrativa"]),
             "anexo_cortado": cortado, "correcao_manual": nota_corr}
        if mppa:
            r["operacao"] = OPERACAO_TJPA.get(numero, "")
            r["ancora_cap"] = seg["ancora"]
            r["cap_no_preambulo"] = bool(seg.get("capitulacao_no_preambulo"))
        r.update({"a_" + k: v for k, v in f.items()})
        r.update(campos(numero, t, seg))
        # tipo pela capitulação (pós-estratificação)
        if f["154A"]:
            tipo = "154-A"
        elif f["171_2_VII"]:
            tipo = "171 §2º VII"
        elif f["171_2A"]:
            tipo = "171 §2º-A"
        elif f["155_4B"]:
            tipo = "155 §4º-B"
        elif f["171"]:
            tipo = "171 outro"
        elif f["155"]:
            tipo = "155 outro"
        elif f["158"]:
            tipo = "158"
        elif f["180"]:
            tipo = "180"
        elif f["lavagem"]:
            tipo = "lavagem"
        elif seg["capitulacao"]:
            tipo = "outro tipo"
        else:
            tipo = "indeterminado"
        r["tipo_capitulacao"] = tipo
        al = []
        if r["chars_total"] in (30000,) or numero in TRUNCADOS:
            al.append("texto_truncado")
        if not seg["capitulacao"]:
            al.append("sem_capitulacao")
        if len(seg["narrativa"]) < 400:
            al.append("narrativa_curta")
        if tipo == "indeterminado":
            al.append("tipo_indeterminado")
        if r["estrato"] == "INV" and tipo != "154-A":
            al.append("estrato_inv_sem_154A")
        if r["estrato"] == "FE" and tipo != "171 §2º-A":
            al.append("estrato_fe_sem_2A")
        r["alerta"] = ";".join(al)
        r["_texto"] = t
        linhas.append(r)
        json.dump({"numero": numero, **seg}, open(f"{OUT}/{cfg['segmentos']}/{numero}.json", "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
    # mesma denúncia em mais de um processo (desmembramento): marca o processo mais novo
    vistos = {}
    manual = DUPLICATA_MANUAL_TJPA if mppa else {}
    for r in linhas:
        h = hashlib.sha256(r.pop("_texto").encode()).hexdigest()
        r["duplicata_de"] = manual.get(r["numero"]) or vistos.get(h, "")
        if r["duplicata_de"]:
            r["alerta"] = ";".join(filter(None, [r["alerta"], "denuncia_duplicada"]))
        vistos.setdefault(h, r["numero"])
    cols = list(linhas[0].keys())
    with open(f"{OUT}/{cfg['saida']}", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(linhas)
    print(len(linhas), "processos")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "tjsp")
