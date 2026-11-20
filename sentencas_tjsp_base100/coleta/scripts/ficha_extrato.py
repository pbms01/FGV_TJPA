"""Extrato para fichamento: abertura longa (narrativa), janela de tipificação e dispositivo."""
import json, re, sys
from pathlib import Path
D = Path(__file__).resolve().parents[1] / "triagem"
sys.path.insert(0, str(Path(__file__).parent))
from extrato import limpa, RX_DISP
RX_TIP = re.compile(r"da tipifica|adequa[cç][aã]o t[ií]pica|desclassific|emendatio|art(?:igo)?\.? 383|qualificadora|§\s*4º-B|§\s*2º-A|4º-B|2º-A|154-A", re.I)
procs = sys.argv[1].split(","); nab, nj, nd = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
for line in (D / "corpus.jsonl").open(encoding="utf-8"):
    r = json.loads(line)
    if not any(r["processo"].startswith(p) for p in procs): continue
    t = r["texto"]; i = max(t.lower().find("vistos"), 0)
    ms = list(RX_DISP.finditer(t)); jd = ms[-1].start() if ms else len(t) - nd
    ini_f = i + nab
    corpo = t[ini_f:jd]
    hits = [m.start() for m in RX_TIP.finditer(corpo)]
    jan = ""
    if hits:
        h = hits[-1] if len(hits) > 1 else hits[0]
        jan = limpa(corpo[max(0, h - nj // 2): h + nj // 2])
    print(f"=== {r['processo']} | {r.get('Comarca')} | {r.get('Vara')} | sent {r.get('Data de Disponibilização')} | {len(t)} chars")
    print("[AB]", limpa(t[i:i + nab])); print("[TIP]", jan or "(sem termo)"); print("[DISP]", limpa(t[jd:jd + nd]))
