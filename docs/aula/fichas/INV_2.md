# Aula de segurança da informação, par único, âncora: INV 2

Par: INV 2 (âncora, TJSP) e AP 2428 (contraste, STF). Perguntas examinadas: 1 (como a barreira cai), 2 (a barreira no processo) e 4 (quem tem a chave). Frase do par: nos dois casos a barreira não foi quebrada pela técnica, foi aberta por credenciais legítimas; aqui, a credencial própria de uma funcionária da operadora; lá, credenciais de servidores e de uma magistrada tomadas por quem não as tinha.

## Identificação

- Exercício: "O chip que mudou de mão às 21h57".
- Processo 1500431-37.2021.8.26.0482, 3ª Vara Criminal de Presidente Prudente. Estrato INV.
- Fatos de 20 a 22/01/2021 contra as vítimas de Presidente Prudente, com a organização narrada desde 2019; fato anterior à Lei 14.155/2021, de modo que o 154-A é o da redação de 2012, que exigia a "violação indevida de mecanismo de segurança". Denúncia de 17/10/2023 (32,9 meses depois do fato, questão 5). Sentença de 26/09/2025, publicada no DJEN em 29/09/2025; recurso de uma das rés recebido em 06/10/2025. Andamento em segundo grau não verificado.
- Peças lidas: a denúncia (quatro partes), a sentença (até o limite de 100 mil caracteres do Codex e, a partir dele, no arquivo original, lido em 23/11/2026 pelo link do Codex) e o dispositivo pelo DJEN.
- Casos citados: INV 11 (senhas de policiais compradas, condenado, autoria pelo IP do acesso), INV 8 e INV 45 (acesso interno com autoria pelos logs), INV 13, INV 14 e INV 26 (sentenças que exigem a elementar suprimida e absolvem), INV 38 e INV 44 (que a exigem e a encontram).
- Conferido por segundo leitor cego (via, elementar e prova da autoria; `docs/analise/segundo-leitor-seguranca.md`).

## 1. Conduta registrada

Sete denunciados, em quatro funções que a denúncia nomeia: "crackers", "distribuidores", "correntistas" e "operadores em empresas de telefonia". Os operadores eram funcionários de lojas terceirizadas da operadora, com login, senha e token do sistema de atendimento. Pelo sistema, trocavam o ICCID da linha da vítima, que perdia o sinal e achava que era pane; a linha passava a um aparelho do grupo, que recebia os códigos e entrava nas contas bancárias. A denúncia imputa 171, §2º-A, e 154-A, duas vezes cada, organização criminosa e lavagem.

O sistema é o objeto, e a barreira é a autenticação da linha telefônica, que o banco usa como segundo fator. Ela não foi vencida de fora: foi operada de dentro, por quem tinha a credencial.

O que a denúncia não narra e a sentença traz: o token da operadora trocava a cada 30 segundos; a funcionária fez trocas fora do horário de trabalho (esta às 21h57) e de linhas de DDDs que ela dizia não conseguir atender; ao menos 25 das trocas feitas por ela em um mês correspondem a linhas de vítimas com boletim de ocorrência.

## 2. Processamento

Investigação. Começou por uma transferência de R$ 190,00 a um desconhecido e chegou ao grupo pela conta de destino, pela operadora e pelas contas Google e Apple ligadas aos IMEIs que hospedaram as linhas das vítimas (Vivo, Google e Apple informaram; questão 5).

Sentença, tipicidade. O SIM card é dispositivo informático, e o ICCID, dado nele contido; a troca "destruiu e alterou remotamente" esses dados. Como a redação aplicável exigia a violação de mecanismo de segurança, a sentença a encontrou na própria credencial: "Mediante uso indevido de senha e token, funcionários de lojas terceirizadas da Tim acessaram o sistema da empresa", e "a violação do mecanismo de segurança deu-se por meio do aliciamento de funcionários com acesso ao sistema".

Sentença, autoria. Pelo registro do sistema: a troca foi feita com o login da ré. A tese de que outros usavam a senha dela caiu pelo token de 30 segundos, pelos horários e pelos DDDs.

Dosimetria da funcionária. Para o 154-A, "não se vislumbram elementos de culpabilidade desfavoráveis": pena no mínimo, 3 meses de detenção (preceito da redação de 2012). A culpabilidade só é elevada no furto, pelo concurso de agentes. A posição de quem tinha a credencial dentro do serviço não é valorada.

Dispositivo. Nova definição jurídica do 171, §2º-A, para o 155, §4º, II e IV (art. 383 do CPP); três rés condenadas também pelo 154-A, a funcionária por uma das duas trocas e absolvida da outra e da lavagem (art. 386, V), com 5 anos e 4 meses de reclusão e 3 meses de detenção em semiaberto; as duas outras rés, 9 anos de reclusão em fechado e 3 meses e 15 dias de detenção em semiaberto. Reparação mínima de R$ 190,00; dano moral não arbitrado. Os demais réus seguem em autos desmembrados.

## 3. Leitura pelas perguntas

Pergunta 1. Na base, a técnica é a via em 5 das 41 denúncias em que a passagem está narrada; em 7, a porta foi aberta por quem tinha acesso legítimo. O INV 2 é o caso mais claro dessas 7: a "invasão" é o uso, por quem a tinha, de uma credencial válida.

Pergunta 2. Sob a redação de 2012, a sentença precisou chamar de "violação de mecanismo de segurança" o uso de senha e token legítimos. A leitura é defensável, mas mostra por que a elementar foi suprimida: a barreira estava íntegra, e quem a abriu estava autorizado a abri-la para outro fim. Depois de 28/05/2021 a pergunta já não é de tipicidade, e cinco sentenças da base com fato posterior ainda a fazem: três absolvem por falta da barreira e duas a encontram, contra quatro que a dispensam.

Pergunta 4. A credencial interna é a oportunidade e é a prova: nos 7 acessos internos da base, todos com condenação ao menos parcial, a sentença atribuiu o acesso pelo registro do sistema em 5. O mesmo registro que permitiu a troca permitiu atribuí-la, e o detalhe técnico que decidiu (o token de 30 segundos) é um controle de segurança lido como prova.

O acréscimo ao magistrado. Na cautelar e na instrução, pedir à operadora ou à empresa o registro de quem executou a operação (login, token, horário, terminal) antes do rastro externo; na sentença, distinguir a credencial cedida da credencial própria usada fora da finalidade; na dosimetria, a posição de confiança dentro do serviço é o dado a examinar: aqui ela não pesou, ao passo que no INV 8, também acesso interno, a sentença acentuou a culpabilidade porque os réus "se aproveitaram da relação profissional e da confiança depositada neles".

## 4. Para a turma

1. Onde estava a barreira que o grupo precisava vencer? Resposta esperada: na autenticação da linha telefônica, que o banco usa como segundo fator; ela foi operada por dentro, não quebrada.
2. Por que a sentença precisou encontrar uma "violação de mecanismo de segurança"? Resposta esperada: fato de janeiro de 2021, redação de 2012 do 154-A; a sentença a encontrou no uso indevido de senha e token por funcionários aliciados.
3. Que prova decidiu a autoria da funcionária? Resposta esperada: o registro do sistema da operadora (login, token de 30 segundos, horário fora do expediente, DDDs fora da região), contra a versão de senha compartilhada.
4. A posição da funcionária pesou na pena do 154-A? Resposta esperada: não; pena mínima, culpabilidade sem elementos desfavoráveis. Compare com o INV 8, em que a confiança acentuou a culpabilidade, e discuta qual fundamento o 59 comporta.
5. Compare com a AP 2428. Resposta esperada: aqui a credencial era da própria agente; lá, de servidores e de uma magistrada, tomadas pela recuperação de senha; nos dois, a técnica não foi a quebra da barreira.

## Fontes

- Denúncia: https://github.com/pbms01/FGV_TJPA/tree/main/textos/tjsp/denuncias/1500431-37.2021.8.26.0482
- Sentença (texto cortado em 100 mil caracteres): https://github.com/pbms01/FGV_TJPA/tree/main/textos/tjsp/sentencas/1500431-37.2021.8.26.0482; dosimetria lida no original (Codex, documento 778c9717-aed2-5ea4-8686-57812cb23d04), texto ainda não gravado no repositório.
- Dispositivo: DJEN, disponibilização de 29/09/2025, e recebimento do recurso, 06/10/2025 (consulta pelo Codex em 22/11/2026).
- Via e prova na base: `dados/analise/s_barreira.csv`, nota `docs/analise/s-barreira.md`.
