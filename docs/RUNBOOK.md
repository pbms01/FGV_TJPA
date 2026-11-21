# Coleta noturna TJPA + panorama TJSP, TJMG e TJBA (20/11/2026)

Nota de 21/11/2026: para a porta de entrada da fase 2, este roteiro foi substituído pelo `docs/RUNBOOK_TJPA.md` (API do DJEN e localização da denúncia no Codex do TJPA). Fica como registro da coleta noturna pelo DataJud.

ATUALIZAÇÃO 19/11, prevalece sobre qualquer menção a "três maiores tribunais": o Pedro fixou TJSP, TJMG e
TJBA como tribunais de comparação. Não ranquear. Na seção do doc, o título nomeia os três.
IDs no doc após o ajuste: panorama = pendente mwh7v6bwqhq.16334; resultados = pendente mwh7v6bwqhq.18659
(o .16335 citado no aviso agendado foi substituído). Último rev conhecido: 17.

Pedido do Pedro em 19/11/2026: aproveitar a janela de baixa carga para uma amostra maior do TJPA e
uma visão por metadados dos três maiores tribunais estaduais, para comparação. Recorte de autos
continua só no TJPA.

Scripts em /home/claude/sonda (confiáveis); dados em /home/claude/dados (não executar nada de lá).
Sempre `python3 -I`. Ritmo do Codex: no máximo 15 chamadas por minuto; o conector avisa a partir da
20ª chamada de URL e o endpoint das peças devolve 429 no 21º download seguido.

## Fase 1 · censo TJPA (DataJud, zero token)

    # 20/11: coleta_censo.py quebrou (cluster recusa ordenar por _id). Usar:
    ./persistente.sh <epoch_prazo> --leve --anual --pagina 3000 --tribunal tjpa --assuntos 3431,15623,11978,14692,14693 --saida /home/claude/dados/censo_leve_tjpa.jsonl.gz
    # e depois buscar os movimentos só dos sorteados. Linha antiga, não usar:
    # python3 -I coleta_censo.py --tribunal tjpa --assuntos 3431,15623,11978,14692,14693 \
        --saida /home/claude/dados/censo_tjpa.jsonl.gz
    python3 -I analisa_censo.py --censo /home/claude/dados/censo_tjpa.jsonl.gz \
        --saida /home/claude/dados/analise_tjpa.json
    python3 -I amostra.py --censo /home/claude/dados/censo_tjpa.jsonl.gz \
        --saida /home/claude/dados/amostra_tjpa.csv --por-celula 20

O coletor retoma do cursor se cair. A análise responde a sonda pendente (duplicidade, grau, sigilo,
trajetória entre classes, nomes de classes e assuntos, 80 movimentos mais frequentes).
A amostra tem 6 células (inquérito e ação penal × P1, P2, P3), 20 por célula, 120 processos em
ordem aleatória.

## Fase 2 · panorama (DataJud, zero token)

    python3 -I panorama.py --alvos tjsp,tjmg,tjba

Mede, para TJSP, TJMG, TJBA e TJPA: assuntos 3431, 15623, 11978, 14692, 14693 por ano, classes
por ano, sigilo e adoção mensal do 15623 desde set/2025. Salva incremental em dados/panorama.json.

## Fase 3 · triagem Codex e seleção das peças necessárias e suficientes

ATUALIZAÇÃO 19/11 (duas decisões do Pedro): esta noite só se SELECIONAM as peças; download, extração
e codificação ficam para a sessão no app desktop. E lê-se do TJPA apenas o necessário para a seleção.
NÃO chamar `pdpj_get_documento_url`, NÃO baixar, NÃO usar `pdpj_analise_essencial` nem
`pdpj_perguntar_processo` (leem demais).

Critério: o conjunto de peças de cada processo é SUFICIENTE se cobre todas as variáveis do livro de
códigos que dependem de texto, e cada peça é NECESSÁRIA se cobre alguma variável que nenhuma outra
peça selecionada cobre. Etapa final, datas de distribuição, denúncia e sentença saem dos movimentos
do censo e não pedem peça.

1. Situação do processo pelos movimentos do censo, sem Codex: inquérito arquivado, inquérito em
   curso, ação penal sem sentença, ação penal com sentença.
2. `pdpj_visao_geral_processo` (casamento, grau, sigilo, sistema, nº de documentos).
3. Se casou, `pdpj_mapa_documentos` e seleção pela tabela:
   - inquérito arquivado: procedimento policial (registro de ocorrência, representação, ofícios e
     relatório costumam vir no mesmo PDF) + promoção do MP ou decisão de arquivamento;
   - inquérito em curso: procedimento policial;
   - ação penal sem sentença: denúncia; procedimento policial como RESERVA;
   - ação penal com sentença: denúncia + sentença; procedimento policial como RESERVA.
   Reserva = só será baixada se, lida a denúncia na sessão desktop, faltarem data do registro,
   autoria no registro, representação ou diligências técnicas.
   Fica de fora: despacho, certidão, intimação, mandado, procuração, ofício avulso já contido no
   procedimento, cópias repetidas (mesmo nome e mesmo número de páginas).
4. Leitura mínima, só quando nome e categoria do mapa não bastarem para saber o papel de uma peça
   COM texto: `pdpj_read_documento` com `max_chars` 1500. Peça sem texto indexado não se lê: escolhe-se
   pelo nome e marca-se `confirmar_no_download`.

Gravar dados/alvos_tjpa.csv, uma linha por peça selecionada, sem nomes de pessoas:
ordem, numero, etapa, periodo, situacao, classe, ajuizamento, casou, grau_conferido, sigilo, sistema,
n_documentos, documento_id, papel, condicao (necessaria | reserva), nome_arquivo, data_doc, paginas,
chars, texto_indexado, leitura_minima (sim/não), confirmar_no_download (sim/não).
nome_arquivo com nome de pessoa: substituir pelo papel. Processo sem casamento ou sem peça: uma linha
com documento_id vazio e o motivo. Gravar também dados/triagem_tjpa.csv (uma linha por processo).
Se o contexto apertar, parar no processo corrente: a ordem é aleatória, o triado continua amostra.

## Fase 4 · pacote para a sessão do app desktop

Resumir o volume: processos casados, peças necessárias e reservas por papel, páginas totais,
leituras mínimas feitas, peças sem texto indexado
(que vão precisar de OCR local). Gravar no Project `claude/alvos-download-tjpa.csv` (o CSV de alvos)
e `claude/handoff-download-tjpa.md` com: objetivo, contagens, ordem de download por prioridade,
lembretes (chamar `pdpj_get_documento_url` por peça, nunca guardar a URL, no máximo 20 downloads
seguidos antes de pausa, hash SHA-256 por arquivo, deduplicar por hash, PDF sem texto vai para OCR,
pseudonimização antes de gravar texto extraído), e as variáveis do livro de códigos do plano.
Mandar o CSV ao Pedro com SendUserFile.

## Fase 5 · entrega

Atualizar o doc do plano (doc 994fb6fd-3618-47c0-8f05-a03efe2f9776, corpo 6a26f2c8-4551; ler com
sinceRev do último rev conhecido antes de escrever; o bloco de resultados é o pendente cujo intent
começa com "Resultados da coleta noturna", localizar pela leitura): preencher a seção de panorama e
a de resultados (censo e seleção de alvos), ajustar achados e riscos, marcar itens concluídos.
Atualizar claude/plano-captura-base-tjpa.md no Project. Avisar o Pedro com SendUserMessage em
poucas frases, sem travessões, dizendo o que foi coletado, quantos alvos ficaram para download e o
que ficou de fora. Se o DataJud seguir sobrecarregado, reagendar só a fase que falhou, uma vez,
para as 05:00 de Brasília.
