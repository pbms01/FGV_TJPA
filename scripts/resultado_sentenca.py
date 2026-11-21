"""Resultado, dispositivos acolhidos e pena lidos no dispositivo da sentença penal.

Uso como módulo (pipe_sentencas.py) ou direto, para validar contra as sentenças
lidas à mão da matriz:

    python3 scripts/resultado_sentenca.py valida

A leitura é por regras e serve de pré-codificação: cada sentença recebe também
`revisar`, verdadeiro quando o resultado é parcial, indeterminado, envolve
desclassificação ou a capitulação não foi achada, para conferência humana.
"""
import csv
import glob
import os
import re
import sys

sys.path.insert(0, "scripts")
from extrai_denuncias import artigos  # noqa: E402  (mesmas regex da capitulação da denúncia)

# marcos do dispositivo; o último "julgo ... procedente" é o melhor, o fecho genérico às vezes
# cai na parte sobre a prisão ou na jurisprudência citada
RE_MARCO = re.compile(r"julgo[^.]{0,60}procedente|julgo[^.]{0,30}improcedente|\babsolvo\b|declaro extinta|"
                      r"rejeito o pedido (formulado |contido |deduzido )?(na |pela )?(den[úu]ncia|condenat|acusat|da acusa|inicial|ministerial)|\bcondeno\b", re.I)
RE_FECHO = re.compile(r"(ante o exposto|diante do exposto|posto isso|isto posto|pelo exposto|em face do exposto|"
                      r"diante disso|ante o acima exposto|em raz[aã]o do exposto)", re.I)
RE_COND = re.compile(r"\bcondeno\b|(?<!deixo de )(?<!deixa de )(?<!deixo de se )\bcondenar\b|\bcondena-se\b|julgo (parcialmente |integralmente )?procedente|"
                     r"procedente em parte|parcialmente procedente", re.I)
RE_ABS = re.compile(r"\babsolv(o|er|endo|e-se|[eê]-l[oa]s?)\b|julgo (totalmente )?improcedente|rejeito o pedido (formulado |contido |deduzido )?(na |pela )?(den[úu]ncia|condenat|acusat|da acusa|inicial|ministerial)|"
                    r"improcedente a (pretens|a[çc][ãa]o|den[úu]ncia)", re.I)
RE_EXT = re.compile(r"extint[ao] a punibilidade|extin[çc][ãa]o da punibilidade|declaro extint", re.I)
RE_PARCIAL = re.compile(r"parcialmente procedente|procedente em parte|julgo parcialmente", re.I)
RE_DESCL = re.compile(r"desclassific|emendatio libelli|nova defini[çc][ãa]o jur[íi]dica|\bart(igo)?\.?\s*383\b", re.I)
RE_LEI_NOVA = re.compile(r"15\.?397", re.I)
RE_REGIME = re.compile(r"regime\s+(?:inicial(?:mente)?\s+)?(?:de\s+cumprimento(?:\s+de\s+pena)?\s+)?(?:o\s+)?(fechado|semi-?aberto|aberto)", re.I)
RE_SUBST = re.compile(r"substitu\w*[^.]{0,160}(restritiv|presta[çc][ãa]o)|substitu[íi]da (na forma|conforme|nos termos)", re.I)
EXTENSO = {"um": 1, "uma": 1, "dois": 2, "duas": 2, "tres": 3, "três": 3, "quatro": 4, "cinco": 5, "seis": 6,
           "sete": 7, "oito": 8, "nove": 9, "dez": 10, "onze": 11, "doze": 12, "treze": 13, "quatorze": 14,
           "catorze": 14, "quinze": 15}


def dispositivo(t, n=4000):
    t = re.sub(r"\s+", " ", t)
    ms = [m for m in RE_MARCO.finditer(t) if m.group(0).lower() != "condeno"]
    if not ms:
        ms = list(RE_MARCO.finditer(t)) or list(RE_FECHO.finditer(t))
    if not ms:
        return t[-n:]
    # recua até o fecho genérico mais próximo, para não cortar o "julgo" do primeiro réu
    ini = ms[-1].start()
    primeiros = [m for m in ms if m.start() > ini - 6000]
    ini = primeiros[0].start() if primeiros else ini
    return t[ini:ini + n]


def trechos_condenacao(d):
    """Pedaços do dispositivo entre um 'condeno/condenar' e o próximo 'absolv' ou fim do réu."""
    partes, i = [], 0
    for m in re.finditer(r"\bcondeno\b|\bcondenar\b|\bcondena-se\b|julgo[^.]{0,60}procedente", d, re.I):
        fim = re.search(r"\babsolv|\bcondeno\b(?! (o|a|os|as) (r[ée]u|acusad|sentenciad)[^.]{0,40}(ao pagamento|nas custas|[àa]s custas))|"
                        r"custas|recorrer em liberdade|apelar em liberdade|tr[âa]nsito em julgado", d[m.end():], re.I)
        partes.append(d[m.start(): m.end() + (fim.start() if fim else 700)])
    return " ".join(partes)


def tipo_de(f):
    for k, nome in (("154A", "154-A"), ("171_2_VII", "171 §2º VII"), ("171_2A", "171 §2º-A"), ("155_4B", "155 §4º-B"),
                    ("171", "171 outro"), ("155", "155 outro"), ("158", "158"), ("157", "157"), ("180", "180"),
                    ("288", "288"), ("lavagem", "lavagem"), ("drogas", "drogas"), ("147", "147"), ("307", "307"),
                    ("298_299", "falsidade")):
        if f.get(k):
            return nome
    return ""


def num(s):
    s = s.lower()
    m = re.match(r"\d+", s)
    if m:
        return int(m.group(0))
    return EXTENSO.get(s.split()[0], 0) if s else 0


def pena_antiga(trecho):
    """Primeira pena privativa no trecho de condenação, em meses (aproximação), e o texto."""
    m = re.search(r"pena[^.]{0,60}?(de\s+)?((\d{1,2}|um|uma|dois|duas|tr[eê]s|quatro|cinco|seis|sete|oito|nove|dez|onze|doze)"
                  r"[^.]{0,160}?)(de\s+)?(reclus[ãa]o|deten[çc][ãa]o)", trecho, re.I)
    if not m:  # "pena de reclusão, pelo prazo de 5 anos e 10 meses"
        m = re.search(r"pena (de\s+)?((reclus[ãa]o|deten[çc][ãa]o)[^.]{0,40}?(\d{1,2}|um|uma|dois|tr[eê]s|quatro|cinco|seis|sete|oito)"
                      r"[^.]{0,80}?(anos?|m[eê]s(es)?))()", trecho, re.I)
        if m:
            txt = trecho[m.start(2): m.end(2) + 40]
            m5 = ""
        else:
            return "", ""
    else:
        txt, m5 = m.group(2), m.group(5)
    W = r"(\d{1,2}|um|uma|dois|duas|tr[eê]s|quatro|cinco|seis|sete|oito|nove|dez|onze|doze)"
    a = re.search(W + r"\s*(\([^)]*\)\s*)?anos?", txt, re.I)
    me = re.search(W + r"\s*(\([^)]*\)\s*)?m[eê]s(es)?", txt, re.I)
    di = re.search(W + r"\s*(\([^)]*\)\s*)?dias?", txt, re.I)
    meses = (num(a.group(1)) * 12 if a else 0) + (num(me.group(1)) if me else 0) + (round(num(di.group(1)) / 30, 1) if di else 0)
    return (meses or ""), re.sub(r"\s+", " ", txt + " " + m5)[:120]



def pena(trecho):
    """Primeira pena privativa no trecho de condenação, em meses (aproximação), e o texto."""
    W = r"(\d{1,2}|um|uma|dois|duas|tr[eê]s|quatro|cinco|seis|sete|oito|nove|dez|onze|doze)"
    m = re.search(r"\bpenas?\s+(?:privativas?\s+de\s+liberdade\s+|corporal\s+)?(?:total\s+)?(?:de\s+|em\s+)"
                  r"(?:(?:reclus[ãa]o|deten[çc][ãa]o)\s*,?\s*(?:de\s+|pelo prazo de\s+)?)?"
                  r"(" + W + r"[^.;]{0,140}(?:anos?|m[eê]s(?:es)?|dias?(?![-\w]))(?:[^.;]{0,60}?(?:reclus[ãa]o|deten[çc][ãa]o))?)",
                  trecho, re.I)
    if not m:
        return pena_antiga(trecho)
    txt = m.group(1)
    corte = re.search(r"reclus[ãa]o|deten[çc][ãa]o", txt, re.I)
    base = txt[:corte.end()] if corte else txt
    a = re.search(W + r"\s*(\([^)]*\)\s*)?anos?", base, re.I)
    me = re.search(W + r"\s*(\([^)]*\)\s*)?m[eê]s(es)?", base, re.I)
    di = re.search(W + r"\s*(\([^)]*\)\s*)?dias?(?![-\w])", base, re.I)
    meses = (num(a.group(1)) * 12 if a else 0) + (num(me.group(1)) if me else 0) + (round(num(di.group(1)) / 30, 1) if di else 0)
    return (meses or ""), re.sub(r"\s+", " ", base)[:120]

def le(t):
    d = dispositivo(t)
    cond, abs_, ext = bool(RE_COND.search(d)), bool(RE_ABS.search(d)), bool(RE_EXT.search(d))
    if cond and (abs_ or RE_PARCIAL.search(d)):
        res = "procedência parcial"
    elif cond:
        res = "condenação"
    elif abs_:
        res = "absolvição"
    elif ext:
        res = "extinção"
    else:
        res = "indeterminado"
    tc = trechos_condenacao(d) if cond else ""
    # "§2ºA", "§ 2º A" e "parágrafo 2º-A" sem hífen: normaliza antes das regex da denúncia
    tc = re.sub(r"(§|par[áa]grafo)\s*2\s*[ºo°ª]?\s*-?\s*A\b", "§ 2º-A", tc)
    f = artigos(tc) if tc else {}
    if tc:
        f["157"] = bool(re.search(r"\b157\b", tc))
    meses, ptxt = pena(tc) if tc else ("", "")
    reg = RE_REGIME.search(tc) if tc else None
    out = dict(resultado_auto=res, condena_auto=cond, absolve_auto=abs_, extingue_auto=ext,
               parcial_dito=bool(RE_PARCIAL.search(d)), tipo_acolhido_auto=tipo_de(f),
               acolhe_171_2A=f.get("171_2A", False), acolhe_171_2_VII=f.get("171_2_VII", False),
               acolhe_154A=f.get("154A", False), acolhe_155_4B=f.get("155_4B", False), acolhe_158=f.get("158", False),
               acolhe_288=f.get("288", False), acolhe_tentativa=f.get("tentativa", False),
               pena_meses_auto=meses, pena_texto_auto=ptxt,
               n_penas_auto=len(re.findall(r"(reclus[ãa]o|deten[çc][ãa]o)", tc, re.I)) if tc else 0,
               regime_auto=(reg.group(1).lower().replace("-", "") if reg else ""),
               substituida_auto=(bool(RE_SUBST.search(tc)) and not re.search(
                   r"(n[ãa]o|incab[íi]vel|invi[áa]vel|descab\w+|deixo de|deixa-se de|deixa de|impossibilidade de)[^.]{0,90}substitu", tc, re.I)) if tc else False,
               menciona_desclassificacao=bool(RE_DESCL.search(t)), menciona_lei_15397=bool(RE_LEI_NOVA.search(t)),
               desclassifica_disp=bool(re.search(r"desclassific|emendatio|\b383\b|nova defini", d[:1500], re.I)))
    fa = []
    for m in re.finditer(r"386[\s,]{0,4}(?:incisos?\s*|incs?\.\s*)?((?:[IVX]{1,4}\b[\s,e]*)+)", d):
        fa += re.findall(r"[IVX]{1,4}", m.group(1))
    out["fundamento_abs_auto"] = ",".join(dict.fromkeys(fa)) if abs_ else ""
    out["revisar"] = (res in ("procedência parcial", "indeterminado", "extinção") or (cond and not out["tipo_acolhido_auto"])
                      or out["desclassifica_disp"] or out["menciona_lei_15397"])
    return out


# referência das 30 sentenças lidas à mão (dados/extracao/sentencas_matriz.csv), por arquivo:
# (houve condenação, houve absolvição de réu ou imputação, tipo do crime mais grave acolhido)
REF = {
    "FE 35": (1, 0, "171 §2º-A"), "CL 42": (1, 0, "171 outro"), "FE 107": (1, 1, "171 outro"),
    "FE 55": (1, 1, "171 §2º-A"), "FE 24": (1, 0, "171 §2º-A"), "CL 41": (1, 0, "155 §4º-B"),
    "FE 122": (1, 1, "171 §2º-A"), "FE 52": (1, 0, "171 §2º-A"), "FE 65": (1, 0, "171 §2º-A"),
    "FE 39": (1, 0, "171 §2º-A"), "FE 54": (1, 1, "171 §2º-A"), "FE 79": (1, 0, "171 §2º-A"),
    "FE 84": (1, 0, "171 §2º-A"), "CL 1": (1, 0, "158"), "CL 11": (1, 0, "171 §2º VII"),
    "CL 11 (corréu)": (1, 0, "158"), "CL 18": (1, 1, "158"), "CL 7": (1, 1, "171 §2º VII"),
    "INV 39": (1, 0, "154-A"), "INV 20": (1, 0, "154-A"), "FE 50": (1, 0, "171 §2º-A"),
    "INV 14": (0, 1, ""), "INV 30": (1, 0, "154-A"), "INV 11": (1, 0, "154-A"), "INV 21": (1, 0, "154-A"),
    "CL 56": (1, 1, "171 §2º-A"), "FE 105": (1, 0, "171 §2º-A"), "FE 115": (1, 0, "171 §2º-A"),
    "FE 77": (1, 0, "171 §2º-A"), "FE 96": (1, 0, "171 §2º-A"),
}
ARQ_CORREU = "92d811d7-98e6-5074-979b-341266563911"


def texto_do_caso(numero, caso):
    fs = sorted(glob.glob(os.path.join("textos", "tjsp", "sentencas", numero, "*.txt")))
    if numero == "0027710-68.2025.8.26.0050":
        fs = [f for f in fs if (ARQ_CORREU in f) == (caso == "CL 11 (corréu)")]
    return "\n".join(open(f, encoding="utf-8").read() for f in fs)


def valida():
    rows = list(csv.DictReader(open("dados/extracao/sentencas_matriz.csv", encoding="utf-8")))
    ok = dict(cond=0, abs=0, tipo=0)
    for r in rows:
        numero = r["numero"].split(" ")[0]
        if r["caso"] == "CL 11 (corréu)":
            numero = "0027710-68.2025.8.26.0050"
        o = le(texto_do_caso(numero, r["caso"]))
        c, a, tp = REF[r["caso"]]
        erros = []
        if o["condena_auto"] == bool(c):
            ok["cond"] += 1
        else:
            erros.append(f"cond {o['condena_auto']}")
        if o["absolve_auto"] == bool(a):
            ok["abs"] += 1
        else:
            erros.append(f"abs {o['absolve_auto']}")
        if o["tipo_acolhido_auto"] == tp:
            ok["tipo"] += 1
        else:
            erros.append(f"tipo {o['tipo_acolhido_auto']!r} x {tp!r}")
        print(f"{r['caso']:15} {o['resultado_auto']:13} {str(o['pena_meses_auto']):6} {o['regime_auto']:10} "
              f"rev={int(o['revisar'])} {'; '.join(erros)}")
    n = len(rows)
    print(f"\nacertos em {n}: condenação {ok['cond']}, absolvição {ok['abs']}, tipo acolhido {ok['tipo']}")


if __name__ == "__main__" and sys.argv[1:] == ["valida"]:
    valida()
