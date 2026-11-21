"""Baixa as fontes externas das séries de estelionato eletrônico para dados/bruto/ (fora do git).

Fontes:
- planilhas do Anuário Brasileiro de Segurança Pública (FBSP), 17ª a 20ª edições, pelo repositório
  DSpace do FBSP (os UUIDs dos bitstreams foram lidos pela API /server/api/core/items/<item>/bundles
  em 21/11/2026);
- versão web do artigo de Silva, Ramos e Reis Netto (2026), Revista Tópicos, cuja Tabela 1 traz o
  censo da SIAC/SEGUP-PA (o PDF corta a tabela, por isso se lê o HTML).

As planilhas e o artigo não vão para o repositório, pela regra de gravar só o que foi lido; o que se
leu deles fica em dados/estatisticas/. Uso, da raiz do repo: python3 scripts/estatisticas_baixa.py
"""
import pathlib
import urllib.request

BRUTO = pathlib.Path("dados/bruto")
FBSP = "https://publicacoes.forumseguranca.org.br/bitstreams/{}/download"
ANUARIOS = {  # arquivo local: (bitstream, item da edição)
    "anuario2023.xlsx": ("4e602f08-0d9f-44db-9eb7-cfeb82c0f113", "721e3396-1a66-4ff6-8ceb-ea319684a57a"),  # 17ª
    "anuario2024.xlsx": ("8d67098f-1319-4d84-b57c-fb3246a5f66f", "f62c4196-561d-452d-a2a8-9d33d1163af0"),  # 18ª
    "anuario2025.xlsx": ("a64087c0-e7f5-419d-b0f3-08c55faca5b1", "c3605778-37b3-4ad6-8239-94e4cb236444"),  # 19ª
    "anuario2026.xlsx": ("f659572d-8a06-431e-99ab-95448ca88c58", "bb542342-3cf8-47a5-a51d-a0eb911914b9"),  # 20ª
}
ARTIGO_PA = ("https://revistatopicos.com.br/artigos/caracterizacao-dos-crimes-patrimoniais-"
             "praticados-por-meio-cibernetico-no-estado-do-para-de-2022-a-2025?noblockage")


def baixa(url, destino):
    destino.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (pesquisa FGV_TJPA)"})
    with urllib.request.urlopen(req, timeout=180) as r:
        destino.write_bytes(r.read())
    print(f"{destino}  {destino.stat().st_size:,} bytes")


def main():
    for nome, (bitstream, _item) in ANUARIOS.items():
        baixa(FBSP.format(bitstream), BRUTO / "anuario" / nome)
    baixa(ARTIGO_PA, BRUTO / "para" / "artigo_revista_topicos.html")


if __name__ == "__main__":
    main()
