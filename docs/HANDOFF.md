# Handoff: fase 1 TJSP coletada; análise criminológica com as questões 1 a 7 feitas, e as três primeiras conferidas por segundo leitor (21/11/2026)

Repositório pbms01/FGV_TJPA. O branch `coleta-datajud` foi mesclado no main em 21/11/2026, depois da questão 3, junto com a base de 130 casos que estava só no main. Este arquivo substitui o estado da conversa e deve ser lido antes de qualquer passo novo.

## Para a próxima sessão: análise sob a perspectiva da criminologia informática

A coleta da fase 1 está encerrada para fins de análise. As pendências de coleta seguem na seção de próximos passos e não bloqueiam a análise: conferência humana da codificação assistida e das decisões do segundo leitor, FE 16, inteiro teor de 18 acórdãos e o CL 34, pautado para 03/12/2026. A referência teórica é o doc `claude/criminologia-informatica-linhas-de-pesquisa.md` do Project, versão 0.4 (21/11/2026), espelhado em `docs/linhas-de-pesquisa.md` e no doc editável do Claude Docs; a versão 0.4 acrescentou a distância como agrupamento dos canais, a regra proposta da mediação acessória (ainda não aplicada à base) e os limites da fonte judicial para escala e dano. O núcleo é: quatro elementos (delito, infrator, vítima, controle social), a mediação técnica relevante como critério distintivo, o teste de eliminação de Wall reformulado em dois eixos como critério comum (retira-se o sistema informático, em rede ou isolado, e observa-se se a conduta desaparece, perde escala ou continua por outros meios; depois, identifica-se o canal pelo qual o agente chegou ao sistema) e a exigência de produto utilizável por quem investiga, acusa, julga ou previne. A internet é um canal entre outros.

Análise feita nesta fase, com os dois eixos codificados em `scripts/eixos_mediacao.py` (sistema: objeto ou meio; canal: internet, telefonia, rede interna, contato físico, presencial, correio, sem contato; distância como agrupamento dos canais):

- Questão 1, linhas 2.2 e 1.4: quem o sistema penal alcança na fraude eletrônica e o que a Lei 15.397/2026 muda. Nota em `docs/analise/q1-alcance-elo-fisico.md` (Project: `claude/analise-q1-alcance-elo-fisico.md`), script `scripts/analise_q1_alcance.py`, saídas em `dados/analise/q1_*`. Achado central: o sistema alcança o elo físico e registral (conta, linha, recolha do cartão), e no contato remoto do CL fica só no titular em 39 de 40 denúncias (a exceção, CL 40, atribui o ardil ao titular pela própria conta); o regime de atribuição segue a distância, e o golpe por telefone se comporta como o golpe pela internet; a lei reprecificou o titular da conta sem ampliar o alcance.
- Questão 2, linha 1.1: o que a eliminação do sistema separa e se a capitulação acompanha. Nota em `docs/analise/q2-teste-eliminacao.md` (Project: `claude/analise-q2-teste-eliminacao.md`), script `scripts/analise_q2_eliminacao.py`, saídas em `dados/analise/q2_*`. Achado central: o crime informático não depende da internet (13 das 33 invasões do INV persistem sem ela, por contato físico ou rede interna); a fraude é crime informático impróprio à distância; o §2º-A qualifica pelo canal à distância e é aplicado a cinco enganos face a face; o 154-A sai da denúncia quando o invasor não é alcançado e cai na sentença quando é meio de outro crime.
- Questão 3, linha 3.3 (com reflexo na 3.4, na 2.2 e na 4.1): que dano a sentença reconhece além do financeiro e como a reparação mínima do art. 387, IV, do CPP se distribui. Nota em `docs/analise/q3-tipologia-dano.md` (Project: `claude/analise-q3-tipologia-dano.md`), leitor em `scripts/reparacao_387.py` (validação: `python3 scripts/reparacao_387.py valida`), análise em `scripts/analise_q3_dano.py`, saídas em `dados/analise/q3_*`, método na última seção do `dados/extracao/LEIAME.md`. Achado central: das 171 condenações (sem as quatro denúncias fora da tipologia), 79 fixam a reparação, 34 a negam e 58 silenciam; o dano moral foi fixado em três; o dano não econômico entra pela dosimetria (9 das pelo menos 26 sentenças que valoraram as consequências contra o réu, com o dano reputacional em duas) e serve à pena, porque em 12 dessas 26 a vítima ficou sem reparação. A reparação segue o pedido do MP, que segue o extrato, e por isso recai sobre o titular da conta (65,1% das condenações de titulares na FE, contra 35,7% do autor remoto), quase sempre pelo valor inteiro do golpe (19 de 31 na FE, 14 de 22 no CL); só oito sentenças a limitam ao que entrou na conta. Quando o banco ressarciu, a reparação é negada e o dano sai do processo (6 das 10 negativas no CL).
- Questão 4, linha 2.1: o que a acusação trata como organização e o que a denúncia narra da estrutura. Nota em `docs/analise/q4-organizacao.md` (Project: `claude/analise-q4-organizacao.md`), leitor em `scripts/organizacao.py` (validação do número de denunciados: `python3 scripts/organizacao.py valida`), análise em `scripts/analise_q4_organizacao.py`, saídas em `dados/analise/q4_*`, método na seção própria do `dados/extracao/LEIAME.md`. Achado central: a fraude é processada como obra de poucos (um único denunciado em 73,1% das FE e 52,6% das CL; quatro ou mais em 9 de 194 denúncias), e o que a denúncia narra é a camada das mulas e dos elos locais da rede; coordenação aparece em 14 das 65 denúncias plurais e hierarquia em uma, o que corresponde à cooperação frouxa de Leukfeldt, Lavorgna e Kleemans (2017) vista só pelo componente do dinheiro. Associação criminosa em 10 denúncias e organização criminosa em 3 (todas INV); 4 imputações recaem sobre um único denunciado associado a não identificados, dois grupos que preenchem o critério do art. 1º, §1º, da Lei 12.850 foram denunciados só por 288, e a sentença acolheu o 288 em 6 de 10 sem acompanhar de modo visível a estrutura narrada. O núcleo aparece quando o sistema é o objeto (5 dos 9 grupos coordenados) e, com frequência, é família, casal ou equipe de trabalho.
- Questão 5, linha 4.4: quanto tempo separa o fato da denúncia, de que custodiante vem o dado que a denúncia narra e o que a cota ainda pede, contra os prazos de guarda. Nota em `docs/analise/q5-tempo-dado.md` (Project: `claude/analise-q5-tempo-dado.md`), leitor em `scripts/tempo_dado.py` (validação: `python3 scripts/tempo_dado.py valida`), análise em `scripts/analise_q5_tempo_dado.py`, saídas em `dados/analise/q5_*`. Achado central: mediana de 21,6 meses do fato à denúncia na FE e 28,2 no CL, 27,0 no canal internet, onde 97 de 106 denúncias chegam depois dos 6 meses de guarda dos registros de aplicação (art. 15 do Marco Civil) e 88 depois do ano dos registros de conexão (art. 13); nenhuma das 106 narra dado de plataforma ou de provedor de conexão (só 4 do sistema-objeto, todas INV), o terceiro custodiante da fraude é a operadora (cadastro da linha, 11 denúncias, que aponta terceiro não denunciado em 4), e o titular da conta é nomeado sem dado obtido do banco em 59 de 101. A cota pede dado em 14 denúncias, ao banco e ao aparelho apreendido, e preservação em nenhuma. Produto: protocolo de preservação por canal, a executar no registro da ocorrência.
- Questão 6, linhas 3.4 e 4.1: a fraude explora a pessoa ou o serviço, e onde estava o banco. Nota em `docs/analise/q6-servico-vulnerabilidade.md` (Project: `claude/analise-q6-servico-vulnerabilidade.md`), leitor em `scripts/servico_banco.py`, análise em `scripts/analise_q6_servico.py`, saídas em `dados/analise/q6_*`. Achado central: das 171 denúncias em que o dinheiro passou pelo serviço financeiro, a vítima idosa é 26,3% das pessoas físicas e se concentra onde a fraude imita alguém de confiança (45,7% no falso parente e afins, 33,3% na falsa instituição, 8,9% na venda falsa), sem perder mais (mediana de R$ 4.706 contra R$ 5.257); o aumento pela idade é capitulado em 39 de 42. A credencial sai da vítima em 14 das 43 fraudes que imitam instituição, 8 contratam crédito em nome da vítima, 22 narram repasse imediato no destino; as 12 sentenças com ressarcimento pelo intermediário estão todas nas famílias que passam pela segurança do serviço e nenhuma nas 91 de venda falsa e falso parente, o que acompanha a Súmula 479 pelo lado de quem envia e deixa sem cobrança o banco de destino.
- Questão 7, linha 2.3 reduzida à entrada do titular: o que o titular de só conta diz de como a conta saiu das mãos dele e o que isso decide. Nota em `docs/analise/q7-titular-conta.md` (Project: `claude/analise-q7-titular-conta.md`), leitor em `scripts/titular_conta.py` (`python3 scripts/titular_conta.py valida` imprime as 101 leituras), análise em `scripts/analise_q7_titular.py`, saídas em `dados/analise/q7_*`. Achado central: 47 de 101 admitem a cessão (28 empréstimo, 18 venda ou aluguel, 1 anúncio de empréstimo), por preço mediano declarado de R$ 200 (de R$ 50 a R$ 2.000), a desconhecidos, conhecidos e amigos; 38 negam ou não reconhecem a conta e 12 estão ausentes. Quem admite é condenado em 45 de 47, 27 vezes no §2º-A e 6 no inciso VII, sem que o conteúdo da versão separe um do outro; o titular condenado é primário em 41 e tem antecedentes em 13, e há réu menor de 21 anos em 12 processos. A cota trata do ANPP em 68 e invoca a pena mínima em 46.
- Conferência por segundo leitor das três questões. Nota de método em `docs/analise/segundo-leitor.md` (Project: `claude/segundo-leitor-conferencia.md`), script `scripts/segundo_leitor.py`, arquivos em `dados/conferencia/` (seção final do `dados/extracao/LEIAME.md`). Um segundo leitor cego (outra instância do mesmo modelo) codificou 34 denúncias e 50 sentenças pelos livros de códigos; concordância de 85% a 100% nos campos de escolha única e de 50 em 50 na reparação, com o ponto fraco na atribuição dos danos aos temas de Agrafiotis (8 em 16). As 57 divergências foram adjudicadas em `adjudicacao.csv` (36 para o segundo leitor, 21 para o primeiro), aplicadas aos dados e conferidas pelo script; a primeira leitura ficou congelada em `primeira_leitura.csv`.
- Pendências das três questões: conferência humana das 57 decisões de adjudicação; conferir os dicionários `NIVEL` (questão 1), `OBJETO` e `CANAL_MANUAL` (eixos), `CORRECAO`, `CONSEQ_MANUAL`, `LIMITADA_CONTA` e `INTERMEDIARIO_RESSARCIU` (questão 3), que o segundo leitor só cobriu em parte; reler as consequências nas condenações que o leitor por termos não marcou (o FE 21 mostrou que ele perde valoração sem a palavra); separar no sistema-meio a mediação relevante da acessória; ler nos acórdãos já coletados o que o segundo grau faz com a reparação; acompanhar o Tema 1.389 do STJ (exigências do art. 387, IV), com vista pedida em 13/05/2026 e ainda pendente na última fonte localizada (01/09/2026).
- Pendências das questões 5 a 7, que não tiveram segundo leitor: os dicionários `TERCEIRO`, `PEDIDO_COTA` e `DATA_MANUAL` (questão 5), `CREDITO`, `REACAO`, `AUMENTO_MANUAL` e `PJ` (questão 6) e `VERSAO_MANUAL` com as 101 leituras de versão (questão 7); os pontos do serviço da questão 6 são triagem por termos.
- Para reproduzir: `python3 scripts/analise_q1_alcance.py`, `python3 scripts/analise_q2_eliminacao.py`, `python3 scripts/analise_q3_dano.py`, `python3 scripts/analise_q4_organizacao.py`, `python3 scripts/segundo_leitor.py` (que depende do `q3_dano.csv` e diz se a adjudicação está aplicada), `python3 scripts/analise_q5_tempo_dado.py`, `python3 scripts/analise_q6_servico.py` (depende do `q3_dano.csv` e do `q5_tempo_dado.csv`) e `python3 scripts/analise_q7_titular.py` (depende do `q1_alcance.csv`, do `q4_organizacao.csv` e do `q5_tempo_dado.csv`), nessa ordem, da raiz do repo; `-q` grava sem imprimir.

Ponto de partida da próxima sessão: a conferência humana das 57 decisões de adjudicação do segundo leitor (`dados/conferencia/adjudicacao.csv`, coluna `motivo`), que o usuário pediu para depois das questões 5 a 7; o roteiro está no primeiro dos próximos passos. Das perguntas pendentes das linhas de pesquisa, foram priorizadas pelo propósito prático e feitas a 4.4, a 3.4 com a 4.1 e a 2.3 reduzida à entrada do titular; ficaram de lado a 3.2, a 1.2, a 1.3, a 4.2, a 3.1, a 2.4 e a 4.3.

Base analítica, unida pela coluna `numero`, com o peso de `dados/cjpg/amostra_tjsp.csv` e sem as duplicatas marcadas em `duplicata_de` (198 denúncias):

| Arquivo | Unidade | O que traz | Estado |
| --- | --- | --- | --- |
| `dados/extracao/denuncias_tjsp.csv` | denúncia (200) | estrato, capitulação, indicadores de meio, conta, Pix, boleto, ano do fato | extração por regras validada por leitura; `ano_fato` com ruído |
| `dados/extracao/codificacao_manual_r1.csv`, `_r2.csv` e `codificacao_assistida.csv` | denúncia | artifício, meio de contato, papel do denunciado, valor em conta de denunciado, contexto de violência doméstica | 36 manuais; 164 assistidas sem conferência do pesquisador, 34 delas com segundo leitor e adjudicação |
| `dados/extracao/sentencas_amostra.csv` | processo (199) | resultado, capitulação acolhida, pena, regime, substituição, Lei 15.397/2026, notas | 29 lidas à mão, 57 corrigidas, 113 só pelo leitor por regras (24 delas com segundo leitor) |
| `dados/extracao/matriz_casos.csv` e `sentencas_matriz.csv` | caso (29) | matriz de seleção para exame qualitativo | lida à mão |
| `dados/tjsp2/apelacoes_amostra.csv` | processo (23) | andamento em segundo grau das sentenças que trataram do inciso VII | DJEN até 21/11/2026 |
| `dados/tjsp2/acordaos_inciso_vii.csv` | acórdão (125) | decisão e fundamento sobre o 171 §2º, VII | leitura da ementa |
| `dados/analise/q3_dano.csv` | denúncia (198) | reparação do art. 387, IV (status, valores, fundamento, pedido, individualização, ressarcimento por intermediário) e consequências do crime com a tipologia do dano | leitor por regras calibrado na matriz e revisto cláusula a cláusula; 50 sentenças com segundo leitor e adjudicação |
| `dados/analise/q4_organizacao.csv` | denúncia (198) | número de denunciados, enquadramento do concurso, estrutura narrada (divisão de papéis, coordenação, vínculo, reiteração), desfecho do 288 e da Lei 12.850, pedido e remuneração da conta | número de denunciados validado na matriz (26 de 29 pela regra); estrutura lida pelo assistente, sem segundo leitor |
| `dados/analise/q5_tempo_dado.csv` | denúncia (198) | data do fato e da denúncia, intervalo e faixas contra os prazos de guarda, fontes narradas por custodiante, dado de operadora, plataforma ou conexão e pedidos da cota | data do fato conferida na matriz (29 de 29); custodiantes não bancários e pedidos lidos um a um; sem segundo leitor |
| `dados/analise/q6_servico.csv` | denúncia (198) | família do artifício, vítima idosa e pessoa jurídica, aumento pela idade, pontos do serviço, crédito em nome da vítima, reação do banco, ressarcimento pelo intermediário | idosa, crédito e reação lidos; pontos do serviço por termos; sem segundo leitor |
| `dados/analise/q7_titular.csv` | denúncia de só conta (101) | versão do titular, a quem e por quanto, antecedentes, menoridade relativa, ANPP da cota e desfecho | 101 versões conferidas pelo trecho, 11 corrigidas; sem segundo leitor |
| `dados/conferencia/` | caso (84) | segundo leitor cego, primeira leitura congelada, concordância e adjudicação | adjudicação aplicada; conferência humana pendente |
| `textos/tjsp/` | peça | texto integral de denúncias, sentenças, acórdãos e razões do MP | sem máscara |

O que a base sustenta, por linha de pesquisa:

- Com força: 2.2 (gargalos logísticos: a conta laranja, com o papel do denunciado, o valor em conta, a pena do titular e a desclassificação para o VII em primeiro e segundo grau), 1.4 (avaliação do tipo novo da Lei 15.397/2026, com sentenças, apelações, razões do MP e 56 acórdãos), 1.1 (taxonomia pelo teste de eliminação reformulado, cruzando sistema e canal com a capitulação da denúncia e da sentença) e 3.3 (tipologia do dano: reparação do art. 387, IV, e consequências do crime nas 171 condenações). As três primeiras foram tratadas nas questões 1 e 2, a 3.3 na questão 3 e a 2.1, que a base sustenta em parte (só a camada da rede que chega ao processo), na questão 4.
- Em parte: 3.4 e 4.1 (vulnerabilidade e governança privada, questão 6: a vítima idosa por família do artifício, os pontos do serviço e o ressarcimento pelo intermediário, sem o que o banco fez fora do processo penal), 4.4 (tempo do dado, questão 5: o intervalo do fato à denúncia e os custodiantes narrados, sem as datas dos pedidos feitos no inquérito), 2.3 (questão 7, só a entrada do titular da conta), 3.2 (notificação: a representação e o §5º revogado aparecem nos textos, sem variável) e o eixo da seletividade do controle (quem chega à denúncia e à pena).
- Não sustenta: 1.2 e 1.3 (cifra oculta e deslocamento pedem séries externas, como DataJud e boletins de ocorrência), 2.3 fora da entrada do titular, 3.1, 4.2 e 4.3.

Vieses que toda conclusão precisa carregar: o cjpg lista só processos com sentença de primeiro grau publicada, de modo que a base é de casos que chegaram à sentença; os estratos vêm de termos da sentença, corrigidos pela pós-estratificação pela capitulação da denúncia; processos em segredo de justiça ficam fora; é só o TJSP, com sentenças de 2021 a 2026, quase metade de 2026 (a do CL 1 é de 2014); e a codificação assistida e as sentenças lidas por regras tiveram segundo leitor só em amostra (34 denúncias, 50 sentenças), feito por outra instância do mesmo modelo e ainda sem conferência humana.

A questão 1 foi escolhida por ser a única que a base acompanha em todas as etapas (papel na denúncia, pena na sentença e desclassificação em segundo grau); a questão 2, por fixar a taxonomia que as demais linhas usam; a questão 3, porque a reparação e as consequências do crime estavam nos textos das sentenças e só pediam extração.

## Onde estamos

A amostra TJSP de 200 denúncias está completa, gravada e extraída.

| Estrato | Critério no cjpg | Desenho | Denúncias ok | Perdas |
| --- | --- | --- | --- | --- |
| INV | "invasão de dispositivo informático" | censo das 45 ações penais | 36 | 8 sem peça inicial, 1 sigilo |
| CL | variantes de "conta laranja" e "cessão de conta" | sorteio | 50 | 3 sem peça inicial, 5 sigilo |
| FE | "fraude eletrônica" | sorteio, com complemento | 114 | 9 sem peça inicial, 5 sigilo |

No sorteio, a semente é 20261120, com páginas sistemáticas e intercaladas e duas elegíveis por página. O peso é 1/(fração de páginas × fração tomada na página). O complemento da FE (ordens 120 a 131) foi sorteado em `scripts/sorteio_complemento_fe.py`.

Arquivos de dados:

- texto das denúncias em `textos/tjsp/denuncias/<numero>/NN_<id>.txt`;
- manifesto em `textos/tjsp/manifesto.csv` (606 partes);
- status por processo em `dados/codex/status.csv`, onde vale a última linha de cada número;
- amostra e pesos em `dados/cjpg/amostra_tjsp.csv` e `dados/cjpg/sorteio_listas.json`.

Codificação de artifício, meio e papel: cobre as 200 denúncias, com 36 manuais (`dados/extracao/codificacao_manual_r1.csv` e `_r2.csv`) e 164 assistidas (`dados/extracao/codificacao_assistida.csv`). A assistida foi feita pelo assistente, por leitura caso a caso com `scripts/lote_codificacao.py` e gravação por `scripts/grava_codificacao.py`, e ainda não foi conferida pelo pesquisador; 34 denúncias tiveram segundo leitor, e 14 linhas foram regravadas pela adjudicação. Regras, categorias novas e casos de fronteira estão na seção própria do `dados/extracao/LEIAME.md`.

Sentenças: 197 das 198 denúncias sem duplicatas têm sentença lida (falta o FE 16). As 29 da matriz foram lidas à mão (`dados/extracao/sentencas_matriz.csv`, 30 linhas com o corréu do CL 11); as demais, pelo leitor por regras de `scripts/resultado_sentenca.py`, validado contra a matriz, com revisão à mão dos casos marcados. Uma linha por processo em `dados/extracao/sentencas_amostra.csv` (199 linhas, com as duas duplicatas), texto em `textos/tjsp/sentencas/<numero>/`, manifesto em `textos/tjsp/manifesto_sentencas.csv`, status em `dados/codex/status_sentencas.csv` e consolidação em `scripts/consolida_sentencas.py`, que grava `dados/extracao/resumo_sentencas.json`. As duas seções finais do `dados/extracao/LEIAME.md` descrevem a coleta, o leitor e os resultados.

Extração: `python scripts/extrai_denuncias.py` gera `dados/extracao/denuncias_tjsp.csv` (200 linhas, cerca de 72 colunas) e `dados/extracao/segmentos/<numero>.json` (cota, narrativa, capitulação). As regras, a validação e as decisões estão em `dados/extracao/LEIAME.md`, a leitura obrigatória antes de mexer na extração.

## Decisões tomadas

- Pós-estratificação pela capitulação da própria denúncia (`tipo_capitulacao`), cruzada com o estrato de origem, porque o estrato veio da sentença.
- A unidade principal é a denúncia sem duplicatas (`duplicata_de`), com o peso do processo. Há duas duplicatas: INV 7 repete INV 2, e INV 3 repete INV 32. O denunciado é a unidade secundária e depende de codificação manual.
- Dados pessoais sem máscara nesta fase, por decisão do usuário ("não vamos por ora mascarar"). O `scripts/extrai_inicio.py` mascara, mas não está em uso.
- Correções manuais conferidas em outra peça ficam no dicionário `CORRECOES` do script. Por ora há só o INV 35, cuja capitulação diz 155-A e cuja sentença lê 154-A.
- Papel do denunciado, regra de adjudicação do segundo leitor: a execução atribuída ao denunciado junto com comparsa não identificada (CL 48, FE 51, FE 89) mantém o titular de conta; só a atribuição individual do ardil faz misto (CL 40).
- Denúncias fora da tipologia (classe "fora" dos eixos: INV 40, CL 12, CL 25, FE 123) ficam nos CSVs e fora dos resumos das questões 1 e 3.
- INV 22 foi relido pela cópia de 2025 (OCR), porque o texto nativo do PJe termina na página 16 de 24.
- As regex do §2º-A e do §4º do 171 só aceitam o parágrafo solto quando o trecho desde a última menção a artigo cita o 171 (rodada 3 do LEIAME). Antes, o §2º-A do roubo levava CL 11 e CL 18 ao 171 §2º-A; hoje estão no 158.

## Resultados até aqui

Distribuição pela capitulação, sem duplicatas e com peso dentro do estrato:

| Estrato | Denúncias | Distribuição |
| --- | --- | --- |
| INV | 34 | 154-A 85,3% |
| CL | 50 | 171 §2º-A 43,2%; 171 sem §2º-A 27,8%; 155 §4º-B 10,7%; 158 7,2% |
| FE | 114 | 171 §2º-A 86,3%; 171 sem §2º-A 10,8% |

Nenhuma denúncia capitula o 171 §2º, VII.

Sentenças da matriz (29 casos, sem peso, porque a matriz é escolha e não amostra):

- Há condenação de ao menos um réu em 28; a absolvição integral é o INV 14, em que a devassa do celular da ex-companheira foi denunciada como furto e caiu por falta de ânimo de assenhoramento.
- A sentença muda a capitulação da denúncia em quatro: FE 107 afasta o §2º-A, FE 84 passa do 155 §4º-B ao 171 §2º-A por emendatio libelli, CL 11 e CL 7 desclassificam a extorsão para o 171 §2º, VII (Lei 15.397/2026) como lei mais benéfica.
- O FE 77 (27/05/2026) recusou essa desclassificação, por falta de prova de que os recursos financiassem atividade criminosa ou dela proviessem. São duas leituras do novo inciso em juízos de primeiro grau.
- O titular da conta de passagem vai da absolvição (FE 55, FE 107) a 5a4m em semiaberto (CL 18, oito dias antes da lei), com 4 anos no §2º-A como resposta mais comum. No mesmo fato do CL 11, o executor recebeu 11a4m em fechado e o cedente da conta 1 ano em aberto.
- Os indicadores `condena` e `absolve` do cjpg acertaram 21 de 28 condenações e 1 de 8 absolvições. O teor do cjpg para perto de 50 mil caracteres e perde o dispositivo das sentenças longas, de modo que não servem como resultado.

Sentenças da amostra (197 de 198 denúncias sem duplicatas, % ponderado dentro do estrato):

| Estrato | Ao menos um réu condenado | Capitulação acolhida nas condenações | Mantém a capitulação da denúncia |
| --- | --- | --- | --- |
| INV | 85,3% | 154-A 66,7% | 70,4% |
| CL | 94,2% | 171 §2º-A 31,5%; 171 sem §2º-A 25,9%; 171 §2º, VII 22,7% | 65,8% |
| FE | 87,3% | 171 §2º-A 82,1%; 171 sem §2º-A 15,3% | 86,7% |

- Lei 15.397/2026: das 32 sentenças CL posteriores a 04/05/2026, 10 aplicam o 171 §2º, VII, 8 recusam, 2 o mencionam sem decidir sobre ele, 10 silenciam e 2 só têm o dispositivo. Na FE, das 39 posteriores, 1 aplica (FE 42), 2 recusam (FE 72, FE 77) e 36 silenciam. As recusas se apoiam em participação maior que a cessão da conta, em falta de prova da cessão inocente ou em direito intertemporal, onde FE 72 (irretroatividade) e CL 13 (lei mais benéfica) leem o mesmo problema ao contrário.
- Pena mediana no 171 §2º-A: 48 meses no CL e na FE; no 171 §2º, VII, 12 meses; no 171 sem §2º-A, 12 a 14 meses.
- O movimento do Codex contradiz o texto em cinco absolvições (INV 19, CL 31, FE 4, FE 7, FE 18).

Segundo grau da Lei 15.397/2026 (`dados/tjsp2/LEIAME.md`):

- Das 23 sentenças da amostra que trataram do inciso VII, duas apelações foram julgadas sem decidir sobre ele (CL 48, FE 77); o MP apelou de quatro aplicações (CL 7, CL 11, CL 13, CL 45), com teses de participação no §2º-A, de restrição do inciso ao estelionato e, no CL 45, de irretroatividade em dilema.
- No cjsg, 56 acórdãos de 24/06 a 19/11/2026 decidem o inciso na ementa: ele prevalece em 25 (16 por retroatividade benigna) e é recusado em 31, quase sempre porque o titular aderiu à fraude e é partícipe pelo art. 29. A irretroatividade do FE 72 aparece em um acórdão da 5ª Câmara (1545200-63.2024.8.26.0050). A 16ª Câmara concentra as aplicações (13 das 25).
- Seis processos da amostra já têm acórdão: FE 56, CL 6, CL 58, FE 101 e FE 96 foram desclassificados para o VII em segundo grau; o CL 47 teve a desclassificação recusada.

Achados da codificação de 198 denúncias sem duplicatas (36 manuais e 162 assistidas), com peso dentro do estrato:

- O valor do fato entrou em conta de denunciado em 48 das 50 denúncias CL (96,5%) e em 90 das 114 FE (78,8%). As duas CL restantes estão fora da tipologia (tráfico e anabolizantes). Em FE o papel se divide em titular 52,7%, misto 26,1% e executor sem conta 21,2%; os executores concentram-se em compras fraudulentas contra empresas e no golpe do motoboy.
- Artifícios principais: em FE, venda falsa 30,3%, falso parente 20,3% e falsa central 18,9%; em CL, venda falsa 22,7%, falso parente 19,5% e falsa central 12,8%; no INV, controle da parceira 26,5%, invasão de sistema com venda de dados 17,6% e sequestro de conta 14,7%.
- No INV, 7 das 34 denúncias (5 das 29 no 154-A) têm contexto de violência doméstica (coluna `contexto_vd`, que coincide com a codificação), sem nenhuma nos outros estratos. Outras 4 são conflitos entre ex-parceiros ou colegas sem VD narrada (`relacional`).

A validação das regex fora da amostra (rodada r2, 12 casos) deu concordância de 0,83 a 1,00 (`dados/extracao/validacao_regex.csv`). Contra a codificação assistida (`validacao_regex_assistida.csv`, 162 casos), a concordância vai de 0,77 (conta do denunciado) a 0,98 (falso parente), com as regex de conta, venda falsa e falsa central errando por omissão. `m_pix` e `m_boleto` medem menção, não meio de pagamento.

## Próximos passos, em ordem

1. Conferência humana, pelo pesquisador, das 57 decisões de `dados/conferencia/adjudicacao.csv` (coluna `motivo`), começando pelas de fronteira (CL 48 e CL 40 no papel, INV 4, INV 30 e FE 125 nos danos, CL 13 e CL 58 no intermediário). Mudança de decisão entra no lugar de sempre (`grava_codificacao.py`, `pipe_sentencas.py corrige` ou os dicionários dos scripts de análise), com a coluna `final` atualizada; `python3 scripts/segundo_leitor.py` acusa o que não estiver aplicado. A conferência decide também se as categorias novas da codificação (`relacional`, `extorsao_transferencia`, `taxa_antecipada`, `devassa_privacidade`, `falso_relacionamento`, `outro`) ficam ou são fundidas.
2. Releitura das consequências do crime nas condenações que o leitor por termos não marcou (`conseq_valoracao` = "não lida" em `q3_dano.csv`, cerca de 98), porque a amostra mostrou uma negativa perdida em 21 (FE 21); e decisão sobre o FE 16 (1505916-93.2021.8.26.0554, sentença de 14/11/2024 no cjpg sem movimento nem DJEN; tentar a lista de documentos do Codex ou o cjpg no navegador).
3. Segundo leitor para as tabelas que a conferência não cobriu: `NIVEL` e o vetor da questão 1, `OBJETO` e `CANAL_MANUAL` dos eixos, o dicionário `ESTRUTURA` da questão 4, com leitura integral das 65 denúncias plurais, e os dicionários manuais das questões 5 a 7 (`TERCEIRO`, `PEDIDO_COTA`, `CREDITO`, `REACAO`, `VERSAO_MANUAL`), com as 101 versões do titular lidas no texto integral da sentença.
4. Lei 15.397/2026 em segundo grau, continuação: ler o inteiro teor dos 18 acórdãos sem ementa ou com o tema só no inteiro teor (`acordaos_inciso_vii.csv`, decisões "ementa indisponível" e "ementa não trata"); acompanhar o CL 34 (pauta virtual de 03/12/2026, 10ª Câmara) e os apelos do MP no CL 7, CL 11, CL 13 e CL 45; repetir as duas buscas do cjsg mensalmente para ver se a irretroatividade da 5ª Câmara ganha outras câmaras; ler o motivo da troca do VII pelo 171 caput na 2ª Câmara (1502402-29.2022.8.26.0577).
5. Portar as melhorias do pipe da conversa (`scripts/pipe_conversa.py`) para `scripts/codex_denuncias.py`: candidata de reserva antes do "Recebida a denúncia", filtro de denúncia nomeada, deduplicação por código PJe, guarda contra folha de inquérito e regras de OCR.
6. Máscara de CPF, RG, telefone e endereço para a versão de circulação, quando o usuário decidir.
7. Fase 2 (TJPA), a replanejar. Convém testar se a consulta de julgados do TJPA permite a mesma busca textual.

## Como operar o Codex (TecJustica) nesta pesquisa

- Chamadas sequenciais, na metade da cota (cerca de 10 por minuto), sem subagentes.
- Nunca usar `pdpj_perguntar_processo`.
- Batch com até 50 IDs. Repetir o ID até a saída passar de cerca de 75 KB força a gravação em arquivo, e então `scripts/pipe_conversa.py grava <arquivo>` grava texto, manifesto e status.
- Rodar de dentro da raiz do repo. O roteiro por processo é este:
  1. Chamar `pdpj_mapa_documentos`.
  2. Rodar `python3 scripts/pipe_conversa.py ids <mapa> | head -1`. Se o mapa veio inline, rodar `bash scripts/mk_mapa.sh NUM "ord|data|nome|chars|id|pje"`.
  3. Ler pelo batch com os IDs impressos.
  4. Rodar `grava` e depois `next`.
  5. Para registrar perdas: `status NUM sem_peca_inicial|sigilo "detalhe"`.
- Sem denúncia nomeada, use a petição ou manifestação do MP imediatamente anterior ao movimento "Recebida a denúncia". A denúncia às vezes está em "Outros".
- Quando o texto nativo vem cortado, procure no mapa uma cópia posterior da mesma peça, sem texto indexado, e leia-a por OCR.
- O `pipe_conversa.py` usa `/tmp/cur.json` como estado do processo corrente, que se perde ao trocar de sessão.
- Limite por hora: a coleta das sentenças, em cerca de 100 processos por hora (duas chamadas cada), esbarrou no limite horário do conector, que respondeu com espera de 1109 s e aviso contra uso em lote. Retomada com intervalo mínimo de 40 s entre chamadas (cerca de 90 por hora), sem novo bloqueio. Não repetir a chamada recusada antes da espera indicada.
- Segundo grau: o DJEN pelo Codex (`pdpj_buscar_comunicacoes` com o número e a janela desde a sentença, sem texto completo) mostra entrada, distribuição, pauta e "intimação de acórdão"; o acórdão aparece em `pdpj_list_movimentos` com `tipo_filter="Julgamento"` ("Julgado virtualmente", com documento) e é lido em lote. As razões do MP estão em `pdpj_list_documentos`, como páginas de "Petição" ou "Razões de Apelação" na data da interposição. Registro em `scripts/registra_apelacao.py` e texto em `scripts/grava_acordao.py`.
- Jurisprudência de segundo grau (cjsg): pelo navegador embutido, em `esaj.tjsp.jus.br/cjsg/consultaCompleta.do`; a pesquisa livre aceita aspas e o operador E. As páginas seguintes vêm de `/cjsg/trocaDePagina.do?tipoDeDecisao=A&pagina=N&conversationId=` na mesma sessão, com pausa de 3 s; o retorno grande do `javascript_tool` vai para arquivo e é lido pelo shell sem passar pelo contexto. A ementa integral está em `#textAreaDados_<cdacordao>`.
- Sentenças da amostra, com `scripts/pipe_sentencas.py`: `prox` dá o próximo caso da amostra; depois do `pdpj_list_movimentos` e do batch (ID repetido 15 vezes para a saída ir a arquivo), `lote <arquivo> "data|movimento|complemento"` grava e lê; `djen NUM "mov" campo=valor` registra o dispositivo lido no DJEN; `corrige NUM campo=valor` corrige à mão; `recalcula` relê tudo depois de mudar o leitor. Roteiro antigo da matriz: `next` dá o caso; `pdpj_list_movimentos(NUM, tipo_filter="cedência")` dá o movimento de procedência ou improcedência e o ID da sentença; `ids NUM ID[:chars]` imprime os IDs repetidos; o batch com eles grava em arquivo; `grava <arquivo>` guarda texto, manifesto e status e imprime só o dispositivo. Sem documento no movimento, `pdpj_list_documentos` acha a sentença pelo nome (CL 1, CL 11). O estado fica em `/tmp/sent_cur.json`; rodar `ids` antes de cada batch.

## Restrições permanentes

- Gravar só o texto lido de cada peça, sem baixar a peça.
- Nunca gravar a linha `Original:` do Codex, porque o link contém token.
- Sem contornar CAPTCHA nem recusas de acesso automatizado ao TJSP. O cjpg roda pelo navegador embutido ou no computador do usuário.
- Repositório privado.
- Respostas em português, sem travessões, em prosa, começando pela resposta. Nas escolhas binárias, decidir pelo usuário e justificar em uma frase.

## Documentos de contexto

- `README.md`: mapa do repositório.
- `docs/RUNBOOK_TJSP.md`: roteiro do cjpg e do Codex.
- `docs/plano-captura.md`: plano completo.
- `dados/extracao/LEIAME.md`: extração.
- No Project "Criminologia Informática" do claude.ai, o doc `claude/plano-captura-base-tjpa.md` espelha o estado da coleta, e o `claude/matriz-selecao-casos.md` resume a matriz de 29 casos para exame criminológico (documento editável em https://claude.ai/artifact/4rUKtiqaqKiia9LUKqGm3Y), agora com a seção de sentenças.
