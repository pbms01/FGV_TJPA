# Segurança da informação: como a barreira cai, o que o processo faz com ela e quem tem a chave

Nota analítica de 22/11/2026, sobre a base da fase 1 (TJSP), para a aula de segurança da informação e criptografia (Project: `claude/arquitetura-aula-seguranca-criptografia.md` e `claude/seguranca-criptografia-questoes.md`, grupo 1). Tabelas reproduzíveis por `python3 scripts/analise_s_barreira.py`, que grava `dados/analise/s_barreira.csv` (uma linha por denúncia do universo) e `dados/analise/s_resumo.json`; `python3 scripts/analise_s_barreira.py valida` imprime os trechos das sentenças em que a técnica do agente aparece perto da dosimetria. Usa as questões 2 (eixos), 5 (data do fato) e 6 (credencial) e a triagem da elementar do 154-A (`dados/aula/inv_elementar_seguranca.csv`). Linhas de pesquisa: 1.1, 3.4, 4.1 e 2.3. Não passou por segundo leitor.

## Resposta

A barreira técnica quase nunca é quebrada. Nas 58 denúncias em que a narrativa diz por onde o agente passou, a técnica (falha explorada, programa malicioso, força bruta) é a via em 5. Em 36 a credencial saiu da própria vítima, por engano (31) ou por relação e coação (5), contadas as duas camadas; em 10 a porta foi aberta por quem tinha acesso legítimo, com a própria credencial (7) ou com a de um colega, comprada ou cedida (3); em 6 o aparelho ou a sessão já estavam nas mãos do agente; em 1 a senha resistiu. É o padrão que Anderson descreveu em 1993 para os caixas eletrônicos: as fraudes vinham de erros de implementação e de gestão, não da criptoanálise.

O processo, por sua vez, ainda procura a barreira que a lei deixou de exigir. Nas 28 denúncias com o sistema como objeto e fato posterior a 28/05/2021, uma imputa com a redação revogada do art. 154-A (INV 33) e cinco narram a violação de um sistema de segurança como fato (INV 6, INV 13, CL 10, CL 15, CL 41). Nas sentenças do INV com fato posterior à lei que tratam da elementar, três a exigem e absolvem ou afastam o 154-A (INV 13, INV 14, INV 26), contra quatro que a dispensam e uma que condena o acesso feito com a senha entregue na relação (INV 27). A técnica do agente aparece ligada à pena em uma sentença da base (INV 4, "expertise e habilidade incomuns"); fora da base, a AP 2428 do STF valorou contra o réu o "reconhecido conhecimento técnico" na culpabilidade.

O acesso interno é a via em que a prova da autoria é mais forte. Das 10 denúncias, 9 terminaram com condenação ao menos parcial; a absolvição (INV 34, art. 386, VII) é a do administrador de rede com senha de todas as máquinas, fato de 2016. Onde a peça foi lida neste ponto, a autoria veio do registro do próprio sistema: o login e o token da operadora no INV 2, a auditoria da Polícia Militar e o IP do modem no INV 11, o IP do acesso ao servidor no INV 30, a auditoria da empresa no INV 34, o aparelho apreendido com o aplicativo e a lista de senhas no INV 21.

## Base e método

Universo: 68 denúncias sem duplicata. Entram as 38 com o sistema como objeto (eixo da questão 2) e as 30 de sistema-meio em que a credencial saiu da vítima pelo indicador da questão 6, ou foi fornecida por servidoras com acesso legítimo (INV 10, peculato). A via do sistema-objeto é leitura à mão das narrativas, com o trecho que decide no dicionário `BARREIRA`; a do sistema-meio é a triagem por termos da questão 6 e vale como piso. Dez denúncias com sistema-objeto não narram a via ("invadiu", "acessaram indevidamente").

| Via | Sistema-objeto (38) | Sistema-meio, triagem (30) | Total |
| --- | --- | --- | --- |
| Credencial própria de quem tinha acesso legítimo | 7 | 0 | 7 |
| Credencial de quem tinha acesso legítimo, comprada ou cedida | 2 | 1 | 3 |
| Credencial obtida da vítima por engano | 4 | 27 | 31 |
| Credencial obtida da vítima por relação ou coação | 3 | 2 | 5 |
| Aparelho ou sessão em mãos, sem barreira narrada | 6 | 0 | 6 |
| Técnica | 5 | 0 | 5 |
| A barreira resistiu | 1 | 0 | 1 |
| Via não narrada | 10 | 0 | 10 |

A técnica: engenharia reversa do aplicativo bancário com JADX e FRIDA (INV 19), vulnerabilidade do sistema do banco explorada por especialista em segurança (INV 33), programas maliciosos no sistema bancário (INV 35), invasão da Polícia Civil por quem se apresentava como hacker (INV 22) e máquina da empresa sem antivírus (CL 28). O acesso interno: a funcionária de loja terceirizada da operadora que faz o SIM swap (INV 2), o escrevente (INV 4), os responsáveis pelo sistema da empresa (INV 8), o ex-funcionário de TI (INV 30), o administrador de rede (INV 34), o correspondente bancário com funcionários cooptados (INV 36), o funcionário de laboratório (INV 45); e, com credencial de colega, as senhas de policiais compradas (INV 11, INV 21) e as cedidas por servidoras (INV 10).

Regime legal pela data do fato contra 28/05/2021, publicação e vigência da Lei 14.155/2021. A elementar na denúncia separa a imputação com a redação revogada da violação narrada como fato; a transcrição do §4º-B do art. 155 ("com ou sem violação de mecanismo de segurança") não conta. A valoração da técnica é triagem por termos ("conhecimento técnico", "expertise", "sofisticação", "especialista") a até 600 caracteres de termo de dosimetria, conferida pelos trechos; o texto da sentença do INV 2 está cortado em 100 mil caracteres pelo Codex e não traz a dosimetria, de modo que a contagem é piso.

## O que isso dá a quem previne, a quem investiga e a quem julga

| Momento | O que conferir | Dado da base |
| --- | --- | --- |
| Prevenção e dever de cuidado | se a barreira dependia de segredo que a vítima pode recitar ou entregar | a credencial sai da vítima em 36 de 58 vias narradas |
| Investigação | o registro de acesso do próprio sistema (login, token, horário, IP) antes do rastro externo | a autoria interna foi provada pelo registro nos 5 casos lidos |
| Recebimento da denúncia | se a imputação usa a redação revogada do 154-A | 1 de 28 com fato posterior à lei |
| Sentença, tipicidade | o 154-A não exige senha nem barreira desde 28/05/2021 | 3 sentenças ainda a exigem e absolvem |
| Sentença, dosimetria | se a técnica ou a posição de confiança foi valorada, e com que fundamento | 1 sentença na base; a AP 2428 a valorou na culpabilidade |

## Limites

A via é o que a denúncia narra, não o que o laudo prova. As 10 vias não narradas e a triagem da camada sistema-meio fazem dos números pisos. O universo do acesso interno é pequeno (10), e a prova só foi lida em 5. Não passou por segundo leitor. A triagem da elementar nas sentenças cobre só o INV.

## Fontes conferidas nesta sessão

- Anderson, R. Why Cryptosystems Fail. 1st ACM Conference on Computer and Communications Security, 1993: https://www.cl.cam.ac.uk/~rja14/wcf.html
- Cornish, D. B.; Clarke, R. V. Opportunities, precipitators and criminal decisions. Crime Prevention Studies, v. 16, 2003 (25 técnicas; "controlar o acesso"): https://popcenter.asu.edu/sites/default/files/Responses/crime_prevention/PDFs/Cornish&Clarke.pdf e tabela do UNODC: https://www.unodc.org/documents/e4j/CPCJ/CPCJ_Module_2_Crime_Prevention_-_table_25_opportunity_reducing_techniques.pdf
- STF, AP 2428, voto do relator (reprodução no Migalhas): https://www.migalhas.com.br/arquivos/2025/5/5811413F4DB41C_conteudo(2).pdf; embargos rejeitados em 06/06/2025: https://noticias.stf.jus.br/?p=97957
- INV 2, dispositivo da sentença no DJEN de 29/09/2025 (pdpj_buscar_comunicacoes).
- Art. 313-A do CP: não conferido nesta sessão (o acesso ao Planalto ficou pendente de aprovação).
