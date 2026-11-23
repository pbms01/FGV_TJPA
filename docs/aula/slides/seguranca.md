# Segurança da informação e criptografia

Para que serve a criminologia aqui (na prática jurídica)

Entre o agente e o sistema há uma barreira: senha, código, token, biometria, a autenticação da linha telefônica. O direito penal tratou essa barreira como elementar do art. 154-A até 2021. A criminologia informática pergunta por onde a barreira cai de fato, o que o processo faz com ela e quem tem a chave. Na base, quase nunca é a técnica: a porta é aberta por credenciais.

---

# E a barreira?

- Art. 154-A do CP, redação da Lei 12.737/2012: invadir "mediante violação indevida de mecanismo de segurança". A Lei 14.155/2021, vigente desde 28/05/2021, suprimiu a exigência: invadir basta.
- Art. 359-N do CP (Lei 14.197/2021): o processo eleitoral conserva a elementar, "mediante violação indevida de mecanismos de segurança do sistema eletrônico de votação".
- Convenção de Budapeste, art. 2: a Parte pode exigir a violação de medida de segurança só por declaração com base no art. 40, que o Brasil não fez.
- Art. 313-A do CP (Lei 9.983/2000): o funcionário autorizado que insere dados falsos ou altera dados corretos em sistema da Administração, reclusão de 2 a 12 anos; art. 313-B, modificação de sistema sem autorização. Para o empregado privado, não há tipo próprio, e destruir dados com acesso legítimo não tem tipo autônomo (lacuna do art. 4 da Convenção).
- Quem responde pela barreira fraca: art. 14 do CDC e Súmula 479 do STJ (fortuito interno das instituições financeiras).

---

# Segurança: a base teórica

Cohen e Felson, como na Aula 01: a barreira é o guardião capaz. Cornish e Clarke (Crime Prevention Studies, 2003) a põem entre as 25 técnicas de prevenção situacional: controlar o acesso, endurecer o alvo.

Ross Anderson, "Why Cryptosystems Fail" (ACM CCS, 1993): estudando as fraudes em caixas eletrônicos, concluiu que a maioria não vinha da criptoanálise nem de ataques técnicos, e sim de erros de implementação e de falhas de gestão.

A pergunta para os autos: o sistema penal procura a quebra da barreira ou quem tinha a chave?

---

# Segurança: o fenômeno na base

Base TJSP da fase 1, 68 denúncias com barreira entre o agente e o sistema. Análise reproduzível por scripts/analise_s_barreira.py; segundo leitor cego com concordância de 0,74 na via (kappa 0,67), adjudicada e conferida pelo pesquisador.

| Por onde a barreira caiu | Denúncias |
| --- | --- |
| Credencial obtida da vítima por engano | 19 |
| Credencial obtida da vítima por relação ou coação | 5 |
| Credencial própria de quem tinha acesso legítimo | 4 |
| Credencial de colega, comprada ou cedida | 3 |
| Aparelho ou sessão já nas mãos do agente | 4 |
| Técnica (falha, programa malicioso, força bruta) | 5 |
| A barreira resistiu | 1 |
| Via não narrada | 19 |
| Sem barreira: a vítima pagou ou autorizou (maquininha, comprovante falso) | 8 |

A técnica é a via em 5 das 41 denúncias que narram a passagem.

---

# A barreira no processo e quem tem a chave

A barreira no processo. Nas 28 denúncias com o sistema como objeto e fato posterior a 28/05/2021, uma imputa com a redação revogada (INV 33) e seis narram a violação como fato. Nas sentenças com fato posterior à lei que se pronunciam, cinco ainda tratam a barreira como exigência (três absolvem por falta dela: INV 13, INV 14, INV 26; duas a encontram: INV 38, INV 44) e quatro a dispensam. A técnica pesa na pena em uma sentença da base (INV 4, "expertise e habilidade incomuns"); a posição de confiança, em duas (INV 4 e INV 8), e não no INV 2.

Quem tem a chave. Sete acessos internos, todos com condenação ao menos parcial; em cinco, a sentença atribuiu o acesso pelo registro do próprio sistema (login, token, IP, logs).

Quem paga pela barreira fraca. As 12 sentenças com ressarcimento pelo banco ou instituição de pagamento estão nas fraudes que passaram pela segurança do serviço; quando o banco já pagou, a reparação é negada e o dano sai do processo (questões 3 e 6).

| Momento | O que conferir | Dado da base |
| --- | --- | --- |
| Prevenção e dever de cuidado | se a barreira dependia de segredo que a vítima pode recitar ou entregar | a credencial sai da vítima em 24 de 41 vias narradas |
| Investigação | o registro de acesso do próprio sistema antes do rastro externo | autoria interna provada pelo registro em 5 de 7 |
| Recebimento da denúncia | se a imputação usa a redação revogada do 154-A | 1 de 28 com fato posterior à lei |
| Sentença, tipicidade | o 154-A não exige barreira desde 28/05/2021 | 5 sentenças ainda a exigem, contra 4 que a dispensam |
| Sentença, dosimetria | se a técnica ou a posição de confiança foi valorada, com fundamento | técnica em 1, confiança em 2 |

---

# Uma reflexão prática: quem guarda a chave

A lei de 2021 tirou a barreira do tipo porque ela não descreve o fenômeno: na base, a porta é aberta por credenciais, da vítima, de quem tem acesso ou recuperadas, e quase nunca quebrada. Sentenças que ainda procuram a barreira absolvem casos que a lei quis alcançar.

O que separa os casos é de quem era a chave. Com a credencial própria, o registro do sistema aponta quem agiu, e o controle de segurança vira prova. Com a credencial alheia, o registro aponta quem não agiu, e a autoria pede outra trilha.

Para o magistrado: na tipicidade, não exigir barreira depois de 28/05/2021; na prova, perguntar de quem era a credencial que o log registra; na pena, examinar a técnica e a posição de confiança como circunstâncias do art. 59, com fundamento concreto.

---

# ESTUDOS DE CASO

Par TJSP 4 - INV 2 e AP 2428 (STF): nos dois casos a barreira não foi quebrada pela técnica, foi aberta por credenciais legítimas. No INV 2, a credencial própria de uma funcionária da operadora, e o registro a apontou; na AP 2428, credenciais de servidores e de uma magistrada tomadas pela recuperação de senha e por segredos expostos, e o registro apontou quem não agiu.

Âncora: INV 2 (Presidente Prudente). Contraste: AP 2428 (STF, Primeira Turma). Questões examinadas: como a barreira cai, a barreira no processo e quem tem a chave.

---

# INV 2 (âncora)

Identificação. Exercício "O chip que mudou de mão às 21h57": https://claude.ai/artifact/E7N8JER88jeQcvRMwrLfWs

Peças: denúncia https://github.com/pbms01/FGV_TJPA/tree/main/textos/tjsp/denuncias/1500431-37.2021.8.26.0482 e sentença https://github.com/pbms01/FGV_TJPA/tree/main/textos/tjsp/sentencas/1500431-37.2021.8.26.0482

Citados: INV 8 e INV 45 (acesso interno com autoria pelos logs; no INV 8, a confiança pesou na pena); INV 11 (senhas de policiais compradas, autoria pelo IP); INV 13, INV 14 e INV 26 (sentenças que exigem a elementar suprimida e absolvem); AP 2428 (contraste).

Estrato INV. Comarca de Presidente Prudente, 3ª Vara Criminal. Fatos de 20 a 22/01/2021, antes da Lei 14.155/2021; denúncia em 17/10/2023; sentença em 26/09/2025; recurso de uma das rés recebido em 06/10/2025. Peças lidas por inteiro: denúncia e sentença (texto integral do original). Segundo leitor: sim, na via, na elementar e na prova da autoria.

1. Conduta registrada

Sete denunciados em quatro funções: "crackers", "distribuidores", "correntistas" e "operadores em empresas de telefonia". Os operadores, funcionários de lojas terceirizadas da operadora, com login, senha e token, trocavam o ICCID da linha da vítima pelo de um chip do grupo; a vítima perdia o sinal, e o aparelho do grupo recebia os códigos dos bancos. A denúncia imputa 171, §2º-A, e 154-A, duas vezes cada, organização criminosa e lavagem.

O que a denúncia não narra e a sentença traz: o token trocava a cada 30 segundos; a funcionária fez trocas fora do horário (uma às 21h57) e em DDDs que dizia não atender; ao menos 25 trocas dela num mês correspondem a linhas de vítimas com boletim.

2. Processamento

Investigação pela conta de destino de um Pix de R$ 190,00, pela operadora e pelas contas Google e Apple dos aparelhos. Sentença: a violação de mecanismo de segurança, exigida pela redação de 2012, foi achada no "uso indevido de senha e token" por "funcionários com acesso ao sistema"; a autoria, no registro do sistema, contra a versão de senhas emprestadas entre colegas. Nova definição para o furto mediante fraude (155, §4º, II e IV). A funcionária: condenada por uma invasão, absolvida da outra e da lavagem, 5 anos e 4 meses de reclusão e 3 meses de detenção em semiaberto; no 154-A, pena mínima, sem "elementos de culpabilidade desfavoráveis". Reparação mínima de R$ 190,00.

3. Leitura pelas questões

Como a barreira cai. Onde o caso está: entre os 7 acessos internos. O mecanismo: a autenticação da linha, segundo fator dos bancos, operada por dentro. O acréscimo ao magistrado: o SIM swap parece técnica e é uso de acesso funcional.

A barreira no processo. A sentença precisou chamar de violação o uso de credencial legítima; depois de 28/05/2021, a pergunta não é mais de tipicidade.

Quem tem a chave. O registro que permitiu a troca a atribuiu. Na pena, a posição de confiança não pesou, ao contrário do INV 8: circunstância a examinar no art. 59.

---

# AP 2428 (contraste)

Identificação. Exercício "Esqueceu a senha?": https://claude.ai/artifact/FXmWEqe2Vj9g1hSnvBkdLx

Peças: certidão de julgamento e andamentos no portal do STF https://portal.stf.jus.br/processos/detalhe.asp?incidente=6950766 e voto do relator (reprodução) https://www.migalhas.com.br/arquivos/2025/5/5811413F4DB41C_conteudo(2).pdf

Citados: INV 4 (TJSP: o escrevente que entrou na conta gov.br de um juiz pela opção "esqueci a senha", com "expertise e habilidade incomuns" na pena); INV 2 (âncora).

STF, Primeira Turma, relator ministro Alexandre de Moraes. Fatos de agosto de 2022 a janeiro de 2023, posteriores à Lei 14.155/2021; denúncia da PGR recebida em maio de 2024; julgamento em sessão virtual de maio de 2025, unânime; embargos rejeitados em 06/06/2025, com certificação do trânsito em julgado. Segundo leitor: não.

1. Conduta registrada

Ao menos 13 invasões aos sistemas do CNJ, a mando de uma parlamentar, com 16 inserções de documentos falsos, entre eles alvarás de soltura e um mandado de prisão contra ministro do STF. Pelo voto: a funcionalidade "Esqueceu a senha?" do sistema de controle de acesso, credenciais violadas de um funcionário e dados de outro usuário, credenciais forjadas, as credenciais de uma magistrada no Renajud e segredos e tokens expostos por uma vulnerabilidade no GitHub. A denúncia narra que o executor "teria violado indevidamente mecanismos de segurança".

2. Processamento

Art. 154-A, §2º, 13 vezes, e art. 299, 16 vezes, cada grupo em continuidade, em concurso material. O voto aplica a pena da Lei 14.155 sem analisar a elementar. Dosimetria do executor: quatro circunstâncias negativas, com o "reconhecido conhecimento técnico em matéria de invasão de sistemas informatizados" na culpabilidade e o planejamento nas circunstâncias; 4 anos e 6 meses pela invasão e 3 anos e 9 meses pela falsidade, 8 anos e 3 meses em regime fechado; danos materiais e morais coletivos de R$ 2 milhões. A autoria, pela confissão, pelo material entregue e pela investigação.

3. Leitura pelas questões

Como a barreira cai. Onde o caso está: o caso de maior repercussão do período confirma a base; a porta foi aberta pela recuperação de senha e por credenciais. O mecanismo: falhas de gestão de credenciais encadeadas, como em Anderson.

A barreira no processo. Sob a lei nova, a violação narrada migrou do tipo para a pena, com fundamento concreto.

Quem tem a chave. O log registrava as credenciais de servidores e da magistrada, que não agiram. O acréscimo ao magistrado: diante de um log, perguntar de quem era a credencial registrada.
