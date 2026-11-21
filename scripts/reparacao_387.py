"""Leitor por regras da reparação mínima (art. 387, IV, do CPP) e das consequências do
crime (art. 59 do CP) nas sentenças da amostra do TJSP, e do pedido de reparação na
denúncia.

Uso como módulo (analise_q3_dano.py) ou direto:

    python3 scripts/reparacao_387.py valida        # compara com a leitura à mão da matriz
    python3 scripts/reparacao_387.py trechos "FE 5" # imprime as janelas lidas de um caso

Decisões que não saltam aos olhos:
- O texto de cada processo é a concatenação das partes gravadas, sem repetição: a coleta
  repetiu o ID do documento para forçar a saída em arquivo, e várias partes são cópias
  idênticas (mesmo sha256 no manifesto).
- A decisão sobre a reparação é procurada só depois do fim do relatório ("é o
  relatório", "decido", "fundamento e decido"), porque o relatório traz os pedidos do MP
  e da defesa com o mesmo vocabulário. O pedido feito nas alegações finais é lido à
  parte, no relatório.
- Uma cláusula só conta como decisão quando tem verbo na primeira pessoa ou impessoal
  ("fixo", "arbitro", "condeno", "fica condenado", "deixo de fixar", "incabível"). Isso
  exclui a jurisprudência citada, que fala do que outro juízo fixou.
- Os valores são os R$ da cláusula de fixação, depois do verbo, sem os que vêm junto de
  prestação pecuniária, fiança, custas, honorários ou dias-multa. O tipo (material ou
  moral) é lido no trecho entre o valor e o anterior. O mesmo valor repetido na
  fundamentação e no dispositivo conta uma vez.
- A janela das consequências do crime é a da dosimetria, e a valoração negativa é lida
  por termos; é triagem, e o dano que ela nomeia é conferido à mão (dicionário
  CONSEQ_MANUAL em analise_q3_dano.py).
"""
import csv
import glob
import hashlib
import os
import re
import sys

BASE = os.path.join(os.path.dirname(__file__), "..")
SENT_DIR = os.path.join(BASE, "textos/tjsp/sentencas")
DEN_DIR = os.path.join(BASE, "textos/tjsp/denuncias")
ARQ_CORREU = "92d811d7-98e6-5074-979b-341266563911"  # sentença do corréu do CL 11, na mesma pasta


def le_partes(pasta, excluir=None):
    vistos, out = set(), []
    for f in sorted(glob.glob(os.path.join(pasta, "*.txt"))):
        if excluir and excluir(f):
            continue
        t = open(f, encoding="utf-8").read()
        h = hashlib.sha256(t.encode()).hexdigest()
        if h in vistos:
            continue
        vistos.add(h)
        out.append(t)
    return re.sub(r"\s+", " ", " ".join(out))


def texto_sentenca(numero, caso=""):
    if numero == "0027710-68.2025.8.26.0050":
        return le_partes(os.path.join(SENT_DIR, numero), lambda f: (ARQ_CORREU in f) != (caso == "CL 11 (corréu)"))
    return le_partes(os.path.join(SENT_DIR, numero))


def texto_denuncia(numero):
    return le_partes(os.path.join(DEN_DIR, numero))


# fim do relatório; a primeira ocorrência marca o início da fundamentação
RE_REL = re.compile(r"[ée] o (breve |sucinto )?relat[óo]rio|relatados? os autos|\brelatado\b|\brelatei\b|"
                    r"fundamento e decido|passo a (decidir|fundamentar)|\bdecido\b|\bfundamenta[çc][ãa]o\s*[:.]", re.I)
# assunto da reparação
RE_TEMA = re.compile(r"387[^0-9]{0,30}IV|repara[çc][ãa]o|indeniza[çc][ãa]o|indenizat[óo]ri|\bindenizar\b|ressarcimento|"
                     r"\bressarcir\b|\breparar\b|danos? (mora|materia)|perdas e danos|pagar (para |à |a )(a )?v[íi]tima", re.I)
# Os radicais levam \w* porque a fronteira de palavra depois de "condenad" falha em
# "condenada" (FE 64).
RE_FIXA = re.compile(r"\b(fixo|arbitro|fixa-se|arbitra-se|fica(m)? (fixad|arbitrad|estabelecid)\w*|estabele[çc]o|"
                     r"condeno|condena-se|fica(m)? (ainda )?condenad\w*|dever[áã]o? (ainda,? )?(indenizar|ressarcir|reparar)|"
                     r"condenando-[ao]s?|acolho o (pleito|pedido)|imponho|determino (que|o pagamento)|"
                     r"determino,? (ainda,? )?(o|a) (ressarcimento|repara[çc][ãa]o|indeniza[çc][ãa]o))(?!\w)", re.I)
# "CONDENO a ré à pena de ... e ao pagamento do valor de R$ 2.200,00 a título de reparação
# mínima" (CL 54): o verbo fica longe; vale a locução com o valor e o título.
RE_FIXA_LOCUCAO = re.compile(r"ao pagamento d[oae]s? (valor|quantia|import[âa]ncia|montante)?\s*(de\s+)?R\$(?:[^.;]|\.(?=\d)){0,120}?"
                             r"a t[íi]tulo de (repara|indeniza)", re.I)
# trecho de ementa ou de acórdão citado: o que se fixou ou negou ali é de outro processo
RE_EMENTA = re.compile(r"Tese de julgamento|Recurso (des)?provido|RECURSO (PARCIALMENTE )?(DES)?PROVIDO|\(TJ-?SP|TJSP;|"
                       r"\bRel\.|Relator\s*\(a\)|Apela[çc][ãa]o Criminal n|\bDJe\b|Quest[ãa]o em discuss[ãa]o|"
                       r"Caso em exame|Raz[õo]es de decidir|apela[çc][ãa]o interposta|\bj\. \d", re.I)
# Negativa forte: verbo de decisão cujo objeto é a reparação (o tema tem de vir até 200
# caracteres depois). Negativa fraca: adjetivo ou locução ("incabível", "não há que se
# falar"), que só conta com o tema logo depois (120) ou abrindo a mesma frase ("Quanto
# ao pedido de reparação, ... incabível"); sem isso pega a insignificância (CL 56).
RE_NEGA = re.compile(r"deixo,?( \w+,)? de (fixar|arbitrar|estabelecer|condenar|aplicar|acolher|impor|proceder|determinar)|"
                     r"deixa-se de (fixar|arbitrar|condenar)|deixa(m)? de ser (fixad|arbitrad)|"
                     r"n[ãa]o (fixo|arbitro|condeno)|indefiro|afasto o (pedido|pleito)|rejeito o (pedido|pleito)|"
                     r"n[ãa]o (será|ser[áa]|deve ser|h[áa] de ser) fixad|sem fixa[çc][ãa]o de", re.I)
RE_NEGA_FRACA = re.compile(r"incab[íi]ve(l|is)|descab(e|id)|invi[áa]ve(l|is)|"
                           r"n[ãa]o h[áa] (como|que se falar|falar|que fixar|o que fixar|que cogitar)|"
                           r"n[ãa]o (é|se mostra|sendo|se faz) (poss[íi]vel|cab[íi]vel|o caso)|"
                           r"prejudicad[ao]|n[ãa]o merece acolhimento|n[ãa]o comporta (acolhimento|fixa)|"
                           r"releg(ar|o|a-se|ada)|remeto (as partes|a v[íi]tima|a quest)", re.I)
RE_ABRE_TEMA = re.compile(r"(quanto|no tocante|em rela[çc][ãa]o|relativamente|no que (tange|concerne)|acerca|sobre)\s+(a|à|ao|o)?\s*"
                          r"(pedido|pleito|requerimento|fixa[çc][ãa]o|valor m[íi]nimo|repara|indeniza)|^\s*(repara[çc][ãa]o|indeniza[çc][ãa]o)", re.I)
RE_VALOR = re.compile(r"R\$\s?((?:\d{1,3}(?:\.\d{3})+|\d+)(?:,\d{1,2})?)(?!\d)")
RE_NAO_REPARA = re.compile(r"presta[çc][ãa]o pecuni[áa]ria|fian[çc]a|custas|honor[áa]rios|dias?-multa|sal[áa]rios? m[íi]nimo|"
                           r"\bmulta\b|UFESP", re.I)
# fim de frase: ponto e maiúscula, ou o parêntese que fecha a citação ("... - grifei) Fixo
# a indenização", FE 17)
RE_FIM = re.compile(r"[.)]\s+(?=[A-ZÁÉÍÓÚÂÊÔÃÕÇ])|P\.?\s?R\.?\s?I\.?", re.U)

FUNDAMENTOS = {
    "sem pedido": r"pedido expresso|(aus[êe]ncia|m[íi]ngua|falta) de (pedido|requerimento|pleito|requisi)|ausente (pedido|requerimento|requisi)|"
                  r"n[ãa]o h[áa] (pedido|requerimento)|n[ãa]o contemplou|n[ãa]o houve (pedido|requerimento|pleito)|"
                  r"falta de (pedido|requerimento)|inexist[êe]ncia de (pedido|requerimento)|sem (pedido|requerimento)|"
                  r"n[ãa]o (foi|houve|tendo sido) (formulad|requerid|pleitead|deduzid)|n[ãa]o (requereu|pleiteou|formulou)|"
                  r"deixou de formular",
    "contraditório e instrução": r"contradit[óo]rio|ampla defesa|instru[çc][ãa]o (espec[íi]fica|pr[óo]pria|probat)|"
                                 r"congru[êe]ncia|(debatid|discutid)[oa]s? (nos autos|durante|na instru)|dila[çc][ãa]o probat",
    "valor não apurado": r"(falta|aus[êe]ncia|m[íi]ngua|car[êe]ncia) de (elementos|prova|comprova|dados|par[âa]metros|documenta)|"
                         r"par[âa]metros seguros|prova (suficiente|espec[íi]fica) (acerca|a respeito|sobre) d[ao] (extens|quantifica)|"
                         r"n[ãa]o (h[áa]|haver|havendo|existem|existir) (elementos|prova|comprova|nos autos (elementos|prova))|elementos (seguros|suficientes|concretos)|"
                         r"n[ãa]o se apur|n[ãa]o (foi|restou|ficou) (apurad|comprovad|demonstrad|quantificad)|"
                         r"(indefinid|incert|il[íi]quid)[oa]|quantum|n[ãa]o (h[áa]|houve) (como )?(apurar|quantificar|precisar)",
    "vítima ressarcida": r"ressarcid|ressarci(u|ram)|(informa[çc][ãa]o|not[íi]cia)[^.]{0,30}ressarcimento|restitu[íi]d|devolvid|recuperad|reembols|estornad|integralmente reparad|"
                         r"repara(ram|do|dos) (os|o|integralmente)|n[ãa]o remanesc",
    "sem prejuízo": r"n[ãa]o (h[áa]|houve) preju[íi]zo|aus[êe]ncia de preju[íi]zo|sem preju[íi]zo (material|a reparar|[àa] v[íi]tima)|"
                    r"inexist[êe]ncia de preju[íi]zo|tentad|tentativa",
    "ação cível em curso": r"ajuizou a[çc][ãa]o|a[çc][ãa]o (civil|c[íi]vel) (j[áa] )?(ajuizad|propost|em curso)",
    "reparação por outro instrumento": r"presta[çc][ãa]o pecuni[áa]ria|acordo de n[ãa]o persecu|\bANPP\b|transa[çc][ãa]o penal",
    "remete à via cível": r"via (c[íi]vel|pr[óo]pria|adequada|ordin[áa]ria)|esfera c[íi]vel|ju[íi]zo c[íi]vel|"
                          r"a[çc][ãa]o (pr[óo]pria|c[íi]vel|competente|aut[ôo]noma)",
}


def inicio_fundamentacao(t):
    m = RE_REL.search(t)
    return m.end() if m else 0


def inicio_frase(t, ini, p, n=600):
    """Início da frase que contém a posição p (último ponto seguido de maiúscula antes dela)."""
    a = max(ini, p - n)
    fins = list(RE_FIM.finditer(t, a, min(len(t), p + 1)))  # +1: o lookahead precisa ver a maiúscula
    return fins[-1].end() if fins else a


def clausula(t, i, n=420):
    """Trecho de t a partir de i até o fim da frase (ou n caracteres)."""
    s = t[i:i + n]
    m = RE_FIM.search(s, 12)
    return s[:m.start() + 1] if m else s


def valores(cl, antes_verbo=""):
    """Valores de reparação numa cláusula de fixação: [(valor, 'material'|'moral', trecho)].
    O tipo do primeiro valor considera também o trecho anterior ao verbo ("diante do dano
    moral causado ..., fixo em R$ 2.000,00", INV 39)."""
    out, ant = [], 0
    ms = list(RE_VALOR.finditer(cl))
    nums = [float(x.group(1).replace(".", "").replace(",", ".")) for x in ms]
    # "R$ 33.638,81, composto por R$ 30.000,00 de prejuízo principal e R$ 3.638,81 de encargos"
    # (CL 13), "R$ 7.900,00, sendo R$ 7.700,00 ... e R$ 200,00" (CL 43): o total e as parcelas;
    # ficam as parcelas fora
    parcelas = set()
    for i in range(len(nums)):
        acc = 0
        for j in range(i + 1, len(nums)):
            acc += nums[j]
            if j > i + 1 and abs(acc - nums[i]) < 0.01:
                parcelas.update(range(i + 1, j + 1))
                break
    for i, m in enumerate(ms):
        if i in parcelas:
            ant = m.end()
            continue
        antes = cl[ant:m.start()]
        depois = cl[m.end():m.end() + 70]
        ant = m.end()
        if RE_NAO_REPARA.search(antes[-90:]):
            continue
        v = float(m.group(1).replace(".", "").replace(",", "."))
        ctx = (antes_verbo[-300:] + " " + antes) if i == 0 else antes
        mo = [x.end() for x in re.finditer(r"\bmora(l|is)\b", ctx, re.I)]
        depois = cl[m.end():(ms[i + 1].start() if i + 1 < len(ms) else m.end() + 90)][:90]
        ma = [x.end() for x in re.finditer(r"\bmateria(l|is)\b|patrimonia(l|is)|preju[íi]zo", ctx, re.I)]
        moral = bool(mo) and (not ma or max(mo) > max(ma))  # vale o qualificativo mais próximo do valor
        dm = re.search(r"danos? (mora|materia|patrimon)", depois, re.I)
        if dm:  # "R$ 5.000,00 (cinco mil reais) a título de reparação mínima pelos danos morais" (INV 44)
            moral = dm.group(1).lower() == "mora"
        out.append((v, "moral" if moral else "material", cl[max(0, m.start() - 80): m.end() + 40]))
    return out


def le_reparacao(t):
    """Decisão sobre a reparação na sentença. Devolve dict com status, valores e fundamentos."""
    ini = inicio_fundamentacao(t)
    clas_fix, clas_neg = [], []
    for m in RE_TEMA.finditer(t, ini):
        jan_ini = max(ini, m.start() - 260)
        jan = t[jan_ini: m.end() + 320]
        for v in RE_FIXA.finditer(jan):
            p = jan_ini + v.start()
            # o verbo precisa estar perto do tema (antes dele ou até 160 caracteres depois)
            if not (m.start() - 260 <= p <= m.end() + 220):
                continue
            cl = clausula(t, p)
            if re.search(r"pena|regime|reclus|deten|dias-multa|\banos?\b|honor[áa]rios|custas", cl[:70], re.I) and not RE_TEMA.search(cl[:90]):
                continue  # "fixo a pena-base", "condeno ao pagamento das custas"
            # o tema na própria cláusula, ou logo antes do verbo com um valor na cláusula
            # ("diante do dano material causado ..., fixo-o em R$ 4.825,81", FE 96)
            if RE_EMENTA.search(t[inicio_frase(t, ini, p):p] + cl):
                continue
            if RE_TEMA.search(cl) or (RE_TEMA.search(t[max(ini, p - 300):p]) and RE_VALOR.search(cl)):
                clas_fix.append((p, cl))
        for rx, depois, fraca in ((RE_NEGA, 200, False), (RE_NEGA_FRACA, 120, True)):
            for v in rx.finditer(jan):
                p = jan_ini + v.start()
                frase_ini = inicio_frase(t, ini, p, 500)
                # o objeto da negativa tem de estar na mesma frase
                seguinte = clausula(t, jan_ini + v.end(), depois)
                # "Assim, deixa de ser fixada ..." (CL 28): o motivo está na frase anterior
                if re.match(r"\s*(assim|dessa forma|desse modo|portanto|logo|por isso|diante disso|destarte|nesse contexto)\b",
                            t[frase_ini:p], re.I):
                    frase_ini = inicio_frase(t, ini, frase_ini - 2, 600)
                abre = t[frase_ini:p]
                if RE_EMENTA.search(t[inicio_frase(t, ini, p, 500): jan_ini + v.end()] + seguinte):
                    continue
                # a negativa tem de ser da reparação, não da substituição da pena, do ANPP
                # ou da insignificância
                if RE_TEMA.search(seguinte) or RE_ABRE_TEMA.search(abre) or (not fraca and RE_TEMA.search(abre[-200:])):
                    clas_neg.append((p, t[frase_ini: jan_ini + v.end() + 460]))
    for m in RE_FIXA_LOCUCAO.finditer(t, ini):
        frase = t[inicio_frase(t, ini, m.start(), 1200): m.end()]
        # só vale com o verbo de condenação na mesma frase: "O réu também foi condenado ...
        # ao pagamento de R$ 54.695,00, a título de reparação" é relato de acórdão citado (CL 8)
        if (RE_FIXA.search(frase) or re.search(r"procedente[^.]{0,120}\bcondenar\b", frase, re.I)) and not RE_EMENTA.search(frase):
            clas_fix.append((m.start(), clausula(t, m.start())))
    # deduplica por posição
    fix = {p: c for p, c in clas_fix}
    neg = {p: c for p, c in clas_neg}
    vals, vistos = [], set()
    for p in sorted(fix):
        achados = valores(fix[p], t[max(ini, p - 300):p])
        if not achados:
            # "Comprovado o dano material ... no valor de R$ 600,00 ..., CONDENO o réu a pagar à
            # vítima tal montante" (FE 87): o valor vem antes do verbo, na mesma frase
            achados = valores(t[inicio_frase(t, ini, p, 500):p])
        for v, tipo, tr in achados:
            if (v, tipo) in vistos:
                continue
            vistos.add((v, tipo))
            vals.append((v, tipo, tr))
    # "valor do prejuízo" sem R$ na cláusula
    sem_valor = [c for p, c in fix.items() if not RE_VALOR.search(c) and not RE_VALOR.search(t[inicio_frase(t, ini, p, 500):p])]
    nega_txt = " ".join(neg.values())
    nega_moral = bool(re.search(r"danos? mora|morais", nega_txt, re.I))
    fund = [k for k, r in FUNDAMENTOS.items() if re.search(r, nega_txt, re.I)]
    material = round(sum(v for v, tp, _ in vals if tp == "material"), 2)
    moral = round(sum(v for v, tp, _ in vals if tp == "moral"), 2)
    if vals:
        status = "fixa"
    elif fix and not neg:
        status = "fixa sem valor lido"
    elif neg:
        status = "nega"
    else:
        status = "silente"
    trechos = [c for _, c in sorted(fix.items())] + [c for _, c in sorted(neg.items())]
    solid = bool(re.search(r"solidari", " ".join(fix.values()), re.I))
    return dict(status=status, valor_material=material, valor_moral=moral, n_valores=len(vals),
                valores=";".join(f"{v:.2f}:{tp}" for v, tp, _ in vals), nega_moral=nega_moral and not moral,
                fundamentos="|".join(fund), solidaria=solid, n_clausulas_fixa=len(fix), n_clausulas_nega=len(neg),
                fixa_sem_valor=len(sem_valor), trechos=trechos, ini_fundamentacao=ini)


# Pedido de reparação na denúncia. A redação varia ("requeiro a fixação", "fixando-se,
# ainda, valor mínimo", "até final condenação que fixe, inclusive, a quantia de R$ ...",
# "que deve incluir, nos termos do art. 387, IV, indenização", "Requer-se seja fixado em
# R$ ..."), por isso vale o termo técnico do pedido, e não o verbo. Ficam fora a reparação
# como condição da suspensão do processo ou do ANPP e a narrativa ("inviabilizando o
# ressarcimento da vítima").
RE_PEDIDO = re.compile(r"387[^0-9]{0,30}IV|\bIV,? do art(igo)?\.? 387|valor m[íi]nimo (para |de |a t[íi]tulo de )?(a |à )?(repara|indeniza|ressarc)|"
                       r"indeniza[çc][ãa]o (civil )?m[íi]nima|repara[çc][ãa]o m[íi]nima|"
                       r"condena[çc][ãa]o (d[oa]s? (r[ée]us?|denunciad[oa]s?|acusad[oa]s?) )?(ao pagamento de |à |a )indeniza|"
                       r"fixa[çc][ãa]o,? (em senten[çc]a,? )?de (valor|indeniza)|"
                       r"condenad[oa]s? (a ressarci|a reparar|a indenizar|à repara|ao ressarcimento|ao pagamento de indeniza)|"
                       r"\b(requeiro|requer|requer-se|postulo|pugno|pleiteio|pleiteia-se)\b[^.]{0,60}(o ressarcimento|a repara[çc][ãa]o|indeniza[çc][ãa]o)|"
                       r"fixado (o )?valor[^.]{0,60}para (a )?repara", re.I)
RE_PEDIDO_FORA = re.compile(r"suspens[ãa]o (condicional )?do processo|art(igo)?\.? 89|sursis|\bANPP\b|acordo de n[ãa]o persecu|28-A", re.I)


def pedido_denuncia(t):
    """Pedido de reparação na denúncia: (há pedido, valor pedido, pede dano moral, trecho)."""
    for m in RE_PEDIDO.finditer(t):
        antes = t[max(0, m.start() - 220): m.start()]
        antes = re.split(r"[.;]\s", antes)[-1]  # só a frase ou o item do pedido (CL 47: "28-A; 03. Requer-se seja fixado")
        if RE_PEDIDO_FORA.search(antes):
            continue
        if re.search(r"deixo de requerer|deixa de requerer|n[ãa]o (requer|requeiro|se requer)", t[max(0, m.start() - 80): m.end()], re.I):
            return False, "", False, "MP declina: " + t[max(0, m.start() - 80): m.end() + 200]  # FE 124
        tr = t[max(0, m.start() - 200): m.end() + 260]
        v = RE_VALOR.search(t[max(0, m.start() - 120): m.end() + 200])
        return True, (float(v.group(1).replace(".", "").replace(",", ".")) if v else ""), bool(re.search(r"\bmora(l|is)\b", tr, re.I)), tr[:460]
    return False, "", False, ""


def pedido_alegacoes(t):
    """Pedido de reparação no relatório da sentença (denúncia ou alegações finais do MP)."""
    ini = inicio_fundamentacao(t)
    rel = t[:ini] if ini else ""
    m = re.search(r"(requer|pleite|postul|pugn|pediu|pedido)[^.]{0,200}?(387[^0-9]{0,30}IV|valor m[íi]nimo (para|de) (a )?(repara|indeniza)|"
                  r"indeniza[çc][ãa]o m[íi]nima|repara[çc][ãa]o (m[íi]nima )?(dos|do|de) danos?|danos? mora)", rel, re.I)
    return bool(m), (rel[m.start(): m.end() + 200] if m else "")


RE_CONSEQ = re.compile(r"(?<!em )(?<!como )(?<!por )\bconsequ[êe]ncias\b|\bconsequ[êe]ncia (do|dos|da) (crime|delito|fato|infra|conduta)", re.I)
RE_NEG59 = re.compile(r"desfavor|negativ|\bgraves?\b|gravíssim|extrapol|exced|superior(es)? ao|expressiv|elevad|consider[áa]ve|vultos|"
                      r"significativ|bastante|acentuad|reprov|exaspe|justifica|nefast|danos[ao]s|severa", re.I)
RE_NORMAL59 = re.compile(r"normais|inerentes?|pr[óo]pri[ao]s (do|ao|à|da) (tipo|esp[ée]cie|delito|crime)|comuns|"
                         r"n[ãa]o (excede|extrapol|desbord|ultrapass|merece|h[áa] (que|o que|nada))|nada a valorar|"
                         r"normalidade|sem relev|n[ãa]o (podem|devem) ser (majorad|valorad)|integram o tipo|ordin[áa]ri[ao]s (ao|à|do|da)", re.I)
DANO59 = {
    "econômico": r"preju[íi]zo|patrimon|R\$|montante|quantia|econ[ôo]mic|financeir|valor(es)? (subtra|desvia|obtid|elevad)|desfalque",
    "psicológico": r"abalo|emocion|ps[íi]qu|psicol|trauma|sofrimento|ang[úu]sti|medo|desespero|ansiedade|depress|alarmad|"
                   r"receio|intranquil|p[âa]nico|terror|humilha",
    "reputacional": r"imagem|reputa|\bhonra\b|credibilidade|bom nome|clientes|seguidores|constrang|vergonha|vexa",
    "digital e informacional": r"intimidade|privacidade|dados pessoais|dados (e|ou) (documentos|informa)|divulga|exposi[çc]|"
                               r"vazament|\bfotos?\b|v[íi]deos? [íi]ntim|vida privada|sigilo|perda (de|do) acesso|conta (invadid|perdid)",
    "físico e saúde": r"sa[úu]de|f[íi]sic|les[ãa]o|integridade|hospital|card[íi]ac|internad",
    "social e relacional": r"fam[íi]li|relacionament|social|comunidade|isolament|filh",
}


def le_consequencias(t):
    """Valoração das consequências do crime na dosimetria: (valoração, danos nomeados, trecho)."""
    ini = inicio_fundamentacao(t)
    achados = []
    for m in RE_CONSEQ.finditer(t, ini):
        jan = t[m.start(): m.start() + 330]
        jan = jan[:RE_FIM.search(jan, 40).end()] if RE_FIM.search(jan, 40) else jan
        frase = t[inicio_frase(t, ini, m.start(), 500): m.start()] + jan
        if re.search(r"jurisprud|precedente|\bSTJ\b|\bSTF\b|Rel\.|Apela[çc][ãa]o (Criminal )?n", jan, re.I) or RE_EMENTA.search(frase):
            continue
        if re.match(r"[A-ZÁÉÍÓÚÂÊÔÃÕÇ\s,.;:\u2013-]{40,}$", frase[-200:]) or frase[-120:].isupper():
            continue  # cabeçalho de ementa em maiúsculas
        neg, norm = bool(RE_NEG59.search(jan)), bool(RE_NORMAL59.search(jan))
        val = "negativa" if neg and not norm else ("neutra" if norm else "indefinida")
        danos = [k for k, r in DANO59.items() if re.search(r, jan, re.I)] if val == "negativa" else []
        achados.append((val, danos, jan))
    if not achados:
        return "não lida", [], ""
    negs = [a for a in achados if a[0] == "negativa"]
    if negs:
        danos = sorted({d for a in negs for d in a[1]})
        return "negativa", danos, " || ".join(a[2] for a in negs)[:900]
    if any(a[0] == "neutra" for a in achados):
        return "neutra", [], next(a[2] for a in achados if a[0] == "neutra")
    return "indefinida", [], achados[0][2]


# Leitura à mão da reparação nas 30 sentenças da matriz (dados/extracao/sentencas_matriz.csv).
# (status, valor material, valor moral, fundamento da negativa, nota). Lida nas janelas
# impressas por `trechos` e, quando a janela não bastou, no texto integral.
REF = {
    "FE 35": ("silente", 0, 0, "", ""),
    "CL 42": ("fixa", 4993, 0, "", "condena os acusados à reparação no valor do dano"),
    "FE 107": ("silente", 0, 0, "", ""),
    "FE 55": ("fixa", 1580, 0, "", "solidária entre os dois condenados; abate valores bloqueados no SISBAJUD"),
    "FE 24": ("fixa", 10000, 0, "", ""),
    "CL 41": ("fixa", 30947, 0, "", "vítima é a instituição de pagamento (PagSeguro)"),
    "FE 122": ("nega", 0, 0, "vítima ressarcida|valor não apurado", "pedido na denúncia; vítima ressarcida pelo banco"),
    "FE 52": ("nega", 0, 0, "sem prejuízo", "tentativa, sem prejuízo"),
    "FE 65": ("silente", 0, 0, "", "ressarcimento pelo banco só nas consequências do crime"),
    "FE 39": ("silente", 0, 0, "", ""),
    "FE 54": ("fixa", 25000, 0, "", ""),
    "FE 79": ("silente", 0, 0, "", ""),
    "FE 84": ("silente", 0, 0, "", "a reparação aparece só em ementa citada"),
    "CL 1": ("silente", 0, 0, "", "sentença de 2014"),
    "CL 11": ("silente", 0, 0, "", ""),
    "CL 11 (corréu)": ("silente", 0, 0, "", ""),
    "CL 18": ("nega", 0, 0, "vítima ressarcida", "os bancos repararam os prejuízos"),
    "CL 7": ("silente", 0, 0, "", ""),
    "INV 39": ("fixa", 0, 2000, "", "dano moral, com relatório psicológico; pedido expresso na denúncia"),
    "INV 20": ("nega", 0, 0, "contraditório e instrução|valor não apurado|remete à via cível", ""),
    "FE 50": ("silente", 0, 0, "", ""),
    "INV 14": ("silente", 0, 0, "", "absolvição; o MP pedira dano moral"),
    "INV 30": ("nega", 0, 0, "valor não apurado", ""),
    "INV 11": ("silente", 0, 0, "", ""),
    "INV 21": ("silente", 0, 0, "", ""),
    "CL 56": ("silente", 0, 0, "", "a reparação aparece só na discussão da insignificância"),
    "FE 105": ("silente", 0, 0, "", "restituição pelo corréu discutida no arrependimento posterior"),
    "FE 115": ("fixa", 2950, 0, "", "condena a ressarcir no valor do prejuízo"),
    "FE 77": ("silente", 0, 0, "", "a reparação aparece só em ementa citada"),
    "FE 96": ("fixa", 4825.81, 0, "", "pedido expresso na denúncia"),
}


def valida():
    rows = list(csv.DictReader(open(os.path.join(BASE, "dados/extracao/sentencas_matriz.csv"), encoding="utf-8")))
    ok = dict(status=0, valor=0, n=0, fund=0, fund_n=0)
    for r in rows:
        numero = "0027710-68.2025.8.26.0050" if r["caso"] == "CL 11 (corréu)" else r["numero"].split(" ")[0]
        o = le_reparacao(texto_sentenca(numero, r["caso"]))
        ref = REF.get(r["caso"])
        if not ref:
            print(f"{r['caso']:15} sem referência: {o['status']} {o['valores']} {o['fundamentos']}")
            continue
        ok["n"] += 1
        st, vm, vmo, fund, nota = ref
        e = []
        st_auto = "fixa" if o["status"].startswith("fixa") else o["status"]
        if st_auto == st:
            ok["status"] += 1
        else:
            e.append(f"status {o['status']} x {st}")
        if abs(o["valor_material"] - vm) < 0.01 and abs(o["valor_moral"] - vmo) < 0.01:
            ok["valor"] += 1
        else:
            e.append(f"valor {o['valor_material']}/{o['valor_moral']} x {vm}/{vmo}")
        if st == "nega":
            ok["fund_n"] += 1
            if set(filter(None, o["fundamentos"].split("|"))) == set(filter(None, fund.split("|"))):
                ok["fund"] += 1
            else:
                e.append(f"fundamento {o['fundamentos']!r} x {fund!r}")
        print(f"{r['caso']:15} {o['status']:20} {o['valores'][:40]:40} {'; '.join(e)}")
    print(f"\nacertos em {ok['n']}: status {ok['status']}, valor {ok['valor']}; fundamento da negativa {ok['fund']} de {ok['fund_n']}")


def trechos(caso):
    sent = {x["caso"]: x for x in csv.DictReader(open(os.path.join(BASE, "dados/extracao/sentencas_amostra.csv"), encoding="utf-8"))}
    numero = sent[caso.replace(" (corréu)", "")]["numero"]
    t = texto_sentenca(numero, caso)
    o = le_reparacao(t)
    print(f"== {caso} {numero} chars={len(t)} fundamentação desde {o['ini_fundamentacao']}")
    print({k: v for k, v in o.items() if k != "trechos"})
    for c in o["trechos"]:
        print("  >>", c[:500])
    print("  pedido nas alegações:", pedido_alegacoes(t))
    print("  consequências:", le_consequencias(t))
    print("  pedido na denúncia:", pedido_denuncia(texto_denuncia(numero)))


if __name__ == "__main__":
    if sys.argv[1:2] == ["valida"]:
        valida()
    elif sys.argv[1:2] == ["trechos"]:
        for c in sys.argv[2:]:
            trechos(c)
