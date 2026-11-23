# Fase 2: TJPA pela API do DJEN e pelo Codex

Revisão de 21/11/2026. O produto é o mesmo da fase 1: o máximo de denúncias com a descrição da conduta e a tipificação dada pelo MP, com a sentença quando houver, agora no TJPA, onde entram também os inquéritos pela regra de seleção do `docs/plano-captura.md`. Este roteiro substitui, para a porta de entrada, o `docs/RUNBOOK.md` (coleta noturna pelo DataJud, de 19 e 20/11/2026), que fica como registro.

## Por que o DJEN

O desenho da fase 1 pedia uma consulta pública com busca textual e inteiro teor, como o cjpg do TJSP. O TJPA não tem essa consulta:

| Fonte | O que oferece | Serve como porta de entrada? |
| --- | --- | --- |
| Banco de Jurisprudência (jurisprudencia.tjpa.jus.br) | Só acórdãos e decisões monocráticas, com busca textual, segundo a página do portal publicada em 24/07/2026; em 21/11/2026 não respondeu, nem do navegador do usuário nem do workspace | Não; no máximo complemento para apelações |
| Consulta pública do PJe e Consulta Unificada | Número, parte, advogado | Não |
| DataJud | Recorte por código; o 15623 tem 0 processos no TJPA, e o 3431 é o estelionato inteiro | Só como denominador |
| API pública do DJEN | Busca textual por tribunal e período, com inteiro teor, classe, tipo de documento e órgão de cada ato publicado | Sim |

A Resolução TJPA 14, de 11/08/2021, regulamenta a publicação dos atos no DJEN. A série de controle mostra cobertura desde 2022: "estelionato" tem 1.086 publicações em 2022, 1.565 em 2023, 2.018 em 2024, 2.739 em 2025 e 2.869 em 2026 até 20/11. "Fraude eletrônica" passa de 24 (2022), 42 (2023) e 57 (2024) a 301 (2025) e 925 (2026), crescimento muito maior que o da cobertura.

## A API

`GET https://comunicaapi.pje.jus.br/api/v1/comunicacao`, a mesma que alimenta o comunica.pje.jus.br.

| Parâmetro | Uso |
| --- | --- |
| `texto` | Uma frase |
| `siglaTribunal` | `TJPA` |
| `dataDisponibilizacaoInicio`, `dataDisponibilizacaoFim` | `AAAA-MM-DD`; a janela 2020-01-01 a 2026-11-20 rodou inteira, sem fatiar |
| `pagina`, `itensPorPagina` | Usamos 100 por página |

A resposta traz `count` e `items`. Cada item tem `id`, `numeroprocessocommascara`, `codigoClasse`, `nomeClasse`, `tipoDocumento` (Sentença, Decisão, Ementa, Intimação, Despacho, Edital), `nomeOrgao`, `data_disponibilizacao`, `texto` (inteiro teor), `destinatarios` e `destinatarioadvogados`.

Semântica medida em 21/11/2026:

- Cada consulta é uma frase. Aspas são indiferentes, e "fraude eletrônica estelionato" devolve 4 publicações (a frase, não a interseção). Não há OU nem E: cada variante é uma consulta, e a união se faz pelo `id`.
- Não há filtro de classe; parâmetros como `codigoClasse` são ignorados. O filtro se aplica depois, pelo `codigoClasse` do item.
- O número do artigo sozinho não serve: "154-A" devolve 340 publicações. "171, § 2º-A" e "art. 171, § 2º-A" funcionam como frase.
- No TJPA a apelação criminal mantém o número de origem, de modo que a ementa publicada leva ao processo de primeiro grau. O habeas corpus tem número próprio (final 0000) e fica fora.
- Acesso: do workspace da sessão a API devolve 403 (CloudFront); do navegador do usuário respondeu sem captcha, com pausa de 1,2 a 1,5 s, sem recusa em cerca de 100 chamadas.

## Consultas

| Rótulo | Frases | Publicações (2020-01-01 a 2026-11-20) |
| --- | --- | --- |
| FE | "fraude eletrônica" | 1.358 |
| FE_amp | "171, § 2º-A"; "art. 171, § 2º-A" | 486; 332 |
| INV | "invasão de dispositivo informático" | 102 |
| CL | "conta laranja"; "contas laranja"; "contas laranjas"; "cessão de conta"; "cessão de contas" | 33; 4; 28; 10; 0 |
| EE | "estelionato eletrônico" | 92 |

## Resultado da sondagem (21/11/2026)

Por rótulo, contando processos pelas publicações da própria classe:

| Rótulo | Publicações | Ações penais | Com sentença publicada | Apelações criminais |
| --- | --- | --- | --- | --- |
| FE | 1.358 | 78 | 51 | 28 |
| FE_amp (só as duas frases) | 486 | 152 | 43 | 18 |
| INV | 102 | 16 | 7 | 2 |
| CL | 66 | 10 | 7 | 3 |
| EE | 92 | 9 | 5 | 4 |
| União | 1.861 | 204 | 75 | 33 |

A união, em `dados/djen/alvos_djen_tjpa.csv`, tem 299 números:

- 225 de ação penal ou apelação criminal (204 e 33, com 12 nos dois conjuntos; 21 só como apelação);
- 99 com sentença conhecida, publicada no DJEN ou já apelada;
- 74 inquéritos (279) e 14 autos de prisão em flagrante (280), dos quais 12 inquéritos têm o mesmo número de uma ação penal da lista, porque no TJPA o inquérito e a ação penal compartilham o número;
- 144 dos 225 são de Belém (0401); entre as ações penais FE, 46 de 78.

Ficam fora da lista 180 habeas corpus e os processos cíveis que casam com as frases, entre eles 322 de procedimento comum, 349 de juizado especial cível e 112 apelações cíveis (`dados/djen/totais_tjpa.json`, `processos_por_classe`).

No TJSP, só "fraude eletrônica" devolvia 1.702 julgados no cjpg. No TJPA o universo cabe inteiro, e o desenho passa de amostra a censo.

## Vieses, a medir antes de tratar a lista como censo

- O DJEN só traz atos com intimação publicada. Dos 225 processos de ação penal ou apelação, 101 só têm publicações sem advogado entre os destinatários, então a publicação não depende de defesa constituída; mas o processo em que só o MP e a Defensoria são intimados pelo sistema pode não ter publicação nenhuma. Teste: uma amostra de ações penais por estelionato do DataJud (ou do Codex, pelo CNPJ do MPPA), procurada no DJEN pelo número.
- Ao contrário do cjpg, entram ações penais sem sentença (129 das 204, por decisões de recebimento, de audiência ou intimações), o que tira do corpus de denúncias a restrição aos sentenciados.
- A frase casa citação, não imputação: no 0822630-11.2023.8.14.0401 a denúncia capitula o art. 171, caput, e a "fraude eletrônica" vem da sentença. A precisão se mede na leitura da capitulação, como no TJSP.

## Passo 1: números-alvo

Via A, no computador do usuário (só biblioteca padrão):

    python scripts/djen_alvos.py --fim 2026-11-20          # TJPA, as cinco consultas
    python scripts/djen_alvos.py --so FE INV               # só alguns rótulos
    python scripts/djen_alvos.py --controle estelionato    # série de cobertura por ano
    python scripts/djen_alvos.py --teste                   # parser e consolidação, sem rede

Grava `dados/djen/bruto/TJPA_<rótulo>.jsonl` (uma linha por publicação e frase, sem nomes de pessoas), `dados/djen/alvos_djen_tjpa.csv` e `dados/djen/totais_tjpa.json`. Com `--texto`, grava o inteiro teor em `textos/tjpa/djen/<id>.txt`. Em 403 para e avisa; em 429 ou 5xx espera e tenta três vezes.

Via B, navegador (foi a da sondagem): abrir `https://comunica.pje.jus.br/`, colar `scripts/djen_navegador.js` na aba e usar `djen.iniciar({tribunal: 'TJPA', inicio: '2020-01-01', fim: '2026-11-20'})`, `djen.estado()`, `djen.totais()`, `djen.csv()` e `djen.controle()`. Para trazer o CSV à sessão sem passar pelo contexto, devolver pelo `javascript_tool` um JSON com o CSV repetido, acima de cerca de 50 KB, que a sessão grava em arquivo; depois ler o arquivo pelo shell.

Campos de `alvos_djen_tjpa.csv`: numero; acao_penal, apelacao, inquerito, flagrante (classe de alguma publicação); data_sentenca_djen (última publicação de ação penal classificada como sentença: tipo Sentença, ou verbo do dispositivo com "ante o exposto", "isto posto", "diante do exposto" ou "dispositivo"); primeira_pub e ultima_pub; consultas (rótulos que trouxeram o processo); m_fraude_eletronica, m_171_2A, m_154A, m_laranja (indicadores em alguma publicação); n_pubs e n_pubs_sem_advogado; orgao_1g.

## Passo 2: ler a denúncia e a sentença pelo Codex

Testado em cinco processos em 21/11/2026; todos públicos e em PJe, com denúncia e sentença em texto nativo nos três abertos por dentro.

| Processo | O que se viu |
| --- | --- |
| 0822630-11.2023.8.14.0401, 8ª Vara Criminal de Belém | "Peça Inicial" é o ofício de remessa do inquérito (564 caracteres); a denúncia é um "Petição.pdf" juntado como petição sob sigilo, achado por leitura mínima; capitula o art. 171, caput; sentença em Sentença.html, 25 mil caracteres |
| 0815181-65.2024.8.14.0401, 1ª Vara Criminal de Belém, em 2º grau | Denúncia do tipo "Denúncia" (8,4 mil caracteres, art. 171, § 2º-A, venda falsa em rede social); "Petição Inicial" é o inquérito, com 34 páginas |
| 0803104-11.2023.8.14.0061, Tucuruí, em apelação | Denúncia do tipo "Denúncia"; os documentos do 1º grau aparecem duplicados no dossiê de 2º grau, com outro código PJe |
| 0012873-31.2020.8.14.0401 | Número antigo abre no PJe; o Codex ainda o classifica como Inquérito Policial, embora sentenciado |
| 0003478-80.2013.8.14.0006 | Número de 2013, digitalizado, abre com 174 documentos |

A rota do TJSP (`pdpj_mapa_documentos` e leitura em lote da categoria "Peça Inicial") lê aqui o ofício do delegado ou o inquérito. A rota do TJPA:

1. `pdpj_list_documentos` com `limit=100`. A lista vem do mais novo para o mais antigo e traz o tipo entre parênteses; para chegar às primeiras peças, `offset` = total menos 100. Escolher o documento do tipo "Denúncia" (e os aditamentos).
2. Sem documento do tipo "Denúncia": `pdpj_list_movimentos` com `tipo_filter="Denúncia"` dá a data de "Recebida a denúncia"; as petições juntadas antes dela, que não sejam da defesa, são lidas com `max_chars=1500` até o cabeçalho "DENÚNCIA". O mesmo princípio está no `HANDOFF.md` para o TJSP.
3. Sentença: documento do tipo "Sentença" na mesma lista, ou o movimento de procedência ou improcedência. Quando publicada, o inteiro teor também está no DJEN (`texto` do item com `tipoDocumento` Sentença).
4. `pdpj_read_documentos_batch` com a denúncia e a sentença; em processo apelado, deduplicar por nome, páginas e caracteres e ficar com uma cópia.
5. Gravar como na fase 1: `textos/tjpa/denuncias/<numero>/` e `textos/tjpa/sentencas/<numero>/`, manifesto com sha256 e data da leitura, sem a linha `Original:`.

### Operação na conversa (`scripts/pipe_tjpa.py`, desde 21/11/2026)

A coleta roda na conversa, com o conector Codex, e o texto lido não passa pelo contexto: a leitura em lote repete os IDs até a resposta passar de cerca de 100 mil caracteres, e a sessão a grava em arquivo sem prévia. Fila em `dados/codex_tjpa/fila.csv` (grupo 1: 99 com sentença conhecida; grupo 2: 126 ações penais restantes; ordem aleatória, semente 20261121); status em `dados/codex_tjpa/status.csv` (vale a última linha); textos em `textos/tjpa/denuncias/` e `textos/tjpa/sentencas/`; manifesto em `textos/tjpa/manifesto.csv`.

Roteiro por processo, da raiz do repositório:

1. `python3 scripts/pipe_tjpa.py prox` dá o próximo número.
2. `pdpj_visao_geral_processo`: total de documentos, grau e sigilo. Sigilo: `status NUM sigilo "..." 1`. Fato fora do tema (por exemplo, termo circunstanciado ambiental): `status NUM fora_do_tema "..." 1`.
3. Com mais de cerca de 330 documentos, `pdpj_mapa_documentos` vai a arquivo, e `python3 scripts/pipe_tjpa.py mapa ultimo` imprime denúncia, sentença, recebimento e candidatas. Com menos, `pdpj_list_movimentos(tipo_filter="cedência")` dá o documento da sentença, e `pdpj_list_documentos(limit=45, offset=total-45)` dá as primeiras peças (até 45 documentos, uma chamada só com `offset=0`). Sem documento do tipo "Denúncia" na janela, `pdpj_list_movimentos(tipo_filter="Denúncia")` dá a data do recebimento e orienta a página seguinte; as petições e pareceres do MP antes dela entram como `cand`.
4. `python3 scripts/pipe_tjpa.py sel NUM "den:ID|nome|data|chars" "sent:ID|nome|data|0" ["cand:..."]` imprime a lista de IDs repetidos; tamanho 0 (desconhecido) usa 30 IDs.
5. `pdpj_read_documentos_batch` com essa lista; depois `python3 scripts/pipe_tjpa.py grava ultimo N "nota"` (N = chamadas do processo), que grava, aceita candidata só se o texto for de denúncia e imprime capitulação e dispositivo.
6. `python3 scripts/pipe_tjpa.py resumo` dá o andamento. Commit a cada 10 a 20 processos.

Lições dos primeiros 20: o movimento "Improcedência" às vezes acompanha sentença condenatória (o resultado sai do texto); processo migrado traz a denúncia como "doc 0NN - denuncia.pdf" (Documento de Migração) logo depois dos volumes do inquérito; processo nascido de flagrante tem a denúncia mais adiante na lista; sentença lida pelo movimento tem tamanho desconhecido, e por isso o `sel` usa 0. Quando a denúncia não aparece, grava-se só a sentença (`so_sentenca`), cujo relatório transcreve a imputação, e o processo fica para uma segunda passada.

Custo medido: 610 chamadas registradas para os 225 processos, perto de 2,7 por processo, porque a visão geral deixa a lista, os movimentos e o mapa quase de graça e o sigilo se resolve com uma chamada. O limite horário do conector bloqueou uma vez (espera de 60 s), e a partir daí a coleta passou a dormir 40 s entre processos (30 s depois de um sigilo), sem novo bloqueio. O `scripts/codex_denuncias.py` ainda segue a rota do TJSP e precisa do localizador acima antes de rodar no TJPA.

### Estado ao fim da coleta (21/11/2026)

Os 225 números de ação penal ou apelação foram tratados. No grupo 1 (99 com sentença conhecida no DJEN), 87 ficaram com denúncia e, destes, 85 com sentença; 5 ficaram só com a sentença, 5 em sigilo e 2 fora do tema. No grupo 2 (126 restantes), 104 ficaram com denúncia e 25 com sentença ou decisão terminativa achada no Codex, que o DJEN não tinha classificado como sentença; 14 em sigilo, 6 fora do tema e 2 com a denúncia sem texto no Codex. O acervo tem 209 partes de denúncia e 121 de sentença, cerca de 5,25 milhões de caracteres, em `textos/tjpa/`, com o manifesto em `textos/tjpa/manifesto.csv`. Os 74 inquéritos sem ação penal ficaram fora, por decisão desta fase.

Duas famílias de desmembramento repetem a mesma denúncia e precisam contar uma vez só como peça acusatória, embora cada processo tenha andamento e réus próprios:

- Patrick Auler Stefanes, na Vara de Combate ao Crime Organizado de Belém (md5 do texto sem as três linhas de cabeçalho `1129e03326c83a6252b191f3377c8483`): 0802404-14.2025, 0802159-03.2025, 0802415-43.2025, 0802399-89.2025, 0802298-52.2025, 0802294-15.2025 e 0807765-75.2026.
- 10ª Vara Criminal de Belém, IPL 592 (md5 `2a12908e23003ebc9f5792d0e67712cb`): 0817567-05.2023, 0820198-53.2022, 0817564-50.2023, 0817558-43.2023, 0817566-20.2023 e 0817569-72.2023.

### Lições da coleta

Onde a denúncia aparece, além do documento do tipo "Denúncia":

- petição do MP juntada "sob sigilo", que a `pdpj_list_documentos` filtra como capa; o ID sai do movimento "Juntada de Petição de Sob sigilo" anterior ao recebimento, e o Codex às vezes devolve "Texto do documento indisponível" (o lote pode estourar o tempo no OCR), caso em que o processo fica `sem_texto` para a segunda passada;
- documento com outro nome ou tipo: "Resposta" (0800137-24.2024.8.14.0104), "Estelionato.pdf" (0802805-05.2023.8.14.0006), "Petição Inicial" da ação penal ajuizada pelo CyberGAECO com PIC (0811121-78.2026.8.14.0401), "Denúncia.html" do tipo Petição, cópia juntada com a citação quando o original ficou sob sigilo (0823242-46.2023.8.14.0401);
- denúncia em vários arquivos de uma página juntados no mesmo minuto; a ordem e o fim da peça saem do rodapé numerado, e o último arquivo pode ser outra manifestação do MP (0825320-42.2025.8.14.0401);
- capa com a palavra espaçada letra a letra ("D E N Ú N C I A"), que a busca do cabeçalho precisa tolerar;
- aditamento juntado como petição sob sigilo e recebido meses depois; grava-se como segunda parte da denúncia (0046698-39.2015.8.14.0401, recapitulação para o art. 171, caput, por fato anterior à Lei 14.155/2021).

O que conta como sentença: além da sentença de mérito, grava-se como sentença a decisão que encerra a ação no juízo, com nota, que é a rejeição da denúncia (inclusive parcial, só quanto a um réu, como em 0817566-20.2023.8.14.0401), a extinção da punibilidade por decadência (0824029-12.2022 e a queixa por invasão em 0800337-36.2021.8.14.0007) e a declinação de competência para a Justiça Federal (0815026-28.2025.8.14.0401, "chupa-cabra" em agência da Caixa). Em autos importados de 2022 para números de 2025, a "Sentença.html" de 666 caracteres datada de 24/10/2023 não é decisão de mérito e não se lê. Em sentença com vários réus, vale o primeiro dispositivo depois do "Ante o exposto", e o réu suspenso pelo art. 366 do CPP entra na nota.

Outras regras de operação:

- A vara sai de `orgao_1g` do `alvos_djen_tjpa.csv`, porque o órgão do Codex é o juízo das garantias ou o JECrim; a classe do Codex é defasada (inquérito, flagrante ou comunicado de mandado de prisão em processos sentenciados) e não decide nada.
- Família de desmembramento se confere com `sed 1,3d textos/tjpa/denuncias/<n>/01_*.txt | md5sum`, e a nota de cada membro cita os demais.
- Quando o `pdpj_mapa_documentos` cabe na resposta e não vai a arquivo, o `mapa ultimo` lê o mapa anterior; nesse caso os IDs se tiram do próprio mapa.
- Fato claramente fora do tema (termo circunstanciado de drogas, tráfico, receptação ou furto de moto, honra em conflito familiar) se marca pela visão geral ou por leitura mínima da inicial, sem gravar texto; nos demais, o tema se confere por busca de termos na denúncia gravada. A consulta INV do DJEN traz processos em que a publicação só cita a invasão de dispositivo.
- Nota não infere fato: a origem do réu não se escreve pelo estado da OAB do advogado, e decisão não lida fica como "não lida".
- A capitulação ainda escapa ao leitor quando o artigo vem a mais de 40 caracteres do verbo ("praticaram os crimes de furto qualificado, associação criminosa e lavagem de dinheiro, previsto nos arts. 155"), como em 0812438-48.2025.8.14.0401; a capitulação vai à nota.

## Pendências

1. Segunda passada, feita em 23/11/2026 (detalhe nas notas do `status.csv`): denúncias achadas por `pdpj_perguntar_processo` em 0818456-51.2026 ("doc 014 - denuncia.pdf", lavagem e organização criminosa), 0003478-80.2013 (início do volume digitalizado, AP01 partes 1 e 2) e 0814230-71.2024 ("Denúncia.pdf", posição 90); denúncias lidas do PDF original pelo `pdpj_get_documento_url` e `scripts/original_para_lote.py` em 0801497-10.2023 (a11b8a13) e 0800083-74.2023 (3f51107f), ambas com camada de texto; sentenças de 0000410-23.2021 (7d69679d) e 0802544-82.2024 (739ac9ed) lidas do HTML original guardado pelo Codex. Seguem sem denúncia 0814581-95.2022 (`so_sentenca`: o Codex só achou o indiciamento do flagrante) e 0811946-61.2022 (`sem_texto`: o ID e4d29280 não existe mais no Codex e a busca não achou a peça).
2. Peças vistas e não lidas: o acórdão de 0805552-38.2022 (08f78e51-37d7-5303-8b19-0e1a8ffc7f35), a decisão de 06/11/2026 em 0805897-96.2025, a guia de execução de Kerolayne em 0817569-72.2023 e as decisões interlocutórias marcadas "não lida" nas notas.
3. Medir a cobertura do DJEN contra o DataJud ou o Codex (viés acima), agora com a vantagem de que o grupo 2 mostrou 25 sentenças que o DJEN não classificava como tal.
4. Ampliar a janela da regex de capitulação no `cmd_grava` e regravar os casos com "capitulação não localizada".
5. Portar o localizador do TJPA ao `scripts/codex_denuncias.py`, se a coleta for repetida fora da conversa.
6. Inquéritos: aplicar a regra de seleção do `plano-captura.md` aos 74 inquéritos da lista, se a análise os pedir.
7. Tentar de novo o Banco de Jurisprudência do TJPA para os acórdãos das 33 apelações.
