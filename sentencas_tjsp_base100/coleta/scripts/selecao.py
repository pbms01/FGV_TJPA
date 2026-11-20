"""Seleciona até N por família na fila, metade com sinal de divergência.
Sinal de divergência: solução com absolvição/desclassificação/extinção, ou tipo da
abertura ausente do dispositivo. Ordena por tamanho (sentença mais longa tende a
fundamentar a capitulação)."""
import csv, json, sys
from pathlib import Path
D = Path(__file__).resolve().parents[1] / "triagem"
MAP = {"154A": "154-A", "155B": "155§4B", "171A": "171§2A"}
def diverge(r):
    s = r["sol"]
    if any(x in s for x in ("absolvo", "desclassifica", "extincao", "improcedente")):
        return True
    for t in r["tipos_ab"].split("+"):
        if t in MAP and MAP[t] not in r["arts_disp"]:
            return True
    return False
fam, n = sys.argv[1], int(sys.argv[2])
L = [r for r in csv.DictReader((D / "fila.csv").open(encoding="utf-8")) if r["fam"].split("/")[0] == fam]
L.sort(key=lambda r: -int(r["chars"]))
dv = [r for r in L if diverge(r)][: (n + 1) // 2]
cv = [r for r in L if not diverge(r)][: n - len(dv)]
print(",".join(r["processo"] for r in dv + cv))
