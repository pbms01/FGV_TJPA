"""Extratos de leitura: abertura (capitulação e narrativa da denúncia) e dispositivo.

Uso: extrato.py <tag_da_consulta> [--max N] [--abertura 900] [--disp 500] [--so processo1,processo2]
Lê triagem/corpus.jsonl e triagem/triagem.csv; não acessa a rede.
"""
import json, csv, re, sys, argparse, unicodedata
from pathlib import Path
D = Path(__file__).resolve().parents[1] / "triagem"
RX_DISP = re.compile(r"(ante o exposto|diante do exposto|posto isso|isso posto|pelo exposto|em face do exposto|diante do quanto|por todo o exposto|face ao exposto|diante disso|ante o quanto)", re.I)


def limpa(s):
    s = s.replace("\r", "")
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n", s)
    return s.strip()


def extrato(t, nab, ndisp):
    i = t.lower().find("vistos")
    i = i if i >= 0 else 0
    ab = limpa(t[i:i + nab])
    ms = list(RX_DISP.finditer(t))
    j = ms[-1].start() if ms else max(0, len(t) - ndisp)
    disp = limpa(t[j:j + ndisp])
    return ab, disp


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("tag")
    ap.add_argument("--max", type=int, default=12)
    ap.add_argument("--abertura", type=int, default=900)
    ap.add_argument("--disp", type=int, default=500)
    ap.add_argument("--so", default="")
    ap.add_argument("--pular", default="")
    a = ap.parse_args()
    tri = {r["processo"]: r for r in csv.DictReader((D / "triagem.csv").open(encoding="utf-8"))}
    so = set(x for x in a.so.split(",") if x)
    pular = set(x for x in a.pular.split(",") if x)
    n = 0
    for line in (D / "corpus.jsonl").open(encoding="utf-8"):
        r = json.loads(line)
        p = r["processo"]
        if so and p not in so:
            continue
        if not so and (a.tag not in r["_tags"] or tri[p]["status"] != "ok" or p in pular):
            continue
        ab, disp = extrato(r["texto"], a.abertura, a.disp)
        tr = tri[p]
        print(f"=== {p} | {tr['comarca']} | {tr['data_sent']} | fato~{tr['data_fato_est']} | arts:{tr['arts_texto']} | sol:{tr['solucao']}")
        print("[AB]", ab)
        print("[DISP]", disp)
        n += 1
        if n >= a.max:
            break
