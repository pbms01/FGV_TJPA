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

Custo: de 3 a 4 chamadas por processo, perto de 350 para os 99 com sentença e de 800 para os 225, ou seja, de 4 a 9 horas a 90 chamadas por hora. O `scripts/codex_denuncias.py` ainda segue a rota do TJSP e precisa do localizador acima antes de rodar no TJPA.

## Pendências

1. Medir a cobertura do DJEN contra o DataJud ou o Codex (viés acima).
2. Decidir entre o censo dos 99 com sentença conhecida e o dos 225.
3. Adaptar `scripts/codex_denuncias.py` (ou o `pipe_conversa.py`) ao localizador do TJPA e rodar.
4. Inquéritos: aplicar a regra de seleção do `plano-captura.md` aos 74 inquéritos da lista, se a fase 2 os mantiver.
5. Tentar de novo o Banco de Jurisprudência do TJPA para os acórdãos das 33 apelações.
