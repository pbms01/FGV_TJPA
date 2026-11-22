# Fase 4: TJSC pela API do DJEN e pelo Codex

Versão 0.1, de 22/11/2026. O produto é o das fases anteriores: o máximo de denúncias com a descrição da conduta e a capitulação dada pelo MP, com a sentença quando houver, agora no TJSC, gravadas como texto lido, sem baixar a peça e sem pseudonimização, para comparação campo a campo com o TJSP, o TJPA e o TJRJ. O desenho repete o do TJPA e do TJRJ (`docs/RUNBOOK_TJPA.md`, `docs/RUNBOOK_TJRJ.md`): lista de alvos pela busca textual do DJEN, leitura das peças pelo Codex. Este roteiro registra só o que muda. Nesta versão a lista de alvos e a fila estão prontas; o Codex ainda não foi consultado, e a localização da denúncia e da sentença no eproc fica para a sondagem no Codex, que abre a coleta.

## Sondagem (22/11/2026)

| Fonte | O que se viu | Papel |
| --- | --- | --- |
| Pesquisa de jurisprudência (módulo do eproc, www.tjsc.jus.br/web/jurisprudencia) | Acórdãos, decisões monocráticas e despachos ou decisões do TJSC, das Turmas Recursais, das Turmas de Uniformização e do Conselho da Magistratura, com inteiro teor ou só ementa; o manual (atualizado em 06/10/2025) não menciona sentenças de 1º grau | Complemento para apelações, como o eJuris do TJRJ |
| API pública do DJEN | Responde para `siglaTribunal=TJSC` pelo navegador embutido; o inteiro teor vem em HTML com entidades nomeadas, o que muda a busca (abaixo) | Porta de entrada |
| Codex | Não consultado nesta etapa, por decisão do usuário | Leitura das peças |
| DataJud | Não consultado | Denominador, se a análise pedir |

Sistema processual: o eproc foi implantado na competência criminal do 1º grau em 07/10/2019, e a tramitação pelo SAJ se encerrou em 21/01/2021, no 1º e no 2º grau, depois da migração do acervo (notícias do TJSC de 24/09/2019 e de 2021). Todos os 454 números de ação penal ou apelação da lista têm a forma do eproc (5xxxxxx); só um inquérito tem número do SAJ (0305409-25.2017.8.24.0039). A apelação criminal mantém o número de origem (por exemplo 5035333-96.2022.8.24.0038, ação penal e apelação; e 0004245-58.2015.8.24.0075, apelação de processo do SAJ vista na sondagem). Se o inquérito e a ação penal partilham o número, como no TJPA, fica para a sondagem no Codex: há 13 inquéritos na lista e nenhum coincide com número de ação penal.

DJEN: a Resolução TJ n. 5/2021 adotou o DJEN em 21/06/2021, para despachos, decisões, dispositivos de sentença e ementas de acórdão. Para o eproc, porém, as intimações passaram a contar da publicação no DJEN só a partir de 17/03/2025, pela Resolução CNJ 455/2022 (comunicado do TJSC de 12/03/2025). A série de controle mostra que a cobertura de atos decisórios começa de fato em maio de 2025:

| Termo | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 (até 21/11) |
| --- | --- | --- | --- | --- | --- | --- |
| "estelionato" | 20 | 48 | 65 | 77 | 1.590 | 1.797 |

Por mês, "estelionato" tem de 1 a 12 publicações de janeiro de 2024 a abril de 2025, 61 em maio de 2025, 143 em junho, 203 em julho e de 140 a 320 por mês desde então (117 em novembro de 2026, até o dia 21). Na coleta, todas as 152 publicações criminais anteriores a maio de 2025 são editais de citação (tipo "80"); depois disso aparecem as decisões, as sentenças e os acórdãos.

## A diferença decisiva: entidades HTML

No TJSC o campo `texto` vem em HTML com entidades nomeadas (`eletr&ocirc;nica`, `&sect; 2&ordm;-A`), e a busca do DJEN casa a cadeia crua. Em 2025, "fraude eletrônica" devolve 30 publicações e "fraude eletr&ocirc;nica", 74; "171, § 2º-A" devolve 114 e "171, &sect; 2&ordm;-A", 85; no TJPA a forma com entidade devolve 0. A busca não distingue maiúsculas (`FRAUDE ELETR&Ocirc;NICA` dá o mesmo que a minúscula) nem o espaço depois do `&sect;`; a entidade numérica (`&#244;`) quase não aparece (1). Por isso o `scripts/djen_navegador.js` ganhou a opção `entidades: true`, que roda cada frase acentuada também na forma com entidades, com o mesmo rótulo e união pelo `id`, e decodifica o HTML antes dos indicadores `m_*`. Sem a opção, TJPA e TJRJ se reproduzem como antes. A mesma revisão parte ao meio, por data, a janela cuja contagem bate no teto de 10.000; nesta coleta nenhuma janela precisou ser partida.

Variante deixada de fora, para manter as frases iguais às dos outros tribunais: "171, &sect; 2&deg;-A" (grau em vez de ordinal), 28 publicações em todo o período.

## Consultas e lista de alvos

`djen.iniciar({tribunal: 'TJSC', inicio: '2020-01-01', fim: '2026-11-21', entidades: true})`. Publicações de 01/01/2020 a 21/11/2026, forma acentuada e forma com entidades:

| Rótulo | Frase | Acentuada | Com entidades |
| --- | --- | --- | --- |
| FE | "fraude eletrônica" | 88 | 625 |
| FE_amp | "171, § 2º-A" | 285 | 391 |
| FE_amp | "art. 171, § 2º-A" | 109 | 214 |
| INV | "invasão de dispositivo informático" | 3 | 14 |
| CL | "conta laranja"; "contas laranja"; "contas laranjas" | 9; 4; 2 | (sem acento) |
| CL | "cessão de conta"; "cessão de contas" | 0; 11 | 4; 3 |
| EE | "estelionato eletrônico" | 0 | 23 |
| | União | 1.283 publicações distintas | |

Por rótulo, em processos: FE 121 ações penais e 8 apelações; FE_amp 421 e 7; INV 2 e 0; CL 0 e 0; EE 9 e 1. As 33 publicações CL são todas cíveis.

`dados/djen/alvos_djen_tjsc.csv` (mesmos campos do TJPA) tem 467 números criminais: 454 de ação penal ou apelação criminal (447 ações penais e 10 apelações, 7 só como apelação), 61 com sentença publicada no DJEN, 13 inquéritos e nenhum flagrante. Totais e séries em `dados/djen/totais_tjsc.json`; os metadados de cada publicação (sem texto e sem nomes) em `dados/djen/publicacoes_tjsc.csv`. Pelo estrato da fase 1: 452 FE, 2 INV e nenhum CL. A Capital (0023) tem 45 números, mas as varas criminais da Capital somam 149, porque o eproc numera por unidade regional (0523, 0538, 0539 e outras). Ficam fora 19 habeas corpus, os pedidos cautelares e os processos cíveis que casam com as frases (212 de procedimento comum, 98 de juizado especial cível, 65 apelações cíveis, 44 agravos de instrumento, 43 recursos inominados).

## O viés do edital

A composição das publicações criminais é outra que a do TJPA e do TJRJ: das 675 publicações de ação penal, apelação e inquérito, 452 são editais (tipos "Edital", "80" e "EDITAL DE CITAÇÃO", 450 deles de ação penal), 166 são despachos ou decisões, 54 sentenças e 3 acórdãos. O edital é publicado quando o réu está em lugar incerto, e o modelo do TJSC transcreve a "Síntese da Denúncia", em geral a capitulação ("Artigo 171, § 2º-A [fraude eletrônica], do Código Penal"), o que explica o peso do FE_amp. Todas as 54 sentenças publicadas têm advogado entre os destinatários; a intimação do MP e da Defensoria corre pelo portal do eproc e não chega ao DJEN.

Consequências: a lista do TJSC tem dois universos. Um, de 134 processos, com decisão, sentença ou apelação publicada desde maio de 2025, em que há defesa com advogado. Outro, de 320 processos, que só aparecem pelo edital de citação, de réu não localizado, com provável suspensão pelo art. 366 do CPP e sentença rara. A denúncia existe nos dois, mas o segundo sobrerrepresenta o réu de fora do estado ou sem endereço (o titular de conta de outra unidade da federação, por exemplo, que interessa à questão 1, sobre alcance e elo físico). A ausência de INV e CL entre as ações penais é efeito da cobertura e da forma das publicações (o edital resume a capitulação, e "conta laranja" é palavra da narrativa), não medida do fenômeno.

## Fila

`dados/codex_tjsc/fila.csv`, semente 202611224 (data do plano e sufixo da fase), gerada por `TRIB=tjsc python3 scripts/pipe_tjpa.py prox`:

| Grupo | Critério | Processos |
| --- | --- | --- |
| 1 | Sentença publicada no DJEN ou apelação | 68 |
| 2 | Demais ações penais com despacho ou decisão publicada | 66 |
| 3 | Ações penais que só aparecem pelo edital de citação | 320 |

O grupo 3 é a novidade: vai por último e em ordem aleatória, de modo que, se a coleta parar no meio dele, o lido é amostra aleatória simples desse estrato, com peso N/n (320 sobre os lidos). Os 13 inquéritos ficam fora, como nas fases anteriores.

Custo previsto, pelas fases anteriores (2,7 chamadas por processo no TJPA, 4,5 no TJRJ) e pelo ritmo de 40 s entre processos: cerca de 360 a 600 chamadas nos grupos 1 e 2 juntos, uma ou duas sessões; o grupo 3 sozinho pede mais 860 a 1.440 chamadas, três a cinco sessões.

## Operação

O condutor é o mesmo, `TRIB=tjsc python3 scripts/pipe_tjpa.py prox|sel|grava|status|nota|mapa|resumo`, com as regras de nota do TJPA. Textos em `textos/tjsc/denuncias/` e `textos/tjsc/sentencas/`, manifesto em `textos/tjsc/manifesto.csv`, status em `dados/codex_tjsc/status.csv`. As regras de localização próprias do eproc (nomes de documento da denúncia e da sentença, posição do recebimento, onde ficam as peças do inquérito) entram no `mapa` depois da sondagem de 3 a 5 processos no Codex, que é o primeiro passo da coleta. Na extração, a regex CNJ do TJSC é `8\.24`.

## Vieses e ressalvas

- Cobertura decisória de cerca de 19 meses (05/2025 a 11/2026), mais curta que a do TJRJ; antes disso só os editais.
- Viés de defesa constituída nas sentenças publicadas e viés de réu não localizado no grupo 3 (acima).
- Busca dependente da codificação do texto: sem as entidades, a lista teria perdido a maior parte das publicações; outras codificações (grau no lugar do ordinal) ficam de fora e foram medidas.
- Como no TJPA e no TJRJ, entram ações penais sem sentença, e a frase casa citação: a precisão se mede na capitulação lida.

## Extensões possíveis, fora desta coleta

- Pesquisa de jurisprudência do TJSC, com as mesmas frases e filtro criminal, para trazer apelações de sentenças anteriores a maio de 2025; o número da apelação é o de origem.
- Inteiro teor dos editais (`texto: true`), cuja "Síntese da Denúncia" permitiria conferir a capitulação dos 320 do grupo 3 antes da leitura pelo Codex.
- Os 13 inquéritos, pela regra de seleção do `docs/plano-captura.md`.

## Fontes

- [TJSC adota o DJEN a partir de 21/06/2021 (Resolução TJ n. 5/2021), notícia reproduzida pela AASP](https://www.aasp.org.br/?p=33019)
- [Mudanças nas intimações do eproc determinadas pelo CNJ, TJSC, 12/03/2025](https://www.tjsc.jus.br/web/imprensa/-/mudancas-nas-intimacoes-do-eproc-determinadas-pelo-cnj-entram-em-vigor-na-proxima-segunda-feira)
- [Instituições preparam implantação da competência criminal do eproc, TJSC, 24/09/2019](https://www.tjsc.jus.br/web/imprensa/-/instituicoes-preparam-implantacao-da-competencia-criminal-do-sistema-eproc)
- [TJSC facilita acesso ao eproc (migração concluída em 21/01/2021)](https://www.tjsc.jus.br/web/imprensa/-/tjsc-facilita-acesso-ao-eproc-com-tutoriais-especificos-para-diversos-profissionais-)
- [Tutorial de pesquisa da jurisprudência no eproc, TJSC, atualizado em 06/10/2025](https://eproc1g.tjsc.jus.br/eproc/modulos/jurisprudencia/ajuda/doc/manual_jurisprudencia_tjsc_113.pdf)
- Sondas próprias de 22/11/2026 na API pública do DJEN, registradas em `dados/djen/totais_tjsc.json`
