#!/usr/bin/env python3
"""Extração por regras das denúncias do corpus TJSP (fase 1).

Entrada: textos/tjsp/denuncias/<numero>/NN_<id>.txt, dados/codex/status.csv e
dados/cjpg/amostra_tjsp.csv. Saída:
  dados/extracao/denuncias_tjsp.csv  (uma linha por processo, campos codificados)
  dados/extracao/segmentos/<numero>.json  (cota, narrativa e capitulação em texto)

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
"""
import csv, glob, hashlib, json, os, re, unicodedata

BASE = "textos/tjsp/denuncias"
OUT = "dados/extracao"
TRUNCADOS = set()  # 1503431-80.2021 foi relido pela cópia de 2025 (OCR), completa
# correções conferidas em outra peça do processo; valem sobre o parser
CORRECOES = {
    "1521208-63.2020.8.26.0228": ({"154A": True}, "capitulação diz 155-A; a sentença de 22/09/2022 lê 154-A e §2º"),
}
CNJ = r"\d{7}-\d{2}\.\d{4}\.8\.26\.\d{4}"


def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def carrega(numero):
    partes = []
    for f in sorted(glob.glob(f"{BASE}/{numero}/*.txt")):
        t = open(f, encoding="utf-8").read()
        t = re.sub(r"\[Texto nativo do PJe\]|\[OCR[^\]]*\]", " ", t)
        partes.append(t)
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


def segmenta(t):
    seg = {"cota": "", "narrativa": "", "capitulacao": ""}
    m_end = RX_ENDERECO.search(t)
    if m_end and m_end.start() > 150:
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
    if not cands:  # último recurso: "incurso" com artigo de tipo penal
        for m in RX_INCURSO.finditer(corpo):
            if RX_ART_CRIME.search(corpo[m.start(): m.start() + 300]):
                cands.append((3, m.start(), m.start()))
    if cands:
        _, anc, cap_ini = sorted(cands)[0]
        # fim: primeiro pedido processual ("Requeiro", "Requer-se", "Rol") depois de 250
        # caracteres; teto de 6000 para as denúncias com lista de denunciados (GAECO)
        m_fim = RX_FIM_CAP.search(corpo, anc + 250)
        fim = min(m_fim.start() if m_fim else anc + 900, anc + 6000)
        seg["capitulacao"] = corpo[cap_ini: fim].strip()
        narr_fim = cap_ini
    else:
        narr_fim = len(corpo)
    m_n = RX_INICIO_NARR.search(corpo[:narr_fim])
    # um "Consta" muito adiante costuma ser citação de documento; então a narrativa
    # começa no endereçamento
    narr_ini = m_n.start() if m_n and m_n.start() < 1500 else 0
    seg["narrativa"] = corpo[narr_ini:narr_fim].strip()
    # cota ao fim (quando não veio no início): trecho depois da capitulação com "ANPP"/"28-A"
    if not seg["cota"]:
        resto = corpo[narr_fim + 900:]
        if re.search(r"28-A|n[ãa]o persecu", resto, re.I):
            seg["cota"] = resto.strip()[:4000]
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


def artigos(cap):
    """Lista de dispositivos do Código Penal e leis citados na capitulação."""
    c = sem_acento(cap).lower()
    c = c.replace("º", "o").replace("°", "o").replace("ª", "a")
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
    n = re.sub(r"(WhatsApp|Telefone|Tel\.?|Fone)\s*:\s*\(?\d{2}\)?\s*[\d\s-]{8,11}|[\w.]+@mpsp\.mp\.br", " ", n)
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


def main():
    os.makedirs(f"{OUT}/segmentos", exist_ok=True)
    amostra = {r["numero"]: r for r in csv.DictReader(open("dados/cjpg/amostra_tjsp.csv", encoding="utf-8"))}
    status = {r["numero"]: r for r in csv.DictReader(open("dados/codex/status.csv", encoding="utf-8"))}
    linhas = []
    # ordem cronológica do número CNJ (ano, depois sequencial) para que a duplicata
    # aponte para o processo originário
    for numero in sorted(os.listdir(BASE), key=lambda n: (n[11:15], n[:7])):
        if status.get(numero, {}).get("status") != "ok":
            continue
        a = amostra.get(numero, {})
        t, cortado = carrega(numero)
        seg = segmenta(t)
        f = artigos(seg["capitulacao"])
        corr, nota_corr = CORRECOES.get(numero, ({}, ""))
        f.update(corr)
        r = {"numero": numero, "estrato": a.get("estrato"), "ordem": a.get("ordem_no_estrato"),
             "lista": a.get("lista"), "peso": a.get("peso"), "comarca": a.get("comarca"),
             "chars_total": len(t), "chars_cota": len(seg["cota"]), "chars_narrativa": len(seg["narrativa"]),
             "anexo_cortado": cortado, "correcao_manual": nota_corr}
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
        json.dump({"numero": numero, **seg}, open(f"{OUT}/segmentos/{numero}.json", "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
    # mesma denúncia em mais de um processo (desmembramento): marca o processo mais novo
    vistos = {}
    for r in linhas:
        h = hashlib.sha256(r.pop("_texto").encode()).hexdigest()
        r["duplicata_de"] = vistos.get(h, "")
        if r["duplicata_de"]:
            r["alerta"] = ";".join(filter(None, [r["alerta"], "denuncia_duplicada"]))
        vistos.setdefault(h, r["numero"])
    cols = list(linhas[0].keys())
    with open(f"{OUT}/denuncias_tjsp.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(linhas)
    print(len(linhas), "processos")


if __name__ == "__main__":
    main()
