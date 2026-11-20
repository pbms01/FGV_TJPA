"""Coletor da Consulta de Julgados de 1º Grau (CJPG) do TJSP.

Decisões de arquitetura:
- A CJPG guarda a consulta na sessão do servidor; a paginação (trocarDePagina.do)
  só funciona com o mesmo cookie da pesquisa inicial, por isso cada consulta usa
  uma requests.Session própria.
- O texto integral vem embutido na página de resultados (div oculta), então não
  há segunda requisição por sentença: uma página = 10 sentenças inteiras.
- Cada consulta grava JSONL bruto em coleta/raw; triagem e fichamento leem
  dali, nunca da rede, para que tudo seja reprodutível e auditável.
- Intervalo de datas limitado a 1 ano pelo próprio tribunal.
"""
import argparse, json, re, sys, time, hashlib, html as htmlmod
from pathlib import Path
import requests
from bs4 import BeautifulSoup

BASE = "https://esaj.tjsp.jus.br/cjpg"
UA = {"User-Agent": "Mozilla/5.0 (pesquisa academica; criminologia informatica)"}


def parse(page_html):
    soup = BeautifulSoup(page_html, "html.parser")
    total = None
    m = re.search(r"Resultados\s*<strong>\s*[\d.]+\s*a\s*[\d.]+\s*</strong>\s*de\s*([\d.]+)", page_html)
    if m:
        total = int(m.group(1).replace(".", ""))
    out = []
    for tr in soup.select("tr.fundocinza1"):
        rec = {}
        a = tr.find("a", attrs={"title": "Visualizar Inteiro Teor"})
        if a:
            rec["processo"] = a.get_text(strip=True)
            rec["cdDoc"] = a.get("name")
        for row in tr.select("tr.fonte"):
            st = row.find("strong")
            if st:
                k = st.get_text(strip=True).rstrip(":")
                v = row.get_text(" ", strip=True)[len(st.get_text(strip=True)):].strip()
                rec[k] = v
        divs = tr.find_all("div", attrs={"align": "justify"})
        if divs:
            # get_text("") preserva as quebras originais do texto pré-formatado;
            # separador "\n" partia os termos destacados pela busca (ex.: 154-A).
            for br in divs[-1].find_all("br"):
                br.replace_with("\n")
            full = divs[-1].get_text("")
            rec["texto"] = re.sub(r"\n\s*\n+", "\n\n", full).strip()
        out.append(rec)
    return total, out


def consulta(q, dt_ini=None, dt_fim=None, classe=None, paginas=1, pausa=1.5):
    s = requests.Session()
    s.headers.update(UA)
    params = {
        "dadosConsulta.pesquisaLivre": q,
        "tipoNumero": "UNIFICADO",
        "dadosConsulta.ordenacao": "DESC",
        "classeTreeSelection.values": classe or "",
        "assuntoTreeSelection.values": "",
        "varasTreeSelection.values": "",
        "dadosConsulta.dtInicio": dt_ini or "",
        "dadosConsulta.dtFim": dt_fim or "",
    }
    r = s.get(f"{BASE}/pesquisar.do", params=params, timeout=60)
    r.encoding = "utf-8"
    total, recs = parse(r.text)
    if total is None and "no máximo 1 ano" in r.text:
        raise SystemExit("intervalo de datas acima de 1 ano")
    todos = recs
    for p in range(2, paginas + 1):
        if total is not None and (p - 1) * 10 >= total:
            break
        time.sleep(pausa)
        r = s.get(f"{BASE}/trocarDePagina.do", params={"pagina": p, "conversationId": ""}, timeout=60)
        r.encoding = "utf-8"
        _, recs = parse(r.text)
        if not recs:
            break
        todos += recs
    return total, todos


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("q")
    ap.add_argument("--ini")
    ap.add_argument("--fim")
    ap.add_argument("--classe")
    ap.add_argument("--paginas", type=int, default=1)
    ap.add_argument("--tag", required=True)
    a = ap.parse_args()
    total, recs = consulta(a.q, a.ini, a.fim, a.classe, a.paginas)
    outdir = Path(__file__).resolve().parents[1] / "raw"
    outdir.mkdir(exist_ok=True)
    fn = outdir / f"{a.tag}.jsonl"
    with fn.open("w", encoding="utf-8") as f:
        for r in recs:
            r["_consulta"] = {"q": a.q, "ini": a.ini, "fim": a.fim, "classe": a.classe, "total": total}
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"{a.tag}: total={total} baixados={len(recs)} -> {fn.name}")
    for r in recs[:10]:
        print(" ", r.get("processo"), "|", r.get("Classe"), "|", r.get("Assunto"), "|", r.get("Comarca"), "|", r.get("Data de Disponibilização"), "| chars", len(r.get("texto", "")))
