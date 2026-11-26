# Questão 7 no TJPA: a versão do titular da conta, o desfecho e a posição do MP

Nota de 26/11/2026. Leva ao TJPA a questão 7 da fase 1 (como o titular entra na fraude, segundo ele mesmo, e o que isso decide) e põe ao lado de cada desfecho a posição do MP nas alegações finais (`dados/analise/posicao_mp_fe.csv`). Tabelas por `python3 scripts/analise_q7_titular_tjpa.py`, que grava `dados/analise/q7_titular_tjpa.csv` e `q7_resumo_tjpa.json`.

## Resposta

Quando o MPPA denuncia o titular como titular (o papel da codificação é só a conta) e ele admite ter cedido a conta, o desfecho é o do TJSP: condenação em 8 de 8 sentenças, contra 45 de 47 em São Paulo. O que separa os tribunais está em dois lugares. O primeiro é a denúncia que descreve o titular como autor do ardil (o misto): entre os mistos que admitiram a cessão, só 1 de 6 foi condenado, e 4 das 5 absolvições foram pedidas pelo próprio MP. O segundo é a frequência do pedido de absolvição: na FE, o MP pede a absolvição em 16 das 54 sentenças de mérito de titulares e mistos no TJPA (30%), contra 2 das 57 do grupo "só conta" no TJSP (3,5%). Dado o pedido de condenação, a absolvição é igual nos dois tribunais: 4 de 36 (11,1%) no TJPA e 5 de 45 (11,1%) no TJSP.

A versão do titular, portanto, decide no TJPA o que decide no TJSP quando a acusação a sustenta até o fim; o que muda é a acusação, que no TJPA desiste com frequência dez vezes maior e desiste sobretudo do titular que ela própria descreveu como autor da mensagem.

## Base e método

- Unidade: as denúncias sem duplicata da FE e do CL com papel `titular_conta` (62) ou `misto` (64) na codificação assistida do TJPA; 63 têm sentença de mérito (FE: 24 titulares e 30 mistos; CL: 4 e 5). Sem a tabela de nível da questão 1 no TJPA, a unidade é o papel da codificação, e não o "só conta" do TJSP; o misto entra como grupo próprio porque a codificação das denúncias e a das absolvições mostraram que parte dele é titular descrito como autor do ardil.
- Versão: a leitura de `scripts/titular_conta.py`, agora com `TRIB=tjpa` (sem mudança no TJSP: `q7_titular.csv` sai igual), que procura a versão frase a frase, só nas frases de declaração, interrogatório, silêncio ou revelia, na denúncia e na sentença. Os 67 casos com sentença foram conferidos pelo trecho, e 18 leituras foram corrigidas à mão (`VERSAO_MANUAL_TJPA`, com o motivo): a regra tomava "à revelia dos titulares" da descrição da Operação Trojan, o direito ao silêncio citado na doutrina das sentenças e o depoimento da vítima pela versão do réu.
- Desfecho: o da sentença por família; condenação inclui a procedência parcial. Posição do MP: a de `posicao_mp_fe.csv`, que cobre a FE; no CL fica em branco.

## Resultado

| Versão | TJPA, titular | TJPA, misto | TJSP, só conta (questão 7) |
| --- | --- | --- | --- |
| Cessão admitida | 8 de 8 (100%) | 1 de 6 (17%) | 45 de 47 (96%) |
| Nega ou não reconhece a conta | 5 de 11 (45%) | 9 de 12 (75%) | 30 de 37 (81%) |
| Ausente (silêncio ou revelia) | 3 de 4 (75%) | 6 de 9 (67%) | 9 de 11 (82%) |
| Sem versão | 3 de 5 (60%) | 4 de 8 (50%) | 4 de 4 (100%) |

Condenações entre as sentenças de mérito. TJPA na FE e no CL; TJSP na FE e no CL.

| FE, versão | TJPA: MP pede condenação (condena / absolve) | TJPA: MP pede absolvição | TJSP: MP pede condenação (condena / absolve) | TJSP: MP pede absolvição | TJSP: sem registro (condena / absolve) |
| --- | --- | --- | --- | --- | --- |
| Cessão admitida | 7 / 0 | 4 | 23 / 1 | 0 | 4 / 0 |
| Nega ou não reconhece | 13 / 2 | 7 | 13 / 4 | 1 | 4 / 1 |
| Ausente | 8 / 1 | 2 | 3 / 0 | 1 | 0 / 0 |
| Sem versão | 4 / 1 | 3 | 1 / 0 | 0 | 1 / 0 |

Todos os pedidos de absolvição terminaram em absolvição, nos dois tribunais. No TJPA, dois mistos da FE sem registro da posição do MP foram condenados.

## Leitura

1. A cessão admitida tem, no TJPA, o mesmo efeito que no TJSP quando a denúncia trata o titular como titular. Os sete titulares da FE que admitiram a cessão (PA-FE 7, 14, 25, 44, 46, 89 e 145, três deles mediante pagamento, um por R$ 300,00) foram condenados, sempre com pedido de condenação do MP, e o CL 35 também.

2. O misto que admite a cessão é absolvido, e a pedido do MP. Nos PA-FE 70, 108, 179 e 215, a denúncia atribuía aos réus o ardil (o contato, a mensagem ou a participação no grupo) e, em juízo, eles disseram ter emprestado ou vendido a conta, por favor ou por pequena quantia; o MP pediu a absolvição pela falta de prova do dolo ou da autoria narrada. O padrão sugere que a denúncia que descreve o titular como autor da mensagem, sem prova além da conta, perde o caso justamente quando a instrução revela o que o TJSP condena, a cessão. Se o pedido de absolvição decorre da correlação entre acusação e sentença (o fato provado não é o narrado) ou de um juízo do MP sobre o dolo do cedente, não está dito nas sentenças lidas, e pede a leitura dos memoriais.

3. Negar ou não reconhecer a conta absolve mais no TJPA (6 de 11 titulares absolvidos, contra 7 de 37 no TJSP), mas a maior parte dessas absolvições foi pedida pelo MP: na FE, das 9 absolvições entre os que negam, 7 foram pedidas.

4. Fixada a posição da acusação, o TJPA não absolve mais do que o TJSP: dado o pedido de condenação, 11,1% nos dois, entre titulares e mistos da FE no TJPA e o "só conta" da FE no TJSP. A questão 7 confirma, no recorte do titular, o que a nota das absolvições (`docs/analise/fundamento-absolvicoes-fe.md`) mostrou para toda a FE.

## Limites e pendências

- A unidade difere: papel da codificação no TJPA, nível "só conta" no TJSP. A comparação mais próxima é a dos titulares do TJPA com o "só conta" do TJSP; o misto não tem equivalente direto em São Paulo.
- As contagens são pequenas (8 titulares com cessão admitida, 6 mistos), e a versão sai da sentença ou da denúncia, não do interrogatório gravado.
- A posição do MP no CL não foi codificada.
- Falta, nas questões, a tabela de nível da questão 1 no TJPA, que permitiria a unidade "só conta"; e falta ler os memoriais dos quatro mistos com cessão admitida absolvidos a pedido do MP, para saber se o pedido se apoia na correlação ou no dolo.
