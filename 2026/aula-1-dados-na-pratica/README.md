# Aula 1 — Dados na Prática

**Data:** 16/06/2026
**Duração:** 4 horas (3 blocos de 70 min + 2 intervalos de 15 min)

> Objetivo: você sai sabendo ler dados, fazer consultas em SQL e Python, e entregar sua primeira análise no GitHub.

---

## Roteiro

| Bloco | Tema | Notebooks |
|-------|------|-----------|
| 1 | Por que dados, e por que agora? | 01, 02 |
| 2 | Pegando os dados na mão | 03, 04, 05, 06 |
| 3 | Sua primeira entrega | 07 |

---

## Notebooks (siga na ordem)

| # | Arquivo | Tópico | Tempo médio |
|---|---------|--------|-------------|
| 01 | [`01-python-essencial.ipynb`](./01-python-essencial.ipynb) | Variáveis, listas, dicionários, import | 10 min |
| 02 | [`02-formatos-csv-json-parquet.ipynb`](./02-formatos-csv-json-parquet.ipynb) | Os 3 formatos mais comuns de dados | 15 min |
| 03 | [`03-pandas-basico.ipynb`](./03-pandas-basico.ipynb) | DataFrame, filtros, groupby | 25 min |
| 04 | [`04-duckdb-3-modos.ipynb`](./04-duckdb-3-modos.ipynb) | Como o DuckDB se comporta | 15 min |
| 05 | [`05-duckdb-sql-em-arquivo.ipynb`](./05-duckdb-sql-em-arquivo.ipynb) | SQL direto em arquivos | 20 min |
| 06 | [`06-pandas-vs-duckdb.ipynb`](./06-pandas-vs-duckdb.ipynb) | Quando usar cada um (benchmark) | 15 min |
| 07 | [`07-bloco-3-olist-analise.ipynb`](./07-bloco-3-olist-analise.ipynb) | Análise real do Olist (Bloco 3) | 50 min |

---

## Pasta extra

| Pasta | O que tem |
|-------|-----------|
| [`08-pipeline-ml-completo/`](./08-pipeline-ml-completo/) | Pipeline de ML pronto: features → treino → predição → avaliação. Material de apoio para a Aula 4. |
| [`data/`](./data/) | Dataset pequeno de exemplo (`clientes_pequeno.csv`/`.json`/`.parquet`). |

---

## Datasets grandes (baixados sob demanda)

Estes ficam em GitHub Releases públicos. Os notebooks já baixam automaticamente quando você roda a primeira célula.

| Nome | Linhas | Tamanho | Quando usado |
|------|--------|---------|--------------|
| `empresas.parquet` (CNPJ Receita Federal) | ~6.3M | 138 MB | Notebooks 05 e 06 |
| `olist.parquet` (Brazilian E-Commerce) | ~96k | 8.4 MB | Notebook 07 e pasta 08 |

---

## Como rodar

1. Confirme que [`../00-setup/`](../00-setup/) está concluído.
2. Abra qualquer notebook no Cursor (ou Jupyter): `jupyter notebook 01-python-essencial.ipynb`
3. Rode célula por célula (Shift + Enter).

---

## Tarefa para a Aula 2

Antes de 23/06, escolha **uma API pública** que te interesse:
- PokéAPI (https://pokeapi.co/)
- Hacker News (https://github.com/HackerNews/API)
- OpenWeather (https://openweathermap.org/api)
- IBGE (https://servicodados.ibge.gov.br/api/docs/)

Na Aula 2 vamos coletar dados dessa API automaticamente, sem código, usando n8n.
