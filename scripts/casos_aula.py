"""Casos da aula: índice dos 16 casos do plano (e do par 9, do TJPA) e esqueleto de cada ficha.

Uso, da raiz do repo:
    python3 scripts/casos_aula.py indice            # grava dados/aula/casos_aula.csv
    python3 scripts/casos_aula.py esqueleto "INV 39" # imprime os valores já codificados do caso
    python3 scripts/casos_aula.py links "INV 39" "INV 14" ...  # links do GitHub para as peças, em markdown

O plano está em docs/aula/plano-exame-casos.md. O esqueleto reúne, para um caso,
o que as questões 1 a 7 já gravaram (codificação, extração, sentença e saídas de
análise) e os fenômenos em que ele entra, para que a leitura integral confirme ou
corrija campo a campo, e não reescreva. As divergências vão para
dados/aula/divergencias.csv, e a correção segue o caminho de sempre
(grava_codificacao.py, pipe_sentencas.py corrige ou os dicionários dos scripts).
"""
import csv
import os
import sys

# Os oito pares do plano, na ordem da aula, com as questões que cada par examina.
# A ordem e as questões são decisão do plano confirmado em 21/11/2026; mudar aqui
# exige mudar o plano.
PARES = [
    (1, "INV 39", "INV 14", "2,3"),
    (2, "CL 56", "FE 105", "2,4,5,6"),
    (3, "CL 42", "FE 35", "1,3,4,5,6,7"),
    (4, "FE 107", "FE 55", "1,2,4,5,6"),
    (5, "FE 115", "FE 77", "1,3,6,7"),
    (6, "CL 7", "CL 18", "1,2,5,7"),
    (7, "FE 122", "FE 54", "1,3,4,5,6"),
    (8, "CL 48", "CL 13", "1,3,6,7"),
]

# Par 9, do TJPA, montado por decisão do usuário em 22/11/2026 (plano 0.3): família CL,
# com sentença e acórdão nos dois casos. A extração do TJPA não está no main e não há fenômenos do TJPA; o caso é
# designado pelo número curto (na extração descrita no Project, PA-FE 89 e PA-CL 95), e os metadados vêm da leitura (estrato pela conduta).
PARES_TJPA = [
    (9, "TJPA 0800121", "TJPA 0815181", "1,3,5,7"),
]
CASOS_TJPA = {
    "TJPA 0800121": ("0800121-52.2024.8.14.0401", "CL", "Belém (6ª Vara Criminal)"),
    "TJPA 0815181": ("0815181-65.2024.8.14.0401", "CL", "Belém (1ª Vara Criminal)"),
}

INDICE = "dados/aula/casos_aula.csv"
FICHAS = "docs/aula/fichas"

# Links para as pastas das peças no GitHub. Apontam para o main porque os textos
# chegaram lá na mescla de 21/11/2026. O repositório é público desde 21/11/2026, e os
# links entram nas fichas e nos slides da aula (cartões do GitHub de cada caso).
REPO = "https://github.com/pbms01/FGV_TJPA/tree/main"
PECAS = [("denuncias", "denúncia"), ("sentencas", "sentença"), ("acordaos", "acórdão"), ("recursos", "razões de recurso")]

# Campos mostrados no esqueleto, por arquivo de origem. Os arquivos são unidos pela
# coluna caso (ou numero, na codificação, que não tem caso).
FONTES = [
    ("dados/extracao/denuncias_tjsp.csv", "numero",
     ["tipo_capitulacao", "a_154A", "a_155_4B", "a_171_2A", "a_171_4", "a_288", "vitima_idosa", "contexto_vd",
      "valor_max", "ano_fato"]),
    ("codificacao", "numero",
     ["contexto", "meio_contato", "artificio", "papel_denunciado", "conta_do_denunciado", "invasao", "nota"]),
    ("dados/analise/q2_eliminacao.csv", "caso",
     ["eixo_sistema", "eixo_canal", "eixo_distancia", "acesso", "classe", "sem_internet", "cap", "tipo_acolhido"]),
    ("dados/analise/q1_alcance.csv", "caso", ["nivel", "vetor", "lei", "pena_meses", "regime", "substituida"]),
    ("dados/analise/q3_dano.csv", "caso",
     ["resultado", "data_sentenca", "pedido_denuncia", "pedido_moral", "rep_status", "rep_valores", "fundamentos",
      "intermediario_ressarciu", "conseq_valoracao", "conseq_danos", "conseq_nota", "dano_extra"]),
    ("dados/analise/q4_organizacao.csv", "caso",
     ["n_denunciados", "enquadramento", "divisao", "coordenacao", "vinculo", "tipo_estrutura", "sentenca_org"]),
    ("dados/analise/q5_tempo_dado.csv", "caso",
     ["data_fato", "data_denuncia", "meses", "fonte_vitima", "fonte_dispositivo", "fonte_banco", "fonte_operadora",
      "terceiro", "pedido_cota", "pedido_preservacao"]),
    ("dados/analise/q6_servico.csv", "caso", ["familia", "idosa", "aumento_idade", "pj", "credencial", "reacao_banco"]),
    ("dados/analise/q7_titular.csv", "caso", ["versao", "a_quem", "valor_cessao", "antecedentes", "cota_anpp"]),
    ("dados/extracao/sentencas_amostra.csv", "caso", ["resultado", "tipo_acolhido", "pena_meses", "regime", "conferido", "nota"]),
]


def ler(caminho):
    with open(caminho, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def codificacao():
    # Manual (r1, r2) e assistida; a assistida prevalece quando o número se repete,
    # como em grava_codificacao.py.
    linhas = {}
    for p in ["dados/extracao/codificacao_manual_r1.csv", "dados/extracao/codificacao_manual_r2.csv",
              "dados/extracao/codificacao_assistida.csv"]:
        for r in ler(p):
            linhas[r["numero"]] = dict(r, _fonte=os.path.basename(p))
    return linhas


def numeros():
    return {r["caso"]: r for r in ler("dados/analise/q3_dano.csv")}


def amostra():
    return {r["numero"]: r for r in ler("dados/cjpg/amostra_tjsp.csv")}


def fenomenos(caso):
    dentro, base = [], []
    for r in ler("dados/analise/fenomenos_casos.csv"):
        if r["caso"] == caso:
            (dentro if r["no_numerador"] == "True" else base).append(r["id"])
    return dentro, base


def pecas(numero, trib="tjsp"):
    out = []
    for tipo in ["denuncias", "sentencas", "acordaos", "recursos"]:
        d = os.path.join("textos", trib, tipo, numero)
        if os.path.isdir(d):
            n = sum(os.path.getsize(os.path.join(d, x)) for x in os.listdir(d))
            out.append(f"{tipo[:-1]}:{len(os.listdir(d))}:{n}")
    return ";".join(out)


def urls(numero, trib="tjsp"):
    """Peça -> link da pasta no GitHub, só para as peças gravadas."""
    return {rotulo: f"{REPO}/textos/{trib}/{tipo}/{numero}" for tipo, rotulo in PECAS
            if os.path.isdir(os.path.join("textos", trib, tipo, numero))}


def links(casos):
    num = numeros()
    for caso in casos:
        if caso in CASOS_TJPA:
            u = urls(CASOS_TJPA[caso][0], "tjpa")
        elif caso in num:
            u = urls(num[caso]["numero"])
        else:
            sys.exit(f"caso desconhecido: {caso}")
        print(f"- {caso}: " + ", ".join(f"[{rotulo}]({url})" for rotulo, url in u.items()))


def indice():
    num, amo = numeros(), amostra()
    anteriores = {}
    if os.path.exists(INDICE):
        anteriores = {r["caso"]: r for r in ler(INDICE)}
    linhas = []
    for ordem, ancora, contraste, qs in PARES:
        for papel, caso in (("âncora", ancora), ("contraste", contraste)):
            n = num[caso]["numero"]
            dentro, base = fenomenos(caso)
            ficha = os.path.join(FICHAS, caso.replace(" ", "_") + ".md")
            # O estado é o da ficha em disco; as notas do índice anterior são mantidas.
            estado = "redigida" if os.path.exists(ficha) else "pendente"
            u = urls(n)
            linhas.append({
                "ordem": ordem, "par": f"{ancora} / {contraste}", "papel": papel, "caso": caso, "numero": n,
                "estrato": num[caso]["estrato"], "comarca": amo.get(n, {}).get("comarca", ""),
                "questoes": qs, "fenomenos_numerador": ",".join(dentro), "fenomenos_base": ",".join(base),
                "pecas": pecas(n), "ficha": ficha if estado == "redigida" else "", "estado": estado,
                "url_denuncia": u.get("denúncia", ""), "url_sentenca": u.get("sentença", ""),
                "url_acordao": u.get("acórdão", ""), "url_recursos": u.get("razões de recurso", ""),
                "nota": anteriores.get(caso, {}).get("nota", ""),
            })
    for ordem, ancora, contraste, qs in PARES_TJPA:
        for papel, caso in (("âncora", ancora), ("contraste", contraste)):
            n, estrato, comarca = CASOS_TJPA[caso]
            ficha = os.path.join(FICHAS, caso.replace(" ", "_") + ".md")
            estado = "redigida" if os.path.exists(ficha) else "pendente"
            u = urls(n, "tjpa")
            linhas.append({
                "ordem": ordem, "par": f"{ancora} / {contraste}", "papel": papel, "caso": caso, "numero": n,
                "estrato": estrato, "comarca": comarca, "questoes": qs,
                "fenomenos_numerador": "", "fenomenos_base": "",
                "pecas": pecas(n, "tjpa"), "ficha": ficha if estado == "redigida" else "", "estado": estado,
                "url_denuncia": u.get("denúncia", ""), "url_sentenca": u.get("sentença", ""),
                "url_acordao": u.get("acórdão", ""), "url_recursos": u.get("razões de recurso", ""),
                "nota": anteriores.get(caso, {}).get("nota", ""),
            })
    os.makedirs(os.path.dirname(INDICE), exist_ok=True)
    with open(INDICE, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0]))
        w.writeheader()
        w.writerows(linhas)
    print(f"{INDICE}: {len(linhas)} casos, {sum(r['estado'] == 'redigida' for r in linhas)} fichas redigidas")


def esqueleto(caso):
    num = numeros()
    if caso not in num:
        sys.exit(f"caso desconhecido: {caso}")
    n = num[caso]["numero"]
    cod = codificacao()
    print(f"# {caso} ({n})\n")
    for origem, chave, campos in FONTES:
        if origem == "codificacao":
            r = cod.get(n, {})
            rotulo = f"codificação ({r.get('_fonte', 'ausente')})"
        else:
            alvo = n if chave == "numero" else caso
            r = next((x for x in ler(origem) if x.get(chave) == alvo), {})
            rotulo = origem
        print(f"## {rotulo}")
        for c in campos:
            if c in r and r[c] not in ("",):
                print(f"- {c}: {r[c]}")
        print()
    dentro, base = fenomenos(caso)
    print("## fenômenos")
    print("- no numerador: " + (", ".join(dentro) or "nenhum"))
    print("- só na base: " + (", ".join(base) or "nenhum"))
    print(f"\n## peças\n- {pecas(n)}")


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "indice":
        indice()
    elif len(sys.argv) >= 3 and sys.argv[1] == "esqueleto":
        esqueleto(" ".join(sys.argv[2:]))
    elif len(sys.argv) >= 3 and sys.argv[1] == "links":
        links(sys.argv[2:])
    else:
        sys.exit(__doc__)
