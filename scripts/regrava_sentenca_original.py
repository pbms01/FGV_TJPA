"""Regrava em textos/tjsp/sentencas/ o texto integral de uma sentença que o Codex cortou em
100 mil caracteres, a partir do arquivo original baixado pelo link do Codex (fora do repo).

Uso (da raiz do repo): python3 scripts/regrava_sentenca_original.py NUMERO DOCUMENTO_ID ARQUIVO

Decisões que não saltam aos olhos:
- O texto do original substitui o do Codex no mesmo arquivo (01_<documento_id>.txt), com o
  marcador de procedência na primeira linha, como na primeira passada; a linha do manifesto
  (textos/tjsp/manifesto_sentencas.csv) é atualizada em procedência, chars, sha256 e lido_em.
- Só substitui se o texto novo contiver o início do antigo (salvo cabeçalho e espaços), para
  não trocar a peça por outra.
- A conversão é a de scripts/original_para_lote.py (RTF, PDF ou HTML).
"""
import csv
import datetime
import hashlib
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from original_para_lote import texto_pdf  # noqa: E402

BASE = os.path.join(os.path.dirname(__file__), "..")
MAN = os.path.join(BASE, "textos/tjsp/manifesto_sentencas.csv")


def norm(t):
    return re.sub(r"[\s|]+", "", t)


def main(numero, uid, arq):
    destino = os.path.join(BASE, "textos/tjsp/sentencas", numero, f"01_{uid}.txt")
    antigo = open(destino, encoding="utf-8").read()
    fonte, novo = texto_pdf(arq)
    novo = re.sub(r"[ \t]+\n", "\n", novo).strip() + "\n"
    trecho = norm(antigo.split("SENTENÇA", 1)[-1])[:400]
    if trecho not in norm(novo):
        sys.exit(f"{numero}: o original não contém o início do texto gravado; nada mudou")
    corpo = f"[{fonte}]\n\n{novo}"
    open(destino, "w", encoding="utf-8").write(corpo)
    linhas = list(csv.DictReader(open(MAN, encoding="utf-8")))
    for l in linhas:
        if l["numero"] == numero and l["documento_id"] == uid:
            l.update(procedencia=fonte, chars=str(len(corpo)),
                     sha256=hashlib.sha256(corpo.encode("utf-8")).hexdigest(),
                     lido_em=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00"))
    with open(MAN, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0]))
        w.writeheader()
        w.writerows(linhas)
    print(numero, fonte, len(antigo), "->", len(corpo))


if __name__ == "__main__":
    main(*sys.argv[1:4])
