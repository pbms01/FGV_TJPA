"""Busca a íntegra de sentenças pela consulta por número da CJPG.

A pesquisa livre devolve o texto cortado perto de 50 mil caracteres; a consulta
por número devolve a sentença inteira na mesma div oculta. Grava um JSON por
processo em coleta/integra para que o fichamento leia do disco.
Uso: integra.py proc1 proc2 ...
"""
import json, sys, time, subprocess
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from cjpg import parse

OUT = Path(__file__).resolve().parents[1] / "integra"
UA = "Mozilla/5.0 (pesquisa academica; criminologia informatica)"

def url(p):
    num, foro = p[:15], p[-4:]
    return ("https://esaj.tjsp.jus.br/cjpg/pesquisar.do?conversationId=&dadosConsulta.pesquisaLivre="
            f"&tipoNumero=UNIFICADO&numeroDigitoAnoUnificado={num}&foroNumeroUnificado={foro}"
            f"&dadosConsulta.nuProcesso={p}&dadosConsulta.ordenacao=DESC")

for p in sys.argv[1:]:
    r = subprocess.run(["curl", "-s", "-L", "-m", "60", "-A", UA, url(p)], capture_output=True)
    page = r.stdout.decode("utf-8", errors="ignore")
    _, recs = parse(page)
    recs = [x for x in recs if x.get("processo") == p]
    if not recs:
        print(p, "SEM RESULTADO", len(page)); continue
    best = max(recs, key=lambda x: len(x.get("texto", "")))
    (OUT / f"{p}.json").write_text(json.dumps(best, ensure_ascii=False), encoding="utf-8")
    print(p, len(recs), "doc(s); maior texto:", len(best.get("texto", "")))
    time.sleep(1.5)
