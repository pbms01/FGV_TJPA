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
