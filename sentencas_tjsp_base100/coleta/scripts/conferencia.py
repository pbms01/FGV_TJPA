"""Conferência das fichas contra a fonte: rebusca cada sentença na CJPG pelo número
(não usa o corpus local) e verifica data do fato, capitulação na abertura e solução
no dispositivo, por padrões definidos por caso."""
import json, re, sys, time, requests
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from cjpg import parse
from extrato import RX_DISP
B = Path(__file__).resolve().parents[1] / "base"
# id: (regex data do fato, regex capitulação na abertura, regex solução no dispositivo)
E = {
 "C01": (r"21 de julho de 2023", r"171, ?§ ?2[°º]-A", r"171, § 2º-A e §4º"),
 "C02": (r"03 de fevereiro de 2022", r"155, §4º, incisos II e IV", r"171, caput e §§2ºA e 4º"),
 "C03": (r"05 de junho de 2024", r"171, § 2º-A e § 4º", r"ABSOLVER a acusada.{0,200}386, inciso VII"),
 "C04": (r"07 de março de 2022", r"171, caput", r"383 e 387"),
 "C05": (r"06 de julho de 2023", r"171, §2° e §4°", r"171, caput, c\.c\. seu §2º-A e §4°"),
 "C06": (r"5 de agosto de 2026", r"171, § 2º-A, na forma do artigo 71", r"171, § 2º-A, na fo"),
 "C07": (r"17 de dezembro de 2021", r"171, §2º-A", r"DESCLASSIFICAR.{0,200}171, \"caput\""),
 "C08": (r"6 de novembro de 2022", r"171, caput e § 2º-A", r"por duas vezes"),
 "C09": (r"17 de janeiro de 2025", r"171, § 2º-A, na forma do § 4º", r"CONDENO a acusada"),
 "C10": (r"09 de novembro de 2022", r"171, § 2º-A", r"171, § 2º, inciso VII"),
 "C11": (r"05 de janeiro de 2023", r"171, parágrafo 2º-A", r"155, parágrafo 4º-B"),
 "C12": (r"11 de junho de 2025", r"158, §1º", r"158, §1º.{0,40}14, II"),
 "C13": (r"30 de novembro de 2021", r"155, § 4º-B", r"CONDENAR o réu WESLEY"),
 "C14": (r"7/9/2022", r"154-A, § 3º", r"386, III.{0,120}154-A, § 3º"),
 "C15": (r"23 de dezembro de 2021", r"154-A e 171, §2º-A", r"154-A e 171, §2º-A"),
 "C16": (r"16 de novembro de 2021", r"154-A, § 3º", r"154-A, § 3º"),
 "C17": (r"26 de junho de 2026", r"154-A, caput", r"386, incisos V e VII"),
 "C18": (r"27 de setembro de 2021", r"154-A", r"incisos III e VII do art\. 386"),
 "C19": (r"17 de outubro de 2024", r"155, § 4º-B", r"CONDENAR o réu NICOLAS"),
 "C20": (r"setembro de 2024", r"155, §4º, incisos II e IV, § 4º-B e §4º-C", r"155, §4º, incisos II e IV, § 4º-B e §4º-C"),
 "C21": (r"29 de maio e 4 de junho de 2024", r"171, § 2º-A, por três vezes", r"155, § 4º-B, por três vezes"),
 "C23": (r"22 de outubro de 2021", r"171, § 2º-A", r"01 \(um\) ano, 04 \(quatro\) meses"),
 "C24": (r"26 de agosto de 2023", r"171, §2°-A", r"171, §2º-A"),
 "C25": (r"07 de setembro de 2023", r"154-A, § 2º", r"154-A, §2º"),
 "C26": (r"16/05/2023", r"mediante violação indevida de mecanismo de segurança", r"386, III"),
 "C28": (r"23 de janeiro de 2023", r"155, §4º-B, c/c §4º-C", r"PROCEDENTE em parte"),
 "C29": (r"08 de abril de 2024", r"155, § 4º-B, c\.c o artigo 71", r"155, § 4º-B, c\.c o artigo 71"),
 "C30": (r"08 de dezembro de 2023", r"155, § 4º-B, c\.c artigo 71", r"155, § 4º, inciso II"),
}
F = {json.loads(l)["id"]: json.loads(l) for l in (B / "fichas.jsonl").open(encoding="utf-8")}
res = {}
for cid, (rdata, rcap, rsol) in E.items():
    p = F[cid]["processo"]
    url = ("https://esaj.tjsp.jus.br/cjpg/pesquisar.do?conversationId=&dadosConsulta.pesquisaLivre=&tipoNumero=UNIFICADO"
           f"&numeroDigitoAnoUnificado={p[:15]}&foroNumeroUnificado={p[-4:]}&dadosConsulta.nuProcesso={p}&dadosConsulta.ordenacao=DESC")
    try:
        r = requests.get(url, timeout=60); r.encoding = "utf-8"
        tot, recs = parse(r.text)
    except Exception as e:
        res[cid] = {"erro": str(e)}; continue
    mesmos = [x for x in recs if x.get("processo") == p]
    outras = [(x.get("Data de Disponibilização"), len(x.get("texto", ""))) for x in mesmos]
    alvo_data = F[cid]["data_decisao"]
    rec = next((x for x in mesmos if x.get("Data de Disponibilização") == alvo_data and x.get("texto")), None)
    if not rec:
        res[cid] = {"achou": False, "decisoes": outras}; continue
    t = re.sub(r"\s+", " ", rec["texto"])
    i = max(t.lower().find("vistos"), 0)
    ms = list(RX_DISP.finditer(t)); jd = ms[-1].start() if ms else len(t) - 3000
    res[cid] = {"achou": True, "data": bool(re.search(rdata, t)), "cap": bool(re.search(rcap, t[i:i + 3500])),
                "sol": bool(re.search(rsol, t[jd - 300:])), "data_sent": rec.get("Data de Disponibilização"),
                "url": url, "decisoes": outras}
    time.sleep(1.2)
json.dump(res, (B / "conferencia.json").open("w", encoding="utf-8"), ensure_ascii=False, indent=1)
for k, v in res.items():
    print(k, F[k]["processo"], {x: v.get(x) for x in ("achou", "data", "cap", "sol", "data_sent", "decisoes")})
