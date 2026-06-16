# Aula 4 — Agentes de IA + Pipeline ML completo

**Data:** 28/07/2026

> Em construção. Material disponível depois da Aula 3.

---

## O que vamos ver

| Bloco | Tema |
|-------|------|
| 1 | LLM como ferramenta + agente em n8n (classificando reviews PT-BR) |
| 2 | Agente robusto: guardrails, observability, custo |
| 3 | Projeto final dos alunos + ponte para cloud |

---

## A ponte com a Aula 1

O **pipeline ML** que você construiu em [`../aula-1-dados-na-pratica/08-pipeline-ml-completo/`](../aula-1-dados-na-pratica/08-pipeline-ml-completo/) vai ser comparado aqui com um **agente de IA** que classifica os reviews em português direto.

Pergunta da aula: **quem ganha?**
- Modelo clássico (RandomForest treinado com features)
- vs. Agente LLM (lê o texto e diz se é positivo)

---

## Pré-requisitos

- Aulas 1, 2 e 3 concluídas
- API key da OpenAI ou Anthropic (free tier serve)
- Conta n8n da Aula 2

---

## O que vai ter aqui depois

- Workflow n8n com agente IA classificando reviews
- Notebook comparando acurácia: pipeline clássico vs LLM
- Material sobre guardrails e observability
