# Sentenças da base de 130 casos (furto eletrônico, fraude eletrônica, invasão de dispositivo)

Íntegras das sentenças de primeiro grau do TJSP que compõem a base de 130 casos do Project "Criminologia Informática", coletadas em 20/11/2026 na Consulta de Julgados de 1º Grau (CJPG), consulta pública. A base nasceu com 100 casos (C01 a C100) e foi ampliada com 30 (C101 a C130), três por família; a pasta mantém o nome original para não quebrar links.

## Conteúdo

- `sentencas/`: 128 arquivos de texto, um por sentença, nomeados `C###_<número CNJ>.txt`. O texto é o publicado na CJPG, extraído do HTML da consulta, sem edição.
- `indice.csv`: uma linha por caso (C01 a C130), com família, processo, órgão, data da decisão, data do fato, arquivo, tamanho, indicação de texto completo e link de consulta por número na CJPG.
- `fichas.jsonl`: as 130 fichas de análise (conduta, capitulação, solução, fundamento, pena, divergência e ponto para análise), a mesma base da planilha.

## Lacunas

- C21 (MPCE) e C27 (MPSP) são denúncias conhecidas só por notícia; não há peça arquivada.
- C34, C45, C50 e C73, e na ampliação C110, C112, C120 e C123, vieram cortados perto de 50 mil caracteres na consulta por termo da CJPG e foram substituídos pela íntegra obtida na consulta por número (coluna `link_cjpg`), conferida pelo mesmo início e pela presença do dispositivo.

## Recorte e método

Condutas praticadas a partir de 28/05/2021 (vigência da Lei 14.155/2021), pela data do fato e não do processo. Amostra intencional por modo de execução, dez famílias com dez casos cada na base original e treze cada depois da ampliação. Na ampliação, a escolha favoreceu casos que acrescentam um problema novo à família, entre eles os efeitos da Lei 15.397/2026 (cessão de conta, nova redação do § 2º-A do art. 171, penas da receptação e do § 4º-B do art. 155), e manteve cerca de metade de soluções divergentes da denúncia. Cada sentença foi rebuscada na CJPG pelo número do processo e conferida quanto à data do fato, à capitulação e ao dispositivo.

## Atenção

Os textos trazem os nomes de réus, vítimas e testemunhas tal como publicados pelo tribunal, inclusive em casos de violência doméstica e com vítimas idosas. As fichas omitem esses nomes; os textos não. Não redistribuir sem anonimização.
