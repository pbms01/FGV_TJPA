# Sentenças da base de 100 casos (furto eletrônico, fraude eletrônica, invasão de dispositivo)

Íntegras das sentenças de primeiro grau do TJSP que compõem a base de 100 casos do Project "Criminologia Informática", coletadas em 20/11/2026 na Consulta de Julgados de 1º Grau (CJPG), consulta pública.

## Conteúdo

- `sentencas/`: 98 arquivos de texto, um por sentença, nomeados `C###_<número CNJ>.txt`. O texto é o publicado na CJPG, extraído do HTML da consulta, sem edição.
- `indice.csv`: uma linha por caso (C01 a C100), com família, processo, órgão, data da decisão, data do fato, arquivo, tamanho, indicação de texto completo e link de consulta por número na CJPG.
- `fichas.jsonl`: as 100 fichas de análise (conduta, capitulação, solução, fundamento, pena, divergência e ponto para análise), a mesma base da planilha.

## Lacunas

- C21 (MPCE) e C27 (MPSP) são denúncias conhecidas só por notícia; não há peça arquivada.
- C34, C45, C50 e C73 vieram cortados perto de 50 mil caracteres na consulta por termo da CJPG e foram substituídos pela íntegra obtida na consulta por número (coluna `link_cjpg`), conferida pelo mesmo início e pela presença do dispositivo.

## Recorte e método

Condutas praticadas a partir de 28/05/2021 (vigência da Lei 14.155/2021), pela data do fato e não do processo. Amostra intencional por modo de execução, dez famílias com dez casos cada. Cada sentença foi rebuscada na CJPG pelo número do processo e conferida quanto à data do fato, à capitulação e ao dispositivo.

## Atenção

Os textos trazem os nomes de réus, vítimas e testemunhas tal como publicados pelo tribunal, inclusive em casos de violência doméstica e com vítimas idosas. As fichas omitem esses nomes; os textos não. Não redistribuir sem anonimização.
