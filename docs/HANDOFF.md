# Handoff: fase 1 TJSP coletada; próxima sessão começa a análise criminológica (21/11/2026)

Repositório pbms01/FGV_TJPA, branch `coleta-datajud`, que ainda não foi mesclado no main. Este arquivo substitui o estado da conversa e deve ser lido antes de qualquer passo novo.

## Para a próxima sessão: análise sob a perspectiva da criminologia informática

A coleta da fase 1 está encerrada para fins de análise. As pendências de coleta seguem na seção de próximos passos e não bloqueiam a análise: conferência da codificação assistida, segundo leitor das sentenças lidas por regras, FE 16, inteiro teor de 18 acórdãos e o CL 34, pautado para 03/12/2026. A referência teórica é o doc `claude/criminologia-informatica-linhas-de-pesquisa.md` do Project: quatro elementos (delito, infrator, vítima, controle social), o teste de eliminação de Wall como critério comum e a exigência de produto utilizável por quem investiga, acusa, julga ou previne.

Base analítica, unida pela coluna `numero`, com o peso de `dados/cjpg/amostra_tjsp.csv` e sem as duplicatas marcadas em `duplicata_de` (198 denúncias):

| Arquivo | Unidade | O que traz | Estado |
| --- | --- | --- | --- |
| `dados/extracao/denuncias_tjsp.csv` | denúncia (200) | estrato, capitulação, indicadores de meio, conta, Pix, boleto, ano do fato | extração por regras validada por leitura; `ano_fato` com ruído |
| `dados/extracao/codificacao_manual_r1.csv`, `_r2.csv` e `codificacao_assistida.csv` | denúncia | artifício, meio de contato, papel do denunciado, valor em conta de denunciado, contexto de violência doméstica | 36 manuais; 164 assistidas sem conferência do pesquisador |
| `dados/extracao/sentencas_amostra.csv` | processo (199) | resultado, capitulação acolhida, pena, regime, substituição, Lei 15.397/2026, notas | 29 lidas à mão, 57 corrigidas, 113 só pelo leitor por regras |
| `dados/extracao/matriz_casos.csv` e `sentencas_matriz.csv` | caso (29) | matriz de seleção para exame qualitativo | lida à mão |
| `dados/tjsp2/apelacoes_amostra.csv` | processo (23) | andamento em segundo grau das sentenças que trataram do inciso VII | DJEN até 21/11/2026 |
| `dados/tjsp2/acordaos_inciso_vii.csv` | acórdão (125) | decisão e fundamento sobre o 171 §2º, VII | leitura da ementa |
| `textos/tjsp/` | peça | texto integral de denúncias, sentenças, acórdãos e razões do MP | sem máscara |

O que a base sustenta, por linha de pesquisa:

- Com força: 2.2 (gargalos logísticos: a conta laranja, com o papel do denunciado, o valor em conta, a pena do titular e a desclassificação para o VII em primeiro e segundo grau), 1.4 (avaliação do tipo novo da Lei 15.397/2026, com sentenças, apelações, razões do MP e 56 acórdãos) e 1.1 (taxonomia pelo teste de eliminação, cruzando artifício e meio com a capitulação da denúncia e da sentença).
- Em parte: 2.1 (organização: 288 e Lei 12.850 nas capitulações e o papel "misto"), 3.4 (vulnerabilidade: §4º do 171 e artifícios dirigidos a idosos), 3.3 (dano: os valores de reparação do art. 387, IV, estão nos textos das sentenças, ainda não extraídos), 3.2 (notificação: a representação e o §5º revogado aparecem nos textos, sem variável) e o eixo da seletividade do controle (quem chega à denúncia e à pena).
- Não sustenta: 1.2 e 1.3 (cifra oculta e deslocamento pedem séries externas, como DataJud e boletins de ocorrência), 2.3, 3.1, 4.1, 4.2, 4.3 e 4.4.

Vieses que toda conclusão precisa carregar: o cjpg lista só processos com sentença de primeiro grau publicada, de modo que a base é de casos que chegaram à sentença; os estratos vêm de termos da sentença, corrigidos pela pós-estratificação pela capitulação da denúncia; processos em segredo de justiça ficam fora; é só o TJSP, com sentenças de 2021 a 2026, quase metade de 2026 (a do CL 1 é de 2014); e a codificação assistida e 113 sentenças ainda não tiveram segundo leitor.

Primeira questão proposta para a análise: quem o sistema penal alcança na fraude eletrônica, o elo físico (o titular da conta de passagem) ou o autor do ardil, e o que a Lei 15.397/2026 muda nisso. Escolhi essa porque é a única que a base acompanha em todas as etapas (papel na denúncia, pena na sentença e desclassificação em segundo grau) e porque devolve produto direto às linhas 2.2 e 1.4.

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

Codificação de artifício, meio e papel: cobre as 200 denúncias, com 36 manuais (`dados/extracao/codificacao_manual_r1.csv` e `_r2.csv`) e 164 assistidas (`dados/extracao/codificacao_assistida.csv`). A assistida foi feita pelo assistente, por leitura caso a caso com `scripts/lote_codificacao.py` e gravação por `scripts/grava_codificacao.py`, e ainda não foi conferida pelo pesquisador. Regras, categorias novas e casos de fronteira estão na seção própria do `dados/extracao/LEIAME.md`.

Sentenças: 197 das 198 denúncias sem duplicatas têm sentença lida (falta o FE 16). As 29 da matriz foram lidas à mão (`dados/extracao/sentencas_matriz.csv`, 30 linhas com o corréu do CL 11); as demais, pelo leitor por regras de `scripts/resultado_sentenca.py`, validado contra a matriz, com revisão à mão dos casos marcados. Uma linha por processo em `dados/extracao/sentencas_amostra.csv` (199 linhas, com as duas duplicatas), texto em `textos/tjsp/sentencas/<numero>/`, manifesto em `textos/tjsp/manifesto_sentencas.csv`, status em `dados/codex/status_sentencas.csv` e consolidação em `scripts/consolida_sentencas.py`, que grava `dados/extracao/resumo_sentencas.json`. As duas seções finais do `dados/extracao/LEIAME.md` descrevem a coleta, o leitor e os resultados.

Extração: `python scripts/extrai_denuncias.py` gera `dados/extracao/denuncias_tjsp.csv` (200 linhas, cerca de 72 colunas) e `dados/extracao/segmentos/<numero>.json` (cota, narrativa, capitulação). As regras, a validação e as decisões estão em `dados/extracao/LEIAME.md`, a leitura obrigatória antes de mexer na extração.

## Decisões tomadas

- Pós-estratificação pela capitulação da própria denúncia (`tipo_capitulacao`), cruzada com o estrato de origem, porque o estrato veio da sentença.
- A unidade principal é a denúncia sem duplicatas (`duplicata_de`), com o peso do processo. Há duas duplicatas: INV 7 repete INV 2, e INV 3 repete INV 32. O denunciado é a unidade secundária e depende de codificação manual.
- Dados pessoais sem máscara nesta fase, por decisão do usuário ("não vamos por ora mascarar"). O `scripts/extrai_inicio.py` mascara, mas não está em uso.
- Correções manuais conferidas em outra peça ficam no dicionário `CORRECOES` do script. Por ora há só o INV 35, cuja capitulação diz 155-A e cuja sentença lê 154-A.
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

1. Conferência da codificação assistida pelo pesquisador, numa amostra estratificada (por exemplo, 8 casos por estrato com semente nova) somada aos casos de fronteira listados no `dados/extracao/LEIAME.md`. Correções entram por `python3 scripts/grava_codificacao.py`, que substitui a linha do mesmo número. A conferência decide também se as categorias novas (`relacional`, `extorsao_transferencia`, `taxa_antecipada`, `devassa_privacidade`, `falso_relacionamento`, `outro`) ficam ou são fundidas.
2. Conferência das 113 sentenças com `conferido=auto` por segundo leitor, numa amostra estratificada, e decisão sobre o FE 16 (1505916-93.2021.8.26.0554, sentença de 14/11/2024 no cjpg sem movimento nem DJEN; tentar a lista de documentos do Codex ou o cjpg no navegador).
3. Lei 15.397/2026 em segundo grau, continuação: ler o inteiro teor dos 18 acórdãos sem ementa ou com o tema só no inteiro teor (`acordaos_inciso_vii.csv`, decisões "ementa indisponível" e "ementa não trata"); acompanhar o CL 34 (pauta virtual de 03/12/2026, 10ª Câmara) e os apelos do MP no CL 7, CL 11, CL 13 e CL 45; repetir as duas buscas do cjsg mensalmente para ver se a irretroatividade da 5ª Câmara ganha outras câmaras; ler o motivo da troca do VII pelo 171 caput na 2ª Câmara (1502402-29.2022.8.26.0577).
4. Portar as melhorias do pipe da conversa (`scripts/pipe_conversa.py`) para `scripts/codex_denuncias.py`: candidata de reserva antes do "Recebida a denúncia", filtro de denúncia nomeada, deduplicação por código PJe, guarda contra folha de inquérito e regras de OCR.
5. Máscara de CPF, RG, telefone e endereço para a versão de circulação, quando o usuário decidir.
6. Fase 2 (TJPA), a replanejar. Convém testar se a consulta de julgados do TJPA permite a mesma busca textual.

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
