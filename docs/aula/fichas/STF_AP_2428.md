# Aula de segurança da informação, par único, contraste: AP 2428 (STF)

Par: INV 2 (âncora, TJSP) e AP 2428 (contraste, STF). Perguntas examinadas: 1, 2 e 4. A variável que muda é de quem era a credencial: aqui, de servidores do CNJ e de uma magistrada, tomadas por quem não tinha acesso; no INV 2, da própria funcionária.

## Identificação

- Exercício: "Esqueceu a senha?".
- STF, Primeira Turma, Ação Penal 2428/DF, relator ministro Alexandre de Moraes. Denúncia da PGR (Pet 11626) recebida em maio de 2024; condenação unânime concluída em 14/05/2025; embargos de declaração rejeitados em sessão virtual encerrada em 06/06/2025.
- Fatos entre agosto de 2022 e janeiro de 2023, posteriores à Lei 14.155/2021.
- Caso citado da base: INV 4 (TJSP), o escrevente que entrou duas vezes na conta gov.br de um juiz, mesmo depois da troca de senha e da verificação em duas etapas, e confessou ter usado a opção "esqueci a senha"; condenado no 154-A, §3º, com "expertise e habilidade incomuns" valoradas na pena.
- Peças lidas: o voto do relator, em reprodução publicada pelo Migalhas, lido por extração automática em duas partes; o texto não foi gravado no repositório, e a captura do inteiro teor no portal do STF fica pendente. Não passou pelo segundo leitor.

## 1. Conduta registrada

O executor invadiu ao menos 13 vezes sistemas do CNJ, a mando de uma deputada federal, e inseriu documentos falsos, entre eles um mandado de prisão contra ministro do STF e alvarás de soltura (16 falsidades). Segundo o voto, ele se valeu da funcionalidade "Esqueceu a senha?" da tela de login do Sistema de Controle de Acesso (SCA), que controla o acesso ao BNMP e a outros sistemas, de credenciais violadas de um funcionário e de dados de outro usuário; criou credenciais forjadas; usou as credenciais de uma magistrada no Renajud; e entrou no GitLab do CNJ a partir de uma vulnerabilidade encontrada no GitHub, que expôs segredos e tokens.

O sistema é o objeto, e a barreira é o controle de acesso do próprio CNJ. Ela foi vencida pela recuperação de senha e pelo reaproveitamento de credenciais legítimas, não pela quebra de cifra.

## 2. Processamento

Capitulação. Art. 154-A, §2º, do CP, 13 vezes, e art. 299, 16 vezes, cada grupo em continuidade (art. 71), em concurso material (art. 69).

A elementar. A denúncia narra que o executor "teria violado indevidamente mecanismos de segurança"; o voto aplica a pena da Lei 14.155/2021, registra a alteração do tipo e não analisa a elementar, que já não existia.

Dosimetria do executor. Quatro circunstâncias judiciais negativas: culpabilidade (pleno conhecimento da ilicitude e "reconhecido conhecimento técnico em matéria de invasão de sistemas informatizados"), personalidade, circunstâncias (planejamento detalhado e medidas para dificultar a descoberta) e consequências (dano à credibilidade do sistema de justiça). Pena-base de 2 anos e 3 meses por invasão; agravante do art. 62, IV, compensada com a confissão; aumento de um terço pelo §2º e de metade pela continuidade, 4 anos e 6 meses; falsidade, 3 anos e 9 meses; total de 8 anos e 3 meses em regime fechado. Danos materiais e morais coletivos de R$ 2.000.000,00, solidários, ao fundo do art. 13 da Lei 7.347/1985.

## 3. Leitura pelas perguntas

Pergunta 1. O caso de maior repercussão do período confirma o padrão da base: a porta foi aberta por credenciais, a recuperação de senha e um segredo exposto num repositório; a habilidade do agente estava em encontrar e encadear essas falhas, não em quebrar a criptografia.

Pergunta 2. Com o fato já sob a Lei 14.155, a violação do mecanismo deixa de ser questão de tipicidade e migra para a pena: o "conhecimento técnico" entra na culpabilidade, e o planejamento, nas circunstâncias. Na base estadual, a mesma migração aparece numa sentença, a do INV 4, que é também a mesma via: a recuperação de senha.

Pergunta 4. A credencial de terceiro é o oposto da credencial própria do INV 2: lá a prova da autoria veio do registro, que apontava para a dona da credencial; aqui, o registro apontava para os titulares das credenciais, que não agiram, e a autoria se provou pela confissão, pelo material entregue pelo executor e pela investigação.

O acréscimo ao magistrado. Em invasão por credencial alheia, o log identifica a credencial e não a pessoa: a autoria depende de cruzar o registro com outra trilha. E a técnica do agente, sem a elementar, é matéria de dosimetria que precisa de fundamento concreto, como o voto deu.

## 4. Para a turma

1. Que barreira o executor venceu e como? Resposta esperada: o controle de acesso do CNJ, pela recuperação de senha ("Esqueceu a senha?"), por credenciais de funcionários e de uma magistrada e por segredos expostos no GitHub.
2. A violação de mecanismo de segurança importou à tipicidade? Resposta esperada: não; fatos de 2022 e 2023, sob a Lei 14.155. Importou à pena, pelo conhecimento técnico na culpabilidade.
3. Por que o registro de acesso não bastava para a autoria? Resposta esperada: porque registrava as credenciais de terceiros; foi preciso a confissão e a investigação.
4. Compare com o INV 2. Resposta esperada: lá a credencial era da agente e o registro a apontou; aqui a credencial era de outros e o registro os apontou indevidamente.

## Fontes

- Voto do relator, AP 2428 (reprodução): https://www.migalhas.com.br/arquivos/2025/5/5811413F4DB41C_conteudo(2).pdf
- STF, rejeição dos embargos, 07/06/2025: https://noticias.stf.jus.br/?p=97957
- STF, recebimento da denúncia (Pet 11626): https://noticias.stf.jus.br/?p=91641
- MPF, votos pela condenação e penas: https://www.mpf.mp.br/o-mpf/unidades/procuradoria-geral-da-republica-pgr/noticias/ministros-do-stf-votam-pela-condenacao-de-deputada-federal-por-invasao-ao-sistema-virtual-do-cnj-em-2023
