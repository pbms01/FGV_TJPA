# Questão 4: o que a acusação trata como organização na fraude eletrônica, e o que a denúncia narra da estrutura

Nota analítica de 21/11/2026, sobre a base da fase 1 (TJSP). Tabelas reproduzíveis por `python3 scripts/analise_q4_organizacao.py`, que grava `dados/analise/q4_organizacao.csv` (uma linha por denúncia) e `dados/analise/q4_resumo.json`. A leitura das denúncias é de `scripts/organizacao.py`, que se valida com `python3 scripts/organizacao.py valida`. Linha de pesquisa atendida: 2.1 (organização e enquadramento), com reflexo na 2.2 (gargalos logísticos) e no eixo da seletividade do controle. Usa os eixos de `scripts/eixos_mediacao.py` e o nível alcançado da questão 1 (`claude/analise-q1-alcance-elo-fisico.md`).

## Resposta

A fraude eletrônica que chega à sentença no TJSP é processada como obra de poucos e quase nunca como organização. Há um único denunciado em 73,1% das denúncias FE e em 52,6% das CL, e só 9 das 194 denúncias da tipologia reúnem quatro ou mais. A acusação enquadra o concurso como associação criminosa (art. 288 do CP) em 10 denúncias e como organização criminosa (Lei 12.850/2013) em 3; as demais ficam no concurso de pessoas ou na autoria singular. O que a denúncia narra é a camada da rede que tocou o mundo físico: o titular de conta sozinho diante de uma rede não identificada (metade das denúncias FE e CL), vários titulares do mesmo golpe reunidos no mesmo processo (31,7% no CL) e pequenos grupos de dois ou três com papéis complementares (a conta e a linha, a conta e a execução presencial). Coordenação aparece em 14 das 65 denúncias com mais de um denunciado, atribuída a um denunciado em 8 e a pessoa não denunciada em 6, e hierarquia, em uma (INV 2). É o desenho que Leukfeldt, Lavorgna e Kleemans (2017) acharam em 40 redes de fraude bancária na Holanda, na Alemanha, no Reino Unido e nos Estados Unidos, nenhuma com hierarquia estrita e várias com três camadas: um núcleo que coordena, facilitadores e "money mules". A diferença está no recorte: a base brasileira vê quase só a camada das mulas e dos elos locais, o componente do dinheiro que Lusthaus et al. (2024) separam do componente do golpe.

O enquadramento como organização não acompanha a estrutura narrada. Das 13 imputações de associação ou organização criminosa, 4 recaem sobre um único denunciado associado a pessoas não identificadas. Dos 9 grupos com papéis complementares e coordenação narrada, 6 foram enquadrados como associação ou organização e 3 ficaram no concurso de pessoas (FE 107, FE 24, FE 55). Dos 4 grupos que preenchem, numa leitura conservadora, o critério do art. 1º, §1º, da Lei 12.850 (quatro ou mais denunciados com divisão de papéis), dois foram denunciados por organização criminosa e dois por associação criminosa. Na sentença, o 288 foi acolhido em 6 das 10 imputações, inclusive contra dois denunciados únicos e contra oito executores sem divisão de papéis narrada (FE 31), e afastado em 4, duas delas contra grupos com coordenação narrada (FE 97 e FE 102). O que decide é a prova do vínculo associativo, e a amostra é pequena demais para dizer que critério a sentença usa para dá-la por feita.

## Base e método

A unidade é a denúncia sem duplicatas, com o peso amostral do processo e percentuais ponderados dentro de cada estrato, como nas questões anteriores. Ficam fora as quatro denúncias fora da tipologia (INV 40, CL 12, CL 25 e FE 123), restando 33 no INV, 48 no CL e 113 na FE.

O número de denunciados é lido nos nomes em maiúsculas da capitulação e nos nomes do texto integral seguidos de qualificação, com a deduplicação e as exceções descritas em `organizacao.py`. Contra a contagem à mão das 29 denúncias da matriz, a regra acerta 26; os três erros (uma vítima em maiúsculas no FE 79, o OCR degradado do CL 1 e um nome repetido com grafia diferente no CL 56) e os demais achados na revisão das denúncias plurais e das com contagem duvidosa estão em `N_MANUAL`, com o que a contagem final acerta as 29. O enquadramento vem da capitulação: Lei 12.850 ou "organização criminosa", depois 288, depois concurso de pessoas (art. 29 na capitulação ou, na narrativa, ajuste prévio, unidade de desígnios, comparsas ou coautores não identificados), e o resto é autoria singular.

A estrutura do grupo foi lida pelo assistente nas 65 denúncias com dois ou mais denunciados e nas 4 de denunciado único com 288 ou Lei 12.850 (dicionário `ESTRUTURA`), a partir da nota da codificação e dos trechos de contexto dos termos de coordenação, recrutamento e parentesco, não do texto integral. Para cada uma registrou-se a divisão de papéis entre os denunciados, a coordenação narrada, o vínculo pessoal entre eles e a reiteração. Daí a estrutura narrada, em cinco tipos:

| Tipo | O que a denúncia narra |
| --- | --- |
| Autor isolado | um denunciado que executa o fato, sem coautores narrados |
| Nó isolado de rede não identificada | um denunciado com coautores não identificados, ou titular de conta ou elo logístico, que a codificação já define como peça de esquema executado por outro |
| Pluralidade sem divisão de papéis | dois ou mais denunciados no mesmo papel: titulares de conta do mesmo golpe, em paralelo ou em cadeia, ou executores do mesmo ato |
| Papéis complementares | dois ou mais denunciados com ao menos dois papéis distintos (captação ou execução, conta, saque ou recolha, insumo técnico, recrutamento) |
| Papéis complementares com coordenação | o mesmo, com a denúncia atribuindo a alguém, denunciado ou não, organizar, recrutar ou dirigir |

Os dois tipos penais usam critérios diferentes. O art. 288 do CP, na redação da Lei 12.850/2013, pune associarem-se 3 ou mais pessoas para o fim específico de cometer crimes, com reclusão de 1 a 3 anos. O art. 1º, §1º, da Lei 12.850 define organização criminosa como a associação de 4 ou mais pessoas estruturalmente ordenada e caracterizada pela divisão de tarefas, ainda que informalmente, com o objetivo de obter vantagem mediante infrações penais cujas penas máximas sejam superiores a 4 anos, ou de caráter transnacional. As figuras da fraude da amostra passam desse limiar de pena (o 171 caput vai a 5 anos, o §2º-A a 8, o 155 §4º-B a 10), mas o 154-A caput, com máximo de 4 anos, não passa sozinho. Na fraude, portanto, o que separa a organização criminosa da associação e do concurso é a estrutura, e não a pena.

## Primeira etapa: quantos a denúncia reúne

| Denunciados | INV (33) | CL (48) | FE (113) |
| --- | --- | --- | --- |
| 1 | 25 (75,8%) | 25 (52,6%) | 79 (73,1%) |
| 2 | 4 (12,1%) | 14 (28,4%) | 28 (22,4%) |
| 3 | 2 (6,1%) | 4 (8,9%) | 4 (2,7%) |
| 4 ou mais | 2 (6,1%) | 5 (10,1%) | 2 (1,8%) |

O denunciado único é a regra na fraude e na invasão, e o CL, que já fala em conta laranja, é o estrato com mais pluralidade. Entre as denúncias de um só denunciado, a narrativa declara coautores não identificados em 84,0% no CL e em 48,2% na FE; na FE, a parte que não declara inclui titulares a quem a denúncia atribui o golpe inteiro pela conta, que é a inferência registral da questão 1. A pluralidade segue a distância, como o alcance da questão 1. No CL, as denúncias de contato próximo com a vítima (maquininha, roubo e extorsão com transferência) reúnem dois ou mais denunciados em 8 de 9, contra 38,7% das de contato à distância: quem está junto da vítima é preso junto, e de longe chega-se às contas.

Das 9 denúncias com quatro ou mais denunciados, quatro reúnem só titulares de conta do mesmo golpe (FE 53, CL 42, CL 16, CL 52), uma reúne oito executores flagrados juntos (FE 31) e quatro descrevem divisão de papéis (INV 2, INV 36, CL 15, CL 56). O número, sozinho, não diz nada sobre organização: seis titulares de conta de uma mesma vítima idosa (CL 52) são seis mulas, não uma organização.

## Segunda etapa: o que a denúncia narra da estrutura

| Estrutura narrada | INV (33) | CL (48) | FE (113) |
| --- | --- | --- | --- |
| Autor isolado | 18 (54,5%) | 1 (1,9%) | 23 (22,9%) |
| Nó isolado de rede não identificada | 7 (21,2%) | 24 (50,7%) | 56 (50,2%) |
| Pluralidade sem divisão de papéis | 2 (6,1%) | 15 (31,7%) | 15 (13,5%) |
| Papéis complementares | 2 (6,1%) | 7 (13,5%) | 14 (8,9%) |
| Papéis complementares com coordenação | 3 (9,1%) | 1 (2,2%) | 5 (4,5%) |
| Indeterminada | 1 (3,0%) | 0 | 0 |

Na fraude, a denúncia típica é a de um nó: metade das denúncias CL e FE tem um único denunciado que a própria narrativa situa numa rede maior, quase sempre o titular da conta. Quando há mais de um denunciado, a divisão de papéis aparece em 32 das 65 denúncias plurais, mas a forma dominante no CL é a de titulares em paralelo ou em cadeia (15 de 23): várias contas que receberam o dinheiro do mesmo golpe, sem que nenhum dos denunciados tenha falado com a vítima. Os papéis complementares, quando aparecem, são poucos e locais: um habilita a linha e outro abre a conta (FE 61), um rende a vítima e a outra fornece a conta e saca (CL 1), dois aplicam o golpe da maquininha e um terceiro recebe (FE 105), uma negocia e o companheiro é o titular (FE 1).

A coordenação é narrada em 14 das 65 denúncias plurais. Em 8, a denúncia atribui a um denunciado organizar, recrutar ou dirigir: a dona de correspondente bancário que monta consignados com o marido, o filho e funcionários "cooptados" (INV 36), o grupo de SIM swap com "atribuições e hierarquia definidas" e operadores de telefonia (INV 2), a prima que orienta os repasses (INV 32), o tio que coordena as compras com dados de terceiros, ao lado da sobrinha e de outro denunciado (FE 102), o denunciado que recruta os comparsas, divide as tarefas e engana a vítima (FE 55), o "consultor" que capta contas para golpes por 10 a 30% dos valores (FE 24), quem organiza e recruta dois titulares (FE 107) e a colega de trabalho que pede ao denunciado a solicitação dos cartões que ele foi preso ao retirar (FE 97). Em 6, o coordenador é alguém que a denúncia nomeia ou supõe e não alcança: "Lobo", líder de quem dois denunciados cooptavam titulares (CL 15), "Max", para quem uma titular convertia o dinheiro em bitcoin por 5% (FE 45), e os comparsas que invadem a conta, habilitam a linha ou fazem o anúncio enquanto os denunciados só recebem (CL 10, CL 19, CL 42, FE 88). O mesmo se dá, com um só denunciado, no policial que vendia consultas a uma organização de pelo menos quinze não identificados (INV 11). Hierarquia, no sentido de escalões e comando, só é dita no INV 2.

Dois traços distinguem os grupos em que o núcleo foi alcançado. O primeiro é o sistema como objeto: dos 9 grupos com coordenação narrada, 5 atacaram um sistema (a base do INSS, o chip das vítimas, contas bancárias, o WhatsApp da vítima, o sistema da empresa de benefícios), contra 4 de engano à vítima, embora as denúncias plurais com sistema-objeto sejam 13 e as com sistema-meio, 52. Quando a fraude exige ataque técnico, a denúncia tende a vir de investigação mais extensa, como as que sustentam o INV 2 e o INV 36, e o núcleo aparece. O segundo é o vínculo pessoal: das 65 denúncias plurais, 11 narram parentesco, relação conjugal ou de trabalho entre denunciados, e 6 delas estão entre os 9 grupos coordenados (INV 2, INV 36, INV 32, FE 55, FE 102 e FE 97). O núcleo alcançado é, com frequência, uma família, um casal ou uma equipe de trabalho. A reiteração (vários fatos, várias vítimas ou um período narrado) aparece em 14 das 65, e o mesmo grupo responde a processos diferentes por fatos diferentes (CL 56 e FE 105 têm três denunciados em comum), sem que um processo veja o outro.

O recrutamento da conta, que é o ponto de contato entre a camada das mulas e o resto da rede, aparece pouco e pelo lado do titular. Sete denúncias dizem a quem o titular emprestou a conta: a um amigo de prenome "Lucio" (CL 35), a um vizinho já falecido (CL 40), a um conhecido de vulgo "Dodô" (FE 5), a um terceiro desconhecido menor de idade (FE 73), ao primo (FE 55) e a corréus (FE 126 e CL 7). Seis registram a remuneração: R$ 50 prometidos pelo primo (FE 55), cerca de 10% transferidos a outra conta própria (FE 35), 10% retidos (FE 88), 5% por operação (FE 45), 20% dos valores (INV 32) e 10 a 30% para o captador de contas (FE 24). A remuneração em percentual do golpe é um indício de participação no lucro, não de simples aluguel da conta, e a questão 1 a propôs como indicador da adesão ao golpe, que é o que decide entre o §2º-A e o inciso VII.

## Terceira etapa: enquadramento e sentença

| Enquadramento na denúncia | INV (33) | CL (48) | FE (113) |
| --- | --- | --- | --- |
| Organização criminosa (Lei 12.850) | 3 (9,1%) | 0 | 0 |
| Associação criminosa (art. 288) | 3 (9,1%) | 2 (4,1%) | 5 (4,6%) |
| Concurso de pessoas | 9 (27,3%) | 42 (87,5%) | 75 (62,3%) |
| Autoria singular | 18 (54,5%) | 4 (8,4%) | 33 (33,1%) |

| Caso | Imputação | Denunciados | Estrutura narrada | Sentença |
| --- | --- | --- | --- | --- |
| INV 2 | organização criminosa | 7 | complementar, coordenação por denunciado | três rés condenadas por organização criminosa e lavagem |
| INV 36 | organização criminosa | 9 | complementar, coordenação por denunciada | não lida (texto cortado antes do dispositivo) |
| INV 11 | organização criminosa | 1 | nó de organização não identificada | condenação só no 154-A |
| INV 28 | associação | 3 | complementar | absolvição do 288 |
| INV 32 | associação | 3 | complementar, coordenação pela prima | condenação no 288 |
| INV 21 | associação | 1 | nó isolado | condenação no 288 |
| CL 15 | associação | 6 | complementar, líder não denunciado | condenação no 288 de quatro réus |
| CL 56 | associação | 7 | complementar | condenação no 288 |
| FE 52 | associação | 1 | nó isolado | condenação no 288 |
| FE 54 | associação | 1 | nó isolado | absolvição do 288, a pedido do MP |
| FE 97 | associação | 2 | complementar, coordenação por denunciada | absolvição do 288 |
| FE 31 | associação | 8 | execução conjunta | condenação no 288 (DJEN) |
| FE 102 | associação | 3 | complementar, coordenação por denunciado | absolvição do 288 |

A organização criminosa aparece só no INV, nas duas operações com investigação de fôlego (INV 2 e INV 36) e na imputação ao policial que vendia consultas a uma organização de que nenhum outro membro foi identificado (INV 11). Na fraude dos estratos CL e FE, a imputação de grupo é o 288, e nunca a Lei 12.850, inclusive nos dois grupos que preenchem o critério do art. 1º, §1º, na leitura conservadora: CL 15, com seis denunciados, líder narrado e quinze fatos, e CL 56, com sete denunciados, execução e contas divididas e o mesmo grupo processado também no FE 105.

O 288 é usado de dois modos. Num, descreve um grupo efetivamente narrado, com três ou mais denunciados e papéis distintos (CL 15, CL 56, INV 32, INV 28, FE 102). No outro, imputa a um único denunciado a associação com pessoas não identificadas (FE 52, FE 54, INV 21), o que converte a rede invisível em crime autônomo do único alcançado: "associou-se em 3 (três) ou mais pessoas, para o fim específico de cometer crimes", diz a denúncia do FE 54 sobre quem recebeu os cartões do motoboy. A sentença não separa os dois modos: condena dois dos três denunciados únicos e os oito executores do FE 31, e absolve no FE 97 e no FE 102, em que a denúncia narra quem pedia e quem coordenava. Com dez imputações, a amostra não permite dizer que a sentença acompanha ou contraria a estrutura narrada; permite dizer que não a segue de modo visível.

## Leitura criminológica

No elemento infrator (linha 2.1), a resposta à pergunta de Leukfeldt, Lavorgna e Kleemans é, na base, a da cooperação frouxa e do recorte. A fraude eletrônica processada no TJSP é cibercrime que é organizado, no sentido de que depende de papéis distintos (quem engana, quem fornece a conta, quem saca, quem recolhe o cartão), mas não é processada como crime organizado, porque o processo só vê um ou dois desses papéis de cada vez. A estrutura que os autores encontraram em autos de investigação policial (núcleo, facilitadores, mulas) aparece aqui por fragmentos: o núcleo em 9 denúncias e as mulas na maior parte delas, com os facilitadores locais (a linha, a maquininha, o motoboy) no meio. A ausência de hierarquia, que no estudo deles é um achado sobre as redes, é aqui também um efeito da fonte, que não teria como mostrá-la.

No elemento controle social, o enquadramento depende da investigação e não da estrutura. A organização criminosa aparece nas investigações mais extensas (o GAECO no INV 36, a apuração do SIM swap com operadores de telefonia no INV 2), e o núcleo é alcançado sobretudo quando o sistema é o objeto do ataque. Na fraude contra a pessoa, que é a maior parte do volume, a investigação que para na primeira conta (questão 1) produz denúncias de nó isolado ou de contas em paralelo, e o 288 contra o denunciado único é a forma de a acusação registrar, no tipo penal, a rede que não investigou. O vínculo pessoal entre os denunciados dos grupos coordenados (família, casal, colegas) indica que as redes alcançadas são as de proximidade social, e que as redes formadas entre pessoas que não se conhecem ficam fora do processo.

## Produto para quem investiga, acusa, julga ou previne

Para a acusação e o julgamento, a base devolve critérios observáveis para o art. 1º, §1º, da Lei 12.850 na fraude eletrônica, que separam a organização da associação e do concurso. Primeiro, a contagem de pessoas com papel narrado, identificadas ou não, porque o tipo exige quatro pessoas e não quatro denunciados, e a denúncia que fala em "terceiros não identificados" sem dizer quantos nem o que faziam não deveria sustentar nem o 288 nem a organização. Segundo, a divisão de tarefas entre funções distintas (captação, conta, saque ou recolha, insumo técnico, recrutamento), e não a soma de titulares do mesmo golpe, que é pluralidade de mulas. Terceiro, a ordenação, lida em indícios concretos: quem recruta, quem paga e como (o percentual sobre o golpe, no FE 24, no FE 45 e no INV 32), quem dá as orientações (a prima do INV 32) e a quem se presta contas (o "comprovante da operação" exibido à coordenadora no INV 36). Quarto, a estabilidade: mais de uma vítima, um período, o mesmo grupo em outros processos. Quinto, a pena máxima das infrações visadas, que na fraude passa de 4 anos e no 154-A caput, sozinho, não passa.

Para a investigação, o ponto de entrada no núcleo é o recrutamento da conta. O titular que diz ter emprestado a conta a um amigo, a um vizinho ou a um conhecido de apelido está indicando o elo seguinte, e a base mostra que esse elo quase nunca é seguido. A consulta cruzada de processos pelos titulares e pelas contas recebedoras mostraria grupos que hoje são processados em pedaços (CL 56 e FE 105).

Para a avaliação legislativa (linha 1.4), o 288 contra o denunciado único associado a não identificados merece atenção, porque cumula, sobre o único alcançado, a pena do crime e a de uma associação cuja existência a denúncia afirma e não descreve. A Lei 15.397/2026, ao criar o inciso VII para a cessão de conta, ofereceu uma figura para o titular que não adere ao golpe; o mesmo raciocínio vale para o 288, que deveria exigir a narrativa de quem são, ao menos por função, os outros associados.

## Vieses e pendências desta análise

Valem os vieses da base: só processos com sentença de primeiro grau publicada no TJSP, fora o segredo de justiça, com estratos definidos por termos da sentença. O segredo de justiça, que a base exclui, é mais provável nos processos com interceptação e colaboração premiada, de modo que a base tende a subestimar a organização criminosa. A estrutura do grupo é leitura do assistente sobre a nota da codificação e trechos de contexto, sem leitura integral e sem segundo leitor; o vínculo só é registrado quando a denúncia o narra; e a coluna de coautores não identificados vem da extração por regras, que perde grafias de OCR. Duas sentenças de organização criminosa foram lidas pelo DJEN ou ficaram sem dispositivo (INV 2, INV 36), e a do FE 31 também veio do DJEN. As imputações de 288 e de Lei 12.850 são 13, número que permite descrever e não estimar.

Ficam como passos desta questão: segundo leitor para o dicionário `ESTRUTURA`, com leitura integral das 65 denúncias plurais; codificação, nos acórdãos já coletados, de como o segundo grau trata o 288 contra o denunciado único; cruzamento de processos pelos nomes e pelas contas recebedoras, para medir quantos grupos a base processa em pedaços; e, na fase 2, a mesma medida no TJPA.

## Fontes conferidas nesta sessão

- Leukfeldt, E. R.; Lavorgna, A.; Kleemans, E. R. "Organised Cybercrime or Cybercrime that is Organised? An Assessment of the Conceptualisation of Financial Cybercrime as Organised Crime", European Journal on Criminal Policy and Research 23 (2017), 287-300, https://doi.org/10.1007/s10610-016-9332-z (40 casos; nenhuma rede com hierarquia estrita; núcleo, facilitadores e "money mules"), conferido no resumo e em trechos do texto (VU Research Portal e Springer).
- Lusthaus, J.; Kleemans, E.; Leukfeldt, R.; Levi, M.; Holt, T. "Cybercriminal networks in the UK and Beyond: Network structure, criminal cooperation and external interactions", Trends in Organized Crime 27 (2024), 364-387, https://doi.org/10.1007/s12117-022-09476-9 (divisão entre os componentes do golpe e do dinheiro; elementos offline e locais), conferido no resumo.
- Lei 12.850/2013, art. 1º, §1º, e art. 2º, caput (reclusão de 3 a 8 anos e multa): conferidos depois no texto do Planalto, https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2013/lei/l12850.htm, na sessão da questão 5; antes, pela norma atualizada da Câmara dos Deputados, https://www2.camara.leg.br/legin/fed/lei/2013/lei-12850-2-agosto-2013-776714-normaatualizada-pl.docx, e por reproduções.
- Art. 288 do CP, na redação da Lei 12.850/2013: em reprodução do texto compilado do Planalto (juridico.ai) e na Enciclopédia Jurídica da PUC-SP, não no Planalto.
- Penas do 171 caput, do §2º-A, do 155 §4º-B e do 154-A caput: conferidas no Planalto em sessões anteriores (notas das questões 1 e 2), não nesta.
