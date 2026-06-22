# 🎯 Treine o Algoritmo

Jogo de classificação de sentimento para a **Aula 2** — Data Engineering, POLI USP PRO.

O aluno lê avaliações reais de e-commerce (em português) e adivinha se o cliente ficou satisfeito. No fim, compara sua acurácia com a de um modelo de Machine Learning. Cada jogada vira dado coletado — que o professor usa para treinar um modelo ao vivo.

---

## Como funciona

```
1. Aluno lê um review (texto) e chuta 👍 / 👎
2. Sistema revela: a verdade (estrela do cliente) + o que o MODELO previu
3. Placar da turma compara todos vs o modelo
4. Toda jogada é gravada → vira o dataset para o professor treinar ao vivo
```

---

## Rodar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

Abre em `http://localhost:8501`.

---

## Deploy gratuito (Streamlit Community Cloud)

1. Garanta que esta pasta está no GitHub (já está, neste repo)
2. Acesse https://share.streamlit.io e faça login com o GitHub
3. "New app" → selecione o repo `poliusppro-data-engineering`
4. **Main file path:** `2026/aula-2-pipelines-n8n/jogo-treine-o-algoritmo/app.py`
5. Deploy → você recebe uma URL pública tipo `treine-o-algoritmo.streamlit.app`
6. Compartilhe o link com a turma no início da aula

> O deploy leva ~2 minutos. A primeira abertura treina o modelo (~1s).

---

## Fluxo na aula

| Momento | O que fazer |
|---------|-------------|
| Início | Compartilhe a URL. Turma joga por ~10 min |
| Durante | Acompanhe o placar enchendo ao vivo |
| Coleta | No app, abra "⚙️ Professor" → baixe `jogadas_coletadas.csv` |
| Treino ao vivo | Abra `treinar-ao-vivo.ipynb` e treine um modelo com os dados da turma |
| Fechamento | Compare: acurácia da turma vs modelo vs (na Aula 4) o LLM |

---

## Arquivos

| Arquivo | O que é |
|---------|---------|
| `app.py` | O jogo (Streamlit) |
| `reviews.csv` | 6.000 reviews reais do Olist (texto + estrela) |
| `requirements.txt` | Dependências |
| `treinar-ao-vivo.ipynb` | Notebook para o professor treinar um modelo ao vivo |
| `plays.db` | Banco SQLite gerado em runtime (jogadas) — não versionado |

---

## Sobre os dados

Os reviews vêm do **Brazilian E-Commerce Public Dataset by Olist** — o mesmo da Aula 1. São avaliações reais, em português, de compras feitas entre 2016 e 2018.

O rótulo de "satisfeito" é derivado da nota: **4 ou 5 estrelas = satisfeito**, 1 a 3 = insatisfeito.
