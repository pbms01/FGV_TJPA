# Questão 7: como o titular entra na fraude, segundo ele mesmo, e o que isso decide

Nota analítica de 21/11/2026, sobre a base da fase 1 (TJSP). Tabelas reproduzíveis por `python3 scripts/analise_q7_titular.py`, que grava `dados/analise/q7_titular.csv` (uma linha por denúncia) e `dados/analise/q7_resumo.json`. A leitura da versão, dos antecedentes e da idade é de `scripts/titular_conta.py`, que imprime com `python3 scripts/titular_conta.py valida` a versão e o trecho de cada uma das 101 denúncias. Linha de pesquisa atendida: 2.3, reduzida à entrada do titular da conta (recrutamento, remuneração, perfil e desfecho), com reflexo na 1.4 (o inciso VII da Lei 15.397/2026). Usa a questão 1 (desfecho) e a questão 4 (pedido e remuneração da conta).

## Resposta

O titular de conta denunciado sozinho conta, em quase metade dos casos, que entregou a conta: 47 das 101 denúncias de só conta trazem, na denúncia ou na sentença, a admissão de que a conta foi emprestada (28), vendida, alugada ou cedida por remuneração (18) ou entregue em resposta a anúncio de empréstimo (1). Outras 38 trazem a negativa ou a alegação de que a conta não é dele ou de que perdeu os documentos, 12 a ausência (revelia, não localização, silêncio) e 4 nenhuma versão. Quando diz a quem, o titular aponta um desconhecido (12), um conhecido ou cliente (8), um amigo, vizinho ou colega (5), um parente ou companheiro (2), um credor (2) ou um anúncio (1); em 17 não diz. Quando diz por quanto, o preço é pequeno: R$ 50, 150, 150, 200, 200, 200, 300, 500 e 500, e R$ 2.000 no caso de uma titular de 19 anos em dificuldade financeira (CL 45), com mediana de R$ 200. A questão 4 registra ainda remuneração em percentual (5% por operação, 10%, de 10 a 30% para o captador). A sentença declara primário o titular condenado em 41 casos e reincidente ou com maus antecedentes em 13, e registra a menoridade relativa (menos de 21 anos na data do fato) de algum réu em 12 processos.

A versão do titular decide menos a absolvição do que o tipo. Quem admite a cessão é condenado em 45 de 47 sentenças (95,7%); quem nega ou não reconhece a conta, em 30 de 37 (81,1%); quem está ausente, em 9 de 12. A admissão da cessão é, na prática, confissão do elemento material, que a sentença chega a chamar de "confissão qualificada" (CL 45), e o dolo é inferido dela. O que a versão não decide é a capitulação: das 45 condenações com cessão admitida, 27 ficaram no §2º-A, com pena mínima de 4 anos, e 6 no inciso VII criado pela Lei 15.397/2026, com a pena do caput; entre os 18 que disseram ter vendido ou alugado a conta, 9 foram condenados no §2º-A e 5 no VII. A mesma narrativa (cedi a conta, recebi pouco, não sei para quê) sustenta a condenação como autor da fraude eletrônica e como cedente.

Para quem acusa, isso tem duas consequências. A primeira é o acordo: a cota trata do ANPP em 68 das 101 denúncias e invoca a pena mínima em 46, porque 74 capitulam o §2º-A; o titular que admite a cessão já admitiu, muitas vezes na polícia, o fato que a confissão formal e circunstanciada do art. 28-A precisa cobrir, e no inciso VII o requisito de pena mínima inferior a 4 anos está atendido. A segunda é a investigação: a pergunta "a quem" é respondida em 30 das 47 admissões, com prenome ou apelido ("Lucio", "Dodô", "Gustavo", "Murian", "Naiara", "Renan", "Arnaldo"), e é o ponto de partida para a camada que recruta as contas, que a questão 4 mostrou quase nunca alcançada.

## Base e método

A unidade é a denúncia de só conta da FE e do CL (o titular é o único papel do denunciado, na codificação da questão 1): 101 denúncias, 42 no CL e 59 na FE, 100 delas com sentença. Quando há mais de um titular, a versão é a primeira que a leitura acha, e os antecedentes e a idade são os de qualquer réu da sentença; a unidade é o processo, não a pessoa.

A versão foi procurada frase a frase na narrativa e na cota da denúncia e no texto da sentença, só nas frases com verbo de declaração, interrogatório, versão, álibi, silêncio ou revelia, para não tomar a descrição da conduta pela acusação ("cedeu sua conta") como palavra do titular. A categoria mais específica vence: cessão mediante pagamento (venda, aluguel, porcentagem, contraprestação), proposta de trabalho, renda ou crédito, empréstimo a alguém, perda do controle ou não reconhecimento da conta, negativa, silêncio, não localização ou revelia. O verbo de cessão precedido de negação ("nunca vendeu, cedeu ou emprestou", "negou ter emprestado") conta como negativa. As ementas de acórdãos citadas na sentença saem antes da leitura, porque falam de outro réu (a mesma ementa, de um réu que "admitiu ter 'alugado' sua conta", aparece em três sentenças). As 101 leituras foram conferidas pelo trecho; 11 foram corrigidas à mão (`VERSAO_MANUAL`), quase todas porque a regra pegava a fala da vítima, do titular da linha ou do juiz. A versão vem da sentença em 58, da denúncia em 32 e da leitura manual em 11.

Antecedentes e idade vêm da dosimetria. Reincidência ou maus antecedentes afirmados vencem a primariedade, e a menção negada ("ausentes maus antecedentes", "não ostenta condenação apta a configurar maus antecedentes") não conta. Como a absolvição não tem dosimetria, os antecedentes são lidos entre os condenados. A idade é a menoridade relativa, reconhecida ou pedida, e as 12 menções foram conferidas; no FE 24 o réu de 20 anos é o captador, não o titular. A atenuante do art. 65, I, do CP alcança o agente "menor de 21 (vinte e um) anos, na data do fato", e o art. 115 reduz à metade os prazos de prescrição pelo mesmo critério.

## Primeira etapa: o que o titular diz

| Versão | CL (42) | FE (59) | Total |
| --- | --- | --- | --- |
| Cedeu mediante pagamento | 10 | 8 | 18 |
| Aceitou proposta de trabalho, renda ou crédito | 0 | 1 | 1 |
| Emprestou a alguém | 9 | 19 | 28 |
| Perdeu o controle ou não reconhece a conta | 2 | 6 | 8 |
| Nega | 12 | 18 | 30 |
| Silêncio | 1 | 0 | 1 |
| Não localizado ou revel | 6 | 5 | 11 |
| Sem versão | 2 | 2 | 4 |

No CL, mais titulares dizem ter vendido ou alugado a conta (10 de 42) do que na FE (8 de 59), onde predomina o empréstimo. A diferença é a do vocabulário da cessão: no CL ela aparece como negócio, com preço; na FE, como favor.

As admissões descrevem três entradas. A primeira é o favor a alguém próximo, que pede a conta por estar com a sua bloqueada (CL 34), para receber uma remuneração de trabalho (FE 68), um dinheiro de venda (CL 31) ou por dizer que o valor era alto (FE 109); o titular diz não saber para que a conta seria usada (FE 88, FE 115). A segunda é a venda a desconhecido, por R$ 150 a R$ 300, com o preço fixado por conta (CL 7: duas contas, R$ 150 cada) e às vezes por anúncio ("alegou ter vendido sua conta bancária a terceiros por meio de anúncio que viu no Facebook", CL 21). A terceira é a dívida ou a necessidade: o agiota a quem a conta pagaria a dívida (CL 36), o empréstimo procurado na internet (FE 37), a "dificuldade financeira" da titular de 19 anos (CL 45), o vendedor de balas a quem "um rapaz conhecido perguntou se o interrogando queria vender sua conta bancária" (CL 18). A remuneração em percentual (questão 4: FE 24, FE 35, FE 45, FE 88) é outra coisa: é participação no fluxo e indica adesão.

As negativas têm um padrão próprio, o da conta que o titular diz não reconhecer: a conta "fraudulentamente aberta em seu nome" (FE 114), os documentos perdidos (CL 47, FE 106, CL 43, "há 05 anos"), a foto dos documentos tirada por terceiro (FE 119), a situação de rua e o alcoolismo, com documentos perdidos "em diversas ocasiões" (FE 94). É a defesa que a biometria na abertura (questão 1) contesta, e a que mais absolve: 2 das 8 que não reconhecem a conta terminaram em absolvição.

## Segunda etapa: o que a versão decide

| Versão agrupada | Sentenças | Condenação | §2º-A | Inciso VII | Outros | Absolvição |
| --- | --- | --- | --- | --- | --- | --- |
| Cessão admitida | 47 | 45 (95,7%) | 27 | 6 | 12 | 2 |
| Nega ou não reconhece | 37 | 30 (81,1%) | 19 | 2 | 9 | 7 |
| Ausente | 12 | 9 (75,0%) | 7 | 0 | 2 | 2 |
| Sem versão | 4 | 4 | 3 | 0 | 1 | 0 |

"Outros" reúne o 171 sem o §2º-A, o 155, o 158 e o 180. A cessão admitida quase não absolve: as duas absolvições (CL 31, FE 18) são de titulares que disseram ter emprestado o cartão a um cliente ou os dados a um cunhado, e a questão 1 mostrou que a absolvição do titular se apoia, em 10 de 11 casos, na insuficiência de prova (art. 386, VII, do CPP). A negativa absolve um em cada cinco, porque obriga a acusação a provar o vínculo do titular com a conta, e é nesse terreno que a prova registral, a selfie e o extrato decidem.

A capitulação não acompanha a versão. Quem diz ter vendido a conta por R$ 150 ou R$ 200 (FE 101, FE 99) foi condenado no §2º-A, como autor da fraude, e quem diz o mesmo por R$ 200 ou R$ 500 (CL 39, CL 13) foi condenado no inciso VII. A questão 1 mostrou que o VII entrou nas sentenças por retroação benéfica, a pedido da defesa, e que 14 das 16 sentenças FE posteriores à lei sobre titulares não o mencionam. Aqui se vê o mesmo pelo lado da narrativa: o fato que o tipo novo descreve, "cede, gratuita ou onerosamente, conta bancária", é o que o titular diz em 47 das 101 denúncias, e a sentença o enquadra no VII em 6 delas.

Os antecedentes desenham um perfil. Entre os condenados, a sentença diz primário em 41, reincidente ou com maus antecedentes em 13 e não diz em 30. O jovem aparece em 12 processos com a menoridade relativa, reconhecida ou pedida. O titular típico da base é primário, recebe pouco e entra por um conhecido ou por um comprador de contas, e o processo o trata como autor de uma fraude cujo ardil foi de outro.

## O que isso dá a quem acusa, a quem julga e a quem previne

Para quem acusa, a admissão da cessão é o momento de escolher o tipo e de subir na cadeia. Nos fatos posteriores a 04/05/2026, a cessão confessada sem indício de adesão ao golpe cabe no inciso VII, e então o ANPP deixa de ser vedado pela pena mínima: o art. 28-A exige que o investigado tenha "confessado formal e circunstancialmente a prática de infração penal sem violência ou grave ameaça e com pena mínima inferior a 4 (quatro) anos", e o veda ao reincidente ou quando houver "conduta criminal habitual, reiterada ou profissional" (§2º, II). O acordo pode ter como condição, ou ser precedido de, a identificação de quem pediu a conta e por quanto, que as admissões da base já trazem em parte. O §2º-A com o art. 29 fica para quando houver o que a questão 1 chamou de adesão: o percentual, o saque e o repasse em espécie, o recrutamento de outras contas, o contato com a vítima.

Para quem julga, a versão do titular é o lugar onde a distinção entre cessão e participação tem de ser feita, e a base mostra que ela não está sendo feita pelo conteúdo da versão: o preço baixo, o desconhecimento do uso e o favor a conhecido aparecem igualmente nas condenações pelo §2º-A e pelo VII.

Para quem previne, a entrada do titular é barata e próxima. O preço mediano declarado é de R$ 200, o recrutamento passa por conhecidos e por compradores de contas, e um em cada oito processos tem réu com menos de 21 anos. A biometria na abertura não impede essa entrada, porque a conta é aberta pelo próprio titular e entregue depois.

## Limites

A versão é a que chega ao papel: o interrogatório gravado em mídia, que muitas sentenças não transcrevem, fica fora, e a sentença às vezes resume a versão nas palavras do juiz. As 101 leituras foram conferidas pelo trecho, não pelo texto integral. Antecedentes e idade só existem onde a sentença os diz, e a absolvição não tem dosimetria. O valor da cessão é o declarado pelo titular, dez vezes, e não há como saber se é o valor real. A comparação entre §2º-A e VII mistura fatos anteriores e posteriores à Lei 15.397/2026 e, como na questão 1, mede sobretudo a retroação.

## Fontes conferidas nesta sessão

- Código Penal, art. 65, I, e art. 115: https://www.planalto.gov.br/ccivil_03/decreto-lei/del2848compilado.htm
- Código de Processo Penal, art. 28-A, caput e §2º, II: https://www.planalto.gov.br/ccivil_03/decreto-lei/del3689compilado.htm
- Lei 15.397/2026 (inciso VII do §2º do art. 171): conferida no Planalto na questão 1, https://www.planalto.gov.br/ccivil_03/_Ato2023-2026/2026/Lei/L15397.htm
- Questões 1 e 4: `docs/analise/q1-alcance-elo-fisico.md`, `docs/analise/q4-organizacao.md`
