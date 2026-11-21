# Handoff: fase 1 TJSP, amostra, extração e codificação de papel fechadas (20/11/2026, noite)

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

Achados da codificação de 198 denúncias sem duplicatas (36 manuais e 162 assistidas), com peso dentro do estrato:

- O valor do fato entrou em conta de denunciado em 48 das 50 denúncias CL (96,5%) e em 90 das 114 FE (78,8%). As duas CL restantes estão fora da tipologia (tráfico e anabolizantes). Em FE o papel se divide em titular 52,7%, misto 26,1% e executor sem conta 21,2%; os executores concentram-se em compras fraudulentas contra empresas e no golpe do motoboy.
- Artifícios principais: em FE, venda falsa 30,3%, falso parente 20,3% e falsa central 18,9%; em CL, venda falsa 22,7%, falso parente 19,5% e falsa central 12,8%; no INV, controle da parceira 26,5%, invasão de sistema com venda de dados 17,6% e sequestro de conta 14,7%.
- No INV, 7 das 34 denúncias (5 das 29 no 154-A) têm contexto de violência doméstica (coluna `contexto_vd`, que coincide com a codificação), sem nenhuma nos outros estratos. Outras 4 são conflitos entre ex-parceiros ou colegas sem VD narrada (`relacional`).

A validação das regex fora da amostra (rodada r2, 12 casos) deu concordância de 0,83 a 1,00 (`dados/extracao/validacao_regex.csv`). Contra a codificação assistida (`validacao_regex_assistida.csv`, 162 casos), a concordância vai de 0,77 (conta do denunciado) a 0,98 (falso parente), com as regex de conta, venda falsa e falsa central errando por omissão. `m_pix` e `m_boleto` medem menção, não meio de pagamento.

## Próximos passos, em ordem

1. Conferência da codificação assistida pelo pesquisador, numa amostra estratificada (por exemplo, 8 casos por estrato com semente nova) somada aos casos de fronteira listados no `dados/extracao/LEIAME.md`. Correções entram por `python3 scripts/grava_codificacao.py`, que substitui a linha do mesmo número. A conferência decide também se as categorias novas (`relacional`, `extorsao_transferencia`, `taxa_antecipada`, `devassa_privacidade`, `falso_relacionamento`, `outro`) ficam ou são fundidas.
2. Capitulação acolhida na sentença e resultado (condenação ou absolvição), campos previstos no produto e ainda não coletados. A `amostra_tjsp.csv` já traz `condena` e `absolve`, indicadores sem conferência calculados sobre o teor da sentença no cjpg, e `cd_doc_cjpg`, mas o teor não foi guardado no repo. Há dois caminhos: reler a sentença pelo cjpg, no navegador, pelo `cd_doc_cjpg`, ou pelo Codex, uma chamada de batch por processo com a sentença no mapa.
3. Portar as melhorias do pipe da conversa (`scripts/pipe_conversa.py`) para `scripts/codex_denuncias.py`: candidata de reserva antes do "Recebida a denúncia", filtro de denúncia nomeada, deduplicação por código PJe, guarda contra folha de inquérito e regras de OCR.
4. Máscara de CPF, RG, telefone e endereço para a versão de circulação, quando o usuário decidir.
5. Fase 2 (TJPA), a replanejar. Convém testar se a consulta de julgados do TJPA permite a mesma busca textual.

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
- No Project "Criminologia Informática" do claude.ai, o doc `claude/plano-captura-base-tjpa.md` espelha o estado da coleta, e o `claude/matriz-selecao-casos.md` resume a matriz de 29 casos para exame criminológico (documento editável em https://claude.ai/artifact/4rUKtiqaqKiia9LUKqGm3Y), que convém usar para ordenar a coleta das sentenças do passo 2.
