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
 "C61": (r"22 de fevereiro de 2022", r"171, § 2º-A e § 4º", r"5 anos e 4 meses"),
 "C62": (r"11 de agosto de 2022", r"§ 4°-B e § 4°-C", r"4 \(quatro\) anos de reclusão"),
 "C63": (r"12 e 16 de janeiro de 2024", r"171, §4º, c\.c\. artigo 29", r"01 \(um\) ano, 07 \(sete\) meses"),
 "C64": (r"06 de janeiro de 2022", r"171, §4º, na forma do art\. 69", r"08 \(oito\) anos, 04"),
 "C65": (r"20 de março de 2023", r"parágrafo 2º-A e parágrafo 4º", r"171, § 2º, VII"),
 "C66": (r"04\.05\.2023", r"§§ 2º-A e 4º", r"171, § 2º, VII"),
 "C67": (r"11 de fevereiro de 2022", r"171, §2º-A", r"12 anos, 1 mês e 18 dias"),
 "C68": (r"27 de outubro de 2022", r"171, §2-A e §4º", r"caput.{0,3} c/c § 4º"),
 "C69": (r"26 de março de 2025", r"171, § 2º-A, c/c artigo 29", r"05 \(cinco\) anos de reclusão"),
 "C70": (r"11 de maio de 2023", r"171, § 2º-A", r"ABSOLVER a ré"),
 "C71": (r"28 de setembro de 2022", r"171, §2º-A c\.c artigo 29", r"ABSOLVER a corré"),
 "C72": (r"27 de fevereiro de 2025", r"171, § 2º-A e § 4º", r"ABSOLVO o réu"),
 "C73": (r"18 de novembro de 2022", r"171, caput e §4º", r"emendatio libelli"),
 "C74": (r"3 de fevereiro de 2023", r"155, §§ 4º-B e 4º-C", r"4 \(quatro\) anos de reclusão"),
 "C75": (r"28 de abril de 2023", r"155, § 4º, incisos II e IV", r"02 \(dois\) anos de reclusão"),
 "C76": (r"12 de junho de 2025", r"171, §2º-A e §3º", r"293, VI, §1º, I"),
 "C77": (r"2 de abril de 2022", r"171, §§ 2º-A", r"4 \(quatro\) anos de reclusão"),
 "C78": (r"16 de dezembro de 2021", r"155, §§ 4º-B", r"386, VII"),
 "C79": (r"18 de fevereiro de 2022", r"171, § 2º-A, combinado", r"04 \(quatro\) anos e 08 \(oito\) meses"),
 "C80": (r"17 de junho de 2024", r"304, c\.c\. artigo 299", r"02 \(DOIS\) ANOS E 04"),
 "C81": (r"13 de fevereiro de 2022", r"invadiu dispositivo informático", r"ABSOLVO o réu do deito previsto no artigo 154-A"),
 "C82": (r"03\.09\.2025", r"155, §4º-B", r"155, § 4º, II, do CP, às penas de 01"),
 "C83": (r"11 de julho de 2025", r"4º-B", r"2 anos, 2 meses e 20 dias"),
 "C84": (r"13 a 17 de janeiro de 2025", r"155, § 4º, II, c\.c\. artigo 61", r"3 \(três\) anos, 10"),
 "C85": (r"23 de janeiro de 2025", r"171, §2º-A e §4º", r"1 \(um\) ano 9 \(nove\) meses"),
 "C86": (r"12 de julho de 2023", r"171, caput, combinado com o artigo 14", r"171, §1º, c\.c\. artigo 14"),
 "C87": (r"27 de janeiro de 20", r"288, 171, §4º, 328 e 307", r"03 \(três\) anos de reclusão"),
 "C88": (r"15 de junho de 2022", r"fraude eletrônica", r"01 \(um\) mês e 05 \(cinco\) dias"),
 "C89": (r"13 de setembro de 2021", r"171, caput, c\.c\. artigo 29", r"1 \(um\) ano de reclusão"),
 "C90": (r"24 de novembro de 2021", r"171, §2º-A", r"1 ano, 6 meses e 20 dias"),
 "C91": (r"06 de julho de 2021", r"171, § 2o-A", r"um ano, dois meses e doze dias"),
 "C92": (r"16 de dezembro de 2021", r"fraude eletrônica", r"3 \(três\) anos e 4 \(quatro\) meses"),
 "C93": (r"26 de abril de 2024", r"154-A, §§ 3º e 4º", r"02 \(dois\) anos e 08 \(oito\) meses"),
 "C94": (r"26 de outubro de 2022", r"154-A, §§3º e 4º", r"386, inciso VII"),
 "C95": (r"05 de julho de 2023", r"155, §4º, II e § 4º-B", r"06 anos e 08 meses"),
 "C96": (r"22 de abril de 2025", r"155, §4º-B, c\.c artigo 14", r"2 \(dois\) anos e 8 \(oito\) meses"),
 "C97": (r"28 de janeiro de 2026", r"§ 4º-B, e § 4º-C, II", r"01 ano, 09 meses e 24 dias"),
 "C98": (r"23 de agosto de 2024", r"157, §2º-A, inciso I, e artigo 155, §4º-B", r"08 \(oito\) anos, 10"),
 "C99": (r"31 de outubro de 2024", r"155, §4º .B.", r"155, §4º, inciso II, por três vezes"),
 "C100": (r"12 de junho de 2024", r"155, § 4°-B, c\.c\. Artigo 71", r"386, inciso III"),
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
json.dump(res, (B / "conferencia3.json").open("w", encoding="utf-8"), ensure_ascii=False, indent=1)
for k, v in res.items():
    print(k, F[k]["processo"], {x: v.get(x) for x in ("achou", "data", "cap", "sol", "data_sent", "decisoes")})
