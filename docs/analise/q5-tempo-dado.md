# Questão 5: o tempo do dado na fraude eletrônica, e o que ainda se pode pedir quando a denúncia chega

Nota analítica de 21/11/2026, sobre a base da fase 1 (TJSP). Tabelas reproduzíveis por `python3 scripts/analise_q5_tempo_dado.py`, que grava `dados/analise/q5_tempo_dado.csv` (uma linha por denúncia) e `dados/analise/q5_resumo.json`. A leitura das datas, das fontes de dado e dos pedidos da cota é de `scripts/tempo_dado.py`, que se valida com `python3 scripts/tempo_dado.py valida`. Linha de pesquisa atendida: 4.4 (tempo do dado e preservação), com reflexo na 1.1 (alcance) e na 4.1 (governança privada). Usa os eixos de `scripts/eixos_mediacao.py` e o nível alcançado da questão 1 (`claude/analise-q1-alcance-elo-fisico.md`).

## Resposta

A denúncia de fraude eletrônica chega tarde demais para o dado que identificaria o autor remoto. Entre o fato e a denúncia passam, na mediana, 21,6 meses na FE e 28,2 no CL; 88,7% das denúncias FE e 88,8% das CL vêm depois de seis meses, e 76,0% e 84,4%, depois de um ano. Nas 106 denúncias em que o ardil passou pela internet, a mediana é de 27,0 meses, e 97 delas chegam depois de seis meses e 88 depois de um ano. São justamente os prazos de guarda que o Marco Civil impõe aos registros do canal: seis meses para os registros de acesso a aplicações (art. 15, caput, da Lei 12.965/2014) e um ano para os de conexão (art. 13, caput). Quando o Ministério Público assina a denúncia, o provedor de aplicação já não está obrigado a guardar o que permitiria chegar a quem escreveu à vítima em 97 das 106, e o de conexão, em 88, salvo se alguém tiver pedido a guarda antes (arts. 13, §2º, e 15, §2º). Os dados que sobrevivem ao tempo do processo são os do banco, que guarda cadastro e transações por no mínimo cinco anos (art. 10, §2º, da Lei 9.613/1998), e os registros de ligações da operadora, também por cinco anos (art. 17 da Lei 12.850/2013).

É o que as denúncias mostram. Nenhuma das 106 de fraude pela internet narra dado obtido de plataforma ou de provedor de conexão; esses dados aparecem em 4 das 38 denúncias em que o sistema é o objeto do crime, todas do INV. O dado de terceiro custodiante que aparece na fraude contra a pessoa é o cadastro da linha telefônica, em 11 denúncias (9 pela internet, porque o número do WhatsApp é uma linha, e 2 pela telefonia), e o que domina é o dado bancário e o material que a própria vítima traz: comprovante, extrato, print. Nas 101 denúncias em que o denunciado é só o titular da conta, 59 o nomeiam sem narrar dado algum obtido do banco: o titular aparece como o da conta que o golpista indicou à vítima e que o comprovante registra. A trilha que resiste ao tempo e produz um denunciado é a que a vítima entrega no dia do registro e que o banco guarda por cinco anos. A questão 1 achou o titular da conta como camada alcançada; esta questão acha a razão temporal dessa seletividade.

O cadastro da linha não tem o mesmo peso que o da conta. Das 16 denúncias que narram dado de operadora, plataforma ou provedor, 9 identificaram por ele um denunciado, 2 o corroboraram, 1 ficou sem resultado (a linha pré-paga fora cancelada e desprogramada, FE 16) e 4 apontaram um titular de linha que o Ministério Público não denunciou, em três com fundamentação expressa: linha pré-paga "facilmente habilitada em nome de terceiros" (CL 22), titular que negou a linha e não aparece nos extratos (CL 54), falta de indícios (FE 66). O mesmo destino teve a titular da linha usada como chave Pix no FE 25, arquivada. O registro da conta basta para levar o titular à denúncia; o da linha, quando não coincide com outra trilha, leva ao arquivamento. A diferença está na verificação de identidade na adesão, mais forte na abertura de conta (a selfie e a biometria que a questão 1 encontrou em 11 denúncias) do que na habilitação da linha pré-paga.

A cota da denúncia quase nada pede de dado: 15 das 194 requerem, apoiam ou aguardam alguma medida de obtenção, nenhuma pede preservação e nenhuma se dirige a plataforma ou a provedor de conexão. O que se pede é dado bancário (8, um deles à própria vítima), conteúdo de aparelho apreendido ou laudo pericial (6) e o resultado de uma quebra telefônica já autorizada (1), custodiantes sem prazo curto. Para quem investiga, a consequência é um protocolo por canal que se executa no registro da ocorrência, e não na denúncia: a guarda dos registros de aplicação dentro de seis meses, a de conexão dentro de um ano, o cadastro da linha como pista e não como prova de autoria, e a conta de destino como ponto de partida para a camada seguinte da rede, pela quebra dos repasses.

## Base e método

A unidade é a denúncia sem duplicatas, com o peso amostral do processo e percentuais ponderados dentro de cada estrato. Ficam fora as quatro denúncias fora da tipologia (INV 40, CL 12, CL 25 e FE 123), restando 33 no INV, 48 no CL e 113 na FE. Por canal, nível e prisão no ato, os números são contagens simples das três camadas somadas, porque o canal atravessa os estratos, com mediana e quartis em meses de 30,44 dias. A leitura integral do par 2 do exame em aula (21/11/2026) corrigiu a data da denúncia do CL 56 (27/09/2023, e não a da cópia remetida ao STJ), a prisão no ato no CL 56 e no FE 105 e o pedido da cota no FE 105; os números desta nota já trazem as correções, registradas em `dados/aula/divergencias.csv`.

A data do fato é a primeira data da narrativa depois da âncora ("Consta", "Apurou-se", "Relata", "1) "), descartadas as de nascimento, de documento (fls., boletim, ofício, relatório, portaria) e de assinatura, as anteriores a 2010 e as posteriores à denúncia. Num período vale o início, porque o dado mais antigo é o primeiro a vencer; quando a denúncia só dá o limite ("até a data de 09 de novembro de 2023"), a data fica marcada como "até" e o intervalo é um mínimo. Das 194 denúncias, 193 têm data: 174 com dia, 8 só com mês e ano, 11 com limite. Quatro datas são da leitura manual (CL 1, de OCR degradado, com o ano pelo número do inquérito; INV 36, INV 27 e FE 86), e o CL 49 fica sem data, porque diz apenas "no dia dos fatos". Nas 29 denúncias da matriz, lidas à mão no trecho que segue a âncora, a regra acerta as 29; os ajustes de contexto (a portaria de instauração no FE 24 e no FE 54, a assinatura no INV 36, o início do período no INV 11) saíram dessa leitura, que não é, portanto, independente da regra. Uma amostra de 16 denúncias fora da matriz, conferida depois, não mostrou erro.

A data da denúncia é a da assinatura na própria peça (o último "Cidade, dia de mês de ano" da cota ou do fecho) e, sem ela, a do documento no PJe. As duas coincidem em até sete dias em 94 das 98 denúncias que têm as duas; nas quatro que divergem (INV 17, CL 41, CL 11, INV 34) o documento do PJe é posterior à assinatura, e vale a assinatura.

O intervalo medido é o do fato à denúncia. Não é o tempo até o pedido de dado, que corre dentro do inquérito e que a denúncia raramente data; é o teto desse tempo e é, exatamente, a idade do dado no dia em que a cota pede alguma coisa. Quando a denúncia narra dado de plataforma ou de operadora, ele foi pedido antes, e o intervalo não diz quando.

As fontes de dado são triagem por termos na narrativa e na cota, agrupadas pelo custodiante: o banco (quebra, resposta a ofício, cadastro e documentos da abertura, extrato da conta do investigado, selfie ou biometria), a vítima (comprovante, extrato próprio, print), a operadora, a plataforma, o provedor de conexão, o aparelho apreendido e as câmeras. Os achados de operadora, plataforma e conexão foram lidos um a um, e a leitura manual (dicionário `TERCEIRO`) substitui a regra: 16 denúncias com dado obtido, 3 achados descartados (o golpista que ligou para a operadora da vítima no CL 15, a linha digitável de boleto no FE 41 e o IP achado pela auditoria da própria empresa vítima no INV 34). Os pedidos da cota foram lidos do mesmo modo (`PEDIDO_COTA`, com os descartes em `FALSO_PEDIDO`: ofícios para localizar o réu, bloqueio de valores para reparação, laudos em geral). "Preso no ato" é a triagem de termos da questão 1 (flagrante, foi preso, abordado, surpreendido), não uma codificação.

## Os prazos de guarda

Os prazos foram conferidos no texto do Planalto nesta sessão.

| Custodiante e dado | Prazo de guarda | Fundamento | Medidas previstas |
| --- | --- | --- | --- |
| Provedor de aplicação (pessoa jurídica, com fins econômicos): registros de acesso a aplicações | 6 meses | Lei 12.965/2014, art. 15, caput | guarda por prazo maior a pedido cautelar da polícia, de autoridade administrativa ou do Ministério Público (art. 15, §2º), com pedido judicial de acesso em 60 dias (art. 13, §3º, por remissão) |
| Administrador de sistema autônomo (provedor de conexão): registros de conexão | 1 ano | Lei 12.965/2014, art. 13, caput | guarda por prazo superior a pedido cautelar (art. 13, §2º); sigilo do requerimento e perda de eficácia sem o pedido judicial no prazo (art. 13, §4º) |
| Concessionária de telefonia: registros de identificação dos terminais de origem e destino das ligações | 5 anos | Lei 12.850/2013, art. 17 | |
| Instituições do art. 9º da Lei 9.613 (entre elas as que captam, intermedeiam e aplicam recursos de terceiros): cadastro de clientes e registro de transações | no mínimo 5 anos, do encerramento da conta ou da conclusão da transação, ampliável pela autoridade competente | Lei 9.613/1998, art. 10, I, II e §2º | quebra do sigilo bancário "quando necessária para apuração de ocorrência de qualquer ilícito", em qualquer fase do inquérito ou do processo (LC 105/2001, art. 1º, §4º) |

O fornecimento judicial dos registros de conexão e de acesso exige, sob pena de inadmissibilidade, fundados indícios do ilícito, justificativa motivada da utilidade dos registros e o período a que se referem (art. 22, parágrafo único, do Marco Civil). O provedor de conexão não pode guardar registros de acesso a aplicações (art. 14), de modo que o caminho é sempre da aplicação para a conexão: a plataforma dá o IP e o horário, e só com eles o provedor de conexão diz quem estava conectado. Os dados cadastrais de qualificação, filiação e endereço têm regime próprio: o delegado e o Ministério Público os acessam sem autorização judicial junto a empresas telefônicas, instituições financeiras, provedores de internet e administradoras de cartão (art. 15 da Lei 12.850 e art. 17-B da Lei 9.613, este incluído pela Lei 12.683/2012), e o Marco Civil ressalva o acesso das autoridades administrativas com competência legal para requisitá-los (art. 10, §3º). Nas leis lidas não há prazo de guarda para o cadastro de linha nem para imagens de câmera. Se os arts. 15 da Lei 12.850 e 17-B da Lei 9.613 alcançam investigações que não sejam de organização criminosa ou de lavagem é questão interpretativa que esta nota não resolve.

## Primeira etapa: quanto tempo separa o fato da denúncia

| Intervalo do fato à denúncia | INV (33) | CL (47 com data) | FE (113) |
| --- | --- | --- | --- |
| Até 6 meses | 13 (39,4%) | 5 (11,2%) | 14 (11,3%) |
| 6 a 12 meses | 7 (21,2%) | 2 (4,4%) | 14 (12,7%) |
| 12 a 24 meses | 5 (15,2%) | 13 (28,4%) | 36 (32,4%) |
| 24 a 60 meses | 7 (21,2%) | 24 (51,1%) | 48 (43,0%) |
| Mais de 60 meses | 1 (3,0%) | 3 (4,9%) | 1 (0,6%) |
| Mediana (quartis), em meses | 8,1 (2,7 a 24,2) | 28,2 (17,7 a 45,0) | 21,6 (12,4 a 32,9) |

A fraude vai à denúncia, tipicamente, no segundo ano depois do fato, e o CL, no terceiro. A invasão é mais rápida porque concentra prisões no ato (10 das 33, contra 17 das 113 na FE e 2 das 48 no CL) e operações com busca e apreensão. Somadas as três camadas, a denúncia com o autor preso no ato tem mediana de 7,3 meses (29 denúncias, quartis de 0,7 a 20,4) e a demais, de 23,4 meses (164, quartis de 16,0 a 34,9). O que encurta o tempo é a prisão, que dispensa a reconstrução pelo dado.

| Canal do ardil | Denúncias com data | Mediana (quartis), em meses | Depois de 6 meses | Depois de 1 ano | Depois de 5 anos |
| --- | --- | --- | --- | --- | --- |
| Internet | 106 | 27,0 (17,5 a 37,7) | 97 | 88 | 2 |
| Telefonia | 31 | 20,4 (10,2 a 30,8) | 27 | 22 | 0 |
| Presencial | 14 | 12,9 (3,7 a 27,6) | 10 | 8 | 2 |
| Correio ou sem contato | 4 | 27,7 | 4 | 4 | 0 |
| Sistema como objeto | 38 | 8,6 (2,8 a 21,4) | 23 | 16 | 1 |

O canal mais lento é o da internet, e é nele que os prazos de guarda são mais curtos. Na data da denúncia, o prazo legal de guarda dos registros de acesso do canal já tinha passado em 97 das 106, e o dos de conexão, em 88; os registros de ligação e os bancários seguiam dentro do prazo em quase todas (só 5 das 193 denúncias passam de cinco anos). Pelo nível alcançado da questão 1, na FE e no CL, a denúncia de só conta tem mediana de 26,8 meses (100), a de autor remoto, de 22,7 (37), a de autor presencial, de 13,0 (13), e a de elo logístico, de 11,8 (10); 6 dos 10 elos logísticos foram presos no ato da entrega ou do saque, contra 2 dos 101 titulares de conta.

## Segunda etapa: de quem vem o dado que a denúncia narra

| Fonte narrada | INV (33) | CL (48) | FE (113) |
| --- | --- | --- | --- |
| Banco | 7 (21,2%) | 22 (47,1%) | 29 (26,4%) |
| Material da vítima | 10 (30,3%) | 24 (48,8%) | 49 (42,3%) |
| Operadora | 3 (9,1%) | 2 (4,1%) | 9 (9,6%) |
| Plataforma | 2 (6,1%) | 0 | 0 |
| Provedor de conexão | 3 (9,1%) | 0 | 0 |
| Aparelho apreendido | 5 (15,2%) | 1 (2,2%) | 5 (4,1%) |
| Câmeras | 0 | 0 | 1 (0,7%) |

Plataforma e provedor de conexão só aparecem quando o sistema é o objeto: o INV 2 (a Vivo vinculou o IP da criação de uma conta Google a uma linha usada com 12 IMEIs, e Facebook e Google forneceram dados das contas do denunciado), o INV 42 (a Meta informou o celular cadastrado na conta invadida e a TIM, o titular da linha), o INV 30 (o IP do acesso a um servidor, da Claro, com cadastro em nome da esposa do acusado) e o INV 11 (consultas feitas de modem da Vivo em nome da mãe do denunciado). No INV 34, o IP do invasor veio da auditoria da própria empresa atacada. Na fraude contra a pessoa, nenhuma denúncia narra dado de plataforma ou de conexão, embora 60 das 106 do canal internet tenham passado pelo WhatsApp, 19 por sites e 12 por redes sociais.

O que a fraude traz de terceiro custodiante é a linha. As 16 denúncias com dado de operadora, plataforma ou conexão estão assim, na data da denúncia:

| Denúncia | Canal | Meses até a denúncia | O que veio | Efeito |
| --- | --- | --- | --- | --- |
| FE 13 | internet | 29,2 | a Claro informou que a linha do falso vendedor estava em nome do correntista denunciado | identificou |
| FE 25 | internet | 28,3 | a linha que falou com a vítima estava em nome da denunciada; a da chave Pix, em nome de terceira, arquivada | identificou |
| FE 55 | internet | 24,7 | a Vivo identificou o denunciado como titular da linha usada no golpe | identificou |
| FE 108 | internet | 22,5 | a TIM informou que a linha pertencia à denunciada no período do fato | identificou |
| FE 61 | telefonia | 20,4 | a linha TIM usada no contato foi habilitada por um dos denunciados | identificou |
| INV 2 | sistema-objeto | 32,9 | IP, linha e dados de contas Google e Facebook do denunciado | identificou |
| INV 42 | sistema-objeto | 23,8 | celular cadastrado na conta invadida (Meta) e titular da linha (TIM) | identificou |
| INV 11 | sistema-objeto | 21,0 | modem da Vivo em nome da mãe do denunciado, no endereço dele | identificou |
| INV 30 | sistema-objeto | 6,0 | IP da Claro com cadastro em nome da esposa do acusado | identificou |
| FE 14 | internet | 37,0 | linha da falsa leiloeira em nome de terceiro, com o endereço da empresa da denunciada | corroborou |
| INV 36 | sistema-objeto | 19,8 | linha usada pela funcionária em nome de outra denunciada | corroborou |
| CL 22 | internet | 23,1 | linha pré-paga do golpe em nome de terceiro, arquivado | apontou terceiro |
| CL 54 | internet | 37,6 | linha em nome de terceiro, arquivado | apontou terceiro |
| FE 66 | internet | 21,1 | titulares das linhas não indiciados nem denunciados | apontou terceiro |
| FE 5 | telefonia | 19,3 | linha que recebeu os comprovantes em nome de terceiro não denunciado | apontou terceiro |
| FE 16 | internet | 29,5 | linha pré-paga cancelada e desprogramada, sem titular | sem resultado |

A linha identificou o denunciado na fraude quando coincidiu com outra trilha: o titular da linha era também o correntista (FE 13), a denunciada recebeu o Pix (FE 25, FE 108), o titular reunia outros elementos (FE 55, FE 61). Sozinha, levou ao arquivamento. No CL 22, a cota diz por quê: a linha pré-paga é "facilmente habilitada em nome de terceiros por golpistas". O FE 16 mostra o outro limite, que não é o do Marco Civil: a linha pré-paga cancelada e desprogramada não devolveu titular, e o que se perde ali é o vínculo entre o número e a pessoa, antes de qualquer prazo de guarda.

O titular da conta, ao contrário, é nomeado sem precisar do banco. Das 101 denúncias de só conta, 42 narram dado obtido do banco, 21 narram só o material da vítima e 38 não narram fonte, nomeando o titular da conta "de titularidade de" alguém que o golpista indicou à vítima e que o comprovante registra. A camada que a base alcança é a que já estava no bolso da vítima no dia do registro.

## Terceira etapa: o que a cota pede

| Denúncia | Meses até a denúncia | Pedido ou providência | Alvo |
| --- | --- | --- | --- |
| CL 7 | 0,4 | requer quebra bancária | contas de destino, com cadastro, selfies e extratos, para rastrear o dinheiro |
| INV 32 | 0,4 | apoia representação policial | quebra bancária e fiscal das contas dos denunciados, via BACEN |
| FE 105 | 13,0 | requer ofício à delegacia | extratos da vítima das duas operações, que a denúncia não tinha |
| FE 113 | 19,0 | requer ofício | extrato da conta do indiciado |
| FE 5 | 19,3 | requer quebra bancária | cadastro e extratos da conta do denunciado |
| FE 74 | 22,1 | junta resultado | quebra bancária da denunciada |
| FE 122 | 23,4 | apoia representação policial | quebras bancária e telefônica e bloqueio, depois da prisão, para alcançar comparsas |
| FE 14 | 37,0 | requer ofício | documentação da abertura da conta e fotografia do titular |
| INV 13 | 0,2 | requer perícia | celular da vítima |
| INV 21 | 0,5 | aguarda laudos | aparelhos eletrônicos apreendidos |
| FE 17 | 0,8 | requer extração | dados do celular apreendido, para apurar a associação |
| INV 28 | 0,9 | requer perícia | objetos apreendidos |
| CL 56 | 2,1 | aguarda laudos | material apreendido |
| INV 8 | 3,5 | aguarda resultado | quebra telefônica já autorizada |
| FE 103 | 4,7 | indica representação futura | dados telefônicos e telemáticos do celular apreendido |

A cota pede dado em 15 das 194 denúncias, e pede ao custodiante cujo dado não venceu: o banco, dentro dos cinco anos, e o aparelho, que está apreendido. No FE 105 pede à própria vítima, pela delegacia, o extrato das duas operações, porque a denúncia saiu treze meses depois do flagrante sem a prova de que o dinheiro chegou à conta do denunciado que a forneceu. Nenhuma pede preservação, nenhuma se dirige a plataforma ou a provedor de conexão. Os pedidos bancários dos casos lentos (FE 5, FE 113, FE 14, de 19 a 37 meses depois do fato) ainda estão dentro do prazo do art. 10, §2º, da Lei 9.613; os dos casos rápidos (CL 7 e INV 32, com 12 dias) vêm de prisões no ato e miram as contas seguintes, que é a única extensão da investigação que a base registra na denúncia. Três cotas mencionam a camada de cima e a deixam para depois ou para outro feito (FE 17, FE 103, FE 122), sempre a partir de um celular apreendido. A cota do FE 66 declara não requerer diligências sobre os titulares das linhas.

## Protocolo de preservação por canal

O protocolo segue o que a base mostra: o dado que identifica o autor remoto vence antes da denúncia, e o que sobrevive identifica o titular da conta. Ele se executa no registro da ocorrência ou nos primeiros dias do inquérito.

| Canal ou elemento | Custodiante e dado | Guarda | Providência imediata | Fundamento |
| --- | --- | --- | --- | --- |
| Conversa, anúncio, perfil ou e-mail usado no golpe | a vítima: o aparelho e o histórico | enquanto a vítima não apagar | orientar a vítima a não apagar a conversa, exportar o histórico e registrar número, nome do perfil, endereço do anúncio e horário dos contatos; são o identificador e o período de que os pedidos seguintes dependem | |
| Aplicação usada (WhatsApp, rede social, marketplace, site, e-mail) | provedor de aplicação: registros de acesso da conta usada (IP, data e hora) | 6 meses | requerimento cautelar de guarda pela polícia ou pelo Ministério Público, com o identificador e o período; pedido judicial de fornecimento em até 60 dias, com indícios, utilidade e período | Lei 12.965/2014, arts. 15, caput e §2º, 13, §§3º e 4º, e 22 |
| IP devolvido pela aplicação | provedor de conexão: registros de conexão | 1 ano | requerimento cautelar de guarda assim que o IP chegar e pedido judicial de fornecimento | Lei 12.965/2014, arts. 13, caput e §2º, e 22 |
| Linha que falou com a vítima ou que sustenta o WhatsApp | operadora: cadastro do titular e registros de ligações | cadastro sem prazo nas leis lidas; ligações, 5 anos | requisição do cadastro logo, antes que a linha pré-paga seja cancelada; leitura do titular como pista, cruzada com a conta e com o dinheiro, e não como autor | Lei 12.850/2013, arts. 15 e 17; Lei 9.613/1998, art. 17-B |
| Conta que recebeu o dinheiro | banco ou instituição de pagamento: cadastro, documentos e selfie da abertura, transações e repasses | no mínimo 5 anos | requisição do cadastro e da documentação de abertura; quebra judicial dos repasses, que é o único caminho da camada das contas para a seguinte | Lei 9.613/1998, arts. 10, §2º, e 17-B; LC 105/2001, art. 1º, §4º |
| Entrega, saque, maquininha | quem mantém as câmeras (agência, comércio, condomínio, vizinhança) | sem prazo nas leis lidas | pedido imediato das imagens ao detentor (no FE 81 a câmera da vizinhança registrou a ação) | |
| Sistema como objeto | o titular do sistema atacado: os próprios registros; e os provedores de conexão dos IPs | os do titular; conexão, 1 ano | preservação dos registros do sistema pelo titular (como a auditoria do INV 34) e guarda junto ao provedor de conexão de cada IP | Lei 12.965/2014, art. 13 |

Duas observações de uso. A primeira é a ordem: o pedido à aplicação precede o pedido ao provedor de conexão, porque só a aplicação sabe o IP da conta, e os seis meses dela são o prazo que governa a investigação inteira. A segunda é o peso de cada registro: o cadastro da conta, verificado na abertura, sustenta as 101 denúncias de só conta; o da linha pré-paga, sozinho, sustentou arquivamentos. Uma política que endureça a verificação de identidade na habilitação de linhas faria pela trilha telefônica o que a biometria fez pela bancária, que é tornar o registro atribuível depois do fato, sem prevenir a cessão.

## Limites

A base é de denúncias e sentenças; os ofícios, as representações e as respostas dos provedores estão no inquérito, que não foi lido. Uma denúncia que não narra dado de plataforma pode vir de inquérito que o pediu e não o recebeu, ou que o recebeu e não o usou; o que se afirma é o que chega à acusação. A data do fato é a primeira da narrativa, e em denúncias com vários fatos o intervalo é o do mais antigo. A leitura de fontes por termos tem a imprecisão de toda triagem, menor nos custodiantes não bancários, que foram lidos um a um. A amostra de denúncias com dado de terceiro (16) é pequena, e a assimetria entre o registro da conta e o da linha se apoia em quatro decisões fundamentadas de não denunciar o titular da linha (CL 22, CL 54, FE 66 e a terceira do FE 25) e num titular não denunciado sem fundamentação na denúncia (FE 5), não em contagem.

## Fontes conferidas nesta sessão

- Lei 12.965/2014 (Marco Civil da Internet), arts. 10, §3º, 13, caput e §§2º a 4º, 14, 15, caput e §2º, e 22: https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2014/lei/l12965.htm
- Lei 12.850/2013, arts. 15 e 17 (e art. 1º, §1º, e art. 2º, caput, usados na questão 4): https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2013/lei/l12850.htm
- Lei 9.613/1998, arts. 9º, 10, I, II e §2º, e 17-B (incluído pela Lei 12.683/2012): https://www.planalto.gov.br/ccivil_03/leis/l9613compilado.htm
- Lei Complementar 105/2001, art. 1º, caput e §4º: https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp105.htm
- Questão 1 (biometria na abertura de conta em 11 denúncias; nível alcançado): `docs/analise/q1-alcance-elo-fisico.md`
