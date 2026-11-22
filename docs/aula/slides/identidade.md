# Identidade Digital e Anonimato

Para que serve a criminologia aqui (na prática jurídica)

No crime informático, o sistema interpõe uma credencial entre a pessoa e o ato. A persecução alcança a credencial (a conta, a linha, o perfil, o cadastro) e só alcança a pessoa quando a credencial leva até ela. A criminologia informática dá ao intérprete o que o texto normativo não contém: o conhecimento de como essa distância entre o nome registrado e a pessoa que age se produz, e de como o processo a trata.

O anonimato que importa aos autos raramente é a ausência de identidade (Tor, criptoativos). É identidade deslocada: a conta, o chip, o perfil ou o documento de uma pessoa real, usados por outra.

---

# Essa contribuição opera em 2 planos

1. O alcance do tipo

A falsa identidade tem tipo próprio desde 1940 (art. 307 do CP), mas subsidiário: só incide "se o fato não constitui elemento de crime mais grave". A cessão de documento de identidade também (art. 308). A cessão de conta ganhou tipo em 2026 (art. 171, §2º, VII, Lei 15.397/2026). O que decide é se a identidade se exaure no golpe ou tem potencialidade própria (Súmula 17 do STJ).

2. A prova da pessoa

Quando o titular nega a conta, a titularidade não responde à negativa, porque é ela o que a negativa contesta. Quem responde é o procedimento de abertura que a instituição está obrigada a adotar para "verificar e validar a identidade e a qualificação dos titulares da conta" (art. 2º da Resolução CMN 4.753/2019).

---

# Analisando o fenômeno

Base TJSP da fase 1: 198 denúncias e suas sentenças (164 de fraude, 50 no estrato CL e 114 no FE; 34 de invasão de dispositivo). Contagens simples por estrato. Análise reproduzível por scripts/analise_i_identidade.py no repositório pbms01/FGV_TJPA; segundo leitor cego com concordância de 81,6% na abertura (31 de 38) e 91,7% na identidade usada (22 de 24), adjudicada.

De quem é a identidade que o golpe usa diante da vítima:

| Identidade usada | CL (50) | FE (114) | Total (164) |
| --- | --- | --- | --- |
| Pessoa real (parente, conhecido, perfil clonado) | 12 | 26 | 38 |
| Instituição ou funcionário | 11 | 26 | 37 |
| Personagem fictício (vendedor, investidor) | 13 | 45 | 58 |
| Não usa identidade alheia | 14 | 17 | 31 |

133 das 164 denúncias de fraude usam a identidade de outra pessoa. O art. 307 não aparece em nenhuma das 198 capitulações.

---

# A identidade como meio e como instrumento

Como meio, a identidade engana a vítima: a falsa filha no WhatsApp, o falso gerente, o perfil clonado da amiga. É absorvida pelo estelionato: das 38 de pessoa real, 29 vão ao §2º-A e 9 ao 171 sem a qualificadora.

Como instrumento, a identidade de terceiro recebe ou opera: linha habilitada com dados de terceiro (CL 42, FE 7), linha pré-paga em nome de terceiro (CL 22), números cadastrados em nome de terceiros (FE 66), cartões de terceiros apreendidos (CL 15, FE 29), dados de terceiros para compras (FE 6, FE 102). Em nenhum dos 8 casos há imputação de crime de identidade.

As duas imputações autônomas da base terminaram em absolvição nesse ponto:

- INV 4: a sentença deu à falsa identidade da locação a definição do art. 307 (art. 383 do CPP) e absolveu por consunção, como "etapa necessária do crime-fim de estelionato"; condenou pelo art. 297, §1º, o holerite falso, por ter potencialidade que transbordava a locação.
- FE 122: falsa central presencial; absolvição nos arts. 328, parágrafo único, e 304, porque, segundo as vítimas, o réu não usou documento, "tendo apenas se apresentado verbalmente como funcionário"; condenação no §2º-A.

---

# O desafio normativo brasileiro

- Art. 307 do CP: falsa identidade, detenção de três meses a um ano, ou multa, "se o fato não constitui elemento de crime mais grave".
- Art. 308 do CP: usar como próprio documento de identidade alheia, ou ceder a outrem documento dessa natureza, próprio ou de terceiro.
- Art. 171, §2º, VII, do CP (Lei 15.397/2026): ceder, gratuita ou onerosamente, conta bancária para que nela transitem recursos de atividade criminosa.
- Art. 171, §2º-A: a fraude eletrônica qualifica-se pelas "informações fornecidas pela vítima ou por terceiro induzido a erro", sem nomear a identidade usurpada.
- Súmula 17 do STJ: "Quando o falso se exaure no estelionato, sem mais potencialidade lesiva, é por este absorvido."
- Art. 5º, IV ("vedado o anonimato") e LXXIX (proteção de dados pessoais) da Constituição.
- Lei 10.703/2003: cadastro obrigatório dos usuários de telefonia pré-paga.
- Resolução CMN 4.753/2019: verificação e validação da identidade na abertura de conta, com confronto em bases públicas ou privadas.

Em tramitação: PL 675/2025 (Senado), que cria o art. 171-B, falsa identidade digital, aprovado na Comissão de Segurança Pública em 30/06/2026 e aguardando relator na CCJ; PL 4849/2026 (Câmara), sobre falsidade de identidade por conteúdo gerado ou alterado por IA (informação de agregador, não conferida no site da Câmara).

---

# Criminologia e identidade

Qual base teórica recai sobre o fenômeno?

Lusthaus, Industry of Anonymity (Harvard University Press, 2018): o cibercrime lucrativo vive o dilema de equilibrar o anonimato com a necessidade de construir reputação e confiança entre parceiros que não se identificam (capítulo "Nicknames and Identity"). Nos autos brasileiros, o dilema se resolve fora da rede: a confiança do golpe vem da identidade de uma pessoa real usada diante da vítima, e o anonimato do autor vem da identidade de outra pessoa real no registro.

Copes e Vieraitis, Identity Thieves: Motives and Methods (Northeastern University Press, 2012): entrevistas com 59 condenados por furto de identidade, que atuavam sozinhos, em grupos de rua ou em equipes com acesso ocupacional a dados. A base brasileira mostra o mercado do lado do registro: a planilha de CPF vendida por consulta (INV 36), o documento e a selfie cedidos para abrir conta (CL 39).

Becker e Baratta, como na Aula 01: a seleção não é feita pela gravidade do papel, e sim pela exposição registral. Aqui, a pergunta é se o sistema condena a pessoa ou o nome.

---

# Olhando pela prática jurídica

Quais são as perguntas que trabalharemos? Todas respondidas com a base da fase 1, sem coleta nova.

I1. Quanto da fraude usa identidade alheia e por que ela some da capitulação. Linhas 1.1 (taxonomia) e 1.2 (cifra oculta).

I2. O que se cede: a conta, o documento ou os dados. Linhas 2.2 (gargalos logísticos) e 1.4 (avaliação do tipo novo).

I3. O que os autos trazem sobre a abertura da conta quando o titular a nega. Linhas 3.4 (vulnerabilidade da pessoa ou do serviço) e 4.1 (governança privada).

I4. O que essa prova decide. Linha 3.4, com reflexo na 2.3.

---

# I3 e I4: a prova da abertura nas 38 negativas

| O que os autos trazem sobre a abertura | Casos | Condenação | Absolvição |
| --- | --- | --- | --- |
| Selfie ou biometria da abertura | 13 | 12 | 1 |
| Documentos ou ficha de abertura, sem selfie | 5 | 5 | 0 |
| Instituição não colheu ou não achou foto ou documento | 2 | 0 | 2 |
| Só titularidade, extrato ou cadastro | 15 (14 com sentença) | 11 | 3 |
| Nada além do comprovante | 3 | 2 | 1 |

A titularidade sozinha condena quase tanto quanto a abertura documentada (11 de 14 contra 17 de 18). A absolvição aparece quando a instituição diz não ter como mostrar quem abriu a conta (FE 114 e FE 4, ambos de São José dos Campos). A selfie não fecha a questão: no FE 47 ela foi juntada depois, e o MP pediu a absolvição; no CL 19, a comparação de biometria facial foi objeto do único exame pericial da base.

I2: só 4 denúncias ou sentenças narram que o titular cedeu documentos, dados ou selfie, ou abriu a conta a pedido de outro (CL 39, FE 14, CL 23, FE 41); nenhuma imputa o art. 308. Outras 9 narram a vítima entregando os próprios documentos ou dados ao golpista, inclusive a selfie (FE 70).

---

# Momento da decisão

| Momento | Questão | O que conferir | Dado da base |
| --- | --- | --- | --- |
| Cautelares do inquérito | I3 | Requisição do dossiê de abertura: documentos, selfie ou prova de vida, IP, dispositivo e geolocalização da abertura | 13 das 38 negativas têm selfie ou biometria nos autos |
| Recebimento da denúncia | I3 | Se a denúncia que imputa a fraude ao titular que nega a conta traz algo além da titularidade | 15 das 38 negativas só com titularidade; 3 sem nada |
| Autoria | I4 | Se a instituição pôde mostrar quem abriu a conta | 2 de 2 absolvições quando não pôde |
| Tipo | I1 | Se a falsa identidade se exaure no golpe (Súmula 17) ou tem potencialidade autônoma | 0 de 198 capitulações com o art. 307; INV 4 e FE 122 |
| Tipo | I2 | Se há narrativa do ato de cessão (a quem, quando, por quanto) antes do inciso VII; se a cessão foi de documento (art. 308) | 4 narrativas de cessão de documento ou selfie; 0 imputações do 308 |
| Reparação (art. 387, IV, do CPP) | I1 | A pessoa cuja identidade foi usada também é vítima e só entra com pedido | CL 43: o dono do carro ficou sem reparação |

---

# NOSSO FOCO

Três itens de maior valor prático, pelos mesmos critérios da Aula 01: quantos casos alcançam, o efeito na pena, na liberdade ou na reparação, e se dá para conferir nos próprios autos.

| Segmento | Item | Por que vale mais |
| --- | --- | --- |
| Autoria | Exigir o dossiê de abertura quando o titular nega a conta | Alcança as 38 negativas; separa o cedente do usurpado; quando falta, a base absolve em 2 de 2 |
| Tipo | Narrar o ato de cessão antes do inciso VII | O tipo pune ceder "para que" a conta sirva ao crime; a base infere a cessão do registro em quase todos os casos |
| Tipo | Consunção ou concurso da falsa identidade | A identidade usada para enganar é absorvida; o documento com potencialidade própria não é (INV 4) |

---

# /uma reflexão prática: quem é o dono do nome

Na Aula 01, a base mostrou que, na fraude à distância, o sistema seleciona pela exposição registral, e não pela gravidade do papel. Aqui se vê o mecanismo por dentro. O golpe usa duas identidades de pessoas reais: uma para enganar (a amiga do perfil clonado, o dono do carro anunciado) e outra para receber (o titular da conta). O processo só alcança a segunda, porque é a única que está num registro.

Quando o titular nega, a pergunta deixa de ser o que ele fez e passa a ser o que o registro prova. A base responde: a titularidade condena em 11 de 14 casos, embora seja ela o que a negativa contesta, e a falta do procedimento de abertura absolve. O filtro, de novo, não é o olhar do policial; é o que a instituição guardou sobre a abertura.

Para o magistrado, isso vira procedimento. Antes de inferir autoria do registro, perguntar o que a instituição informou sobre a abertura e o que liga o titular ao golpe além da conta: o destino do dinheiro, o número de contas, o contato com a vítima, a remuneração. Se nada disso aparece, o registro prova o nome, e não a pessoa.

---

# ESTUDOS DE CASO

Par TJSP: FE 114 e CL 43. A mesma negativa, contra a mesma instituição de pagamento, foi decidida pelo que a instituição pôde dizer sobre a abertura da conta, e não pelo que o titular fez.

Âncora: FE 114 (São José dos Campos). Contraste: CL 43 (Jacareí). Questões examinadas: I1, I3 e I4 e, no contraste, I2.

---

# FE 114 (âncora)

Identificação. Exercício "O investidor do perfil clonado": https://claude.ai/artifact/1r94F1Qw3Fh51vfNrMPcnG

Peças: denúncia https://github.com/pbms01/FGV_TJPA/tree/main/textos/tjsp/denuncias/1501872-88.2023.8.26.0577 e sentença https://github.com/pbms01/FGV_TJPA/tree/main/textos/tjsp/sentencas/1501872-88.2023.8.26.0577

Citados: FE 4 (a outra absolvição sem selfie, mesma comarca); FE 119 (documentos fotografados por terceiro, condenação com selfie); FE 94 (titular em situação de rua, absolvição); CL 43 (contraste).

Estrato FE. Comarca de São José dos Campos, 2ª Vara Criminal. Fato em 16/01/2023; denúncia em 28/08/2025, recebida em 02/09/2025; sentença em 16/04/2026; trânsito em julgado em 12/05/2026. Peças lidas por inteiro: cota, denúncia e sentença. Segundo leitor: sim, na classificação da abertura.

1. Conduta registrada

A vítima viu no Instagram de uma amiga a indicação de um investidor, conversou com o perfil da amiga e com o investidor e pagou R$ 6.000,00 por Pix a uma chave de e-mail formada com o nome do denunciado, numa conta do PagSeguro em nome dele. O perfil da amiga tinha sido clonado. Três identidades: a da amiga, pessoa real, como meio do engano; o investidor, personagem; o nome do denunciado, como instrumento do recebimento. A denúncia (171, §2º-A, c/c art. 29) diz que "a documentação e o rastro financeiro não deixam qualquer margem de dúvida".

O que a denúncia não narra: a resposta da instituição, já no inquérito (fl. 88), de que não pediu foto nem documento para abrir a conta; qualquer diligência sobre o perfil clonado, o perfil do investidor ou o e-mail da chave Pix; a oitiva do denunciado, nunca ouvido na polícia.

2. Processamento

Do fato à denúncia, 31,4 meses. Cota: ANPP recusado pela pena mínima de quatro anos. Em juízo, o réu disse desconhecer a conta; nos debates, as duas partes pediram a absolvição. Sentença: absolvição pelo art. 386, V, do CPP. A sentença invoca a experiência das aberturas fraudulentas quando o banco se contenta com documento e foto à distância, cita a Apelação Cível 1001614-53.2024.8.26.0011 do TJSP (selfie e documento não bastam, inclusive pelo risco de deepfake; o processo, que também tem o PagSeguro como parte, está em agravo em recurso especial no STJ, e o teor da ementa não foi conferido) e conclui que nem isso houve: o réu pode ter sido "também vítima de golpe".

3. Leitura pelas questões

I1. Onde o caso está: entre as 38 fraudes com identidade de pessoa real e as 6 com perfil clonado. O mecanismo: o processo só alcança a identidade que está no registro. O acréscimo ao magistrado: no recebimento, a denúncia precisa dizer o que liga o titular à clonagem ou ao investidor.

I3 e I4. Onde o caso está: uma das 2 negativas em que a instituição não tinha foto nem documento, ambas absolvidas. O mecanismo: a negativa contesta o vínculo entre o nome e a pessoa, e só o procedimento de abertura responde. A reflexão prática: diante da negativa, requisitar o dossiê de abertura antes de inferir autoria do registro e, se ele não existir, tratar o titular como possível vítima de usurpação.

---

# CL 43 (contraste)

Identificação. Exercício "O Celta anunciado na OLX": https://claude.ai/artifact/UJj9zGfxGnGWMzhprDTHFu

Peças: denúncia https://github.com/pbms01/FGV_TJPA/tree/main/textos/tjsp/denuncias/1501240-78.2022.8.26.0292 e sentença https://github.com/pbms01/FGV_TJPA/tree/main/textos/tjsp/sentencas/1501240-78.2022.8.26.0292

Citados: FE 114 (âncora); CL 39 (cessão de documentos e selfie para abrir conta, condenação no inciso VII); FE 45 (negativa vencida pela selfie e pelo endereço coincidente); INV 4 (falsa identidade absorvida pelo estelionato).

Estrato CL. Comarca de Jacareí, 1ª Vara Criminal. Fato em 07 e 08/02/2022; denúncia de 23/05/2025, recebida em 11/07/2025; sentença em 13/07/2026; trânsito em julgado em 14/09/2026. Peças lidas por inteiro: cota, denúncia e sentença. Segundo leitor: sim, na classificação da abertura.

1. Conduta registrada

Golpe da triangulação: com os dados do dono de um Celta "obtidos nas redes sociais", os golpistas anunciaram o carro na OLX e enganaram compradora e dono. A compradora transferiu R$ 7.900,00: R$ 200,00 para um denunciado e R$ 7.700,00 para a conta da outra denunciada no PagSeguro. A titular negou tudo na polícia (documentos perdidos havia cinco anos, nunca abriu a conta); a denúncia respondeu com os documentos apresentados à polícia e ao banco, "idênticos", e com a resposta do PagSeguro: R$ 4.900,00 seguiram por Pix para uma conta no Nubank "em nome da própria" denunciada.

O que a denúncia não narra: quem usou a linha do anúncio; o ato de cessão (a quem, quando, por quanto), embora atribua aos denunciados "fornecer as suas contas bancárias e dados pessoais"; a selfie da abertura, se existia.

2. Processamento

Do fato à denúncia, 39,5 meses. Cota: ANPP recusado pela pena mínima, bloqueio de R$ 7.900,00 e diligência sobre o beneficiário do boleto. Em juízo, a titular disse que a conta foi dela, mas foi bloqueada e "hackeada"; o outro réu foi revel. O MP pediu a desclassificação para o inciso VII. Sentença: condenação dos dois no art. 171, §2º, VII, como lei mais benéfica (citada como "Lei n. 15.367/2026", erro material), 1 ano de reclusão substituído; para a sentença, não há "prova cabal" de que soubessem concorrer para o estelionato, mas a prova documental é "segura" de que receberam os depósitos, "tendo de fato apenas cedido as contas bancárias". O §4º, imputado, não é examinado. Reparação dividida pelo que entrou em cada conta; o dono do carro ficou sem reparação, por falta de pedido.

3. Leitura pelas questões

I3 e I4. Onde o caso está: entre as 5 negativas com documentos de abertura, todas condenadas. O mecanismo: a prova da abertura derruba a negativa, e o registro passa a provar a pessoa; a sentença não usou o dado mais forte, o Pix para outra conta da própria titular.

I2. Onde o caso está: fora das 4 narrativas de cessão de documento ou selfie. O mecanismo: da titularidade provada a sentença passou à cessão, sem narrativa de entrega, destinatário ou preço. A reflexão prática: o inciso VII pune ceder "para que nela transitem recursos" de crime; fica para discussão se a ausência de prova da ciência é compatível com esse elemento.

I1. O dono do carro teve a identidade usada para dar credibilidade ao anúncio e foi tratado como testemunha, sem reparação.

O acréscimo ao magistrado: separar titularidade e cessão no tipo, examinar a causa de aumento imputada e limitar a reparação ao que entrou em cada conta, o que só 8 de 31 sentenças FE da base fizeram.
