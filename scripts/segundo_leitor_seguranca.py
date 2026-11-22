"""Segundo leitor da aula de segurança da informação (scripts/analise_s_barreira.py).

Um segundo leitor cego (outra instância do mesmo modelo, sem acesso à primeira leitura nem
às notas) codifica, pelo livro de códigos de dados/conferencia/seguranca/livro_codigos_*.md,
as 68 denúncias do universo e as 38 sentenças com o sistema como objeto (mais o INV 10).

Uso (da raiz do repo):

    python3 scripts/segundo_leitor_seguranca.py prepara DESTINO   # lotes cegos fora do repo
    python3 scripts/segundo_leitor_seguranca.py                   # compara e grava a concordância
    python3 scripts/segundo_leitor_seguranca.py -q

Decisões que não saltam aos olhos:
- Os lotes vão para fora do repositório, com identificadores neutros (D01 a D68, S01 a S38)
  sorteados com a semente 20261123; a correspondência fica em dados/conferencia/seguranca/mapa.json.
- A denúncia é a narrativa do segmento da extração, a mesma que a primeira leitura leu; a
  sentença é o texto integral gravado (o do INV 2 está cortado em 100 mil caracteres).
- O vocabulário da via tem um valor a mais que a primeira leitura (sem_barreira), para que o
  segundo leitor possa recusar a premissa da triagem da questão 6 de que a credencial saiu da
  vítima; na comparação, sem_barreira conta como divergência.
- A primeira leitura fica congelada em dados/conferencia/seguranca/primeira_leitura.csv no
  momento da preparação, para que a adjudicação não mude a medida.
"""
import csv
import glob
import json
import os
import random
import re
import sys
from collections import Counter

BASE = os.path.join(os.path.dirname(__file__), "..")
CONF = os.path.join(BASE, "dados/conferencia/seguranca")
MAPA = os.path.join(CONF, "mapa.json")
PRIMEIRA = os.path.join(CONF, "primeira_leitura.csv")
SEMENTE = 20261123

VIA = {  # rótulo da primeira leitura -> código do livro
    "credencial própria de quem tinha acesso legítimo": "interna_propria",
    "credencial de quem tinha acesso legítimo, comprada ou cedida": "interna_terceiro",
    "credencial obtida da vítima por engano": "vitima_engano",
    "credencial obtida da vítima por relação ou coação": "vitima_relacao_coacao",
    "aparelho ou sessão em mãos, sem barreira narrada": "aparelho_aberto",
    "técnica (falha explorada, programa malicioso, força bruta)": "tecnica",
    "a barreira resistiu": "resistiu",
    "via não narrada": "nao_narrada",
}
ELEM_SENT = {  # posição da triagem de dados/aula/inv_elementar_seguranca.csv -> código do livro
    # só as posições que a triagem afirmou; fato anterior à lei, redação revogada transcrita
    # sem efeito (INV 38) e absolvição por outra razão (INV 33) ficam sem primeira leitura
    "dispensa": "dispensa", "dispensa implícita": "dispensa",
    "exige a elementar suprimida": "exige_e_afasta",
}


def le(p):
    return list(csv.DictReader(open(p, encoding="utf-8")))


def limpa(t):
    return re.sub(r"[ \t]+", " ", re.sub(r"\n{3,}", "\n\n", t))


def prepara(destino):
    L = le(os.path.join(BASE, "dados/analise/s_barreira.csv"))
    elem = {x["caso"]: x for x in le(os.path.join(BASE, "dados/aula/inv_elementar_seguranca.csv"))}
    rnd = random.Random(SEMENTE)
    den = L[:]
    rnd.shuffle(den)
    sen = [r for r in L if r["sistema"] == "objeto" or r["caso"] == "INV 10"]
    sen = [r for r in sen if glob.glob(os.path.join(BASE, "textos/tjsp/sentencas", r["numero"], "*.txt"))]
    rnd.shuffle(sen)
    mapa = {"D": {}, "S": {}}
    os.makedirs(destino, exist_ok=True)
    lotes_d = [den[0:23], den[23:46], den[46:]]
    k = 0
    for i, lote in enumerate(lotes_d, 1):
        pasta = os.path.join(destino, f"lote_D{i}")
        os.makedirs(pasta, exist_ok=True)
        for r in lote:
            k += 1
            ident = f"D{k:02d}"
            mapa["D"][ident] = r["caso"]
            seg = json.load(open(os.path.join(BASE, "dados/extracao/segmentos", r["numero"] + ".json"), encoding="utf-8"))
            open(os.path.join(pasta, ident + ".txt"), "w", encoding="utf-8").write(limpa(seg["narrativa"] + "\n\nCAPITULAÇÃO: " + (seg.get("capitulacao") or "")))
    # sentenças: quatro lotes equilibrados pelo tamanho
    tam = {r["caso"]: sum(os.path.getsize(a) for a in glob.glob(os.path.join(BASE, "textos/tjsp/sentencas", r["numero"], "*.txt"))) for r in sen}
    lotes_s = [[], [], [], []]
    for r in sorted(sen, key=lambda r: -tam[r["caso"]]):
        min(lotes_s, key=lambda l: sum(tam[x["caso"]] for x in l)).append(r)
    k = 0
    for i, lote in enumerate(lotes_s, 1):
        pasta = os.path.join(destino, f"lote_S{i}")
        os.makedirs(pasta, exist_ok=True)
        for r in lote:
            k += 1
            ident = f"S{k:02d}"
            mapa["S"][ident] = r["caso"]
            t = "\n".join(open(a, encoding="utf-8").read() for a in sorted(glob.glob(os.path.join(BASE, "textos/tjsp/sentencas", r["numero"], "*.txt"))))
            open(os.path.join(pasta, ident + ".txt"), "w", encoding="utf-8").write(limpa(t))
    os.makedirs(CONF, exist_ok=True)
    json.dump(mapa, open(MAPA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for nome in ("livro_codigos_denuncias.md", "livro_codigos_sentencas.md"):
        open(os.path.join(destino, nome), "w", encoding="utf-8").write(open(os.path.join(CONF, nome), encoding="utf-8").read())
    with open(PRIMEIRA, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["caso", "via", "elementar_denuncia", "elementar_sentenca", "tecnica_na_pena", "prova_interna"])
        for r in L:
            ed = "redacao_revogada" if r["denuncia_redacao_revogada"] == "True" else ("violacao_como_fato" if r["denuncia_narra_elementar"] == "True" else "nao")
            es = ELEM_SENT.get(elem.get(r["caso"], {}).get("posicao", ""), "")
            w.writerow([r["caso"], VIA[r["via"]], ed, es, "1" if r["tecnica_na_pena"] == "True" else "0", r["prova_interna"]])
    print(f"{len(den)} denúncias em 3 lotes, {len(sen)} sentenças em 4 lotes, em {destino}")


def kappa(pares):
    n = len(pares)
    if not n:
        return None
    po = sum(a == b for a, b in pares) / n
    ca, cb = Counter(a for a, _ in pares), Counter(b for _, b in pares)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / n / n
    return round((po - pe) / (1 - pe), 2) if pe < 1 else 1.0


def compara(quieto=False):
    mapa = json.load(open(MAPA, encoding="utf-8"))
    p1 = {x["caso"]: x for x in le(PRIMEIRA)}
    d2, s2 = {}, {}
    for a in glob.glob(os.path.join(CONF, "segundo_leitor_D*.csv")):
        for x in le(a):
            d2[mapa["D"][x["id"].strip()]] = x
    for a in glob.glob(os.path.join(CONF, "segundo_leitor_S*.csv")):
        for x in le(a):
            s2[mapa["S"][x["id"].strip()]] = x
    linhas, resumo = [], {}

    def campo(nome, fonte, chave1, chave2, filtro=lambda c: True):
        pares = []
        for c, x in fonte.items():
            if not filtro(c) or c not in p1 or not p1[c][chave1]:
                continue
            a, b = p1[c][chave1].strip(), x.get(chave2, "").strip()
            pares.append((a, b))
            linhas.append({"campo": nome, "caso": c, "primeira": a, "segunda": b, "concorda": a == b, "nota": x.get("nota", "")})
        resumo[nome] = {"casos": len(pares), "concordancia": round(sum(a == b for a, b in pares) / len(pares), 2) if pares else None, "kappa": kappa(pares)}

    campo("via", d2, "via", "via")
    campo("elementar_denuncia", d2, "elementar_denuncia", "elementar_denuncia")
    campo("elementar_sentenca", s2, "elementar_sentenca", "elementar_sentenca")
    campo("tecnica_na_pena", s2, "tecnica_na_pena", "tecnica_na_pena")
    with open(os.path.join(CONF, "concordancia.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["campo", "caso", "primeira", "segunda", "concorda", "nota"])
        w.writeheader()
        w.writerows(linhas)
    resumo["respostas"] = {"denuncias": len(d2), "sentencas": len(s2)}
    resumo["prova_interna_segundo_leitor"] = {c: x.get("prova_autoria", "") for c, x in s2.items() if x.get("prova_autoria", "").strip() not in ("", "nao_se_aplica")}
    resumo["confianca_na_pena"] = [c for c, x in s2.items() if x.get("confianca_na_pena", "").strip() == "1"]
    json.dump(resumo, open(os.path.join(CONF, "concordancia_resumo.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if not quieto:
        print(json.dumps(resumo, ensure_ascii=False, indent=1))
        for l in linhas:
            if not l["concorda"]:
                print(f'{l["campo"]:20} {l["caso"]:7} 1ª={l["primeira"]:22} 2ª={l["segunda"]:22} {l["nota"][:160]}')


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "prepara":
        prepara(sys.argv[2])
    else:
        compara("-q" in sys.argv)
