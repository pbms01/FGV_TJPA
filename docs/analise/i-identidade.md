# Identidade digital e anonimato na base da fase 1: questões I1 a I4

Nota analítica de 22/11/2026, sobre a base da fase 1 (TJSP: 198 denúncias, 164 delas de fraude, 50 no estrato CL e 114 no FE, e 34 do estrato INV). Tabelas reproduzíveis por `python3 -I scripts/analise_i_identidade.py`; leitura do segundo leitor em `dados/conferencia/segundo_leitor_identidade.csv` (amostra em `segundo_leitor_identidade_lista.csv`); fichas em `docs/aula/fichas/FE_114.md` e `CL_43.md`; exercícios em `docs/aula/exercicios/identidade-*.html`; texto do Gamma em `docs/aula/slides/identidade.md`, que grava `dados/analise/i_identidade.csv` (uma linha por denúncia) e `dados/analise/i_resumo.json`; `python3 -I scripts/analise_i_identidade.py trechos` imprime os trechos achados pelas regras, para conferência. Questões e fontes normativas em `claude/identidade-anonimato-questoes.md`; arquitetura da aula em `claude/arquitetura-aula-identidade-anonimato.md`. Contagens simples por estrato, como nas questões 1 a 7.

## Resposta em uma frase por questão

I1. Quatro em cada cinco denúncias de fraude da base usam a identidade de outra pessoa diante da vítima (133 de 164), e nenhuma imputa o art. 307 do CP; as duas denúncias da base que imputaram crime de identidade ao lado do patrimonial (INV 4 e FE 122) terminaram em absolvição nesse ponto, uma por consunção e outra porque a falsa identidade foi só verbal.

I2. A cessão de identidade que os autos narram não é a do documento, e sim a da conta: só 4 denúncias ou sentenças narram que o titular cedeu documentos, dados pessoais ou selfie, ou abriu a conta a pedido de outro, e nenhuma imputa o art. 308; outras 9 narram a vítima entregando os próprios dados e documentos ao golpista, inclusive selfie (FE 70).

I3. Nas 38 denúncias de só conta em que o titular nega ou não reconhece a conta, os autos trazem a selfie ou a biometria da abertura em 13, documentos ou ficha de abertura sem selfie em 5, a informação da instituição de que não colheu ou não achou foto ou documento em 2 e só a titularidade, o extrato ou o cadastro em 15 (nada sobre a conta, além do comprovante, em 3).

I4. A prova da abertura quase não muda o desfecho, salvo quando falta: a negativa termina em condenação em 17 de 18 casos com abertura documentada e em 11 de 14 com só a titularidade, e em absolvição nos 2 casos em que a instituição não tinha foto nem documento (FE 114 e FE 4, ambos de São José dos Campos).

## I1. A identidade como meio e a capitulação

Classificação pela codificação validada do artifício (questão 1 da fase 1), completada por leitura dos perfis clonados de pessoa real e corrigida em 2 casos pelo segundo leitor (CL 57, vendedora de agência de veículos real, com CNPJ; FE 86, anúncio no próprio perfil): pessoa real é o falso parente, o falso conhecido, o falso advogado, o sequestro de conta e o perfil clonado de pessoa real (FE 76, FE 98, CL 14, FE 101, FE 114, FE 89); instituição é a falsa central, a falsa taxa de plataforma e o boleto falso; fictícia é a venda falsa, o investimento falso, a taxa antecipada e o falso relacionamento.

| Identidade usada diante da vítima | CL (50) | FE (114) | Total (164) |
| --- | --- | --- | --- |
| Pessoa real | 12 | 26 | 38 |
| Instituição ou funcionário | 11 | 26 | 37 |
| Personagem fictício | 13 | 45 | 58 |
| Não usa identidade alheia | 14 | 17 | 31 |

A capitulação absorve a identidade: das 38 de pessoa real, 29 vão ao §2º-A e 9 ao 171 sem a qualificadora; das 37 institucionais, 30 ao §2º-A; das 58 fictícias, 48 ao §2º-A. O art. 307 não aparece em nenhuma das 198 capitulações da base.

A identidade de terceiro também aparece como instrumento, e não como engano: 8 denúncias de fraude narram linha, cartão ou cadastro em nome de outra pessoa (CL 42 e FE 7, linha habilitada com dados de terceiro; CL 22, linha pré-paga habilitada em nome de terceiro; FE 66, dois números cadastrados em nome de terceiros; CL 15 e FE 29, cartões de terceiros apreendidos; FE 6 e FE 102, dados de terceiros para compras). Em nenhuma há imputação de crime de identidade.

Os dois casos em que a identidade foi imputada à parte mostram o mecanismo. No INV 4, a denúncia capitulou como uso de documento falso a falsa identidade usada para alugar um imóvel; a sentença deu ao fato a definição do art. 307 (art. 383 do CPP) e absolveu por consunção, porque a falsa identidade foi "etapa necessária do crime-fim de estelionato", mas condenou pelo art. 297, §1º, o holerite falso, por ter potencialidade lesiva que transbordava a locação. É a regra da Súmula 17 do STJ: "Quando o falso se exaure no estelionato, sem mais potencialidade lesiva, é por este absorvido". No FE 122, falsa central presencial, a denúncia imputou também o art. 328, parágrafo único, e o art. 304 c/c 297; a sentença absolveu nos dois porque, segundo as vítimas, o réu "não se utilizou de qualquer documento durante a abordagem, tendo apenas se apresentado verbalmente como funcionário", e condenou no §2º-A.

## I2. O que se cede: a conta, o documento ou os dados

| Narrativa de cessão de identidade (leitura à mão) | Casos |
| --- | --- |
| Titular cedeu documentos, dados pessoais ou selfie, ou abriu a conta a pedido | CL 39, FE 14, CL 23, FE 41 |
| Vítima entregou documentos, dados pessoais ou selfie ao golpista | FE 70, FE 24, CL 45, FE 90, FE 127, CL 21, CL 36, FE 126, CL 48 |
| Mercado de dados de terceiros narrado | INV 36 (planilhas de CPF vendidas por consulta), INV 4 |

O caso mais nítido é o CL 39: o acusado "forneceu seus documentos pessoais e fotografia de face para abertura de conta corrente digital no Banco Bradesco, cedendo o acesso"; foi condenado no inciso VII. A cessão do documento de identidade, que o art. 308 pune desde 1940, não foi imputada em nenhum caso; a do documento acompanhado da selfie, que é o que abre uma conta digital, cai na cessão da conta. A regra também achou 8 casos em que "dados bancários" emprestados são a própria conta (FE 53, FE 73, FE 99, CL 52, FE 21, FE 77, INV 35, INV 5), que ficam na questão 7.

## I3 e I4. A prova da abertura nas 38 negativas

| O que os autos trazem sobre a abertura | Casos | Com sentença | Condenação | Absolvição |
| --- | --- | --- | --- | --- |
| Selfie ou biometria da abertura | 13 | 13 | 12 | 1 (FE 47) |
| Documentos ou ficha de abertura, sem selfie | 5 | 5 | 5 | 0 |
| Instituição não colheu ou não achou foto ou documento | 2 | 2 | 0 | 2 (FE 114, FE 4) |
| Só titularidade, extrato ou cadastro | 15 | 14 | 11 | 3 (FE 26, FE 94, CL 4) |
| Nada sobre a conta, além do comprovante | 3 | 3 | 2 | 1 (FE 41) |

A condenação inclui a procedência parcial. As 7 absolvições somam as da questão 7 (7 de 37 sentenças).

Três achados. Primeiro, a titularidade sozinha condena quase tanto quanto a abertura documentada (11 de 14 contra 17 de 18): o processo trata o registro como prova da pessoa. Segundo, a absolvição aparece quando a instituição diz não ter como mostrar quem abriu a conta: no FE 114, o PagSeguro "informou ao juízo não ter solicitado nenhuma fotografia ou documento para abertura da conta" (fl. 88); no FE 4, o Bradesco "não localizou fotografia do tipo selfie" e informou conta com assinatura digital. Terceiro, a selfie não fecha a questão: no FE 47 ela foi juntada depois, e o próprio MP pediu a absolvição; no CL 19 a comparação de biometria facial foi objeto de exame pericial, o único da base.

Nas outras 63 denúncias de só conta, a triagem por termos (não conferida à mão) acha selfie ou biometria em 14, documentos de abertura em 7, só dado cadastral ou extrato em 40 e nada em 2.

## O que isso dá a quem acusa, a quem julga e a quem previne

Para quem acusa, a negativa do titular pede, antes da denúncia, o dossiê de abertura da conta (documentos, selfie, prova de vida, IP e geolocalização da abertura), e não só o extrato: em 15 das 38 negativas os autos só traziam a titularidade, e em outras 3 nem isso. A Resolução CMN 4.753/2019 obriga a instituição a "verificar e validar a identidade e a qualificação dos titulares da conta" (art. 2º), e é esse procedimento que se requisita. Quando a falsa identidade tem potencialidade que transborda o golpe (documento guardado, cadastro reutilizável), a imputação autônoma tem base na própria Súmula 17; quando é verbal ou se exaure no golpe, não tem.

Para quem julga, a pergunta que separa o cedente do usurpado é o que a instituição pôde mostrar sobre a abertura. A base mostra que a resposta "nada" absolve e que a resposta "titularidade" condena em 11 de 14, embora, logicamente, a titularidade seja o que a negativa contesta.

Para quem previne, a identidade que o sistema penal alcança é a do registro, e a que o golpe usa é a de outra pessoa (o parente, o funcionário, o anunciante). O dever de identificar na abertura é o único ponto em que as duas se encontram.

## Limites

A classificação da identidade usada (I1) herda a codificação do artifício e lê à mão só os perfis clonados; a regra para identidade de terceiro como instrumento foi lida à mão, mas pode perder casos que usam outra redação. I2 é triagem por termos com leitura à mão dos achados: é piso. I3 foi lida à mão nas 38 negativas e conferida por segundo leitor cego (seção seguinte); nas demais 63 é só triagem. A selfie e a biometria registradas são as que denúncia e sentença mencionam, não as que estão nos autos sem menção.

## Segundo leitor

Um segundo leitor cego (agente separado, sem acesso à codificação) releu as 38 negativas e uma amostra sorteada de 24 denúncias de fraude (semente 20261122), só pelos textos das peças. Concordância: 31 de 38 na abertura (81,6%) e 22 de 24 na identidade usada (91,7%). Na adjudicação, a leitura do segundo leitor foi acolhida em 6 casos de abertura (FE 75 e FE 96, selfie ou foto do cadastro que a primeira leitura não achou; FE 36, fichas cadastrais da abertura; CL 50 e FE 41, só o comprovante; FE 26, resposta do banco sobre o encerramento da conta) e nos 2 de identidade (CL 57 e FE 86). Foi mantida a primeira leitura no FE 124: a abertura "sem a imagem pessoal da acusada" é a leitura que a defesa fez do ofício, e a sentença lê no mesmo ofício a abertura com documento pessoal, enquanto uma testemunha menciona resposta posterior com foto. As tabelas acima já trazem os números adjudicados. Nenhuma denúncia da amostra imputa os arts. 307, 308 ou 299; o FE 86 menciona o 299 para dizê-lo absorvido pela Súmula 17.

## Fontes conferidas nesta sessão

- Código Penal, arts. 307, 308 e 171, §2º, VII, e §2º-A: https://www.planalto.gov.br/ccivil_03/decreto-lei/del2848compilado.htm
- Código de Processo Penal, art. 383: conferido pela própria sentença do INV 4; não transcrito do Planalto nesta sessão
- Súmula 17 do STJ: https://scon.stj.jus.br/SCON/sumstj/toc.jsp?livre=%40num%3D17
- Resolução CMN 4.753/2019, arts. 1º, 2º e 4º, I: https://normativos.bcb.gov.br/lists/normativos/attachments/50847/res_4753_v3_l.pdf (alterada pelas Resoluções CMN 5.218/2025 e 5.261/2025, segundo fonte secundária; texto alterado não conferido)
