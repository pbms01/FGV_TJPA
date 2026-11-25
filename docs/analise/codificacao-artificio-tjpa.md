# Codificação do artifício nas denúncias do TJPA (leitura assistida, com segundo leitor)

Nota de 23/11/2026. Primeira codificação do artifício no TJPA, feita para pôr a base no formato do gráfico das famílias de artifício do TJSP, conferida no mesmo dia por segundo leitor cego numa amostra e com a adjudicação das divergências revista contra o texto integral. Base: as 196 denúncias com texto em `textos/tjpa/denuncias/` no ramo main de pbms01/FGV_TJPA (commit 1006135), menos 13 duplicatas, o que dá 183 denúncias. Duplicatas: 12 por texto idêntico (a família do originário 0802159-03.2025, com seis desmembramentos; a do originário 0820198-53.2022, com quatro; Santa Maria do Pará, 0800267-58.2024 com o originário 0800643-78.2023; e 0818456-51.2026, cópia de 0000586-02.2021) e o 0817567-05.2023, que leva o aditamento da família da 10ª Vara, como na extração descrita em `claude/extracao-tjpa-fase2.md`. Os códigos PA seguem a regra daquela extração (estrato pelo rótulo do DJEN, na ordem INV, CL, FE, e ordem na fila).

Método. Para cada denúncia, li a abertura da narrativa (cerca de 1.100 caracteres a partir da seção dos fatos) e, quando ela não bastava, trechos adiante, e atribuí um único valor do campo `artificio` do livro de códigos do TJSP (`dados/conferencia/livro_codigos_denuncias.md`), pelo fato principal. A família segue o mapeamento de `scripts/servico_banco.py` e a regra que reproduz o gráfico do TJSP: controle da parceira, devassa, venda de dados e acesso interno formam a sexta família; `outro` é fora da tipologia; a taxa antecipada que imita oferta (falso sorteio, PA-FE 67; falsa vaga, PA-FE 81) vai para imita oferta, como CL 44, FE 9 e FE 117 no TJSP. A sexta família foi renomeada para "ataca sistema ou usa acesso interno", porque no TJPA ela reúne cinco desvios de dinheiro da própria vítima por quem tinha acesso (PA-CL 88, PA-FE 54, PA-FE 99, PA-FE 166, PA-FE 206), o que o rótulo do TJSP, "sem dinheiro da vítima", não descreve. Só o artifício foi codificado (sem meio, papel ou indicadores).

## No repositório

Gravado no main de pbms01/FGV_TJPA em 25/11/2026, a pedido do pesquisador. Os arquivos de trabalho de 23/11/2026 (o JSON da codificação, os excertos, o CSV da segunda leitura e o gráfico) ficaram na conversa em que a codificação foi feita e não chegaram ao repositório; o que está aqui foi reconstituído da tabela e do quadro de adjudicação desta nota, sem nova leitura das denúncias.

- `docs/analise/codificacao-artificio-tjpa.md`: esta nota, espelhada no Project como `claude/codificacao-artificio-tjpa.md`.
- `dados/extracao/codificacao_artificio_tjpa.csv`: uma linha por denúncia sem duplicata (183), com `codigo`, `numero`, `estrato`, `ordem` (posição na fila da coleta), `artificio`, `familia`, `segundo_leitor` (`amostra`, `fronteira` ou vazio), `primeira_leitura`, `segunda_leitura` (vazia fora da amostra) e `nota`. Nos 58 casos da amostra sem divergência, a primeira e a segunda leitura são iguais ao valor final, por construção.
- `dados/conferencia/tjpa/adjudicacao_artificio.csv`: as 17 divergências, com as colunas de `dados/conferencia/adjudicacao.csv` (`id`, `caso`, `bloco`, `campo`, `primeira`, `segunda`, `final`, `decisao`, `motivo`) e mais `numero` e `parte`.
- `scripts/artificio_tjpa.py`: `importa` refaz os dois CSV a partir desta nota; sem argumento, confere os CSV contra a fila da coleta, os rótulos do DJEN, os textos gravados, o mapeamento de famílias de `scripts/servico_banco.py` e os números da seção "Resultado".

## Segundo leitor

Outra instância do mesmo modelo, sem acesso à primeira leitura, ao Project nem à memória, codificou o artifício de 75 denúncias pelo mesmo livro, com trechos de 3.000 caracteres em ordem embaralhada e o texto integral à disposição (abriu cinco). A amostra tem duas partes: 53 por sorteio estratificado (as 11 INV, as 12 CL e 30 FE, semente 20261123), que medem a concordância, e 22 casos de fronteira escolhidos por mim, que não entram na medida.

| Parte | n | Artifício: concordância | kappa | Família: concordância | kappa |
| --- | --- | --- | --- | --- | --- |
| Amostra sorteada | 53 | 86,8% | 0,85 | 94,3% | 0,93 |
| Casos de fronteira | 22 | 54,5% | 0,48 | 59,1% | 0,51 |

Das 17 divergências, a adjudicação adotou o segundo leitor em 14, a primeira leitura em 2 (PA-FE 36 e PA-FE 90) e um terceiro valor em 1 (PA-FE 113, falsa central). Nove mudaram de família, todas na FE. A adjudicação foi revista em seguida, com releitura integral das 17 denúncias, e só o PA-FE 54 mudou: a primeira adjudicação lhe dera inserção de dados, terceiro valor, e a revisão adotou insider_empresa, como propusera o segundo leitor, porque a denúncia narra a funcionária lançando o empréstimo no sistema da própria loja, que é a definição literal do livro. A revisão também procurou, nas denúncias fora da amostra codificadas em compra fraudulenta, acesso interno e inserção de dados, empregado, gerente ou correspondente agindo como agente; as três ocorrências (PA-FE 34, 48 e 154) são empregados da loja vítima que atenderam o golpista, e nenhum caso fora da amostra mudou. A conferência confirma a regra na amostra e mostra que a fronteira entre as famílias que imitam e as que atacam a conta, e entre compra fraudulenta e inserção de dados, é onde a leitura de trecho mais erra; o fundamento de cada decisão está abaixo. As 108 denúncias fora da amostra têm só a primeira leitura.

| Código | Parte | Primeira | Segunda | Final | Fundamento |
| --- | --- | --- | --- | --- | --- |
| PA-FE 112 | fronteira | falso_conhecido | taxa_antecipada | taxa_antecipada | segundo leitor: o perfil falso de político oferece cheque moradia e emprego mediante pagamento; a vítima não o conhecia, e o expediente é a taxa |
| PA-FE 113 | fronteira | taxa_antecipada | venda_falsa | falsa_central | nenhum dos dois: a empresa de nome semelhante se passa pela administradora de consórcios credenciada pelo BCB (se passa por financeira) |
| PA-FE 144 | fronteira | taxa_antecipada | venda_falsa | venda_falsa | segundo leitor: o anúncio é de um Onix pago e não entregue; a administradora de consórcio é a fachada do vendedor |
| PA-FE 158 | fronteira | compra_fraudulenta_empresa | falso_conhecido | falso_conhecido | segundo leitor, confiança média: o Pix sai quando o fraudador se apresenta como o conhecido da vítima que recebera o falso pagamento a maior |
| PA-FE 177 | fronteira | insercao_dados_falsos | compra_fraudulenta_empresa | compra_fraudulenta_empresa | segundo leitor: conta e cartão abertos em nome da tia com os documentos e a biometria dela, como no PA-FE 93 |
| PA-FE 206 | fronteira | outro | insider_empresa | insider_empresa | segundo leitor: o recepcionista desvia as vendas da maquininha do hotel para conta aberta em nome do pai |
| PA-FE 207 | sorteada | invasao_sistema_bancario | falsa_central | falsa_central | segundo leitor: falso funcionário do Banpará obtém o token por telefone para a transferência |
| PA-FE 28 | sorteada | outro | compra_fraudulenta_empresa | compra_fraudulenta_empresa | segundo leitor, confiança baixa: o livro põe a locação sem devolução em compra fraudulenta, embora a vítima seja pessoa física, e outro é só para fato sem fraude |
| PA-FE 36 | fronteira | insercao_dados_falsos | insider_empresa | insercao_dados_falsos | primeira leitura: o dono da própria promotora abre conta no Agibank sem consentimento, e a denúncia não narra vínculo de correspondente nem acesso interno ao sistema do banco; segue o INV 36 do TJSP, e migra para insider_empresa se a instrução mostrar a promotora como correspondente |
| PA-FE 54 | fronteira | falsa_central | insider_empresa | insider_empresa | segundo leitor, na revisão: a funcionária da Gazin capta os dados por link, lança no sistema da própria loja o empréstimo de R$ 1.300 em nome da cliente e recebe o valor (a primeira adjudicação dera insercao_dados_falsos) |
| PA-FE 73 | sorteada | falsa_central | compra_fraudulenta_empresa | compra_fraudulenta_empresa | segundo leitor, confiança média: apólice falsa apresentada pelo fornecedor para a empresa liberar pagamento, análoga ao comprovante falso |
| PA-FE 90 | fronteira | insercao_dados_falsos | compra_fraudulenta_empresa | insercao_dados_falsos | primeira leitura, confiança baixa: empréstimos e cartão em nome do idoso; a denúncia não descreve o ardil |
| PA-FE 168 | sorteada | insercao_dados_falsos | invasao_sistema_bancario | invasao_sistema_bancario | segundo leitor: o agente acessa a conta digital da vítima e transfere o crédito |
| PA-FE 209 | sorteada | falsa_central | taxa_antecipada | taxa_antecipada | segundo leitor: promessa de quitar o consignado e transferência antecipada à falsa assessoria |
| PA-FE 45 | sorteada | falsa_central | taxa_antecipada | taxa_antecipada | segundo leitor: a vítima paga R$ 1.000 antecipados pelo falso repasse do governo |
| PA-FE 71 | fronteira | insercao_dados_falsos | invasao_sistema_bancario | invasao_sistema_bancario | segundo leitor: além do empréstimo, transferências da conta do idoso para a agente sem consentimento |
| PA-INV 131 | sorteada | insider_empresa | invasao_sistema_venda_dados | invasao_sistema_venda_dados | segundo leitor: ex-funcionários, já sem vínculo, entram no sistema com senha de funcionário para extrair clientes |

## Resultado

| Família | INV (11) | CL (12) | FE (160) |
| --- | --- | --- | --- |
| imita instituição | 0 | 0 | 31 |
| imita oferta | 0 | 5 | 50 |
| imita relação pessoal | 0 | 2 | 26 |
| manipula o pagamento | 0 | 0 | 24 |
| ataca a conta ou o aparelho | 3 | 4 | 24 |
| ataca sistema ou usa acesso interno | 8 | 1 | 4 |
| fora da tipologia | 0 | 0 | 1 |

Na FE, a venda falsa sozinha soma 47 de 160, seguida da compra fraudulenta (22), do falso parente (21), da falsa central (17) e da invasão de conta ou sistema bancário (16, entre elas cinco denúncias da Operação Trojan e os chupa-cabras sem contato com a vítima). A família que ataca a conta ou o aparelho tem 24 das 160 denúncias FE, contra 5 de 114 no gráfico do TJSP. As contagens são simples, porque a base do TJPA é censo do que o DJEN publicou.

Ressalva de leitura. Depois da revisão, ataca a conta ou o aparelho e manipula o pagamento empatam em 24 na FE, e a ordem entre as duas não é robusta. Quatro decisões de confiança reduzida (PA-FE 28, 73, 90 e 158) mudariam de família se lidas pela alternativa, e basta o PA-FE 90 passar a compra fraudulenta para inverter aquela ordem. O gráfico não deve ser lido como diferença entre essas duas famílias.

## Tabela

| Código | Número | Estrato | Artifício | Família | Segundo leitor | Nota |
| --- | --- | --- | --- | --- | --- | --- |
| PA-INV 23 | 0000410-23.2021.8.14.0401 | INV | invasao_sistema_bancario | ataca a conta ou o aparelho | amostra | Operação Trojan: dados bancários, malware e troca de senha na central do banco |
| PA-INV 29 | 0814654-84.2022.8.14.0401 | INV | controle_parceira | ataca sistema ou usa acesso interno | amostra | ex-namorado, violência psicológica e invasão de dispositivo |
| PA-INV 56 | 0021621-23.2018.8.14.0401 | INV | controle_parceira | ataca sistema ou usa acesso interno | amostra | ex-companheiro furta aparelhos, acessa o e-mail dela e escreve em seu nome |
| PA-INV 59 | 0801803-28.2022.8.14.0008 | INV | controle_parceira | ataca sistema ou usa acesso interno | amostra | programa espião no celular da ex-companheira e ameaça de divulgar conteúdo íntimo |
| PA-INV 68 | 0800532-36.2022.8.14.0023 | INV | controle_parceira | ataca sistema ou usa acesso interno | amostra | ex-companheiro incendeia a casa, leva o celular e posta em nome dela |
| PA-INV 94 | 0009738-16.2017.8.14.0013 | INV | devassa_privacidade | ataca sistema ou usa acesso interno | amostra | celular comprado da vítima, backup recuperado e fotos íntimas divulgadas a colegas |
| PA-INV 107 | 0019953-80.2019.8.14.0401 | INV | sequestro_conta | ataca a conta ou o aparelho | amostra | código do WhatsApp obtido por falso funcionário da OLX e pedidos de dinheiro a conhecidos |
| PA-INV 125 | 0802231-20.2022.8.14.0037 | INV | roubo_celular_invasao | ataca a conta ou o aparelho | amostra | receptação de celulares roubados e invasão para apagar dados e revender |
| PA-INV 131 | 0818615-96.2023.8.14.0401 | INV | invasao_sistema_venda_dados | ataca sistema ou usa acesso interno | amostra | Ex-funcionário usa senha de funcionário para acessar chat de clientes da empresa e desviar clientela ao concorrente [adjudicação do segundo leitor, 23/11/2026: primeira leitura insider_empresa, segunda invasao_sistema_venda_dados] |
| PA-INV 182 | 0800337-36.2021.8.14.0007 | INV | devassa_privacidade | ataca sistema ou usa acesso interno | amostra | queixa-crime: acesso a comunicações privadas de ex-colega e ameaça de divulgação |
| PA-INV 214 | 0800436-02.2024.8.14.0136 | INV | controle_parceira | ataca sistema ou usa acesso interno | amostra | companheiro invade as redes sociais e troca as senhas |
| PA-CL 5 | 0825125-62.2022.8.14.0401 | CL | invasao_sistema_bancario | ataca a conta ou o aparelho | amostra | acessa a conta bancária da empresa vítima e transfere para a própria conta |
| PA-CL 6 | 0805119-21.2023.8.14.0006 | CL | falso_relacionamento | imita relação pessoal | amostra | perfil no Facebook com troca de fotos íntimas e pedidos de dinheiro |
| PA-CL 16 | 0000586-02.2021.8.14.0401 | CL | invasao_sistema_bancario | ataca a conta ou o aparelho | amostra | Operação Trojan: dados bancários, malware e troca de senha na central do banco |
| PA-CL 35 | 0800326-11.2023.8.14.0080 | CL | venda_falsa | imita oferta | amostra | loja de roupas no Instagram e WhatsApp, Pix para a conta da denunciada |
| PA-CL 38 | 0804309-46.2023.8.14.0006 | CL | venda_falsa | imita oferta | amostra | imóvel anunciado na OLX, pagamento à suposta proprietária |
| PA-CL 39 | 0014826-69.2016.8.14.0401 | CL | venda_falsa | imita oferta | amostra | venda enganosa de casa da Cohab com cheque moradia, 2013 a 2016 |
| PA-CL 60 | 0810363-70.2024.8.14.0401 | CL | roubo_celular_invasao | ataca a conta ou o aparelho | amostra | roubo de celulares de motoristas de aplicativo e Pix para a conta do denunciado |
| PA-CL 61 | 0010324-06.2019.8.14.0006 | CL | venda_falsa | imita oferta | amostra | venda de moto na OLX com pagamento a conta de terceira e furto do veículo no dia seguinte |
| PA-CL 76 | 0804049-11.2024.8.14.0401 | CL | extorsao_transferencia | ataca a conta ou o aparelho | amostra | vítima rendida e levada a cativeiro, com transferências |
| PA-CL 88 | 0802801-36.2021.8.14.0006 | CL | insider_empresa | ataca sistema ou usa acesso interno | amostra | gestora financeira do sindicato com senhas e token transfere para familiares |
| PA-CL 95 | 0815181-65.2024.8.14.0401 | CL | venda_falsa | imita oferta | amostra | geladeira anunciada no Marketplace do Facebook |
| PA-CL 123 | 0804452-98.2024.8.14.0006 | CL | falso_parente | imita relação pessoal | amostra | WhatsApp se passando pelo filho para pagar boleto |
| PA-FE 1 | 0806056-44.2022.8.14.0401 | FE | invasao_sistema_bancario | ataca a conta ou o aparelho |  | portabilidade do salário da vítima sem conhecimento e Pix ao denunciado |
| PA-FE 2 | 0813962-22.2021.8.14.0401 | FE | falso_parente | imita relação pessoal |  | WhatsApp se passando por familiar de idosa |
| PA-FE 3 | 0801007-56.2021.8.14.0401 | FE | falso_conhecido | imita relação pessoal |  | WhatsApp com o número de uma amiga pedindo empréstimo |
| PA-FE 7 | 0801359-37.2023.8.14.0015 | FE | venda_falsa | imita oferta |  | leilão virtual fraudulento de motocicleta (site Leilão do Pará Oficial) |
| PA-FE 10 | 0003478-80.2013.8.14.0006 | FE | invasao_sistema_bancario | ataca a conta ou o aparelho | fronteira | chupa-cabra em caixa eletrônico e saques nas contas dos clientes |
| PA-FE 11 | 0021956-42.2018.8.14.0401 | FE | falso_relacionamento | imita relação pessoal |  | perfil de general americano no Facebook e conversa amorosa |
| PA-FE 13 | 0813146-35.2024.8.14.0401 | FE | venda_falsa | imita oferta |  | golpe na compra, venda e financiamento de veículo |
| PA-FE 14 | 0821266-04.2023.8.14.0401 | FE | falsa_central | imita instituição | amostra | SMS de compra falsa e orientações por telefone para Pix |
| PA-FE 15 | 0000548-87.2021.8.14.0401 | FE | invasao_sistema_bancario | ataca a conta ou o aparelho |  | Operação Trojan: dados bancários, malware e troca de senha na central do banco |
| PA-FE 17 | 0819528-15.2022.8.14.0401 | FE | falsa_central | imita instituição |  | ligação de suposta gerente do Banpará |
| PA-FE 19 | 0814230-71.2024.8.14.0401 | FE | compra_fraudulenta_empresa | manipula o pagamento |  | compras em loja com cartões depois contestados |
| PA-FE 20 | 0801938-63.2022.8.14.0065 | FE | compra_fraudulenta_empresa | manipula o pagamento | amostra | comprovante falso a vendedores no Facebook para retirar os bens |
| PA-FE 21 | 0000533-21.2021.8.14.0401 | FE | invasao_sistema_bancario | ataca a conta ou o aparelho | amostra | Operação Trojan: dados bancários, malware e troca de senha na central do banco |
| PA-FE 22 | 0814514-45.2025.8.14.0401 | FE | venda_falsa | imita oferta | amostra | instalação de placas solares contratada e não feita |
| PA-FE 24 | 0824890-27.2024.8.14.0401 | FE | invasao_sistema_bancario | ataca a conta ou o aparelho |  | Pix não autorizado pela vítima, falha de autenticação do banco explorada |
| PA-FE 25 | 0803124-27.2024.8.14.0009 | FE | venda_falsa | imita oferta | amostra | Operação Arremate: leilão falso do Detran em site hospedado no exterior |
| PA-FE 26 | 0805335-87.2025.8.14.0401 | FE | venda_falsa | imita oferta |  | venda de euros por suposta agente de turismo, nunca entregues |
| PA-FE 27 | 0816542-54.2023.8.14.0401 | FE | compra_fraudulenta_empresa | manipula o pagamento |  | compra tentada em e-commerce com CPF de terceiro |
| PA-FE 28 | 0800055-72.2024.8.14.0013 | FE | compra_fraudulenta_empresa | manipula o pagamento | amostra | Pega veículo emprestado a pretexto de locá-lo à HYDRO, não devolve e o vende pelo WhatsApp a terceiro [adjudicação do segundo leitor, 23/11/2026: primeira leitura outro, segunda compra_fraudulenta_empresa] |
| PA-FE 30 | 0818513-11.2022.8.14.0401 | FE | falso_parente | imita relação pessoal |  | WhatsApp se passando pela tia |
| PA-FE 31 | 0810382-65.2023.8.14.0028 | FE | compra_fraudulenta_empresa | manipula o pagamento |  | comprovantes de Pix falsos para pagar a escola |
| PA-FE 32 | 0003882-76.2014.8.14.0013 | FE | invasao_sistema_bancario | ataca a conta ou o aparelho | fronteira | chupa-cabra em caixas eletrônicos |
| PA-FE 33 | 0811342-58.2021.8.14.0006 | FE | compra_fraudulenta_empresa | manipula o pagamento | amostra | compras de celulares com o cartão de crédito da vítima |
| PA-FE 34 | 0824223-12.2022.8.14.0401 | FE | compra_fraudulenta_empresa | manipula o pagamento |  | compra em loja de roupas por WhatsApp com pagamento fraudado |
| PA-FE 36 | 0800819-77.2025.8.14.0060 | FE | insercao_dados_falsos | ataca a conta ou o aparelho | fronteira | promotora de crédito abre conta sem consentimento e desvia benefício de idosos [adjudicação do segundo leitor, 23/11/2026: primeira leitura insercao_dados_falsos, segunda insider_empresa] |
| PA-FE 37 | 0817590-64.2023.8.14.0040 | FE | venda_falsa | imita oferta | amostra | moto anunciada em perfil falso no Facebook |
| PA-FE 41 | 0815190-27.2024.8.14.0401 | FE | falsa_central | imita instituição |  | ligação de suposto gerente do Banpará |
| PA-FE 42 | 0809824-96.2022.8.14.0006 | FE | roubo_celular_invasao | ataca a conta ou o aparelho |  | celular esquecido furtado e transferência pelo aplicativo |
| PA-FE 44 | 0805412-04.2022.8.14.0401 | FE | falso_parente | imita relação pessoal | amostra | WhatsApp com a foto da filha |
| PA-FE 45 | 0803104-11.2023.8.14.0061 | FE | taxa_antecipada | imita instituição | amostra | Promessa de repasse do Governo a aposentados, finge falar com servidor do INSS; vítima paga R$1.000, entrega cartão e senha; empréstimos [adjudicação do segundo leitor, 23/11/2026: primeira leitura falsa_central, segunda taxa_antecipada] |
| PA-FE 46 | 0812575-64.2024.8.14.0401 | FE | falso_parente | imita relação pessoal |  | WhatsApp se passando pela filha |
| PA-FE 47 | 0802544-82.2024.8.14.0401 | FE | maquininha | manipula o pagamento |  | falso presente de aniversário e maquininha adulterada |
| PA-FE 48 | 0801497-10.2023.8.14.0401 | FE | compra_fraudulenta_empresa | manipula o pagamento |  | compra de cerveja com Pix simulado |
| PA-FE 49 | 0800533-86.2023.8.14.0087 | FE | roubo_celular_invasao | ataca a conta ou o aparelho |  | celular furtado e transferências da conta da vítima |
| PA-FE 51 | 0803456-37.2021.8.14.0061 | FE | falso_advogado | imita instituição |  | falsa advogada cobrando por benefícios do INSS |
| PA-FE 52 | 0819887-96.2021.8.14.0401 | FE | compra_fraudulenta_empresa | manipula o pagamento |  | pedidos de entrega de carnes pagos com fraude bancária |
| PA-FE 53 | 0804511-02.2023.8.14.0401 | FE | venda_falsa | imita oferta |  | caminhonete anunciada na OLX por falso sargento |
| PA-FE 54 | 0802658-21.2024.8.14.0013 | FE | insider_empresa | ataca sistema ou usa acesso interno | fronteira | funcionária da loja capta os dados da cliente por link de falsa validação de garantia e lança empréstimo em nome dela no sistema da loja [adjudicação do segundo leitor, 23/11/2026: primeira leitura falsa_central, segunda insider_empresa; na revisão da adjudicação, adotada a segunda] |
| PA-FE 57 | 0005766-67.2019.8.14.0401 | FE | falsa_central | imita instituição |  | ligações de falsa gerente do Banco do Brasil a idosa |
| PA-FE 58 | 0813074-82.2023.8.14.0401 | FE | venda_falsa | imita oferta |  | site de vendas com produto não entregue |
| PA-FE 62 | 0012873-31.2020.8.14.0401 | FE | venda_falsa | imita oferta | amostra | moto anunciada pela vítima na OLX, golpe do intermediário |
| PA-FE 63 | 0000352-20.2021.8.14.0401 | FE | invasao_sistema_bancario | ataca a conta ou o aparelho |  | Operação Trojan: dados bancários, malware e troca de senha na central do banco |
| PA-FE 64 | 0804578-58.2023.8.14.0015 | FE | compra_fraudulenta_empresa | manipula o pagamento | fronteira | cadastro com documentos extraviados de terceira em revendedora de cosméticos |
| PA-FE 65 | 0815210-18.2024.8.14.0401 | FE | venda_falsa | imita oferta |  | planos de academia vendidos abaixo do preço e não contratados |
| PA-FE 66 | 0819889-84.2022.8.14.0028 | FE | compra_fraudulenta_empresa | manipula o pagamento | amostra | comprovantes de Pix falsificados em delivery de açaí |
| PA-FE 67 | 0803061-73.2022.8.14.0008 | FE | taxa_antecipada | imita oferta | fronteira | falso sorteio de iPhone em nome de loja, com cobrança de frete |
| PA-FE 69 | 0800643-78.2023.8.14.0057 | FE | maquininha | manipula o pagamento |  | troca da maquininha do frentista no posto de combustível |
| PA-FE 70 | 0010101-78.2020.8.14.0051 | FE | sequestro_conta | ataca a conta ou o aparelho | amostra | falso convite do Gshow e código do WhatsApp entregue pela vítima |
| PA-FE 71 | 0800118-17.2024.8.14.0072 | FE | invasao_sistema_bancario | ataca a conta ou o aparelho | fronteira | Quem guardava documentos do idoso analfabeto fez empréstimo e transferências da conta dele para si sem consentimento [adjudicação do segundo leitor, 23/11/2026: primeira leitura insercao_dados_falsos, segunda invasao_sistema_bancario] |
| PA-FE 72 | 0802098-73.2024.8.14.0015 | FE | boleto_falso | imita instituição |  | boletos falsos de energia emitidos por conta de fachada (Recolhi Pag Energia) |
| PA-FE 73 | 0822630-11.2023.8.14.0401 | FE | compra_fraudulenta_empresa | manipula o pagamento | amostra | Envio por e-mail de apólice de seguro-garantia falsa à Equatorial para liberar aditamento de R$5,8 mi [adjudicação do segundo leitor, 23/11/2026: primeira leitura falsa_central, segunda compra_fraudulenta_empresa] |
| PA-FE 74 | 0805971-87.2024.8.14.0401 | FE | falso_parente | imita relação pessoal |  | WhatsApp, golpe do falso parente |
| PA-FE 75 | 0820374-48.2025.8.14.0006 | FE | compra_fraudulenta_empresa | manipula o pagamento |  | pedidos por WhatsApp a loja de suplementos em nome de pessoas diversas |
| PA-FE 77 | 0800838-69.2021.8.14.0401 | FE | invasao_sistema_bancario | ataca a conta ou o aparelho |  | Pix da conta da vítima no Banpará depois de cadastro de dispositivo |
| PA-FE 78 | 0013033-56.2020.8.14.0401 | FE | venda_falsa | imita oferta |  | veículo anunciado pela vítima na OLX, golpe do intermediário |
| PA-FE 79 | 0823940-81.2025.8.14.0401 | FE | falsa_central | imita instituição |  | ligação de falso funcionário do Bradesco |
| PA-FE 80 | 0815331-80.2023.8.14.0401 | FE | falsa_central | imita instituição |  | ligação de falso funcionário do Banco do Brasil |
| PA-FE 81 | 0819144-86.2021.8.14.0401 | FE | taxa_antecipada | imita oferta | fronteira | falsa vaga de secretária em hospital, com cobrança de passagem e certificado |
| PA-FE 82 | 0803127-79.2024.8.14.0009 | FE | venda_falsa | imita oferta |  | falsas leiloeiras com cartas de arrematação e logotipo do Detran |
| PA-FE 83 | 0819275-56.2024.8.14.0401 | FE | venda_falsa | imita oferta |  | PS4 anunciado na OLX |
| PA-FE 84 | 0814661-08.2024.8.14.0401 | FE | roubo_celular_invasao | ataca a conta ou o aparelho | amostra | roubo do carro e do celular e pedido de dinheiro ao irmão em nome da vítima |
| PA-FE 85 | 0818547-41.2021.8.14.0006 | FE | venda_falsa | imita oferta |  | venda de apartamento por imobiliária e falsa corretora |
| PA-FE 86 | 0800169-85.2024.8.14.0053 | FE | roubo_celular_invasao | ataca a conta ou o aparelho |  | roubo de bolsa com celular e cartões de idoso |
| PA-FE 89 | 0800121-52.2024.8.14.0401 | FE | venda_falsa | imita oferta |  | veículo anunciado na OLX |
| PA-FE 90 | 0800263-98.2021.8.14.0033 | FE | insercao_dados_falsos | ataca a conta ou o aparelho | fronteira | conhecido leva o idoso a contratar empréstimos e pede cartão em nome dele [adjudicação do segundo leitor, 23/11/2026: primeira leitura insercao_dados_falsos, segunda compra_fraudulenta_empresa] |
| PA-FE 91 | 0000323-67.2021.8.14.0401 | FE | invasao_sistema_bancario | ataca a conta ou o aparelho |  | Operação Trojan: dados bancários, malware e troca de senha na central do banco |
| PA-FE 92 | 0007684-09.2019.8.14.0401 | FE | venda_falsa | imita oferta |  | anúncio clonado de moto na OLX |
| PA-FE 93 | 0802578-85.2023.8.14.0015 | FE | compra_fraudulenta_empresa | manipula o pagamento | fronteira | CNH da vítima fraudada para abrir conta e obter cartão no Banco do Brasil |
| PA-FE 96 | 0802613-17.2024.8.14.0401 | FE | venda_falsa | imita oferta |  | veículo anunciado na OLX |
| PA-FE 97 | 0801263-28.2023.8.14.0401 | FE | invasao_sistema_bancario | ataca a conta ou o aparelho | amostra | transferências indevidas pelo sistema do Banpará para contas dos denunciados |
| PA-FE 98 | 0800205-87.2023.8.14.0401 | FE | falso_parente | imita relação pessoal |  | WhatsApp se passando pelo sobrinho |
| PA-FE 99 | 0811772-81.2024.8.14.0401 | FE | insider_empresa | ataca sistema ou usa acesso interno | fronteira | funcionários alteram boletos no sistema de pagamentos do grupo varejista |
| PA-FE 100 | 0800422-90.2025.8.14.0133 | FE | venda_falsa | imita oferta | amostra | negociação de imóvel por indicação, com valores desviados |
| PA-FE 102 | 0821605-60.2023.8.14.0401 | FE | invasao_sistema_bancario | ataca a conta ou o aparelho | fronteira | vizinho de confiança usa as senhas do idoso e transfere |
| PA-FE 103 | 0824635-06.2023.8.14.0401 | FE | venda_falsa | imita oferta |  | site de leilões falso |
| PA-FE 106 | 0808038-25.2024.8.14.0401 | FE | falso_parente | imita relação pessoal |  | WhatsApp se passando pela filha |
| PA-FE 108 | 0822617-12.2023.8.14.0401 | FE | venda_falsa | imita oferta |  | veículos inexistentes anunciados em plataformas de venda |
| PA-FE 109 | 0800780-28.2023.8.14.0003 | FE | venda_falsa | imita oferta |  | negociação de carro e moto com Pix ao denunciado |
| PA-FE 110 | 0802367-50.2026.8.14.0401 | FE | falsa_central | imita instituição |  | link falso do Banco do Brasil sobre pontos Livelo |
| PA-FE 111 | 0809175-47.2021.8.14.0401 | FE | venda_falsa | imita oferta |  | leilão falso do Detran |
| PA-FE 112 | 0818196-13.2022.8.14.0401 | FE | taxa_antecipada | imita instituição | fronteira | Perfil falso de político no Facebook oferece cheques moradia e emprego mediante pagamento de R$11 mil [adjudicação do segundo leitor, 23/11/2026: primeira leitura falso_conhecido, segunda taxa_antecipada] |
| PA-FE 113 | 0801489-49.2023.8.14.0040 | FE | falsa_central | imita instituição | fronteira | falso consórcio com representantes recrutados por comissão [adjudicação do segundo leitor, 23/11/2026: primeira leitura taxa_antecipada, segunda venda_falsa] |
| PA-FE 114 | 0801325-68.2023.8.14.0401 | FE | falso_parente | imita relação pessoal |  | WhatsApp se passando pela filha de idosa |
| PA-FE 116 | 0824029-12.2022.8.14.0401 | FE | venda_falsa | imita oferta | amostra | moto anunciada na OLX |
| PA-FE 117 | 0818746-66.2026.8.14.0401 | FE | outro | fora da tipologia | fronteira | furto de bolsa em carro com bloqueador de sinal do alarme |
| PA-FE 118 | 0823709-88.2024.8.14.0401 | FE | taxa_antecipada | imita instituição |  | promessa de inclusão em Cheque Moradia e Minha Casa Minha Vida mediante pagamento |
| PA-FE 119 | 0801064-58.2023.8.14.0125 | FE | venda_falsa | imita oferta |  | moto anunciada em página do Facebook |
| PA-FE 120 | 0802812-73.2023.8.14.0401 | FE | falsa_central | imita instituição | amostra | falsa funcionária do Banpará oferecendo conversão de pontos |
| PA-FE 122 | 0000666-63.2021.8.14.0401 | FE | invasao_sistema_bancario | ataca a conta ou o aparelho |  | Operação Trojan: dados bancários, malware e troca de senha na central do banco |
| PA-FE 124 | 0812695-94.2022.8.14.0040 | FE | venda_falsa | imita oferta |  | contrato de construção pago e não executado |
| PA-FE 128 | 0818121-71.2022.8.14.0401 | FE | falso_parente | imita relação pessoal |  | WhatsApp com a foto do filho |
| PA-FE 129 | 0814827-69.2026.8.14.0401 | FE | falso_advogado | imita instituição |  | falso escritório de advocacia com dados processuais verdadeiros |
| PA-FE 132 | 0819725-54.2023.8.14.0006 | FE | venda_falsa | imita oferta |  | aluguel de imóvel alheio anunciado no Facebook |
| PA-FE 133 | 0803125-12.2024.8.14.0009 | FE | venda_falsa | imita oferta |  | falsa leiloeira do Detran |
| PA-FE 134 | 0819648-87.2024.8.14.0401 | FE | venda_falsa | imita oferta |  | site de leilões fraudulento |
| PA-FE 135 | 0804592-48.2023.8.14.0401 | FE | boleto_falso | imita instituição |  | site falso da Unimed e códigos de barras para empresa de fachada |
| PA-FE 136 | 0820933-52.2023.8.14.0401 | FE | taxa_antecipada | imita instituição | amostra | falso empréstimo oferecido por suposta empresa de crédito |
| PA-FE 137 | 0800652-96.2023.8.14.0006 | FE | venda_falsa | imita oferta |  | peça de automóvel anunciada na OLX |
| PA-FE 138 | 0803490-83.2026.8.14.0013 | FE | falsa_central | imita instituição |  | falsos funcionários da Equatorial com uniforme colhem documentos e fotos faciais de idosos |
| PA-FE 139 | 0814917-14.2025.8.14.0401 | FE | falso_parente | imita relação pessoal | amostra | WhatsApp se passando pela filha |
| PA-FE 140 | 0824285-52.2022.8.14.0401 | FE | falso_parente | imita relação pessoal |  | WhatsApp se passando pelo filho de idoso |
| PA-FE 141 | 0802159-03.2025.8.14.0401 | FE | venda_falsa | imita oferta |  | caminhonete anunciada na OLX, golpe do intermediário (GAECO, 21 réus) |
| PA-FE 142 | 0801839-21.2023.8.14.0401 | FE | venda_falsa | imita oferta |  | carro anunciado pela vítima na OLX, golpe do intermediário |
| PA-FE 143 | 0824232-37.2023.8.14.0401 | FE | falsa_central | imita instituição |  | link para página falsa do Banpará sobre pontos de fidelidade |
| PA-FE 144 | 0805552-38.2022.8.14.0401 | FE | venda_falsa | imita oferta | fronteira | Anúncio no Facebook de Onix por suposta administradora de consórcio; vítima paga R$19.400 e o veículo nunca é entregue [adjudicação do segundo leitor, 23/11/2026: primeira leitura taxa_antecipada, segunda venda_falsa] |
| PA-FE 145 | 0820198-53.2022.8.14.0401 | FE | falso_parente | imita relação pessoal |  | WhatsApp se passando por filhos das vítimas |
| PA-FE 146 | 0811347-54.2024.8.14.0401 | FE | venda_falsa | imita oferta |  | imóvel ofertado por imobiliária com CNPJ inexistente |
| PA-FE 147 | 0818138-73.2023.8.14.0401 | FE | compra_fraudulenta_empresa | manipula o pagamento |  | compra de porcelanato em loja em nome de terceiro |
| PA-FE 149 | 0824186-82.2022.8.14.0401 | FE | falso_parente | imita relação pessoal | amostra | WhatsApp se passando pelo filho |
| PA-FE 151 | 0800501-05.2023.8.14.0080 | FE | venda_falsa | imita oferta |  | moto ofertada por falso funcionário de leilões |
| PA-FE 152 | 0805897-96.2025.8.14.0401 | FE | roubo_celular_invasao | ataca a conta ou o aparelho |  | roubo de pertences e subtração das contas da empresa da vítima |
| PA-FE 154 | 0801802-91.2023.8.14.0401 | FE | compra_fraudulenta_empresa | manipula o pagamento |  | compra em loja por WhatsApp com Pix falso |
| PA-FE 158 | 0800183-52.2024.8.14.0091 | FE | falso_conhecido | imita relação pessoal | fronteira | Falso comprador de combustível alega pagamento a maior e depois se passa pelo conhecido Irinelson pedindo o reembolso por PIX [adjudicação do segundo leitor, 23/11/2026: primeira leitura compra_fraudulenta_empresa, segunda falso_conhecido] |
| PA-FE 160 | 0812807-13.2023.8.14.0401 | FE | venda_falsa | imita oferta |  | moto vendida por empresa e não entregue |
| PA-FE 162 | 0801095-26.2023.8.14.0401 | FE | falsa_central | imita instituição |  | ligação de falso funcionário do Banco do Brasil a idosa |
| PA-FE 163 | 0810057-09.2021.8.14.0401 | FE | boleto_falso | imita instituição |  | site falso do Banco BV para segunda via de boleto |
| PA-FE 164 | 0800028-66.2024.8.14.1605 | FE | compra_fraudulenta_empresa | manipula o pagamento |  | comprovantes de Pix falsos em lanchonete |
| PA-FE 166 | 0801365-31.2024.8.14.0008 | FE | insider_empresa | ataca sistema ou usa acesso interno | fronteira | funcionária comercial desvia pagamentos de clientes da empresa |
| PA-FE 167 | 0800083-74.2023.8.14.0401 | FE | venda_falsa | imita oferta |  | intermediário falso com anúncios copiados da OLX |
| PA-FE 168 | 0801283-46.2023.8.14.0004 | FE | invasao_sistema_bancario | ataca a conta ou o aparelho | amostra | Obtém empréstimo para a vítima e acessa a conta digital dela, transferindo o crédito para terceiro [adjudicação do segundo leitor, 23/11/2026: primeira leitura insercao_dados_falsos, segunda invasao_sistema_bancario] |
| PA-FE 170 | 0820852-35.2025.8.14.0401 | FE | falsa_central | imita instituição | amostra | ligação de falso funcionário do Bradesco com número gravado na agenda |
| PA-FE 172 | 0815441-79.2023.8.14.0401 | FE | falso_parente | imita relação pessoal |  | WhatsApp se passando pela irmã |
| PA-FE 173 | 0800155-61.2023.8.14.0401 | FE | venda_falsa | imita oferta | amostra | aluguel de carro anunciado na OLX, com caução |
| PA-FE 175 | 0801790-43.2024.8.14.0401 | FE | venda_falsa | imita oferta |  | instalação de cortinas contratada pelo Instagram e não feita |
| PA-FE 177 | 0817591-20.2024.8.14.0006 | FE | compra_fraudulenta_empresa | manipula o pagamento | fronteira | Sobrinho obtém documentos e biometria da tia sob pretexto e abre conta e cartão em nome dela, fazendo compras [adjudicação do segundo leitor, 23/11/2026: primeira leitura insercao_dados_falsos, segunda compra_fraudulenta_empresa] |
| PA-FE 179 | 0811695-72.2024.8.14.0401 | FE | falso_conhecido | imita relação pessoal |  | perfil falso da vice-governadora pedindo valores a prefeita (tentativa) |
| PA-FE 181 | 0807591-37.2024.8.14.0401 | FE | venda_falsa | imita oferta | amostra | milhas aéreas vendidas sem validade na companhia |
| PA-FE 183 | 0810547-89.2025.8.14.0401 | FE | falso_parente | imita relação pessoal |  | WhatsApp se passando pelo irmão |
| PA-FE 184 | 0823242-46.2023.8.14.0401 | FE | falso_parente | imita relação pessoal |  | WhatsApp se passando pela filha |
| PA-FE 185 | 0806335-25.2025.8.14.0401 | FE | venda_falsa | imita oferta |  | carro anunciado no Marketplace do Facebook |
| PA-FE 186 | 0823725-42.2024.8.14.0401 | FE | taxa_antecipada | imita instituição |  | promessa de facilitar imóvel do Minha Casa Minha Vida mediante pagamento |
| PA-FE 187 | 0812600-77.2024.8.14.0401 | FE | compra_fraudulenta_empresa | manipula o pagamento |  | compras de material por falsa cliente |
| PA-FE 188 | 0800657-34.2022.8.14.0110 | FE | falso_conhecido | imita relação pessoal |  | WhatsApp com a foto de subprocurador do MPPA |
| PA-FE 190 | 0811587-09.2025.8.14.0401 | FE | falso_parente | imita relação pessoal |  | WhatsApp com a foto da esposa |
| PA-FE 192 | 0046698-39.2015.8.14.0401 | FE | venda_falsa | imita oferta |  | carro anunciado na OLX como prêmio da Sabesp |
| PA-FE 193 | 0813417-44.2024.8.14.0401 | FE | taxa_antecipada | imita instituição |  | venda de vagas no Cheque Moradia com suposto parente na Cohab |
| PA-FE 195 | 0811121-78.2026.8.14.0401 | FE | falso_advogado | imita instituição |  | golpe do falso advogado contra clientes de escritório (CyberGAECO) |
| PA-FE 197 | 0801548-17.2025.8.14.0024 | FE | invasao_sistema_bancario | ataca a conta ou o aparelho |  | filha faz transações não autorizadas na conta da mãe idosa |
| PA-FE 199 | 0803402-79.2025.8.14.0401 | FE | falso_advogado | imita instituição | amostra | falso escritório de advocacia cobrando por desconto no imposto de renda |
| PA-FE 200 | 0800137-24.2024.8.14.0104 | FE | compra_fraudulenta_empresa | manipula o pagamento |  | pagamento por Pix fraudado em conveniência, com adolescentes (tentativa) |
| PA-FE 201 | 0802805-05.2023.8.14.0006 | FE | venda_falsa | imita oferta |  | imóvel anunciado no Marketplace do Facebook |
| PA-FE 202 | 0825320-42.2025.8.14.0401 | FE | falso_parente | imita relação pessoal |  | WhatsApp se passando pela filha |
| PA-FE 203 | 0800300-21.2024.8.14.0066 | FE | venda_falsa | imita oferta |  | caminhonete ofertada por telefone, com ameaça posterior |
| PA-FE 205 | 0819419-64.2023.8.14.0401 | FE | falsa_central | imita instituição | amostra | ligação de falso atendente do Banco Inter oferecendo portabilidade |
| PA-FE 206 | 0801392-93.2021.8.14.0048 | FE | insider_empresa | ataca sistema ou usa acesso interno | fronteira | Recepcionista com acesso ao caixa desvia vendas da maquininha do hotel para conta aberta em nome do pai [adjudicação do segundo leitor, 23/11/2026: primeira leitura outro, segunda insider_empresa] |
| PA-FE 207 | 0806944-08.2025.8.14.0401 | FE | falsa_central | imita instituição | amostra | Falso funcionário do Banpará liga, já com dados e senha da conta do conselho escolar, e obtém o IN TOKEN; transferência de R$47 mil [adjudicação do segundo leitor, 23/11/2026: primeira leitura invasao_sistema_bancario, segunda falsa_central] |
| PA-FE 208 | 0808389-61.2025.8.14.0401 | FE | investimento_falso | imita oferta |  | anúncio de Plataforma Pix no Instagram de amiga com perfil invadido |
| PA-FE 209 | 0809734-33.2023.8.14.0401 | FE | taxa_antecipada | imita instituição | amostra | Suposta atendente de assessoria financeira promete quitar consignado, faz novo empréstimo e a vítima transfere o valor à empresa [adjudicação do segundo leitor, 23/11/2026: primeira leitura falsa_central, segunda taxa_antecipada] |
| PA-FE 210 | 0813866-65.2025.8.14.0401 | FE | venda_falsa | imita oferta |  | site de leilão falso aberto por anúncio no R7 |
| PA-FE 211 | 0814607-76.2023.8.14.0401 | FE | venda_falsa | imita oferta |  | site de leilão de veículos falso |
| PA-FE 213 | 0809161-92.2023.8.14.0401 | FE | falso_parente | imita relação pessoal |  | mensagem se passando pelo filho |
| PA-FE 215 | 0810134-76.2025.8.14.0401 | FE | falso_parente | imita relação pessoal |  | WhatsApp com a foto da filha |
| PA-FE 216 | 0815026-28.2025.8.14.0401 | FE | falsa_central | imita instituição | fronteira | chupa-cabra retém o cartão e falso atendente da central de segurança atende a idosa |
| PA-FE 218 | 0812438-48.2025.8.14.0401 | FE | compra_fraudulenta_empresa | manipula o pagamento | fronteira | pagamentos indevidos com o cartão corporativo da Defesa Civil a empresas sem contrato |
| PA-FE 220 | 0804356-83.2021.8.14.0040 | FE | compra_fraudulenta_empresa | manipula o pagamento |  | comprovantes de TED falsos em compras por WhatsApp |
| PA-FE 221 | 0800451-34.2024.8.14.0018 | FE | invasao_sistema_bancario | ataca a conta ou o aparelho |  | empréstimo indevido pelo aplicativo do Banpará e saques na agência |
| PA-FE 222 | 0810000-15.2026.8.14.0401 | FE | venda_falsa | imita oferta |  | televisão anunciada na OLX |
| PA-FE 223 | 0823007-45.2024.8.14.0401 | FE | falso_parente | imita relação pessoal |  | WhatsApp com a foto da filha |
| PA-FE 224 | 0814092-75.2022.8.14.0401 | FE | falsa_central | imita instituição |  | golpe do motoboy contra idosos, equipe hospedada em hotéis |
| PA-FE 225 | 0823904-44.2022.8.14.0401 | FE | venda_falsa | imita oferta |  | geladeira anunciada na OLX |
