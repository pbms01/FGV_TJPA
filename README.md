# FGV_TJPA

Base processual para um exame cibercriminológico do funil de atrito da fraude mediada por tecnologia, construída apenas com processos judiciais: o DataJud (API pública do CNJ) define o universo e sorteia a amostra, o Codex (PDPJ) localiza as peças, e uma sessão local baixa, extrai, pseudonimiza e codifica.

Estado em 20/11/2026 (revisão do plano): a fase 1 é o TJSP, e o produto é o máximo de denúncias com a descrição da conduta e a tipificação, por censo dos três códigos que nomeiam o tipo (roteiro em `docs/RUNBOOK_TJSP.md`, censo em `scripts/censo_denuncias_tjsp.py`). O recorte TJPA será replanejado depois. O alvo atual é o TJSP. A seleção dos números de processo está pronta em `scripts/sorteio_datajud_tjsp.py`, mas ainda não rodou contra o servidor, porque a API pública do DataJud ficou saturada de 19/11 à tarde até 20/11 (registro em `dados/datajud_disponibilidade_20261119_20.jsonl`).

## Estrutura

| Caminho | Conteúdo |
| --- | --- |
| `docs/plano-captura.md` | Plano completo: recorte, achados da sondagem, escada de captura, amostragem, livro de códigos, regra de seleção das peças, dado pessoal, riscos |
| `docs/linhas-de-pesquisa.md` | Arquitetura das linhas de pesquisa em criminologia informática que o livro de códigos serve |
| `docs/RUNBOOK.md` | Roteiro da coleta do TJPA (fases, ritmo, IDs do documento do plano) |
| `docs/RUNBOOK_TJSP.md` | Fase 1: censo, localização da denúncia no Codex, download e extração, campos do corpus |
| `scripts/censo_denuncias_tjsp.py` | Censo DataJud dos códigos 11978, 15623 e 15755 no TJSP, consolidado por número e ordenado pela presença de movimento de denúncia |
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

## Recorte do TJSP (decisão de 20/11/2026)

Só entram os assuntos da TPU que nomeiam o próprio tipo, conferidos no SGT versão 05/11/2026:

| Código | Assunto no SGT | Tipo | Janela de ajuizamento |
| --- | --- | --- | --- |
| 11978 | Invasão de Dispositivo Informático | art. 154-A CP | 19/11/2016 em diante, partida em 28/05/2021 (Lei 14.155/2021) |
| 15623 | Fraude Eletrônica | art. 171, § 2º-A, CP | 28/05/2021 em diante, partida em 19/09/2025 (criação do código) |
| 15755 | Estelionato Mediante Cessão de Conta Laranja | art. 171, § 2º, VII, CP | 04/05/2026 em diante (Lei 15.397/2026) |

Ficam fora o furto informático (art. 155, § 4º-B), sem código próprio e absorvido pelo 3417 Furto Qualificado, e os códigos genéricos de estelionato (3431, 3432, 14692), que não separam o meio digital. 14693, 15624 e 15756 pertencem à árvore de ato infracional.

## Como gerar a lista de alvos do TJSP

```bash
python scripts/sorteio_datajud_tjsp.py                  # até 20 alvos por célula (10 células) em alvos_tjsp.csv
python scripts/sorteio_datajud_tjsp.py --por-celula 50  # amostra maior
python scripts/sorteio_datajud_tjsp.py --so-consulta    # só imprime as consultas
```

O script retoma das células já sorteadas (`sorteio_bruto_tjsp/`), trata 429, 504 e shard falho como sobrecarga e repete, e grava as respostas brutas com data e hora para tornar o sorteio auditável.

## Cuidados

- A chave do DataJud nos scripts é a chave pública que o próprio CNJ publica para todos os usuários; pode ser substituída pela variável `DATAJUD_API_KEY`.
- Nenhum link de peça, nome de parte ou CPF entra no repositório. Texto extraído de autos fica fora do controle de versão (`.gitignore`).
- Publicações derivadas devem citar CNJ e DataJud como fonte (Portaria CNJ 160/2020, art. 4º, na redação da Portaria 374/2026).
