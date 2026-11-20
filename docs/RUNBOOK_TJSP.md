# Fase 1: corpus de denúncias do TJSP

Revisão do plano em 20/11/2026. O TJSP vem primeiro, e o produto desta fase é o máximo de denúncias com a descrição da conduta e a tipificação dada pelo Ministério Público. O recorte TJPA fica suspenso e será replanejado depois desta coleta.

## Recorte

Assuntos da TPU que nomeiam o próprio tipo, conferidos no SGT versão 05/11/2026, em qualquer classe e grau, só processos públicos (sigilo 0):

| Código | Assunto | Tipo | Janela de ajuizamento |
| --- | --- | --- | --- |
| 11978 | Invasão de Dispositivo Informático | art. 154-A CP | desde 19/11/2016 |
| 15623 | Fraude Eletrônica | art. 171, § 2º-A, CP | desde 28/05/2021 (vigência do tipo; o código é de 19/09/2025) |
| 15755 | Estelionato Mediante Cessão de Conta Laranja | art. 171, § 2º, VII, CP | desde 04/05/2026 |

Censo, não amostra. Ficam fora o furto informático (sem código próprio) e os códigos genéricos de estelionato.

## Passo 1 · censo no DataJud (zero token)

    python scripts/censo_denuncias_tjsp.py

Grava `censo_tjsp.jsonl` (registros brutos, com movimentos resumidos) e `numeros_tjsp.csv` (um número por linha, já ordenado: primeiro os que têm movimento de denúncia, depois ações penais sem esse movimento, depois o resto). Retoma das janelas feitas se cair. Rodar quando a API pública responder; em 19 e 20/11/2026 ela esteve saturada.

## Passo 2 · localizar a denúncia no Codex (sessão com o conector)

Na ordem de `numeros_tjsp.csv`, ritmo de até 15 chamadas por minuto:

1. `pdpj_list_movimentos` com `tipo_filter` "Denúncia": o movimento de oferecimento ou recebimento costuma trazer o documento vinculado.
2. Sem vínculo, `pdpj_mapa_documentos`. No e-SAJ do TJSP os nomes são genéricos ("Petição.pdf", "Documento_1.pdf"), então vale a leitura mínima: `pdpj_read_documento` com `max_chars` 1500 nas candidatas (primeiras peças do MP depois da distribuição da ação penal), só para reconhecer a denúncia ou o aditamento.
3. Se o conector devolver só o dossiê de 2º grau (ele não escolhe grau, e o registro de apelação traz poucas peças), o acórdão entra como fonte de reserva: costuma resumir a narrativa da denúncia e a capitulação. Marcar como tal.
4. Peça sem texto indexado não se lê: escolhe-se pelo vínculo ou pela posição e marca-se para confirmação no download.

Gravar `alvos_denuncias_tjsp.csv`, sem nomes e sem URL: ordem, numero, codigos, documento_id, papel (denuncia, aditamento, acordao_reserva), texto_indexado, paginas, chars, leitura_minima, motivo (quando não houver alvo).

## Passo 3 · download e extração (sessão no app desktop)

1. Por alvo, `pdpj_get_documento_url`, download imediato, hash SHA-256, manifesto sem a URL, pausa a cada 20 downloads.
2. Texto: `pdftotext`; OCR (`tesseract -l por`) só nas páginas com menos de 500 caracteres.
3. Pseudonimização antes de gravar o texto: CPF e CNPJ viram hash com sal (`scripts/extrai_inicio.py`); nomes de denunciados e vítimas viram papéis (DENUNCIADO 1, VÍTIMA 1).
4. Dois campos por denúncia: a narrativa do fato (do início do relato até o pedido) e a capitulação (o trecho "incurso nas penas do art. ..." e os dispositivos citados).

PDFs e textos brutos ficam no computador, fora do repositório.

## Produto: `denuncias_tjsp.csv`

| Campo | Conteúdo |
| --- | --- |
| numero | número CNJ |
| codigo_tpu | 11978, 15623 ou 15755 (pode haver mais de um) |
| classe, orgao, ajuizamento | do DataJud |
| data_denuncia | do movimento ou do texto |
| narrativa | descrição da conduta, pseudonimizada |
| capitulacao_texto | trecho literal da tipificação |
| dispositivos | lista normalizada (ex.: CP 171 § 2º-A; CP 154-A § 3º; CP 288) |
| fonte | denuncia, aditamento ou acordao_reserva |
| extracao | texto nativo ou OCR |
| hash_pdf | SHA-256 do arquivo |

## Achados que condicionam a fase (sondagem de 20/11/2026)

- O Codex abre documentos do e-SAJ do TJSP, de 1º e de 2º grau, mas os nomes dos arquivos não dizem o que são e as peças recentes vêm sem texto indexado.
- Um número com apelação pode abrir no Codex só com o acórdão.
- O volume é desconhecido até o censo rodar; no TJPA o 15623 não aparece em processo algum, e se o TJSP também quase não o usa, a fraude eletrônica terá poucas denúncias, o que já é um achado sobre a visibilidade do tipo (ver `claude/quadro-visibilidade-tpu-lei-14155.md` no Project).
