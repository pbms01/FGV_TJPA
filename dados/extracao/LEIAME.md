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

## Distribuição pela capitulação (sem duplicatas, % ponderado dentro do estrato)

- INV, 34 denúncias: 154-A 28 (82,4%), outro tipo 2, 155 2, lavagem 1, 171 §2º-A 1.
- CL, 50: 171 §2º-A 23 (47,3%), 171 sem §2º-A 14 (27,8%), 155 §4º-B 5 (10,7%), 158 2, 180 2, 155 comum 2, lavagem 1, drogas 1. Nenhuma denúncia capitula o 171 §2º, VII.
- FE, 114: 171 §2º-A 100 (86,3%), 171 sem §2º-A 11 (10,8%), 155 comum 2, 155 §4º-B 1.

## Unidade de análise

A unidade principal é a denúncia, sem as duplicatas, com o peso amostral do processo. O processo é a unidade do sorteio, e as duas duplicatas saem das contagens. O tipo de análise é o da capitulação (`tipo_capitulacao`), cruzado com o estrato de origem. A estimativa de incidência dentro de cada estrato usa o peso. O denunciado fica como unidade secundária, para as perguntas sobre papel (titular da conta, autor da fraude) e concurso, e depende da codificação manual.

## Pendências

- Codificar manualmente o meio e o papel do denunciado numa subamostra, para medir a precisão das regex `m_*`.
- Conferir na sentença a capitulação de INV 35 (155-A).
