# Plano de captura da base processual de cibercriminologia (Codex e DataJud)

19/11/2026, revisto em 20/11/2026 · Pedro Mourão. Cópia do documento editável: https://claude.ai/artifact/Kw2iKide29wwxXsfJixi2q

## Revisão de 21/11/2026: porta de entrada do TJPA

O recorte TJPA volta como fase 2, com o desenho da fase 1. O universo não sai mais do DataJud por código: os números-alvo vêm da API pública do DJEN, por busca textual nas publicações, porque o TJPA não tem consulta de sentenças de 1º grau. A lista de 01/01/2020 a 20/11/2026 tem 299 números (225 de ação penal ou apelação criminal, 99 com sentença conhecida, 74 inquéritos) e cabe inteira, o que troca a amostra pelo censo. O DataJud fica como denominador e como teste de cobertura do DJEN. No Codex, a denúncia se localiza pelo tipo de documento ou pelo movimento de recebimento, porque a "Peça Inicial" do TJPA é o ofício do delegado ou o inquérito. Detalhes em `docs/RUNBOOK_TJPA.md`. O restante deste plano (livro de códigos, regra de seleção das peças, dado pessoal, riscos) continua valendo.

## Objetivo e unidade de análise

A base mede o funil de atrito da criminalidade patrimonial mediada por tecnologia no Tribunal de Justiça do Pará, de novembro de 2016 a novembro de 2026, usando apenas processos judiciais. O produto são taxas de passagem entre etapas (inquérito, ação penal, sentença, recurso) e o perfil do que passa, separados por período normativo.

A unidade de análise é o número CNJ seguido por todas as classes que assume, e não o acórdão isolado. O escopo material do piloto é o estelionato (art. 171 do CP, inclusive o § 2º-A) e a invasão de dispositivo informático (art. 154-A do CP). O furto mediante fraude eletrônica e a via cível de consumo bancário entram numa segunda volta, depois de calibrado o método.

O TJSP, o TJMG e o TJBA entram apenas por metadados, como termo de comparação; a leitura de autos continua restrita ao TJPA. Em 20/11/2026 o recorte TJPA foi posto de lado, e o TJSP passou a ser o alvo da seleção de processos (ver `scripts/sorteio_datajud_tjsp.py`). No TJSP, entram só os códigos que nomeiam o próprio tipo: 11978 (art. 154-A), 15623 (art. 171, § 2º-A) e 15755 (art. 171, § 2º, VII); o furto informático fica fora por não ter código (ver README).

## O que a sondagem de 19/11/2026 estabeleceu

O achado que governa o desenho: no TJPA, nenhum processo usa o código de fraude eletrônica da TPU, de modo que o caráter digital do fato não se recorta por metadado em ano algum e precisa ser codificado no texto dos autos.

| Achado | Evidência | Consequência para o desenho |
| --- | --- | --- |
| O Codex não recorta universo | `pdpj_buscar_processos` aceita só CPF/CNPJ ou nome da parte, com filtros de tribunal e situação, e exibe 10 processos por chamada. O nome do MPPA devolve 580.856 processos no TJPA; o CNPJ da Polícia Civil do Pará (00368105000106), 55.184 | O universo sai do DataJud; o Codex só lê a amostra |
| O inquérito é judicializado | Classe 279 no PJe, Polícia Civil no polo ativo, MPPA (CNPJ 05054960000158) e vítima "sob sigilo" como outros participantes, sigilo público | A etapa de atribuição de autoria é observável no tribunal |
| O procedimento policial chega em bloco | Um ou dois PDFs ("Procedimento Policial.pdf" e anexo do IPL), sem texto indexado nos recém-distribuídos | O registro de ocorrência está dentro do PDF: download e extração local das primeiras páginas |
| O código de fraude eletrônica não é usado | 15623 (Estelionato por Fraude Eletrônica) foi criado na versão do SGT de 19/09/2025 (boletim CGTPUPD 3/2025). No índice do TJPA: 15623 com 0 processos; 3431 com 13.350 registros; 11978 com 195; 14692 com 216; 14693 com 3 | O recorte é o estelionato inteiro, e a mediação digital vira variável codificada |
| O DataJud responde, mas falha calado | Chave pública aceita; respostas 429, 504 e com shards falhos, que dão contagem parcial sem erro | Só se aceita resposta com zero shards falhos |
| Armadilhas medidas no TJCE (skill de levantamento, 12/09/2026) | Índice sem partes; `dataAjuizamento` numérico (`yyyyMMddHHmmss`); `assuntos.codigo` casa com qualquer item do array; mais de um registro por número; o conector não aceita grau; limite a partir da 20ª chamada de URL | Deduplicação por número e grau, conferência do grau, ritmo controlado |
| A madrugada não é janela de baixa carga | Em 20/11, das 02h59 às 05h33 de Brasília, 106 tentativas e 2 respostas íntegras; das 10h25 às 11h15, 44 tentativas e nenhuma; em 13h18, até contagem simples no TJSP deu 504. A ordenação por `_id`, desempate do `search_after`, passou a ser recusada | Coletor por janelas de data, sem ordenação; sorteio no próprio servidor; horário escolhido por medição |

Reiter leu o salto de 4 para 217 processos com o código 15623, de 2024 para 2025, como consolidação da resposta institucional. A data de criação do código sugere artefato de classificação, hipótese que esta base pode testar. O código 11978 é associado ao art. 154-A pelo mesmo artigo; o nome no SGT ainda não foi conferido.

## Arquitetura em três camadas

1. Metadados (DataJud, por script, fora do contexto do modelo): universo, deduplicação, contagens por etapa, sorteio estratificado.
2. Autos (Codex, em sessão): `pdpj_visao_geral_processo` e `pdpj_mapa_documentos` para triagem e seleção das peças.
3. Local (scripts, no app desktop): download com hash SHA-256 e manifesto sem URL, extração das primeiras páginas, OCR só em página-imagem, pseudonimização antes de gravar, codificação.

## Recorte

- Assuntos, em qualquer posição do array: 3431, 15623, 14692, 14693 e 11978.
- Classes de etapa: 272 (notícia de crime), 279 (inquérito), 280 (flagrante), 283 e 10943 (ação penal), 417 (apelação). A 307 marca prisão; a 355 (precatória) sai.
- Exclusão: violência doméstica e contra a mulher, por assunto e órgão julgador, já no primeiro passo.

Registros com assunto 3431 no índice do TJPA, por ano (contagem bruta, sem deduplicação; 2026 até 19/11):

| Ano | Registros | Inquérito (279) | Ação penal (283) | Apelação (417) |
| --- | --- | --- | --- | --- |
| 2026 | 1.423 | 891 | 122 | 128 |
| 2025 | 1.394 | 626 | 372 | 98 |
| 2024 | 1.515 | 657 | 491 | 88 |
| 2023 | 1.472 | 540 | 487 | 70 |
| 2022 | 1.235 | 414 | 411 | 61 |
| 2021 | 920 | 312 | 326 | 43 |
| 2020 | 742 | 304 | 288 | 33 |
| 2019 | 907 | 353 | 436 | 32 |
| 2018 | 620 | 204 | 363 | 13 |
| 2017 | 396 | 99 | 251 | 17 |
| 2016 | 278 | 154 | 96 | 10 |

Períodos normativos: P1 até a vigência da Lei 13.964/2019 (janeiro de 2020, data exata a conferir); P2 até 27/05/2021; P3 com representação exigida e competência pelo domicílio da vítima (Lei 14.155/2021) até 03/05/2026; P4 com ação incondicionada desde 04/05/2026 (Lei 15.397/2026), só para fatos posteriores. Num estudo de tribunal único, a mudança de competência de 2021 pode explicar sozinha parte da alta de 2021 para 2022.

## Escada de captura

1. Degrau 0, universo (DataJud): deduplicação, trajetória do número entre classes, contagens por movimento. Sigilosos contados como massa escura.
2. Degrau 1, triagem (Codex): visão geral e mapa de documentos.
3. Degrau 2, seleção das peças necessárias e suficientes (abaixo), com leitura mínima.
4. Degrau 3, sessão no app desktop: download, extração, OCR, pseudonimização e codificação, com dupla codificação em 10% da amostra.
5. Degrau 4, consolidação: taxas por etapa e período com intervalo de confiança e análise de sobrevivência.

## Desenho amostral

Seis células (inquérito e ação penal em P1, P2 e P3), 20 processos por célula no piloto, sorteio com semente fixa e ordem aleatória, de modo que o que for lido primeiro continue amostra. No plano completo, 96 por célula para margem de 10 pontos a 95%, corrigido pela prevalência digital observada no piloto (96/p).

```latex
n = \frac{z^2 \, p(1-p)}{e^2} = \frac{1{,}96^2 \times 0{,}25}{0{,}10^2} \approx 96
```

## Livro de códigos

| Variável | Peça de origem | Valores | Linha |
| --- | --- | --- | --- |
| mediação digital | registro de ocorrência, denúncia | sim, não, indeterminado, com o critério de Wall anotado | 1.1 |
| vetor | registro de ocorrência | PIX, boleto, cartão, conta invadida, WhatsApp ou perfil falso, marketplace, falso funcionário, investimento, outro | 1.1, 3.1 |
| datas | registro, denúncia, movimentos | fato, registro, distribuição, denúncia, sentença | 4.4 |
| autoria no registro | registro de ocorrência | conhecida, desconhecida | 2.2 |
| diligências técnicas | inquérito | requisição a banco, provedor ou operadora; resposta; dado já inexistente | 4.4 |
| representação | inquérito, autos | presente, ausente, não exigida | 3.2 |
| etapa final | movimentos | arquivado, denunciado, sentenciado, recorrido, em curso | 1.2 |
| fundamento do arquivamento | decisão de arquivamento | autoria não identificada, atipicidade, decadência, prescrição, outro | 2.2, 3.2 |
| papel do denunciado | denúncia | titular da conta, cedente de chip, sacador, operador, organizador, indeterminado | 2.1, 2.2 |
| tipo de vítima | registro de ocorrência | pessoa física, jurídica, administração; vulnerabilidade declarada | 3.4 |
| dano declarado | registro de ocorrência | valor; recuperação pelo banco | 3.3 |
| classificação jurídica | denúncia e sentença | art. 171 caput, § 2º-A, § 4º; art. 154-A; art. 155, § 4º-B; reclassificação | 1.1, 1.4 |
| desfecho | movimentos e sentença | condenação, absolvição com fundamento, extinção, acordo de não persecução penal | 4.2 |

Seleção das peças: o conjunto de cada processo é suficiente quando cobre todas as variáveis que dependem de texto, e cada peça é necessária quando cobre alguma que nenhuma outra cobre. Etapa e datas processuais saem dos movimentos do DataJud.

| Situação pelos movimentos | Peças necessárias | Reserva |
| --- | --- | --- |
| Inquérito arquivado | procedimento policial; promoção do MP ou decisão de arquivamento | nenhuma |
| Inquérito em curso | procedimento policial | nenhuma |
| Ação penal sem sentença | denúncia | procedimento policial |
| Ação penal com sentença | denúncia; sentença | procedimento policial |

A reserva só é baixada se a denúncia não trouxer data do registro, autoria no registro, representação ou diligências técnicas. Na triagem, lê-se no máximo 1.500 caracteres de uma peça, e só quando nome e categoria não bastarem.

## Dado pessoal e segurança

- Nada é gravado antes da pseudonimização: nomes saem na extração; CPF e CNPJ viram hash com sal secreto (`extrai_inicio.py`).
- O link de peça devolvido pelo conector é credencial portadora sem expiração: não vai para arquivo nem repositório.
- Violência doméstica e dignidade sexual ficam fora já no primeiro passo.
- Base legal e parecer ético a definir antes da amostra completa.
- Publicações citam CNJ e DataJud como fonte (Portaria CNJ 160/2020, art. 4º, redação da Portaria 374/2026).

## Riscos e controles

| Risco | Controle |
| --- | --- |
| Digital misturado no 3431 | Codificação no texto, categoria indeterminado, kappa de pelo menos 0,7 |
| Cobertura do conector por ano | Taxa de casamento DataJud para Codex medida no piloto |
| Contagem parcial por shard falho | Resposta com shard falho é rejeitada e registrada |
| Grau e duplicidade | Deduplicação por número e grau |
| Maturação de 2025 e 2026 | Análise de sobrevivência |
| Sigilo das cautelares | Diligências contadas só quando juntadas ao inquérito público |
| Competência antes de maio de 2021 | Séries quebradas entre P2 e P3 |
| Disponibilidade do DataJud | Sorteio no servidor, coleta por janelas, retomada automática |

## Fontes

- [Boletim CGTPUPD nº 3/2025](https://www.tjdft.jus.br/pje/tabelasprocessuaisunificadas/boletim-cgtpupd-edicao-3-de-2025_para-publicar.pdf)
- [Reiter, Levantamento de dados de crimes cibernéticos no Brasil a partir do DATAJUD/CNJ, Revista Científica do CPJM, 2026](https://rcpjm.emnuvens.com.br/revista/article/download/439/331/783)
- [Lei 14.155/2021](https://planalto.gov.br/ccivil_03/_ato2019-2022/2021/lei/l14155.htm)
- [Portaria CNJ 160/2020, compilada com a Portaria 374/2026](https://atos.cnj.jus.br/files/compilado150115202608196a85c53b90432.pdf)
- Sondas próprias de 19 e 20/11/2026 (Codex e API pública do DataJud), registradas em `dados/`
