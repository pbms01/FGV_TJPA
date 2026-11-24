# Fase 3: TJRJ pela API do DJEN e pelo Codex

Versão 0.1, de 22/11/2026. O produto é o das fases 1 e 2: o máximo de denúncias com a descrição da conduta e a capitulação dada pelo MP, com a sentença quando houver, agora no TJRJ, gravadas como texto lido, sem baixar a peça e sem pseudonimização, para comparação campo a campo com o TJSP e o TJPA. O desenho repete o do TJPA (`docs/RUNBOOK_TJPA.md`): lista de alvos pela busca textual do DJEN, leitura das peças pelo Codex, censo e não amostra. Este roteiro registra só o que muda.

## Sondagem (22/11/2026)

| Fonte | O que se viu | Papel |
| --- | --- | --- |
| eJuris (www3.tjrj.jus.br/ejuris) | Bases de 2ª instância, alçadas, turma recursal e Conselho da Magistratura; nenhuma de 1º grau | Complemento para apelações anteriores à janela do DJEN |
| API pública do DJEN | Responde para `siglaTribunal=TJRJ` pelo navegador embutido, com a mesma semântica do TJPA | Porta de entrada |
| Codex | Abre processos dos três sistemas do TJRJ (PJe, DCP e eJUD) | Leitura das peças |
| DataJud | Não consultado nesta fase | Denominador, se a análise pedir |

A diferença decisiva é a janela. Pelo Aviso TJ 347/2024, complementado pelo Aviso TJ 372/2024, o DJEN passou a ser o meio único de publicação dos atos processuais do TJRJ nos sistemas DCP, PJe e eJUD a partir de 11/11/2024; antes disso o tribunal publicava no DJERJ. A série de controle confirma: "estelionato" tem 0 publicações de 2020 a 2023, 562 em 2024 e 7.031 em 2025, e "fraude eletrônica", 6 em 2024 e 300 em 2025. No TJPA a série começava em 2022. Consequência: entram os processos com algum ato publicado desde novembro de 2024, inclusive processos antigos que tiveram ato nesse período (há números de 2006 a 2021 na lista); ficam fora os processos encerrados antes disso sem ato posterior. A sentença anterior a novembro de 2024 só entra pela apelação, cujo número é o de origem.

Sistemas, pelo número e pelo Codex: o número 08xxxxx ou 09xxxxx é PJe (competência criminal no PJe desde 18/07/2022, depois do piloto de Resende de 2022); o 00xxxxx ou 01xxxxx é DCP, migrado ou não, ou eJUD no segundo grau. A apelação criminal tramita no eJUD com o número de origem e traz, no dossiê, as peças do primeiro grau (644 documentos no 0003460-60.2021.8.19.0064).

## Consultas e lista de alvos

As mesmas frases e rótulos do TJPA (FE, FE_amp, INV, CL, EE), pelo `scripts/djen_navegador.js` carregado na aba do comunica.pje.jus.br, com `djen.iniciar({tribunal: 'TJRJ', inicio: '2024-01-01', fim: '2026-11-21'})`. Publicações de 01/01/2024 a 21/11/2026:

| Frase | Publicações |
| --- | --- |
| "fraude eletrônica" | 977 |
| "171, § 2º-A"; "art. 171, § 2º-A" | 322; 104 |
| "invasão de dispositivo informático" | 92 |
| "conta laranja"; "contas laranja"; "contas laranjas"; "cessão de conta"; "cessão de contas" | 25; 8; 12; 11; 3 |
| "estelionato eletrônico" | 63 |
| União | 1.366 publicações distintas |

Por rótulo, em processos: FE 109 ações penais e 67 apelações; FE_amp 72 e 61; INV 20 e 8; CL 14 e 2; EE 21 e 8.

`dados/djen/alvos_djen_tjrj.csv` (mesmos campos do TJPA) tem 302 números criminais: 281 de ação penal ou apelação criminal (205 ações penais e 97 apelações, 76 só como apelação), 108 com sentença publicada no DJEN, 10 inquéritos e 15 autos de prisão em flagrante. Totais em `dados/djen/totais_tjrj.json`. Pelo estrato da fase 1 (INV, depois CL, depois FE): 238 FE, 27 INV e 16 CL. Pelo sistema: 211 PJe e 70 DCP ou eJUD. A capital (0001) tem 93; nenhum número de apelação termina em 0000. Ficam fora 142 habeas corpus, 9 recursos em sentido estrito, os pedidos cautelares e os processos cíveis que casam com as frases (355 de procedimento comum, 109 de juizado especial cível, 105 apelações cíveis).

Fila em `dados/codex_tjrj/fila.csv`, semente 20261122: grupo 1, 186 processos com sentença publicada ou apelação; grupo 2, 95 ações penais restantes. Os inquéritos e flagrantes ficam fora, como no TJPA.

## Onde está a denúncia, por sistema

| Sistema | Caso testado | Denúncia | Sentença |
| --- | --- | --- | --- |
| PJe | 0849853-63.2025.8.19.0001 (17ª Vara Criminal da Capital) | "Ajuizamento de Ação.pdf", tipo "Petição Inicial", juntada no próprio inquérito, que mantém o número e a classe Inquérito Policial no Codex (como no TJPA); texto nativo; o MPRJ abre com "vem oferecer DENÚNCIA ... pela prática da seguinte conduta delituosa" | Tipo "Sentença" (a confirmar na coleta) |
| DCP migrado | 0021684-28.2018.8.19.0007 (2ª Vara de Barra Mansa, Operação Open Doors II) | "NNNNN-NN - Tipo: Denúncia.pdf", tipo "Denúncia" (71 mil caracteres), com a "Cota de oferecimento da denúncia" ao lado, entre os documentos mais antigos | A confirmar |
| eJUD (apelação) | 0003460-60.2021.8.19.0064 (Valença) | "... - Denúncia - Ajuizamento de Ação - denúncia.pdf", sem texto indexado; a leitura devolveu "Texto do documento indisponível" | "Despacho / Sentença / Decisão.pdf", nome comum a todo ato do juiz; a de mérito se distingue pelo tamanho (65 mil caracteres) e pelo movimento |

Regras de localização, acrescidas às do TJPA:

1. PJe: documento do tipo "Petição Inicial" ou "Denúncia" posterior ao relatório do inquérito; "Ajuizamento de Ação" no nome é a marca do MPRJ.
2. DCP: documento cujo nome tem "Tipo: Denúncia"; a cota vai como parte da denúncia, como na fase 1.
3. eJUD: denúncia pelo nome; sem texto, tentar de novo uma vez e, persistindo, `sem_texto` para a segunda passada. A sentença sai do movimento de julgamento e, no mapa, dos "Despacho / Sentença / Decisão" com mais de 8 mil caracteres (`TRIB=tjrj` no `pipe_tjpa.py`).
4. Sigilo: três de sete processos testados estavam sob sigilo no Codex. A perda por sigilo deve ser maior que no TJPA (19 de 225) e entra na tabela de perdas.

## Operação

O condutor é o mesmo da fase 2, `scripts/pipe_tjpa.py`, agora parametrizado: `TRIB=tjrj python3 scripts/pipe_tjpa.py prox|sel|grava|status|nota|mapa|resumo`. Sem `TRIB`, roda o TJPA como antes. Textos em `textos/tjrj/denuncias/` e `textos/tjrj/sentencas/`, manifesto em `textos/tjrj/manifesto.csv`, status em `dados/codex_tjrj/status.csv`. Ritmo e regras de nota do TJPA: 40 s entre processos, a vara de `orgao_1g` (vazio nas 76 só apelação, que se preenche pela vara de origem lida no dossiê), classe do Codex sem valor de decisão, famílias de desmembramento pelo md5.

## Vieses e ressalvas

- Janela de dois anos (11/2024 a 11/2026), contra quase cinco no TJPA: o conjunto favorece processos com movimento recente e subestima os julgados antes de novembro de 2024, salvo os apelados.
- O DJEN só traz ato com intimação publicada; o teste de cobertura contra o DataJud ou o Codex segue pendente nos dois tribunais.
- Entram ações penais sem sentença (97 das 205), como no TJPA.
- A frase casa citação: a precisão se mede na capitulação lida.

## Extensões possíveis, fora desta coleta

- eJuris, base de 2ª instância, com as mesmas frases e filtro criminal, para trazer apelações de sentenças anteriores a novembro de 2024; os números levam ao dossiê do eJUD, que contém a denúncia e a sentença do primeiro grau.
- Os 10 inquéritos e 15 flagrantes da lista, pela regra de seleção do `docs/plano-captura.md`.

## Estado da coleta (22/11/2026)

Coleta iniciada pelo grupo 1, com o condutor parametrizado: 5 processos tratados, 4 com denúncia e sentença gravadas e 1 em sigilo, em 16 chamadas. Retomar com `TRIB=tjrj python3 scripts/pipe_tjpa.py prox`.

| Processo | Sistema | Denúncia | Sentença |
| --- | --- | --- | --- |
| 0825457-23.2024.8.19.0206 | (sigilo) | | |
| 0835222-17.2025.8.19.0001 | eJUD com número PJe | "Ajuizamento de Ação.pdf"; art. 155, §4º, II, c/c §4º-B e §4º-C, II | Procedência em parte, 11/08/2026 |
| 0804129-35.2023.8.19.0024 (Itaguaí) | PJe | Peça inicial "DEN 171 CP"; art. 171, §2º-A | Condena a 1 ano em aberto (embargos acolhidos em 28/10/2025, não lidos) |
| 0855318-39.2025.8.19.0038 | PJe, autos importados de 2023 | "Petição Inicial.pdf"; art. 171, §2º-A, c/c §2º-B | Procedência parcial, 19/10/2026, pelo movimento |
| 0803193-07.2024.8.19.0046 (Rio Bonito) | eJUD com número PJe | "Ajuizamento de Ação.pdf", juntada como petição sob sigilo; art. 171, §2º-A e §4º | Procedência em parte, 10/12/2024; acórdão de 16/04/2025 não lido |

Lições dos primeiros cinco:

- O condutor ganhou duas regras do TJRJ no `mapa`: "Ajuizamento de Ação" no nome é denúncia, e "Despacho / Sentença / Decisão" com mais de 8 mil caracteres é candidata a sentença.
- O movimento "Recebida a denúncia" aparece no mapa do PJe; a juntada da denúncia aparece como "Juntada de Petição de Sob sigilo", como no TJPA.
- Custo de contexto: o mapa de um dossiê de 280 a 330 documentos às vezes cabe na resposta e entra inteiro na conversa (até 25 mil tokens). Para economizar, preferir: `pdpj_visao_geral_processo`; `pdpj_list_movimentos(tipo_filter="cedência", limit=5)` para a sentença; `pdpj_list_documentos(limit=30, offset=total-30)` para as primeiras peças; e o mapa só quando a denúncia não aparecer na janela. Em sessão longa, a coleta inteira (cerca de 280 processos) pede mais de uma conversa.

## Lições dos processos 6 a 19 (22/11/2026)

Estado: 19 tratados (14 com denúncia e sentença ou só denúncia, 1 só com sentença, 3 em sigilo, 1 sem denúncia), 86 chamadas registradas, cerca de 4,5 por processo, quase o dobro do TJPA.

- DCP e dossiês do eJUD de processo DCP: a denúncia é a "Petição Inicial.pdf" do tipo "Petição Inicial/Doc. de Origem", o documento mais antigo da lista (`offset` = total menos 2), às vezes com a "COTA DEN" ao lado. O julgamento aparece como movimento "Conclusão" com a descrição "Julgado procedente o pedido" (o filtro por tipo "cedência" não o acha; usar `tipo_filter="Conclus"`); o documento do movimento gêmeo é só a capa "Conclusão ao Juiz" (cerca de 400 caracteres), e a sentença é o "Despacho / Sentença / Decisão.pdf" juntado logo depois, às vezes repetido com os mandados de intimação. Às vezes a lista marca o tipo "(Sentença)".
- PJe: a denúncia ("Ajuizamento de Ação.pdf", "Petição Inicial", "Den. 171 ...") vem depois das peças numeradas do inquérito e logo antes da decisão de recebimento; o movimento "Recebida a denúncia" dá a posição. Em flagrante, a denúncia pode estar entre as "Petição de Sob sigilo" anteriores ao recebimento.
- "Sentença.html" pode dizer só "Sentença em anexo"; o texto está no anexo do mesmo dia ("PJE - Sentença - ....pdf", tipo Outros Anexos). O condutor agora rejeita documento com menos de 200 caracteres úteis ou "(sem conteudo)".
- Dossiês no STJ (AREsp, sistema SIAJ) abrem no Codex com as peças do 1º grau.
- Classe do DJEN não garante ação penal: 0034414-11.2026 era pedido de prisão preventiva extinto por litispendência (`sem_denuncia`).
- Denúncia sem texto indexado no DCP antigo (0069207-15.2022) volta "(sem conteudo)": `so_sentenca`, para a segunda passada.

## Lições dos processos 20 a 30 (22/11/2026)

Estado: 30 tratados, todos do grupo 1 (19 `ok`, 8 `sigilo`, 1 `so_sentenca`, 1 `sem_denuncia`, 1 `sem_texto`), 129 chamadas registradas. Próximo da fila: 0000096-45.2019.8.19.0066 (ordem 31), apelação no eJUD de processo DCP de Volta Redonda, com 327 documentos; a visão geral já foi lida e o processo não tem status gravado.

- Limite do Codex. Duas respostas de "limite de consultas por minuto" nesta sessão, a primeira com chamadas em paralelo e a segunda já com chamadas em série, pausas de 8 a 10 s entre elas e 30 s entre processos. A mensagem diz que o serviço é para consultas pontuais, não para automação, raspagem em lote ou extração massiva, e que o uso inadequado pode levar à suspensão da conta. A coleta parou aqui por cautela, a pedido do usuário. Por decisão do usuário, as consultas ficam suspensas por 24 horas, até 23/11/2026, 17h30 UTC (14h30 em Brasília). Antes de retomar, decidir o ritmo (uma chamada por vez, com o intervalo de 40 s do roteiro entre processos e mais espaço entre chamadas do mesmo processo) ou pedir limite maior ao suporte, e considerar fechar só o grupo 1.
- Sigilo cresce: 8 de 30 (27%), contra 19 de 225 no TJPA. Os dois números de órgão 0601 tratados estavam em sigilo (0802538-82.2025 e 0803746-04.2025; o DJEN os dá como varas criminais da Capital). Chamar a visão geral sozinha primeiro, porque o sigilo responde em uma chamada e poupa as demais.
- DCP do Juizado de Violência Doméstica (0001060-58.2023.8.19.0014, rótulo INV): sem movimento de recebimento da denúncia, e a "Petição Inicial.pdf" do tipo "Petição Inicial/Doc. de Origem" é a denúncia, como nos demais DCP; a classe do Codex é Inquérito Policial.
- DCP antigo sem texto em todo o processo (0009844-84.2019.8.19.0007, Barra Mansa, 462 documentos): a lista marca "[sem texto indexado: leitura mais lenta]" e a leitura em lote devolve "(sem conteudo)" para a denúncia, a cota e a sentença. Gravado como `sem_texto`, com os IDs na nota, para a segunda passada pelo original (`pdpj_get_documento_url`, como nos acórdãos do TJPA). O julgamento aparece no filtro "Conclus", não em "Julgado".
- Capitulação divergente entre denúncia e sentença: 0964662-37.2023.8.19.0001 foi denunciado por extorsão (art. 158, §1º) e condenado no art. 171, §2º, VII; fica para a extração conferir a precisão do recorte.
- O leitor do dispositivo pegou a linha das despesas processuais em 0816832-93.2025.8.19.0002 ("Condeno ao réu, outrossim, ao pagamento das despesas"): o filtro do `grava` exclui "custas" e "honor", mas não "despesas"; corrigir na extração, sem mexer na coleta.

## Lições dos processos 31 a 45 (22/11/2026, noite)

Estado: 45 tratados, todos do grupo 1 (30 `ok`, 9 `sigilo`, 2 `so_sentenca`, 1 `sem_denuncia`, 3 `sem_texto`), 203 chamadas registradas. Próximo da fila: ordem 46 (`prox`).

- Ritmo. A coleta foi retomada às 19h30 (Brasília) do mesmo dia, por decisão do usuário, antes do fim da suspensão de 24 horas, com uma chamada por vez, cerca de 15 s entre chamadas e 40 s entre processos. Em 15 processos e cerca de 74 chamadas não houve novo aviso de limite. Manter esse ritmo; se o aviso voltar, parar e tentar de novo às 3h30 de Brasília, conforme a instrução do usuário.
- DCP antigo sem texto: três processos de 2019 e 2021 (0009844-84.2019.8.19.0007, 0000096-45.2019.8.19.0066 e 0004316-29.2021.8.19.0030) têm todos os documentos marcados "[sem texto indexado: leitura mais lenta]". Testar só a denúncia com `max_chars_por_doc=600`; voltando "(sem conteudo)", gravar `sem_texto` sem procurar a sentença. Custo: 3 ou 4 chamadas, contra 8 da primeira vez.
- DCP com documentos recentes de 0 caracteres: em 0023749-06.2021.8.19.0002 a denúncia antiga tinha texto, mas a sentença de 2026 voltou vazia; gravado como `ok` só com a denúncia, com nota para a segunda passada da sentença.
- DCP: a "Petição Inicial/Doc. de Origem" nem sempre é a denúncia. Em 0003462-30.2021.8.19.0064 (Valença) era a peça do inquérito; o `grava` a rejeitou e o processo ficou `so_sentenca`.
- Filtro "Conclus": o julgamento pode estar na segunda página (`offset=10`), como em 0013763-13.2021.8.19.0007.
- PJe: quando o movimento "Recebida a denúncia" tem número baixo, listar as 35 primeiras peças. Se a janela mostrar só peças numeradas do inquérito, a denúncia está logo antes da decisão de recebimento na ordem da lista, não entre as peças do IP: em 0801112-17.2024.8.19.0004 ela estava na posição 129 de 267, junto da decisão (posição 130), e só apareceu no mapa, depois de três listas. Melhor do que o mapa (cerca de 25 mil tokens de contexto) é buscar a decisão de recebimento pela lista, perto de `offset = total - posição da decisão`.
- Classes do Codex sem valor de decisão: Pedido de Prisão Preventiva (0803195-74.2024.8.19.0046) e Auto de Prisão em Flagrante (0864282-98.2026.8.19.0001) com a ação penal no mesmo número; a denúncia vem como "Ajuizamento de Ação.pdf" do tipo "Denúncia (Outras)".
- O `grava` aceita o resultado persistido em `.json` (formato `toolu_...json`) além do `.txt`.

## Segunda passada (23/11/2026)

- `pdpj_perguntar_processo` localiza a peça em uma chamada ("Qual documento é a denúncia oferecida pelo Ministério Público? Informe o ID, a data de juntada e a capitulação"), lendo 1 a 3 documentos do processo e devolvendo o ID; depois se lê a peça pelo lote normal. Resolveu a denúncia de 0003462-30.2021.8.19.0064 (posição 35 de 324, "... - Denúncia - IP 01518-2021_Art. 171, caput e §2º-A CP") e o anexo "PJE - Sentença" de 0864686-23.2024.8.19.0001 (4 anos e 8 meses, semiaberto). Não acha peça sem texto: em 0023749-06.2021.8.19.0002 respondeu que nenhuma sentença foi lida.
- 0069207-15.2022.8.19.0001: as duas decisões gravadas são condenatórias e iguais salvo a capitulação; a de 02/04/2025 acrescenta o §2º-A e é a definitiva. A denúncia 2ffdbf47 segue sem texto.
- Originais pelo `pdpj_get_documento_url`: o link baixa pelo `curl` do workspace, mas para as peças do TJRJ (DCP e eJUD, 2019 a 2026) o servidor respondeu 503 ("O sistema de origem está instável") em todas as tentativas, ao longo de cerca de 15 minutos: 0000096-45.2019 (a87bc7e8), 0004316-29.2021 (a8d472a6) e 0023749-06.2021 (6cf8c0d5). Ficam pendentes, com 0009844-84.2019 (6560b840, ebcc8efa, 09c34132) e a denúncia de 0069207-15.2022 (2ffdbf47), para nova tentativa em outro dia.
- O texto do original entra no repositório pelo `scripts/original_para_lote.py`, que monta um lote no formato do Codex (camada de texto pelo `pdftotext`, OCR pelo `tesseract` quando a camada falta, HTML sem marcação) para o `grava ARQUIVO`; o PDF fica em `/tmp`, fora do repositório, e o manifesto registra a procedência ("parser pdftotext do original", "OCR tesseract do original" ou "parser HTML do original").

## Processos 46 a 50 (23/11/2026)

Estado: 50 tratados, todos do grupo 1 (33 `ok`, 11 `sigilo`, 2 `so_sentenca`, 1 `sem_denuncia`, 3 `sem_texto`), 215 chamadas registradas. Próximo da fila: ordem 51 (`prox`).

- Roteiro novo, mais barato em chamadas e em contexto: visão geral; movimento de julgamento (`tipo_filter="cedência"`, ou "Conclus" no DCP); `pdpj_perguntar_processo` com "Qual documento é a denúncia oferecida pelo Ministério Público? Informe o ID do documento, a data de juntada e a capitulação pedida."; leitura em lote. São 4 chamadas por processo, sem listas de documentos na conversa. No DCP, uma só pergunta pede a denúncia e a sentença de mérito ("Quais documentos são a denúncia ... e a sentença de mérito de primeiro grau? Informe o ID de cada um ..."), e a resposta aponta a peça mesmo quando não a lê (seção "PECAS NAO LIDAS").
- Repetição no lote: com tamanhos desconhecidos, 4 a 5 repetições bastam para o resultado ir a arquivo; as 15 que o `sel` propõe geram até 700 mil caracteres sem necessidade.
- Terceiro número de órgão 0601 em sigilo (0809777-40.2025); a regra se confirma.
- 0000185-66.2022.8.19.0065 (Vassouras): emendatio libelli, de 171, §2º-A, para 171, caput; a denúncia ea014f4c não tem texto no Codex e o original deu 503.

## Processos 51 a 72 (23/11/2026, tarde)

Estado: 72 tratados, todos do grupo 1 (46 `ok`, 16 `sigilo`, 6 `so_sentenca`, 1 `sem_denuncia`, 3 `sem_texto`), 286 chamadas registradas. Neste lote, 22 processos em 71 chamadas (13 `ok`, 4 `so_sentenca`, 5 `sigilo`), com o roteiro de 4 chamadas e sem aviso de uso em lote. Próximo da fila: ordem 73 (`prox`), 0180954-67.2022.8.19.0001, eJUD de processo DCP do I Juizado de Violência Doméstica da Capital, INV, público, 194 documentos; a visão geral e uma pergunta já foram gastas nele (2 chamadas sem registro no status).

- Cota diária do `pdpj_perguntar_processo`: no 73 o Codex respondeu "Voce atingiu o limite de 30 analises automaticas por dia", com a cota zerada no dia seguinte; visão geral, mapa e `pdpj_read_documento` não entram no limite. Como a pergunta é a terceira chamada do roteiro e os sigilos não a gastam, o roteiro rende cerca de 30 processos não sigilosos por dia, somadas as perguntas de todas as sessões (a segunda passada e os processos 46 a 50 gastaram parte da cota de 23/11). Esgotada a cota, ou se espera o dia seguinte ou se volta às listas de documentos (`tipo_filter` e `offset`, seção "Lições dos processos 6 a 19"), que custam mais chamadas e mais contexto.
- Repetições no lote: com a denúncia vazia e a sentença curta, 5 repetições ficaram abaixo do limiar de gravação em arquivo, e o lote do 72 (27 mil caracteres) entrou inteiro na conversa. Nesse caso o `grava ultimo` pegaria o arquivo do processo anterior; o certo foi refazer a leitura só com a sentença, repetida 25 vezes, e passar o caminho do arquivo ao `grava`. Quando a denúncia for peça do DCP com prefixo numérico longo ("2021001016... - Denúncia.pdf"), que tende a vir sem texto, usar 15 repetições, como o `sel` propõe.
- Denúncia sem texto no Codex, padrão do DCP: nos quatro `so_sentenca` do lote a denúncia é a peça do DCP com prefixo numérico ("... - Denúncia - Ajuizamento de Ação.pdf", "... - Denúncia.pdf") e voltou "(sem conteudo)", como em 0000185-66.2022.8.19.0065. A capitulação está na nota, lida da sentença. Entram na segunda passada pelo original: 0126752-43.2022.8.19.0001 (ec3d34ec-6861-513e-812b-41dbe813a384), 0093789-21.2018.8.19.0001 (df1418fc-3bbb-5a0f-aaab-a4ad6f6c700f), 0003460-60.2021.8.19.0064 (193ae021-21b6-54e4-af1f-fc90f6f7a1a4) e 0020478-63.2021.8.19.0042 (bac9e0fa-09e5-571b-a45b-4d59d7f7cf4e).
- Sigilo: o órgão 0601 nem sempre está em sigilo (0805131-84.2025 e 0820078-46.2025 públicos, 0802603-77.2025 em sigilo). Em sigilo também os dois PJe da 2ª Vara Criminal de Cabo Frio (0805491-77.2024 e 0812642-94.2024), o de Itaguaí (0804894-06.2023) e o INV do Juizado de Violência Doméstica de Niterói (0112465-07.2024); o INV do Juizado da Capital (73) é público pelo eJUD.
- Classes do Codex sem valor de decisão: Recurso Extraordinário com Agravo no STF (0849060-27.2025.8.19.0001, 713 documentos, com partes de outro processo misturadas na lista), Inquérito Policial (0820078-46.2025 e 0813311-84.2023) e Auto de Prisão em Flagrante (0020478-63.2021), todos com a ação penal no mesmo número.
- Denúncia com outro número CNJ no cabeçalho: 0849060-27.2025 (originário 0843245-20.2023.8.19.0001) e 0808468-13.2022.8.19.0011 ("cópia denúncia 02477581720228190001.pdf", da Capital). Na extração, conferir se a regex `8\.19`, que corta peça de outro processo anexada, não corta essas denúncias.
- Para a extração: 0805131-84.2025 condena no art. 171, §4º, contra a denúncia por furto mediante fraude (155, §4º-B); 0809409-82.2025 desclassifica (denúncia no 171, caput); 0003460-60.2021 tem duas sentenças condenatórias que diferem na fundamentação (provável republicação; tomar a de 11/08/2025, a conferir); 0093789-21.2018 é INV com a Oi S.A. como assistente de acusação (154-A, caput e §3º, e 288).
- Push: a sessão começou com o repositório só para leitura (o anexo com push foi negado duas vezes pelo controle de permissões), fez os commits localmente e só os enviou ao main depois do pedido expresso do usuário, já rebaseados sobre o trabalho de outra sessão.

## Processos 73 a 80 (24/11/2026)

Estado: 80 tratados, todos do grupo 1 (51 `ok`, 18 `sigilo`, 6 `so_sentenca`, 1 `sem_denuncia`, 4 `sem_texto`), 311 chamadas registradas. Neste lote, 8 processos em 25 chamadas (5 `ok`, 2 `sigilo`, 1 `sem_texto`), com 6 perguntas da cota diária e sem aviso de limite. Próximo da fila: ordem 81 (`prox`).

- Processo todo sem texto, sinal na pergunta: em 0180954-67.2022.8.19.0001 (eJUD de processo DCP do Juizado de Violência Doméstica da Capital) a pergunta respondeu "Documentos lidos: 0 de 194" e só listou candidatas; as três voltaram "(sem conteudo)" no lote, gravado como `sem_texto`. Quando a pergunta não ler nenhum documento, testar uma das candidatas com `max_chars_por_doc=600` e uma repetição antes de montar o lote (lote vazio de 30 itens entra inteiro na conversa).
- A peça do DCP com prefixo numérico nem sempre vem vazia: em 0018198-72.2022.8.19.0014 (Campos) a "202200101620000219 - Denúncia - Ajuizamento de Ação.pdf" tinha texto. O sinal útil é a pergunta: se ela leu a peça, o lote também lê.
- Dossiê no STJ (AREsp, SIAJ) com a ação penal PJe da Capital dentro: 0924511-29.2023.8.19.0001, roteiro normal.
- Falso positivo da frase do DJEN: 0844793-77.2023.8.19.0002 é ação por roubo majorado (art. 157, §2º, II, e §2º-A, I), gravada como `ok`; a sentença absolve do roubo e descreve golpe de triangulação, com o pagamento desviado a terceira pessoa e o acusado e a vítima enganados ("cenário de evidente fraude eletrônica, incompatível com a narrativa de roubo"). Interessa à questão do intermediário; a extração deve marcá-la fora do recorte da capitulação.
- Sigilo: DCP da 2ª Vara Criminal de Resende (0003937-43.2021) e PJe da 2ª Vara Criminal de Nova Friburgo (0812552-71.2025).

## Processos 81 a 105 (24/11/2026)

Estado: 105 tratados, todos do grupo 1 (69 `ok`, 24 `sigilo`, 7 `so_sentenca`, 1 `sem_denuncia`, 4 `sem_texto`), 393 chamadas registradas. Neste lote, 25 processos em 82 chamadas (18 `ok`, 1 `so_sentenca`, 6 `sigilo`), com 20 perguntas da cota diária (26 das 30 do dia, somadas as 6 do lote 73 a 80) e sem aviso de uso em lote. Próximo da fila: ordem 106 (`prox`), 0868152-25.2024.8.19.0001. Conferência do lote entre status, arquivos e manifesto: sem divergência.

- Sentença em audiência: em 0908048-75.2024.8.19.0001 (27ª Vara Criminal da Capital) o documento do movimento Procedência ("Sentença.html", 741 caracteres) só diz que "o texto da sentença está disponível no documento Ata da Audiência", a ata do movimento Audiência diz "em anexo", e o texto está na "Assentada ... - Leit Sent.pdf", juntada no mesmo dia. O `grava` aceitou o aviso como sentença, porque passa de 200 caracteres. Sinal: o `wc -c` da sentença gravada abaixo de mil caracteres e o "dispositivo não localizado". Conserto, que custou 5 chamadas a mais (9 no processo): segunda pergunta ao `pdpj_perguntar_processo` pedindo o documento com o texto da sentença proferida em audiência, nova leitura em lote e regravação. O filtro "cedência" não mostra o movimento "Julgamento | Sentença em Audiência", que só aparece na lista sem filtro, ao lado do "Procedência"; em vara que sentencia em audiência, a pergunta dupla do DCP (denúncia e sentença de mérito) no lugar da pergunta da denúncia tende a achar a assentada na mesma chamada, o que ainda não foi testado.
- Mais de um registro da mesma peça: em 0003464-97.2021.8.19.0064 (2ª Vara de Valença) a pergunta devolveu dois registros da denúncia, de mesmo sha256, e três de sentença. O lote foi lido com os cinco, inspecionado por tamanho e sha256 antes do `grava`, e o `sel` refeito só com os distintos (o `sel` só regrava a seleção corrente e pode ser repetido depois da leitura).
- Repetições: com tamanhos desconhecidos, 5 a 8 repetições de denúncia e sentença foram a arquivo em todos os processos; o menor lote teve 59 mil caracteres (5 repetições, denúncia de 8 mil e o aviso de sentença em audiência) e foi a arquivo com prévia de 2 KB. Em processo grande (0018079-77.2007, 0840224-22.2023, 0804963-97.2025 e 0032854-39.2023), 4 a 8 repetições geraram de 0,8 a 1,5 milhão de caracteres; com muitos réus ou mais de mil documentos na visão geral, 3 repetições bastam.
- DCP, pergunta dupla: leu a denúncia e a sentença em 0004897-62.2023.8.19.0066 (1º Juizado Especial Criminal de Volta Redonda, INV com violência doméstica), 0003464-97.2021.8.19.0064, 0018079-77.2007.8.19.0066 (DCP de primeiro grau, 3.202 documentos) e 0032854-39.2023.8.19.0001 (1.394 documentos). Em 0159865-22.2021.8.19.0001 (39ª Vara Criminal da Capital) a denúncia veio em "PECAS NAO LIDAS" e voltou "(sem conteudo)": `so_sentenca`, com a peça e26d52e6-1621-5160-8290-9419c8015280 na segunda passada. Confirma a regra do lote anterior: se a pergunta leu a peça, o lote também lê.
- Fora do recorte da capitulação, gravados como `ok`: 0018079-77.2007.8.19.0066 (lavagem, Lei 9.613/1998, e usura, Lei 1.521/1951; rótulo CL pelo indicador de conta laranja), 0840224-22.2023.8.19.0038 (extorsão, roubo majorado e 288, parágrafo único; rótulo CL; a sentença fala em Pix 16 vezes) e 0804963-97.2025.8.19.0014 (155 §4º, IV, 180 §1º e 288, sem o §4º-B; rótulo FE). A extração deve marcá-los e decidir pelo fato narrado.
- Para a extração: 0003464-97.2021 tem duas sentenças do mesmo juiz com resultados opostos (condena em 06/03/2025, absolve em 16/03/2025 depois de reconhecer a nulidade do reconhecimento pessoal), gravadas como partes 1 e 2, a decidir pelo acórdão; em 0800661-42.2025.8.19.0073 (Guapimirim) o símbolo de parágrafo foi lido como 8 ("155, 84º, IV", "171, 82º-A"); a denúncia de 0018079-77.2007 tem ruído de digitalização; 0814989-66.2025.8.19.0011 condena por estelionato consumado contra denúncia pela forma tentada; 0812609-04.2024.8.19.0206 tem sentença de 18/12/2024 e publicação de sentença no DJEN em 12/06/2025; a denúncia de 0800892-80.2024.8.19.0016 (Carmo) é datada de 01/11/2023, antes do número; 0032854-39.2023 (3ª Vara Especializada em Organização Criminosa, onze réus, Lei 12.850/2013) é material direto da questão 4; o furto mediante fraude eletrônica (155 §4º-B) é a capitulação de 0902168-05.2024, 0858544-03.2024 e 0884193-67.2024, todos da Capital.
- Sigilo (6 de 25): 0009311-73.2025.8.19.0021 (Duque de Caxias, INV), 0822913-07.2025.8.19.0601 (órgão 0601, Nilópolis), 0019680-86.2016.8.19.0007 (DCP, 2ª Vara Criminal de Barra Mansa), 0800974-29.2024.8.19.0011 (terceiro PJe da 2ª Vara Criminal de Cabo Frio em sigilo), 0010286-36.2023.8.19.0031 (Juizado Especial Adjunto Criminal e de Violência Doméstica de Maricá, INV) e 0004297-34.2026.8.19.0002 (Juizado de Violência Doméstica de Niterói, INV, o segundo desse juizado). Público o da 1ª Vara Criminal de Cabo Frio (0814989-66.2025).
- Operação: os CSV de status e de manifesto têm fins de linha mistos (CRLF nas linhas do condutor, LF em algumas antigas), e reescrevê-los inteiros, pelo `csv.writer` ou em modo texto, altera dezenas de linhas antigas no diff. Aconteceu duas vezes neste lote, desfeito por `git checkout` do arquivo e reanexação das linhas novas com `c.anexar`. Correção de nota vai pelo `nota`; para desfazer uma gravação, apagar os arquivos do processo, restaurar o CSV do git e reanexar. Trecho de cabeçalho capturado por `grep` não deve entrar na nota sem conferência (a nota de 0858544-03.2024 saiu com resíduo e foi corrigida por `nota`).
- Push: o anexo com permissão de escrita foi pedido na mensagem inicial do usuário e aceito de primeira; cinco commits de dados no main, um a cada 5 processos, cada qual com `git fetch --depth=50 origin main && git rebase origin/main` antes.
