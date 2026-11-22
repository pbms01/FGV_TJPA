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

- Limite do Codex. Duas respostas de "limite de consultas por minuto" nesta sessão, a primeira com chamadas em paralelo e a segunda já com chamadas em série, pausas de 8 a 10 s entre elas e 30 s entre processos. A mensagem diz que o serviço é para consultas pontuais, não para automação, raspagem em lote ou extração massiva, e que o uso inadequado pode levar à suspensão da conta. A coleta parou aqui por cautela, a pedido do usuário. Antes de retomar, decidir o ritmo (uma chamada por vez, com o intervalo de 40 s do roteiro entre processos e mais espaço entre chamadas do mesmo processo) ou pedir limite maior ao suporte, e considerar fechar só o grupo 1.
- Sigilo cresce: 8 de 30 (27%), contra 19 de 225 no TJPA. Os dois números de órgão 0601 tratados estavam em sigilo (0802538-82.2025 e 0803746-04.2025; o DJEN os dá como varas criminais da Capital). Chamar a visão geral sozinha primeiro, porque o sigilo responde em uma chamada e poupa as demais.
- DCP do Juizado de Violência Doméstica (0001060-58.2023.8.19.0014, rótulo INV): sem movimento de recebimento da denúncia, e a "Petição Inicial.pdf" do tipo "Petição Inicial/Doc. de Origem" é a denúncia, como nos demais DCP; a classe do Codex é Inquérito Policial.
- DCP antigo sem texto em todo o processo (0009844-84.2019.8.19.0007, Barra Mansa, 462 documentos): a lista marca "[sem texto indexado: leitura mais lenta]" e a leitura em lote devolve "(sem conteudo)" para a denúncia, a cota e a sentença. Gravado como `sem_texto`, com os IDs na nota, para a segunda passada pelo original (`pdpj_get_documento_url`, como nos acórdãos do TJPA). O julgamento aparece no filtro "Conclus", não em "Julgado".
- Capitulação divergente entre denúncia e sentença: 0964662-37.2023.8.19.0001 foi denunciado por extorsão (art. 158, §1º) e condenado no art. 171, §2º, VII; fica para a extração conferir a precisão do recorte.
- O leitor do dispositivo pegou a linha das despesas processuais em 0816832-93.2025.8.19.0002 ("Condeno ao réu, outrossim, ao pagamento das despesas"): o filtro do `grava` exclui "custas" e "honor", mas não "despesas"; corrigir na extração, sem mexer na coleta.
