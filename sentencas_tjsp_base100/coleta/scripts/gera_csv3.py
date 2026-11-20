"""Gera base/casos_c61_c100.csv (sem cabeçalho) na ordem de colunas da aba Casos."""
import csv, json, re
from pathlib import Path
B = Path(__file__).resolve().parents[1] / "base"
TIPOS = {
 "C61": "171 § 2º-A; 171 § 4º", "C62": "155 § 4º-B; 155 § 4º-C", "C63": "171 § 4º; 171 § 2º-A (omitido)",
 "C64": "171 § 4º; 171 § 2º-A (na fundamentação); orcrim", "C65": "171 § 2º-A; 171 § 2º, VII", "C66": "171 § 2º-A; 171 § 2º, VII; ANPP",
 "C67": "171 § 2º-A; orcrim", "C68": "171 § 2º-A; 171 caput", "C69": "171 § 2º-A", "C70": "171 § 2º-A; 155 § 4º-B (latente)",
 "C71": "171 § 2º-A; 155 § 4º-B (latente)", "C72": "171 § 2º-A", "C73": "171 caput; 171 § 2º-A; 155 § 4º-B (latente)",
 "C74": "155 § 4º-B; 155 § 4º-C; 171 § 2º-A", "C75": "155 § 4º, II; 155 § 4º-B (omitido)", "C76": "171 § 2º-A; 293, VI",
 "C77": "171 § 2º-A; 154-A (latente)", "C78": "155 § 4º-B; 154-A (latente)", "C79": "171 § 2º-A; 155 § 4º-B (latente)",
 "C80": "304; 299; 296; 154-A (latente)", "C81": "154-A; 129 § 13", "C82": "155 § 4º-B; 155 § 4º, II", "C83": "155 § 4º-B",
 "C84": "155 § 4º, II", "C85": "171 § 2º-A", "C86": "171 § 1º; 304", "C87": "171 § 4º; 288; 328", "C88": "155 § 4º-B; 349",
 "C89": "171 caput; 171 § 2º-A (omitido)", "C90": "171 § 2º-A; 171 caput", "C91": "171 § 2º-A; 171 caput",
 "C92": "171 § 2º-A; art. 29, § 1º", "C93": "154-A §§ 3º e 4º", "C94": "154-A §§ 3º e 4º", "C95": "155 § 4º-B; 171 § 2º-A",
 "C96": "155 § 4º-B tentado; 154-A (latente)", "C97": "155 § 4º-B; 155 § 4º, II", "C98": "155 § 4º-B; 157",
 "C99": "155 § 4º-B; 155 § 4º, II", "C100": "155 § 4º-B",
}
PROVA = {
 "C69": "extração de celulares e confissão do operador da conversa", "C70": "extratos e dados cadastrais das contas",
 "C73": "interceptação telefônica e relatório de medida cautelar (roteiro de instalação do RustDesk)",
 "C81": "palavra da vítima, sem perícia no aparelho", "C87": "rastreamento de IP e linhas; reconhecimento pela vítima",
 "C94": "sem perícia; registros técnicos juntados após a instrução", "C96": "flagrante com o notebook do banco e relatório interno",
}
def dt(s):
    m = re.fullmatch(r"(\d{2})/(\d{2})/(\d{4})", s.strip())
    return f"{m[3]}-{m[2]}-{m[1]}" if m else s
def tx(s):
    s = (s or "").strip()
    if s == "-": return ""
    return "'" + s if s and s[0] in "=+-@" else s
def link(p):
    return ("https://esaj.tjsp.jus.br/cjpg/pesquisar.do?conversationId=&dadosConsulta.pesquisaLivre=&tipoNumero=UNIFICADO"
            f"&numeroDigitoAnoUnificado={p[:15]}&foroNumeroUnificado={p[-4:]}&dadosConsulta.nuProcesso={p}&dadosConsulta.ordenacao=DESC")
F = [json.loads(l) for l in (B / "fichas.jsonl").open(encoding="utf-8")]
with (B / "casos_c61_c100.csv").open("w", encoding="utf-8", newline="") as o:
    w = csv.writer(o)
    for f in F:
        if int(f["id"][1:]) < 61: continue
        w.writerow([f["id"], f["familia"], tx(f["canal_pretexto"]), tx(f["quem_executou"]), tx(f["capitulacao_denuncia"]), tx(f["solucao"]),
                    tx(f["convergencia"]), tx(f["ponto_analise"]), TIPOS[f["id"]], f["processo"], f["orgao"], dt(f["data_decisao"]),
                    dt(f["data_fato"]), tx(f["obtido_da_vitima"]), tx(f["acesso_dispositivo_conta"]), tx(f["trajeto_dinheiro"]),
                    tx(f["valor"]), tx(f["vitima_vulneravel"]), tx(f["fundamento"]), tx(f["pena"]), tx(PROVA.get(f["id"], f.get("prova", ""))),
                    f["fonte"], link(f["processo"])])
print("ok")
