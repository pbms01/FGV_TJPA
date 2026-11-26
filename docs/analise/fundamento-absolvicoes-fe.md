# Fundamento das absolvições integrais da FE no TJPA e no TJSP

Nota de 26/11/2026. Responde ao passo que o HANDOFF dava como o que mais pesa na fase 2: dizer se a absolvição integral de 29,3% na FE do TJPA, contra 12,1% no TJSP, é achado ou artefato da base. A resposta curta é que a diferença é achado, situado na acusação e não no julgamento: quando o Ministério Público pede a condenação, o TJPA absolve na FE em proporção próxima à do TJSP (7,6% contra 5,4%), e quase toda a distância vem das absolvições que o próprio MP pede nas alegações finais (20,7% contra 3,8%). A lista 2 do DJEN infla a taxa do TJPA, mas a lista 1 sozinha conserva o dobro do TJSP e a mesma decomposição. Codificada depois a posição do MP também nas condenações, a conta fecha: dado o pedido de condenação, a absolvição integral é de 10,8% no TJPA e de 7,7% no TJSP; dado o pedido de absolvição, é de 100% nos dois tribunais; e o MP pede a absolvição em 21,6% das sentenças de mérito da FE no TJPA, contra 3,9% no TJSP.

## Base e método

- TJPA: as 27 absolvições integrais entre as 92 sentenças da FE contadas por família (`dados/extracao/sentencas_tjpa.csv`, extração regerada em 25/11/2026). Censo, com contagens simples.
- TJSP: as 11 absolvições integrais entre as 113 sentenças da FE da amostra do cjpg (`dados/analise/q1_alcance.csv`), com o peso amostral nas proporções.
- Leitura de um só leitor, sem segundo leitor, sobre trechos selecionados de cada sentença (o relatório das alegações finais, as frases da fundamentação que tocam autoria, dolo, titularidade, prova judicializada, revelia e pedido do MP, e o dispositivo), completada por leitura adicional do texto em 13 sentenças em que os trechos não decidiam o fundamento ou a posição do MP. O papel e o artifício vêm da codificação das denúncias (`codificacao_assistida_tjpa.csv`; no TJSP, a tabela da questão 1).
- Posição do MP nas condenações (segunda etapa, no mesmo dia): nas 61 sentenças condenatórias da FE do TJPA e nas 101 do TJSP, um leitor por regras tomou, no relatório anterior à fundamentação, a frase em que o MP formula o pedido final; a regra só decidiu pedidos de condenação (103 sentenças), e uma amostra de 14 delas foi conferida no texto, com as 14 confirmadas (duas passaram a pedido parcial). As outras 59 foram lidas caso a caso. Nas absolvições, a posição é a da codificação do fundamento. O pedido parcial (condenação de uns réus ou crimes e absolvição de outros) está subcontado, porque a regra não o separa, o que não afeta a decomposição.
- Arquivos: `dados/analise/fundamento_absolvicoes_fe.csv` (uma linha por absolvição, com o trecho decisivo da sentença), `dados/analise/posicao_mp_fe.csv` (a posição do MP nas 200 sentenças de mérito da FE dos dois tribunais, com a fonte e o trecho) e `scripts/fundamento_absolvicoes.py`, que confere a cobertura, o vocabulário, o papel contra a codificação e a posição do MP contra a das absolvições, e imprime as tabelas desta nota.

## Livro de códigos

`fundamento` registra a lacuna que a sentença aponta, pelo que liga o réu ao fato e não pelo rótulo que o juiz usa (muitas sentenças dizem "autoria" quando o que falta é o dolo do titular):

- `titularidade_insuficiente`: o que liga o réu ao fato é a conta (titularidade, recebimento, chave Pix), e a sentença diz que isso não prova a participação nem a ciência;
- `adesao_nao_provada`: está provado outro ato do réu (guarda das mercadorias, intermediação), mas não a adesão ao ardil;
- `autoria_ato`: há dúvida sobre se o réu praticou o ato que a denúncia lhe atribui (imagem, presença, contato, nome usado por terceiro), ou ele não tem ligação nem pela conta;
- `instrucao_vazia`: nada se produziu em juízo (vítima não ouvida, por desistência ou não localização, e só testemunhas que não presenciaram o fato), e é isso que a sentença invoca;
- `atipicidade`: o fato não é crime (insignificância, ilícito civil, falta de relevância penal);
- `pedido_mp`: a sentença absolve só porque o MP pediu, sem examinar a prova.

Os demais campos são `inciso_386` (ou o inciso do art. 397), `mp_absolvicao` (o MP pediu a absolvição nas alegações finais ou na manifestação que antecedeu a absolvição sumária; `nd` quando a sentença não registra), `mp_vincula` (a sentença diz que não pode condenar contra o pedido do MP, isto é, afasta o art. 385 do CPP), `revel`, `vitima_juizo` (`s`, `n`, `parcial`, `nd`), `falta_prova_tecnica` (a sentença aponta a falta de extrato, registro de acesso, IP, IMEI, ERB ou perícia), `prova_inquerito` (a sentença diz que a prova ficou no inquérito, art. 155 do CPP) e `versao_reu`.

## Resultado

| Fundamento | TJPA (27) | TJSP (11, % ponderado) |
| --- | --- | --- |
| titularidade insuficiente | 12 | 9 (86,1%) |
| adesão não provada | 1 | 1 (6,9%) |
| autoria do ato | 5 | 0 |
| instrução vazia | 4 | 1 (6,9%) |
| atipicidade | 3 | 0 |
| só o pedido do MP | 2 | 0 |

| Absolvição integral da FE | TJPA (92 sentenças, censo) | TJSP (113 sentenças, % ponderado) |
| --- | --- | --- |
| Total | 27 (29,3%) | 11 (12,1%) |
| pedida pelo MP | 19 (20,7%) | 4 (3,8%) |
| contra o pedido de condenação | 7 (7,6%) | 5 (5,4%) |
| posição do MP não registrada | 1 (1,1%) | 2 (2,9%) |

| Absolvição por papel do denunciado | TJPA | TJSP (ponderado) |
| --- | --- | --- |
| titular de conta | 8 de 25 (32,0%) | 8 de 58 (17,3%) |
| misto | 12 de 32 (37,5%) | 2 de 31 (8,6%) |
| executor | 7 de 34 (20,6%) | 1 de 24 (3,9%) |

| TJPA, lista do DJEN | Sentenças | Absolvições | pedidas pelo MP | sem pedido do MP |
| --- | --- | --- | --- | --- |
| 1 | 72 | 18 (25,0%) | 13 (18,1%) | 5 (6,9%) |
| 2 | 19 | 9 (47,4%) | 6 (31,6%) | 3 (15,8%) |

| Sentenças de mérito da FE | TJPA (88, censo) | TJSP (112, % ponderado) |
| --- | --- | --- |
| MP pediu a condenação, total ou parcial | 65 (73,9%) | 83 (71,0%) |
| MP pediu a absolvição | 19 (21,6%) | 4 (3,9%) |
| posição do MP não registrada | 4 (4,5%) | 25 (25,2%) |
| absolvição integral, dado o pedido de condenação | 7 de 65 (10,8%) | 5 de 83 (7,7%) |
| absolvição integral, dado o pedido de absolvição | 19 de 19 | 4 de 4 |
| absolvição integral, sem registro da posição | 1 de 4 | 2 de 25 (11,5%) |

Inciso: VII em 23 das 27 no TJPA (III em duas; absolvição sumária pelo art. 397, II e III, em duas) e em 9 das 11 no TJSP (III e V em uma cada).

## Leitura

1. A diferença entre os tribunais está quase toda nas absolvições que o MP pede. Contra um pedido de condenação, o TJPA absolve em 7,6% das sentenças da FE e o TJSP em 5,4% (8,3% no limite, se as duas sem registro fossem contra o pedido); a pedido do MP, 20,7% contra 3,8% (6,7% no limite). Tomada a taxa condicional, a absolvição integral dado o pedido de condenação é de 10,8% no TJPA (7 de 65) e de 7,7% no TJSP (5 de 83), diferença pequena para contagens dessa ordem; dado o pedido de absolvição, é total nos dois tribunais, e nenhuma das 200 sentenças condena contra o pedido do MP, de modo que o art. 385 do CPP, na prática, não opera em nenhum deles. O juiz paraense não absolve muito mais do que o paulista; o que muda é a frequência com que a acusação se desfaz no fim da instrução, que é de 21,6% das sentenças de mérito no TJPA e de 3,9% no TJSP (até cerca de 6% se as duas absolvições paulistas sem registro tiverem sido pedidas).

2. O que o MP abandona é, em primeiro lugar, o titular da conta. Das 19 absolvições pedidas, 9 têm por fundamento a titularidade insuficiente: a denúncia alcança quem recebeu o dinheiro, muitas vezes sem descrever outro ato (a codificação das denúncias já registrava casos em que "a denúncia não descreve seu ato além do recebimento", e o misto que vem da redação), e a mesma instituição reconhece, nos memoriais, que a conta não prova a adesão. Em três processos o réu admitiu ter cedido a conta, num deles por pequena quantia e noutro sacando e entregando o dinheiro a terceiro (PA-FE 108, 215 e 70), e o MP pediu a absolvição; no TJSP, quem admite a cessão é condenado em 45 de 47 sentenças, somados os estratos (questão 7).

3. Em segundo lugar, o MP abandona a instrução: em quatro das 19, a vítima não foi ouvida, por desistência do MP (PA-FE 224, golpe do motoboy, com reconhecimento e confissão só na delegacia) ou das partes (PA-FE 37) ou por não ter sido localizada (PA-FE 58), ou só depôs quem não presenciou o fato (PA-FE 179). No PA-FE 92, a desistência de uma das vítimas precedeu o pedido de absolvição.

4. A parte judicial existe, mas é menor. Em 7 das 19, a sentença diz não poder condenar contra o pedido do MP, afastando o art. 385 do CPP; em duas delas, da 9ª Vara Criminal de Belém, a absolvição se apoia só no pedido, sem exame da prova (PA-FE 53 e 80), e nas outras cinco a sentença também examina a prova ou a tipicidade. As absolvições pedidas espalham-se por dez varas, oito delas de Belém, de modo que não se trata de um juízo isolado.

5. A composição por papel não explica a diferença: o TJPA absolve mais em cada papel, e a distância é maior no misto (37,5% contra 8,6%). Dos 12 mistos absolvidos, 6 o foram pela titularidade insuficiente, o que confirma que o misto do MPPA é em boa parte de redação (a denúncia atribui o ardil, mas prova a conta) e que a fronteira entre titular e misto, frágil na codificação, pesa também aqui.

6. O artefato da base é parcial. As sentenças da lista 2 do DJEN, que não estavam classificadas como sentença, absolvem em 47,4%, contra 25,0% na lista 1, e elevam a taxa do TJPA em cerca de quatro pontos. A lista 1 sozinha, porém, ainda absolve o dobro do TJSP, com a mesma decomposição: 18,1% a pedido do MP e 6,9% contra o pedido.

7. Para as questões: na questão 1, o TJPA alcança o titular pela denúncia, mas a resposta do sistema a ele se decide nos memoriais do MP, e a tabela de nível precisa ler o desfecho com a posição da acusação ao lado; na questão 7, a versão da cessão admitida, que no TJSP equivale a confissão, no TJPA convive com o pedido de absolvição. A diferença de 29,3% contra 12,1% deve ser lida como diferença de conduta da acusação na fase final, e não como leniência judicial nem como simples efeito do censo.

## Limites e pendências

- Um só leitor, sobre trechos, sem segundo leitor. A posição do MP foi lida no relatório da sentença, não nos memoriais; três ficaram sem registro. A fronteira entre `titularidade_insuficiente` e `autoria_ato` é a mais frágil e deve entrar no segundo leitor cego, com a do papel.
- As contagens contra o pedido de condenação são pequenas (7 e 5), e a comparação é entre um censo e uma amostra ponderada.
- No TJSP, um quarto das sentenças de mérito não registra a posição do MP (alegações orais gravadas, relatório que só diz que as partes se manifestaram); 23 dessas 25 terminaram em condenação, sem nenhuma menção ao art. 385, o que sugere pedido de condenação, mas não o prova. No TJPA, são 4.
- Singularidades registradas na coluna `nota`: o termo de audiência do PA-FE 37 traz o nome e o tipo (art. 121) de outro processo antes da sentença correta; o PA-FE 187 absolve também o corréu cujo processo estava suspenso pelo art. 366; o PA-FE 78 é absolvição sumária pedida depois da instrução, pelo art. 397, II.
- Passo seguinte natural: levar a posição do MP (`posicao_mp_fe.csv`) às tabelas das questões 1 e 7, para ler o desfecho do titular com a posição da acusação ao lado, e estender a codificação aos estratos INV e CL.
