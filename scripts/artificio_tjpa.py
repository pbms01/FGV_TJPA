"""Codificação do artifício nas denúncias do TJPA (leitura assistida de 23/11/2026, com segundo
leitor por amostra e adjudicação revista): grava e confere os CSV.

Uso, da raiz do repo:
  python3 scripts/artificio_tjpa.py            confere os CSV e imprime o quadro por família
  python3 scripts/artificio_tjpa.py importa    refaz os CSV a partir da nota e confere

Decisões que não saltam aos olhos:
- A fonte dos CSV é a tabela da nota `docs/analise/codificacao-artificio-tjpa.md`, e não o
  contrário. Os arquivos de trabalho da codificação ficaram na conversa de 23/11/2026 e não
  chegaram ao repositório; a nota, espelhada no Project, guardava a tabela completa e o quadro de
  adjudicação, e foi dela que os CSV saíram em 25/11/2026. Daqui em diante corrige-se o CSV, e a
  nota acompanha.
- A segunda leitura só é conhecida, caso a caso, nas 17 divergências. Nos outros 58 casos da
  amostra ela é igual à primeira e ao valor final, por definição de concordância, e é assim que a
  coluna é preenchida. Fora da amostra fica vazia.
- O código PA não é guardado como dado solto: a conferência o recalcula pela regra da extração do
  TJPA (estrato pelo rótulo do DJEN, na ordem INV, CL, FE, e posição na fila da coleta) e acusa
  qualquer linha que não a reproduza.
- A família é conferida contra o mapeamento da fase 1 (`servico_banco.FAMILIA`), para que o TJPA e
  o TJSP não se afastem em silêncio; o que o TJPA acrescenta está em SEXTA, FORA e OFERTA_TJPA.
"""
import collections
import csv
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from servico_banco import FAMILIA  # noqa: E402  (mapeamento da fase 1, sem efeito colateral na importação)

BASE = os.path.join(os.path.dirname(__file__), "..")
NOTA = os.path.join(BASE, "docs/analise/codificacao-artificio-tjpa.md")
COD = os.path.join(BASE, "dados/extracao/codificacao_artificio_tjpa.csv")
ADJ = os.path.join(BASE, "dados/conferencia/tjpa/adjudicacao_artificio.csv")
FILA = os.path.join(BASE, "dados/codex_tjpa/fila.csv")
ALVOS = os.path.join(BASE, "dados/djen/alvos_djen_tjpa.csv")
TEXTOS = os.path.join(BASE, "textos/tjpa/denuncias")

SEXTA = "ataca sistema ou usa acesso interno"
FORA = "fora da tipologia"
# Artifícios que no gráfico do TJSP formam a sexta família ("sem dinheiro da vítima"), renomeada
# no TJPA porque aqui ela reúne desvios de dinheiro da própria vítima por quem tinha acesso.
SEXTA_ARTIFICIOS = {"controle_parceira", "devassa_privacidade", "invasao_sistema_venda_dados", "insider_empresa"}
OFERTA_TJPA = {"PA-FE 67", "PA-FE 81"}  # taxa antecipada que imita oferta (falso sorteio, falsa vaga)
ORDEM_FAMILIAS = ["imita instituição", "imita oferta", "imita relação pessoal", "manipula o pagamento",
                  "ataca a conta ou o aparelho", SEXTA, FORA]
# Seção "Resultado" da nota: família -> (INV, CL, FE). A conferência falha se os CSV não a reproduzem.
RESULTADO = {
    "imita instituição": (0, 0, 31), "imita oferta": (0, 5, 50), "imita relação pessoal": (0, 2, 26),
    "manipula o pagamento": (0, 0, 24), "ataca a conta ou o aparelho": (3, 4, 24), SEXTA: (8, 1, 4),
    FORA: (0, 0, 1),
}
CAMPOS_COD = ["codigo", "numero", "estrato", "ordem", "artificio", "familia", "segundo_leitor",
              "primeira_leitura", "segunda_leitura", "nota"]
CAMPOS_ADJ = ["id", "caso", "numero", "parte", "bloco", "campo", "primeira", "segunda", "final", "decisao", "motivo"]


def familia(codigo, artificio):
    if artificio == "outro":
        return FORA
    if artificio in SEXTA_ARTIFICIOS:
        return SEXTA
    if artificio == "taxa_antecipada" and codigo in OFERTA_TJPA:
        return "imita oferta"
    return FAMILIA.get(artificio, "")


def tabela(texto, cabecalho):
    """Linhas de uma tabela markdown da nota, achada pelo começo do cabeçalho."""
    linhas = texto.split("\n")
    i = next(k for k, l in enumerate(linhas) if l.startswith(cabecalho))
    out = []
    for l in linhas[i + 2:]:
        if not l.startswith("|"):
            break
        out.append([c.strip() for c in l.strip().strip("|").split("|")])
    return out


def grava(caminho, campos, linhas):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=campos, lineterminator="\n")
        w.writeheader()
        w.writerows(linhas)


def importa():
    texto = open(NOTA, encoding="utf-8").read()
    adj = {}
    for cod, parte, pri, seg, fim, motivo in tabela(texto, "| Código | Parte | Primeira"):
        decisao = "segunda" if fim == seg else "primeira" if fim == pri else "terceira"
        adj[cod] = dict(caso=cod, parte=parte, bloco="codificacao", campo="artificio", primeira=pri,
                        segunda=seg, final=fim, decisao=decisao, motivo=motivo)
    cods = []
    for cod, numero, estrato, art, fam, leitor, nota in tabela(texto, "| Código | Número | Estrato"):
        a = adj.get(cod)
        if a:
            a["numero"] = numero
        na_amostra = bool(leitor)
        cods.append(dict(codigo=cod, numero=numero, estrato=estrato, ordem=cod.split()[1], artificio=art,
                         familia=fam, segundo_leitor=leitor,
                         primeira_leitura=a["primeira"] if a else art,
                         segunda_leitura=(a["segunda"] if a else art) if na_amostra else "",
                         nota=nota))
    chave = {c["codigo"]: k for k, c in enumerate(cods)}
    adjs = sorted(adj.values(), key=lambda a: chave[a["caso"]])
    for k, a in enumerate(adjs, 1):
        a["id"] = f"A{k:02d}"
    grava(COD, CAMPOS_COD, cods)
    grava(ADJ, CAMPOS_ADJ, adjs)
    print(f"gravados {len(cods)} códigos e {len(adjs)} adjudicações")


def confere():
    cods = list(csv.DictReader(open(COD, encoding="utf-8")))
    adjs = list(csv.DictReader(open(ADJ, encoding="utf-8")))
    fila = {r["numero"]: r["ordem"] for r in csv.DictReader(open(FILA, encoding="utf-8"))}
    rotulos = {r["numero"]: set(re.findall(r"\w+", r["consultas"])) for r in csv.DictReader(open(ALVOS, encoding="utf-8"))}
    erros = []

    def estrato(numero):
        r = rotulos.get(numero, set())
        return "INV" if "INV" in r else "CL" if "CL" in r else "FE"

    vistos = set()
    for c in cods:
        cod, num = c["codigo"], c["numero"]
        if num in vistos:
            erros.append(f"{cod}: número repetido")
        vistos.add(num)
        if not os.path.isdir(os.path.join(TEXTOS, num)):
            erros.append(f"{cod}: sem texto de denúncia em textos/tjpa/denuncias/{num}")
        esperado = f"PA-{estrato(num)} {fila.get(num, '?')}"
        if cod != esperado or c["estrato"] != estrato(num) or c["ordem"] != fila.get(num):
            erros.append(f"{cod}: a regra de código dá {esperado}")
        if c["familia"] != familia(cod, c["artificio"]):
            erros.append(f"{cod}: família {c['familia']!r}, o mapeamento dá {familia(cod, c['artificio'])!r}")
        if bool(c["segundo_leitor"]) != bool(c["segunda_leitura"]):
            erros.append(f"{cod}: segunda leitura e marca de amostra não combinam")

    por_cod = {c["codigo"]: c for c in cods}
    for a in adjs:
        c = por_cod.get(a["caso"])
        if not c:
            erros.append(f"{a['caso']}: adjudicação sem linha na codificação")
            continue
        if (c["artificio"], c["primeira_leitura"], c["segunda_leitura"]) != (a["final"], a["primeira"], a["segunda"]):
            erros.append(f"{a['caso']}: adjudicação não aplicada na codificação")
        if a["primeira"] == a["segunda"]:
            erros.append(f"{a['caso']}: adjudicação sem divergência")
    divergentes = {c["codigo"] for c in cods if c["segunda_leitura"] and c["segunda_leitura"] != c["primeira_leitura"]}
    if divergentes != {a["caso"] for a in adjs}:
        erros.append("divergências da codificação e linhas da adjudicação não coincidem")

    quadro = collections.Counter((c["familia"], c["estrato"]) for c in cods)
    for fam, esperado in RESULTADO.items():
        achado = tuple(quadro[(fam, e)] for e in ("INV", "CL", "FE"))
        if achado != esperado:
            erros.append(f"família {fam}: {achado}, a nota diz {esperado}")

    n = collections.Counter(c["estrato"] for c in cods)
    partes = collections.Counter(c["segundo_leitor"] for c in cods if c["segundo_leitor"])
    print(f"{len(cods)} denúncias sem duplicata: INV {n['INV']}, CL {n['CL']}, FE {n['FE']}")
    print(f"segundo leitor: {partes['amostra']} sorteadas, {partes['fronteira']} de fronteira; {len(adjs)} adjudicações "
          f"({collections.Counter(a['decisao'] for a in adjs).most_common()})")
    for parte in ("amostra", "fronteira"):
        casos = [c for c in cods if c["segundo_leitor"] == parte]
        iguais = sum(c["primeira_leitura"] == c["segunda_leitura"] for c in casos)
        fam_iguais = sum(familia(c["codigo"], c["primeira_leitura"]) == familia(c["codigo"], c["segunda_leitura"]) for c in casos)
        print(f"  {parte}: artifício {iguais}/{len(casos)} ({iguais / len(casos):.1%}), família {fam_iguais}/{len(casos)} ({fam_iguais / len(casos):.1%})")
    print(f"{'família':38} INV  CL  FE")
    for fam in ORDEM_FAMILIAS:
        print(f"{fam:38} {quadro[(fam, 'INV')]:3} {quadro[(fam, 'CL')]:3} {quadro[(fam, 'FE')]:3}")
    fe = collections.Counter(c["artificio"] for c in cods if c["estrato"] == "FE")
    print("FE, artifícios mais frequentes:", ", ".join(f"{a} {k}" for a, k in fe.most_common(5)))
    fora = sorted(set(os.listdir(TEXTOS)) - vistos)
    print(f"denúncias com texto e sem linha (duplicatas): {len(fora)}")
    for num in fora:
        print("  ", num)
    if erros:
        print(f"\n{len(erros)} ERRO(S):")
        for e in erros:
            print("  ", e)
        sys.exit(1)
    print("\nconferência sem divergência")


if __name__ == "__main__":
    if sys.argv[1:] == ["importa"]:
        importa()
    confere()
