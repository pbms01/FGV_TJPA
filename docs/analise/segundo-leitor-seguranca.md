# Segundo leitor da aula de segurança da informação

Nota de método de 22/11/2026. Reproduzível por `python3 scripts/segundo_leitor_seguranca.py`, que compara as duas leituras e grava `dados/conferencia/seguranca/concordancia.csv` e `concordancia_resumo.json`. A primeira leitura foi congelada em `dados/conferencia/seguranca/primeira_leitura.csv` antes da comparação; os lotes cegos foram gerados por `python3 scripts/segundo_leitor_seguranca.py prepara DESTINO` fora do repositório, com identificadores sorteados (semente 20261123) e a correspondência em `mapa.json`.

## Resposta

A codificação da via, que é o centro da pergunta 1, foi o campo menos reprodutível (concordância de 0,74, kappa de 0,67, em 68 denúncias), e a adjudicação deu razão ao segundo leitor em todas as 18 divergências. Os erros da primeira leitura foram de dois tipos, ambos no sentido de afirmar mais do que a denúncia narra: herdar da triagem da questão 6 a "credencial saída da vítima" em golpes em que a vítima pagou sem entregar credencial ao agente (as cinco maquininhas, o comprovante falso, a triangulação, o falso parente), e completar a via a partir do modus operandi genérico, do cargo do agente ou da perícia quando a denúncia não diz como se deu o acesso no fato. A correção não inverte a conclusão: a técnica continua sendo a via em 5 casos, que passam de 5 em 58 a 5 em 41 vias narradas, e a credencial saída da vítima cai de 36 para 24. O acesso interno cai de 10 para 7, porque o cargo de escrevente (INV 4) e a função em correspondente bancário (INV 36) não davam acesso legítimo ao sistema invadido, e porque o fato principal do INV 34 é o ataque por força bruta. A elementar na denúncia (0,94, kappa 0,83) e a técnica na pena (38 em 38) resistiram.

## Desenho

O segundo leitor, outra instância do mesmo modelo, sem acesso à primeira leitura, às notas ou ao repositório, recebeu as 68 denúncias do universo (narrativa e capitulação, em três lotes) e as 38 sentenças com o sistema como objeto e o INV 10 que têm sentença gravada (o INV 6 não tem; quatro lotes equilibrados pelo tamanho), com os livros de códigos de `dados/conferencia/seguranca/livro_codigos_*.md`. O vocabulário da via tem um valor que a primeira leitura não usava (sem_barreira), para que o leitor pudesse recusar a premissa da triagem. As sentenças foram lidas por inteiro, o que dá à posição sobre a elementar, à confiança na pena e à prova da autoria uma leitura que a primeira, por termos, não tinha; nesses campos o segundo leitor é fonte, e não só conferência.

## Concordância

| Campo | Casos | Concordância | Kappa |
| --- | --- | --- | --- |
| Via | 68 | 0,74 | 0,67 |
| Elementar na denúncia | 68 | 0,94 | 0,83 |
| Elementar na sentença (posições afirmadas pela triagem) | 8 | 0,88 | 0,77 |
| Técnica na pena | 38 | 1,00 | 1,00 |

## Adjudicação

As 23 decisões estão em `dados/conferencia/seguranca/adjudicacao.csv`, 22 para o segundo leitor. Na via: oito casos passam a sem barreira (FE 105, FE 18, FE 29, CL 24, FE 50, FE 110, FE 16, CL 49); nove passam a via não narrada (FE 10, FE 102, FE 17, FE 97, INV 36, INV 22, INV 44, INV 4, CL 41), e o INV 34 passa a técnica. Na elementar da denúncia, o INV 11 passa à redação revogada ("violando indevidamente mecanismo de segurança", e a regex foi ampliada), o INV 4 e o INV 36 passam a violação narrada como fato, e o INV 2 fica sem elementar, porque o trecho apontado descreve a senha funcional, não a violação. Na sentença, o INV 27 passa de dispensa a não trata, porque condena sem dizer por quê. As correções estão em `scripts/analise_s_barreira.py` (dicionários `BARREIRA`, `VIA_MEIO` e `ELEM_DEN_MANUAL`, e a leitura das sentenças pelo segundo leitor em `le_sentencas`).

## O que mudou na nota

As frases da nota `docs/analise/s-barreira.md` foram refeitas com os números adjudicados. Duas leituras novas vieram das sentenças: cinco sentenças com fato posterior à lei ainda tratam a barreira como exigência (três absolvem por falta dela, duas a encontram: INV 38 e INV 44), contra quatro que a dispensam; e a posição de confiança foi valorada na pena em duas (INV 4, INV 8). O INV 4 entra como paralelo da AP 2428: o escrevente confessou ter entrado na conta gov.br de um juiz pela opção "esqueci a senha".

## Limites

O segundo leitor mede a reprodutibilidade a partir do texto, não a ausência de viés comum aos dois leitores. A prova da autoria nas absolvições sem atribuição do acesso não tinha código próprio, e os leitores oscilaram entre "outra" e "não se aplica"; na análise, só "registro_sistema" é usado. A conferência humana das 23 decisões fica pendente.
