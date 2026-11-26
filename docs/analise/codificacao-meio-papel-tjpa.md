# Codificação de contexto, meio, papel e indicadores nas denúncias do TJPA (leitura assistida)

Nota de 25/11/2026. Completa, no TJPA, a codificação de base que no TJSP sustenta as questões 1 a 7: o artifício já estava codificado e conferido por segundo leitor (`docs/analise/codificacao-artificio-tjpa.md`), e faltavam o contexto, o meio de contato, o papel do denunciado e os nove indicadores. Feita depois de regerada a extração da fase 2 sobre a segunda passada (seção final do `dados/extracao/LEIAME.md`). Base: as 183 denúncias sem duplicata de `dados/extracao/denuncias_tjpa.csv` (INV 11, CL 12, FE 160), censo do que o DJEN publicou, com contagens simples.

## No repositório

Produzido em 25/11/2026 numa sessão com o repositório só para leitura e gravado no main em 26/11/2026, com autorização do pesquisador, pelo patch daquela sessão aplicado sobre o main do dia (conflito só no título do HANDOFF). A extração regerada do patch confere com uma regeração independente feita em 26/11 (a única diferença é o PA-FE 47 marcado como conferido, pela inclusão em `CONFERIDAS`), e o lote do TJSP sai igual ao da versão anterior dos scripts.

- `dados/extracao/codificacao_assistida_tjpa.csv`: uma linha por denúncia, com as mesmas colunas de `codificacao_assistida.csv` (TJSP): `numero`, `estrato`, `ordem`, `contexto`, `meio_contato`, `artificio`, `papel_denunciado`, os nove indicadores e `nota`. O artifício é cópia de `codificacao_artificio_tjpa.csv`.
- `scripts/lote_codificacao.py` e `scripts/grava_codificacao.py`, agora com `TRIB=tjpa`: o primeiro imprime o lote compacto a partir de `segmentos_tjpa/`, sem as duplicatas e com o artifício como pista; o segundo grava no arquivo do TJPA, aceita `=` no lugar do artifício e aborta se o artifício escrito diferir do codificado. Sem `TRIB`, os dois rodam o TJSP como antes (a saída do lote foi comparada byte a byte com a da versão anterior).
- `scripts/codificacao_tjpa.py`: confere a cobertura, o artifício, o vocabulário e a coerência entre os campos, com nove exceções justificadas, e imprime as tabelas desta nota.

## Método

Livro de códigos de `dados/conferencia/livro_codigos_denuncias.md`, sem categoria nova, e as regras escritas no LEIAME da fase 1, inclusive a da adjudicação do papel: a execução atribuída ao denunciado junto com pessoa não identificada mantém o titular de conta, e só a atribuição individual do ardil faz misto. Antes de começar, as linhas do TJSP para os artifícios de invasão, de celular roubado, de acesso interno, de boleto e de compra fraudulenta foram relidas, para alinhar convenções que o livro não escreve: aparelho em mãos é meio presencial e conta acessada de longe é sistema; a tomada de conta por código entregue conta como invasão, e a falsa central em que a vítima digita a senha, não; a tela ou o boleto falso não acendem o indicador de falsa central; o comprovante falso não é Pix nem conta de denunciado.

A leitura foi a do lote compacto (início da narrativa, frases que tocam o papel, o pagamento e o canal, fim e capitulação, cerca de 1.700 caracteres por denúncia), completada por buscas dirigidas na narrativa em cerca de 60 denúncias em que o lote não decidia o papel, o meio ou o Pix. Não houve leitura integral nem segundo leitor. Decisões próprias do TJPA, que o livro não cobria:

- As sete denúncias da Operação Trojan imputam lavagem ou furto a beneficiários das transferências: titular de conta, meio sistema, invasão 1.
- Denúncia que atribui o ardil, em conjunto, a vários denunciados cuja ligação descrita com o fato são as contas (PA-FE 106, 145, 184, 213) ficou como titular de conta; a que diz que o interlocutor era o denunciado, ou que liga a ele a linha ou o perfil usado, ficou como misto.
- Quem recebe em espécie, em mãos, sem conta narrada, é executor (PA-FE 160, PA-FE 201, PA-FE 203, PA-CL 39).
- O indicador de Pix seguiu a narrativa lida; onde ela só dizia transferência, valeu a menção a Pix na denúncia a partir de novembro de 2020.
- O acesso com credenciais confiadas pelo idoso e usadas sem autorização (PA-FE 71, PA-FE 102, PA-FE 197) conta como invasão, porque a conduta é a operação na conta, sem engano.

## Resultado

| Campo | INV (11) | CL (12) | FE (160) |
| --- | --- | --- | --- |
| Contexto | patrimonial 4; violência doméstica 5; relacional 2 | patrimonial 11; institucional 1 | patrimonial 155 (96,9%); institucional 4; outro 1 |
| Meio de contato | sistema 7; presencial 3; WhatsApp 1 | WhatsApp 4; sistema 3; presencial 3; rede social 1; telefone 1 | WhatsApp 68 (42,5%); telefone 25 (15,6%); sistema 23 (14,4%); presencial 21 (13,1%); site 14 (8,8%); rede social 5; outro 3; e-mail 1 |
| Papel do denunciado | invasor 8; titular 2; executor 1 | misto 6; titular 4; executor 2 | titular 58 (36,2%); misto 58 (36,2%); executor 44 (27,5%) |
| Valor em conta de denunciado | 2 (18,2%) | 10 (83,3%) | 115 (71,9%) |
| WhatsApp usado | 6 | 4 | 81 (50,6%) |
| Pix | 0 | 7 | 69 (43,1%) |
| Invasão | 11 | 3 | 26 (16,2%) |

Na fase 1 (TJSP, percentuais ponderados), o papel era, na FE, titular 52,7%, misto 26,1% e executor 21,2%, com o valor em conta de denunciado em 78,8%; no CL, titular 87,9%; no INV, invasor 52,9%.

Papel por artifício na FE: venda falsa 47 (titular 16, misto 24, executor 7); compra fraudulenta 22 (executor 20, misto 2); falso parente 21 (titular 14, misto 7); falsa central 17 (titular 9, misto 5, executor 3); invasão de conta ou sistema bancário 16 (titular 7, misto 6, executor 3).

## Leitura, com as ressalvas

1. O titular sozinho pesa menos na FE do TJPA (36,2%) do que na do TJSP (52,7%), e o misto, mais (36,2% contra 26,1%). Parte da diferença é de redação: o MPPA escreve com frequência que a denunciada "se passava" pelo parente ou que o anunciante "era, na realidade," a denunciada, quando a prova que cita é a conta. Em 26 dos 58 mistos da FE a extração conta um só denunciado (em outros 14 ela não conta os denunciados), e os oito mistos do falso parente (sete na FE e o PA-CL 123) são dessa forma. A regra do livro manda codificar a atribuição, e não a prova; para a questão 1, que mede o que o processo alcançou, a tabela de nível terá de olhar a prova, como no CL 40 do TJSP.
2. O executor sem conta própria se concentra na compra fraudulenta contra empresa (20 de 44), como no TJSP, seguida da venda falsa paga em mãos e do celular roubado.
3. O engano face a face capitulado no §2º-A, que no TJSP apareceu em cinco denúncias, aparece aqui em 14 das 24 fraudes de CL e FE com meio presencial (PA-FE 13, 36, 48, 54, 69, 84, 113, 124, 138, 146, 160, 164, 177 e 200). No PA-FE 47, denunciado no caput, a sentença aplicou de ofício a emendatio para o §2º-A porque a máquina de cartão "possui ligação direta com a internet". É material direto da questão 2.
4. O sistema como meio (23 na FE) reúne a Operação Trojan, os equipamentos de captura de cartão em caixa eletrônico, as contas operadas por quem tinha acesso e os celulares roubados; a capitulação vai do 155, §4º-B (8), ao 155 sem o §4º-B (5), ao §2º-A (5) e à lavagem (4), o que repete a fronteira instável entre furto e estelionato vista no TJSP.

## Limites e pendências

- Leitura de um só leitor, sobre trecho compacto. O papel e o meio são os campos em que o segundo leitor do TJSP mais divergiu nas invasões de conta e nos casos de atribuição conjunta; aqui a fronteira entre titular e misto é o ponto mais frágil.
- Segundo leitor cego, no desenho do artifício (amostra sorteada por estrato e casos de fronteira), e conferência do pesquisador.
- Três segmentos de narrativa da extração estão errados ou sujos e foram lidos no texto integral ou pelas buscas: PA-CL 123 (pegou o pedido de prisão preventiva), PA-FE 73 (pegou a manifestação sobre o sequestro de bens) e PA-FE 10 (começa na papeleta digitalizada). A correção cabe a `scripts/extrai_denuncias.py`.
- PA-FE 218 (cartão corporativo movimentado por terceiros) está em compra fraudulenta na codificação do artifício; pela leitura do meio e da invasão, fica mais perto da invasão de conta. Não foi mudado.
- O passo seguinte é parametrizar por tribunal os scripts das questões 1, 2, 6 e 7, que hoje leem só os arquivos do TJSP, e ler as tabelas de nível e de objeto no TJPA.
