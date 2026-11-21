"""Estatísticas de Fraude no Pix (MED) do Banco Central, mensais, pela API Olinda de dados abertos.

Medida externa à classificação policial: transações Pix contestadas pelo pagador no Mecanismo
Especial de Devolução. Não separa o golpe em que a vítima transfere (estelionato) da transação
feita por terceiro com acesso à conta (furto mediante fraude eletrônica): mede a soma das duas no
Pix, e depende das regras do MED (MED 2.0 obrigatório desde 02/02/2026).

Decisão não óbvia: o parâmetro Database da função EstatisticasFraudesPix funciona como mês inicial;
com '202001' a API devolve a série inteira disponível (de 202201 em diante, conferido em 21/11/2026).
Uso, da raiz do repo: python3 scripts/estatisticas_bcb_pix.py
Grava dados/estatisticas/bcb_fraudes_pix_mensal.csv e imprime os totais anuais.
"""
import csv
import json
import pathlib
import urllib.request

URL = ("https://olinda.bcb.gov.br/olinda/servico/Pix_DadosAbertos/versao/v1/odata/"
       "EstatisticasFraudesPix(Database=@Database)?@Database='202001'&$format=json")
SAIDA = pathlib.Path("dados/estatisticas/bcb_fraudes_pix_mensal.csv")


def main():
    with urllib.request.urlopen(URL, timeout=120) as r:
        valores = json.load(r)["value"]
    valores.sort(key=lambda x: x["AnoMes"])
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    with open(SAIDA, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(valores[0].keys()))
        w.writeheader()
        w.writerows(valores)
    anos = {}
    for v in valores:
        a = anos.setdefault(v["AnoMes"] // 100, [0, 0, 0])
        a[0] += 1
        a[1] += v["Qtdecontestacoesaceitas"]
        a[2] += v["ValorPixcontestadosaceitos"]
    print(f"{len(valores)} meses, de {valores[0]['AnoMes']} a {valores[-1]['AnoMes']}")
    for ano, (meses, qtd, valor) in sorted(anos.items()):
        print(f"{ano}: {meses} meses, {int(qtd):,} contestações aceitas, R$ {valor / 1e9:.2f} bi")


if __name__ == "__main__":
    main()
