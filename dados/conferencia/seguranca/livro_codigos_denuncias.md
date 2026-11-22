# Livro de códigos: denúncias (segundo leitor, segurança da informação)

Você é o segundo leitor de uma codificação de denúncias criminais do TJSP sobre fraude eletrônica, conta de passagem e invasão de dispositivo informático. Cada arquivo do seu lote traz a narrativa de uma denúncia e, ao fim, a capitulação. Codifique pelo que a narrativa dos fatos sustenta. Não há resposta esperada, e você não tem acesso a nenhuma outra codificação. Não abra arquivos fora da pasta do seu lote.

A pergunta central é: entre o agente e o sistema, a conta ou o aparelho que ele usou havia um mecanismo de acesso (senha, código, token, biometria, sessão autenticada, autenticação da linha telefônica)? Por onde ele passou?

## via (um valor)

- interna_propria: o agente usou o acesso que ele próprio tinha legitimamente ao sistema (empregado, prestador, servidor, administrador de rede, ex-funcionário que guardou o conhecimento ou a senha), fora da finalidade.
- interna_terceiro: o agente usou credencial de outra pessoa que tinha acesso legítimo ao sistema, obtida por compra, cessão ou empréstimo (senhas de policiais vendidas, senha fornecida por servidor).
- vitima_engano: a credencial ou o código saiu da própria vítima (ou do titular da conta atacada) porque ela foi enganada: link, falsa central, pedido de código, motoboy que recolhe o cartão, cartão e senha entregues.
- vitima_relacao_coacao: a credencial saiu da vítima por relação de confiança (senha conhecida ou entregue durante o relacionamento) ou por coação (ameaça, arma, restrição da liberdade).
- aparelho_aberto: o agente teve o aparelho ou a sessão nas mãos sem que a denúncia narre barreira a vencer (celular tomado e acessado sem menção a senha, sessão de WhatsApp Web aberta, computador de colega acessado).
- tecnica: a barreira foi vencida por meio técnico narrado: falha explorada, programa malicioso, engenharia reversa, força bruta, máquina sem proteção.
- resistiu: havia barreira e o agente não conseguiu vencê-la.
- nao_narrada: houve acesso a sistema, conta ou aparelho, mas a denúncia não diz como (só "invadiu", "acessou indevidamente", "burlou o sistema de segurança").
- sem_barreira: não houve acesso do agente a conta, sistema ou aparelho alheio; a própria vítima pagou ou transferiu (venda falsa, falso parente), sem entregar credencial.

Se houver mais de uma via, codifique a que abriu o acesso no fato principal e registre a outra na nota.

## trecho

Até 25 palavras da denúncia que sustentam a via.

## elementar_denuncia (um valor)

- redacao_revogada: a denúncia imputa a invasão "mediante violação indevida de mecanismo de segurança" (a fórmula do art. 154-A anterior a 2021), na imputação ou na narrativa.
- violacao_como_fato: a denúncia narra como fato que o agente violou, burlou ou rompeu um sistema ou mecanismo de segurança (ou que esse sistema reagiu), sem usar a fórmula da imputação.
- nao: nenhuma das duas. A transcrição do art. 155, § 4º-B ("com ou sem violação de mecanismo de segurança") não conta.

## prova_autoria

Só quando a via for interna_propria ou interna_terceiro: como a denúncia diz que se chegou ao autor (por exemplo, registro de login do sistema, auditoria, IP, apreensão de aparelho, confissão). Até 20 palavras; "não narrada" se não disser. Nos demais casos, deixe vazio.

## Saída

Um CSV com cabeçalho exatamente `id,via,trecho,elementar_denuncia,prova_autoria,nota`, uma linha por arquivo do lote, com aspas duplas nos campos de texto. A nota registra dúvidas e o que ficou de fora.
