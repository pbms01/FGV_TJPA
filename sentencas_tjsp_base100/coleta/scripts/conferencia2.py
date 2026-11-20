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
 "C31": (r"15 de junho de 2021", r"171, § 2º-A e § 4º", r"171, § 2º-A e § 4º"),
 "C32": (r"18 de setembro de 2\.?024", r"171, §4º", r"171, §4º"),
 "C33": (r"23 de novembro de 2021", r"171, parágrafo 2º-A", r"artigo 71"),
 "C34": (r"21 de outubro de 2021", r"171, §2º-A, e §4º", r"171, §2º-A, e §4º"),
 "C35": (r"08 de outubro de 2021", r"171, §2º-A", r"UM ANO DE RECLUSÃO"),
 "C36": (r"20 de dezembro de 2021", r"171, § 4º, c\.c\. artigo 29", r"171, § 4º, c\.c\. artigo 29"),
 "C37": (r"26 de outubro de 2023", r"4º-B e parágrafo 4º-C", r"PROCEDENTE EM PARTE"),
 "C38": (r"01 de agosto de 2022", r"171, § 2º-A", r"04 \(quatro\) anos"),
 "C39": (r"17 de julho de 2024", r"171, § 2º ?-A", r"ABSOLVO"),
 "C40": (r"08 de setembro de 2023", r"171, § 2º-A", r"171, § 2º-A"),
 "C41": (r"20 de dezembro de 2021", r"155, § 4º-B", r"386, inciso VII"),
 "C42": (r"07 de novembro de 2022", r"171, §2º-A", r"04 \(quatro\) anos e 08"),
 "C43": (r"16 de janeiro de 2023", r"154-A", r"386, inciso V"),
 "C44": (r"28 de dezembro de 2021", r"171, § 2°-A", r"04 \(quatro\) anos"),
 "C45": (r"13 de janeiro de 2022", r"171, caput, c\.c\. seu §2º-A", r"04 \(quatro\) anos"),
 "C46": (r"23 de maio de 2023", r"154-A", r"147-A"),
 "C47": (r"24 de agosto de 2024", r"154-A e 218-C", r"ABSOLVER"),
 "C48": (r"03 de novembro de 2022", r"155, § 4º-B", r"155, § 4º-B"),
 "C49": (r"04 de julho", r"155, § 4º-B e § 4º-C", r"PROCEDENTE"),
 "C50": (r"10 de junho de 2025", r"155, § 4º, II, IV e § 4º-B", r"155, § 4º, II, IV e § 4º-B"),
 "C51": (r"19 de abril de 2024", r"171, §4º", r"§§4ºB e C"),
 "C52": (r"26 de maio de 2022", r"171, § 2-A", r"171, “caput”"),
 "C53": (r"setembro de 2023", r"171, §2-A", r"por no mínimo quatro vezes"),
 "C54": (r"29 de setembro de 2022", r"171, §2°-A", r"171"),
 "C55": (r"09 de agosto de 2022", r"154-A, §3º", r"386, inc\. III"),
 "C56": (r"09 de novembro de 2023", r"154-A, § 3º e § 4º", r"154-A, combinado com o artigo 14"),
 "C57": (r"11 de abril de 2022", r"violação indevida de mecanismo de segurança", r"386, inc\. VII"),
 "C58": (r"08 de outubro de 2021", r"155, §4º-B e §4º-C", r"155, §4º-B e §4º-C"),
 "C59": (r"09 de junho de 2026", r"§ 4o-B", r"155, parágrafo 4o, incisos II e IV"),
 "C60": (r"10/02/2022", r"171, caput", r"155, § 4º-B"),
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
    res[cid] = {"achou": True, "data": bool(re.search(rdata, t)), "cap": bool(re.search(rcap, t[i:i + 4500])),
                "sol": bool(re.search(rsol, t[len(t) // 3:])), "data_sent": rec.get("Data de Disponibilização"),
                "url": url, "decisoes": outras}
    time.sleep(1.2)
json.dump(res, (B / "conferencia2.json").open("w", encoding="utf-8"), ensure_ascii=False, indent=1)
for k, v in res.items():
    print(k, F[k]["processo"], {x: v.get(x) for x in ("achou", "data", "cap", "sol", "data_sent", "decisoes")})
