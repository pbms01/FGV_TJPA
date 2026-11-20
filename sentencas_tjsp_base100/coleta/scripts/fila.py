"""Fila de leitura: filtra pela capitulação e pela narrativa da abertura da sentença.

Decisão: a família de conduta é atribuída pelos termos da narrativa acusatória
(primeiros ~3.500 caracteres depois de "Vistos"), e não pelo texto inteiro, porque a
fundamentação cita precedentes e alegações que falam de outros golpes.
Entra na fila quem tem, na abertura, art. 154-A, 155 ou 171 e algum marcador digital.
"""
import json, csv, re, unicodedata
from pathlib import Path
from collections import Counter, defaultdict
D = Path(__file__).resolve().parents[1] / "triagem"


def norm(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


DIG = re.compile(r"pix|transferenc|aplicativo|app\b|internet|whatsapp|link|senha|token|conta (?:bancaria|digital)|celular|e-?mail|instagram|facebook|online|on-line|site|eletronic|informatic|biometria|selfie|chip|remoto|cartao")
CAP = re.compile(r"154\s*-\s*a|\b155\b|\b171\b")
FAM = {
    "F01": r"falsa central|central de atendimento|central de seguranca|(?:funcionari|atendente|preposto|gerente)[oa]?s? (?:do|de) (?:banco|instituicao)|se passando por (?:funcionari|atendente|gerente)|setor de (?:seguranca|fraude)",
    "F02": r"whatsapp clonad|clonagem (?:do|de) whatsapp|perfil falso|se passando por (?:seu|sua|um|uma)? ?(?:filh|sobrinh|net|irma|pai|mae|amig|parente)|numero novo",
    "F03": r"phishing|link|pagina falsa|site falso|codigo de (?:verificacao|seguranca|acesso)|sms",
    "F04": r"acesso remoto|anydesk|teamviewer|programa malicioso|malware|espelhamento|aplicativo de acesso|instalar (?:um )?aplicativo",
    "F05": r"troca de chip|chip|portabilidade|linha telefonica",
    "F06": r"instagram|facebook|rede social|conta de e-?mail|perfil",
    "F07": r"companheir|namorad|ex-?mulher|ex-?marido|violencia domestica|11\.340",
    "F08": r"biometria|reconhecimento facial|prova de vida|selfie|abertura de conta|emprestimo|consignado",
    "F09": r"anuncio|marketplace|olx|corretora|investimento|criptomoed|venda (?:de|do|da) ",
    "F10": r"acesso privilegiado|sistema interno|credenciais|login e senha|funcionari[oa] da empresa|empregad[oa]",
    "FIA": r"inteligencia artificial|deepfake|deep fake|voz sintetica|clonagem de voz",
}
RXF = {k: re.compile(v) for k, v in FAM.items()}


def tipos(ab):
    t = []
    if re.search(r"154\s*-\s*a", ab): t.append("154A")
    if re.search(r"\b4\s*o?\s*-\s*b\b", ab): t.append("155B")
    elif re.search(r"\b155\b", ab): t.append("155")
    if re.search(r"\b2\s*o?\s*-\s*a\b", ab) and "171" in ab: t.append("171A")
    elif re.search(r"\b171\b", ab): t.append("171")
    return t


if __name__ == "__main__":
    tri = {r["processo"]: r for r in csv.DictReader((D / "triagem.csv").open(encoding="utf-8"))}
    out = []
    for line in (D / "corpus.jsonl").open(encoding="utf-8"):
        r = json.loads(line)
        p = r["processo"]
        if tri[p]["status"] != "ok":
            continue
        t = norm(r["texto"])
        i = t.find("vistos")
        i = i if i >= 0 else 0
        ab = t[i:i + 1200]
        narr = t[i:i + 3500]
        if not CAP.search(ab) or not DIG.search(narr):
            continue
        tp = tipos(ab)
        if not tp:
            continue
        fam = {k: len(rx.findall(narr)) for k, rx in RXF.items()}
        top = [k for k, v in sorted(fam.items(), key=lambda x: -x[1]) if v][:2]
        out.append({"processo": p, "fato": tri[p]["data_fato_est"], "comarca": tri[p]["comarca"][:18],
                    "tipos_ab": "+".join(tp), "fam": "/".join(top) or "-", "sol": tri[p]["solucao"],
                    "arts_disp": tri[p]["arts_disp"], "chars": tri[p]["chars"]})
    with (D / "fila.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader(); w.writerows(out)
    print("na fila:", len(out))
    print("por tipo na abertura:", Counter(o["tipos_ab"] for o in out).most_common(10))
    c = Counter(o["fam"].split("/")[0] for o in out)
    print("por família principal:", sorted(c.items()))
