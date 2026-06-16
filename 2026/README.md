# Edição 2026 — Data Engineering

MBA **Data Science & Analytics para Operações** — POLI USP PRO
Professor: **Fernando Henrique Vilella Nakamuta**

---

## As 4 aulas

| # | Data | Tema | Pasta |
|---|------|------|-------|
| 1 | 16/06/2026 | Dados na prática (Python, Pandas, DuckDB, Olist) | [`aula-1-dados-na-pratica/`](./aula-1-dados-na-pratica/) |
| 2 | 23/06/2026 | Pipelines visuais com n8n + APIs | [`aula-2-pipelines-n8n/`](./aula-2-pipelines-n8n/) |
| 3 | 21/07/2026 | Banco de dados + Dashboards | [`aula-3-banco-e-dashboard/`](./aula-3-banco-e-dashboard/) |
| 4 | 28/07/2026 | Agentes de IA + Pipeline ML completo | [`aula-4-agentes-ia/`](./aula-4-agentes-ia/) |

Cada aula ocupa 4 horas (3 blocos de 70 minutos com 2 intervalos de 15 minutos).

---

## Stack do curso

| Camada | Ferramenta | Por quê |
|--------|-----------|--------|
| Linguagem | Python 3.10+ | Padrão de mercado em dados |
| Editor | Cursor (ou VS Code) | IA integrada para autocomplete e chat |
| Análise interativa | Jupyter Notebook | Código + texto + resultado em 1 documento |
| Manipulação | Pandas | DataFrame em Python |
| SQL analítico | DuckDB | SQL direto em arquivos, sem servidor |
| Orquestração visual | n8n | Pipelines sem código (Aula 2) |
| Banco | Postgres + Docker | Storage real (Aula 3) |
| Dashboard | Metabase | Visualização (Aula 3) |
| ML | scikit-learn | RandomForest e regressão (Aula 4) |
| Agentes IA | LLM via API | Substituindo ML clássico (Aula 4) |

**Tudo gratuito. Tudo na sua máquina.** Você não precisará criar conta em nenhum serviço pago.

---

## Antes de começar

1. Faça o **setup do ambiente** em [`00-setup/`](./00-setup/) (30–45 minutos).
2. Confirme que o script `00-setup/teste_setup.py` imprime `Setup OK!`.
3. Abra a primeira aula em [`aula-1-dados-na-pratica/`](./aula-1-dados-na-pratica/).

---

## Estrutura do repositório

```
2026/
├── 00-setup/                      ← prepare o ambiente antes da aula 1
├── aula-1-dados-na-pratica/       ← 7 notebooks + pipeline ML
├── aula-2-pipelines-n8n/          ← (em construção)
├── aula-3-banco-e-dashboard/      ← (em construção)
├── aula-4-agentes-ia/             ← (em construção)
└── requirements.txt               ← dependências Python unificadas
```

---

## Como instalar

```bash
# A partir da raiz do repositório
cd 2026
pip install -r requirements.txt
```

Recomendado: use um ambiente virtual (`python -m venv .venv && source .venv/bin/activate`) para isolar as dependências.

---

## Datasets

Os datasets pequenos vivem dentro de `data/` de cada aula. Os grandes (CNPJ da Receita Federal, Olist, etc.) são baixados sob demanda via `wget` ou `urllib` direto do GitHub Releases deste repositório.
