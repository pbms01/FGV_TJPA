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

## Validação por leitura (rodada 1)

Foram lidas as capitulações dos alertas do estrato INV, dos casos sem capitulação e de oito processos sorteados (semente 7). Os oito sorteados tiveram tipo, artigos, valor e ano corretos. Os 17 alertas `estrato_fe_sem_2A` (FE capitulados como 171 sem §2º-A, 155 ou 155 §4º-B) ainda não foram lidos um a um.

Os casos de estrato sem o tipo esperado são, em regra, denúncias reais de outro tipo, porque o estrato veio da sentença (CJPG) e não da denúncia:

- INV 3 (0001915-31.2023.8.26.0050): a peça salva é uma manifestação sobre prisão preventiva, não a denúncia. Precisa de nova leitura no Codex.
- INV 22 (1503431-80.2021.8.26.0050): o texto do Codex vem cortado na página 16 de 24, antes da capitulação. A cota informa a imputação de 154-A (invasão de banco de dados da Polícia Civil). Precisa de nova leitura.
- INV 36 (1007980-49.2022.8.26.0506), GAECO de Ribeirão Preto, Operação Atratus: a capitulação imputa organização criminosa (Lei 12.850) e lavagem. O 154-A aparece apenas na narrativa, como crime antecedente.
- INV 35 (1521208-63.2020.8.26.0228): a capitulação diz "artigos 155-A e parágrafo 2º". Provável erro material por 154-A, a conferir na sentença.
- INV 5, 10, 14 e 40: denúncias de estelionato eletrônico (171 §2º-A), de peculato com 313-A, de furto em violência doméstica e de calúnia (art. 138). O 154-A entrou pela sentença ou por outro réu.
- INV 7 (0000455-37.2024.8.26.0482): a denúncia é idêntica à do INV 2 (1500431-37.2021.8.26.0482), com hash igual nas quatro partes; é um desmembramento. Para contagem por denúncia, fica só o processo originário.
- CL 25 (0030316-06.2018.8.26.0506): organização criminosa de anabolizantes (273 CP), com contas de laranjas usadas para lavagem.

## Pendências

- Reler INV 3 e INV 22 no Codex.
- Decidir a unidade de análise (processo, denúncia ou denunciado) e o tratamento das denúncias de outro tipo dentro dos estratos.
- Codificar manualmente meio e papel do denunciado numa subamostra, para medir a precisão das regex.
