"""Confere e tabula o fundamento das absolvições integrais da FE no TJPA (27, por família) e no TJSP (11).

Uso (da raiz do repo):
    python3 scripts/fundamento_absolvicoes.py           confere e imprime as tabelas
    python3 scripts/fundamento_absolvicoes.py tabelas   só as tabelas

Lê dados/analise/fundamento_absolvicoes_fe.csv (leitura caso a caso da fundamentação e do
dispositivo, em 26/11/2026), as sentenças lidas (sentencas_tjpa.csv, sentencas_amostra.csv), a
codificação do papel (codificacao_assistida_tjpa.csv; q1_alcance.csv no TJSP) e a lista do DJEN
(denuncias_tjpa.csv). A conferência não relê as sentenças: verifica que o arquivo cobre exatamente
as absolvições integrais da FE de cada tribunal, que papel e artifício são os da codificação e que
os valores estão no vocabulário. As tabelas decompõem a taxa de absolvição pela posição do MP nas
alegações finais, que é o que separa o TJPA do TJSP.
"""
import csv
import sys
from collections import Counter, defaultdict

ARQ = "dados/analise/fundamento_absolvicoes_fe.csv"
VOC = {
    "fundamento": {"titularidade_insuficiente", "adesao_nao_provada", "autoria_ato", "instrucao_vazia",
                   "atipicidade", "pedido_mp", "materialidade", "outro"},
    "inciso_386": {"III", "V", "VII", "397-II", "397-III"},
    "mp_absolvicao": {"0", "1", "nd"}, "mp_vincula": {"0", "1"}, "revel": {"0", "1"},
    "vitima_juizo": {"s", "n", "parcial", "nd"}, "falta_prova_tecnica": {"0", "1"}, "prova_inquerito": {"0", "1"},
    "versao_reu": {"nega", "cessao", "conta_aberta_por_terceiro", "golpe_sofrido", "perda_aparelho",
                   "explicacao_licita", "confissao", "silencio", "revel", "nd"},
}


def le(arq):
    with open(arq, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def universo():
    pa = [r for r in le("dados/extracao/sentencas_tjpa.csv") if r["estrato"] == "FE" and not r["duplicata_de"] and r["resultado"]]
    sp = [r for r in le("dados/analise/q1_alcance.csv") if r["estrato"] == "FE" and r["resultado"]]
    return pa, sp


def confere(A):
    pa, sp = universo()
    cod = {r["numero"]: r for r in le("dados/extracao/codificacao_assistida_tjpa.csv")}
    q1 = {r["numero"]: r for r in sp}
    erros = []
    alvo = {("TJPA", r["numero"]) for r in pa if r["resultado"] == "absolvição"}
    alvo |= {("TJSP", r["numero"]) for r in sp if r["resultado"] == "absolvição"}
    if {(r["tribunal"], r["numero"]) for r in A} != alvo:
        erros.append("o arquivo não cobre exatamente as absolvições integrais da FE dos dois tribunais")
    for r in A:
        c = cod.get(r["numero"]) if r["tribunal"] == "TJPA" else q1.get(r["numero"])
        papel = (c or {}).get("papel_denunciado") or (c or {}).get("papel")
        if not c or c["artificio"] != r["artificio"] or papel != r["papel_denunciado"]:
            erros.append(f"{r['caso']}: artifício ou papel diferem da codificação")
        for k, voc in VOC.items():
            if r[k] not in voc:
                erros.append(f"{r['caso']}: {k}={r[k]} fora do vocabulário")
        if r["mp_vincula"] == "1" and r["mp_absolvicao"] != "1":
            erros.append(f"{r['caso']}: vinculação ao pedido sem pedido do MP")
        if r["fundamento"] == "pedido_mp" and r["mp_vincula"] != "1":
            erros.append(f"{r['caso']}: fundamento no pedido do MP sem a vinculação")
        if not r["trecho"]:
            erros.append(f"{r['caso']}: sem trecho")
    return erros


def pct(a, b):
    return f"{100 * a / b:.1f}%".replace(".", ",") if b else "-"


def tabelas(A):
    pa, sp = universo()
    a = {r["numero"]: r for r in A}
    den = {r["numero"]: r for r in le("dados/extracao/denuncias_tjpa.csv")}
    cod = {r["numero"]: r for r in le("dados/extracao/codificacao_assistida_tjpa.csv")}
    print("Fundamento da absolvição (TJPA: contagem; TJSP: contagem e % ponderado pela amostra)\n")
    print("| Fundamento | TJPA (27) | TJSP (11) |")
    print("| --- | --- | --- |")
    pw = {r["numero"]: float(r["peso"]) for r in sp}
    W = sum(pw[r["numero"]] for r in A if r["tribunal"] == "TJSP")
    for f in ["titularidade_insuficiente", "adesao_nao_provada", "autoria_ato", "instrucao_vazia", "atipicidade", "pedido_mp"]:
        n1 = sum(r["fundamento"] == f for r in A if r["tribunal"] == "TJPA")
        sub = [r for r in A if r["tribunal"] == "TJSP" and r["fundamento"] == f]
        w = sum(pw[r["numero"]] for r in sub)
        print(f"| {f.replace('_', ' ')} | {n1} | {len(sub)} ({pct(w, W)}) |")
    print("\nTaxa de absolvição integral da FE pela posição do MP nas alegações finais\n")
    print("| | TJPA (92 sentenças, censo) | TJSP (113 sentenças, % ponderado) |")
    print("| --- | --- | --- |")
    Wt = sum(pw.values())
    for rot, cond in [("Absolvição integral", lambda r: True),
                      ("pedida pelo MP", lambda r: r["mp_absolvicao"] == "1"),
                      ("contra o pedido de condenação", lambda r: r["mp_absolvicao"] == "0"),
                      ("posição do MP não registrada", lambda r: r["mp_absolvicao"] == "nd")]:
        n1 = sum(1 for r in pa if r["resultado"] == "absolvição" and cond(a[r["numero"]]))
        w = sum(pw[r["numero"]] for r in sp if r["resultado"] == "absolvição" and cond(a[r["numero"]]))
        n2 = sum(1 for r in sp if r["resultado"] == "absolvição" and cond(a[r["numero"]]))
        print(f"| {rot} | {n1} ({pct(n1, len(pa))}) | {n2} ({pct(w, Wt)}) |")
    print("\nAbsolvição por papel do denunciado (codificação da denúncia)\n")
    print("| Papel | TJPA | TJSP (pond.) |")
    print("| --- | --- | --- |")
    for p in ["titular_conta", "misto", "executor"]:
        s1 = [r for r in pa if cod.get(r["numero"], {}).get("papel_denunciado") == p]
        a1 = sum(r["resultado"] == "absolvição" for r in s1)
        s2 = [r for r in sp if r["papel"] == p]
        w2 = sum(float(r["peso"]) for r in s2)
        a2 = sum(float(r["peso"]) for r in s2 if r["resultado"] == "absolvição")
        n2 = sum(r["resultado"] == "absolvição" for r in s2)
        print(f"| {p.replace('_', ' ')} | {a1} de {len(s1)} ({pct(a1, len(s1))}) | {n2} de {len(s2)} ({pct(a2, w2)}) |")
    print("\nTJPA pela lista do DJEN\n")
    print("| Lista | Sentenças | Absolvições | pedidas pelo MP | sem pedido do MP |")
    print("| --- | --- | --- | --- | --- |")
    for l in ("1", "2"):
        s = [r for r in pa if den.get(r["numero"], {}).get("lista") == l]
        ab = [r for r in s if r["resultado"] == "absolvição"]
        m = sum(a[r["numero"]]["mp_absolvicao"] == "1" for r in ab)
        print(f"| {l} | {len(s)} | {len(ab)} ({pct(len(ab), len(s))}) | {m} ({pct(m, len(s))}) | {len(ab) - m} ({pct(len(ab) - m, len(s))}) |")
    print("\nTJPA: fundamento por posição do MP\n")
    c = Counter((r["fundamento"], r["mp_absolvicao"]) for r in A if r["tribunal"] == "TJPA")
    for (f, m), n in sorted(c.items(), key=lambda x: (-x[1], x[0])):
        print(f"- {f.replace('_', ' ')}, MP {'pediu a absolvição' if m == '1' else 'pediu a condenação' if m == '0' else 'não registrado'}: {n}")
    mist = Counter(r["fundamento"] for r in A if r["tribunal"] == "TJPA" and r["papel_denunciado"] == "misto")
    print(f"\nTJPA, mistos absolvidos por fundamento: {dict(mist)}")


def main():
    A = le(ARQ)
    if sys.argv[1:] != ["tabelas"]:
        erros = confere(A)
        if erros:
            sys.exit("\n".join(erros))
        print(f"{len(A)} absolvições codificadas (TJPA {sum(r['tribunal'] == 'TJPA' for r in A)}, "
              f"TJSP {sum(r['tribunal'] == 'TJSP' for r in A)}); conferência sem divergência\n")
    tabelas(A)


if __name__ == "__main__":
    main()
