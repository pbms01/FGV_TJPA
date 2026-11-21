"""Grava o texto de acórdãos lidos pelo Codex e imprime os trechos sobre a Lei 15.397/2026.

Uso: python3 scripts/grava_acordao.py ARQUIVO_DO_BATCH NUMERO [recursos]
Com "recursos", grava em textos/tjsp/recursos/ (razões de apelação) em vez de acordaos/.
Grava cada documento distinto do batch em textos/tjsp/acordaos/<numero>/NN_<id>.txt, sem a
linha "Original:" (o link traz token), acrescenta ao manifesto textos/tjsp/manifesto_acordaos.csv
e imprime ementa, dispositivo e os trechos que citam o inciso VII ou a lei nova.
"""
import csv
import json
import os
import re
import sys

BASE = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.dirname(__file__))
import resultado_sentenca as rs  # noqa: E402  (mesma regex de menção à lei nova)

RE_BLOCO = re.compile(r"^--- (.+?) ---\nOriginal: \S*/doc/[^/]+/([0-9a-f-]{36})\S*\n", re.M)


def blocos(bruto):
    if bruto.lstrip().startswith("["):  # saída persistida como JSON de blocos de texto
        bruto = "".join(b.get("text", "") for b in json.loads(bruto))
    ms = list(RE_BLOCO.finditer(bruto))
    vistos = {}
    for i, m in enumerate(ms):
        fim = ms[i + 1].start() if i + 1 < len(ms) else len(bruto)
        texto = bruto[m.end():fim]
        texto = texto.split("\nAo responder, cite as pecas")[0]
        vistos.setdefault(m.group(2), (m.group(1), texto.strip()))
    return vistos


def main():
    arq, num = sys.argv[1], sys.argv[2]
    tipo = sys.argv[3] if len(sys.argv) > 3 else "acordaos"
    docs = blocos(open(arq, encoding="utf-8").read())
    pasta = os.path.join(BASE, "textos/tjsp", tipo, num)
    os.makedirs(pasta, exist_ok=True)
    man = os.path.join(BASE, f"textos/tjsp/manifesto_{tipo}.csv")
    novo = not os.path.exists(man)
    with open(man, "a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        if novo:
            w.writerow(["numero", "parte", "documento_id", "nome", "chars"])
        for i, (did, (nome, texto)) in enumerate(docs.items(), 1):
            open(os.path.join(pasta, f"{i:02d}_{did}.txt"), "w", encoding="utf-8").write(texto + "\n")
            w.writerow([num, i, did, nome, len(texto)])
            print(f"gravado {i:02d}_{did} ({len(texto)} chars)")
    t = re.sub(r"\s+", " ", " ".join(x[1] for x in docs.values()))
    if tipo != "acordaos":
        print(t)
        return
    e = re.search(r"(?i)ementa", t)
    print("\nEMENTA:", t[e.start():e.start() + 1500] if e else t[:1200])
    ultimos = list(re.finditer(r"(?i)(negaram|deram|deu|negou|nega-se|dá-se) (parcial )?provimento|conheceram", t))
    if ultimos:
        k = ultimos[-1].start()
        print("\nDISPOSITIVO:", t[max(0, k - 300):k + 500])
    vistos = -10**9
    for m in rs.RE_LEI_NOVA.finditer(t):
        if m.start() - vistos < 600:
            continue
        vistos = m.start()
        print("\nLEI NOVA >", t[max(0, m.start() - 700):m.end() + 700])


if __name__ == "__main__":
    main()
