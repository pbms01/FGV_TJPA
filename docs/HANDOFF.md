# Handoff: fase 1 TJSP, com amostra, extração, codificação de papel e sentenças da matriz (21/11/2026)

Repositório pbms01/FGV_TJPA, branch `coleta-datajud`, que ainda não foi mesclado no main. Este arquivo substitui o estado da conversa e deve ser lido antes de qualquer passo novo.

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

Sentenças: as 29 da matriz de seleção foram lidas, com mais a do corréu do CL 11 (`scripts/pipe_sentencas.py`). Texto em `textos/tjsp/sentencas/<numero>/`, manifesto em `textos/tjsp/manifesto_sentencas.csv`, status em `dados/codex/status_sentencas.csv` e resultado, capitulação acolhida e pena em `dados/extracao/sentencas_matriz.csv` (30 linhas). As outras 171 denúncias da amostra ainda não têm sentença lida. A seção final do `dados/extracao/LEIAME.md` descreve a coleta.

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

Achados da codificação de 198 denúncias sem duplicatas (36 manuais e 162 assistidas), com peso dentro do estrato:

- O valor do fato entrou em conta de denunciado em 48 das 50 denúncias CL (96,5%) e em 90 das 114 FE (78,8%). As duas CL restantes estão fora da tipologia (tráfico e anabolizantes). Em FE o papel se divide em titular 52,7%, misto 26,1% e executor sem conta 21,2%; os executores concentram-se em compras fraudulentas contra empresas e no golpe do motoboy.
- Artifícios principais: em FE, venda falsa 30,3%, falso parente 20,3% e falsa central 18,9%; em CL, venda falsa 22,7%, falso parente 19,5% e falsa central 12,8%; no INV, controle da parceira 26,5%, invasão de sistema com venda de dados 17,6% e sequestro de conta 14,7%.
- No INV, 7 das 34 denúncias (5 das 29 no 154-A) têm contexto de violência doméstica (coluna `contexto_vd`, que coincide com a codificação), sem nenhuma nos outros estratos. Outras 4 são conflitos entre ex-parceiros ou colegas sem VD narrada (`relacional`).

A validação das regex fora da amostra (rodada r2, 12 casos) deu concordância de 0,83 a 1,00 (`dados/extracao/validacao_regex.csv`). Contra a codificação assistida (`validacao_regex_assistida.csv`, 162 casos), a concordância vai de 0,77 (conta do denunciado) a 0,98 (falso parente), com as regex de conta, venda falsa e falsa central errando por omissão. `m_pix` e `m_boleto` medem menção, não meio de pagamento.

## Próximos passos, em ordem

1. Conferência da codificação assistida pelo pesquisador, numa amostra estratificada (por exemplo, 8 casos por estrato com semente nova) somada aos casos de fronteira listados no `dados/extracao/LEIAME.md`. Correções entram por `python3 scripts/grava_codificacao.py`, que substitui a linha do mesmo número. A conferência decide também se as categorias novas (`relacional`, `extorsao_transferencia`, `taxa_antecipada`, `devassa_privacidade`, `falso_relacionamento`, `outro`) ficam ou são fundidas.
2. Sentenças das outras 171 denúncias da amostra, pelo mesmo roteiro do `scripts/pipe_sentencas.py` (seção do Codex abaixo). Para isso, o `next` precisa ler a lista de `amostra_tjsp.csv` e pular os 29 já lidos, e convém escrever uma regex de resultado sobre o dispositivo, validada contra as 30 linhas de `sentencas_matriz.csv`, para não depender de `condena` e `absolve` do cjpg.
3. Variável da Lei 15.397/2026 nas sentenças: data do fato e da sentença em relação a 04/05/2026, aplicação ou recusa do 171 §2º, VII e fundamento. A matriz já tem os pares (CL 11, CL 7 e FE 77 depois da lei; CL 18 e FE 115 antes), que conversam com a análise contrafactual do Project.
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
- Sentenças, com `scripts/pipe_sentencas.py`: `next` dá o caso; `pdpj_list_movimentos(NUM, tipo_filter="cedência")` dá o movimento de procedência ou improcedência e o ID da sentença; `ids NUM ID[:chars]` imprime os IDs repetidos; o batch com eles grava em arquivo; `grava <arquivo>` guarda texto, manifesto e status e imprime só o dispositivo. Sem documento no movimento, `pdpj_list_documentos` acha a sentença pelo nome (CL 1, CL 11). O estado fica em `/tmp/sent_cur.json`; rodar `ids` antes de cada batch.

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
