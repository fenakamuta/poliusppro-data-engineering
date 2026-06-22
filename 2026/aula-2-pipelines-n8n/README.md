# Aula 2 — Do dado ao modelo, e a coleta automática

**Data:** 23/06/2026

> Primeiro o ciclo do dado (coletar → tratar → treinar → prever → salvar),
> depois como o dado novo chega sozinho (APIs + n8n).

---

## Estrutura da aula

| Parte | Bloco | Tema |
|-------|-------|------|
| ML | 1 | Do dado ao modelo: jogo, classificação, TF-IDF, cobertura e viés |
| ML | 2 | O ciclo do dado: modelo combinado (texto + tabela), limpeza, holdout, Parquet |
| Coleta | 3 | APIs (HTTP/JSON/REST) e n8n (coletar sem código) |

---

## Notebooks (siga na ordem)

| # | Arquivo | O que ensina |
|---|---------|--------------|
| 00 | [`00-como-texto-vira-numero-tfidf.ipynb`](./00-como-texto-vira-numero-tfidf.ipynb) | Como o texto vira número: Bag of Words e TF-IDF, passo a passo, vendo a tabela mudar |
| 01 | [`01-do-texto-ao-modelo.ipynb`](./01-do-texto-ao-modelo.ipynb) | Modelo **combinado** (texto + tabela) que cobre todos os pedidos — com e sem comentário |

> Os dois rodam em casa. Baixam o dataset do Olist automaticamente na primeira célula.

---

## 🎯 Atividade especial: Treine o Algoritmo

Um jogo onde a turma lê avaliações e classifica satisfeito/insatisfeito, comparando
sua acurácia com a de um modelo. **Os alunos são o benchmark** (a régua humana); o
modelo treina com as notas reais do cliente.

Veja [`jogo-treine-o-algoritmo/`](./jogo-treine-o-algoritmo/).

---

## Parte 2 — APIs e n8n

| Pré-requisito | Link |
|---------------|------|
| Conta gratuita n8n | https://app.n8n.cloud/register |
| API pública para praticar (sem token) | https://dummyjson.com/products |

O workflow exportado e o tutorial passo a passo entram aqui após a aula.
