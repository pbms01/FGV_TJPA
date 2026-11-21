# Livro de códigos: sentenças (segundo leitor)

Você é o segundo leitor de uma codificação de sentenças criminais de primeiro grau do TJSP sobre fraude eletrônica, conta de passagem ("conta laranja") e invasão de dispositivo informático. Para cada caso do seu lote há dois arquivos: `Sxx_sentenca.txt` (a sentença) e `Sxx_denuncia.txt` (a denúncia do mesmo processo). Codifique os campos abaixo pelo que o texto diz. Não há resposta "esperada": codifique o que o texto sustenta.

Cuidados de leitura. A sentença tem relatório (o que as partes pediram), fundamentação e dispositivo. Os campos de decisão se leem na fundamentação e no dispositivo, não no relatório. Sentenças citam ementas e trechos de acórdãos de outros processos; o que esses trechos dizem não é decisão deste processo. Alguns arquivos são longos (mais de 100 mil caracteres): use busca por termos para achar o dispositivo, a dosimetria e o trecho da reparação, mas leia o trecho inteiro antes de codificar.

## Bloco 1: dispositivo

resultado: condenação (todos os réus condenados por ao menos uma imputação e nenhuma absolvição dita); procedência parcial (condena alguém e absolve alguém ou de alguma imputação); absolvição; extinção (da punibilidade, sem condenação); indeterminado.

tipo_acolhido: entre os crimes da condenação (de qualquer réu), o primeiro que aparecer nesta lista de prioridade: 154-A; 171 §2º VII; 171 §2º-A; 155 §4º-B; 171 outro (171 sem §2º-A nem inciso VII, inclusive §§1º, 3º e 4º); 155 outro; 158; 157; 180; 288; lavagem; drogas; 147; 307; falsidade. Se nenhum, "outro"; sem condenação, vazio.

pena_meses: a primeira pena privativa de liberdade fixada no dispositivo (a do primeiro réu condenado), em meses (anos × 12 + meses; dias como fração de 30). Sem condenação, vazio.

regime: aberto, semiaberto, fechado ou vazio, da mesma pena.

substituida: sim se essa pena foi substituída por restritivas de direitos; não; vazio sem condenação.

lei_15397: só para sentença datada de 04/05/2026 em diante; nas anteriores, "anterior". aplica (condena alguém no art. 171, §2º, VII, do CP, criado pela Lei 15.397/2026); recusa (discute o inciso VII e decide não aplicá-lo); menciona (cita a lei ou o inciso sem decidir sobre ele, ou só como argumento); sem menção.

## Bloco 2: reparação mínima (art. 387, IV, do CPP)

rep_status, só nas condenações: fixa (a sentença fixa valor mínimo de reparação ou condena a ressarcir, indenizar ou pagar à vítima); nega (decide expressamente não fixar, com ou sem fundamento); silente (não diz nada sobre reparação). Sem condenação, "n/a".

rep_material: soma, em reais, dos valores fixados como dano material ou sem qualificativo (use ponto decimal, sem separador de milhar: 4825.81). Se houver valor por réu, some os valores de réus diferentes; se houver um total e suas parcelas, conte só o total. Fixação sem valor dito (por exemplo, "o valor da fiança"): escreva "sem valor".

rep_moral: soma dos valores fixados expressamente como dano moral; 0 se nenhum.

rep_fundamentos, só quando nega (um ou mais, separados por |): sem pedido; contraditório e instrução; valor não apurado; vítima ressarcida; sem prejuízo; remete à via cível; ação cível em curso; reparação por outro instrumento (prestação pecuniária, acordo do corréu); outro.

rep_moral_negado: sim se a sentença recusa expressamente o dano moral (mesmo fixando o material); não.

rep_individualizada: sim se a sentença limita o valor de cada condenado ao que entrou na conta dele, ou reparte o valor entre os réus pelo que cada um recebeu; não.

rep_solidaria: sim se a sentença declara a obrigação solidária; não.

intermediario_ressarciu: sim se a sentença narra que banco, instituição de pagamento ou empresa cobriu, no todo ou em parte, o prejuízo da vítima (afirmação de fato aceita pela sentença, não mera alegação da defesa); não.

## Bloco 3: consequências do crime na dosimetria (art. 59 do CP)

conseq_valoracao: negativa (as consequências pesaram contra o réu na pena-base); neutra (examinadas e tidas como normais ou inerentes ao tipo); não examinada (a sentença não as examina uma a uma, ou só as menciona em lista genérica, ementa citada ou pedido da parte). Sem condenação, "n/a".

conseq_danos, só quando negativa (um ou mais, separados por |), pelos temas de Agrafiotis et al. (2018): econômico (prejuízo, valor, patrimônio); psicológico (abalo, medo, sofrimento, insegurança, frustração); digital (dados pessoais expostos ou usados, conta ou sistema comprometido, trabalho ou arquivos perdidos); reputacional (imagem, honra, clientela); social (família, trabalho, relações, instituição, serviço público, saúde pública); físico (saúde, integridade corporal).

## Bloco 4: pedido de reparação na denúncia (leia `Sxx_denuncia.txt`, sobretudo o fim)

pedido_reparacao: sim (a denúncia pede fixação de valor mínimo de reparação, indenização ou ressarcimento à vítima, com ou sem valor); não; recusa (o MP declara que não pede). A reparação como condição de suspensão do processo ou de acordo não conta.

pedido_valor: o valor pedido, se houver; vazio se não.

pedido_moral: sim se o pedido inclui dano moral; não.

## Saída

Grave um CSV em UTF-8, com cabeçalho, no caminho indicado no seu lote, com estas colunas, nesta ordem:

id,resultado,tipo_acolhido,pena_meses,regime,substituida,lei_15397,rep_status,rep_material,rep_moral,rep_fundamentos,rep_moral_negado,rep_individualizada,rep_solidaria,intermediario_ressarciu,conseq_valoracao,conseq_danos,pedido_reparacao,pedido_valor,pedido_moral,confianca,nota

- id: o identificador do caso (por exemplo, S07).
- confianca: alta, media ou baixa, para o conjunto da codificação daquele caso.
- nota: até três frases com o que sustenta os campos mais difíceis (reparação, consequências, resultado) e, entre aspas, trechos curtos (até 25 palavras cada) da sentença. Use aspas duplas no campo e escape aspas internas, para o CSV ficar válido.
