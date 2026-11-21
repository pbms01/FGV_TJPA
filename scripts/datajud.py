# Cliente mínimo da API pública do DataJud para a coleta noturna.
# Decisões não óbvias:
# - resposta com shard falho é tratada como falha: o ES devolve contagem parcial sem erro
#   quando parte dos shards rejeita a busca, e isso já aconteceu no índice do TJPA (19/11/2026);
# - backoff linear e longo porque a rejeição vem de fila cheia no cluster, não de cota do cliente;
# - a chave é lida de DATAJUD_API_KEY e, na falta, usa a pública vigente em 19/11/2026.
import json, os, subprocess, time, sys

KEY = os.environ.get("DATAJUD_API_KEY") or "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
BASE = "https://api-publica.datajud.cnj.jus.br/api_publica_{}/_search"
LOG = "/home/claude/dados/datajud_log.jsonl"

def q(tribunal, body, tries=10, espera=8):
    url = BASE.format(tribunal.lower())
    ultimo = ""
    for i in range(tries):
        t0 = time.time()
        r = subprocess.run(["curl", "-sS", "-m", "180", url, "-X", "POST",
                            "-H", "Content-Type: application/json",
                            "-H", f"Authorization: APIKey {KEY}", "-d", json.dumps(body)],
                           capture_output=True, text=True)
        ultimo = r.stdout[:300] or r.stderr[:300]
        try:
            d = json.loads(r.stdout)
        except Exception:
            d = None
        ok = bool(d) and "error" not in d and d.get("_shards", {}).get("failed", 1) == 0
        with open(LOG, "a") as f:
            f.write(json.dumps({"t": time.strftime("%Y-%m-%dT%H:%M:%S"), "trib": tribunal, "ok": ok,
                                "seg": round(time.time() - t0, 1), "tentativa": i + 1,
                                "motivo": "" if ok else ultimo[:160]}) + "\n")
        if ok:
            return d
        time.sleep(espera * (i + 1))
    raise RuntimeError(f"{tribunal}: falhou após {tries} tentativas: {ultimo}")

def ano(a):
    # dataAjuizamento é numérico yyyyMMddHHmmss; data ISO no range não filtra e não dá erro
    return int(f"{a:04d}0101000000")
