# Livro de códigos: denúncias (segundo leitor)

Você é o segundo leitor de uma codificação de denúncias criminais do TJSP sobre fraude eletrônica, conta de passagem ("conta laranja") e invasão de dispositivo informático. Leia cada denúncia do seu lote e codifique os campos abaixo pelo que a denúncia narra. Não há resposta "esperada": codifique o que o texto sustenta. O texto pode trazer cota, narrativa (os fatos) e capitulação; codifique pela narrativa dos fatos. Quando a denúncia tiver mais de um fato ou mais de um denunciado, codifique o fato principal (o de maior valor ou o primeiro narrado) e registre na nota o que ficou de fora.

## Campos categóricos (um valor por campo, do vocabulário fechado)

contexto
- patrimonial: fim de obter dinheiro ou bem da vítima.
- violencia_domestica: violência doméstica narrada contra a mulher, ou Lei 11.340/2006 na capitulação. Menção solta não basta (nome do anexo no cabeçalho, outro fato do réu).
- relacional: conflito entre ex-parceiros, conhecidos ou colegas, sem violência doméstica narrada.
- institucional: o fato atinge órgão público ou o próprio sistema de uma instituição (servidor que desvia, acesso a sistema estatal).
- outro: fato sem fraude patrimonial nem invasão (tráfico, anabolizantes, calúnia, furto de fios).

meio_contato (o canal em que o agente falou com a vítima)
- whatsapp: WhatsApp nomeado; o anúncio em rede social ou site seguido de conversa no WhatsApp fica como whatsapp.
- rede_social: Instagram, Facebook, Messenger e semelhantes, sem passagem para o WhatsApp.
- site: loja, leilão ou página falsa; plataforma de venda.
- email: correio eletrônico.
- telefone: ligação, SMS ou aplicativo de mensagens não nomeado.
- boleto: o único contato foi o boleto.
- presencial: face a face.
- sistema: não houve contato com a vítima (invasão, acesso direto à conta ou ao sistema).
- outro: canal inexistente ou não descrito.

artificio (o expediente principal)
- venda_falsa: anúncio ou venda de bem ou serviço inexistente, inclusive o golpe do intermediário.
- falso_parente: o agente se passa por filho, neto, sobrinho ou outro parente da vítima.
- falso_conhecido: se passa por amigo, colega ou conhecido (inclusive WhatsApp clonado de conhecido).
- falsa_central: se passa por banco, financeira, central de atendimento ou empresa; inclui o golpe do motoboy que recolhe o cartão.
- falso_advogado: se passa por advogado ou escritório.
- falso_relacionamento: perfil falso que cria vínculo afetivo e pede dinheiro.
- investimento_falso: falso investimento ou investidor.
- taxa_antecipada: falso empréstimo, falsa vaga ou serviço inexistente com pagamento antecipado (taxa, garantia).
- falsa_taxa_plataforma: cobrança falsa de taxa de plataforma de venda ao vendedor.
- boleto_falso: boleto adulterado ou falso.
- maquininha: máquina de cartão com valor ou visor adulterado.
- compra_fraudulenta_empresa: compra contra empresa com cartão de terceiro, comprovante falso, cadastro falso, ou locação sem devolução.
- extorsao_transferencia: vítima constrangida, sob arma ou ameaça, a transferir ou a entregar cartões e senhas.
- sequestro_conta: tomada de conta (rede social, WhatsApp, e-mail) da vítima, por código obtido ou troca de chip, para pedir dinheiro ou resgate.
- roubo_celular_invasao: roubo ou furto do celular seguido de acesso aos aplicativos.
- invasao_sistema_bancario: invasão de conta ou sistema bancário ou de pagamento para transferir ou sacar.
- invasao_sistema_venda_dados: invasão de sistema para extrair ou vender dados.
- insider_empresa: empregado ou prestador que usa o acesso interno ao sistema da empresa.
- insercao_dados_falsos: inserção de dados falsos em sistema (servidor público, cadastro).
- controle_parceira: acesso ao celular, contas ou redes da parceira ou ex-parceira para controlar, vigiar ou expor.
- devassa_privacidade: invasão para ler e divulgar comunicações, sem fim patrimonial e fora da relação de parceria.
- outro: denúncia sem fraude nem invasão.

papel_denunciado (o papel do denunciado, ou dos denunciados, no fato)
- titular_conta: o vínculo descrito do denunciado com o fato é a conta que recebeu o valor (cedida, vendida, emprestada ou aberta para o golpe), inclusive quando ele arregimenta contas de terceiros.
- executor: fez a abordagem, o contato ou a operação, sem que conta sua recebesse o valor.
- misto: a mesma pessoa executa e recebe na própria conta, ou denunciados diferentes têm esses papéis.
- invasor: autor da invasão sem fim patrimonial ou voltada à venda de dados.

## Indicadores binários (0 ou 1)

- whatsapp: o golpista usou WhatsApp.
- pix_pagamento: o valor saiu da vítima, ou da conta dela, para o recebedor por Pix, inclusive Pix feito pelos golpistas de dentro da conta da vítima. Pix tentado, Pix de pulverização posterior ou comprovante falso de Pix não contam.
- boleto: a vítima pagou boleto.
- falso_parente: há falso parente.
- falsa_central: há falsa central (banco, financeira, empresa).
- venda_falsa: há venda falsa.
- investimento: há falso investimento.
- conta_do_denunciado: o valor do fato entrou em conta de denunciado. Nos fatos fora da tipologia (tráfico, anabolizantes), 0.
- invasao: invasão de dispositivo ou acesso não autorizado a conta ou sistema, inclusive aplicativos de celular roubado. A engenharia social em que a própria vítima valida o aparelho do golpista ou entrega a senha é 0.

## Saída

Grave um CSV em UTF-8, com cabeçalho, no caminho indicado no seu lote, com estas colunas, nesta ordem:

id,contexto,meio_contato,artificio,papel_denunciado,whatsapp,pix_pagamento,boleto,falso_parente,falsa_central,venda_falsa,investimento,conta_do_denunciado,invasao,confianca,nota

- id: o identificador do arquivo (por exemplo, D07).
- confianca: alta, media ou baixa, para o conjunto da codificação daquele caso.
- nota: uma ou duas frases com o fato que sustenta a codificação e, entre aspas, um trecho curto (até 25 palavras) da denúncia que a justifique. Use aspas duplas no campo e escape aspas internas, para o CSV ficar válido.
