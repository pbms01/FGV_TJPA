"""Fenômenos da base TJSP: proporção simples e ponderada, com os casos de origem.

Reúne em um só lugar os 18 fenômenos do gráfico de 21/11/2026, cada um com a
questão de onde vem, a base (denominador), o numerador e o percentual simples
e ponderado. Grava:

- dados/analise/fenomenos.csv: uma linha por fenômeno;
- dados/analise/fenomenos_casos.csv: uma linha por fenômeno e caso da base,
  com a marca de que o caso está no numerador. É o ponto de partida para
  examinar cada achado nos processos que o sustentam.

Depende das saídas das questões 1 a 7 e de dados/extracao/denuncias_tjsp.csv.
Rodar da raiz do repo: python3 scripts/fenomenos_ponderados.py [-q]
"""
import csv
import sys
from pathlib import Path

A = Path("dados/analise")


def load(nome):
    with open(A / f"{nome}.csv", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def V(x):
    # Os CSVs das questões gravam booleanos como texto.
    return x == "True"


q1, q2, q3 = load("q1_alcance"), load("q2_eliminacao"), load("q3_dano")
q4, q5, q6, q7 = load("q4_organizacao"), load("q5_tempo_dado"), load("q6_servico"), load("q7_titular")
with open("dados/extracao/denuncias_tjsp.csv", encoding="utf-8") as f:
    # Sem as duplicatas, como em todas as questões.
    # A extração não tem a coluna caso; a junção é pelo número do processo.
    den = {r["numero"]: r for r in csv.DictReader(f) if not r["duplicata_de"]}

SEGURANCA = {"imita instituição", "ataca a conta ou o aparelho", "manipula o pagamento"}
OFERTA_PARENTE = {"imita oferta", "imita relação pessoal"}

# (id, grupo, rótulo, questão, linhas, base, teste do numerador)
# A base é sempre uma lista de linhas de um CSV de questão, e o peso é o da própria linha
# (o peso do processo em dados/cjpg/amostra_tjsp.csv, igual em todos os CSVs).
F = [
    ("inv_sem_internet", "Delito", "Invasões sem internet (contato físico ou rede interna)", "q2", "1.1",
     [x for x in q2 if x["estrato"] == "INV" and x["eixo_sistema"] != "fora"],
     lambda x: x["eixo_sistema"] == "objeto" and x["sem_internet"] == "persiste igual"),
    # A VD vem da codificação (coluna contexto_vd), conta sobre as 34 INV sem duplicatas, com o INV 40.
    ("inv_vd", "Delito", "Invasões em contexto de violência doméstica", "base", "3.4",
     [x for x in q2 if x["estrato"] == "INV"],
     lambda x: V(den[x["numero"]]["contexto_vd"])),
    # Remoto pelo campo remoto da q1 (39 de 40), e não por eixo_distancia (38 de 39).
    ("cl_remoto_so_conta", "Infrator", "À distância: só o titular da conta alcançado", "q1", "2.2",
     [x for x in q1 if x["estrato"] == "CL" and x["nivel"] != "fora" and V(x["remoto"])],
     lambda x: x["nivel"] == "só conta"),
    ("fe_autoria_registro", "Infrator", "Autoria do golpe inferida só do registro", "q1", "2.2",
     [x for x in q1 if x["estrato"] == "FE" and x["nivel"] == "autor remoto" and x["vetor"] == "registro"],
     lambda x: not (V(x["ind_confissao"]) or V(x["ind_reconhecimento"]) or V(x["ind_flagrante"]))),
    ("fe_um_denunciado", "Infrator", "Um único denunciado", "q4", "2.1",
     [x for x in q4 if x["estrato"] == "FE" and not V(x["fora"])],
     lambda x: x["n_denunciados"] == "1"),
    ("plurais_coordenacao", "Infrator", "Denúncias plurais com coordenação narrada", "q4", "2.1",
     [x for x in q4 if not V(x["fora"]) and int(x["n_denunciados"]) > 1],
     lambda x: x["coordenacao"] in ("denunciado", "terceiro")),
    ("titular_admite_cessao", "Infrator", "Titulares que admitem ter cedido a conta", "q7", "2.3",
     q7,
     lambda x: x["grupo_versao"] == "cessão admitida"),
    ("idosa_falso_parente", "Vítima", "Vítima idosa no falso parente e afins", "q6", "3.4",
     [x for x in q6 if not V(x["fora"]) and x["familia"] == "imita relação pessoal" and not V(x["pj"])],
     lambda x: V(x["idosa"])),
    ("idosa_falsa_instituicao", "Vítima", "Vítima idosa na falsa instituição", "q6", "3.4",
     [x for x in q6 if not V(x["fora"]) and x["familia"] == "imita instituição" and not V(x["pj"])],
     lambda x: V(x["idosa"])),
    ("idosa_venda_falsa", "Vítima", "Vítima idosa na venda falsa", "q6", "3.4",
     [x for x in q6 if not V(x["fora"]) and x["familia"] == "imita oferta" and not V(x["pj"])],
     lambda x: V(x["idosa"])),
    ("credencial_falsa_instituicao", "Vítima", "Falsa instituição: senha, código ou cartão entregue", "q6", "4.1",
     [x for x in q6 if not V(x["fora"]) and x["familia"] == "imita instituição"],
     lambda x: V(x["credencial"])),
    ("internet_apos_6m", "Controle social", "Internet: denúncia após os 6 meses de guarda", "q5", "4.4",
     [x for x in q5 if not V(x["fora"]) and x["canal"] == "internet"],
     lambda x: V(x["alem_6m"])),
    ("internet_plataforma_conexao", "Controle social", "Internet: denúncia com dado de plataforma ou conexão", "q5", "4.4",
     [x for x in q5 if not V(x["fora"]) and x["canal"] == "internet"],
     lambda x: V(x["fonte_plataforma"]) or V(x["fonte_conexao"])),
    ("cota_pede_dado", "Controle social", "Cotas que pedem dado novo à investigação", "q5", "4.4",
     [x for x in q5 if not V(x["fora"])],
     lambda x: bool(x["pedido_cota"])),
    # Mesma base do so_conta_fixa_igual_fato de analise_q3_dano.py: condenação, reparação fixada, razão calculável.
    ("fe_reparacao_valor_inteiro", "Controle social", "Reparação do titular pelo valor inteiro do golpe", "q3", "3.3",
     [x for x in q3 if x["estrato"] == "FE" and not V(x["fora"]) and V(x["condena"])
      and x["rep_status"] == "fixa" and x["nivel"] == "só conta" and x["faixa_razao"]],
     lambda x: x["faixa_razao"] == "igual ao valor do fato"),
    ("ressarcimento_seguranca", "Controle social", "Ressarcimento pelo intermediário: golpe pela segurança do serviço", "q6", "4.1",
     [x for x in q6 if not V(x["fora"]) and x["familia"] in SEGURANCA],
     lambda x: bool(x["ressarciu_sentenca"])),
    ("ressarcimento_oferta_parente", "Controle social", "Ressarcimento pelo intermediário: venda falsa e falso parente", "q6", "4.1",
     [x for x in q6 if not V(x["fora"]) and x["familia"] in OFERTA_PARENTE],
     lambda x: bool(x["ressarciu_sentenca"])),
    ("cessao_inciso_vii", "Controle social", "Cessão admitida e condenada no inciso VII", "q7", "1.4",
     [x for x in q7 if x["grupo_versao"] == "cessão admitida" and V(x["condena"])],
     lambda x: x["tipo_acolhido"] == "171 §2º VII"),
]


def pct(a, b):
    return round(100 * a / b, 1) if b else 0.0


linhas, casos = [], []
for fid, grupo, rot, q, lin, base, hit in F:
    h = [x for x in base if hit(x)]
    pb = sum(float(x["peso"]) for x in base)
    ph = sum(float(x["peso"]) for x in h)
    est = sorted({x["estrato"] for x in base})
    linhas.append(dict(id=fid, grupo=grupo, fenomeno=rot, questao=q, linha=lin,
                       estratos="+".join(est), agregado=len(est) > 1,
                       k=len(h), n=len(base), pct_simples=pct(len(h), len(base)), pct_ponderado=pct(ph, pb),
                       casos_numerador="|".join(x["caso"] for x in h)))
    for x in base:
        casos.append(dict(id=fid, questao=q, caso=x["caso"], numero=x["numero"], estrato=x["estrato"],
                          peso=x["peso"], no_numerador=hit(x)))

with open(A / "fenomenos.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(linhas[0]))
    w.writeheader()
    w.writerows(linhas)
with open(A / "fenomenos_casos.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(casos[0]))
    w.writeheader()
    w.writerows(casos)

if "-q" not in sys.argv:
    for l in linhas:
        flag = " (agregado)" if l["agregado"] else ""
        print(f'{l["questao"]:4} {l["fenomeno"][:62]:62} {l["k"]:>3} de {l["n"]:<3} '
              f'{l["pct_simples"]:5.1f}% simples  {l["pct_ponderado"]:5.1f}% ponderado  {l["estratos"]}{flag}')
