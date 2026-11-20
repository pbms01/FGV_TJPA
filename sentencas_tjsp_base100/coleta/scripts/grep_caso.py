"""Trechos curtos de um caso: grep_caso.py <proc-prefixo> <regex> [antes] [depois] [max]."""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from extrato import limpa
p, rx = sys.argv[1], re.compile(sys.argv[2], re.I)
a, d, mx = (int(x) for x in (sys.argv[3:6] if len(sys.argv) > 5 else (150, 350, 4)))
for line in (Path(__file__).resolve().parents[1] / "triagem/corpus.jsonl").open(encoding="utf-8"):
    r = json.loads(line)
    if not r["processo"].startswith(p): continue
    t = r["texto"]; last = -10**6; n = 0
    for m in rx.finditer(t):
        if m.start() - last < a + d: continue
        last = m.start(); n += 1
        print(f"[{m.start()}/{len(t)}]", limpa(t[max(0, m.start() - a):m.start() + d]))
        if n >= mx: break
