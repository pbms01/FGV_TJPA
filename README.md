# FGV_TJPA

Base processual para um exame cibercriminológico da fraude mediada por tecnologia, construída apenas com processos judiciais. A consulta pública de julgados do tribunal fornece os números de processo, e o Codex (PDPJ) lê as peças. O texto lido vai para o repositório.

Estado em 20/11/2026, à tarde: a fase 1 é o TJSP, e o produto é o máximo de denúncias com a descrição da conduta e a tipificação. Os números-alvo vêm da Consulta de Julgados de 1º Grau do e-SAJ (cjpg), por busca textual (`scripts/cjpg_alvos.py`, roteiro em `docs/RUNBOOK_TJSP.md`). O DataJud deixou de ser a porta de entrada por dois motivos: ficou saturado de 19/11 à tarde até 20/11 (registro em `dados/datajud_disponibilidade_20261119_20.jsonl`), e o piloto mostrou que o TJSP quase não usa os códigos que nomeiam o tipo (0 julgados de ação penal no 15623 contra 1.702 pela expressão "fraude eletrônica"). O censo por código fica como denominador. O recorte TJPA será replanejado depois.

## Estrutura

| Caminho | Conteúdo |
| --- | --- |
| `docs/plano-captura.md` | Plano completo: recorte, achados da sondagem, escada de captura, amostragem, livro de códigos, regra de seleção das peças, dado pessoal, riscos |
| `docs/linhas-de-pesquisa.md` | Arquitetura das linhas de pesquisa em criminologia informática que o livro de códigos serve |
| `docs/RUNBOOK.md` | Roteiro da coleta do TJPA (fases, ritmo, IDs do documento do plano) |
| `docs/RUNBOOK_TJSP.md` | Fase 1: números-alvo pelo cjpg, localização da denúncia no Codex, gravação do texto lido, campos do corpus, achados do piloto |
| `scripts/cjpg_alvos.py` | Números-alvo do TJSP pela Consulta de Julgados de 1º Grau: quatro consultas textuais, indicadores de precisão, consolidação por número (só biblioteca padrão) |
| `scripts/cjpg_navegador.js` | Mesmo coletor para rodar numa aba do cjpg (via do piloto) |
| `scripts/testes/cjpg_fixture.html` | Fixture sintética da listagem do cjpg para testar o parser (`--teste`) |
| `dados/cjpg/` | Piloto de 20/11/2026: 110 linhas com metadados, indicadores e recorte da imputação, e os totais de cada consulta |
| `scripts/censo_denuncias_tjsp.py` | Censo DataJud dos códigos 11978, 15623 e 15755 no TJSP (denominador, quando a API voltar) |
| `scripts/sorteio_datajud_tjsp.py` | Seleção dos processos-alvo do TJSP: sorteio estratificado no servidor, autônomo, só biblioteca padrão |
| `scripts/sorteio_servidor.py` | Mesmo sorteio para o TJPA, sobre `datajud.py` |
| `scripts/datajud.py` | Cliente mínimo com rejeição de resposta parcial e registro de cada tentativa |
| `scripts/coleta_janelas.py`, `coleta_censo.py` | Censo por janelas de data (o `coleta_censo.py` depende de ordenar por `_id`, que o cluster passou a recusar) |
| `scripts/analisa_censo.py`, `amostra.py` | Análise local do censo e sorteio local |
| `scripts/panorama.py` | Panorama por metadados de TJSP, TJMG, TJBA e TJPA |
| `scripts/extrai_inicio.py` | Extração das primeiras páginas de PDF com OCR de reserva e troca de CPF/CNPJ por hash |
| `scripts/persistente.sh`, `tenta.sh` | Repetição até concluir ou até um prazo |
| `consultas/consulta_datajud_tjsp.json` | As seis consultas exatas que o sorteio do TJSP envia |
| `dados/` | Contagem por ano do estelionato no TJPA (19/11) e log de disponibilidade da API |

## Recorte do TJSP

Os tipos são os três que a TPU nomeia (decisão de 20/11/2026), mas a busca é pelo texto da sentença, não pelo código, porque o 1º grau do TJSP cadastra essas ações quase sempre como Estelionato (3431). As consultas exatas estão em `docs/RUNBOOK_TJSP.md`. Códigos de referência, conferidos no SGT versão 05/11/2026:

| Código | Assunto no SGT | Tipo | Janela de ajuizamento |
| --- | --- | --- | --- |
| 11978 | Invasão de Dispositivo Informático | art. 154-A CP | 19/11/2016 em diante, partida em 28/05/2021 (Lei 14.155/2021) |
| 15623 | Fraude Eletrônica | art. 171, § 2º-A, CP | 28/05/2021 em diante, partida em 19/09/2025 (criação do código) |
| 15755 | Estelionato Mediante Cessão de Conta Laranja | art. 171, § 2º, VII, CP | 04/05/2026 em diante (Lei 15.397/2026) |

Ficam fora o furto informático (art. 155, § 4º-B), sem código próprio e absorvido pelo 3417 Furto Qualificado, e os códigos genéricos de estelionato (3431, 3432, 14692), que não separam o meio digital. 14693, 15624 e 15756 pertencem à árvore de ato infracional.

## Como gerar a lista de alvos do TJSP

```bash
python scripts/cjpg_alvos.py                   # quatro consultas, todas as páginas, em alvos_cjpg_tjsp.csv
python scripts/cjpg_alvos.py --max-paginas 3   # piloto
python scripts/cjpg_alvos.py --teste scripts/testes/cjpg_fixture.html  # testa o parser sem rede
```

O script guarda cada resultado em `dados/cjpg/bruto/<rótulo>.jsonl`, retoma pelas páginas feitas, espera 3 s entre requisições e para, sem contornar, se a resposta trouxer CAPTCHA ou erro repetido. O sorteio por DataJud (`scripts/sorteio_datajud_tjsp.py`) continua no repositório para o censo de comparação.

## Cuidados

- A chave do DataJud nos scripts é a chave pública que o próprio CNJ publica para todos os usuários; pode ser substituída pela variável `DATAJUD_API_KEY`.
- Decisão de 20/11/2026: o texto lido das peças entra no repositório, sem pseudonimização e sem o arquivo original. O repositório é privado.
- Nenhum link de peça entra no repositório: a linha `Original:` do Codex traz token de acesso.
- Publicações derivadas devem citar o TJSP (Consulta de Julgados de 1º Grau) como fonte dos números, e CNJ e DataJud quando o censo por código for usado (Portaria CNJ 160/2020, art. 4º, na redação da Portaria 374/2026).
