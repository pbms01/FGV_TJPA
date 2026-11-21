# Questão 1: quem o sistema penal alcança na fraude eletrônica, e o que a Lei 15.397/2026 muda nisso

Nota analítica de 21/11/2026, sobre a base da fase 1 (TJSP), branch `coleta-datajud`. Tabelas reproduzíveis por `python3 scripts/analise_q1_alcance.py`, que grava `dados/analise/q1_alcance.csv` (uma linha por denúncia) e `dados/analise/q1_resumo.json`. Linhas de pesquisa atendidas: 2.2 (gargalos logísticos), 1.4 (avaliação do tipo novo) e 1.1 (taxonomia), com reflexo no eixo da seletividade do controle.

O critério de mediação técnica é o das linhas de pesquisa (versão 0.3): retira-se o sistema informático, em rede ou isolado, e identifica-se o canal pelo qual o agente chegou ao sistema ou à vítima; a internet é um canal entre outros. Os dois eixos estão codificados em `scripts/eixos_mediacao.py`, comum a esta questão e à questão 2 (`claude/analise-q2-teste-eliminacao.md`).

## Resposta

Nos processos de fraude eletrônica que chegam à sentença no TJSP, o sistema penal alcança a fraude nos pontos em que ela toca o mundo físico: a conta bancária aberta em nome de alguém, a linha telefônica habilitada com CPF, o cartão recolhido na porta da vítima, a mercadoria retirada na loja. O autor do ardil feito à distância só é alcançado quando deixa o próprio nome num desses registros ou quando aparece fisicamente, e em nenhuma das 161 denúncias de fraude da amostra o rastro do canal do ardil (o número de WhatsApp, o site, o perfil, o endereço IP) identificou o denunciado. Quando o contato com a vítima foi remoto, a denúncia alcançou só o titular da conta em todas as 40 denúncias do estrato CL e em 57,2% das 106 do estrato FE, e isso vale igualmente para o golpe só por telefone, sem internet: só o titular em todas as 7 denúncias CL e em 53,5% das 25 FE, contra 57,7% das 79 FE pela internet. O que decide quem é alcançado é a distância entre agente e vítima, e não a internet. A pena não distingue os papéis: a mediana no 171 §2º-A é de 48 meses para o titular e para o autor do ardil.

A Lei 15.397/2026 não ampliou esse alcance. Nenhuma denúncia da amostra capitula o 171 §2º, VII, e toda aplicação do inciso foi retroativa, a fato anterior a 04/05/2026, sempre em favor de quem já estava no processo como titular da conta. O que a lei fez foi reprecificar o elo físico, de 4 a 8 anos para 1 a 5 anos, e reabrir para ele a justiça consensual que a pena mínima do §2º-A fechava. Esse efeito depende de o debate entrar no processo: nas sentenças do estrato CL, que já falam em conta laranja, o titular condenado no §2º-A caiu de 52,0% para 23,8% das condenações; nas do estrato FE, 14 das 16 sentenças posteriores à lei sobre titulares não mencionam o inciso, e 9 delas condenam no §2º-A. No segundo grau a disputa se desloca para a adesão do titular à fraude (art. 29 do CP), elemento subjetivo que a prova registral, sozinha, não decide.

## Base e método

A unidade é a denúncia sem duplicatas, com o peso amostral do processo, e os percentuais são ponderados dentro de cada estrato. CL e FE não se somam, porque os dois universos do cjpg se sobrepõem (uma sentença de fraude eletrônica pode falar em conta laranja). Ficam fora as três denúncias sem fraude patrimonial (CL 12, CL 25 e FE 123), restando 48 no CL e 113 na FE. O INV não entra nesta questão, porque o titular de conta é ali residual (2 de 34).

A codificação de papel da base (titular, executor, misto) foi refinada numa variável de nível, que registra o nó mais alto da cadeia que a denúncia atinge, e numa variável de vetor, que registra como esse denunciado foi alcançado. O titular de conta ficou como "só conta", com vetor "registro", sem recodificação. Os 56 executores e mistos foram recodificados à mão pela nota de cada linha e, nos casos duvidosos (FE 6, 19, 22, 23, 31, 42, 61, 83, 107 e 108), pela narrativa; a tabela está no dicionário `NIVEL` do script, com o motivo de cada caso de fronteira.

| Nível | O que significa |
| --- | --- |
| só conta | o vínculo do denunciado com o fato é a conta que recebeu o valor |
| elo logístico | recolhe cartão, retira bem, habilita a linha ou arregimenta contas, sem que a denúncia lhe atribua o ardil |
| autor remoto | a denúncia lhe atribui o ardil feito à distância, ou a organização do golpe |
| autor presencial | ardil ou violência face a face (maquininha, comprovante falso no caixa, extorsão) |

| Vetor | O que significa |
| --- | --- |
| registro | conta, linha ou CNPJ em nome do denunciado ou de pessoa próxima o identifica |
| presença | flagrante, abordagem, recolha ou entrega física |
| ambos | os dois |

O contato é remoto quando o canal descrito na codificação é WhatsApp, telefone, site, rede social, e-mail, boleto ou sistema. A variável agrupa os canais pela distância entre agente e vítima. Para separar a distância da internet, o contato remoto foi desdobrado pelo canal: internet (WhatsApp, rede social, site, e-mail, e sempre a venda falsa e os demais golpes que nascem de anúncio online), telefonia (só ligação ou SMS), correio e sistema-objeto.

## Primeira etapa: quem a denúncia alcança

| Nível alcançado | CL (48) | FE (113) |
| --- | --- | --- |
| só conta | 43 (91,1%) | 59 (53,1%) |
| elo logístico | 0 | 10 (7,9%) |
| autor remoto | 0 | 36 (31,2%) |
| autor presencial | 5 (8,9%) | 8 (7,8%) |

A distância separa os dois regimes com nitidez. Com contato presencial, a denúncia alcança o autor do ardil em 6 das 7 denúncias FE (88,5%) e em 5 das 8 CL (56,1%). Com contato remoto, alcança só a conta em todas as 40 denúncias CL e, nas 106 FE, distribui-se assim: só conta 57,2%; autor remoto identificado pelo registro 25,1% (27 denúncias); elo logístico 8,6%; autor remoto identificado pela presença física 7,6% (8); autor presencial 1,5%. Por artifício, na FE, o falso parente fica na conta em 75,3%, a falsa central em 50,3% (e chega ao motoboy ou falso policial que recolhe o cartão em mais 34,3%), a venda falsa divide-se entre conta (46,2%) e autor que recebeu na própria conta (51,6%), e a maquininha alcança o autor presencial em 79,8%.

O desdobramento do contato remoto mostra que esse regime não é da internet.

| Nível alcançado, contato à distância | CL internet (26) | CL telefonia (7) | FE internet (79) | FE telefonia (25) |
| --- | --- | --- | --- | --- |
| só conta | 100% | 100% | 57,7% | 53,5% |
| elo logístico | | | | 31,2% |
| autor remoto | | | 41,3% | 11,9% |
| autor presencial | | | 1,0% | 3,4% |

O golpe por ligação ou SMS deixa o titular da conta sozinho no processo na mesma proporção que o golpe pela internet. A diferença está no que vem além da conta: pela internet, o autor remoto é alcançado sobretudo porque recebeu na própria conta (31,2% das 79 FE, vetor registro), e pela telefonia o que se alcança além da conta é o motoboy ou falso policial que recolhe o cartão (31,2% das 25 FE). Nos dois canais, quem fala com a vítima à distância só aparece quando toca um registro ou um lugar físico. Uma ressalva de medida: o código "telefone" da base inclui aplicativo de mensagens não nomeado, e a semelhança entre os canais pode estar em parte inflada por isso; os golpes por ligação de voz, que dispensam a internet (FE 5, FE 28 e FE 107, para telefone fixo, e CL 30), ficaram na conta (FE 5, CL 30) ou alcançaram o autor só pela conta em nome dele (FE 28) ou do recrutado (FE 107).

O vetor confirma o desenho. Na FE, 77,8% dos denunciados foram alcançados pelo registro, 18,7% pela presença física e 3,5% pelos dois. A busca de termos de investigação telemática (IP, ERB, geolocalização, quebra de sigilo telemático, interceptação, provedor, registros de acesso) nas narrativas e cotas casou em 12 denúncias de fraude, e a leitura de cada trecho mostrou que em nenhuma o dado telemático do canal do ardil identificou o denunciado: são falsos positivos (a sigla de inquérito policial, a "Stone IP S.A."), a geolocalização do celular da vítima no cativeiro (CL 18), um site hospedado no exterior sem continuidade (FE 53) e pedidos de quebra feitos depois da prisão física, para achar comparsas (FE 17, FE 102, FE 122). A investigação telemática, quando aparece, vem depois do flagrante e não antes dele.

Daí decorre um achado sobre a própria autoria. Nas 28 denúncias FE que atribuem o ardil a quem foi identificado pelo registro, a autoria do engano é inferida da conta, da linha ou do CNPJ em nome do denunciado, e em 23 delas a busca de termos não encontra confissão, reconhecimento ou flagrante. O FE 22 é típico: a denúncia diz que a ré, "passando-se como representante" da financeira, enviou o boleto, e a prova narrada é que ela mantinha oito contas e era a beneficiária do código de barras. O FE 42 mostra a fragilidade dessa inferência: a denúncia narra que a ré "entrou em contato com vendedor" no Facebook e recebeu o Pix, recusa o ANPP pela pena mínima do §2º-A, e a sentença, depois da instrução, descreve a conduta como "a cessão de sua conta bancária para o recebimento e a imediata dissipação dos valores" e a reclassifica para o inciso VII por emendatio libelli. A mesma prova registral sustentou a autoria do ardil na denúncia e a mera cessão na sentença.

A investigação, nos casos de só conta, para na primeira conta. A denúncia declara coautores desconhecidos em 71,4% dessas denúncias na FE e em 88,4% no CL, e narra que o dinheiro seguiu para outras contas (repasse, pulverização) em 17,0% na FE e 29,8% no CL, sem que os titulares seguintes sejam denunciados. O preço da conta, quando a narrativa o registra, vai de R$ 50 (FE 55) a R$ 500 (FE 115), com R$ 150 (CL 7, FE 101) e R$ 200 (CL 39) no meio, contra prejuízos que chegam a R$ 118 mil numa única vítima (CL 45). Em 11 denúncias a conta foi aberta com selfie, biometria ou validação facial, que serviram para identificar o titular depois do fato e não impediram a cessão.

## Segunda etapa: o que a sentença faz com cada papel

| Na FE | só conta | autor remoto | elo logístico | autor presencial |
| --- | --- | --- | --- | --- |
| Ao menos um réu condenado | 81,6% (49 de 58) | 90,1% (33 de 36) | 10 de 10 | 8 de 8 |
| Condenação no 171 §2º-A | 88,2% | 80,2% | 100% | 44,9% |
| Pena mediana no §2º-A, sem peso | 48 meses (41) | 48 meses (25) | 52 meses (10) | 44 meses (4) |

No CL, o titular é condenado em 93,4% das denúncias (40 de 43), com pena mediana de 48 meses no §2º-A (14 condenações), 13,5 meses no 171 sem §2º-A e 12 meses no inciso VII. As 11 absolvições de titulares (3 no CL, 8 na FE, onde o nono não condenado é a extinção por prescrição do FE 46) apoiam-se no art. 386, VII, do CPP (insuficiência de prova) em 10 casos e no inciso V em um (FE 114), o que indica que a defesa do titular gira em torno do dolo, e não da autoria.

A sentença, portanto, pune o elo físico como pune o autor. O registro, que na primeira etapa decide quem é alcançado, na segunda não diferencia a resposta, e a dosimetria acrescenta um efeito que merece atenção. Entre os 41 titulares condenados no §2º-A na FE, a pena mediana é de 64 meses quando a vítima é idosa (11 casos, 171 §4º) e de 48 meses quando não é (30); 19 dos 41 ficaram acima de 48 meses, e nenhum desses teve a pena substituída (art. 44, I, do CP), contra 18 de 22 substituídas até 48 meses. A majorante pela idade da vítima recai sobre quem cedeu a conta, embora a escolha da vítima seja do autor remoto, que não está no processo. No CL, 6 dos 14 titulares condenados no §2º-A ficaram acima de 48 meses, nenhum com substituição.

A capitulação no §2º-A também fecha a justiça consensual antes do processo. Na FE, a cota trata do ANPP em 62,8% das denúncias de só conta, e, entre as que capitulam o §2º-A e tratam do acordo, 86,5% (32 de 37) o recusam pela pena mínima, porque o art. 28-A do CPP exige pena mínima inferior a 4 anos e a do §2º-A é de 4. No CL, a proporção é de 8 de 10. A cota do FE 42 diz isso em uma linha, e a sentença do mesmo caso, depois da reclassificação, abre vista ao MP para a suspensão condicional do processo e o ANPP. Há um limite de leitura que precisa acompanhar este número: o cjpg só traz processos com sentença, de modo que os titulares que fizeram ANPP sob o 171 simples nunca entram na base.

## Terceira etapa: o que a Lei 15.397/2026 muda

O texto conferido no Planalto cria, no §2º do art. 171, o inciso VII ("cede, gratuita ou onerosamente, conta bancária para que nela transitem recursos destinados ao financiamento de atividade criminosa ou que dela sejam fruto"), com a pena do caput, de 1 a 5 anos, mantém o §2º-A com 4 a 8 anos, revoga o §5º (a representação) e entra em vigor na publicação, em 04/05/2026.

Na sentença de primeiro grau, o efeito depende do estrato, ou seja, de o tema da conta laranja já estar no processo.

| Titulares (só conta), sentenças posteriores à lei | CL (29) | FE (16) |
| --- | --- | --- |
| Aplica o inciso VII | 8 | 0 |
| Recusa | 8 | 2 (FE 72, FE 77) |
| Não menciona | 9 | 14 |
| Outras (só dispositivo, reforço do dolo, absolvição) | 4 | 0 |

| Capitulação acolhida nas condenações de titulares | antes da lei | depois da lei |
| --- | --- | --- |
| CL, 171 §2º-A | 52,0% (de 14) | 23,8% (de 26) |
| CL, 171 §2º, VII | | 32,6% |
| CL, 171 sem §2º-A | 26,8% | 27,8% |
| FE, 171 §2º-A | 89,6% (de 36) | 84,3% (de 13) |

No CL, a lei deslocou para o VII a maior parte dos titulares que iriam para o §2º-A, e o 171 simples, que alguns juízos já aplicavam ao titular antes dela, ficou estável. Na FE, nada mudou: nove sentenças posteriores à lei condenam titulares no §2º-A sem mencionar o inciso (FE 14, 27, 36, 63, 75, 91, 96, 119 e 126). Nos dois casos mistos do CL em que o inciso foi aplicado (CL 11 e CL 29), ele alcançou o corréu que forneceu a conta, e no CL 29 a sentença diz que o réu "não figura como executor direto" e sim "como titular e disponibilizador da conta". O único fato da amostra posterior à lei (FE 110, de 14/05/2026) não envolve conta de passagem, de modo que toda aplicação do VII na base é retroativa, como lei mais benéfica.

No segundo grau, os seis processos da amostra com acórdão sobre o inciso são todos de titulares condenados no §2º-A: cinco foram desclassificados para o VII (FE 56, CL 6, CL 58, FE 101 e FE 96, este último uma das sentenças FE que silenciaram depois da lei) e um teve a desclassificação recusada (CL 47). No conjunto do cjsg, dos 56 acórdãos que decidem o inciso na ementa, ele prevalece em 25 e é recusado em 31, e a recusa se apoia na participação ou adesão à fraude em 20 das 30 recusas expressas. O critério que decide entre 4 e 1 ano de pena mínima é, portanto, a prova de que o titular aderiu ao golpe determinado, e essa prova raramente existe além do próprio registro, que é o que a primeira etapa mostrou.

A lei, em seus seis primeiros meses, funcionou como figura privilegiada para quem o sistema já alcançava, e não como incriminação nova. A leitura difundida na imprensa, segundo a qual o cedente passa a responder criminalmente mesmo sem participar do golpe, não encontra apoio na base: o cedente já respondia, e com pena maior, como partícipe do §2º-A ou no 171 simples. O que a base não permite medir é o efeito prospectivo, ou seja, se o inciso passará a alcançar o cedente sem adesão a crime determinado, que antes seria absolvido por falta de prova do dolo de participação (é a leitura da 9ª Câmara, que reserva o VII ao cedente de atuação neutra). Isso exige fatos posteriores a 04/05/2026, que ainda não chegaram à sentença.

## Leitura criminológica

No elemento delito (linha 1.1), o diferencial da mediação técnica, neste corpus, está na atribuição e não na conduta, e o eixo que o produz é a distância, não a internet. O engano é o do estelionato de sempre; o que a distância muda, seja pela internet, seja pelo telefone, é o lugar onde fica a prova de quem enganou. Com o agente junto da vítima, o autor aparece no balcão; à distância, o rosto some e o nome fica no cadastro bancário e no da operadora. É um argumento para tratar o §2º-A como crime antigo com prova nova, para medir o tipo pelo que ele faz com a prova de autoria, e para não confundir o problema da investigação à distância com o da internet: o golpe por telefone fixo apresenta o mesmo déficit.

No elemento infrator (linha 2.2), a conta de passagem é o gargalo logístico por excelência, e a base mostra que a repressão incide quase só nele. Como a conta custa entre R$ 50 e R$ 500 e o recrutador raramente é identificado, a punição do titular retira da cadeia o elo mais barato e mais substituível, o que permite supor efeito preventivo baixo; a hipótese pede série externa para ser testada.

No elemento controle social, a seletividade aparece com uma forma específica: o sistema não seleciona pela gravidade do papel, e sim pela exposição registral. Alcança quem pôs o próprio nome na conta ou na linha, seja o laranja, seja o autor descuidado que recebeu na própria chave Pix, e deixa de fora o autor que usa conta de terceiro. Dentro do alcançado, a pena não distingue os papéis, e a majorante da vítima idosa recai sobre quem não a escolheu.

Na avaliação do tipo novo (linha 1.4), a Lei 15.397/2026 corrige parte da desproporção, mas pela via da desclassificação e do retroativo benéfico, dependente de provocação, e sem critério legal para separar cessão de participação. O desfecho de casos análogos varia com o estrato, o juízo e a câmara, o que é o retrato de um tipo que reprecificou o elo físico sem dizer onde ele termina.

## Produto para quem investiga, acusa, julga ou previne

Para a investigação, a conta é o começo do rastro e não o fim. A própria base indica três passos que as denúncias de só conta raramente dão: seguir os repasses que a denúncia já narra até os titulares seguintes; pedir à instituição os dados de abertura e de acesso da conta (a selfie, o aparelho, o endereço IP de abertura), que podem não coincidir com o titular; e perguntar ao titular, formalmente, quem pediu a conta.

Para a acusação, a escolha entre o §2º-A com o art. 29 e o inciso VII precisa de prova de adesão além do registro, sob pena de a capitulação mais grave cair na sentença ou no recurso, como no FE 42 e nos cinco acórdãos da amostra. Quando o caso for de cessão, o ANPP no VII tem como requisito a confissão formal e circunstanciada (art. 28-A, caput, do CPP), que é o momento natural de obter a identificação de quem arregimentou a conta, convertendo o acordo em instrumento de subida na cadeia. Nas condenações de titulares no §2º-A por fato anterior à lei, a aplicação do VII como lei mais benéfica cabe ao tribunal enquanto houver recurso e, depois do trânsito, ao juízo da execução (Súmula 611 do STF; art. 66, I, da LEP); as nove sentenças FE que silenciaram são o caso típico.

Para o julgamento, a base sugere indicadores observáveis para separar a cessão da adesão, a testar contra os 56 acórdãos: o número de contas do mesmo titular (oito no FE 22, cinco com o mesmo documento no FE 63), a dissipação imediata dos valores, o contato direto com a vítima, a remuneração proporcional ao golpe (cerca de 10% no FE 35) e a existência de prova da autoria além do cadastro.

Para a prevenção e a governança privada (linha 4.1), a biometria na abertura de conta aparece na base como instrumento de atribuição posterior, e não de prevenção. A política relevante é a do controle da cessão e do uso da conta depois de aberta, mais do que a da identificação no momento da abertura.

## Vieses e pendências desta análise

As conclusões valem para processos com sentença de primeiro grau publicada no TJSP (sentenças de 2021 a 2026, quase metade de 2026), fora o segredo de justiça, e não para o universo das fraudes, cuja maior parte não chega a inquérito. A codificação de papel é assistida em 140 das 164 denúncias CL e FE e ainda não foi conferida pelo pesquisador, e a recodificação de nível e vetor dos 56 executores e mistos é também do assistente, lida nas notas e, nos casos de fronteira, nas narrativas. Os indícios de confissão, reconhecimento e flagrante vêm de busca de termos, não de leitura integral, e servem de triagem. A pena é a do primeiro réu condenado no dispositivo, o que mistura papéis nos casos mistos. As 85 sentenças FE e 20 CL com `conferido=auto` não tiveram segundo leitor.

Ficam como passos desta questão: conferir a tabela `NIVEL` e a codificação assistida dos titulares; ler o fundamento das 11 absolvições e das 10 recusas do inciso contra a variável de vetor; codificar nos 56 acórdãos do cjsg os indicadores de adesão propostos acima; e repetir a medição quando houver sentenças sobre fatos posteriores a 04/05/2026, que são as únicas capazes de mostrar se o inciso VII alcança alguém que antes ficava de fora.

## Fontes normativas conferidas nesta sessão

- Lei 15.397, de 30/04/2026, texto do Planalto: https://www.planalto.gov.br/ccivil_03/_Ato2023-2026/2026/Lei/L15397.htm
- Súmula 611 do STF, portal do STF: https://portal.stf.jus.br/jurisprudencia/sumariosumulas.asp?base=30&sumula=2560
- Art. 28-A do CPP e art. 171, §4º, do CP: conferidos em reprodução do texto legal (modeloinicial.com.br e ementa do TJRJ), não no Planalto, que pediu aprovação de acesso nesta sessão.
- Art. 44, I, do CP e art. 66, I, da LEP: não conferidos nesta sessão.
- Leitura da imprensa sobre a lei: Jornal Opção, 08/05/2026, https://www.jornalopcao.com.br/ultimas-noticias/nova-lei-endurece-penas-para-crimes-digitais-e-mira-uso-de-contas-laranja-em-golpes-virtuais-823678/
