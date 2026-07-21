# Aula 3 — Banco de dados + Dashboard

**Data:** 21/07/2026

> **Antes da aula:** siga o [`setup-docker.md`](./setup-docker.md) — instala o Docker e
> baixa as imagens (~1,5 GB). Na Wi-Fi do estúdio, com a turma toda ao mesmo tempo, não dá tempo.

---

## O que vamos ver

| Bloco | Tema | Artefatos |
|-------|------|-----------|
| 1 | Por que banco de dados (Postgres + Docker) | `docker-compose.yml`, `sql/`, `carga.py` |
| 2 | n8n alimentando o Postgres | `api-pedidos/`, `n8n-workflow-aula3.json` |
| 3 | Dashboard no Metabase | `sql/02_queries_da_aula.sql` (os 4 cartões) |

---

## Roteiro da aula, artefato por artefato

### Bloco 1 — subir o banco e carregar o Olist

```bash
docker compose up -d                                      # sobe Postgres + Metabase
docker compose exec postgres psql -U aluno -d olist       # entra no banco
```

1. No psql, cole o [`sql/01_create_table.sql`](./sql/01_create_table.sql) — cria a tabela `pedidos`.
2. Carregue o dado (o Parquet baixa sozinho do Release do GitHub):

   ```bash
   python carga.py        # 96.470 pedidos, com a coluna risco_review do modelo da Aula 2
   ```

3. As queries do bloco (a query da Aula 1, índice, EXPLAIN) estão no
   [`sql/02_queries_da_aula.sql`](./sql/02_queries_da_aula.sql), na ordem da aula.

### Bloco 2 — o n8n gravando no banco

1. Suba a API de pedidos (simula o sistema da empresa; devolve pedidos novos a cada chamada):

   ```bash
   cd api-pedidos
   pip install -r requirements.txt
   uvicorn main:app --port 8001
   ```

2. Rode o n8n **local** (`npx n8n` → `localhost:5678`). O n8n.cloud não enxerga a sua máquina.
3. Monte o workflow (ou importe o [`n8n-workflow-aula3.json`](./n8n-workflow-aula3.json)):
   `Manual Trigger → HTTP Request (GET http://localhost:8001/pedidos) → Edit Fields → Postgres`.
   Na credencial do Postgres: host `localhost`, porta `5432`, `aluno` / `aula3` / `olist`.
4. Execute e veja o `SELECT count(*) FROM pedidos;` subir. Ninguém digitou um INSERT.

### Bloco 3 — o dashboard

1. Abra `http://localhost:3000` (Metabase) e conecte no banco.
   ⚠️ **O host é `postgres`** (o nome do serviço no compose), **não** `localhost` —
   o Metabase roda dentro do Docker.
2. Monte o dashboard "Pedidos em risco" com os 4 cartões — o SQL de cada um está no
   fim do [`sql/02_queries_da_aula.sql`](./sql/02_queries_da_aula.sql).

---

## Mapa dos arquivos

| Arquivo | O que é |
|---------|---------|
| [`setup-docker.md`](./setup-docker.md) | Tutorial de pré-aula (instalar Docker + baixar imagens) |
| [`docker-compose.yml`](./docker-compose.yml) | Postgres (`:5432`) + Metabase (`:3000`) com um comando |
| [`sql/01_create_table.sql`](./sql/01_create_table.sql) | O schema da tabela `pedidos` |
| [`sql/02_queries_da_aula.sql`](./sql/02_queries_da_aula.sql) | Todas as queries, na ordem da aula |
| [`carga.py`](./carga.py) | Carrega o Parquet (com `risco_review`) na tabela |
| [`api-pedidos/`](./api-pedidos/) | API que devolve pedidos novos — o que o n8n coleta |
| [`n8n-workflow-aula3.json`](./n8n-workflow-aula3.json) | O workflow pronto para importar no n8n |

> Dependências Python: já estão no [`requirements.txt`](../requirements.txt) do curso
> (`psycopg2-binary`, `pyarrow`, `pandas`). Só a `api-pedidos/` tem as suas próprias.
