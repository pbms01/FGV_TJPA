# Fase 1: corpus de denúncias do TJSP

Revisão de 20/11/2026, à tarde. O produto da fase continua o mesmo: o máximo de denúncias do TJSP com a descrição da conduta e a tipificação dada pelo Ministério Público. Muda a porta de entrada. Os números-alvo passam a vir da Consulta de Julgados de 1º Grau do e-SAJ (cjpg), por busca textual, e não mais do DataJud por código de assunto. O DataJud fica como denominador para quando voltar a responder. O recorte TJPA segue suspenso.

## Por que o cjpg

Piloto de 20/11/2026, com filtro de ação penal (classes TPU 283, 10943 e 10944):

| Tipo | Pelo código de assunto | Pela busca textual |
| --- | --- | --- |
| Fraude eletrônica (art. 171, § 2º-A) | 15623: 0 julgados | "fraude eletrônica": 1.702 |
| Invasão de dispositivo (art. 154-A) | 11978: 2 julgados | "invasão de dispositivo informático": 80 |
| Conta laranja (art. 171, § 2º, VII) | 15755: não existe na árvore do cjpg | variantes de "conta laranja" e "cessão de conta": 364 |

As denúncias por art. 171, § 2º-A estão cadastradas no assunto genérico Estelionato (3431). O código TPU que nomeia o tipo quase não é usado no 1º grau do TJSP, de modo que o recorte por código perderia praticamente todo o fenômeno. A busca pelo texto da imputação o alcança e casa com o objeto da fase. O dado sobre o desuso do código é ele próprio um achado sobre a visibilidade do tipo (ver `claude/quadro-visibilidade-tpu-lei-14155.md` no Project).

## Consultas

Todas com filtro de classe `8657,8803,8804` (código interno do cjpg; a cadeia de cada nó traz o TPU: 283 ordinário, 10943 sumário, 10944 sumaríssimo).

| Rótulo | Pesquisa livre | Total em 20/11 | Observação |
| --- | --- | --- | --- |
| FE | `"fraude eletrônica"` | 1.702 | Também casa furto mediante fraude eletrônica (art. 155, § 4º-B), que está fora do recorte; separar pelo indicador do § 2º-A |
| FE_amp | `"2º-A" E estelionato` | 3.240 | Amplia a FE; o incremento real ainda não foi medido. O piloto rodou a variante `("2º-A" E estelionato) NÃO "fraude eletrônica"` (1.173), mas o NÃO não excluiu a frase e as 20 primeiras linhas coincidiram com a FE; por isso a versão final dispensa o NÃO e deduplica no consolidado |
| INV | `"invasão de dispositivo informático"` | 80 | Só metade das sentenças do piloto cita o art. 154-A; não usar `"dispositivo informático"`, que puxa o furto do art. 155, § 4º-B |
| CL | `"conta laranja" OU "contas laranja" OU "contas laranjas" OU "cessão de conta" OU "cessão de contas"` | 364 | Pega a conduta em qualquer período; a Lei 15.397/2026 (vigente desde 04/05/2026) separa os casos pela data do fato, a apurar na denúncia |

Regras de redação das consultas: o índice quebra o número do artigo (`"154-A"` casou "pág. 154" e devolveu 3.723 resultados dominados por tráfico), então se usa o nome do tipo ou expressões da narrativa, nunca o dispositivo sozinho. A palavra "denúncia" não ajuda a filtrar, porque casa também "denúncia de golpe"; o filtro de classe faz esse papel.

## Universo e vieses

O cjpg só lista processo com sentença de 1º grau publicada. O universo passa a ser o das ações penais sentenciadas, e ficam de fora os processos em curso e os que correm em segredo de justiça. O efeito é maior nos casos recentes, sobretudo na conta laranja posterior a maio de 2026. Quando o DataJud voltar, o censo por código (`scripts/censo_denuncias_tjsp.py`) mede o universo codificado e serve de comparação.

Na invasão, a busca sem filtro de classe devolveu 233 julgados: 80 ações penais (48 citam o art. 154-A), 67 inquéritos policiais (27 citam o 154-A, quase sempre arquivamentos), 25 termos circunstanciados, 15 representações criminais e ações cíveis de indenização. Os arquivamentos ficam fora do corpus de denúncias, mas servem à linha do funil de atrito e estão listados em `dados/cjpg/piloto_totais_20261120.json`.

## Passo 1 · números-alvo pelo cjpg (zero token)

Duas vias, com as mesmas regras e os mesmos indicadores.

Via A, script Python (só biblioteca padrão), para rodar no seu computador:

    python scripts/cjpg_alvos.py                  # as quatro consultas, todas as páginas
    python scripts/cjpg_alvos.py --so INV CL      # só algumas
    python scripts/cjpg_alvos.py --max-paginas 3  # piloto
    python scripts/cjpg_alvos.py --texto          # grava também o inteiro teor da sentença

Grava `dados/cjpg/bruto/<rótulo>.jsonl` (uma linha por resultado, retomável pelas páginas já feitas) e consolida em `alvos_cjpg_tjsp.csv`, um número por linha com as consultas que o trouxeram. Pausa de 3 s entre requisições, um único fluxo, sem disfarce de navegador. Se a resposta trouxer CAPTCHA ou erro repetido, para e registra; não há tentativa de contornar barreira. Nesta sessão de 20/11, o acesso automatizado a partir do workspace foi recusado pelo classificador de segurança, por isso a via A fica para o seu computador ou para uma autorização expressa.

Via B, navegador (foi a do piloto): abrir `https://esaj.tjsp.jus.br/cjpg/`, colar `scripts/cjpg_navegador.js` na aba e usar `cjpg.iniciar('FE')`, `cjpg.estado()` e `cjpg.lote(0, 300)`. Uma consulta por vez, porque a paginação depende da última consulta da sessão. Com o painel do navegador oculto, os temporizadores desaceleram (no piloto, cerca de 10 s por página).

Como o cjpg funciona por dentro: `GET /cjpg/pesquisar.do` com os campos do formulário abre a consulta na sessão, e `GET /cjpg/trocarDePagina.do?pagina=N` devolve cada página de 10 resultados, o mesmo que o botão da página faz. A listagem já traz, oculto, o inteiro teor de cada sentença; os indicadores são calculados sobre ele.

Indicadores por resultado: `m_171_2A`, `m_fraude_eletronica`, `m_154A`, `m_laranja`, `m_imputacao` (achou o trecho "foi denunciado", "ofereceu denúncia", "incurso nas penas"), `condena` e `absolve` (no dispositivo), e `imputacao` (420 caracteres a partir desse trecho).

## Passo 1b · amostra de 200 (decisão de 20/11/2026)

Não se coleta o universo; sorteia-se uma amostra de 200 denúncias.

| Estrato | Lista do cjpg | Meta | Sorteio (com reserva) |
| --- | --- | --- | --- |
| INV | invasão | censo | todas as páginas, todos os julgados com art. 154-A |
| CL | conta laranja | 50 | 34 páginas, até 2 por página |
| FE | "fraude eletrônica" e acréscimo do "§ 2º-A" | 200 menos INV e CL obtidos | 38 páginas da FE e 28 da FE_amp, até 2 por página |

Regras: páginas por amostragem sistemática com início aleatório sobre a lista ordenada por data; dentro da página, até 2 elegíveis escolhidos ao acaso; estratos excludentes por precedência (INV, depois CL, depois FE; do acréscimo FE_amp só entra o que não tem a expressão "fraude eletrônica"); peso igual ao inverso da fração de páginas sorteadas vezes a fração de elegíveis tomados na página; ordem de processamento aleatória dentro do estrato, para que parar na meta produza subamostra aleatória. Semente 20261120. A margem para uma proporção, a 95%, fica perto de 9 pontos na FE e 13 na CL; um modo de execução presente em 3% da FE ou 6% da CL aparece ao menos uma vez com cerca de 95% de probabilidade.

Execução: colar `scripts/cjpg_sorteio.js` numa aba do cjpg, `sorteio.iniciar()`, acompanhar com `sorteio.estado()` e gravar `JSON.stringify(sorteio.resultado())` num arquivo; depois `python scripts/sorteio_para_csv.py arquivo.json`, que gera `dados/cjpg/amostra_tjsp.csv` e `dados/cjpg/sorteio_listas.json`.

## Passo 2 · ler a denúncia pelo Codex (fora do contexto)

    export TECJUSTICA_API_KEY=...
    python scripts/codex_denuncias.py --simular   # plano
    python scripts/codex_denuncias.py             # coleta, retomável
    python scripts/codex_denuncias.py --teste     # parsers, sem rede

O script chama o endpoint MCP da TecJustica direto, em sequência, uma chamada a cada 6,5 s e no máximo 140 chamadas estimadas por hora. Por processo: mapa de documentos, depois leitura em lote de todas as partes da categoria "Peça Inicial" do 1º grau (descarta o dossiê de 2º grau e as cópias redistribuídas). Processa a invasão inteira, a conta laranja até 50 e a fraude até completar 200. Registra `sigilo`, `sem_peca_inicial` e `sem_texto` em `dados/codex/status.csv`; a reserva do mesmo estrato repõe a perda. Grava o texto em `textos/tjsp/denuncias/<numero>/` e o manifesto em `textos/tjsp/manifesto.csv`, sem a linha `Original:`.

## Passo 2 (manual) · localizar a denúncia no Codex numa conversa

Na ordem de `alvos_cjpg_tjsp.csv`, priorizando as linhas com o indicador do tipo verdadeiro, em ritmo de até 15 chamadas por minuto:

1. `pdpj_mapa_documentos`: no caso conferido no piloto (1503319-14.2023.8.26.0577), a denúncia veio como "Peça Inicial (provável)", em três documentos de uma página ("Denncia.pdf", cerca de 2 mil caracteres cada), com texto nativo do PJe.
2. Se o mapa não apontar a peça inicial, `pdpj_list_movimentos` com `tipo_filter` "Denúncia" e leitura mínima (`max_chars` 1500) das primeiras peças do MP depois do recebimento.
3. Se o conector devolver só o dossiê de 2º grau, o acórdão entra como fonte de reserva, marcado como tal.
4. O relatório da sentença do cjpg costuma transcrever a imputação e o resumo dos fatos; serve de conferência e de reserva quando a denúncia não abrir.

No caso conferido, a denúncia cita o inquérito pelo mesmo número da ação penal, o que confirma, ao menos aí, a continuidade do número que o censo por DataJud tratava como "a conferir".

### Dimensionamento do Codex (20/11/2026)

Limites segundo a skill do conector sincronizada nesta sessão (a página publicada não pôde ser conferida): 20 chamadas reais por minuto e 300 por hora por chave; metade disso (10 por minuto, 150 por hora) para fluxos automatizados; teto global de 130 por minuto somando todos os usuários; 30 perguntas por dia em `pdpj_perguntar_processo`; leitura em lote de até 50 documentos por 1 chamada (mais 1 por documento que exija OCR); chamadas sequenciais, nunca em paralelo; diante de "aguarde Xs", esperar e não repetir.

Medições em três processos do piloto:

| Processo | Documentos | O que se observou |
| --- | --- | --- |
| 1503319-14.2023.8.26.0577 | 397 | mapa com 65,8 KB (gravado em arquivo pela sessão); denúncia em 3 partes, 6,3 KB; denúncia e sentença em lote, 30 KB, inteiro no contexto |
| 1501939-55.2025.8.26.0004 | 259 | mapa com 40 KB, inteiro no contexto; denúncia em 5 partes, mas o destaque "peça inicial provável" listou só 3; `pdpj_analise_essencial` com 5 vagas leu 2 páginas da denúncia e 3 despachos |
| 1505779-08.2022.8.26.0577 | não abriu | sigilo no Codex, embora a sentença seja pública no cjpg |

Conclusões: (1) rota por processo é mapa (1 chamada) e leitura em lote de todas as partes da categoria "Peça Inicial" do 1º grau (1 chamada), cerca de 2 chamadas reais; (2) não usar `pdpj_perguntar_processo` (30 por dia), `pdpj_analise_essencial` (gasta vagas com despachos) nem `pdpj_list_movimentos` com filtro "Denúncia" (devolve só a decisão de recebimento); (3) a sentença vem do cjpg e não passa pelo Codex; (4) a perda por sigilo no Codex pode não ser aleatória (a invasão tende a correr em segredo), então é registrada como variável e reposta pela reserva do mesmo estrato.

Orçamento para 200 denúncias, com perda planejada de 25%: cerca de 270 processos e 540 chamadas reais, ou seja, cerca de 3,6 horas na metade da cota (150 por hora), em blocos de até 70 processos por hora. No contexto de uma conversa, cada processo custa de 30 a 80 KB (mapa de 15 a 65 KB, à razão de cerca de 155 bytes por documento, mais a denúncia lida e regravada), o que não cabe numa sessão; daí a coleta por script fora do contexto ou em blocos isolados.

## Passo 3 · gravar o texto lido (sem baixar a peça)

Decisão de 20/11/2026: não se pseudonimiza e não se baixa a peça; grava-se no repositório só o texto lido pelo Codex.

1. `textos/tjsp/denuncias/<numero>/<documento_id>.txt`, um arquivo por documento, na ordem das páginas, com o cabeçalho de procedência que o Codex devolve (texto nativo, OCR ou parser).
2. Manifesto `textos/tjsp/manifesto.csv`: numero, documento_id, papel (denuncia, aditamento, acordao_reserva, sentenca_cjpg), procedencia, chars, sha256 do texto gravado, data da leitura.
3. A linha `Original:` que o Codex devolve traz um link com token de acesso: nunca entra em arquivo, manifesto ou commit.
4. O inteiro teor das sentenças do cjpg, quando gravado (`--texto`), vai para `textos/tjsp/sentencas_cjpg/`.

Em aberto: máscara mínima de CPF, RG, telefone e endereço nos textos gravados, que recomendei e aguarda sua decisão.

## Produto: `denuncias_tjsp.csv`

| Campo | Conteúdo |
| --- | --- |
| numero | número CNJ (dígito verificador conferido) |
| consultas | rótulos do cjpg que trouxeram o número (FE, FE_amp, INV, CL) |
| classe, assunto, comarca, vara | do cjpg |
| data_sentenca | data de disponibilização no cjpg |
| data_denuncia | do texto ou do movimento |
| narrativa | descrição da conduta, do início do relato até o pedido |
| capitulacao_texto | trecho literal da tipificação na denúncia |
| dispositivos | lista normalizada (ex.: CP 171 § 2º-A; CP 154-A § 3º; CP 288) |
| capitulacao_sentenca | tipificação acolhida na sentença, para medir a distância entre denúncia e sentença |
| resultado | condenação, absolvição, parcial (indicadores do cjpg, conferidos na leitura) |
| fonte | denuncia, aditamento, acordao_reserva ou sentenca_cjpg |
| procedencia | texto nativo ou OCR |

## Achados do piloto (20/11/2026)

- 110 linhas, 79 números distintos, todos com dígito verificador válido (`dados/cjpg/piloto_cjpg_tjsp_20261120.csv`).
- FE: o § 2º-A aparece em 23 de 30 sentenças; 3 das 30 estão em assunto de furto. Algumas sentenças trazem denúncia por art. 171, caput, e discutem a fraude eletrônica depois, o que torna útil comparar a capitulação da denúncia com a da sentença.
- CL: "laranja" ou "cessão de conta" em 30 de 30; o § 2º-A em 19.
- INV: o art. 154-A citado em 15 de 30; o resto são sentenças de outros crimes que mencionam a expressão.
- O indicador de condenação (busca de "condeno" ou "julgo procedente" no fim da sentença, ainda sem conferência manual) aparece em 20 de 30 sentenças na FE e em 22 de 30 na CL.

## Pendências

- Rodar a coleta completa (cerca de 5,4 mil resultados brutos somando as quatro consultas, antes de deduplicar): via A no seu computador ou via B no navegador, com o painel visível.
- Medir o incremento real da FE_amp sobre a FE depois de deduplicar.
- Censo por código no DataJud, como denominador, quando a API voltar.
