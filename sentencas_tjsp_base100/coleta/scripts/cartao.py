"""Cartão curto de triagem: capitulação (início), trecho da narrativa e dispositivo."""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from extrato import limpa
D = Path(__file__).resolve().parents[1] / "triagem"
procs = sys.argv[1].split(","); ncap, nnar, ndisp = (int(x) for x in (sys.argv[2:5] if len(sys.argv) > 4 else (330, 480, 200)))
RXN = re.compile(r"Consta|Segundo (?:a denúncia|apurado|se apurou)|Narra|Apurou-se|porque|Conforme (?:apurado|narra)", re.I)
RXD = re.compile(r"(?i)julgo (?:procedente|parcialmente|improcedente|a ação|a denúncia)|absolvo |condeno ")
for line in (D / "corpus.jsonl").open(encoding="utf-8"):
    r = json.loads(line)
    if not any(r["processo"].startswith(p) for p in procs): continue
    t = r["texto"]; i = max(t.lower().find("vistos"), 0)
    m = RXN.search(t, i + 150); k = m.start() if m else i + ncap
    ds = list(RXD.finditer(t)); jd = ds[-1].start() if ds else len(t) - ndisp
    print(f"== {r['processo']} | {r.get('Comarca')} | {r.get('Data de Disponibilização')}")
    print("  CAP:", limpa(t[i + 7:i + ncap])); print("  NAR:", limpa(t[k:k + nnar])); print("  DSP:", limpa(t[jd:jd + ndisp]))
