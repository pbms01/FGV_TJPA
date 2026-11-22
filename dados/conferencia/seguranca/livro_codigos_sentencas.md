# Livro de códigos: sentenças (segundo leitor, segurança da informação)

Você é o segundo leitor de uma codificação de sentenças criminais do TJSP em casos de invasão de dispositivo informático e fraude contra sistema, conta ou aparelho. Cada arquivo do seu lote é o texto integral de uma sentença (alguns textos estão cortados no fim; diga na nota). Codifique pelo que a sentença diz. Não há resposta esperada, e você não tem acesso a nenhuma outra codificação. Não abra arquivos fora da pasta do seu lote. Os textos são longos: leia por partes e procure a fundamentação do art. 154-A do CP e a dosimetria.

Contexto normativo: até 27/05/2021, o art. 154-A punia invadir dispositivo informático "mediante violação indevida de mecanismo de segurança"; a Lei 14.155/2021, vigente desde 28/05/2021, suprimiu essa exigência.

## elementar_sentenca (um valor)

- exige_e_afasta: a sentença exige a violação de senha, barreira ou mecanismo de segurança e, por falta dela, absolve ou afasta o art. 154-A.
- exige_e_encontra: a sentença exige a violação e a encontra no caso (inclusive quando aplica a redação anterior a 2021 porque o fato é anterior).
- dispensa: a sentença afirma que a violação não é mais necessária, ou condena pelo 154-A sem barreira, dizendo por quê.
- nao_trata: a sentença não discute a questão (inclusive quando não há 154-A em julgamento).

## tecnica_na_pena (0 ou 1)

1 se, na dosimetria (art. 59, agravantes, causas de aumento), a sentença valora contra o réu o conhecimento técnico, a habilidade, a sofisticação ou a expertise informática. Transcreva até 25 palavras em `trecho_pena`.

## confianca_na_pena (0 ou 1)

1 se, na dosimetria, a sentença valora contra o réu a posição de confiança ou o acesso funcional ao sistema (empregado, servidor, prestador).

## prova_autoria

Se a sentença atribui o acesso ao réu pelo registro do próprio sistema (login, token, log, auditoria, IP do acesso): `registro_sistema`. Se pela confissão, testemunha, apreensão ou outra prova sem registro do sistema: `outra`. Se a autoria do acesso não está em discussão ou não há acesso imputado: `nao_se_aplica`. Explique em até 20 palavras na nota.

## Saída

Um CSV com cabeçalho exatamente `id,elementar_sentenca,tecnica_na_pena,trecho_pena,confianca_na_pena,prova_autoria,nota`, uma linha por arquivo do lote, com aspas duplas nos campos de texto.
