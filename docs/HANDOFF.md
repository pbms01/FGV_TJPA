# Handoff: fase 1 TJSP, amostra e extração fechadas (20/11/2026, noite)

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

Extração: `python scripts/extrai_denuncias.py` gera `dados/extracao/denuncias_tjsp.csv` (200 linhas, cerca de 72 colunas) e `dados/extracao/segmentos/<numero>.json` (cota, narrativa, capitulação). As regras, a validação e as decisões estão em `dados/extracao/LEIAME.md`, a leitura obrigatória antes de mexer na extração.

## Decisões tomadas

- Pós-estratificação pela capitulação da própria denúncia (`tipo_capitulacao`), cruzada com o estrato de origem, porque o estrato veio da sentença.
- A unidade principal é a denúncia sem duplicatas (`duplicata_de`), com o peso do processo. Há duas duplicatas: INV 7 repete INV 2, e INV 3 repete INV 32. O denunciado é a unidade secundária e depende de codificação manual.
- Dados pessoais sem máscara nesta fase, por decisão do usuário ("não vamos por ora mascarar"). O `scripts/extrai_inicio.py` mascara, mas não está em uso.
- Correções manuais conferidas em outra peça ficam no dicionário `CORRECOES` do script. Por ora há só o INV 35, cuja capitulação diz 155-A e cuja sentença lê 154-A.
- INV 22 foi relido pela cópia de 2025 (OCR), porque o texto nativo do PJe termina na página 16 de 24.

## Resultados até aqui

Distribuição pela capitulação, sem duplicatas e com peso dentro do estrato:

| Estrato | Denúncias | Distribuição |
| --- | --- | --- |
| INV | 34 | 154-A 85,3% |
| CL | 50 | 171 §2º-A 47,3%; 171 sem §2º-A 27,8%; 155 §4º-B 10,7% |
| FE | 114 | 171 §2º-A 86,3%; 171 sem §2º-A 10,8% |

Nenhuma denúncia capitula o 171 §2º, VII.

Achados da codificação manual de 36 denúncias:

- Em 22 das 24 denúncias CL e FE codificadas, o denunciado é o titular da conta recebedora, sozinho ou também como executor.
- No INV, 7 das 34 denúncias (5 das 29 no 154-A) têm contexto de violência doméstica (coluna `contexto_vd`), sem nenhuma nos outros estratos.

A validação das regex fora da amostra (rodada r2, 12 casos) deu concordância de 0,83 a 1,00 (`dados/extracao/validacao_regex.csv`). `m_pix` e `m_boleto` medem menção, não meio de pagamento.

## Próximos passos, em ordem

1. Codificação assistida de artifício, meio e papel do denunciado nas 164 denúncias ainda não codificadas, por leitura caso a caso e em lotes por estrato. O formato é o de `dados/extracao/codificacao_manual_r1.csv`, com as mesmas colunas e o mesmo vocabulário de `artificio` e `papel_denunciado`.
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
- No Project "Criminologia Informática" do claude.ai, o doc `claude/plano-captura-base-tjpa.md` espelha o estado da coleta.
