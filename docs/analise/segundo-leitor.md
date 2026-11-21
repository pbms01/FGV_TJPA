# Conferência por segundo leitor da codificação assistida e das sentenças lidas por regras

Nota de método de 21/11/2026, sobre a base da fase 1 (TJSP). Reproduzível por `python3 scripts/segundo_leitor.py`, que compara as duas leituras, grava `dados/conferencia/concordancia.csv` e `concordancia_resumo.json` e confere se os dados vigentes trazem o que a adjudicação decidiu (`dados/conferencia/adjudicacao.csv`). A primeira leitura, como estava no momento da comparação, fica congelada em `dados/conferencia/primeira_leitura.csv`, para que a medida não mude quando a adjudicação corrige os dados.

## Resposta

A codificação de base e a leitura das sentenças por regras resistem à conferência. Nos campos de escolha única, os dois leitores concordaram em 85% a 100% dos casos (salvo o rótulo do resultado da sentença, que é questão de vocabulário), com kappa entre 0,75 e 1,00 sempre que a categoria não é rara, e a reparação do art. 387, IV, do CPP (resultado, valor material e moral, individualização, solidariedade) concordou em todas as 50 sentenças. As divergências se concentram em três pontos, que são também os mais interpretativos da base: o contexto e o meio das invasões de conta pessoal, a atribuição dos danos aos temas de Agrafiotis nas consequências do crime e a valoração das consequências quando a sentença não usa a palavra. Das 57 divergências, 36 foram resolvidas a favor do segundo leitor e 21 mantiveram a primeira leitura. A adjudicação corrigiu três afirmações das notas sem inverter nenhuma conclusão: o CL deixa de ter titular de conta em todas as denúncias de contato remoto (39 de 40, e a exceção, CL 40, é atribuída pela própria conta), o dano reputacional passa a aparecer na sentença (duas vezes) e as consequências negativas sobem de 25 para pelo menos 26.

## Desenho

O segundo leitor recebeu, às cegas, os textos de 34 denúncias e de 50 sentenças, com identificadores neutros (D01 a D34, S01 a S50) e um livro de códigos para cada bloco (`dados/conferencia/livro_codigos_denuncias.md` e `livro_codigos_sentencas.md`), sem acesso à primeira codificação nem às notas analíticas. A amostra de denúncias soma 24 sorteadas da codificação assistida (8 por estrato, semente 20261122) e os 10 casos de fronteira do LEIAME. A de sentenças soma 24 lidas só pelo leitor de regras (`conferido=auto`; no INV, todas as 8), os 14 casos de que a questão 3 mais depende (correções à mão, dano não econômico, dano moral) e 15 condenações sorteadas, 5 por estrato. Os casos escolhidos entram na concordância, mas são mais difíceis que a média, e o resumo dá a concordância também só nos sorteados.

O segundo leitor é uma instância do mesmo modelo que fez a primeira leitura, sem a memória dela, distribuída em nove lotes. A conferência mede, por isso, a reprodutibilidade da codificação a partir do texto e do livro de códigos, e não a ausência de viés comum aos dois leitores. A conferência humana, pelo pesquisador, das decisões de adjudicação continua pendente.

## Concordância

| Campo | Casos | Concordância | Kappa | Só sorteados |
| --- | --- | --- | --- | --- |
| Contexto da conduta | 34 | 0,88 | 0,75 | 0,92 |
| Meio de contato | 34 | 0,85 | 0,82 | 0,92 |
| Artifício | 34 | 0,91 | 0,90 | 0,92 |
| Papel do denunciado | 34 | 0,91 | 0,88 | 0,92 |
| Nove indicadores binários | 34 | 0,94 a 1,00 | 0,65 a 1,00 | 0,96 a 1,00 |
| Resultado da sentença | 50 | 0,80 | 0,54 | 0,82 |
| Tipo acolhido, pena, regime | 50 | 0,98 a 1,00 | 0,97 | 0,97 a 1,00 |
| Substituição da pena | 50 | 0,94 | 0,89 | 0,91 |
| Lei 15.397/2026 na sentença | 50 | 0,98 | 0,96 | 1,00 |
| Reparação: resultado e valores | 50 | 1,00 | 1,00 | 1,00 |
| Fundamentos da negativa (conjunto) | 11 | 0,82 | | 0,83 |
| Dano moral negado | 50 | 0,98 | 0,79 | 0,97 |
| Intermediário ressarciu | 50 | 0,94 | 0,38 | 0,94 |
| Consequências: valoração | 50 | 0,88 | 0,82 | 0,88 |
| Consequências: danos (conjunto) | 16 | 0,50 | | 1,00 (3) |
| Pedido de reparação na denúncia | 50 | 0,98 | 0,96 | 1,00 |

A divergência no resultado da sentença é de vocabulário, não de leitura: a primeira leitura chama de procedência parcial a condenação em que o dispositivo afasta uma imputação, uma majorante ou um corréu, e o segundo leitor, pelo livro de códigos, chamou de condenação; quanto a ter havido condenação, os dois concordam em 50 de 50. O kappa baixo do intermediário vem da raridade da categoria (três divergências em poucos positivos), e as três foram casos de fronteira entre ressarcimento pelo banco e devolução do valor bloqueado.

## Adjudicação

Cada divergência recebeu decisão e motivo em `adjudicacao.csv`. Na codificação das denúncias, 14 foram para o segundo leitor e 6 ficaram com a primeira. As aceitas corrigem o contexto de quatro casos (FE 97 e INV 34 passam a patrimonial, INV 41 a violência doméstica, INV 40 a outro), o meio de três invasões de conta pessoal, que é o sistema e não a rede social (INV 6, INV 27, INV 41), o meio do FE 47 (site), o artifício do INV 2 (invasão de sistema bancário), três indicadores (INV 32, venda falsa e investimento; INV 36 e CL 35, falsa central) e o papel do CL 40, de titular de conta para misto, porque a denúncia lhe atribui sozinho a mensagem da falsa sobrinha. O papel do CL 48 ficou como titular: a execução é atribuída ao "denunciado e sua comparsa" não identificada, fórmula que também aparece em FE 51 e FE 89, e a atribuição conjunta com pessoa não identificada não diz o que o denunciado fez além de receber na conta. As duplicatas (INV 3 e INV 7) receberam a mesma correção.

Nas sentenças, 22 foram para o segundo leitor e 15 ficaram com a primeira (10 delas o vocabulário do resultado). As aceitas corrigem a substituição da pena em três casos (CL 53, FE 82, INV 5), o regime do FE 20, os fundamentos da negativa em dois (CL 48, CL 58), o dano moral negado do FE 68, o intermediário em dois (FE 70; CL 24, absolutória), o pedido de reparação do FE 125, a valoração das consequências em cinco (FE 21, FE 59, INV 43, CL 12, CL 25) e os danos nomeados em sete. Duas correções viraram regra do leitor em `reparacao_387.py`, e não exceção: o pedido redigido como "fixação do valor do prejuízo mínimo" e a recusa de dano moral que só aparece em jurisprudência transcrita entre aspas. As demais estão nos dicionários dos scripts de análise, marcadas como vindas do segundo leitor, e `segundo_leitor.py` confere que todas estão aplicadas.

## O que mudou nas questões

Na questão 1, o CL 40 deixa a categoria "só conta". O estrato CL passa a ter o titular alcançado sozinho em 39 das 40 denúncias de contato remoto (97,7%), e a exceção confirma a tese: a denúncia imputa ao titular o ardil, mas a prova que invoca é a conta, e o número de WhatsApp não é ligado a ele. Na questão 2, o INV 2 entra no grupo de invasão de conta ou sistema bancário da fronteira entre furto e estelionato, que passa a sete casos, e nenhuma conduta muda de classe. Na questão 3, o dano reputacional aparece em duas sentenças (FE 21, o nome sujo na praça; INV 30, a clientela perdida), o dano físico desaparece, as consequências negativas passam a 26 e o dano não econômico na dosimetria a nove casos, as recusas expressas do dano moral caem para quatro e o FE 125 sai das fixações sem pedido. A adjudicação também expôs que a questão 3 contava quatro denúncias fora da tipologia (INV 40, CL 12, CL 25, FE 123), agora excluídas do resumo como na questão 1, o que leva o denominador a 171 condenações.

## Limites e pendências

A atribuição dos danos aos temas de Agrafiotis é o campo menos reprodutível da base, e a segunda etapa da questão 3 depende das decisões de adjudicação sobre ele (o receio de prejuízo como abalo, as multas do veículo como dano econômico, a perda de clientes como dano à reputação). A valoração das consequências por termos perdeu uma negativa em 21 condenações não marcadas da amostra (FE 21), de modo que a contagem é um piso. A amostra não cobre o detector de indícios da questão 1 nem as tabelas `NIVEL`, `OBJETO` e `CANAL_MANUAL`, que seguem lidas só pelo assistente. Ficam como passos a conferência humana das 57 decisões, a releitura das consequências nas condenações não marcadas e um segundo leitor para as tabelas de nível e de acesso.
