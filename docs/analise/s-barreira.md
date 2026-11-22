# Segurança da informação: como a barreira cai, o que o processo faz com ela e quem tem a chave

Nota analítica de 22/11/2026, sobre a base da fase 1 (TJSP), para a aula de segurança da informação e criptografia (Project: `claude/arquitetura-aula-seguranca-criptografia.md` e `claude/seguranca-criptografia-questoes.md`, grupo 1). Tabelas reproduzíveis por `python3 scripts/analise_s_barreira.py`, que grava `dados/analise/s_barreira.csv` (uma linha por denúncia do universo) e `dados/analise/s_resumo.json`; `python3 scripts/analise_s_barreira.py valida` imprime os trechos das sentenças em que a técnica do agente aparece perto da dosimetria. Usa as questões 2 (eixos), 5 (data do fato) e 6 (credencial) e a triagem da elementar do 154-A (`dados/aula/inv_elementar_seguranca.csv`). Linhas de pesquisa: 1.1, 3.4, 4.1 e 2.3. Conferida por segundo leitor cego (`docs/analise/segundo-leitor-seguranca.md`).

## Resposta

A barreira técnica quase nunca é quebrada. Nas 41 denúncias em que a narrativa diz por onde o agente passou, a técnica (falha explorada, programa malicioso, força bruta) é a via em 5. Em 24 a credencial saiu da própria vítima, por engano (19) ou por relação e coação (5); em 7 a porta foi aberta por quem tinha acesso legítimo, com a própria credencial (4) ou com a de um colega, comprada ou cedida (3); em 4 o aparelho ou a sessão já estavam nas mãos do agente; em 1 a senha resistiu. Outras 19 denúncias narram o acesso sem dizer como, e em 8 não houve barreira a vencer, porque a própria vítima pagou ou autorizou o pagamento (a maquininha adulterada, o comprovante falso, o falso parente). É o padrão que Anderson descreveu em 1993 para os caixas eletrônicos: as fraudes vinham de erros de implementação e de gestão, não da criptoanálise.

O processo, por sua vez, ainda procura a barreira que a lei deixou de exigir. Nas 28 denúncias com o sistema como objeto e fato posterior a 28/05/2021, uma imputa com a redação revogada do art. 154-A (INV 33) e seis narram a violação de um sistema de segurança como fato (INV 4, INV 6, INV 13, CL 10, CL 15, CL 41). Pela leitura integral das sentenças, cinco das que se pronunciam sobre a questão com fato posterior à lei ainda tratam a barreira como exigência: três a exigem e absolvem ou afastam o 154-A (INV 13, INV 14, INV 26) e duas a exigem e a encontram (INV 38, INV 44); quatro a dispensam (INV 1, INV 10, INV 20, INV 39). A técnica do agente pesa na pena em uma sentença da base (INV 4, "expertise e habilidade incomuns"), e a posição de confiança em duas (INV 4 e INV 8); fora da base, a AP 2428 do STF valorou contra o réu o "reconhecido conhecimento técnico" na culpabilidade.

O acesso interno é a via em que a prova da autoria é mais forte. Das 7 denúncias, todas terminaram com condenação ao menos parcial, e em 5 a sentença atribuiu o acesso ao réu pelo registro do próprio sistema: o login e o token da operadora no INV 2, os acessos privilegiados de ex-prestadores no INV 8, o IP do computador do réu no INV 11, o IP informado pelo provedor de nuvem no INV 30, os logs do sistema da empresa no INV 45. Nas outras duas, a autoria veio da confissão (INV 10) e do aparelho apreendido (INV 21).

## Base e método

Universo: 68 denúncias sem duplicata. Entram as 38 com o sistema como objeto (eixo da questão 2) e as 30 de sistema-meio em que a triagem da questão 6 marcou credencial saída da vítima ou cedida por quem tinha acesso legítimo (INV 10, peculato com senha cedida por servidoras). A via do sistema-objeto é leitura à mão das narrativas, com o trecho que decide no dicionário `BARREIRA`; a do sistema-meio vinha da triagem e foi corrigida pelo segundo leitor em 11 casos (dicionário `VIA_MEIO`). A conferência está em `docs/analise/segundo-leitor-seguranca.md`.

| Via | Sistema-objeto (38) | Sistema-meio (30) | Total |
| --- | --- | --- | --- |
| Credencial própria de quem tinha acesso legítimo | 4 | 0 | 4 |
| Credencial de quem tinha acesso legítimo, comprada ou cedida | 2 | 1 | 3 |
| Credencial obtida da vítima por engano | 3 | 16 | 19 |
| Credencial obtida da vítima por relação ou coação | 3 | 2 | 5 |
| Aparelho ou sessão em mãos, sem barreira narrada | 4 | 0 | 4 |
| Técnica | 5 | 0 | 5 |
| A barreira resistiu | 1 | 0 | 1 |
| Via não narrada | 16 | 3 | 19 |
| Sem barreira: a vítima pagou ou autorizou | 0 | 8 | 8 |

A técnica: engenharia reversa do aplicativo bancário com JADX e FRIDA (INV 19), vulnerabilidade do sistema do banco explorada por especialista em segurança (INV 33), ataques de negação de serviço e de força bruta (INV 34), programas maliciosos no sistema bancário (INV 35) e máquina da empresa sem antivírus (CL 28). O acesso interno: a funcionária de loja terceirizada da operadora que faz o SIM swap (INV 2), os responsáveis pelo sistema da empresa (INV 8), o ex-funcionário de TI (INV 30), o funcionário de laboratório (INV 45); e, com credencial de colega, as senhas de policiais compradas (INV 11, INV 21) e as cedidas por servidoras (INV 10). O INV 4 é o paralelo da AP 2428 na base: um escrevente entrou duas vezes na conta gov.br de um juiz, mesmo depois da troca de senha e da verificação em duas etapas, e confessou ter usado a opção "esqueci a senha"; a denúncia não narra a via, que só aparece na sentença.

Regime legal pela data do fato contra 28/05/2021, publicação e vigência da Lei 14.155/2021. A elementar na denúncia separa a imputação com a redação revogada da violação narrada como fato; a transcrição do §4º-B do art. 155 ("com ou sem violação de mecanismo de segurança") não conta. A valoração da técnica foi triagem por termos ("conhecimento técnico", "expertise", "sofisticação", "especialista") a até 600 caracteres de termo de dosimetria, e o segundo leitor, lendo as 38 sentenças por inteiro, achou o mesmo único caso; a posição da sentença sobre a elementar, a valoração da confiança e a prova da autoria vêm da leitura integral do segundo leitor, adjudicada. Três textos de sentença estão cortados pelo Codex: o do INV 2 e o do INV 8 antes da dosimetria do 154-A, o do INV 36 antes da fundamentação; a contagem da pena é piso. Nos arquivos do INV 4, do INV 17, do INV 24 e do INV 41 a mesma sentença está gravada mais de uma vez (cópias idênticas, conferidas pelo segundo leitor).

## O que isso dá a quem previne, a quem investiga e a quem julga

| Momento | O que conferir | Dado da base |
| --- | --- | --- |
| Prevenção e dever de cuidado | se a barreira dependia de segredo que a vítima pode recitar ou entregar | a credencial sai da vítima em 24 de 41 vias narradas |
| Investigação | o registro de acesso do próprio sistema (login, token, horário, IP) antes do rastro externo | a autoria interna foi provada pelo registro em 5 de 7 |
| Recebimento da denúncia | se a imputação usa a redação revogada do 154-A | 1 de 28 com fato posterior à lei |
| Sentença, tipicidade | o 154-A não exige senha nem barreira desde 28/05/2021 | 5 sentenças ainda a exigem (3 absolvem, 2 a encontram), contra 4 que a dispensam |
| Sentença, dosimetria | se a técnica ou a posição de confiança foi valorada, e com que fundamento | técnica em 1 sentença, confiança em 2; a AP 2428 valorou a técnica na culpabilidade |

## Limites

A via é o que a denúncia narra, não o que o laudo prova, e as 19 vias não narradas fazem dos números pisos. O universo do acesso interno é pequeno (7). O segundo leitor é outra instância do mesmo modelo: a conferência mede a reprodutibilidade a partir do texto e do livro de códigos, não a ausência de viés comum; a conferência humana das 23 decisões de adjudicação fica pendente.

## Fontes conferidas nesta sessão

- Anderson, R. Why Cryptosystems Fail. 1st ACM Conference on Computer and Communications Security, 1993: https://www.cl.cam.ac.uk/~rja14/wcf.html
- Cornish, D. B.; Clarke, R. V. Opportunities, precipitators and criminal decisions. Crime Prevention Studies, v. 16, 2003 (25 técnicas; "controlar o acesso"): https://popcenter.asu.edu/sites/default/files/Responses/crime_prevention/PDFs/Cornish&Clarke.pdf e tabela do UNODC: https://www.unodc.org/documents/e4j/CPCJ/CPCJ_Module_2_Crime_Prevention_-_table_25_opportunity_reducing_techniques.pdf
- STF, AP 2428, voto do relator (reprodução no Migalhas): https://www.migalhas.com.br/arquivos/2025/5/5811413F4DB41C_conteudo(2).pdf; embargos rejeitados em 06/06/2025: https://noticias.stf.jus.br/?p=97957
- INV 2, dispositivo da sentença no DJEN de 29/09/2025 (pdpj_buscar_comunicacoes).
- Art. 313-A do CP: não conferido nesta sessão (o acesso ao Planalto ficou pendente de aprovação).
