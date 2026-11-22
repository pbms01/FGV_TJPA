# Plano de exame em aula das sete questões nos casos de origem

Versão 0.3, 22/11/2026. A versão 0.1 foi confirmada pelo usuário em 21/11/2026; a 0.2 inclui, por decisão dele, os acórdãos do CL 56 e do FE 105 entre as peças lidas e corrige a descrição do par 2 pelo que o segundo grau decidiu; a 0.3 acrescenta, também por decisão dele, o par 9, o primeiro do TJPA, com foco na família CL, sentença e acórdão nos dois casos e o mapa das divergências entre as decisões (seção própria, depois da tabela dos pares). Repositório pbms01/FGV_TJPA, branch main. A execução segue a ordem da última seção.

## Propósito e leitura adotada

O exame se faz em aula para magistrados, caso a caso, em três tempos. Primeiro, a conduta tal como a denúncia a registrou. Depois, o modo como o sistema de justiça a processou: investigação, denúncia, sentença e, quando houver, segundo grau. Por fim, o que a resposta criminológica a cada uma das sete questões acrescenta, de modo prático, à decisão do juiz. As sete perguntas são as questões 1 a 7 já respondidas, com notas em `docs/analise/`. Os 18 fenômenos de `dados/analise/fenomenos.csv` são o recorte verificável dessas questões e dão, a cada caso, o número da base em que ele se insere.

Em aula, o caso não prova frequência. O número vem da base, com o peso amostral, e o caso mostra o mecanismo que esse número mede e o ponto em que o juiz pode agir. Por isso a seleção é intencional, e não amostral.

## Decisões

### Que casos

Oito pares, cada um formado por um caso âncora, examinado por inteiro, e por um contraste, que muda uma variável e conserva as demais: o mesmo artifício ou o mesmo papel com outro desfecho, o mesmo grupo em outra comarca, o mesmo papel antes e depois da Lei 15.397/2026. São 16 casos, 14 da matriz de 29 e dois de fora dela (CL 48 e CL 13).

A matriz é a fonte preferida por duas razões. Suas sentenças foram lidas à mão, e ela já foi montada pela pergunta das linhas de pesquisa, com o tipo de seleção de Seawright e Gerring (2008). CL 48 e CL 13 entram porque o par da reparação diante do ressarcimento pelo banco e do inciso VII com devolução ao MP para o ANPP não existe na matriz, e porque os dois têm segundo leitor e adjudicação.

Os critérios, nesta ordem:

- cada questão examinada em pelo menos quatro pares;
- cadeia completa da denúncia à sentença, com o segundo grau quando houver;
- variedade de estrato, de canal e de momento em relação à lei;
- contraste que o juiz reconheça no próprio acervo.

### Que peça

Em todos os casos, a denúncia com a cota e a sentença, por inteiro. Além delas, o acórdão no CL 48, no FE 77, no CL 56 e no FE 105, os quatro já gravados, e as razões do MP no CL 13. Os acórdãos do par 2 entraram por decisão do usuário (21/11/2026), porque no CL 56 o segundo grau mudou o desfecho de dois réus. Nos casos com recurso pendente ou com acórdão não gravado (CL 7, CL 13, FE 115, FE 35), o andamento em segundo grau é atualizado pelo DJEN na véspera da aula.

### O que registrar e onde gravar

O registro é uma ficha por caso, na estrutura descrita adiante, e uma linha por caso num índice.

- `docs/aula/plano-exame-casos.md`: este plano, espelhado no Project como `claude/plano-exame-casos-aula.md`.
- `dados/aula/casos_aula.csv`: o índice, com caso, número, par, papel no par, ordem na aula, questões examinadas, fenômenos em que o caso está no numerador ou só na base, peças lidas e estado da ficha.
- `docs/aula/fichas/<caso>.md`: as 16 fichas, com o caso no nome do arquivo (`FE_115.md`).
- `dados/aula/divergencias.csv`: o que a leitura integral encontrou de diferente da codificação, com caso, campo, arquivo de origem, valor codificado, valor lido, trecho, decisão e se a correção foi aplicada.
- `scripts/casos_aula.py`: grava o índice e o esqueleto de cada ficha já preenchido com os valores codificados nas questões, para que a leitura confirme ou corrija, e não reescreva.

Quando as fichas estiverem prontas, o roteiro da aula vai para um documento editável, como o roteiro de 15 casos, sem dados pessoais.

### Como o exame dialoga com o segundo leitor

Dos 16 casos, só quatro passaram pelo segundo leitor (INV 39, FE 54, CL 48 e CL 13), com cinco adjudicações. No CL 48 foram adjudicados o papel do denunciado, a Lei 15.397 e os fundamentos da reparação; no CL 13, o resultado e o ressarcimento pelo intermediário. Duas dessas adjudicações estão na lista de fronteira do HANDOFF (o papel no CL 48 e o intermediário no CL 13). A conferência humana das cinco entra na preparação, antes da leitura.

A codificação das 16 denúncias é assistida e não teve conferência do pesquisador, e os campos das questões 4 a 7 não tiveram segundo leitor. Nesses casos, a leitura integral feita para a aula passa a ser a conferência de todos os campos que a ficha usa:

- da codificação: artifício, meio, papel e valor em conta;
- da questão 1, `NIVEL` e o vetor; dos eixos, `OBJETO` e `CANAL_MANUAL`;
- da questão 3, os campos de reparação e de consequências;
- da questão 4, `ESTRUTURA`;
- da questão 5, a data, `TERCEIRO` e `PEDIDO_COTA`;
- da questão 6, `CREDITO` e `REACAO`;
- da questão 7, `VERSAO_MANUAL`.

Como a seleção é intencional, essa leitura controla a qualidade do que será mostrado aos magistrados, mas não estima o erro da base. O segundo leitor por amostra das questões 4 a 7 continua no passo 3 dos próximos passos do HANDOFF. As correções entram pelo caminho de sempre (`grava_codificacao.py`, `pipe_sentencas.py corrige` ou os dicionários dos scripts de análise). Depois delas, os scripts são rodados de novo na ordem do HANDOFF, com `fenomenos_ponderados.py` por último, e a ficha registra se algum número mudou.

## Os oito pares

| Ordem | Âncora | Contraste | O que o par mostra | Questões |
| --- | --- | --- | --- | --- |
| 1 | INV 39 | INV 14 | Invasão por contato físico, sem internet. No INV 39, a sessão de WhatsApp Web deixada aberta no computador do posto de saúde foi capturada e divulgada por uma colega de trabalho, com condenação no 154-A e reparação de dano moral. No INV 14, a devassa do celular da ex-companheira foi imputada como furto e terminou em absolvição por falta de ânimo de assenhoramento, com a lesão informacional fora da denúncia. | 2, 3 |
| 2 | CL 56 | FE 105 | Maquininha com o visor adulterado, em venda porta a porta, sem contato à distância: engano face a face qualificado pelo §2º-A. Três réus aparecem nos dois processos, por golpes com 25 dias de intervalo. Em Carapicuíba, entre sete denunciados, dois deles responderam só pela associação e o terceiro foi absolvido; no segundo grau, o absolvido foi condenado no 288, o executor que a vítima reconhecera na polícia foi absolvido do estelionato, e a titular da conta que recebeu o dinheiro ficou como a única condenada no §2º-A (6 anos e 4 meses, somado o 288), enquanto o réu que o acórdão põe em posição de liderança, não denunciado pelo estelionato, ficou com 1 ano em regime aberto. Em Arujá, os dois que em Carapicuíba responderam só pela associação foram condenados no §2º-A, com a pena do condutor reduzida a 4 anos no segundo grau, e o terceiro, citado por edital, teve o processo suspenso. | 2, 4, 5, 6 |
| 3 | CL 42 | FE 35 | A conta de passagem típica do falso parente por WhatsApp. No CL 42, quatro titulares foram alcançados e nenhum autor, com 34 meses do fato à denúncia, condenação no 171 §4º e reparação fixada. No FE 35, o titular único admite ter cedido a conta mediante pagamento e é condenado no §2º-A. | 1, 3, 4, 5, 6, 7 |
| 4 | FE 107 | FE 55 | A subida ao recrutador. No FE 107, o recrutador foi condenado e o titular absolvido, com o §2º-A afastado porque a ligação telefônica não bastaria. No FE 55, a titular que emprestou a conta por R$ 50 foi absolvida, e o negociador e o arregimentador foram condenados no §2º-A. | 1, 2, 4, 5, 6 |
| 5 | FE 115 | FE 77 | O mesmo papel, o do titular que empresta a conta à falsa central. Antes da Lei 15.397/2026, foi condenado a 4 anos no §2º-A. Depois dela, a desclassificação para o inciso VII foi recusada por falta de prova do financiamento, e a apelação foi desprovida. | 1, 3, 6, 7 |
| 6 | CL 7 | CL 18 | A extorsão com transferência e a conta do conteiro. No CL 7, a conduta foi desclassificada para o inciso VII como lei mais benéfica (1 ano e 4 meses, aberto, pena substituída), e o MP apelou. No CL 18, oito dias antes da lei, a pena foi de 5 anos e 4 meses em semiaberto no 158, com a reparação negada porque os bancos ressarciram. | 1, 2, 5, 7 |
| 7 | FE 122 | FE 54 | A falsa central e a recolha do cartão. No FE 122, o executor sem conta própria recebeu 7 anos e 3 meses em fechado, e a reparação foi negada porque a vítima idosa foi ressarcida pelo banco em ação cível. No FE 54, a indenização de R$ 25 mil foi fixada apesar do ressarcimento parcial, e o 288 contra o denunciado único foi retirado pelo próprio MP. | 1, 3, 4, 5, 6 |
| 8 | CL 48 | CL 13 | A falsa central por telefone e o titular da conta. No CL 48, o titular revel teve a pena-base agravada pelo prejuízo e a reparação negada porque o banco ressarciu; o inciso VII, invocado pela defesa, não foi examinado na sentença nem no acórdão que desproveu a apelação. No CL 13, a conduta foi desclassificada para o VII, com devolução ao MP para o ANPP, reparação de R$ 33,6 mil e reflexos pessoais da vítima valorados na dosimetria. | 1, 3, 6, 7 |

A questão 1 é examinada em seis pares, a 2 em quatro, a 3 em cinco, a 4 em quatro, a 5 em cinco, a 6 em seis e a 7 em quatro. A violência doméstica no INV, fenômeno da base sem questão própria, entra pelo INV 14.

Há pontos que só a leitura integral decide e que podem levar à troca de um caso:

- no CL 56 e no FE 105, se houve contato à distância antes da maquininha, o que tiraria o par do engano face a face da questão 2 (decidido na leitura de 21/11/2026: não houve; nos dois casos a abordagem é a de vendedores que passam de carro pela rua, e o par fica);
- no INV 14, se os fatos narrados continham o que o 154-A exigiria;
- no CL 42, por que um golpe por WhatsApp de 2022 foi denunciado e julgado sem o §2º-A;
- no FE 54, o papel do denunciado, que a codificação dá como elo logístico e a sentença como titular da conta destinatária condenado como coautor;
- no INV 39, o número de denunciados, que a extração conta como dois porque conta as vítimas.

## Par 9 (TJPA): a titular da conta e a divergência entre as decisões

| Ordem | Âncora | Contraste | O que o par mostra | Questões |
| --- | --- | --- | --- | --- |
| 9 | TJPA 0800121 | TJPA 0815181 | Duas jovens de Mato Grosso, titulares das contas que receberam o Pix de golpes de anúncio falso aplicados em Belém (um carro na OLX, R$ 80.000,00; uma geladeira no Marketplace, R$ 1.400,00), condenadas em primeiro grau e julgadas em apelação com 19 dias de intervalo. A 2ª Turma de Direito Penal absolveu a que admitiu ter cedido a conta ao namorado, porque a falta de prova da versão não supre a falta de prova do dolo; a 1ª Turma manteve a condenação da que negou a conta e depois disse ter tido o celular roubado, pela conta aberta com a fotografia dela 13 dias antes do golpe, pela chave apresentada pelo executor como da mulher dele e pelas versões contraditórias, e recusou de ofício o inciso VII da Lei 15.397/2026. | 1, 3, 5, 7 |

O par entrou por decisão do usuário (22/11/2026), fora da ordem da aula e da contagem dos critérios acima, para examinar as divergências entre sentença e acórdão em casos da família CL. Peças lidas: denúncia, sentença e acórdão dos dois casos; os acórdãos foram gravados em `textos/tjpa/acordaos/`. As fichas (`docs/aula/fichas/TJPA_0800121.md` e `TJPA_0815181.md`) seguem a estrutura abaixo, com duas diferenças. A ficha da âncora tem uma seção "Onde as decisões divergem", que classifica cada divergência como de critério ou de fato, nos três planos (sentença e acórdão de cada processo; varas e turmas; TJPA e base do TJSP), e traz o quadro dos indicadores dos dois casos. E, como a extração do TJPA não está no main, os números da base citados nas fichas são do TJSP, como comparação, e a conferência do bloco 5 é feita contra os metadados da coleta (`alvos_djen_tjpa.csv`, `status.csv`, `manifesto.csv`).

O espelho deste plano no Project (`claude/plano-exame-casos-aula.md`) registra também outro par do TJPA, de 21/11/2026, feito em outra sessão (PA-FE 74 e PA-FE 46, falso parente por WhatsApp), cujas fichas, exercícios e índice não estão no main em 22/11/2026; o espelho conserva a seção dele, e este arquivo só a menciona. Nos códigos da extração descrita no Project, os casos do par 9 seriam o PA-FE 89 e o PA-CL 95.

A conclusão do mapa: a diferença de resultado entre as turmas se explica pelos fatos (idade da conta, referência do executor, coerência das versões), e não por teses opostas; as divergências de critério estão dentro de cada processo (ônus da versão e dolo eventual na âncora; a conta como contribuição dispensável ou essencial no contraste), entre as duas varas criminais de Belém e, com a ressalva de que o precedente só é conhecido pela ementa, dentro da 2ª Turma. O par acrescenta ao quadro por momento de decisão três indicadores para separar cessão de adesão: a idade da conta em relação ao golpe, a referência do executor ao titular e a coerência das versões entre a polícia e o juízo.

## A ficha

Identificação: código do caso, par e papel no par, estrato, comarca, datas do fato, da denúncia, da sentença e do acórdão, e peças lidas. A ficha não traz nomes; as partes são designadas pela função (o titular, a vítima idosa, o recrutador).

1. Conduta registrada. O que a denúncia narra, nos termos dela: o artifício; o canal pelo qual o agente chegou à vítima ou ao sistema; se o sistema é objeto ou meio; quem fez o quê; a vítima e o que a torna vulnerável; o valor e por onde ele passou. Até dois trechos curtos. Em seguida, o que a denúncia não narra e a base mostra que costuma faltar: quem pediu a conta, o dado da plataforma, a cadeia de repasses, o ressarcimento.
2. Processamento.
   - Investigação: de que custodiante veio o dado narrado, quanto tempo separa o fato da denúncia e o que a cota pede.
   - Denúncia: capitulação, associação ou organização, pedido de reparação.
   - ANPP, se tratado.
   - Instrução: versão do réu ou revelia.
   - Sentença: resultado, tipo acolhido, pena, regime e substituição, consequências e idade na dosimetria, reparação e seu fundamento, Lei 15.397/2026.
   - Segundo grau.
3. Leitura pelas questões. Para cada questão que o par examina, três registros:
   - onde o caso está no achado, no numerador ou fora dele, com o número da base, simples e ponderado, tirado de `fenomenos.csv` ou da nota;
   - o mecanismo que o caso mostra;
   - o acréscimo ao magistrado: o momento de decisão, a pergunta que o juiz pode fazer aos autos e o que estava ao seu alcance na lei vigente à data da decisão.
4. Para a turma. Duas ou três perguntas com a resposta esperada. No contraste, também a versão da ficha que vai para o exercício, sem o desfecho.
5. Conferência. Campo a campo, o valor codificado e o valor lido, com remissão às linhas de `divergencias.csv`.

## O acréscimo ao magistrado, por momento de decisão

| Momento | Questão e achado da base | O que o juiz pode fazer com ele | Pares |
| --- | --- | --- | --- |
| Requerimentos na investigação (guarda e fornecimento de registros, quebra do sigilo bancário) | 5. Das 106 denúncias com canal pela internet, 97 chegam depois dos 6 meses de guarda dos registros de aplicação e 88 depois do ano dos registros de conexão; nenhuma narra dado de plataforma ou de conexão. | Decidir o pedido de fornecimento sabendo que o prazo que governa a investigação é o da aplicação e que o pedido tardio busca um dado que já não existe; o que sobrevive é o cadastro e os repasses da conta. No par 9, a dúvida que absolveu (quem operava a conta) dependia do destino do crédito e dos registros de acesso ao aplicativo, pedidos numa só decisão. | 3, 4, 6, 7, 9 |
| Recebimento da denúncia | 4. A fraude é processada como obra de poucos. Há coordenação narrada em 14 das 65 denúncias plurais, e 4 imputações de associação ou de organização recaem sobre um único denunciado associado a não identificados. | Verificar se a denúncia diz quem são, ao menos por função, os demais associados; distinguir a pluralidade de titulares do mesmo golpe da divisão de tarefas entre funções distintas. | 2, 3, 4, 7 |
| Acordo de não persecução penal | 7 e 1. Na cessão posterior à lei, a pena mínima do inciso VII não veda o acordo. Dos 101 titulares de só conta, 47 admitem a cessão, quase sempre dizendo a quem cederam e por quanto. | No controle do acordo, ver na confissão circunstanciada a identificação de quem pediu a conta. | 5, 6, 8 |
| Interrogatório e sentença: tipicidade do titular | 7 e 1. Quem admite a cessão é condenado em 45 de 47 casos (27 no §2º-A e 6 no VII), sem que o conteúdo da versão separe um tipo do outro. | Separar cessão de adesão por indicadores observáveis: número de contas do titular, dissipação imediata, contato com a vítima, remuneração proporcional ao golpe e prova de autoria além do cadastro; pelo par 9, também a idade da conta em relação ao golpe, a referência do executor ao titular e a coerência das versões. A versão não corroborada não supre a falta de prova do dolo, e a versão desmentida não prova a adesão. | 3, 4, 5, 8, 9 |
| Sentença: tipicidade pelo meio | 2. O §2º-A qualifica pela distância do canal, mas foi aplicado a cinco enganos face a face e afastado num golpe por telefone. Das 33 invasões do INV, 13 persistem sem internet. | Aplicar o roteiro de três perguntas: o sistema é objeto da conduta (154-A, com ou sem internet)? É instrumento da subtração sem disposição pela vítima (155 §4º-B)? A vítima dispôs do patrimônio induzida à distância, por qualquer canal (§2º-A)? | 1, 2, 4, 6 |
| Dosimetria | 6 e 3. O aumento pela idade é capitulado em 39 de 42 casos. As consequências pesaram contra o réu em pelo menos 26 sentenças, e em 12 delas a vítima ficou sem reparação. | Considerar a vulnerabilidade do serviço explorado, e não só a idade; não valorar na pena-base o prejuízo que a reparação deixou de tratar. | 2, 7, 8 |
| Reparação mínima (art. 387, IV, do CPP) | 3 e 6. Nas 171 condenações, a reparação foi fixada em 79, negada em 34 e omitida em 58. Na FE, o valor inteiro do golpe foi fixado contra o titular em 19 de 31 casos, e só 8 sentenças limitam a reparação ao que entrou na conta. Nas 91 fraudes de venda falsa e de falso parente, não há nenhum ressarcimento pelo intermediário. | Aplicar o quadro de seis perguntas da questão 3; a família do artifício antecipa quem já pagou. Absolvido o titular, a reparação cai com ele, e o que protege a vítima é o bloqueio feito cedo; sem pedido, resta destinar a ela a prestação pecuniária substitutiva. | 1, 3, 5, 7, 8, 9 |
| Segundo grau e execução | 1. A lei reprecificou o titular sem ampliar o alcance: o mesmo papel vai de 1 ano e 4 meses em aberto a 5 anos e 4 meses em semiaberto, conforme a data da sentença. | Aplicar o inciso VII como lei mais benéfica às condenações de titulares no §2º-A por fato anterior à lei, quando a prova é de cessão consciente sem adesão ao golpe determinado; com adesão, o fato fica no §2º-A com o art. 29 (par 9, 1ª Turma do TJPA). | 5, 6, 8, 9 |

Os dispositivos legais citados vêm das notas das questões, que registram a fonte em que cada um foi conferido. Eles não foram conferidos de novo nesta sessão, porque o acesso ao Planalto pediu aprovação.

## Tempo de aula

Para uma sessão de três horas, a distribuição proposta é esta:

- abertura de 12 minutos: a base e seus vieses, os dois eixos e a ficha;
- três pares com exercício no aplicativo, de 25 minutos cada: o par 5 (tipicidade do titular), o par 8 (reparação diante do ressarcimento) e o par 2 (o 288 e o grupo dividido). Neles, a turma aplica a questão à ficha do contraste antes de ver o desfecho;
- cinco pares expositivos, de 15 minutos cada;
- fecho de 18 minutos, com o quadro por momento de decisão.

O aplicativo recebe a ficha, e não o texto integral. Se a aula for dividida em duas sessões, como no roteiro de 15 casos, a primeira fica com os pares 1 a 4 e a segunda com os pares 5 a 8.

## Cautelas

- Versão de aula. As notas internas de trabalho ficam de fora: segundo leitor, conferência, divergências, "não conferido nesta sessão" e caminhos de arquivo do repositório. Os links das peças no GitHub e o número do processo podem ir aos slides, porque o repositório é público desde 21/11/2026. Por decisão do usuário, não se avalia a exposição de dados pessoais: as fontes são públicas, o público-alvo são magistrados e o propósito é acadêmico.
- Cada número levado à aula vem com o peso e com o viés da base: são casos que chegaram à sentença, só do TJSP, com sentenças de 2021 a 2026.
- O estado em segundo grau muda: CL 7 e CL 13 têm apelação do MP pendente.

## Execução, na próxima sessão

1. Conferência humana, pelo pesquisador, das cinco adjudicações do CL 48 e do CL 13.
2. `scripts/casos_aula.py`: o índice e os esqueletos das fichas.
3. Leitura integral por par, âncora e contraste juntos, na ordem da aula, com o preenchimento das fichas e das divergências.
4. Aplicação das correções e nova rodada dos scripts, com o registro do que mudou nos números.
5. Atualização do segundo grau pelo DJEN.
6. Roteiro da aula em documento editável e fichas de exercício para o aplicativo.
