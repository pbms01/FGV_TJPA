"""Questão 1 da análise criminológica: quem o sistema penal alcança na fraude eletrônica.

Acompanha cada denúncia dos estratos CL e FE (sem duplicatas) nas três etapas que a base
cobre: quem é denunciado e por que vetor, o que a sentença faz com ele e o que a Lei
15.397/2026 (171 §2º, VII, DOU de 04/05/2026) muda. Grava dados/analise/q1_alcance.csv
(uma linha por denúncia) e dados/analise/q1_resumo.json, e imprime as tabelas.

Decisões que não saltam aos olhos:
- O nível alcançado é o nó mais alto da cadeia que a denúncia atinge, lido da
  codificação de papel (manual r1/r2 e assistida) e, para os 56 executores e mistos,
  recodificado à mão pela nota de cada linha e, nos casos duvidosos, pela narrativa
  (dicionário NIVEL). Titular da conta vira "só conta" sem recodificação, porque a regra
  do papel já diz que o vínculo do denunciado com o fato é a conta.
- "Autor do ardil" é quem a denúncia diz ter enganado a vítima (ou organizado o golpe),
  e não quem a prova mostra ter falado com ela. Por isso o vetor importa: quando o vetor
  é "registro", a autoria do ardil foi imputada a partir da conta, da linha ou do CNPJ em
  nome do denunciado.
- Os percentuais são ponderados dentro do estrato, como no resto da base. CL e FE não se
  somam, porque os dois universos do cjpg se sobrepõem (uma sentença de fraude eletrônica
  pode falar em conta laranja) e o peso de um não vale para o outro.
- O contato remoto (REMOTO) inclui a telefonia. O contato é lido também pelo canal de
  eixos_mediacao.py (critério das linhas de pesquisa, versão 0.3), para separar internet,
  telefonia e presença; a comparação mostra que o regime de atribuição segue a distância.
- As penas são medianas sem peso, da primeira pena do dispositivo, como em
  consolida_sentencas.py; nos casos com mais de um réu a pena pode ser de outro papel.
"""
import csv
import json
import os
import re
import sys
from collections import Counter, defaultdict
from statistics import median

BASE = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.dirname(__file__))
from consolida_sentencas import lei_15397  # mesma regra de categorização da lei nova
from eixos_mediacao import eixos, le_codificacao, ponderada  # eixos comuns às questões 1 e 2

EXT = os.path.join(BASE, "dados/extracao")
SAIDA = os.path.join(BASE, "dados/analise")
ESTRATOS = ["CL", "FE"]
REMOTO = {"whatsapp", "telefone", "site", "rede_social", "email", "boleto", "sistema"}

# Recodificação à mão dos executores e mistos de CL e FE: (nível, vetor).
# nível: elo logístico = recolhe cartão, retira bem, habilita linha ou arregimenta contas,
# sem que a denúncia lhe atribua o ardil; autor remoto = a denúncia lhe atribui o ardil
# feito à distância (ou a organização do golpe); autor presencial = ardil ou violência
# face a face; fora = fato sem fraude patrimonial.
# vetor: registro = conta, linha ou CNPJ em nome dele ou de pessoa próxima o identifica;
# presença = flagrante, abordagem, recolha ou entrega física; ambos.
NIVEL = {
    # executores sem conta própria
    "CL 12": ("fora", "outro"),
    "FE 6": ("autor remoto", "presença"),      # e-mail falso; abordagem policial com a carga
    "FE 10": ("autor remoto", "presença"),     # cartões pedidos com dados da vítima; entrega interceptada
    "FE 17": ("autor remoto", "presença"),     # compras por link; retirada na loja
    "FE 20": ("autor presencial", "presença"),
    "FE 29": ("autor presencial", "presença"),
    "FE 31": ("autor remoto", "presença"),     # lojas falsas; flagrante com os notebooks
    "FE 39": ("elo logístico", "presença"),    # falso policial recolhe o cartão
    "FE 50": ("autor presencial", "presença"),
    "FE 52": ("elo logístico", "presença"),
    "FE 54": ("elo logístico", "presença"),
    "FE 65": ("elo logístico", "presença"),
    "FE 67": ("autor presencial", "presença"),
    "FE 79": ("elo logístico", "presença"),
    "FE 82": ("autor presencial", "presença"),
    "FE 83": ("autor remoto", "registro"),     # empresa em nome dele; os atendentes não foram identificados
    "FE 84": ("elo logístico", "presença"),
    "FE 87": ("autor remoto", "registro"),     # negocia; o corréu saca da conta da irmã
    "FE 97": ("elo logístico", "presença"),    # preso ao retirar os cartões
    "FE 102": ("autor remoto", "presença"),    # compras online; retirada na loja
    "FE 103": ("autor presencial", "presença"),
    "FE 110": ("autor remoto", "presença"),    # flagrante na entrega
    "FE 118": ("autor remoto", "registro"),    # chave Pix de terceiro enganado leva a ele
    "FE 122": ("elo logístico", "presença"),
    "FE 123": ("fora", "outro"),
    # mistos (o valor entrou em conta de denunciado)
    "CL 1": ("autor presencial", "ambos"),
    "CL 11": ("autor presencial", "ambos"),
    "CL 25": ("fora", "outro"),
    "CL 29": ("autor presencial", "ambos"),
    "CL 53": ("autor presencial", "registro"),  # insider; pagamentos ao companheiro
    "CL 56": ("autor presencial", "ambos"),
    "FE 1": ("autor remoto", "registro"),
    "FE 3": ("elo logístico", "ambos"),          # motoboy recolhe e passa na própria maquininha
    "FE 7": ("autor remoto", "registro"),
    "FE 13": ("autor remoto", "registro"),
    "FE 15": ("autor remoto", "registro"),
    "FE 19": ("autor remoto", "registro"),
    "FE 22": ("autor remoto", "registro"),       # a autoria vem do beneficiário do boleto
    "FE 23": ("autor remoto", "registro"),       # canal não descrito
    "FE 25": ("autor remoto", "registro"),
    "FE 28": ("autor remoto", "registro"),
    "FE 30": ("autor remoto", "registro"),
    "FE 42": ("autor remoto", "registro"),
    "FE 55": ("autor remoto", "registro"),
    "FE 58": ("autor remoto", "registro"),
    "FE 61": ("elo logístico", "registro"),      # um abriu a conta, outro habilitou a linha
    "FE 66": ("autor remoto", "registro"),
    "FE 69": ("autor remoto", "registro"),
    "FE 71": ("autor remoto", "registro"),
    "FE 78": ("autor remoto", "registro"),
    "FE 81": ("autor presencial", "ambos"),      # furto do carro e resgate sob ameaça
    "FE 86": ("autor remoto", "registro"),
    "FE 93": ("autor remoto", "registro"),
    "FE 105": ("autor presencial", "ambos"),
    "FE 107": ("autor remoto", "registro"),      # organizador que arregimenta contas; quem ligou não foi identificado
    "FE 108": ("autor remoto", "registro"),      # conta e linha
    "FE 111": ("autor remoto", "registro"),
    "FE 117": ("autor remoto", "registro"),
    "FE 121": ("autor remoto", "registro"),
    "FE 125": ("autor remoto", "ambos"),         # anúncio na OLX e entrega do carro
    "FE 127": ("autor remoto", "registro"),
    "FE 128": ("autor remoto", "ambos"),         # recebe o Pix e leva o carro
    # misto pela adjudicação do segundo leitor (dados/conferencia/adjudicacao.csv)
    "CL 40": ("autor remoto", "registro"),       # a denúncia lhe atribui a mensagem da falsa sobrinha; o Pix entrou na conta dele
}

# Substituição da pena corrigida pela adjudicação do segundo leitor; o leitor de regras grava
# substituida_auto em sentencas_amostra.csv e o recálculo o sobrescreveria, por isso a
# correção fica aqui. CL 53 e INV 5 não substituem (fechado; 67,2 meses); FE 82 substitui.
SUBSTITUIDA = {"CL 53": "False", "INV 5": "False", "FE 82": "True"}
NIVEIS = ["só conta", "elo logístico", "autor remoto", "autor presencial", "fora"]

# Indícios de como o denunciado foi identificado, por busca de termos na narrativa e na
# cota. É triagem, não codificação: o termo pode aparecer sem ter servido à identificação.
INDICIOS = {
    "telematica": r"\bIP\b|endereços? de IP|\bERB\b|estação rádio|geolocaliza|dados telemáticos|sigilo telemático"
                  r"|quebra.{0,40}telem|intercepta|provedor|registros de acesso",
    "linha_em_nome": r"linha (telefônica|móvel)?.{0,80}(em nome|habilitad|cadastrad|titular)|habilitou a linha|titular da linha",
    "confissao": r"confess",
    "reconhecimento": r"reconhec",
    "flagrante": r"flagrante|foi preso|foram presos|abordad|surpreendid",
    "repasse": r"repass|pulveriz|transferi(u|ram|do)[^.]{0,80}(outra|outras|terceir|diversas) contas?",
}
# Leitura dos trechos em que o termo telemático casou: em nenhum deles o dado telemático do
# canal do ardil identificou o denunciado. São falsos positivos (a sigla "IP" de inquérito e
# de instituição de pagamento, "interceptado" no sentido de detido), a geolocalização do
# celular da vítima no cativeiro (CL 18), o site hospedado no exterior sem continuidade
# (FE 53) e pedidos de quebra feitos depois da prisão física, para achar comparsas
# (FE 17, FE 102, FE 122).
TELEMATICA_LIDA = {
    "CL 13": "Stone IP S.A.", "CL 18": "geolocalização do celular da vítima", "CL 41": "IP de inquérito",
    "FE 53": "provedor estrangeiro, sem continuidade", "FE 60": "falso positivo", "FE 77": "IP de inquérito",
    "FE 106": "IP de inquérito", "FE 86": "IP de inquérito", "FE 10": "interceptar o entregador",
    "FE 17": "quebra pedida depois da apreensão", "FE 102": "quebra pedida depois da prisão",
    "FE 29": "falso positivo", "FE 79": "interceptado pela polícia", "FE 122": "quebra pedida depois da prisão",
    "CL 12": "fora da tipologia", "CL 25": "fora da tipologia",
}


def base():
    den = {x["numero"]: x for x in csv.DictReader(open(os.path.join(EXT, "denuncias_tjsp.csv"), encoding="utf-8"))}
    sent = {x["numero"]: x for x in csv.DictReader(open(os.path.join(EXT, "sentencas_amostra.csv"), encoding="utf-8"))}
    cod = le_codificacao()
    apel = {x["caso"]: x for x in csv.DictReader(open(os.path.join(BASE, "dados/tjsp2/apelacoes_amostra.csv"), encoding="utf-8"))}
    linhas = []
    for n, d in den.items():
        if d["estrato"] not in ESTRATOS or d["duplicata_de"]:
            continue
        c, s = cod[n], sent.get(n)
        caso = f'{d["estrato"]} {d["ordem"]}'
        if c["papel_denunciado"] == "titular_conta":
            nivel, vetor = "só conta", "registro"
        else:
            nivel, vetor = NIVEL[caso]  # KeyError aqui = executor ou misto novo sem recodificação
        x = dict(
            caso=caso, numero=n, estrato=d["estrato"], peso=float(d["peso"]),
            papel=c["papel_denunciado"], nivel=nivel, vetor=vetor,
            meio=c["meio_contato"], remoto=c["meio_contato"] in REMOTO, artificio=c["artificio"],
            canal_eixo=(lambda ex: ex["canal_eixo"] if ex["sistema"] == "meio" else "sistema-objeto, " + ex["canal_eixo"])(eixos(caso, c)),
            eixo_canal=eixos(caso, c)["canal_eixo"], eixo_distancia=eixos(caso, c)["distancia"],
            fonte_codificacao=c["fonte_codificacao"], cap=d["tipo_capitulacao"],
            idosa=d["vitima_idosa"] == "True" or d["a_171_4"] == "True",
            coautores_desconhecidos=d["coautores_desconhecidos"] == "True",
            quebra_sigilo=d["pede_quebra_sigilo"] == "True",
            anpp_tratado=d["cota_anpp"] == "True", anpp_recusa_pena=d["anpp_motivo_pena"] == "True",
            n_denunciados=d["n_denunciados_cap"], ano_fato=d["ano_fato"],
            resultado=s["resultado"] if s else "", tipo_acolhido=s["tipo_acolhido"] if s else "",
            pena_meses=float(s["pena_meses"]) if s and s["pena_meses"] else None,
            regime=s["regime"] if s else "", substituida=SUBSTITUIDA.get(caso, s["substituida_auto"]) if s else "",
            data_sentenca=s["data_mov"] if s else "", conferido_sentenca=s["conferido"] if s else "",
            lei=lei_15397(s) if s else "sem sentença",
            apelacao=apel.get(caso, {}).get("recorrente", ""),
        )
        x["condena"] = x["resultado"] in ("condenação", "procedência parcial")
        seg = json.load(open(os.path.join(EXT, "segmentos", f"{n}.json"), encoding="utf-8"))
        texto = re.sub(r"\s+", " ", seg.get("narrativa", "") + " " + seg.get("cota", ""))
        for k, r in INDICIOS.items():
            x["ind_" + k] = bool(re.search(r, texto, re.I))
        linhas.append(x)
    return linhas


def fmt(dist):
    return "; ".join(f"{k} {n} ({p}%)" for k, (n, p) in dist.items())


def main():
    L = base()
    os.makedirs(SAIDA, exist_ok=True)
    campos = [k for k in L[0] if k != "remoto"] + ["remoto"]
    with open(os.path.join(SAIDA, "q1_alcance.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        for x in sorted(L, key=lambda x: (x["estrato"], int(x["caso"].split()[1]))):
            w.writerow(x)

    out = {}
    for e in ESTRATOS:
        E = [x for x in L if x["estrato"] == e]
        fraude = [x for x in E if x["nivel"] != "fora"]
        o = out[e] = {"denuncias": len(E), "fraude": len(fraude)}
        # Etapa 1: quem a denúncia alcança
        o["nivel"] = ponderada(fraude, lambda x: x["nivel"], NIVEIS)
        o["nivel_por_contato"] = {
            "remoto": ponderada([x for x in fraude if x["remoto"]], lambda x: x["nivel"], NIVEIS),
            "presencial ou outro": ponderada([x for x in fraude if not x["remoto"]], lambda x: x["nivel"], NIVEIS)}
        # A distância, e não a internet, separa os regimes: o golpe por telefone sem internet
        # se comporta como o golpe pela internet.
        o["nivel_por_canal"] = {k: ponderada([x for x in fraude if x["canal_eixo"] == k], lambda x: x["nivel"], NIVEIS)
                                for k in sorted({x["canal_eixo"] for x in fraude})}
        o["nivel_vetor_por_canal"] = {k: ponderada([x for x in fraude if x["canal_eixo"] == k], lambda x: f'{x["nivel"]} | {x["vetor"]}')
                                      for k in ("internet", "telefonia")}
        o["nivel_vetor_contato_remoto"] = ponderada([x for x in fraude if x["remoto"]], lambda x: f'{x["nivel"]} | {x["vetor"]}')
        o["nivel_por_artificio"] = {a: ponderada([x for x in fraude if x["artificio"] == a], lambda x: x["nivel"], NIVEIS)
                                    for a in ("falso_parente", "falsa_central", "venda_falsa", "taxa_antecipada", "maquininha")
                                    if any(x["artificio"] == a for x in fraude)}
        autores = [x for x in fraude if x["nivel"] in ("autor remoto", "elo logístico")]
        o["vetor_autor_remoto_e_logistico"] = ponderada(autores, lambda x: f'{x["nivel"]} | {x["vetor"]}')
        o["vetor_todos"] = ponderada(fraude, lambda x: x["vetor"])
        so = [x for x in fraude if x["nivel"] == "só conta"]
        o["so_conta_coautores_desconhecidos"] = ponderada(so, lambda x: x["coautores_desconhecidos"])
        o["so_conta_repasse_narrado"] = ponderada(so, lambda x: x["ind_repasse"])
        o["indicios_por_nivel_vetor"] = {
            k: {i: sum(x["ind_" + i] for x in fraude if f'{x["nivel"]} | {x["vetor"]}' == k) for i in INDICIOS}
            | {"n": sum(f'{x["nivel"]} | {x["vetor"]}' == k for x in fraude)}
            for k in sorted({f'{x["nivel"]} | {x["vetor"]}' for x in fraude})}
        tel = [x["caso"] for x in E if x["ind_telematica"]]
        o["telematica_casou"] = tel
        o["telematica_sem_leitura"] = [c for c in tel if c not in TELEMATICA_LIDA]
        o["quebra_sigilo_por_nivel"] = {k: ponderada([x for x in fraude if x["nivel"] == k], lambda x: x["quebra_sigilo"])
                                        for k in NIVEIS if any(x["nivel"] == k for x in fraude)}
        o["artificio_so_conta"] = ponderada(so, lambda x: x["artificio"])
        o["cap_por_nivel"] = {k: ponderada([x for x in fraude if x["nivel"] == k], lambda x: x["cap"])
                              for k in NIVEIS if any(x["nivel"] == k for x in fraude)}
        o["anpp_so_conta"] = {
            "tratado na cota": ponderada(so, lambda x: x["anpp_tratado"]),
            "recusa pela pena, entre as tratadas, por capitulação": {
                cap: ponderada([x for x in so if x["anpp_tratado"] and x["cap"] == cap], lambda x: x["anpp_recusa_pena"])
                for cap in sorted({x["cap"] for x in so})}}
        # Etapa 2: sentença
        lidas = [x for x in fraude if x["resultado"] and x["resultado"] != "indeterminado"]
        o["condena_por_nivel"] = {k: ponderada([x for x in lidas if x["nivel"] == k], lambda x: x["condena"])
                                  for k in NIVEIS if any(x["nivel"] == k for x in lidas)}
        cond = [x for x in lidas if x["condena"]]
        o["acolhido_por_nivel"] = {k: ponderada([x for x in cond if x["nivel"] == k and x["tipo_acolhido"]], lambda x: x["tipo_acolhido"])
                                   for k in NIVEIS if any(x["nivel"] == k for x in cond)}
        pen = defaultdict(list)
        for x in cond:
            if x["pena_meses"]:
                pen[(x["nivel"], x["tipo_acolhido"])].append(x["pena_meses"])
        o["pena_mediana"] = {f"{k[0]} | {k[1]}": f"n={len(v)}, mediana {median(v)} meses"
                             for k, v in sorted(pen.items()) if len(v) >= 2}
        # pena do titular no §2º-A, com e sem vítima idosa (§4º)
        t2a = [x for x in cond if x["nivel"] == "só conta" and x["tipo_acolhido"] == "171 §2º-A" and x["pena_meses"]]
        o["so_conta_2A_pena"] = {
            "idosa": (len([x for x in t2a if x["idosa"]]), median([x["pena_meses"] for x in t2a if x["idosa"]] or [0])),
            "não idosa": (len([x for x in t2a if not x["idosa"]]), median([x["pena_meses"] for x in t2a if not x["idosa"]] or [0])),
            "acima de 48 meses": sum(x["pena_meses"] > 48 for x in t2a), "n": len(t2a),
            # art. 44, I, CP: a substituição exige pena não superior a 4 anos
            "substituída até 48 meses": f'{sum(x["substituida"] == "True" for x in t2a if x["pena_meses"] <= 48)} de {sum(x["pena_meses"] <= 48 for x in t2a)}',
            "substituída acima de 48 meses": f'{sum(x["substituida"] == "True" for x in t2a if x["pena_meses"] > 48)} de {sum(x["pena_meses"] > 48 for x in t2a)}'}
        o["regime_por_nivel"] = {k: ponderada([x for x in cond if x["nivel"] == k and x["regime"]], lambda x: x["regime"])
                                 for k in NIVEIS if any(x["nivel"] == k for x in cond)}
        # Etapa 3: Lei 15.397/2026
        pos = [x for x in lidas if x["lei"] != "anterior à lei"]
        o["lei_por_nivel"] = {k: ponderada([x for x in pos if x["nivel"] == k], lambda x: x["lei"])
                              for k in NIVEIS if any(x["nivel"] == k for x in pos)}
        o["so_conta_2A_pos_lei_sem_mencao"] = [x["caso"] for x in pos if x["nivel"] == "só conta"
                                               and x["tipo_acolhido"] == "171 §2º-A" and x["lei"] == "sem menção"]
        # o que a sentença fazia com o titular antes da lei
        pre = [x for x in cond if x["nivel"] == "só conta" and x["lei"] == "anterior à lei" and x["tipo_acolhido"]]
        o["so_conta_pre_lei_acolhido"] = ponderada(pre, lambda x: x["tipo_acolhido"])
        posc = [x for x in cond if x["nivel"] == "só conta" and x["lei"] != "anterior à lei" and x["tipo_acolhido"]]
        o["so_conta_pos_lei_acolhido"] = ponderada(posc, lambda x: x["tipo_acolhido"])

    json.dump(out, open(os.path.join(SAIDA, "q1_resumo.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if "-q" in sys.argv:
        return
    for e, o in out.items():
        print(f"\n===== {e}: {o['fraude']} denúncias de fraude de {o['denuncias']}")
        for k, v in o.items():
            if isinstance(v, dict) and v and all(isinstance(t, tuple) for t in v.values()):
                print(f"{k}: {fmt(v)}")
            elif isinstance(v, dict):
                print(f"{k}:")
                for k2, v2 in v.items():
                    print(f"   {k2}: {fmt(v2) if isinstance(v2, dict) and all(isinstance(t, tuple) for t in v2.values()) else v2}")
            else:
                print(f"{k}: {v}")


if __name__ == "__main__":
    main()
