#!/usr/bin/env python3
"""Censo, no DataJud, dos processos do TJSP com os três assuntos que nomeiam o tipo cibernético, para
coletar o máximo de denúncias (descrição da conduta e tipificação). Fase 1 do plano, revisão de 20/11/2026.

Assuntos (SGT versão 05/11/2026): 11978 Invasão de Dispositivo Informático (art. 154-A), 15623 Fraude
Eletrônica (art. 171, § 2º-A), 15755 Estelionato Mediante Cessão de Conta Laranja (art. 171, § 2º, VII).

Uso:
    python censo_denuncias_tjsp.py                 # grava censo_tjsp.jsonl e numeros_tjsp.csv
    python censo_denuncias_tjsp.py --so-consulta   # imprime a consulta de uma janela, sem rede

Decisões não óbvias:
- Censo, não amostra: o objetivo da fase é o máximo de denúncias. O tamanho da coleta é o do universo.
- Sem filtro de classe nem de grau: o registro de 2º grau traz a classe original sob o mesmo número
  (visto no Codex em 20/11/2026), e o inquérito pode seguir como ação penal sob o mesmo número (a conferir
  no censo). Filtrar por classe perderia denúncias; a consolidação por número decide qual registro serve.
- Só sigilo 0: o conector Codex não abre os sigilosos. Eles são contados à parte, como massa escura.
- Janelas mensais de ajuizamento, sem ordenação: o cluster recusa ordenar por _id (20/11/2026), o que
  impede o search_after; uma janela que passar do tamanho da página é partida ao meio e refeita.
- Movimentos vêm só com código, nome e data, para pesar pouco; servem para marcar se houve denúncia
  (nome do movimento com "denúncia") antes de gastar chamadas no Codex.
- Janela de cada código começa na vigência do tipo; processos anteriores ao código só o têm por
  reclassificação, o que é dado a medir.
- Resposta com shard falho é rejeitada (contagem parcial sem erro); retomada pelas janelas feitas.
"""
import argparse
import csv
import json
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sorteio_datajud_tjsp import CHAVE_PUBLICA, busca  # noqa: E402  (mesmo cliente e mesma regra de shard)

CODIGOS = {  # código: (tipo, início da vigência do tipo em yyyyMMddHHmmss)
    11978: ("invasao_dispositivo_154A", 20161119000000),
    15623: ("fraude_eletronica_171_2A", 20210528000000),
    15755: ("conta_laranja_171_2_VII", 20260504000000),
}
CAMPOS = ["numeroProcesso", "classe", "grau", "dataAjuizamento", "orgaoJulgador", "assuntos", "nivelSigilo",
          "movimentos.codigo", "movimentos.nome", "movimentos.dataHora"]
DENUNCIA = re.compile(r"den[úu]ncia", re.I)


def meses(inicio, fim):
    y, m = int(str(inicio)[:4]), int(str(inicio)[4:6])
    while int(f"{y}{m:02d}01000000") < fim:
        a = max(inicio, int(f"{y}{m:02d}01000000"))
        y2, m2 = (y + 1, 1) if m == 12 else (y, m + 1)
        yield f"{y}{m:02d}", a, min(fim, int(f"{y2}{m2:02d}01000000"))
        y, m = y2, m2


def consulta(codigo, inicio, fim, tamanho):
    return {"size": tamanho, "track_total_hits": True, "_source": CAMPOS,
            "query": {"bool": {"filter": [
                {"term": {"assuntos.codigo": codigo}},
                {"term": {"nivelSigilo": 0}},
                {"range": {"dataAjuizamento": {"gte": inicio, "lt": fim}}}]}}}


def janela(url, chave, codigo, i, f, a, out):
    d, motivo = busca(url, chave, consulta(codigo, i, f, a.pagina), a.tentativas, a.espera)
    if d is None:
        raise RuntimeError(motivo)
    if d["hits"]["total"]["value"] > a.pagina:
        meio = (i + f) // 2  # corte aritmético no inteiro yyyyMMddHHmmss: só precisa dividir a janela
        return janela(url, chave, codigo, i, meio, a, out) + janela(url, chave, codigo, meio, f, a, out)
    for h in d["hits"]["hits"]:
        out.write(json.dumps({"_codigo_censo": codigo, **h["_source"]}, ensure_ascii=False) + "\n")
    return len(d["hits"]["hits"])


def consolida(jsonl, saida):
    por = {}
    for linha in open(jsonl, encoding="utf-8"):
        r = json.loads(linha)
        n = r.get("numeroProcesso")
        p = por.setdefault(n, {"codigos": set(), "classes": set(), "graus": set(), "ajuizamento": None,
                               "orgao_g1": None, "denuncia": False, "data_denuncia": None, "registros": 0})
        p["registros"] += 1
        p["codigos"].add(r["_codigo_censo"])
        p["classes"].add(str((r.get("classe") or {}).get("codigo")))
        p["graus"].add(str(r.get("grau")))
        aj = str(r.get("dataAjuizamento") or "")[:8]
        p["ajuizamento"] = min(filter(None, [p["ajuizamento"], aj])) if aj else p["ajuizamento"]
        if r.get("grau") == "G1":
            p["orgao_g1"] = (r.get("orgaoJulgador") or {}).get("nome")
        for m in r.get("movimentos") or []:
            if DENUNCIA.search(str(m.get("nome", ""))):
                p["denuncia"] = True
                dh = str(m.get("dataHora") or "")[:10]
                p["data_denuncia"] = min(filter(None, [p["data_denuncia"], dh])) if dh else p["data_denuncia"]
    # ordem de trabalho: primeiro quem tem movimento de denúncia, depois ação penal sem esse movimento, depois o resto
    def prioridade(item):
        n, p = item
        acao = bool(p["classes"] & {"283", "10943"})
        return (0 if p["denuncia"] else 1 if acao else 2, p["ajuizamento"] or "")
    with open(saida, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["ordem", "numero", "codigos", "classes", "graus", "ajuizamento", "orgao_g1",
                    "movimento_denuncia", "data_primeira_denuncia", "registros"])
        for k, (n, p) in enumerate(sorted(por.items(), key=prioridade), 1):
            w.writerow([k, n, ";".join(map(str, sorted(p["codigos"]))), ";".join(sorted(p["classes"])),
                        ";".join(sorted(p["graus"])), p["ajuizamento"], p["orgao_g1"],
                        "sim" if p["denuncia"] else "não", p["data_denuncia"], p["registros"]])
    return len(por), sum(1 for p in por.values() if p["denuncia"])


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--tribunal", default="tjsp")
    ap.add_argument("--fim", type=int, default=int(time.strftime("%Y%m%d000000")))
    ap.add_argument("--pagina", type=int, default=2000)
    ap.add_argument("--saida", default="censo_tjsp.jsonl")
    ap.add_argument("--numeros", default="numeros_tjsp.csv")
    ap.add_argument("--tentativas", type=int, default=25)
    ap.add_argument("--espera", type=int, default=3)
    ap.add_argument("--chave", default=os.environ.get("DATAJUD_API_KEY", CHAVE_PUBLICA))
    ap.add_argument("--so-consulta", action="store_true")
    a = ap.parse_args()
    url = f"https://api-publica.datajud.cnj.jus.br/api_publica_{a.tribunal.lower()}/_search"
    if a.so_consulta:
        print(json.dumps({"endpoint": url, "exemplo_janela": consulta(15623, 20251001000000, 20251101000000, a.pagina)},
                         ensure_ascii=False, indent=2))
        return 0
    feitas_f = a.saida + ".feitas"
    feitas = set(open(feitas_f).read().split()) if os.path.exists(feitas_f) else set()
    with open(a.saida, "a", encoding="utf-8") as out:
        for codigo, (tipo, inicio) in CODIGOS.items():
            total = 0
            for rot, i, f in meses(inicio, a.fim):
                chave_janela = f"{codigo}_{rot}"
                if chave_janela in feitas:
                    continue
                k = janela(url, a.chave, codigo, i, f, a, out)
                out.flush()
                with open(feitas_f, "a") as ff:
                    ff.write(chave_janela + "\n")
                total += k
                print(f"{codigo} {rot}: {k}", flush=True)
            print(f"{codigo} ({tipo}): {total} registros nesta execução", flush=True)
    n, com_den = consolida(a.saida, a.numeros)
    print(f"{n} números distintos em {a.numeros}; {com_den} com movimento de denúncia")
    return 0


if __name__ == "__main__":
    sys.exit(main())
