"""Leitura por regras das sentenças do TJPA (fase 2), com o leitor da fase 1.

Rodar da raiz do repositório:

    python3 scripts/sentencas_tjpa.py              grava dados/extracao/sentencas_tjpa.csv e imprime o resumo
    python3 scripts/sentencas_tjpa.py disp NUM     imprime o dispositivo lido de um processo, para conferência
    python3 scripts/sentencas_tjpa.py revisar      lista os processos marcados para revisão, com o dispositivo

Entrada: textos/tjpa/sentencas/<numero>/NN_<id>.txt, textos/tjpa/manifesto.csv, o status da coleta
(dados/codex_tjpa/status.csv, vale a última linha), a lista do DJEN (dados/djen/alvos_djen_tjpa.csv),
a fila (dados/codex_tjpa/fila.csv) e a extração das denúncias (dados/extracao/denuncias_tjpa.csv, para
`duplicata_de` e `operacao`). Saída com as colunas de sentencas_amostra.csv da fase 1, trocadas as que
só existem no cjpg pelas do DJEN e do manifesto.

Decisões:
- O leitor é o de `scripts/resultado_sentenca.py` (`le`), sem mudança de regra, com a leitura dos
  artigos tolerante ao OCR do TJPA (a mesma da extração das denúncias).
- A decisão que encerra a ação no juízo sem julgar o mérito foi gravada como sentença na coleta e
  recebe resultado próprio, antes do leitor: rejeição da denúncia (total ou parcial, art. 395 do
  CPP), declinação de competência e extinção sem mérito (decadência, continência). O leitor da fase
  1 devolveria "indeterminado" ou "extinção" para elas.
- Em processo com mais de uma decisão gravada, vale a parte indicada em PARTE_SENTENCA (a sentença
  de mérito); embargos, decisão de prescrição posterior e despacho ficam fora.
- Pena e regime: vale a pena "definitiva" da dosimetria do primeiro réu condenado (e a unificada,
  quando o concurso material vem logo depois), porque no TJPA a dosimetria segue o "condeno" e a
  primeira pena do trecho de condenação, que o leitor da fase 1 lê, costuma ser a pena-base; sem
  pena "definitiva", vale o leitor. A coluna `pena_fonte` diz de onde veio.
- O réu com processo suspenso pelo art. 366 do CPP não entra no resultado; a nota diz quem é.
- O resultado final (`resultado`, `tipo_acolhido`, `pena_meses`, `regime`) é o do leitor, salvo as
  correções conferidas na leitura do dispositivo, em CORRECOES, que marcam `conferido=lido`.
"""
import csv
import glob
import os
import re
import sys

sys.path.insert(0, "scripts")
import resultado_sentenca as rs  # noqa: E402

DIR = os.path.join("textos", "tjpa", "sentencas")
SAIDA = os.path.join("dados", "extracao", "sentencas_tjpa.csv")

# processo com mais de uma decisão gravada: a parte que é a sentença de mérito
PARTE_SENTENCA = {
    "0000548-87.2021.8.14.0401": [1],  # parte 2 (16/02/2023) é decisão de citação, chamada "Sentença nº 03"
    "0005766-67.2019.8.14.0401": [1],  # partes 2 e 3 são os embargos (25/03/2025) e a prescrição de uma ré (07/04/2025)
    "0813074-82.2023.8.14.0401": [1],  # parte 2 é o termo da audiência em que a sentença foi proferida
    "0802098-73.2024.8.14.0015": [1],  # parte 2 (16/10/2024) é decisão posterior, que manda cumprir a sentença
}

# decisão terminativa sem mérito; a ordem importa (a primeira que casar vence)
RE_REJEITA = re.compile(r"\brejeit[oa]\s+(?:liminarmente\s+|parcialmente\s+)?a\s+(?:presente\s+)?den[úu]ncia|\bREJEI[TÇ]\w*\s+(?:PARCIALMENTE\s+)?A\s+DEN[ÚU]NCIA|"
                        r"\brejei[çc][ãa]o\s+(?:parcial\s+)?da\s+den[úu]ncia", re.I)
RE_DECLINA = re.compile(r"\bdeclin\w*\s+(?:d[ae]\s+)?(?:a\s+)?compet[êe]ncia|\b(?:reconhe\w+|declar\w+)\s+a\s+incompet[êe]ncia|"
                        r"remet\w*[^.]{0,60}Justi[çc]a Federal|Se[çc][ãa]o\s+Judici[áa]ria", re.I)
RE_DECADENCIA = re.compile(r"decad[êe]ncia", re.I)
RE_CONTINENCIA = re.compile(r"contin[êe]ncia", re.I)
RE_366 = re.compile(r"\b366\s+do\s+(?:C[óo]digo de Processo Penal|CPP)|art\.?\s*366\b", re.I)


def ler_csv(p):
    return list(csv.DictReader(open(p, encoding="utf-8")))


def texto(numero):
    fs = sorted(glob.glob(os.path.join(DIR, numero, "*.txt")))
    so = PARTE_SENTENCA.get(numero)
    if so:
        fs = [f for f in fs if int(os.path.basename(f)[:2]) in so]
    return "\n".join(open(f, encoding="utf-8").read() for f in fs), len(fs)


def terminativa(t, o):
    """Rótulo da decisão terminativa sem mérito, ou "" quando a sentença julga o mérito.

    Só se procura onde o leitor não achou condenação nem absolvição, e no dispositivo e no fim do
    texto, para não tomar a rejeição pedida pela defesa no relatório.
    """
    if o["condena_auto"] or o["absolve_auto"]:
        # rejeição parcial convive com condenação ou absolvição de outro réu
        fim = re.sub(r"\s+", " ", t)[-5000:]
        return "rejeição parcial da denúncia" if RE_REJEITA.search(fim) and re.search(r"quanto a|em rela[çc][ãa]o a", fim, re.I) else ""
    d = rs.dispositivo(t)
    fim = d + " " + re.sub(r"\s+", " ", t)[-5000:]
    if RE_REJEITA.search(fim):
        parcial = re.search(r"parcialmente|rejei[çc][ãa]o parcial|apenas (?:quanto|em rela[çc][ãa]o)|s[óo] quanto|exclusivamente|"
                            r"prosseguimento do feito quanto aos demais|"
                            r"\brecebo\b[^.]{0,80}den[úu]ncia", fim, re.I)
        return "rejeição parcial da denúncia" if parcial else "rejeição da denúncia"
    if RE_DECLINA.search(fim):
        return "declinação de competência"
    if RE_DECADENCIA.search(fim) and re.search(r"extin", fim, re.I):
        return "extinção sem mérito (decadência)"
    if RE_CONTINENCIA.search(fim) and re.search(r"extin|arquiv", fim, re.I):
        return "extinção sem mérito (continência)"
    return ""


# pena e regime na dosimetria: no TJPA a sentença julga ("JULGO PROCEDENTE ... para CONDENAR") e só
# depois dosa a pena, de modo que a pena definitiva fica fora do trecho de condenação que o leitor da
# fase 1 lê. Quando ele não acha pena, vale a primeira pena "definitiva" depois do início do
# dispositivo e, se logo depois vier a unificação (concurso material) com pena maior, a pena unificada.
RE_DEFINITIVA = re.compile(r"definitiv|pena\s+(?:final|concreta)", re.I)
RE_UNIFICA = re.compile(r"unific|concurso material|soma(?:das|ndo|m-se)|pena total|totaliza", re.I)
_N = r"(?:\d{1,2}|um|uma|dois|duas|tr[eê]s|quatro|cinco|seis|sete|oito|nove|dez|onze|doze)"
_U = r"(?:anos?|m[eê]s(?:es)?|dias?)"
# duração seguida da espécie da pena: "4 (quatro) anos e 3 (três) meses de reclusão"
RE_DURACAO = re.compile(r"(" + _N + r"\s*(?:\([^)]*\)\s*)?" + _U + r"(?:\s*(?:,|e)\s*" + _N + r"\s*(?:\([^)]*\)\s*)?" + _U + r")*)"
                        r"\s*,?\s*(?:de\s+)?(?:reclus[ãa]o|deten[çc][ãa]o)", re.I)


def meses_de(txt):
    a = re.search(_N.replace("(?:", "(", 1) + r"\s*(?:\([^)]*\)\s*)?anos?", txt, re.I)
    me = re.search(_N.replace("(?:", "(", 1) + r"\s*(?:\([^)]*\)\s*)?m[eê]s(?:es)?", txt, re.I)
    di = re.search(_N.replace("(?:", "(", 1) + r"\s*(?:\([^)]*\)\s*)?dias?", txt, re.I)
    return (rs.num(a.group(1)) * 12 if a else 0) + (rs.num(me.group(1)) if me else 0) + (round(rs.num(di.group(1)) / 30, 1) if di else 0)


def duracao_junto(tn, pos):
    """Pena privativa dita junto de "definitiva": a última duração nos 260 caracteres antes
    ("fixando-a em 4 anos de reclusão, que torno definitiva") ou a primeira nos 320 depois
    ("torno definitiva a pena de 4 anos de reclusão")."""
    # "fixo a pena definitiva em 4 anos": a duração logo depois vence a que vem antes, que pode
    # ser a de outro crime ("1 mês de detenção (receptação culposa) ... pena definitiva em ...")
    depois = RE_DURACAO.search(tn, pos, pos + 120)
    antes = [m for m in RE_DURACAO.finditer(tn, max(0, pos - 260), pos + 10)]
    m = depois or (antes[-1] if antes else RE_DURACAO.search(tn, pos, pos + 320))
    if not m:
        return None
    return m.start(), meses_de(m.group(1)), re.sub(r"\s+", " ", m.group(0))[:120]


def pena_dosimetria(t):
    tn = re.sub(r"\s+", " ", t)
    d = rs.dispositivo(t)
    i = max(tn.find(d[:120]), 0)
    achou = None
    for m in RE_DEFINITIVA.finditer(tn, i):
        # título da terceira fase ("3ª Fase: Pena Definitiva (Causas de Aumento...)"), não a pena
        if re.search(r"fase\s*[:.–-]?\s*(?:da\s+)?$", tn[max(0, m.start() - 30): m.start()], re.I) or \
                re.match(r"\w*\s*\(", tn[m.start(): m.start() + 15]):
            continue
        r = duracao_junto(tn, m.start())
        if r and r[1]:
            achou = (m.start(),) + r[1:]
            break
    if not achou:
        return "", "", "", ""
    p, meses, txt = achou
    fonte = "dosimetria"
    for u in RE_UNIFICA.finditer(tn, p, p + 3000):
        r = RE_DURACAO.search(tn, u.start(), u.start() + 400)
        if r and meses_de(r.group(1)) > meses:
            meses, txt, fonte = meses_de(r.group(1)), re.sub(r"\s+", " ", r.group(0))[:120], "dosimetria (unificação)"
            break
    reg = rs.RE_REGIME.search(tn, p)
    return meses, txt, (reg.group(1).lower().replace("-", "") if reg else ""), fonte


# correções conferidas na leitura do dispositivo e da dosimetria: numero -> ({campo: valor}, nota)
CORRECOES = {
    "0811772-81.2024.8.14.0401": ({"resultado": "condenação", "tipo_acolhido": "155 outro", "pena_meses": "", "regime": ""},
                                  "JULGAMOS PROCEDENTE, na primeira pessoa do plural, que o leitor não lê: FLÁVIO e JUAREZ condenados "
                                  "nos arts. 155, §4º, II e IV, do CP, 1º, caput, §2º, I e §4º, da Lei 9.613/98 e 288 do CP; pena total não lida "
                                  "(o 155 continuado do primeiro réu chega a 6 anos e 8 meses)"),
    "0009738-16.2017.8.14.0013": ({"resultado": "absolvição", "terminativa": ""},
                                  "sentença em audiência: absolve RENATO do art. 154-A por atipicidade (fato anterior à Lei 12.737/2012 "
                                  "na leitura do juízo, art. 386, III); prescrição da ameaça e da divulgação de segredo e decote do crime de ação "
                                  "privada antes; não há rejeição da denúncia (o termo veio da jurisprudência transcrita)"),
    "0806056-44.2022.8.14.0401": ({"tipo_acolhido": "171 §2º-A"},
                                  "julga parcialmente procedente: condena no art. 171, §2º-A, que absorve os arts. 297 e 304 por consunção; "
                                  "pena de 5 anos em semiaberto"),
    "0814230-71.2024.8.14.0401": ({"tipo_acolhido": "171 §2º-A", "pena_meses": 56, "regime": "semiaberto"},
                                  "JULGA-SE TOTALMENTE PROCEDENTE (forma impessoal, que o leitor não lê como marco): art. 171, §2º-A, c/c art. 71; "
                                  "4 anos e 8 meses em semiaberto"),
    "0802578-85.2023.8.14.0015": ({"tipo_acolhido": "171 outro", "pena_meses": 12, "regime": "aberto", "substituida_auto": True},
                                  "condena no art. 171, caput, e afasta expressamente o §2º-A (o leitor pegou o §2º-A citado no afastamento); "
                                  "pena de 1 ano (o texto diz '01 de reclusão'), aberto, substituída"),
    "0817558-43.2023.8.14.0401": ({"pena_meses": 48, "regime": "aberto"},
                                  "primeiro réu condenado, LUIZ FELIPE: 4 anos em aberto, substituída (a pena vem na seção do regime, sem 'definitiva')"),
    "0000548-87.2021.8.14.0401": ({},
                                  "Operação Trojan; condena DIOGO e ROMÊNIA no art. 1º, §1º, II, da Lei 9.613/98 e absolve HELISON; pena definitiva "
                                  "não localizada no texto (pena-base de DIOGO em 5 anos e 1 mês); a parte 2 gravada é decisão de citação"),
    "0804049-11.2024.8.14.0401": ({"tipo_acolhido": "159"},
                                  "condena no art. 159, caput (o §1º da denúncia cai), absolve do art. 288, parágrafo único, e extingue a "
                                  "punibilidade de JOYCE pela retratação (art. 342, §2º); 9 anos e 9 meses em fechado para o primeiro réu"),
    "0800533-86.2023.8.14.0087": ({},
                                  "condena nos arts. 155, §4º-B, e 180, §3º; a pena é a do furto (1 ano e 6 meses, com arrependimento posterior "
                                  "em 2/3), e não a da receptação culposa, dita antes"),
}
# sentenças marcadas para revisão cuja leitura do dispositivo e da pena confirmou o leitor
CONFERIDAS = {n: "dispositivo e pena conferidos na leitura; leitura por regras mantida" for n in (
    "0003882-76.2014.8.14.0013", "0000586-02.2021.8.14.0401", "0800337-36.2021.8.14.0007", "0801007-56.2021.8.14.0401",
    "0803456-37.2021.8.14.0061", "0819144-86.2021.8.14.0401", "0801803-28.2022.8.14.0008", "0805412-04.2022.8.14.0401",
    "0805552-38.2022.8.14.0401", "0814654-84.2022.8.14.0401", "0819889-84.2022.8.14.0028", "0820198-53.2022.8.14.0401",
    "0824029-12.2022.8.14.0401", "0800643-78.2023.8.14.0057", "0801497-10.2023.8.14.0401", "0801839-21.2023.8.14.0401",
    "0803104-11.2023.8.14.0061", "0817564-50.2023.8.14.0401", "0817566-20.2023.8.14.0401", "0821266-04.2023.8.14.0401",
    "0822630-11.2023.8.14.0401", "0800169-85.2024.8.14.0053", "0802098-73.2024.8.14.0015", "0803124-27.2024.8.14.0009",
    "0803127-79.2024.8.14.0009", "0804452-98.2024.8.14.0006", "0810363-70.2024.8.14.0401", "0811347-54.2024.8.14.0401",
    "0812575-64.2024.8.14.0401", "0813146-35.2024.8.14.0401", "0814661-08.2024.8.14.0401", "0815181-65.2024.8.14.0401",
    "0815210-18.2024.8.14.0401", "0815026-28.2025.8.14.0401", "0818456-51.2026.8.14.0401", "0014826-69.2016.8.14.0401",
)}

CAMPOS_AUTO = rs_campos = ["resultado_auto", "condena_auto", "absolve_auto", "extingue_auto", "parcial_dito",
                           "tipo_acolhido_auto", "acolhe_171_2A", "acolhe_171_2_VII", "acolhe_154A", "acolhe_155_4B",
                           "acolhe_158", "acolhe_288", "acolhe_tentativa", "pena_meses_auto", "pena_texto_auto",
                           "n_penas_auto", "regime_auto", "substituida_auto", "menciona_desclassificacao",
                           "menciona_lei_15397", "desclassifica_disp", "fundamento_abs_auto", "revisar"]
CAMPOS_SAIDA = (["caso", "estrato", "ordem", "numero", "peso", "status_coleta", "duplicata_de", "operacao",
                 "data_sentenca_djen", "data_doc", "nome_doc", "documentos", "chars", "terminativa", "suspenso_366"]
                + CAMPOS_AUTO + ["pena_fonte", "resultado", "tipo_acolhido", "pena_meses", "regime", "conferido", "nota"])


def linhas():
    status = {r["numero"]: r for r in ler_csv(os.path.join("dados", "codex_tjpa", "status.csv"))}
    alvos = {r["numero"]: r for r in ler_csv(os.path.join("dados", "djen", "alvos_djen_tjpa.csv"))}
    fila = {r["numero"]: r for r in ler_csv(os.path.join("dados", "codex_tjpa", "fila.csv"))}
    den = {r["numero"]: r for r in ler_csv(os.path.join("dados", "extracao", "denuncias_tjpa.csv"))}
    man = {}
    for r in ler_csv(os.path.join("textos", "tjpa", "manifesto.csv")):
        if r["papel"] == "sentenca":
            man.setdefault(r["numero"], []).append(r)
    out = []
    for numero in sorted(os.listdir(DIR), key=lambda n: (n[11:15], n[:7])):
        st = status.get(numero, {})
        if st.get("status") not in ("ok", "so_sentenca"):
            continue
        a, q, d = alvos.get(numero, {}), fila.get(numero, {}), den.get(numero, {})
        rot = set(a.get("consultas", "").split("+"))
        estrato = d.get("estrato") or ("INV" if "INV" in rot else "CL" if "CL" in rot else "FE")
        t, ndocs = texto(numero)
        o = rs.le(t, tolerante=True)
        term = terminativa(t, o)
        partes = sorted(man.get(numero, []), key=lambda r: int(r["parte"]))
        p1 = next((r for r in partes if int(r["parte"]) == (PARTE_SENTENCA.get(numero) or [1])[0]), partes[0] if partes else {})
        res = term if term and not (o["condena_auto"] or o["absolve_auto"]) else o["resultado_auto"]
        r = dict(caso=f"PA-{estrato} {q.get('ordem', '')}", estrato=estrato, ordem=q.get("ordem", ""), numero=numero,
                 peso="1", status_coleta=st.get("status"), duplicata_de=d.get("duplicata_de", ""),
                 operacao=d.get("operacao", ""), data_sentenca_djen=a.get("data_sentenca_djen", ""),
                 data_doc=p1.get("data", ""), nome_doc=p1.get("nome", ""), documentos=ndocs, chars=len(t),
                 terminativa=term, suspenso_366=bool(RE_366.search(t)), conferido="auto", nota="")
        r.update({k: o.get(k, "") for k in CAMPOS_AUTO})
        r["revisar"] = bool(o["revisar"] or term)
        # no TJPA a pena "definitiva" da dosimetria vence a primeira pena do trecho de condenação,
        # que costuma ser a pena-base (a dosimetria vem logo depois do "condeno"); sem ela, vale o leitor
        pena_m, regime, fonte = o["pena_meses_auto"], o["regime_auto"], ("dispositivo" if o["pena_meses_auto"] else "")
        if o["condena_auto"]:
            pm, ptxt, preg, pf = pena_dosimetria(t)
            if pm:
                pena_m, fonte = pm, pf
                r["pena_texto_auto"] = ptxt
                regime = preg or regime
        r.update(pena_fonte=fonte, resultado=res, tipo_acolhido=o["tipo_acolhido_auto"] if not term or o["condena_auto"] else "",
                 pena_meses=pena_m, regime=regime)
        corr, nota = CORRECOES.get(numero, ({}, ""))
        if corr or nota:
            r.update(corr)
            if "pena_meses" in corr:
                r["pena_fonte"] = "leitura" if corr["pena_meses"] != "" else ""
            r["conferido"], r["nota"] = "lido", nota
        elif numero in CONFERIDAS:
            r["conferido"], r["nota"] = "lido", CONFERIDAS[numero]
        out.append(r)
    return out


def main():
    out = linhas()
    with open(SAIDA, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=CAMPOS_SAIDA)
        w.writeheader()
        w.writerows(out)
    from collections import Counter
    print(len(out), "sentenças;", Counter(r["resultado"] for r in out))
    print("revisar:", sum(1 for r in out if r["revisar"]), "| conferidas:", sum(1 for r in out if r["conferido"] == "lido"))


def disp(numero, n=2600):
    t, _ = texto(numero)
    print(rs.dispositivo(t, n))


if __name__ == "__main__":
    if sys.argv[1:2] == ["disp"]:
        disp(sys.argv[2])
    elif sys.argv[1:2] == ["revisar"]:
        for r in linhas():
            if r["revisar"] and r["conferido"] != "lido":
                print(f"== {r['caso']} {r['numero']} | {r['resultado']} | tipo {r['tipo_acolhido'] or '-'} | "
                      f"pena {r['pena_meses'] or '-'} | {r['regime'] or '-'} | term {r['terminativa'] or '-'} | 366 {int(r['suspenso_366'])}")
    else:
        main()
