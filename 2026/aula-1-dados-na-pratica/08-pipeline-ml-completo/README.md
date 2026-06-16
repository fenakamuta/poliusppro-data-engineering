# 08 — Pipeline ML completo

Pipeline de Machine Learning de ponta a ponta usando **DuckDB + scikit-learn**, criado durante a Aula 1 e usado na Aula 4 como base para comparação com agentes de IA.

> Esta pasta **não é material da Aula 1** — é um teaser do que vamos fazer na Aula 4. Você pode rodar agora se quiser ver o caminho completo.

---

## A arquitetura

```
olist.parquet
     │
     ▼
[01_features.py]  ◄── DuckDB SQL faz feature engineering
     │
     ▼
features_olist.parquet
     │
     ▼
[02_train.py]  ◄── scikit-learn treina RandomForest
     │
     ▼
model_review_positivo.joblib
     │
     ▼
[03_batch_predict.py]  ◄── DuckDB lê + sklearn prediz
     │
     ▼
predictions_olist.parquet
     │
     ▼
[04_evaluate.py]  ◄── DuckDB SQL compara predição × verdade
```

---

## Dois caminhos

Você pode rodar o pipeline de duas formas:

### A) Exploração didática — abre o notebook

Use [`00-explorando-o-pipeline-ml.ipynb`](./00-explorando-o-pipeline-ml.ipynb) — é um único notebook que cobre as 4 etapas com markdown explicativo, gráficos, insights e desafios "mexa você mesmo".

Recomendado se você quer **entender** o pipeline.

### B) Produção — rode os 4 scripts em ordem

```bash
# Da raiz da pasta 08-pipeline-ml-completo
cd /caminho/para/08-pipeline-ml-completo

# 1) Features (precisa do olist.parquet baixado pelo notebook 07)
python 01_features.py

# 2) Treino
python 02_train.py

# 3) Predição em batch
python 03_batch_predict.py

# 4) Avaliação
python 04_evaluate.py
```

Recomendado se você quer **rodar** o pipeline igual a produção.

**Pré-requisito comum:** ter rodado o notebook [`07-bloco-3-olist-analise.ipynb`](../07-bloco-3-olist-analise.ipynb) pelo menos uma vez (ele baixa o `olist.parquet`).

---

## Os 4 scripts

| Script | O que faz | Saída |
|--------|----------|-------|
| [`01_features.py`](./01_features.py) | DuckDB SQL extrai features do `olist.parquet` | `features_olist.parquet` |
| [`02_train.py`](./02_train.py) | scikit-learn treina RandomForest (target: `review_positivo`) | `model_review_positivo.joblib` |
| [`03_batch_predict.py`](./03_batch_predict.py) | Carrega o modelo e prediz para todas as linhas | `predictions_olist.parquet` |
| [`04_evaluate.py`](./04_evaluate.py) | DuckDB SQL compara predição com verdade por UF | tabela impressa |

---

## Por que essa arquitetura é boa

- **DuckDB SQL** prepara as features → puro, declarativo, rápido.
- **scikit-learn** treina → modelo simples, baseline robusto.
- **joblib** persiste → arquivo portátil que pode ser servido em produção.
- **DuckDB** avalia → mesma linguagem dos engineers, mesmo motor.

É o jeito que muita gente de mercado constrói **batch scoring pipelines** em produção. Você acabou de ver na Aula 1.

---

## Versão hospedada

Os artefatos resultantes destes scripts já estão disponíveis publicamente no GitHub Release:

```
https://github.com/fenakamuta/poliusppro-data-engineering/releases/tag/aula1-olist-2026-v1
```

- `olist.parquet` (dataset)
- `features_olist.parquet` (features)
- `model_review_positivo.joblib` (modelo treinado)
- `predictions_olist.parquet` (predições)

Você pode baixar diretamente sem precisar rodar — o pipeline aqui é **didático**, para você entender o processo.

---

## Próxima aula

Na **Aula 4**, vamos comparar este pipeline clássico com um **agente de IA** que classifica os reviews em português direto, sem treinar nada. Quem ganha?
