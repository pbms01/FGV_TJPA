"""Triagem local das sentenças baixadas da CJPG.

Decisões:
- Deduplica por número CNJ (a mesma sentença volta em várias consultas).
- Descarte barato pelo ano do número CNJ: processo iniciado antes de 2021
  não pode tratar de conduta posterior a 28/05/2021.
- Data do fato estimada como a data mais antiga do relatório (primeiros
  ~7.000 caracteres), excluídas datas em contexto de nascimento, recebimento da
  denúncia, audiência e publicação. É estimativa para ordenar a leitura; a data
  que vale é a conferida no fichamento.
- Família de conduta por pontuação de termos; a classificação final é humana.
- Solução lida no dispositivo (últimos ~5.000 caracteres).
"""
import json, re, csv, sys, unicodedata
from pathlib import Path
from datetime import date

RAW = Path(__file__).resolve().parents[1] / "raw"
OUT = Path(__file__).resolve().parents[1] / "triagem"
OUT.mkdir(exist_ok=True)
MARCO = date(2021, 5, 28)
MESES = {m: i for i, m in enumerate(["janeiro", "fevereiro", "marco", "abril", "maio", "junho", "julho",
                                      "agosto", "setembro", "outubro", "novembro", "dezembro"], 1)}


def norm(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


RX_DATA_EXT = re.compile(r"(\d{1,2})[º°o]?\s+de\s+(janeiro|fevereiro|marco|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro)\s+de\s+(\d{4})")
RX_DATA_NUM = re.compile(r"\b(\d{1,2})[/.](\d{1,2})[/.](\d{4})\b")
CTX_EXCL = re.compile(r"nascid|nasc\.|data de nasc|recebid|receb|audiencia|publica|disponibiliz|juntad|protocol|distribu|certid|portaria|decis|despach|intimad|citad|sentenca|preso em|prisao em|flagrante em|nº|n\.|lei|decreto|resolucao|tema|resp|hc ")

FAMILIAS = {
    "F01 falsa central": r"falsa central|central de atendimento|central de seguranca|funcionari[oa] do banco|setor de seguranca|se passando por (?:funcionari|atendente|gerente)",
    "F02 whatsapp/parente": r"whatsapp clonado|clonagem do whatsapp|whatsapp foi clonado|clonou o whatsapp|perfil falso|numero novo|trocou de numero|se passando por (?:seu|sua) (?:filh|sobrinh|net|irma)",
    "F03 link/pagina falsa": r"phishing|link falso|pagina falsa|site falso|link malicioso|clicou (?:no|em um) link|codigo de verificacao",
    "F04 acesso remoto/malware": r"acesso remoto|anydesk|teamviewer|programa malicioso|malware|aplicativo de acesso|espelhamento",
    "F05 chip/linha": r"sim swap|troca de chip|clonagem de chip|chip clonado|portabilidade|segunda via do chip|novo chip",
    "F06 conta rede social/email": r"instagram|facebook|conta de e-?mail|rede social|perfil da vitima|invadi(?:u|ram|da) a conta",
    "F07 aparelho em relacao pessoal": r"companheir|namorad|ex-?mulher|ex-?marido|violencia domestica|maria da penha|celular da vitima|aparelho da vitima",
    "F08 biometria/conta em nome": r"biometria|reconhecimento facial|prova de vida|selfie|abertura de conta|conta em nome da vitima|emprestimo consignado|emprestimo em nome",
    "F09 anuncio/investimento": r"anuncio falso|falso anuncio|marketplace|olx|falsa corretora|falso investimento|criptomoeda|investimento",
    "F10 insider/sistema": r"acesso privilegiado|sistema interno|credenciais de acesso|funcionari[oa] (?:da|do) (?:empresa|banco|loja) .{0,80}sistema|login e senha",
    "FIA uso de IA": r"inteligencia artificial|deepfake|voz sintetica|clonagem de voz|deep fake",
}
RX_FAM = {k: re.compile(v) for k, v in FAMILIAS.items()}

# Dispositivos: o token do parágrafo é procurado e validado pela proximidade do
# número do artigo, porque "§ 2º-A" também existe no art. 157 (arma de fogo).
TOK = {
    "154-A": (r"154\s*-\s*a\b", None),
    "155§4B": (r"\b4\s*o?\s*-\s*b\b", "155"),
    "155§4C": (r"\b4\s*o?\s*-\s*c\b", "155"),
    "171§2A": (r"\b2\s*o?\s*-\s*a\b", "171"),
    "155§4II": (r"155[^;]{0,40}4\s*o?,?\s*(?:inciso\s*)?ii\b", None),
    "288": (r"\b288\b", None),
    "orcrim": (r"12\.850", None),
    "lavagem": (r"9\.613", None),
}
RX_TOK = {k: (re.compile(a), b) for k, (a, b) in TOK.items()}


def arts(t):
    achou = []
    for k, (rx, art) in RX_TOK.items():
        for m in rx.finditer(t):
            if art is None or art in t[max(0, m.start() - 120): m.end() + 120]:
                achou.append(k); break
    if "171§2A" not in achou and "fraude eletronica" in t:
        achou.append("171§2A")
    return achou


SOL = {
    "procedente": r"julgo procedente|julgo totalmente procedente",
    "parcial": r"parcialmente procedente",
    "improcedente": r"julgo improcedente",
    "absolvo": r"absolvo|absolver",
    "condeno": r"condeno|condenar",
    "desclassifica": r"desclassific",
    "extincao": r"extinta a punibilidade|declaro extinta|extingo a punibilidade|julgo extinta",
    "386": r"386,?\s*(?:inciso\s*)?(i{1,3}|iv|v|vi{0,2}|vii)\b",
}
RX_SOL = {k: re.compile(v) for k, v in SOL.items()}


def datas_relatorio(t):
    ini = t.find("vistos")
    rel = t[max(ini, 0): max(ini, 0) + 7000]
    achadas = []
    for m in RX_DATA_EXT.finditer(rel):
        d, mes, a = int(m.group(1)), MESES[m.group(2)], int(m.group(3))
        achadas.append((m.start(), d, mes, a))
    for m in RX_DATA_NUM.finditer(rel):
        d, mes, a = int(m.group(1)), int(m.group(2)), int(m.group(3))
        achadas.append((m.start(), d, mes, a))
    validas = []
    for pos, d, mes, a in achadas:
        if not (2015 <= a <= 2026 and 1 <= mes <= 12 and 1 <= d <= 31):
            continue
        ctx = rel[max(0, pos - 60): pos]
        if CTX_EXCL.search(ctx):
            continue
        try:
            validas.append(date(a, mes, d))
        except ValueError:
            pass
    return sorted(validas)


def main():
    recs = {}
    for fn in sorted(RAW.glob("*.jsonl")):
        for line in fn.open(encoding="utf-8"):
            r = json.loads(line)
            p = r.get("processo")
            if not p or not r.get("texto"):
                continue
            tag = r["_consulta"].get("tag", fn.stem)
            if p in recs:
                recs[p]["_tags"].add(tag)
            else:
                r["_tags"] = {tag}
                recs[p] = r
    linhas = []
    for p, r in recs.items():
        t = norm(r["texto"])
        m = re.search(r"\.(\d{4})\.8\.26\.", p)
        ano_cnj = int(m.group(1)) if m else None
        ds = datas_relatorio(t)
        dfato = ds[0] if ds else None
        disp = t[-5000:]
        fam = {k: len(rx.findall(t)) for k, rx in RX_FAM.items()}
        fam_top = sorted([(v, k) for k, v in fam.items() if v], reverse=True)[:3]
        arts_txt = arts(t)
        arts_disp = arts(disp)
        sol = [k for k, rx in RX_SOL.items() if rx.search(disp)]
        if ano_cnj and ano_cnj < 2021:
            status = "descarte_cnj"
        elif dfato and dfato < MARCO:
            status = "fato_anterior?"
        elif dfato is None:
            status = "sem_data"
        else:
            status = "ok"
        linhas.append({
            "processo": p, "ano_cnj": ano_cnj, "data_fato_est": dfato.isoformat() if dfato else "",
            "status": status, "assunto": r.get("Assunto", ""), "comarca": r.get("Comarca", ""),
            "vara": r.get("Vara", ""), "data_sent": r.get("Data de Disponibilização", ""),
            "chars": len(r["texto"]), "tags": ";".join(sorted(r["_tags"])),
            "familias": "; ".join(f"{k}({v})" for v, k in fam_top),
            "arts_texto": ",".join(arts_txt), "arts_disp": ",".join(arts_disp), "solucao": ",".join(sol),
        })
    with (OUT / "triagem.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0].keys()))
        w.writeheader()
        w.writerows(linhas)
    # índice com texto para leitura posterior
    with (OUT / "corpus.jsonl").open("w", encoding="utf-8") as f:
        for p, r in recs.items():
            r = dict(r); r["_tags"] = sorted(r["_tags"])
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    from collections import Counter
    print("sentenças únicas:", len(linhas))
    print(Counter(l["status"] for l in linhas))


if __name__ == "__main__":
    main()
