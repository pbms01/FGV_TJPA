# FGV_TJPA

Repositório do projeto de pesquisa em criminologia informática: bases processuais e documentos de análise sobre a fraude e o acesso informático mediados por tecnologia, construídos com processos judiciais e consulta pública de tribunais. Reúne duas frentes: a base de 130 casos de consulta pública do TJSP, com sentenças e documentação, e a base processual das fases 1 (TJSP, capturada por cjpg, DataJud e Codex, com as notas analíticas) e 2 (TJPA, capturada pelo DJEN e pelo Codex).

| Pasta | Conteúdo |
| --- | --- |
| `sentencas_tjsp_base100/` | Base de 130 casos do TJSP (furto mediante fraude eletrônica, fraude eletrônica e invasão de dispositivo), com íntegras das sentenças, `indice.csv`, `fichas.jsonl`, a planilha exportada (`planilha/`) e a coleta com seus scripts (`coleta/`) |
| `documentacao_projeto/` | Nota metodológica da base, análise contrafactual dos casos, quadro da Convenção de Budapeste e quadro de visibilidade nas TPU, com índice dos documentos e das versões editáveis |
| `roteiro_aula_magistrados/` | Roteiro de aula para magistrados e assessores sobre quinze casos da base, em Markdown e Word |
| `docs/`, `scripts/`, `dados/`, `textos/`, `consultas/` | Base processual da fase 1 (TJSP) e da fase 2 (TJPA, em `dados/djen/`, `dados/codex_tjpa/` e `textos/tjpa/`): plano de captura, linhas de pesquisa, roteiros, amostra de 200 denúncias e suas sentenças, extração, codificação e análises das questões 1 a 7; e as séries oficiais do estelionato eletrônico (Anuário do FBSP, censo do Pará, fraudes no Pix do BCB); mapa detalhado abaixo |

Os textos das sentenças e das denúncias trazem os nomes de réus, vítimas e testemunhas como publicados ou como lidos nos autos; as fichas e a planilha da base de 130 casos os omitem. Não redistribuir os textos sem anonimização.

## Base processual das fases 1 (TJSP) e 2 (TJPA)

Base processual para um exame cibercriminológico da fraude mediada por tecnologia, construída apenas com processos judiciais. A consulta pública de julgados do tribunal fornece os números de processo (no TJPA, que não tem consulta de sentenças de 1º grau, a API pública do DJEN), e o Codex (PDPJ) lê as peças. O texto lido vai para o repositório.

Fase 2 (TJPA), em 21/11/2026: a lista de 299 números saiu do DJEN, com 225 de ação penal ou apelação criminal, e o Codex leu a denúncia de 191 deles e a sentença ou decisão terminativa de 115, com a rota ajustada ao TJPA, onde o inquérito e a ação penal têm o mesmo número. O roteiro, o estado e as lições estão em `docs/RUNBOOK_TJPA.md`; a extração dos campos ainda não foi feita.

Estado em 21/11/2026: a coleta da fase 1 (TJSP) está encerrada para fins de análise, com a amostra de 200 denúncias (INV 36 em censo, CL 50, FE 114) e as sentenças de 197 delas gravadas, extraídas por regras e codificadas (36 denúncias à mão e 164 de forma assistida, estas pendentes de conferência humana), e a análise criminológica tem as questões 1 a 7 feitas, as três primeiras conferidas por segundo leitor cego numa amostra de 34 denúncias e 50 sentenças, com notas em `docs/analise/`. O plano de exame em aula das sete questões, em 16 casos, está em `docs/aula/plano-exame-casos.md`. A fase 2 (TJPA) tem a coleta encerrada e a extração feita: 191 denúncias (179 sem as duplicatas de desmembramento) e 115 sentenças, pelas regras da fase 1, com método e resultados na seção final do `dados/extracao/LEIAME.md`. O estado, as decisões e os próximos passos estão em `docs/HANDOFF.md`, que é o ponto de partida de qualquer sessão nova. Os números-alvo vieram da Consulta de Julgados de 1º Grau do e-SAJ (cjpg), por busca textual, porque o TJSP quase não usa os códigos TPU que nomeiam o tipo. O DataJud fica como denominador.

## Estrutura

| Caminho | Conteúdo |
| --- | --- |
| `docs/HANDOFF.md` | Estado da pesquisa, decisões, próximos passos e modo de operar o Codex; ler primeiro |
| `docs/plano-captura.md` | Plano completo: recorte, achados da sondagem, escada de captura, amostragem, livro de códigos, regra de seleção das peças, dado pessoal, riscos |
| `docs/linhas-de-pesquisa.md` | Arquitetura das linhas de pesquisa em criminologia informática que o livro de códigos serve |
| `docs/RUNBOOK.md` | Roteiro da coleta noturna do TJPA pelo DataJud (19 e 20/11/2026), substituído na porta de entrada pelo `RUNBOOK_TJPA.md` |
| `docs/RUNBOOK_TJPA.md` | Fase 2: números-alvo pela API do DJEN (semântica da busca, consultas, vieses), localização da denúncia no Codex do TJPA, custo e pendências |
| `docs/RUNBOOK_TJRJ.md` | Fase 3: TJRJ pelo DJEN (janela desde 11/2024) e pelo Codex (PJe, DCP e eJUD) |
| `docs/RUNBOOK_TJSC.md` | Fase 4: TJSC pelo DJEN, com as frases também em entidades HTML; lista de 454 ações penais ou apelações e fila em três grupos, com o grupo dos réus citados por edital |
| `scripts/djen_alvos.py` | Números-alvo pela API pública do DJEN: cinco rótulos de consulta por frase, união por id, filtro de classe, indicadores e consolidação por número, sem nomes de pessoas (só biblioteca padrão; roda no computador do usuário) |
| `scripts/djen_navegador.js` | Mesmo coletor para rodar numa aba do comunica.pje.jus.br (via da sondagem de 21/11/2026); `entidades: true` roda as frases também com entidades HTML (TJSC), e a janela que bate no teto de 10.000 se parte por data |
| `scripts/testes/djen_fixture.json` | Fixture sintética da resposta do DJEN para testar o coletor (`--teste`) |
| `dados/djen/` | Listas de alvos do TJPA (`alvos_djen_tjpa.csv`, 299 números), do TJRJ e do TJSC (`alvos_djen_tjsc.csv`, 467 números, com os metadados de cada publicação em `publicacoes_tjsc.csv`) e totais por frase, rótulo e classe, com as séries de controle de cobertura (`totais_<trib>.json`) |
| `docs/RUNBOOK_TJSP.md` | Fase 1: números-alvo pelo cjpg, localização da denúncia no Codex, gravação do texto lido, campos do corpus, achados do piloto |
| `scripts/cjpg_alvos.py` | Números-alvo do TJSP pela Consulta de Julgados de 1º Grau: quatro consultas textuais, indicadores de precisão, consolidação por número (só biblioteca padrão) |
| `scripts/cjpg_navegador.js` | Mesmo coletor para rodar numa aba do cjpg (via do piloto) |
| `scripts/cjpg_sorteio.js` | Sorteio da amostra de 200 (estratos INV, CL, FE; semente 20261120) numa aba do cjpg |
| `scripts/sorteio_para_csv.py` | Converte o resultado do sorteio em `dados/cjpg/amostra_tjsp.csv` |
| `scripts/codex_denuncias.py` | Lê pelo Codex a denúncia de cada processo da amostra e grava só o texto, dentro da cota (roda com a chave TecJustica do usuário) |
| `scripts/testes/cjpg_fixture.html` | Fixture sintética da listagem do cjpg para testar o parser (`--teste`) |
| `dados/cjpg/` | Piloto de 20/11/2026: 110 linhas com metadados, indicadores e recorte da imputação, e os totais de cada consulta |
| `scripts/censo_denuncias_tjsp.py` | Censo DataJud dos códigos 11978, 15623 e 15755 no TJSP (denominador, quando a API voltar) |
| `scripts/sorteio_datajud_tjsp.py` | Seleção dos processos-alvo do TJSP: sorteio estratificado no servidor, autônomo, só biblioteca padrão |
| `scripts/sorteio_servidor.py` | Mesmo sorteio para o TJPA, sobre `datajud.py` |
| `scripts/datajud.py` | Cliente mínimo com rejeição de resposta parcial e registro de cada tentativa |
| `scripts/coleta_janelas.py`, `coleta_censo.py` | Censo por janelas de data (o `coleta_censo.py` depende de ordenar por `_id`, que o cluster passou a recusar) |
| `scripts/analisa_censo.py`, `amostra.py` | Análise local do censo e sorteio local |
| `scripts/panorama.py` | Panorama por metadados de TJSP, TJMG, TJBA e TJPA |
| `scripts/pipe_conversa.py`, `scripts/mk_mapa.sh` | Coleta das denúncias na conversa: IDs da peça a partir do mapa do Codex, gravação do texto, manifesto e status |
| `scripts/pipe_sentencas.py` | Coleta das sentenças na conversa: na matriz, pela ordem de `dados/extracao/matriz_casos.csv`; na amostra, `prox`, `lote`, `djen`, `corrige` e `recalcula`, com gravação do texto sem a linha `Original:`, manifesto, status e uma linha por processo em `dados/extracao/sentencas_amostra.csv` |
| `scripts/resultado_sentenca.py` | Leitor por regras do dispositivo: resultado, capitulação acolhida, pena, regime, substituição e menção à Lei 15.397/2026; `valida` compara com as 30 linhas lidas à mão da matriz |
| `scripts/consolida_sentencas.py` | Consolidação das sentenças da amostra por estrato, com peso, mudança de capitulação, variável da Lei 15.397/2026 e divergência entre movimento e texto; grava `dados/extracao/resumo_sentencas.json` |
| `scripts/eixos_mediacao.py` | Eixos da mediação técnica comuns às análises (sistema: objeto ou meio; canal; distância como agrupamento dos canais), pelo critério das linhas de pesquisa, versão 0.4 |
| `scripts/analise_q1_alcance.py` | Questão 1: quem o sistema penal alcança na fraude eletrônica (nível e vetor de identificação), pena por papel e Lei 15.397/2026; grava `dados/analise/q1_*` |
| `scripts/analise_q2_eliminacao.py` | Questão 2: teste de eliminação reformulado (sistema e canal) cruzado com a capitulação da denúncia e o tipo acolhido; grava `dados/analise/q2_*` |
| `scripts/reparacao_387.py` | Leitor por regras da reparação mínima do art. 387, IV, do CPP, das consequências do crime e do pedido de reparação na denúncia; `valida` compara com a leitura à mão da matriz |
| `scripts/analise_q3_dano.py` | Questão 3: tipologia do dano e distribuição da reparação pelos eixos, pelo nível alcançado e pela vulnerabilidade da vítima; grava `dados/analise/q3_*` |
| `scripts/organizacao.py` | Leitor da organização narrada nas denúncias: número de denunciados, enquadramento do concurso (Lei 12.850, 288, concurso, autoria singular), quem pediu a conta; estrutura do grupo e desfecho do 288 em dicionários; `valida` compara o número de denunciados com a matriz |
| `scripts/analise_q4_organizacao.py` | Questão 4: estrutura narrada e enquadramento cruzados com os eixos, o nível da questão 1 e a sentença; grava `dados/analise/q4_*` |
| `scripts/tempo_dado.py` | Leitor do tempo do dado: data do fato e da denúncia, fontes narradas por custodiante (banco, vítima, operadora, plataforma, conexão, aparelho, câmeras) e pedidos de dado na cota, com leitura manual dos custodiantes não bancários; `valida` confere a data do fato na matriz |
| `scripts/analise_q5_tempo_dado.py` | Questão 5: intervalo do fato à denúncia por estrato, canal e nível, fontes por custodiante e pedidos da cota contra os prazos de guarda do Marco Civil, da Lei 12.850 e da Lei 9.613; grava `dados/analise/q5_*` |
| `scripts/servico_banco.py` | Leitor da vulnerabilidade e do serviço: família do artifício, vítima idosa e pessoa jurídica, aumento pela idade, credencial, crédito em nome da vítima, várias operações, repasse imediato e reação do banco; `valida` imprime os trechos na matriz |
| `scripts/analise_q6_servico.py` | Questão 6: vítima e pontos do serviço por família do artifício, cruzados com o ressarcimento pelo intermediário da questão 3; grava `dados/analise/q6_*` |
| `scripts/titular_conta.py` | Leitor da versão do titular da conta (cessão, negativa, ausência), de a quem e por quanto, dos antecedentes e da menoridade relativa, na denúncia e na sentença; `valida` imprime as 101 leituras |
| `scripts/analise_q7_titular.py` | Questão 7: versão, perfil e desfecho do titular de só conta, com o ANPP da cota; grava `dados/analise/q7_*` |
| `scripts/fenomenos_ponderados.py` | Os 18 fenômenos de maior valor prático das questões 1 a 7, com percentual simples e ponderado e os casos de origem; grava `dados/analise/fenomenos.csv` e `fenomenos_casos.csv` |
| `scripts/segundo_leitor.py` | Concordância entre a primeira leitura (congelada em `dados/conferencia/primeira_leitura.csv`) e o segundo leitor cego, e conferência de que a adjudicação (`dados/conferencia/adjudicacao.csv`) está aplicada aos dados |
| `docs/analise/` | Notas analíticas das questões 1 a 7 e nota de método do segundo leitor, espelhadas no Project "Criminologia Informática" |
| `scripts/artificio_tjpa.py` | Codificação do artifício nas 183 denúncias sem duplicata do TJPA (`dados/extracao/codificacao_artificio_tjpa.csv`, com segundo leitor por amostra e adjudicação em `dados/conferencia/tjpa/adjudicacao_artificio.csv`): confere os códigos PA, a família e o quadro da nota `docs/analise/codificacao-artificio-tjpa.md` |
| `docs/aula/` | Plano de exame em aula das sete questões em oito pares de casos, fichas dos casos (`fichas/`) e fontes dos exercícios com gabarito publicados como artefatos (`exercicios/`) |
| `scripts/casos_aula.py` | Índice dos 16 casos da aula (`dados/aula/casos_aula.csv`), esqueleto de cada ficha com os valores já codificados e links do GitHub das peças |
| `dados/aula/` | Índice dos casos da aula, divergências da leitura integral contra a codificação e triagem das sentenças do INV quanto à elementar de segurança do 154-A |
| `docs/estatisticas/` | Séries oficiais do estelionato eletrônico: nota com método, achados e roteiro de reprodução (espelho do doc do Project), fontes das páginas publicadas como artefatos (`paginas/`) e gráficos em PNG (`graficos/`) |
| `scripts/estatisticas_*.py`, `scripts/templates/` | Download das planilhas do Anuário do FBSP e do artigo do Pará para `dados/bruto/` (fora do git), série por UF e edição, painel balanceado de 18 UFs, página do Pará, fraudes no Pix do BCB e captura das páginas em PNG |
| `dados/estatisticas/` | O que foi lido das fontes externas: estelionato e estelionato por meio eletrônico por UF em cada edição do Anuário e na edição mais recente, tabelas do censo do Pará como lidas, série do Pará contra o Anuário e fraudes mensais no Pix (MED) |
| `scripts/registra_apelacao.py` e `scripts/grava_acordao.py` | Andamento em segundo grau das sentenças que trataram da Lei 15.397/2026 (`dados/tjsp2/apelacoes_amostra.csv`) e gravação de acórdãos e razões de apelação lidos pelo Codex |
| `scripts/classifica_acordaos.py` | Junta as buscas do cjsg sobre o 171 §2º, VII e grava `dados/tjsp2/acordaos_inciso_vii.csv` com a decisão lida em cada ementa |
| `scripts/sorteio_complemento_fe.py` | Complemento do sorteio da FE (ordens 120 a 131) |
| `scripts/extrai_denuncias.py` | Extração por regras das denúncias, por tribunal: sem argumento, as 200 da amostra TJSP (reprodução da fase 1); com `tjpa`, as 191 do TJPA, com a camada do molde do MPPA; cota, narrativa, capitulação, dispositivos, indicadores de meio, alertas e duplicatas; saídas e validação em `dados/extracao/LEIAME.md` |
| `scripts/sentencas_tjpa.py` | Sentenças do TJPA pelo leitor da fase 1, com resultado próprio das decisões terminativas, pena da dosimetria e correções conferidas na leitura; grava `dados/extracao/sentencas_tjpa.csv`; `disp NUM` e `revisar` para conferência |
| `scripts/consolida_tjpa.py` | Consolidação do TJPA por estrato, com cada família de desmembramento uma vez, ao lado do TJSP pelas mesmas regras; grava `dados/extracao/resumo_tjpa.json` |
| `scripts/lote_codificacao.py`, `scripts/grava_codificacao.py` | Codificação assistida de artifício, meio e papel: o primeiro imprime em forma compacta o próximo lote não codificado de um estrato, o segundo grava em `dados/extracao/codificacao_assistida.csv` com checagem de vocabulário; com `TRIB=tjpa`, leem e gravam a codificação do TJPA (`codificacao_assistida_tjpa.csv`), conferida por `scripts/codificacao_tjpa.py` |
| `scripts/fundamento_absolvicoes.py` | Confere e tabula o fundamento das absolvições integrais da FE no TJPA (27) e no TJSP (11), gravado em `dados/analise/fundamento_absolvicoes_fe.csv`, com a decomposição da taxa de absolvição pela posição do MP nas alegações finais |
| `scripts/extrai_inicio.py` | Extração das primeiras páginas de PDF com OCR de reserva e troca de CPF/CNPJ por hash |
| `scripts/persistente.sh`, `tenta.sh` | Repetição até concluir ou até um prazo |
| `consultas/consulta_datajud_tjsp.json` | As seis consultas exatas que o sorteio do TJSP envia |
| `dados/` | Contagem por ano do estelionato no TJPA (19/11) e log de disponibilidade da API |

## Recorte do TJSP

Os tipos são os três que a TPU nomeia (decisão de 20/11/2026), mas a busca é pelo texto da sentença, não pelo código, porque o 1º grau do TJSP cadastra essas ações quase sempre como Estelionato (3431). As consultas exatas estão em `docs/RUNBOOK_TJSP.md`. Códigos de referência, conferidos no SGT versão 05/11/2026:

| Código | Assunto no SGT | Tipo | Janela de ajuizamento |
| --- | --- | --- | --- |
| 11978 | Invasão de Dispositivo Informático | art. 154-A CP | 19/11/2016 em diante, partida em 28/05/2021 (Lei 14.155/2021) |
| 15623 | Fraude Eletrônica | art. 171, § 2º-A, CP | 28/05/2021 em diante, partida em 19/09/2025 (criação do código) |
| 15755 | Estelionato Mediante Cessão de Conta Laranja | art. 171, § 2º, VII, CP | 04/05/2026 em diante (Lei 15.397/2026) |

Ficam fora o furto informático (art. 155, § 4º-B), sem código próprio e absorvido pelo 3417 Furto Qualificado, e os códigos genéricos de estelionato (3431, 3432, 14692), que não separam o meio digital. 14693, 15624 e 15756 pertencem à árvore de ato infracional.

## Como gerar a lista de alvos do TJSP

```bash
python scripts/cjpg_alvos.py                   # quatro consultas, todas as páginas, em alvos_cjpg_tjsp.csv
python scripts/cjpg_alvos.py --max-paginas 3   # piloto
python scripts/cjpg_alvos.py --teste scripts/testes/cjpg_fixture.html  # testa o parser sem rede
```

O script guarda cada resultado em `dados/cjpg/bruto/<rótulo>.jsonl`, retoma pelas páginas feitas, espera 3 s entre requisições e para, sem contornar, se a resposta trouxer CAPTCHA ou erro repetido. O sorteio por DataJud (`scripts/sorteio_datajud_tjsp.py`) continua no repositório para o censo de comparação.

## Como gerar a lista de alvos do TJPA

```bash
python scripts/djen_alvos.py --fim 2026-11-20         # cinco rótulos, em dados/djen/
python scripts/djen_alvos.py --controle estelionato   # série de cobertura por ano
python scripts/djen_alvos.py --teste                  # testa o coletor sem rede
```

Do workspace da sessão a API devolve 403; o script roda no computador do usuário, e o `scripts/djen_navegador.js` roda numa aba do comunica.pje.jus.br.

## Cuidados

- A chave do DataJud nos scripts é a chave pública que o próprio CNJ publica para todos os usuários; pode ser substituída pela variável `DATAJUD_API_KEY`.
- Decisão de 20/11/2026: o texto lido das peças entra no repositório, sem pseudonimização e sem o arquivo original. O repositório passou a público em 21/11/2026.
- Nenhum link de peça entra no repositório: a linha `Original:` do Codex traz token de acesso.
- Publicações derivadas devem citar o TJSP (Consulta de Julgados de 1º Grau) e o DJEN (CNJ) como fonte dos números, e CNJ e DataJud quando o censo por código for usado (Portaria CNJ 160/2020, art. 4º, na redação da Portaria 374/2026).
