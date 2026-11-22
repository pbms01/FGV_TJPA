# Par TJPA 3, contraste: PA-FE 99

Par TJPA 3: PA-FE 24 (âncora) e PA-FE 99 (contraste). Questões examinadas: 1, 2, 3, 4 e 6. O que o par mostra está na ficha da âncora (`PA_FE_24.md`).

O que o contraste muda: a mesma leitura jurídica, furto mediante fraude com o sistema como instrumento, e o mesmo alcance, que chega ao autor porque o dinheiro caiu em empresa e contas dele. Muda quem ataca e de onde vem a prova: em vez do agente externo que explora a autenticação de um banco, os funcionários que administram o sistema de pagamentos da própria vítima; em vez do extrato e da confissão, os registros de acesso do sistema da empresa, a auditoria interna e os relatórios de inteligência financeira. E muda o desfecho: todos os boletos denunciados, lavagem com habitualidade, 11 anos em regime fechado e o produto destinado à vítima.

## Identificação

- Fase 2 (TJPA), fora da base extraída no main; código pela mesma regra da âncora. Família FE (consulta FE do DJEN); o órgão de primeiro grau não veio na lista do DJEN.
- Vara de Combate ao Crime Organizado de Belém (sentença assinada por dois juízes); apelação julgada pela 1ª Turma de Direito Penal do TJPA.
- Datas: fatos de 15/09/2014 a 01/12/2015; inquérito da divisão de crimes tecnológicos da Polícia Civil, de 2016; denúncia do GAECO de 20/09/2018, recebida em 03/10/2018; desmembramento do processo originário para os dois apelantes (art. 80 do CPP); sentença de 22/07/2024; acórdão de 01/10/2026, por unanimidade; embargos de declaração e recursos especial e extraordinário interpostos em outubro de 2026. Do primeiro fato à denúncia, 48,2 meses; do último, 33,6; do recebimento da denúncia à sentença, 69,6.
- Peças lidas: a denúncia, em quatro partes, nos trechos da narrativa, da individualização e dos pedidos; a sentença e o acórdão, por inteiro (este baixado pelo link do original no PDPJ em 22/11/2026 e gravado em `textos/tjpa/acordaos/0811772-81.2024.8.14.0401/`).
- Não passou pelo segundo leitor.
- Partes, pela função: os dois réus deste processo, um gestor com acesso direto ao banco de dados do sistema da empresa e um técnico de contabilidade e informática com perfil no sistema, sócios da empresa de fachada que recebia os pagamentos; a empresa vítima, um grupo varejista de Belém; funcionários do setor de contas a pagar, alguns corréus em autos desmembrados; a filha de um corréu, que abriu conta a pedido do pai; o banco pagador.

## 1. Conduta registrada

Os pagamentos do grupo seguiam um fluxo: o setor de contas a pagar conferia os títulos no sistema de gestão da empresa, gerava o arquivo de pagamento e o enviava pelo site do banco, que pagava e devolvia o arquivo de retorno. Os réus, com acesso ao banco de dados do sistema, alteravam o código de barras e o beneficiário de boletos legítimos que aguardavam pagamento e acrescentavam parcelas a boletos já pagos, de modo que o arquivo enviado ao banco pagava a "M & J Serviços Contábeis e Tecnologia", empresa constituída por eles. Também foram usados boletos falsos com empresas de terceiros como cedentes. Uma das contas da empresa de fachada recebeu R$ 3.815.604,00 entre 15/09/2014 e 01/12/2015, e as contas pessoais dos réus receberam R$ 1.739.501,02 e R$ 1.302.431,90.

Dois traços técnicos. Um notebook ficava escondido num armário do setor de contabilidade, ligado o tempo todo, conectado à rede interna por um cabo passado por um furo feito no móvel por ordem de um dos réus, e operado à distância pelo TeamViewer. E a alteração foi feita direto no banco de dados, sem registro de criação ou de alteração dos títulos, de modo que o analista da empresa fornecedora do sistema não achou rastro; o que restou foram os registros de acesso do sistema, que mostraram o perfil de um dos réus em 24 boletos adulterados.

A fraude apareceu por dois caminhos: boletos de fornecedores pagos duas vezes, que o coordenador de segurança da empresa levou à polícia, e o arquivo de 24/11/2014 que o banco devolveu sem pagar três títulos (R$ 177.648,36). Um dos réus ofereceu a uma funcionária R$ 4.000,00 por boleto para que ela mudasse para o setor de contas a pagar.

O sistema é o instrumento da subtração; o canal é a rede interna da empresa, com acesso remoto; não há contato com a vítima.

O que a denúncia não narra, ou o processo não fez: a perícia do notebook, que nunca foi feita; e o pedido de reparação do art. 387, IV, do CPP, substituído pelo pedido de perdimento dos bens (art. 91, II, do CP).

## 2. Processamento

Investigação. Inquérito da divisão de crimes tecnológicos, com quebras dos sigilos bancário e fiscal (2016) e telefônico (2017), sequestro de bens (2017), prisões preventivas e busca e apreensão (2018), relatórios de inteligência financeira e relatório de análise de dados e de patrimônio. A prova da autoria vem do sistema da própria vítima, da auditoria interna e do caminho do dinheiro.

Denúncia (GAECO): art. 155, §4º, II, do CP, art. 1º da Lei 9.613/1998 e art. 2º da Lei 12.850/2013, contra vários denunciados, com pedido de perdimento dos bens sequestrados.

Sentença (22/07/2024). Procedência parcial.

- Absolvição pela organização criminosa, com a leitura de precedente segundo o qual ela exige hierarquia entre os integrantes; a vara especializada mantém a competência para os crimes conexos (art. 81 do CPP).
- Condenação por furto qualificado (art. 155, §4º, II e IV), em continuidade, por lavagem com a habitualidade (art. 1º, caput, §2º, I, e §4º, da Lei 9.613) e por associação criminosa (art. 288 do CP, 2 anos).
- Pena de 16 anos e 8 meses, regime fechado, 366 dias-multa, para cada réu.
- Perdimento dos bens e valores sequestrados "em favor da empresa vítima".
- O notebook não periciado não pesa, porque a condenação não se baseia em dados dele.

Segundo grau (01/10/2026). Só as defesas apelaram. A 1ª Turma, por unanimidade, deu provimento parcial:

- rejeita a nulidade pela atuação do GAECO, a inépcia, superada pela sentença, e o cerceamento pela falta de perícia no notebook, porque a autoria está nos registros de acesso, na auditoria, nos documentos bancários e na prova oral;
- declara de ofício a prescrição da associação criminosa: pena de 2 anos, prazo de 4 (art. 109, V, do CP), e mais de cinco anos entre o recebimento da denúncia e a sentença;
- mantém o furto mediante fraude e afasta o estelionato: os réus não induziram a empresa a aprovar pagamentos, alteraram "sub-repticiamente" títulos legítimos, e a fraude serviu para burlar a vigilância da vítima, na redação anterior à Lei 14.155/2021;
- mantém a lavagem, pela empresa de fachada e pela pulverização dos valores ao longo de mais de um ano, com a habitualidade;
- reconhece a tentativa nos três títulos que o banco não pagou, sem efeito na pena, porque a continuidade com sete ou mais crimes mantém a fração de dois terços (Súmula 659 do STJ, como transcrita);
- refaz as penas-base pelo critério de um oitavo do intervalo, por falta de fundamento concreto para frações maiores, e chega a 11 anos em regime fechado e 231 dias-multa para cada réu.

## 3. Leitura pelas questões

### Questão 1: quem o sistema alcança

Onde o caso está. Como a âncora, o contraste está entre os casos em que o autor é alcançado porque recebeu em conta própria (31,2% das 79 FE pela internet, no TJSP), aqui pela empresa que os próprios réus constituíram.

O mecanismo. A prova veio de três fontes que não vencem em meses: o sistema da vítima, a auditoria dela e o caminho bancário. A alteração direta no banco de dados apagou o rastro da criação dos títulos, mas não o registro de quem acessou o sistema, e foi esse registro que nomeou o perfil de um dos réus. A investigação durou anos, e os dados que decidiram estavam com a vítima e com os bancos, e não com provedores de aplicação sujeitos ao prazo de guarda (questão 5).

O acréscimo ao magistrado. O momento são os requerimentos na investigação. O aparelho de acesso remoto escondido no armário era a prova de quem operava o sistema, e nunca foi periciado; a defesa fez disso tese de cerceamento, que o acórdão rejeitou porque a autoria tinha outra prova. Quando o ataque é interno, a perícia cedo do equipamento e a preservação dos registros do sistema da vítima são o que o juiz pode deferir antes que a própria empresa os altere ou os perca.

### Questão 2: o que a eliminação do sistema separa

Onde o caso está. Na base do TJSP, a invasão de conta ou de sistema recebe quatro capitulações na denúncia e outras quatro na sentença. O contraste ficou no furto qualificado da denúncia ao acórdão, que respondeu de frente à tese do estelionato.

O mecanismo. A empresa pagou, mas não consentiu em pagar aos réus: pagou o que o sistema, alterado, apresentava como dívida com fornecedores. A fraude burlou a vigilância, e o pagamento não foi entrega voluntária ao agente. É a mesma linha que separa a âncora do §2º-A.

O acréscimo ao magistrado. O momento é a sentença. Para fatos posteriores à Lei 14.155/2021, a mesma conduta cabe no §4º-B, porque é furto mediante fraude cometido por meio de dispositivo informático, "conectado ou não à rede de computadores", e hoje com pena de 4 a 10 anos; para os fatos de 2014 e 2015, cabe o §4º, II (fraude) e IV (concurso), com pena de 2 a 8 anos, como decidiram as duas instâncias. A conduta é a mesma da âncora; a diferença de pena mínima é da data.

### Questão 3: o dano e a reparação

Onde o caso está. Na base do TJSP, a reparação foi omitida em 58 das 171 condenações. O contraste não tem reparação do art. 387, IV, mas tem o que a âncora não tem: sequestro de bens desde 2017 e perdimento em favor da vítima na sentença. E o banco pagador barrou três títulos (R$ 177.648,36), o que o acórdão leu como tentativa.

O mecanismo. A proteção da vítima veio da medida assecuratória feita cedo e da sentença que deu destino ao que foi sequestrado. O art. 91, II, do CP põe a perda em favor da União com a ressalva do "direito do lesado", e o art. 133, §1º, do CPP manda recolher aos cofres públicos só o que não couber ao lesado; a sentença foi direto ao lesado.

O acréscimo ao magistrado. O momento é a sentença: dizer o destino do que foi bloqueado ou sequestrado. É a decisão que faltou na âncora.

### Questão 4: o que a acusação trata como organização

Onde o caso está. Na base do TJSP, o enquadramento não acompanha a estrutura narrada: das 13 imputações de associação ou organização, 4 recaem sobre um único denunciado, a associação criminosa foi acolhida em 6 das 10 imputações, e só 4 grupos preenchem, numa leitura conservadora, o critério do art. 1º, §1º, da Lei 12.850. O contraste é um grupo com divisão de tarefas narrada (o acesso ao banco de dados, o perfil no sistema, o setor de pagamentos cooptado, a empresa de fachada, a conta aberta pela filha de um corréu), com imputação de organização criminosa pelo GAECO.

O mecanismo. A sentença absolveu da organização por falta de hierarquia e condenou pela associação, e a associação prescreveu no segundo grau, porque a pena de 2 anos prescreve em 4 e o processo levou 5 anos e 9 meses do recebimento da denúncia à sentença. A organização criminosa, pela lei, é a associação de 4 ou mais pessoas "estruturalmente ordenada e caracterizada pela divisão de tarefas, ainda que informalmente", com o objetivo de vantagem mediante infrações com pena máxima superior a 4 anos (art. 1º, §1º, da Lei 12.850). A hierarquia não está no texto; é exigência do precedente que a sentença seguiu (leitura desta ficha).

O acréscimo ao magistrado. São dois momentos. Na sentença, testar a organização contra os elementos do art. 1º, §1º, e não contra um requisito que a lei não traz. E, no curso do processo, o tempo: um crime de pena baixa, como a associação, prescreve pela pena aplicada enquanto o processo complexo anda, e só a duração do processo explica a perda dessa condenação.

### Questão 6: a pessoa ou o serviço

Onde o caso está. Na base do TJSP, as fraudes que passam pela segurança do serviço são as únicas em que alguém além da vítima responde pelo prejuízo. No contraste, o serviço explorado é o da própria vítima: o sistema de gestão e o fluxo de pagamentos da empresa.

O mecanismo. É a ameaça interna: quem administra o sistema pode alterar o banco de dados sem deixar registro, e o acesso remoto escondido tira o operador da sala. O controle que funcionou foi externo, o do banco pagador, que devolveu o arquivo com títulos inconsistentes.

O acréscimo ao magistrado. O momento é a dosimetria. O abuso do acesso privilegiado já qualifica o furto (o inciso II do §4º fala em "abuso de confiança, ou mediante fraude"), e o valor desviado foi valorado na culpabilidade do furto e da lavagem sem dupla valoração, como as duas instâncias decidiram. O acórdão mostra o limite: a gravidade não dispensa a fundamentação concreta da fração, e a falta dela custou 3 anos e 8 meses da pena; os outros 2 anos da diferença entre 16 anos e 8 meses e 11 anos caíram com a prescrição da associação.

## 4. Para a turma

As quatro questões estão publicadas como exercício com gabarito no artefato "Vinte e quatro boletos" (https://claude.ai/artifact/8aeNr5VRR8JthwjHpxQrtu), cuja fonte é `docs/aula/exercicios/tjpa03-pafe99.html`. O exercício traz o caso sem o desfecho, aponta para o da âncora e é apontado por ele.

Versão do caso para o exercício, sem o desfecho: o fluxo de pagamentos do grupo; a alteração de boletos no banco de dados, sem registro de alteração, e o pagamento à empresa dos réus; o notebook escondido e o TeamViewer; os registros de acesso com o perfil de um réu em 24 boletos; o banco que devolveu três títulos; os valores na empresa e nas contas pessoais; a denúncia do GAECO por furto qualificado, lavagem e organização criminosa. O exercício não diz o que a sentença e o acórdão decidiram; o gabarito diz.

1. Os réus alteraram boletos no sistema, e a empresa pagou. É furto mediante fraude ou estelionato, e em que redação? Resposta esperada: furto mediante fraude; a fraude burlou a vigilância, e a empresa não consentiu em pagar aos réus. Por fatos de 2014 e 2015, o §4º, II e IV (2 a 8 anos); depois da Lei 14.155/2021, o §4º-B. Desfecho: as duas instâncias afastaram o estelionato.
2. O GAECO imputou organização criminosa. O que a sentença e o acórdão fizeram com ela, e o que estava no texto da lei? Resposta esperada: a sentença absolveu por falta de hierarquia e condenou pela associação, que prescreveu no segundo grau (pena de 2 anos, mais de cinco anos até a sentença). O art. 1º, §1º, da Lei 12.850 pede 4 ou mais pessoas, estrutura e divisão de tarefas, e não hierarquia.
3. A alteração não deixou registro no banco de dados, e o notebook nunca foi periciado. De onde veio a prova da autoria, e o que se perdeu? Resposta esperada: dos registros de acesso do sistema da própria vítima, da auditoria e do caminho bancário, dados que não vencem como os de provedor. Perdeu-se a prova de quem operava pelo acesso remoto; a defesa a usou como tese, rejeitada porque havia outra prova.
4. O que protegeu a vítima? Resposta esperada: o banco que barrou três títulos (tentativa), o sequestro de bens desde 2017 e o perdimento em favor da empresa vítima na sentença. Pena final: 11 anos em regime fechado, depois de o acórdão refazer as penas-base pelo critério de um oitavo do intervalo.

## 5. Conferência

| Arquivo | Campo | Registrado | Lido | Situação |
| --- | --- | --- | --- | --- |
| `dados/djen/alvos_djen_tjpa.csv` | acao_penal, orgao_1g | 0; vazio | ação penal da Vara de Combate ao Crime Organizado de Belém | divergência registrada (linha 14 de `divergencias.csv`), não aplicada: o DJEN só trouxe publicações de segundo grau |
| `dados/codex_tjpa/status.csv` | detalhe | segundo grau; Vara de Combate ao Crime Organizado; organização criminosa com alteração do banco de dados do sistema do grupo para apagar títulos | o mesmo; o acórdão não reconhece organização, e a alteração foi de código de barras e beneficiário de títulos legítimos | confere no essencial |
| `textos/tjpa/manifesto.csv` | sentença | 22/07/2024 | o mesmo | confere |

Efeito nos números: nenhum.

## Fontes no repositório

Exercícios: contraste em https://claude.ai/artifact/8aeNr5VRR8JthwjHpxQrtu; âncora em https://claude.ai/artifact/Tq7W44YmrFo3j5Ho1aM9dE.

- PA-FE 99 (contraste): [denúncia](https://github.com/pbms01/FGV_TJPA/tree/main/textos/tjpa/denuncias/0811772-81.2024.8.14.0401), [sentença](https://github.com/pbms01/FGV_TJPA/tree/main/textos/tjpa/sentencas/0811772-81.2024.8.14.0401), [acórdão](https://github.com/pbms01/FGV_TJPA/tree/main/textos/tjpa/acordaos/0811772-81.2024.8.14.0401)
- PA-FE 24 (âncora): [denúncia](https://github.com/pbms01/FGV_TJPA/tree/main/textos/tjpa/denuncias/0824890-27.2024.8.14.0401), [sentença](https://github.com/pbms01/FGV_TJPA/tree/main/textos/tjpa/sentencas/0824890-27.2024.8.14.0401)

Julgados citados nas decisões e não conferidos nesta sessão (relatados como as decisões os transcrevem): STJ, AgRg no HC 845.139/SP; AgRg no AREsp 1.895.834/SC; AgRg no AgRg no AREsp 2.026.865/SP; AgRg no RHC 144.995/DF; CC 181.538/SP; AgRg no AREsp 2.113.232/TO; Súmula 659 do STJ; Súmula 497 do STF; TJPA, EDcl 0005194-52.2013.8.14.0133. O precedente sobre a hierarquia na organização criminosa está na sentença e também não foi conferido.

Dispositivos: os mesmos da ficha da âncora; os arts. 80, 81 e 563 do CPP e 109, 110 e 117 do CP, citados nas decisões, não foram conferidos nesta sessão.
