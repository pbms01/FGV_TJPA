"""Acrescenta fichas (lista JSON em stdin) a base/fichas.jsonl, substituindo pelo id."""
import json, sys
from pathlib import Path
fn = Path(__file__).resolve().parents[1] / "base" / "fichas.jsonl"
atuais = {}
if fn.exists():
    for l in fn.open(encoding="utf-8"):
        f = json.loads(l); atuais[f["id"]] = f
for f in json.load(sys.stdin):
    atuais[f["id"]] = f
with fn.open("w", encoding="utf-8") as out:
    for k in sorted(atuais, key=lambda k: int(k[1:])):
        out.write(json.dumps(atuais[k], ensure_ascii=False) + "\n")
print("fichas:", len(atuais))
