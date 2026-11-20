"""Abertura curta + janela da fundamentação em torno de um termo + dispositivo curto."""
import json, re, sys
from pathlib import Path
D = Path(__file__).resolve().parents[1] / "triagem"
sys.path.insert(0, str(Path(__file__).parent))
from extrato import limpa, RX_DISP
procs = sys.argv[1].split(","); termo = re.compile(sys.argv[2], re.I)
nab, nj, nd = int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
for line in (D / "corpus.jsonl").open(encoding="utf-8"):
    r = json.loads(line)
    if not any(r["processo"].startswith(p) for p in procs): continue
    t = r["texto"]; i = max(t.lower().find("vistos"), 0)
    ms = list(RX_DISP.finditer(t)); jd = ms[-1].start() if ms else len(t) - nd
    corpo = t[i + 2500: jd]
    m = termo.search(corpo)
    jan = limpa(corpo[max(0, m.start() - nj // 2): m.start() + nj // 2]) if m else "(termo não encontrado)"
    print(f"=== {r['processo']} | {r.get('Comarca')} | {r.get('Data de Disponibilização')}")
    print("[AB]", limpa(t[i:i + nab])); print("[FUND]", jan); print("[DISP]", limpa(t[jd:jd + nd]))
