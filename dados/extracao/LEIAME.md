# Extração das denúncias TJSP (fase 1)

Gerado por `scripts/extrai_denuncias.py` a partir de `textos/tjsp/denuncias/`, `dados/codex/status.csv` (só status ok) e `dados/cjpg/amostra_tjsp.csv`. Os dados pessoais não estão mascarados nesta etapa, por decisão do pesquisador; o mascaramento fica para a versão de circulação.

## Saídas

`denuncias_tjsp.csv` tem uma linha por processo (200), com estes grupos de colunas:

- identificação e desenho: numero, estrato, ordem, lista, peso, comarca;
- tamanhos: chars_total, chars_cota, chars_narrativa, anexo_cortado;
- dispositivos lidos apenas na capitulação (`a_*`): 171, 171 §2º-A, 171 §2º VII, 171 §4º, 171 caput, 154-A, 155, 155 §4º-B, 180, 147, 313-A, drogas, 158, 288, 307, 297 a 299, lavagem, arts. 29, 69, 70 e 71, tentativa e "por N vezes";
- valores em R$ na narrativa (n_valores, valor_max, valor_soma_distintos) e ano do fato;
- indicadores de meio e de dinâmica na narrativa (`m_*`), vítima idosa, coautores desconhecidos, vítima pessoa jurídica;
- número de denunciados nomeados na capitulação, que é aproximado e fica vazio quando a capitulação usa pronome ("denuncio-o");
- cota: ANPP tratado, motivos de recusa (pena, confissão, antecedentes, ausência), pedido de preventiva e de quebra de sigilo;
- `tipo_capitulacao`, a pós-estratificação pela própria denúncia, com precedência 154-A > 171 §2º VII > 171 §2º-A > 155 §4º-B > 171 outro > 155 outro > 158 > 180 > lavagem > outro tipo;
- `alerta` e `duplicata_de`.

`segmentos/<numero>.json` guarda a cota, a narrativa e a capitulação em texto corrido.

## Regras de segmentação

- A cota é o trecho anterior ao endereçamento ("EXCELENTÍSSIMO") quando ele não abre a peça. Quando ela vem depois da denúncia e menciona o art. 28-A, a cota é o trecho posterior à capitulação.
- A capitulação começa numa âncora verbal ("denuncio", "denuncia-se", "oferece denúncia", "é oferecida a presente denúncia", "incidiram", "incorreu"). A âncora precisa vir seguida, em até 600 caracteres, de artigo e de verbo de imputação. Prefere-se a âncora precedida de fecho ("Ante o exposto", "Posto isto") e que contenha "incurso", "infração", "violação" ou "sanções". O trecho termina no primeiro pedido processual (Requeiro, Requer-se, Rol), com teto de 6.000 caracteres para as listas de denunciados do GAECO.
- A narrativa vai do primeiro "Consta", "Segundo se apurou", "Apurou-se" ou equivalente (se aparecer nos primeiros 1.500 caracteres do corpo; senão, desde o endereçamento) até o início da capitulação.
- Os indicadores `m_*` são regex exploratórias e servem à triagem. Não são codificação final. Tendem a subcontar `m_falso_parente` (por exemplo, "identificou-se falsamente como sendo Camila, filha da vítima") e a supercontar `m_transferencia_ted`, que inclui "depósito".

## Validação por leitura

Rodada 1: foram lidas as capitulações de oito processos sorteados (semente 7), e as oito trouxeram tipo, artigos, valor e ano corretos.

Rodada 2: foram lidos todos os alertas. A leitura corrigiu quatro pontos.

- Grafias do §2º-A. O parser passou a aceitar "§ 2ª-A", "§2.º-A", "§ 2-Aº" e o parágrafo partido por cabeçalho de página. Com isso, FE 9, 28, 90, 106 e 120 voltaram ao §2º-A.
- Grafias do 155 §4º-B. O parser passou a aceitar "§4ºB" sem hífen e a combinação "§4º, inciso IV, e §4º-B", o que recuperou CL 15, 24 e 29.
- Rodapé do e-SAJ. O rodapé de conferência ("Este documento é cópia do original...") e o carimbo e-STJ saem do texto antes da segmentação, porque cortavam a capitulação ao meio.
- Regra de anexo. O corte de peça anexada de outro processo passou a tratar como próprio o número de autos citado na abertura da peça.

O último ponto decorre do caso INV 3 (0001915-31.2023.8.26.0050). A peça salva é a denúncia completa, oferecida ainda sob o número de origem 1520714-33.2022.8.26.0228, que é o processo INV 32 da própria amostra. Como as duas denúncias são idênticas, INV 3 fica marcado como duplicata de INV 32.

INV 22 (1503431-80.2021.8.26.0050) foi relido. O texto nativo do PJe termina na página 16 de 24, e foi substituído pela cópia de 2025 da mesma denúncia (OCR em duas páginas), que é completa. A capitulação imputa o 154-A, §§ 3º e 4º, na redação anterior à Lei 14.155/2021, e o art. 12, §§ 1º e 3º, I, da Lei 9.609/98, em concurso material.

Os 14 alertas FE restantes são imputações reais fora do §2º-A, porque o estrato veio da sentença (CJPG) e não da denúncia. São dez processos no 171 caput (um deles tentado), um no 171 §4º, dois no furto qualificado comum (um deles com extorsão para o segundo réu) e um no 155 §4º-B contra idoso.

Os seis alertas INV restantes também são imputações reais de outro tipo:

- INV 36 (1007980-49.2022.8.26.0506), GAECO de Ribeirão Preto, Operação Atratus: imputa organização criminosa (Lei 12.850) e lavagem. O 154-A aparece só na narrativa, como crime antecedente.
- INV 35 (1521208-63.2020.8.26.0228): a capitulação diz "artigos 155-A e parágrafo 2º". É provável erro material por 154-A, a conferir na sentença.
- INV 5, 10, 14 e 40: 171 §2º-A, peculato com 313-A, furto em violência doméstica e calúnia (art. 138).

Duplicatas de denúncia (desmembramento ou renumeração): INV 7 repete INV 2, e INV 3 repete INV 32.

Rodada 3 (20/11/2026, na montagem da matriz de seleção de casos): a alternativa solta que lia o §2º-A partido por cabeçalho de página aceitava qualquer "2º-A" da capitulação, inclusive o §2º-A do roubo (art. 157). A do §4º tinha o mesmo defeito e pegava os §§ 3º e 4º do 154-A, o § 4º do 155 e parágrafos de leis especiais. As duas alternativas passaram a exigir que o trecho entre a última menção a "artigo" ou "art." e o parágrafo cite o 171 (função `do_171` do script). A nova execução mudou só estes campos:

- CL 11 e CL 18 (roubo com arma e extorsão) saíram do 171 §2º-A e foram para o 158; em INV 24 e INV 28, também roubos, caiu só a marca `a_171_2A`, porque o tipo já era 154-A;
- `a_171_4` deixou de marcar CL 25, FE 123 e INV 6, 11, 19, 20, 21, 22, 33, 39 e 44 (de 47 para 36 processos);
- CL 13 e FE 28, em que o cabeçalho de página separa o 171 do parágrafo, continuam com §2º-A e §4º.

## Distribuição pela capitulação (sem duplicatas, % ponderado dentro do estrato)

- INV, 34 denúncias: 154-A 29 (85,3%), outro tipo 2, 155 1, lavagem 1, 171 §2º-A 1.
- CL, 50: 171 §2º-A 21 (43,2%), 171 sem §2º-A 14 (27,8%), 155 §4º-B 5 (10,7%), 158 4 (7,2%), 180 2, 155 comum 2, lavagem 1, drogas 1. Nenhuma denúncia capitula o 171 §2º, VII.
- FE, 114: 171 §2º-A 100 (86,3%), 171 sem §2º-A 11 (10,8%), 155 comum 2, 155 §4º-B 1.

## Unidade de análise

A unidade principal é a denúncia, sem as duplicatas, com o peso amostral do processo. O processo é a unidade do sorteio, e as duas duplicatas saem das contagens. O tipo de análise é o da capitulação (`tipo_capitulacao`), cruzado com o estrato de origem. A estimativa de incidência dentro de cada estrato usa o peso. O denunciado fica como unidade secundária, para as perguntas sobre papel (titular da conta, autor da fraude) e concurso, e depende da codificação manual.

## Pendências

- Codificar à mão uma segunda subamostra independente se os indicadores forem usados como variável de resultado. Os 12 casos da rodada 2 não bastam para estimar precisão por estrato.
- A codificação de artifício e papel cobre agora as 200 denúncias: 36 manuais (`codificacao_manual_r*.csv`) e 164 assistidas (`codificacao_assistida.csv`, seção própria abaixo). A assistida ainda precisa de conferência humana por amostra antes de servir como variável de resultado.
- `tentativa` exige "14, II" ou "tentad" e perde a capitulação "c.c. o art. 14" sem inciso, como no FE 39. Corrigir com cuidado, porque o art. 14 da Lei 10.826/2003 (porte de arma) também aparece em denúncias.
- `n_denunciados_cap` conta nomes na capitulação e às vezes inclui a vítima ou um corréu desmembrado (INV 39 e FE 50 têm 2 na extração e 1 réu na sentença).

## Validação dos indicadores por codificação manual

Codifiquei à mão 36 denúncias, em duas rodadas: `codificacao_manual_r1.csv` (24 casos, 8 por estrato, semente 20261120) e `codificacao_manual_r2.csv` (12 casos, 4 por estrato, semente 20261121, sem repetir a r1). Para cada caso registrei contexto, meio de contato, artifício, papel do denunciado e oito indicadores binários comparáveis às colunas `m_*`.

As regex foram ajustadas olhando a r1. Por isso, a r1 mede o ajuste, e só a r2 mede o desempenho fora da amostra. A r2 foi medida antes dos dois últimos ajustes, e o resultado está em `validacao_regex.csv`. Em 12 casos, a concordância foi:

| Indicador | Concordância (r2) | Divergências |
|---|---|---|
| WhatsApp | 0,92 | FE 14 |
| Falso parente | 0,92 | CL 16 |
| Falsa central | 0,92 | FE 26 |
| Venda falsa | 0,92 | INV 28 |
| Pix | 0,83 | INV 28, CL 29 |
| Conta do denunciado | 0,83 | CL 50, FE 14 |
| Boleto | 1,00 | |
| Invasão | 1,00 | |

Os ajustes posteriores corrigiram duas dessas falhas:

- a limpeza do telefone da Promotoria no cabeçalho apagava o WhatsApp do golpista quando ele vinha sem dois-pontos (FE 14);
- "se fez passar por sua cunhada" não casava com a lista de verbos e de parentescos (CL 16).

Os indicadores `m_pix` e `m_boleto` medem menção, não o meio de pagamento da vítima. Eles também disparam com o Pix tentado pelo invasor, com o boleto da compra fraudulenta feita pelo réu e com o extrato transcrito. `m_conta_laranja` deixa escapar a conta recebedora identificada só pelo número.

A leitura também trouxe um achado substantivo. Dentro do INV, uma parte relevante do 154-A não tem fim patrimonial: é controle da parceira ou ex-parceira, com acesso ao celular ou às redes sociais da vítima, em contexto de violência doméstica. A coluna `contexto_vd` exige um contexto de VD narrado ou a Lei 11.340 na capitulação. Menção solta não basta, como o nome do Anexo de VD no cabeçalho, outro fato do réu ou "a casa da ex-esposa". Com essa regra, são 7 das 34 denúncias INV e 5 das 29 capituladas no 154-A. Nos estratos CL e FE não há nenhuma.

## Codificação assistida das 164 denúncias restantes

`codificacao_assistida.csv` tem as mesmas colunas e o mesmo vocabulário da r1 e cobre as 164 denúncias que as rodadas manuais não alcançaram (INV 24, CL 38, FE 102), incluindo as duas duplicatas, codificadas como a denúncia de origem e marcadas na nota. Somada às rodadas manuais, a codificação cobre as 200 denúncias da amostra, ou 198 sem as duplicatas.

A leitura foi feita caso a caso, em lotes por estrato, por `scripts/lote_codificacao.py ESTRATO N`, que imprime a narrativa e o início da capitulação de cada caso ainda não codificado. A narrativa de até 5.000 caracteres vai inteira. Acima disso vão o início (3.000), as frases do restante que tocam conta, Pix, transferência, invasão ou o denunciado (até 1.800) e o fim (600), porque é ali que a denúncia costuma identificar a conta recebedora. Foram 27 narrativas compactadas (INV 2, 3, 4, 7, 8, 11, 21, 22, 32, 36 e 43; CL 12, 15, 18, 25, 32, 34, 36 e 53; FE 7, 31, 42, 55, 79, 102, 107 e 122), e no INV 36 (GAECO, Operação Atratus) a leitura foi completada por busca dirigida no texto integral. A gravação passa por `scripts/grava_codificacao.py`, que busca o número pelo par estrato e ordem e recusa valor fora do vocabulário.

Esta codificação foi feita pelo assistente, não pelo pesquisador. Ela é um ponto de partida auditável, e a nota de cada linha resume o fato que sustenta a codificação.

### Regras aplicadas

- `papel_denunciado`: `titular_conta` quando o vínculo descrito do denunciado com o fato é a conta que recebeu o valor (cedida, vendida, emprestada ou aberta para o golpe), inclusive quando ele arregimenta contas de terceiros; `executor` quando ele fez a abordagem, o contato ou a operação sem que conta sua recebesse o valor; `misto` quando a mesma pessoa executa e recebe na própria conta, ou quando denunciados diferentes têm esses papéis distintos; `invasor`, como na r1, para o autor da invasão sem fim patrimonial ou voltada à venda de dados.
- `meio_contato`: o canal em que o golpista conversou com a vítima. O anúncio no Facebook ou na OLX seguido de conversa pelo WhatsApp fica como `whatsapp`; leilão e loja falsos ficam como `site`; `telefone` inclui ligação, SMS e aplicativo de mensagens não nomeado; `sistema` quando não houve contato com a vítima (invasão, acesso à conta).
- `pix_pagamento`: o valor saiu da vítima, ou da conta dela, para o recebedor por Pix, inclusive quando o Pix foi feito pelos golpistas de dentro da conta da vítima. A menção a Pix tentado, a Pix de pulverização posterior ou a comprovante falso de Pix não conta.
- `boleto`: a vítima pagou boleto. `invasao`: invasão de dispositivo ou acesso não autorizado a conta ou sistema, inclusive aplicativos bancários de celular roubado. A engenharia social em que a própria vítima valida o aparelho do golpista (falsa central) ficou como 0.
- `conta_do_denunciado`: o valor do fato entrou em conta de denunciado. Nos casos fora da tipologia (tráfico, anabolizantes) ficou 0 mesmo quando a denúncia menciona contas de laranjas.
- `contexto`: `violencia_domestica` segue a regra da coluna `contexto_vd` (VD narrada ou Lei 11.340 na capitulação), e as duas medidas coincidem nos 34 INV.

### Categorias acrescentadas

O vocabulário da r1 não cobria alguns casos. As categorias novas estão no dicionário `NOVOS` de `grava_codificacao.py`:

| Campo | Valor | Uso | Casos |
| --- | --- | --- | --- |
| contexto | `relacional` | conflito entre ex-parceiros ou conhecidos sem VD narrada | INV 6, 27, 39, 41 |
| contexto | `outro` | fato sem fraude patrimonial (tráfico, anabolizantes) | CL 12, 25 |
| meio_contato | `outro` | canal inexistente ou não descrito | INV 40, CL 12, CL 25, FE 23 |
| artificio | `extorsao_transferencia` | vítima constrangida, sob arma ou ameaça, a transferir ou entregar cartões e senhas | CL 1, 7, 11, 18; FE 81 |
| artificio | `taxa_antecipada` | falso empréstimo, falsa vaga ou serviço inexistente com pagamento antecipado | CL 35, 44; FE 2, 8, 9, 37, 66, 117 |
| artificio | `devassa_privacidade` | invasão para ler e divulgar comunicações, sem fim patrimonial e fora da relação de parceria | INV 39 |
| artificio | `falso_relacionamento` | perfil falso que cria vínculo afetivo e pede dinheiro | FE 96 |
| artificio | `outro` | denúncia sem fraude ou invasão (calúnia, tráfico, anabolizantes, furto de fios) | INV 40, CL 12, CL 25, FE 123 |

### Resultados (198 denúncias sem duplicatas, % ponderado dentro do estrato)

| Estrato | Papel do denunciado | Valor na conta de denunciado | Artifícios principais |
| --- | --- | --- | --- |
| INV (34) | invasor 52,9%; executor 20,6%; misto 20,6%; titular 5,9% | 23,5% | controle da parceira 26,5%; invasão de sistema com venda de dados 17,6%; sequestro de conta 14,7%; insider 11,8% |
| CL (50) | titular 87,9%; misto 10,0%; executor 2,1% | 96,5% | venda falsa 22,7%; falso parente 19,5%; falsa central 12,8% |
| FE (114) | titular 52,7%; misto 26,1%; executor 21,2% | 78,8% | venda falsa 30,3%; falso parente 20,3%; falsa central 18,9% |

O achado das rodadas manuais se confirma no corpus. Em CL o valor do fato entrou em conta de denunciado em 48 das 50 denúncias, e as duas restantes estão fora da tipologia (tráfico e anabolizantes). Em FE isso ocorre em 90 das 114, com o denunciado só como titular ou também como executor. Os 24 executores sem conta própria em FE concentram-se nas compras fraudulentas contra empresas (7, com cartão de terceiro ou comprovante falso de Pix) e no golpe do motoboy, em que o falso funcionário do banco recolhe o cartão (7), seguidos da venda falsa (4) e da maquininha (2). No INV, além dos 7 casos de VD, há 4 casos `relacionais` (ex-parceiros ou colegas) sem VD narrada.

### Regex contra a codificação assistida

`validacao_regex_assistida.csv` repete, para as 162 assistidas sem duplicatas, a comparação de `validacao_regex.csv` (rodada `a1`). A concordância foi de 0,98 em falso parente, 0,97 em invasão, 0,96 em boleto, 0,95 em WhatsApp, 0,93 em Pix, 0,90 em falsa central, 0,86 em venda falsa e 0,77 em conta do denunciado. As três últimas erram quase sempre por omissão (15, 17 e 31 falsos negativos), porque a regex não reconhece a falsa central descrita sem as palavras-chave, a venda falsa narrada como "anúncio" ou "intermediário" e a conta recebedora identificada só pelo número ou pela chave Pix. O Pix e o boleto erram por excesso, como já se sabia, porque medem menção. Como a referência aqui é a codificação assistida, a concordância mede coerência entre dois procedimentos automáticos, e não precisão.

### Casos de fronteira para conferência

- INV 6, 27 e 41: ex-parceiros, codificados `relacional` porque a denúncia não narra VD nem invoca a Lei 11.340; no INV 41 a vítima é mulher e há ameaça de divulgar fotos íntimas.
- INV 3 e 32 (mesma denúncia): `titular_conta`, porque a imputação de invasão aos três se apoia nas contas e nos repasses; `misto` seria a leitura alternativa.
- INV 36 e CL 25: denúncias do GAECO muito longas, lidas por trechos.
- FE 23 (dinâmica confusa e canal não descrito), FE 31 (triangulação no Mercado Livre sem conta dos denunciados), FE 67 (locação sem devolução, sem meio eletrônico, em `compra_fraudulenta_empresa`) e FE 97 (sistema da VR Benefícios em `invasao_sistema_bancario`).

## Sentenças dos 29 casos da matriz

Coletadas pelo Codex em 21/11/2026 com `scripts/pipe_sentencas.py`, na ordem de `dados/extracao/matriz_casos.csv`. Por caso, `pdpj_list_movimentos` com `tipo_filter="cedência"` devolve o movimento de procedência ou improcedência e o documento da sentença. A data do movimento coincidiu com a de disponibilização no cjpg em todos os casos. Em `data_sentenca` vai a data de assinatura, que no FE 39 e no FE 96 precede o movimento em três dias. O CL 1 não tem documento ligado ao movimento e foi lido pelas cinco páginas da cópia de execução, com OCR ruidoso.

Saídas: texto em `textos/tjsp/sentencas/<numero>/NN_<id>.txt` (sem a linha `Original:`), manifesto em `textos/tjsp/manifesto_sentencas.csv`, status em `dados/codex/status_sentencas.csv` e resultado em `sentencas_matriz.csv`. Este último tem uma linha por sentença, com `caso`, `numero`, `data_sentenca`, `resultado`, `capitulacao_sentenca`, `coincide_denuncia` (sim, parcial ou não), `pena` e `observacao`. São 30 linhas: os 29 casos e a sentença do corréu do CL 11, proferida em 15/10/2025 no processo de origem 1539767-78.2024.8.26.0050 e guardada na pasta do CL 11.

O resultado foi lido no dispositivo e conferido na fundamentação quando havia desclassificação, absolvição parcial ou pena fora do esperado. Não houve conferência por segundo leitor.

Resultados: 28 casos com condenação de ao menos um réu e uma absolvição integral (INV 14). A sentença diverge da capitulação da denúncia em quatro casos: FE 107 afasta o §2º-A, FE 84 requalifica o 155 §4º-B em 171 §2º-A por emendatio libelli, e CL 11 e CL 7 desclassificam a extorsão para o 171 §2º, VII (Lei 15.397/2026, de 30/04/2026, publicada em 04/05/2026), como lei mais benéfica. O FE 77, de 27/05/2026, recusou a mesma desclassificação por falta de prova de que os recursos financiassem atividade criminosa ou dela proviessem.

Conferência dos indicadores do cjpg (`amostra_tjsp.csv`) contra a leitura:

- `condena` procura "condeno" ou "julgo procedente" nos últimos 4 mil caracteres do teor e acertou 21 das 28 condenações, sem falso positivo. Perdeu quatro porque o teor do cjpg para perto de 50 mil caracteres e corta o dispositivo (FE 79, CL 18, CL 7 e INV 39; na amostra, 16 teores ficam entre 49 mil e 49,93 mil). Perdeu outras três (FE 55, FE 122, FE 54) por redação como "julgo parcialmente procedente".
- `absolve` procura "absolvo" ou "julgo improcedente" e marcou 1 dos 8 casos com absolvição de réu ou imputação. Perde "ABSOLVER o réu", "rejeito o pedido" e a absolvição dentro de procedência parcial.
- Para a amostra inteira, os dois indicadores não servem como resultado. O resultado deve vir da leitura do dispositivo, ou de regex nova validada contra estas 30 linhas.


## Sentenças da amostra (198 denúncias sem duplicatas)

Coletadas pelo Codex em 21/11/2026, depois das 29 da matriz, com `scripts/pipe_sentencas.py` (`prox`, `lote`, `djen`, `corrige`, `recalcula`) e lidas por regras em `scripts/resultado_sentenca.py`. O roteiro por caso é o da matriz: `pdpj_list_movimentos` com `tipo_filter="cedência"` dá o movimento e o documento, a leitura em lote grava o texto, e o leitor por regras preenche resultado, capitulação acolhida, pena, regime, substituição e menção à Lei 15.397/2026. Sem movimento de procedência, a lista completa de movimentos achou a extinção por prescrição (FE 46). Quando o Codex devolve a peça sem conteúdo ou a corta perto de 100 mil caracteres, o dispositivo vem da publicação no DJEN (`pdpj_buscar_comunicacoes` com o número e uma janela de duas semanas a partir do movimento), e a linha fica com `documentos=0`.

Cobertura: 197 das 198 denúncias têm sentença lida. São 162 pelo texto do Codex com o leitor por regras, 29 da matriz lidas à mão e 6 só pelo dispositivo do DJEN (INV 6, CL 20, CL 30, CL 32, FE 8 e FE 118; FE 31 e INV 2 têm texto cortado e o dispositivo do DJEN nas notas; INV 8 e INV 36 também foram cortados antes do dispositivo, sem publicação útil no DJEN, e têm o resultado só pelo movimento). Falta o FE 16 (1505916-93.2021.8.26.0554), cuja sentença de 14/11/2024 no cjpg não aparece em nenhum movimento nem no DJEN de novembro de 2024 a janeiro de 2025.

O leitor por regras acerta 30 de 30 condenações, 29 de 30 absolvições e 30 de 30 capitulações acolhidas contra `sentencas_matriz.csv` (`python3 scripts/resultado_sentenca.py valida`). Na coleta, toda sentença marcada para revisão (procedência parcial, desclassificação, menção à lei nova, divergência com o movimento) teve o dispositivo impresso e lido, e 57 linhas foram corrigidas ou anotadas à mão (`conferido=lido`). As 113 linhas restantes (`conferido=auto`) não tiveram segundo leitor. Ajustes feitos no leitor durante a coleta, cada um por um caso concreto: "rejeito o pedido de desclassificação" deixou de valer como absolvição; "deixo de condenar" deixou de valer como condenação (FE 4); "§2ºA" sem hífen passou a ser lido como §2º-A (FE 1); "10 dias multa" deixou de contar como pena de prisão (FE 45); "regime prisional aberto" passou a ser lido (FE 80); o dispositivo recua até o "ante o exposto" quando a condenação vem antes do primeiro "absolvo" (FE 102); a menção à lei nova deixou de casar com números de processo como 1539731 e passou a cobrir o inciso citado sem o número da lei (CL 43, CL 48, CL 49).

Consolidação: `python3 scripts/consolida_sentencas.py` imprime as tabelas e grava `resumo_sentencas.json`. A unidade é a denúncia sem duplicatas, com o peso do processo, e os percentuais são ponderados dentro do estrato.

| Estrato | Lidas | Ao menos um réu condenado | Absolvição integral | Capitulação acolhida nas condenações | Regime nas condenações |
| --- | --- | --- | --- | --- | --- |
| INV | 34 de 34 | 85,3% | 14,7% | 154-A 66,7%, o resto espalhado (147, 147-A, 158, 180, 171, 155, 138, 312) | aberto 57,7%, fechado 26,9% |
| CL | 50 de 50 | 94,2% | 5,8% | 171 §2º-A 31,5%, 171 sem §2º-A 25,9%, 171 §2º, VII 22,7%, 155 §4º-B 6,7% | aberto 69,8%, semiaberto 19,6% |
| FE | 113 de 114 | 87,3% | 12,1% (e 0,6% de extinção) | 171 §2º-A 82,1%, 171 sem §2º-A 15,3% | aberto 57,3%, semiaberto 27,6% |

- A sentença mantém a capitulação da denúncia em 70,4% das condenações INV, 65,8% das CL e 86,7% das FE. No CL, a mudança dominante é a desclassificação para o 171 §2º, VII (22,7%); na FE, o afastamento do §2º-A (6,7%), quase sempre para o 171 caput ou para o privilégio do §1º, contra 4,0% que acrescentam o §2º-A a uma denúncia do 171 simples.
- Penas medianas (meses, sem peso, primeira pena privativa do dispositivo): 171 §2º-A 48 no CL e na FE; 171 sem §2º-A 14,25 no CL e 12 na FE; 171 §2º, VII 12; 154-A 32 no INV.
- "Procedência parcial" junta a condenação por parte das imputações e a sentença que condena um réu e absolve outro. Por isso o movimento "Procedência" contra o texto "procedência parcial" (ou o inverso) não conta como erro; aconteceu em 9 sentenças INV, 21 CL e 19 FE.
- O movimento contradiz o texto em cinco sentenças, todas absolutórias com movimento de procedência ou procedência em parte: INV 19, CL 31, FE 4, FE 7 e FE 18. O movimento sozinho não serve como resultado.

Variável da Lei 15.397/2026 (publicada em 04/05/2026), pela data do movimento da sentença. As categorias vêm da capitulação acolhida e, para as sentenças que mencionam a lei sem aplicá-la, do dicionário `LEI_MANUAL` do `consolida_sentencas.py`, codificado pela leitura do trecho:

| Estrato | Sentenças depois da lei | Aplica o §2º, VII | Recusa | Outras menções | Sem menção | Só dispositivo |
| --- | --- | --- | --- | --- | --- | --- |
| INV | 3 | 0 | 0 | 0 | 2 | 1 |
| CL | 32 | 10 | 8 | 2 (CL 31 absolve e diz que a falta de dolo alcança o inciso; CL 37 cita a lei só como reforço do dolo) | 10 | 2 |
| FE | 39 | 1 (FE 42, por emendatio) | 2 (FE 72, FE 77) | 0 | 36 | 0 |

- Os fundamentos da recusa são de três tipos: o réu fez mais do que ceder a conta (integrou a fraude ou movimentou a conta de forma articulada: CL 10, CL 16, CL 28, CL 33); falta de prova da cessão inocente ou do vínculo com atividade criminosa (CL 49, FE 77); e direito intertemporal. No direito intertemporal estão o FE 72, que recusa por irretroatividade porque o fato é anterior à lei, o CL 36, para o qual o inciso seria mais grave que a receptação aplicada a fato anterior, e o CL 57, que mantém o caput dizendo que a lei nova não tornou atípica a conduta. A leitura oposta é a do CL 13 e da matriz (CL 7, CL 11), que aplicam o inciso a fato anterior como lei mais benéfica. O CL 48 nega a desclassificação pedida com base na nova figura sem tratar do inciso.
- Pelo ano do fato da extração (`ano_fato`, com ruído conhecido, como um 1995), quase todos os fatos julgados depois da lei são anteriores a ela, de modo que toda aplicação do inciso é retroativa.
- Na FE, 36 das 39 sentenças posteriores à lei não tratam do inciso, inclusive as que condenam o titular da conta no §2º-A.

Limitações: a pena e o regime são os do primeiro réu condenado no dispositivo; o dicionário `LEI_MANUAL` precisa ser revisto se entrar sentença nova que mencione a lei, porque o script marca essas como "menciona, sem codificar"; as linhas só com o dispositivo do DJEN não permitem dizer se a fundamentação tratou do inciso; o `ano_fato` vem da regex da denúncia e não foi conferido caso a caso.


## Reparação do art. 387, IV, do CPP e consequências do crime (questão 3)

Leitor por regras em `scripts/reparacao_387.py`, usado por `scripts/analise_q3_dano.py`, que grava `dados/analise/q3_dano.csv` e `q3_resumo.json`. A nota da questão está em `docs/analise/q3-tipologia-dano.md`.

O texto de cada sentença é a concatenação das partes gravadas sem repetição, porque a coleta repetiu o ID para forçar a saída em arquivo e várias partes são cópias idênticas. A decisão é procurada depois do fim do relatório, em cláusula com verbo de decisão na primeira pessoa ou impessoal, e as ementas transcritas são descartadas. Cada condenação recebe `rep_status` (fixa, nega, silente, indeterminado), os valores material e moral, os fundamentos da negativa, a solidariedade e a individualização pelo que entrou em cada conta (dicionários `SOLIDARIA` e `LIMITADA_CONTA`). O pedido é lido na denúncia gravada (`pedido_denuncia`, `valor_pedido`, `pedido_moral`), no relatório da sentença (`pedido_relatorio`) e no próprio texto da fixação (`pedido_dito_na_sentenca`). As consequências do crime são triadas por termos e lidas à mão nas que o leitor marca (`CONSEQ_MANUAL`), com a tipologia de Agrafiotis et al. (2018).

Validação: `python3 scripts/reparacao_387.py valida` compara com a leitura à mão das 30 sentenças da matriz (dicionário `REF`) e dá 30 de 30 no resultado, 30 de 30 no valor e 5 de 5 no fundamento da negativa. As regras foram calibradas nessas mesmas sentenças, de modo que a conferência fora da matriz foi a leitura, uma a uma, das 80 cláusulas de fixação e das 34 de negativa, e a varredura das silentes por valores e termos fora das cláusulas. Casos que viraram regra: FE 17 (citação fechada por parêntese antes do "Fixo"), FE 64 ("fica condenada"), FE 87 (valor antes do verbo), FE 88 ("determino o ressarcimento"), FE 96 ("fixo-o"), CL 54 (locução "ao pagamento do valor de R$ ... a título de reparação"), CL 57 ("a pagar para a vítima"), CL 28 (motivo na frase anterior), FE 81 ("relegar ao juízo cível"), FE 109 ("deixo de proceder"), CL 13 e CL 43 (total e parcelas). Correções à mão em `CORRECAO`: FE 103 (a indenização é o valor da fiança), FE 125 (valor sem cifrão) e as seis lidas só pelo DJEN (FE 8, FE 118, CL 20 e CL 32 com reparação na nota da coleta; INV 6 e CL 30 indeterminadas). O detector do pedido na denúncia foi conferido em 16 positivos e 16 negativos sorteados; FE 67 e FE 109 viraram regra, e FE 124 ("deixo de requerer") conta como recusa expressa do MP. Não houve segundo leitor.

Resultados (175 condenações, % ponderado dentro do estrato): a reparação é fixada em 14,3% das condenações INV, 53,1% das CL e 47,7% das FE, negada com fundamento em 17,9%, 22,2% e 22,1%, e omitida nas demais. O dano moral foi fixado em três sentenças (INV 39, INV 44, FE 21). As consequências do crime pesaram na pena em 25 sentenças, com dano não econômico nomeado em 10.
