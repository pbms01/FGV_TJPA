# Séries oficiais do estelionato eletrônico: painel de 18 UFs (2021 a 2025), furto mediante fraude eletrônica e o Pará

Versão 0.3, 21/11/2026. Espelho do doc `claude/serie-estelionato-eletronico-painel-18uf.md` do Project "Criminologia Informática". Apoio às linhas 1.2 (medição e cifra oculta) e 1.3 (deslocamento da criminalidade) de `docs/linhas-de-pesquisa.md`.

Páginas publicadas como artefatos do claude.ai, privadas até o usuário as compartilhar: "Estelionato eletrônico em 18 UFs" (https://claude.ai/artifact/RuqeRgeDmHGYSm5UvdJstv) e "Crime patrimonial eletrônico no Pará" (https://claude.ai/artifact/YS8RSQFwPw5Y5gEJdQrj6v). As fontes estão em `paginas/` e os gráficos em PNG, para slide, em `graficos/`.

## Fonte e montagem

Tabelas "Estelionato e Estelionato por meio eletrônico" das planilhas do Anuário Brasileiro de Segurança Pública (FBSP): 17ª ed. (2023), aba T15, anos 2021 e 2022; 18ª (2024), T15, 2022 e 2023; 19ª (2025), T19, 2023 e 2024; 20ª (2026), T17, 2024 e 2025. Para cada UF e ano ficou o valor da edição mais recente, porque o FBSP revisa o ano anterior; o que cada edição publicou está em `dados/estatisticas/anuario_estelionato_por_edicao.csv`. Estelionato comum = total menos eletrônico (o total do Anuário abrange as duas modalidades, nota 1 das tabelas).

## Por que não o total "Brasil" do meio eletrônico

Soma só as UFs que informaram no ano, e a composição muda: SP, RJ e CE nunca informaram (os 346.753 registros de 2025 os excluem). Série nacional do meio eletrônico, portanto, não existe no Anuário.

## Exclusões do painel

SP, RJ e CE (nunca informaram); PE (natureza criada no sistema em dez/2024, nota da 19ª e 20ª; valores de 2021 a 2023 retirados depois); PA (mudança de metodologia da SSP/PA em 2023, de "todas as fraudes" para os §§ 2º-A, 2º-B e 3º; 2023 revisto de 16.884 para 1.686); RS (registra desde 27/07/2023); BA (sem 2021); RN (sem 2021 e 2022); AM (revisões sem nota: 2023 de 877 para 3.829, 2024 de 6.035 para 972).

Painel: AC, AL, AP, DF, ES, GO, MA, MT, MS, MG, PR, PB, PI, RO, RR, SC, SE, TO. Somam 37,0% dos estelionatos registrados no país em 2025.

## Série do painel

| Ano | Eletrônico | Comum | Total | % eletrônico |
| --- | --- | --- | --- | --- |
| 2021 | 108.188 | 430.886 | 539.074 | 20,1% |
| 2022 | 175.260 | 514.694 | 689.954 | 25,4% |
| 2023 | 202.040 | 527.533 | 729.573 | 27,7% |
| 2024 | 250.785 | 551.378 | 802.163 | 31,3% |
| 2025 | 278.590 | 557.897 | 836.487 | 33,3% |

Eletrônico: 2,6 vezes de 2021 a 2025, 1,6 vez de 2022 a 2025. Comum: 1,3 vez e 1,08 vez. Do aumento de 146.533 registros entre 2022 e 2025, 103.330 (70,5%) são eletrônicos.

## Ressalvas

2021 é o primeiro ano da natureza (Lei 14.155/2021) e várias UFs ainda a implantavam (GO 128, RR 59, PI 65 registros), o que infla o crescimento a partir desse ano; 2022 é a base mais segura. O registro policial não separa crescimento do crime de reclassificação do comum para o eletrônico: em GO o total vai de 74.163 (2022) a 79.850 (2025) enquanto o eletrônico vai de 1.488 a 5.691. Revisões entre edições são frequentes (MT 2023 +67%, RO 2024 +64%, MS 2022 +99% no eletrônico), sem nota.

## Furto mediante fraude eletrônica (art. 155, § 4º-B): sem série nacional

Conferido em 21/11/2026. Nenhuma das quatro planilhas do Anuário (17ª a 20ª) tem tabela do § 4º-B; o furto aparece só como furto de veículos e de celulares. O Mapa da Segurança Pública 2026 (Sinesp, ano-base 2025) também não tem indicador de fraude ou furto eletrônico. No Judiciário, o § 4º-B não tem folha nas TPU e se dissolve no 3417 (ver `documentacao_projeto/` e o doc `claude/quadro-visibilidade-tpu-lei-14155.md` do Project). Consequência para a linha 1.3: a série do estelionato eletrônico deixa de fora a metade furto da mesma família de condutas, cuja fronteira com o estelionato é instável (`docs/analise/q2-teste-eliminacao.md`).

Fontes que existem, nenhuma por tipo penal nacional:

- Registros estaduais, por portal ou LAI (ex.: censo do Pará, seção abaixo).
- BCB, Estatísticas de Fraude no Pix (MED), API Olinda `EstatisticasFraudesPix`, mensal de jan/2022 a set/2026, em `dados/estatisticas/bcb_fraudes_pix_mensal.csv`: contestações aceitas 1.555.897 (2022), 2.574.110 (2023), 4.912.207 (2024), 3.933.697 (2025); valor aceito R$ 3,02 bi, 4,35 bi, 6,69 bi, 7,77 bi. Não separa golpe (vítima transfere) de transação feita por terceiro com acesso à conta: mede a união estelionato e furto via Pix, e depende das regras do MED (MED 2.0 obrigatório desde 02/02/2026).
- FBSP/Datafolha, pesquisa de vitimização 2025 (jul/2024 a jun/2025, 2.007 entrevistas): "fraude bancária em conta corrente ou poupança" 6,5%, o item mais próximo do furto informático; não há item de invasão de conta bancária.

## Pará: censo SIAC contra o Anuário

Fonte: Silva, Ramos e Reis Netto (2026), Revista Tópicos, DOI 10.70773/revistatopicos/793465755, Tabela 1 (lida da versão web; a versão em PDF corta a tabela). Censo de 98.039 BOs da SIAC/SEGUP-PA, jan/2022 a dez/2025, consumados e tentados. As duas tabelas do artigo, como lidas, estão em `dados/estatisticas/para_artigo_tabelas.csv`; na Tabela 2 (DECCC), a coluna "Total" das linhas repete a da Tabela 1, por erro do artigo, e a soma correta (8.795, 349 e 453) está na coluna `total_recalculado`.

| Ano | Caput, meio eletrônico | § 2º-A | Furto § 4º-B | Total | Anuário PA (eletrônico) |
| --- | --- | --- | --- | --- | --- |
| 2022 | 13.861 | 2 | 3.782 | 17.645 | 13.099 (18ª) |
| 2023 | 18.144 | 1.628 | 2.797 | 22.569 | 1.686 (19ª) |
| 2024 | 19.472 | 4.199 | 3.645 | 27.316 | 4.165 (20ª) |
| 2025 | 20.718 | 5.362 | 4.429 | 30.509 | 5.164 (20ª) |

Achado: com a mudança de filtro da SSP/PA em 2023, o Anuário passou a contar só a qualificadora. Em 2022 o Anuário (13.099) fica perto de caput mais § 2º-A no censo (13.863); em 2025 (5.164), perto só do § 2º-A (5.362). A série nacional do Pará cai 87% de 2022 para 2023 enquanto os registros policiais crescem 27,9%; desde 2023, o Anuário capta menos de um quinto do registrado (7,5%, 15,2%, 16,9%). Em 2025, 79,4% do estelionato eletrônico ainda é registrado no caput; o furto § 4º-B é 14,5% do total e não aparece em tabela nacional. O estelionato eletrônico do censo equivale a 62,5% de todo o estelionato do Pará no Anuário de 2025 (26.080 de 41.731).

## Como reproduzir

Da raiz do repo, nesta ordem:

1. `python3 scripts/estatisticas_baixa.py`: baixa as quatro planilhas do Anuário e a versão web do artigo para `dados/bruto/` (fora do git, pela regra de gravar só o que foi lido).
2. `python3 scripts/estatisticas_painel.py`: grava `dados/estatisticas/anuario_estelionato_por_edicao.csv` e `estelionato_uf_2021_2025.csv` (requer `openpyxl`).
3. `python3 scripts/estatisticas_pagina_18uf.py`: monta o painel balanceado (exclusões no dicionário `EXCLUIDAS`), imprime o resumo e grava `docs/estatisticas/paginas/estelionato_18uf.html` a partir de `scripts/templates/estelionato_18uf.html`.
4. `python3 scripts/estatisticas_pagina_para.py`: grava `dados/estatisticas/para_artigo_tabelas.csv`, `para_registros_2022_2025.csv` e `docs/estatisticas/paginas/para_crime_eletronico.html`.
5. `python3 scripts/estatisticas_bcb_pix.py`: grava `dados/estatisticas/bcb_fraudes_pix_mensal.csv`.
6. Para conferir o render e refazer o PNG: `python3 scripts/estatisticas_captura.py docs/estatisticas/paginas/<pagina>.html /tmp/inteira.png docs/estatisticas/graficos/<pagina>.png light` (requer `playwright` e Chrome).

Todos os números das páginas saem dos CSVs pelos scripts; nenhum é digitado à mão. A execução de 21/11/2026 refez do zero os dois CSVs e as duas páginas, idênticos byte a byte aos publicados. A paleta das páginas (azul e laranja de destaque, cinzas de contexto) passou pelo validador de cores da skill de visualização, nos modos claro e escuro.
