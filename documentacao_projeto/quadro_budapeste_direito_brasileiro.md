# Convenção de Budapeste e direito brasileiro: correspondência, descompasso e linhas de pesquisa

Versão 0.1, 20/11/2026. Apoio às linhas 1.1, 1.4, 2.4, 4.3 e 4.4 (claude/criminologia-informatica-linhas-de-pesquisa.md).

## Situação do Brasil no sistema

Instrumento depositado em 30/11/2022; vigência para o Brasil no plano externo em 1º/3/2023; promulgação pelo Decreto 11.491/2023. O registro do Conselho da Europa não traz reserva brasileira e lista só duas declarações de conteúdo: o MJSP (DRCI) como autoridade central (arts. 24.7.a e 27.2.c) e a Polícia Federal como ponto de contato da rede 24/7 (art. 35). Não há declaração com base no art. 40, que é a via pela qual uma Parte pode exigir elementos adicionais (violação de medida de segurança, intenção desonesta, sistema conectado) nos arts. 2 e 3. Consequência: o Brasil assumiu as obrigações materiais e processuais em sua extensão integral, e cada descompasso abaixo é descumprimento, não opção exercida.

As disposições penais não são autoexecutáveis (art. 5º, XXXIX, CF). Funcionam como cânone de escolha entre leituras que o tipo nacional já admite, nunca como fonte de incriminação.

## Direito material

| Convenção | O que exige | Correspondente brasileiro | Descompasso | Linha |
| --- | --- | --- | --- | --- |
| Art. 1(a), sistema de computador | Qualquer aparelho, ou conjunto interligado, que processe dados pela execução de programa | "Dispositivo informático" (art. 154-A CP) e "dispositivo eletrônico ou informático" (art. 155, § 4º-B), ambos "conectado ou não à rede" | Convergente no núcleo; a lei não define dispositivo, e o conceito convencional supre a lacuna como critério interpretativo, confirmando que a rede não é elementar | 1.1 |
| Art. 2, acesso ilegal | Acesso doloso e não autorizado a sistema, no todo ou em parte | Art. 154-A: invadir com o fim de obter, adulterar ou destruir dados, ou instalar vulnerabilidades; a Lei 14.155/2021 suprimiu a exigência de violação de mecanismo de segurança; ação condicionada (art. 154-B) | Mais estreito: o elemento subjetivo especial restringe o tipo sem declaração do art. 40 que o autorize; o acesso não autorizado sem aquela finalidade fica atípico | 1.1, 1.4 |
| Art. 3, interceptação ilícita | Interceptação, por meios técnicos, de transmissão não pública de dados | Art. 10 da Lei 9.296/1996 (comunicações telefônicas, informáticas ou telemáticas) | Convergente | sem linha própria |
| Art. 4, violação de dados | Danificar, eliminar, deteriorar, alterar ou suprimir dados; reserva de "sério dano" facultativa e não exercida | Só como finalidade da invasão (art. 154-A); o dano do art. 163 protege coisa | Lacuna: destruição de dados sem invasão (insider, titular de acesso legítimo) não tem tipo autônomo; ler dado como coisa é analogia in malam partem | 1.1, 1.4 |
| Art. 5, interferência em sistema | Obstrução grave do funcionamento de sistema por manipulação de dados | Art. 266, § 1º, CP, restrito a serviço telemático ou de informação de utilidade pública | Lacuna para sistemas privados (negação de serviço, sabotagem); o sequestro de dados tende a ser deslocado para a extorsão, por leitura e não por tipo próprio | 1.1, 3.3 |
| Art. 6, uso indevido de aparelhagem | Produzir, vender, obter, distribuir ou disponibilizar programas e senhas destinados aos crimes dos arts. 2 a 5, inclusive posse; exceção para teste autorizado | Art. 154-A, § 1º: produzir, oferecer, distribuir, vender ou divulgar dispositivo ou programa destinado a permitir a invasão | Lacuna: senhas e códigos de acesso, posse, e ferramentas voltadas a interceptação, dano ou interferência; a ferramenta de uso dual (pentest) depende da leitura de "destinado" | 2.2, 2.4 |
| Art. 7, falsificação informática | Inserir, alterar, apagar ou suprimir dados gerando dados inautênticos com efeito jurídico | Art. 298, p. ú., CP (cartão equiparado a documento particular); art. 313-A CP (funcionário, sistemas da Administração) [313-A não verificado nesta versão] | Lacuna geral: o documento eletrônico privado e o dado com valor probatório dependem de ampliar "documento"; o artefato sintético por IA agrava o problema | 2.4, 4.3 |
| Art. 8, fraude informática | Prejuízo patrimonial causado por manipulação de dados ou interferência em sistema, sem exigir engano de pessoa | Art. 171, § 2º-A (informações da vítima ou de terceiro induzido a erro); art. 155, § 4º-B (furto mediante fraude por dispositivo); penas e redação alteradas pela Lei 15.397/2026 | A figura única da Convenção ficou repartida entre erro e subtração; a fraude contra a máquina cai no furto; concurso aparente com o art. 154-A; o § 4º-B não tem folha nas TPU | 1.1, 1.2, 1.3 |
| Art. 9, pornografia infantil | Produzir, oferecer, distribuir, adquirir ou possuir material por sistema informático | ECA, arts. 240 a 241-E [não verificado nesta versão] | Convergente em linhas gerais; sem reserva do 9.4 | 3.4 |
| Art. 10, direito autoral | Violação dolosa, em escala comercial, por sistema informático | Art. 184 CP; Lei 9.609/1998 [não verificado nesta versão] | Convergente | sem linha própria |
| Art. 11, tentativa e participação | Auxílio e instigação aos crimes dos arts. 2 a 10; tentativa nos arts. 3 a 5, 7, 8 e 9 | Arts. 14, II, e 29 CP | Convergente; a dificuldade real é delimitar participação em cadeias de baixa coesão (conta laranja, revenda de acesso) | 2.1, 2.2 |
| Art. 12, pessoa jurídica | Responsabilidade civil, penal ou administrativa por crime em seu benefício ou por falta de supervisão | Sem responsabilidade penal fora do ambiental; responsabilidade civil e administrativa esparsa [leitura própria] | Conformidade possível pela via não penal; os deveres de cuidado de plataformas e bancos passam a ocupar o espaço (STF, Temas 987 e 533) | 4.1 |

## Direito processual e cooperação

| Convenção | O que exige | Correspondente brasileiro | Descompasso | Linha |
| --- | --- | --- | --- | --- |
| Art. 16, preservação expedita | Ordem de preservação de dados especificados, por até 90 dias | Marco Civil, arts. 13, § 2º, e 15, § 2º: polícia, autoridade administrativa ou MP pedem guarda cautelar de registros de conexão (1 ano) e de acesso (6 meses) por prazo superior, com 60 dias para o pedido judicial | Restrito a registros; conteúdo e demais dados armazenados sem base expressa; a própria PF propõe inserir no Marco Civil o poder de requisitar preservação em harmonia com o art. 16 | 4.4 |
| Art. 17, revelação parcial de tráfego | Preservar tráfego qualquer que seja o número de provedores e revelar o bastante para identificar provedores e caminho | Sem regra própria; a revelação depende de ordem judicial (Marco Civil, arts. 10, § 1º, e 22) | Lacuna: a identificação em cadeia exige ordens sucessivas, e o dado do elo seguinte expira no intervalo | 4.4 |
| Art. 18, ordem de exibição | Ordem para pessoa no território entregar dados sob seu controle e para provedor entregar dados cadastrais | Marco Civil, arts. 11 e 22; ADC 51 (STF, 23/2/2023): o art. 11 encontra respaldo no art. 18, a requisição direta é válida e o MLAT é complementar | Convergente após a ADC 51; permanece reclamada a definição legal de dado cadastral | 4.4 |
| Art. 19, busca e apreensão de dados | Buscar e apreender sistemas e dados, estender a busca a outro sistema acessível a partir do primeiro e obrigar quem conhece o sistema a colaborar | CPP, arts. 240 e seguintes; cadeia de custódia, arts. 158-A a 158-F, cujo art. 158-B, VIII, só prevê características biológicas, físicas e químicas do vestígio | Lacuna: extensão da busca à nuvem a partir do aparelho apreendido sem regra expressa; processamento algorítmico do vestígio sem previsão | 4.3, 2.4 |
| Art. 20, tráfego em tempo real | Coleta ou gravação em tempo real de dados de tráfego de comunicações específicas | Lei 9.296/1996, art. 1º, p. ú. (fluxo de comunicações em sistemas de informática e telemática) | Parcial: a lei regula a interceptação da comunicação; a coleta autônoma de tráfego em tempo real não tem regime próprio [leitura própria] | 4.4 |
| Art. 21, interceptação de conteúdo | Interceptação de conteúdo para rol de crimes graves | Lei 9.296/1996 | Convergente | sem linha própria |
| Art. 22, jurisdição | Território, embarcações, aeronaves e nacionais; reserva facultativa não exercida | CP, arts. 5º a 7º [não verificado nesta versão]; CPP, art. 70, § 4º: no art. 171 praticado por depósito, cheque ou transferência, competência do domicílio da vítima, e prevenção se houver várias | O § 4º do art. 70 só alcança o art. 171; o furto mediante fraude por transferência (art. 155, § 4º-B) fica fora da regra, e a mesma conduta muda de foro conforme a qualificação | 1.1, 4.4 |
| Arts. 25, 27 e 29, assistência mútua | Assistência na maior medida possível; conservação a pedido de outra Parte por no mínimo 60 dias | MJSP (DRCI) como autoridade central, por declaração | Como Parte requerida, o Brasil só conserva o que o Marco Civil manda guardar, de modo que a lacuna do art. 16 se reproduz na cooperação passiva | 4.4 |
| Art. 32, acesso transfronteiriço | Acesso a dado público ou, com consentimento legítimo de quem pode revelá-lo, a dado armazenado em outro território | Sem regra interna | Lacuna: o acesso consentido a conta em nuvem estrangeira não tem disciplina de validade nem de documentação | 4.4 |
| Art. 35, rede 24/7 | Ponto de contato permanente para preservação, coleta e localização | Polícia Federal, por declaração | Convergente na forma; o MP e as polícias estaduais dependem da intermediação da PF [leitura própria] | 4.4 |

## Leitura de conjunto

O descompasso concentra-se em dois blocos. No material, nos arts. 4, 5, 6 e 7, que pressupõem o dado como objeto autônomo de proteção, ao passo que o Código Penal só o protege quando há invasão, serviço público ou documento. No processual, nos arts. 16, 17, 19 e 32, que pressupõem o tempo do dado, ao passo que o Marco Civil foi desenhado para registros e o CPP para vestígios físicos. Os arts. 3, 9, 10, 11 e 21 convergem, e o art. 18 convergiu por obra do STF. O art. 8 é o caso singular: há tipos, mas repartidos por categorias de 1940, o que produz o problema de qualificação, de competência e de visibilidade estatística ao mesmo tempo.

## Pontos não verificados

Texto atual dos arts. 313-A e 184 CP, dos arts. 240 a 241-E do ECA e da Lei 9.609/1998; arts. 5º a 7º CP; redação vigente dos arts. 13 e 15 do Marco Civil (conferida na publicação original); adesão brasileira ao Segundo Protocolo Adicional.

## Fontes

https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2023/Decreto/D11491.htm

https://rm.coe.int/0900001680a93e41

https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2021/lei/l14155.htm

https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2026/lei/l15397.htm

https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2012/lei/l12737.htm

https://www.planalto.gov.br/ccivil_03/leis/l9296.htm

https://www2.camara.leg.br/legin/fed/lei/2014/lei-12965-23-abril-2014-778630-publicacaooriginal-143980-pl.html

https://www.stf.jus.br/arquivo/cms/publicacaoBOInternet/anexo/link_download/casos_relevantes/pt/ADC_51.pdf

https://legis.senado.leg.br/norma/37070076/publicacao/37070087

https://www2.camara.leg.br/atividade-legislativa/comissoes/grupos-de-trabalho/57a-legislatura/grupo-de-trabalho-sobre-protecao-de-criancas-e-adolescentes-em-ambiente-digital/apresentacoes-em-eventos/2025.11.11VALDEMARLATANCENETODiretordoDCIBERPF.pdf

https://revistas.ufpr.br/rrddis/article/download/100127/75572/439455

claude/quadro-visibilidade-tpu-lei-14155.md
