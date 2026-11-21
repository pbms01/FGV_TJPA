# Segundo grau do TJSP e a Lei 15.397/2026 (cessão de conta laranja)

Coleta de 21/11/2026, em duas frentes: o andamento em segundo grau das sentenças da amostra que trataram do 171 §2º, VII, e o conjunto de acórdãos do TJSP que já decidiram sobre o inciso. A Lei 15.397/2026, de 30/04/2026, publicada no DOU de 04/05/2026, criou o inciso VII do §2º do art. 171 ("cede, gratuita ou onerosamente, conta bancária para que nela transitem recursos destinados ao financiamento de atividade criminosa ou que dela sejam fruto"), com a pena do caput, de 1 a 5 anos.

## Arquivos

- `apelacoes_amostra.csv`: uma linha por sentença da amostra posterior à lei que aplicou, recusou ou mencionou o inciso (23 processos, de `consolida_sentencas.py`). Campos: recorrente, distribuição, câmara, relator, julgamento, resultado do acórdão, se o acórdão trata do inciso, fonte e nota. Fonte: DJEN pelo Codex (`pdpj_buscar_comunicacoes` do dia seguinte à sentença até 21/11/2026), acórdão e razões do MP lidos pelo Codex quando havia. Gravação por `scripts/registra_apelacao.py`.
- `textos/tjsp/acordaos/<numero>/` e `textos/tjsp/recursos/<numero>/`: texto de 2 acórdãos e de 3 razões de apelação do MP, sem a linha `Original:` (manifestos `textos/tjsp/manifesto_acordaos.csv` e `manifesto_recursos.csv`, gravação por `scripts/grava_acordao.py`).
- `cjsg_cessao_conta_laranja.json` e `cjsg_15397_inciso_vii.json`: resultado integral das duas buscas na Consulta de Jurisprudência do Segundo Grau (esaj.tjsp.jus.br/cjsg), feitas pelo navegador embutido em 21/11/2026, tipo de publicação "Acórdãos", ordenação por data de publicação. Por acórdão: número, cdacordao, classe e assunto, relator, comarca, órgão julgador, datas de julgamento e publicação e a ementa integral (div "dados sem formatação"). As buscas foram `"cessão de conta laranja"` (58 acórdãos) e `"15.397" E "inciso VII"` (110 acórdãos, 43 em comum com a primeira). Três páginas e seis páginas, com pausa de 3 s entre elas, na sessão aberta no navegador.
- `acordaos_inciso_vii.csv`: a união das duas buscas (125 acórdãos), com a decisão sobre o inciso lida na ementa e o fundamento principal. Gerado por `scripts/classifica_acordaos.py`; a decisão vem do dicionário `MANUAL`, preenchido pela leitura de cada ementa, e as colunas `fundamentos_regex` são só apoio.

## Andamento das apelações da amostra (até 21/11/2026)

Das 23 sentenças, duas apelações foram julgadas, nenhuma sobre o inciso: no CL 48 a 7ª Câmara manteve o §2º-A (a defesa pediu só o estelionato simples) e no FE 77 a 14ª Câmara julgou apenas nulidades. O CL 39 transitou em julgado sem recurso. O FE 42 aguarda audiência de suspensão condicional do processo, aberta pela pena mínima de 1 ano do inciso. O CL 34 está na pauta virtual de 03/12/2026 da 10ª Câmara. As demais estão na origem ou distribuídas, e oito não têm movimento de segundo grau no DJEN.

O MP apelou de quatro sentenças que aplicaram o inciso (CL 7, CL 11, CL 13, CL 45). As razões lidas mostram três linhas, nenhuma igual à do FE 72:

- CL 13 (21/09/2026): o inciso só incide quando a prova se limita à cessão sem vínculo subjetivo com crime determinado mais grave; quem entrega conta e senha mediante paga para uma fraude eletrônica determinada é partícipe do §2º-A (art. 29).
- CL 11 (21/09/2026): pela posição no §2º do 171, o inciso só alcança recursos ligados ao estelionato, citando Rogério Sanches Cunha (Meu Site Jurídico, 04/05/2026); a cessão para uma extorsão com a vítima em cativeiro é participação no 158.
- CL 45 (16/09/2026): além da participação no §2º-A, um dilema intertemporal. Se a conduta de 2021 não era participação no crime então existente, o inciso é tipo novo e não pode retroagir.

## Acórdãos do TJSP sobre o inciso VII (ementas, 24/06 a 19/11/2026)

Dos 125 acórdãos, 56 decidem na ementa se o inciso incide. Os demais estão fora do tema (40: roubo e furto com outro "inciso VII", ou a lei nova em outros crimes), mencionam o tema só no inteiro teor (11), não têm ementa publicada (7), não o enfrentam por via inadequada (9, em embargos, habeas corpus, revisão e agravo em execução) ou absolvem sem decidir sobre ele (2).

| Decisão | Acórdãos | Fundamento principal |
| --- | --- | --- |
| Aplica o VII (desclassifica) | 22 | retroatividade da lei mais benéfica 16, especialidade 5, exceção pluralista à teoria monista 1 |
| Condena no VII em apelo do MP | 2 | contra absolvição e contra desclassificação para receptação |
| Mantém o VII da sentença | 1 | |
| Recusa o VII | 30 | participação ou adesão à fraude 20, crime violento (roubo e extorsão) 4, tipicidade anterior à lei 2, irretroatividade 1, sem fundamento na ementa 3 |
| Troca o VII da sentença pelo 171 caput | 1 | não dito na ementa |

- Nas 43 apelações que decidem o mérito, o inciso prevalece em 24 (aplica, condena no VII ou mantém) e é recusado em 19. Nos embargos, a recusa domina (10 de 11).
- A 16ª Câmara concentra as aplicações: 13 das 25 decisões em que o inciso prevalece, contra 3 recusas na própria câmara. Nove dessas 13 são do relator Guilherme de Souza Nucci, que aplica o VII pela especialidade mesmo com adesão consciente ao golpe (1501016-22.2024.8.26.0438). Na 9ª Câmara são 6 recusas contra 1 aplicação; a relatora Ana Lucia Queiroga reserva o inciso ao cedente de atuação neutra, alheio ao delito de origem.
- O divisor dominante não é o direito intertemporal. A maioria trata o inciso como lei mais benéfica, aplicável a fato anterior, e a recusa se apoia na participação: quando a conta é o destino das transferências no curso da fraude, com adesão consciente, o titular é partícipe ou coautor do §2º-A pelo art. 29. É a mesma tese das razões do MP no CL 13.
- A leitura de irretroatividade do FE 72 aparece em um acórdão: a 5ª Câmara (1545200-63.2024.8.26.0050, 09/11/2026), de ofício, declara o VII inaplicável a fatos anteriores à vigência e readequa ao 171 caput com o art. 29. Na mesma direção, a 2ª Câmara trocou o VII da sentença pelo 171 caput (1502402-29.2022.8.26.0577) sem dizer o motivo na ementa, e a 13ª Câmara (0004925-83.2023.8.26.0050) e um habeas corpus da 16ª (2135942-62.2026.8.26.0000) rejeitam a tese de que a cessão anterior à lei era atípica.
- O acórdão citado nas sentenças do CL 29 e do CL 34, Apelação 1503076-37.2022.8.26.0664 (16ª Câmara, Nucci, 21/08/2026), existe e aplica o VII como novatio legis in mellius.
- Na cessão de conta para roubo ou extorsão, todas as câmaras que decidiram recusam o inciso (4 acórdãos), o que bate com a tese do MP no CL 11.
- Seis processos da amostra já têm acórdão sobre o inciso, todos de sentenças que condenaram no §2º-A: FE 56, CL 6, CL 58 (embargos), FE 101 e FE 96 tiveram a conduta desclassificada para o VII; o CL 47 teve a desclassificação recusada em embargos. O CL 21 tem acórdão que menciona o tema só no inteiro teor.

## Limitações

- A classificação é da ementa. Os 7 acórdãos sem ementa e os 11 que só tratam do tema no inteiro teor não foram lidos, e uma ementa pode omitir a decisão sobre o inciso.
- As duas buscas não garantem o universo: um acórdão que trate do inciso sem usar "cessão de conta laranja", nem "15.397" com "inciso VII", fica fora. O cjsg também não lista acórdãos em segredo de justiça.
- O fundamento principal é o que a ementa destaca; muitas combinam retroatividade e especialidade.
- A data de julgamento dos acórdãos vai de 24/06/2026 a 19/11/2026, de modo que o quadro é dos seis primeiros meses de vigência.
