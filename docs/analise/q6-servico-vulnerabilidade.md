# Questão 6: a fraude explora a pessoa ou o serviço, e onde estava o banco

Nota analítica de 21/11/2026, sobre a base da fase 1 (TJSP). Tabelas reproduzíveis por `python3 scripts/analise_q6_servico.py`, que grava `dados/analise/q6_servico.csv` (uma linha por denúncia) e `dados/analise/q6_resumo.json`. A leitura da família do artifício, da vítima e dos pontos do serviço é de `scripts/servico_banco.py`, que imprime com `python3 scripts/servico_banco.py valida` os trechos que acionam cada indicador nas 29 denúncias da matriz. Linhas de pesquisa atendidas: 3.4 (vulnerabilidade da vítima) e 4.1 (governança privada e deveres de cuidado). Usa a questão 1 (nível alcançado), a questão 3 (valor do fato e ressarcimento pelo intermediário) e a questão 5 (data do fato).

## Resposta

A fraude que chega à sentença explora o serviço mais do que a pessoa, e a pessoa vulnerável é explorada pelo serviço em que ela confia. Das 171 denúncias em que o dinheiro passou pelo sistema financeiro, 43 imitam uma instituição (a falsa central do banco em 30, o boleto falso, o falso empréstimo, o falso advogado, a falsa taxa de plataforma), 56 imitam uma oferta (a venda falsa em 49), 35 imitam uma relação pessoal (o falso parente em 30), 14 manipulam o pagamento (a maquininha e a compra com comprovante falso ou cartão alheio) e 23 atacam a conta ou o aparelho (invasão, tomada de conta, celular roubado, coação). A vítima idosa está em 42 das 160 denúncias contra pessoa física (26,3%), e se concentra onde a fraude imita alguém em quem ela confia: é idosa em 45,7% das vítimas do falso parente e afins e em 33,3% das da falsa instituição, contra 8,9% das da venda falsa. O valor do golpe não a distingue (mediana de R$ 4.706 contra R$ 5.257). O que a distingue é o roteiro: o filho que mudou de número, o funcionário do banco que liga para proteger a conta. A acusação registra essa vulnerabilidade quase sempre, com o aumento do §4º do 171 ou do §4º-C, II, do 155, ou a agravante do art. 61, II, h, em 39 das 42.

O banco aparece em três pontos do fluxo, e o processo penal só vê um. No primeiro, a fraude usa o próprio banco: o nome, o roteiro de segurança (o "bloqueio do cartão", a "conta cofre", o "telefone desconhecido inserido no seu aplicativo do banco"), o segredo que autentica o cliente. A senha, o código ou o cartão saem das mãos da vítima em 14 das 43 fraudes que imitam instituição, em 13 das 23 que atacam a conta e em 10 das 14 que manipulam o pagamento, e em 8 denúncias o golpe contrata crédito em nome da vítima e o transfere em seguida. No segundo, o dinheiro entra numa conta de destino aberta no próprio sistema financeiro, por instituição obrigada a identificar o cliente (art. 10, I, da Lei 9.613/1998), e sai dela em minutos (22 denúncias narram o repasse ou o saque imediato, uma delas com a vítima avisando o banco a tempo e sem reversão, CL 28). No terceiro, o banco absorve o prejuízo: as 12 sentenças que registram ressarcimento pelo intermediário estão todas nas famílias em que a fraude passou pela segurança do serviço (6 na falsa instituição, 4 no ataque à conta, 2 na maquininha), e nenhuma na venda falsa nem no falso parente, que somam 91 denúncias. É a linha do fortuito interno da Súmula 479 do STJ aplicada pelo lado de quem envia o dinheiro. O lado de quem recebe, a conta de destino que a questão 1 mostrou ser a camada alcançada, não é cobrado de ninguém no processo penal, embora seja um serviço bancário com dever de identificar o cliente e, desde novembro de 2023, de compartilhar indícios de fraude na abertura de contas.

## Base e método

A unidade é a denúncia sem duplicatas. Entram as 171 da tipologia em que o dinheiro passou pelo serviço financeiro (11 no INV, 47 no CL, 113 na FE); ficam fora as 4 fora da tipologia e 27 em que não há conta da vítima nem pagamento (controle da parceira, devassa, venda de dados, insider, inserção de dados em sistema público). Por estrato, percentuais ponderados; por família e por ponto do serviço, contagens simples das três camadas somadas, porque a família atravessa os estratos.

A família agrupa o artifício da codificação pelo que a fraude imita. A taxa antecipada se divide: o falso empréstimo imita instituição financeira, e a falsa vaga e o falso editor (CL 44, FE 9, FE 117) imitam oferta. O sequestro de conta fica com os ataques à conta, porque o ato que abre o golpe é a tomada da conta.

A vítima idosa é a da extração (idade, "idoso", Estatuto) ou o §4º do 171 na capitulação. As 44 denúncias com o indicador foram lidas, e só o FE 29 sai, porque a denúncia fala das vítimas do grupo em geral. A pessoa jurídica vítima foi lida na nota da codificação (11 denúncias, 7 delas a compra fraudulenta contra comerciante). O aumento pela idade na capitulação foi lido nas sete denúncias de vítima idosa sem o §4º do 171 na coluna da extração: três têm o §4º-C, II, do 155 ou o §4º escrito como "c.c. §4º", uma tem a agravante, e três não têm aumento (FE 3, com o §3º; INV 36, organização criminosa e lavagem; CL 36, receptação).

Os pontos do serviço são triagem por termos na narrativa: credencial (senha, código, token, cartão entregue ou recolhido, motoboy), acesso remoto ou aplicativo malicioso, mais de uma operação feita pela própria vítima e repasse ou saque imediato pela conta de destino. Crédito em nome da vítima e reação do banco foram lidos um a um (dicionários `CREDITO` e `REACAO`). O indicador de várias operações exige que a vítima seja o sujeito da frase e é, por isso, um piso. O ressarcimento pelo intermediário vem da leitura das sentenças na questão 3.

## Primeira etapa: quem é a vítima

| Família do artifício | Denúncias | Pessoa jurídica | Vítima idosa (pessoa física) | Canal dominante | Valor mediano |
| --- | --- | --- | --- | --- | --- |
| Imita instituição | 43 | 1 | 14 de 42 (33,3%) | telefonia (25) | R$ 5.085 |
| Imita oferta | 56 | 0 | 5 de 56 (8,9%) | internet (56) | R$ 10.000 |
| Imita relação pessoal | 35 | 0 | 16 de 35 (45,7%) | internet (30) | R$ 3.500 |
| Manipula o pagamento | 14 | 7 | 3 de 7 | presencial (9) | R$ 7.000 |
| Ataca a conta ou o aparelho | 23 | 3 | 4 de 20 (20,0%) | sistema como objeto (17) | R$ 9.600 |

Por estrato, a vítima idosa está em 41,2% das denúncias CL, 21,9% das FE e 9,1% das INV da população; no CL, a proporção é quase o dobro da FE.

Duas leituras saem da tabela. A primeira é que a idade é explorada pela confiança e não pelo canal. O falso parente chega pelo WhatsApp e a falsa central pelo telefone, e nos dois a vítima idosa é um terço ou mais; a venda falsa também chega pela internet, mas pede da vítima a iniciativa de comprar, e ali a idosa quase não aparece. A segunda é que a vítima idosa não perde mais: a mediana do prejuízo é de R$ 4.706 entre as idosas e de R$ 5.257 entre as demais, e o golpe mais caro é o da venda falsa, que na base envolve com frequência veículos e quase nunca a vítima idosa. O §4º do 171, que manda considerar "a relevância do resultado gravoso", encontra na base um resultado que não se distingue pelo valor; o que se distingue é o meio.

## Segunda etapa: por onde o golpe passou no serviço

| Ponto do serviço | Imita instituição (43) | Imita oferta (56) | Imita relação pessoal (35) | Manipula o pagamento (14) | Ataca a conta ou o aparelho (23) |
| --- | --- | --- | --- | --- | --- |
| Credencial entregue ou obtida | 14 | 1 | 1 | 10 | 13 |
| Crédito em nome da vítima | 4 | 0 | 0 | 0 | 4 |
| Mais de uma operação da vítima (piso) | 3 | 8 | 3 | 0 | 0 |
| Repasse ou saque imediato no destino | 6 | 6 | 4 | 0 | 6 |
| Reação do banco narrada | 3 | 3 | 0 | 1 | 4 |
| Ressarcimento pelo intermediário na sentença | 6 | 0 | 0 | 2 | 4 |

O primeiro ponto é a autenticação. Nas fraudes que imitam o banco, o golpe é o próprio roteiro de segurança do banco: o falso funcionário avisa de compra suspeita, pede a senha a pretexto de bloquear o cartão, manda um motoboy ou um falso policial buscar o cartão (FE 39, FE 54, FE 65, FE 79, FE 84, FE 122), orienta a transferir para uma "conta cofre" (CL 13) ou a não usar o cartão por cinco dias enquanto a conta é esvaziada (FE 64). A segurança que depende de um segredo que o cliente sabe recitar é vencida por quem imita a voz que o pede.

O segundo é o crédito. Em 8 denúncias o golpe contrata empréstimo na conta da vítima e o transfere logo: pela falsa central (CL 48, R$ 8.630; FE 70; FE 54), pela invasão da conta de aposentado (FE 88, consignado de R$ 6.300), pelo celular roubado (CL 41, R$ 26.000), pela coação (CL 18, R$ 15.600), pelo falso funcionário que altera o consignado e abre outra conta em nome da vítima (FE 58) e pelos correspondentes que montam consignados de aposentados (INV 36). A contratação seguida de transferência imediata a terceiro é o padrão atípico que a própria operação produz.

O terceiro é a conta de destino. A denúncia narra o repasse ou o saque imediato em 22 casos, e em seis diz que a pressa ou a passagem por outras contas servia para evitar o bloqueio (CL 4, CL 33, CL 35, CL 37, FE 9, FE 23). O CL 28 mostra o tempo do serviço contra o tempo do golpe: a empresa avisou o banco "rapidamente", e o dinheiro já tinha sido repassado minutos depois para outras duas contas do titular. A conta de destino, nas questões 1 e 5, é a camada que a investigação alcança e que o banco guarda por cinco anos; aqui ela aparece como a camada que o banco recebeu, abriu e deixou movimentar.

As reações do banco que a denúncia narra são 11. Três bloqueios da conta de destino (INV 35, com a fraude levantada pelo próprio banco; FE 16, meses depois; CL 43, segundo o titular), duas manutenções da cobrança do empréstimo contestado (FE 88, FE 70, este com 84 parcelas descontadas da aposentadoria), um cancelamento do mútuo sem devolução das transferências (CL 48), uma recusa de responsabilidade da plataforma de pagamento (FE 47), dois ressarcimentos (CL 34, CL 41), o estorno contra o lojista nas compras com cartão alheio (FE 17) e o aviso tempestivo sem reversão (CL 28).

## Terceira etapa: quem paga

As 12 sentenças que registram que um banco, uma instituição de pagamento ou uma empresa cobriu o prejuízo (questão 3) estão nas famílias em que a fraude passou pela segurança do serviço: falsa central (FE 65, FE 122, CL 48, FE 70, CL 34, FE 54), ataque à conta (CL 15, CL 18, CL 28, CL 41) e maquininha (CL 24, CL 29). Nenhuma está na venda falsa nem no falso parente. A distribuição acompanha o critério da Súmula 479 do STJ: "As instituições financeiras respondem objetivamente pelos danos gerados por fortuito interno relativo a fraudes e delitos praticados por terceiros no âmbito de operações bancárias". O CDC dá a régua: o fornecedor de serviços responde "independentemente da existência de culpa" pelos defeitos do serviço (art. 14, caput), o serviço é defeituoso quando "não fornece a segurança que o consumidor dele pode esperar" (art. 14, §1º), e a responsabilidade cai com a prova da "culpa exclusiva do consumidor ou de terceiro" (art. 14, §3º, II). Quando a fraude imita o banco ou toma a conta, a falha é do serviço; quando a vítima paga a um vendedor ou a um parente falso, nenhuma sentença da base registra intermediário pagando, e o prejuízo fica com ela.

O que essa leitura deixa de fora é o banco de destino. Nas 91 denúncias de venda falsa e falso parente, o dinheiro entrou numa conta aberta por uma instituição autorizada, em nome de pessoa que, nas denúncias de só conta, quase metade das vezes diz tê-la emprestado ou vendido (questão 7), e saiu dela. A questão 1 achou selfie ou biometria na abertura em 11 denúncias, usadas para identificar o titular depois e não para impedir a cessão. A Resolução Conjunta CMN/BCB nº 6, de 23 de maio de 2023, obriga as instituições a registrar e compartilhar, por sistema eletrônico, dados sobre indícios de ocorrências ou tentativas de fraude, e a Resolução BCB nº 343, de 4 de outubro de 2023, inclui entre as atividades mínimas do registro a abertura de conta de depósitos ou de pagamento. Na base, 29 dos 171 fatos e 13 das 101 denúncias de só conta são posteriores a 1º de novembro de 2023, data de vigência da Resolução Conjunta, o que a amostra ainda não permite avaliar.

## O que isso dá a quem previne, a quem julga e a quem acusa

| Família | Ponto de controle que a base revela | Indicador que o caso traz |
| --- | --- | --- |
| Imita instituição | autenticação que não dependa de segredo recitável; nenhum recolhimento de cartão; confirmação por canal próprio do banco antes de operação pedida por "segurança" | senha, código ou cartão entregue; ligação de "central"; crédito contratado e transferido em seguida |
| Ataca a conta ou o aparelho | vínculo do dispositivo; reforço de autenticação para empréstimo e para Pix a destinatário novo | celular roubado ou tomado; contratação de crédito na sequência |
| Imita relação pessoal | alerta quando o nome do recebedor não é o de quem a vítima julga pagar | conta em nome de estranho, que o comprovante registra; vítima idosa |
| Imita oferta | monitoramento da conta de destino: crédito alto e saída imediata | conta recente, repasse ou saque no mesmo dia |
| Manipula o pagamento | conferência do crédito na conta do lojista, não do comprovante | comprovante de Pix falso, cartão alheio, valor alterado na maquininha |

Para quem julga a reparação, a família do artifício antecipa quem já pagou: nas fraudes que imitam o banco ou atacam a conta, o prejuízo pode ter mudado de titular antes da sentença, e a questão 3 mostrou que a reparação é negada nesses casos. Para quem acusa, o aumento pela idade já é capitulado com regularidade, e a vulnerabilidade que a denúncia poderia narrar além da idade é a do serviço: a falsa central que usa o nome e o roteiro do banco é o mesmo golpe contra o jovem e contra o idoso, e o que a idade muda, na base, é a frequência com que esse roteiro aparece.

## Limites

A denúncia narra o crime, não o serviço; o que o banco fez, quando o fez e o que deixou de fazer está no inquérito, nos extratos e nas ações cíveis, que não foram lidos. As reações do banco e os ressarcimentos são o que a peça penal registra, e por isso pisos. A família do artifício vem da codificação validada nas questões anteriores, mas os pontos do serviço são triagem por termos, conferida por leitura dos trechos e não por codificação independente. A comparação de valores usa o prejuízo narrado e não distingue o valor recuperado. A Resolução BCB nº 343/2023 foi lida em reprodução (LegisWeb e Normas Brasil), e a data de vigência da Resolução Conjunta nº 6 vem de comentários de escritórios e imprensa especializada, não do texto.

## Fontes conferidas nesta sessão

- Súmula 479 do STJ, portal do STJ: https://scon.stj.jus.br/SCON/sumstj/toc.jsp?sumula=479.num.
- Lei 8.078/1990 (CDC), art. 14, caput, §1º e §3º: https://www.planalto.gov.br/ccivil_03/leis/l8078compilado.htm
- Lei 9.613/1998, art. 10, I (identificação do cliente): https://www.planalto.gov.br/ccivil_03/leis/l9613compilado.htm
- Código Penal, art. 61, II, h; art. 155, §4º-C, II; art. 171, §§2º-A, 2º-B e 4º: https://www.planalto.gov.br/ccivil_03/decreto-lei/del2848compilado.htm
- Resolução Conjunta CMN/BCB nº 6/2023, art. 1º e objeto, no Voto BCB 153/2023 e em Normas Brasil: https://normativos.bcb.gov.br/Votos/BCB/2023153/Voto_do_BC_153_2023.pdf e https://www.normasbrasil.com.br/norma/resolucao-conjunta-6-2023_445771.html; vigência em 1º de novembro de 2023 segundo Mattos Filho, https://www.mattosfilho.com.br/unico/resolucao-dados-fraudes/
- Resolução BCB nº 343/2023, art. 2º, I, em reprodução: https://www.legisweb.com.br/legislacao/?id=450442
- Questões 1, 3 e 5: `docs/analise/q1-alcance-elo-fisico.md`, `docs/analise/q3-tipologia-dano.md`, `docs/analise/q5-tempo-dado.md`
