# Coleta e triagem da base de casos

Metadados e scripts com que a base de 130 casos foi montada a partir da Consulta de Julgados de 1º Grau (CJPG) do TJSP, de 20/11/2026. O corpus de texto integral (cerca de 140 MB em `raw/` e `triagem/corpus.jsonl`) não está aqui: traz os nomes das partes como publicados e se refaz rodando os scripts.

## Arquivos

| Arquivo | Conteúdo |
| --- | --- |
| `triagem.csv` | As 2.081 sentenças triadas: número, ano do número CNJ, data do fato estimada, situação (`ok` 1.341, `descarte_cnj` 352, `fato_anterior?` 210, `sem_data` 178), assunto, comarca, vara, data da sentença, tamanho, consultas que a trouxeram, famílias sugeridas, artigos no texto e no dispositivo, solução |
| `fila.csv` | As 586 aptas com art. 154-A, 155 ou 171 na abertura e marcador digital: data do fato, comarca, tipos da abertura, família provável, solução e artigos do dispositivo |
| `usados.json` | Processos que entraram na base (`base`, 130) e os lidos e descartados (`rej`), para que nenhuma rodada releia o mesmo caso |
| `scripts/` | Pipeline, na ordem em que roda (abaixo) |

## Pipeline

1. `matriz.py` roda a matriz de consultas (26 consultas por família de conduta e por artigo, em janelas anuais de 2022 a 2026) e grava um JSONL bruto por consulta e ano em `raw/`. Usa `cjpg.py`, que guarda a sessão de cada consulta e lê o texto integral embutido na página de resultados.
2. `triagem.py` deduplica, descarta número CNJ anterior a 2021, estima a data do fato e marca famílias, artigos e solução; grava `triagem/corpus.jsonl` e `triagem.csv`.
3. `fila.py` filtra pela capitulação e pela narrativa da abertura e grava `fila.csv`; `selecao.py` sugere até N por família, metade com sinal de divergência; na quarta rodada, `candidatos_familia.py` ordenou a fila remanescente por expressões de modo de execução.
4. Leitura: `cartao.py`, `extrato.py`, `ficha_extrato.py`, `janela.py` e `grep_caso.py` imprimem trechos da sentença (abertura, tipificação, fundamentação em torno de um termo, dispositivo).
5. Fichamento: as fichas entram em `base/fichas.jsonl` por `add_ficha.py`; `gera_csv3.py` gera as linhas na ordem de colunas da aba Casos.
6. Conferência: `conferencia.py` a `conferencia3.py` rebuscam cada sentença pelo número e cotejam data do fato, capitulação e dispositivo; `integra.py` busca pela consulta por número a íntegra das sentenças que a consulta por termo corta perto de 50 mil caracteres.

Os scripts supõem a raiz de trabalho `coleta/` com as pastas `raw/`, `triagem/`, `base/` e `integra/`; alguns trazem esse caminho fixo (`/home/claude/coleta`).

## Limites

A CJPG lista só processos com sentença de primeiro grau publicada; ficam fora os feitos em curso e os em segredo de justiça. A data do fato em `triagem.csv` e `fila.csv` é estimativa automática; a da ficha foi conferida na leitura.
