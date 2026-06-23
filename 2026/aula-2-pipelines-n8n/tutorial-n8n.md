# Tutorial n8n — do zero ao primeiro pipeline

Guia passo a passo para a parte de coleta da Aula 2. Tudo gratuito, sem código.

---

## O que é o n8n (em uma frase)

Uma ferramenta visual onde você **liga blocos** numa tela para automatizar tarefas:
pegar dados de um lugar, transformar, e mandar para outro — sem programar.

Cada bloco é um **node**. O fluxo completo é um **workflow**.

---

## 1. Criar a conta (5 min)

1. Acesse https://n8n.cloud e crie uma conta gratuita.
2. (Alternativa avançada: rodar local com Docker — `docker run -p 5678:5678 n8nio/n8n`.)
3. Abra o editor de workflows. Você verá uma tela em branco com um botão "+".

---

## 2. Anatomia de um workflow

Todo pipeline de coleta tem 4 partes:

| # | Node | O que faz |
|---|------|-----------|
| 1 | **Trigger** | inicia o workflow (manual, agendado, ou por evento) |
| 2 | **HTTP Request** | chama uma API e recebe o JSON |
| 3 | **Edit Fields / Set** | escolhe e renomeia os campos que importam |
| 4 | **Saída** | salva (Google Sheets, banco, arquivo) |

---

## 3. Workflow 1 — Coletar produtos de uma API

Vamos coletar produtos da DummyJSON (API pública, sem token).

### Passo a passo

1. **Manual Trigger** — adicione o node "When clicking 'Test workflow'".
2. **HTTP Request** — adicione e configure:
   - Method: `GET`
   - URL: `https://dummyjson.com/products?limit=20`
   - Clique em "Execute step" → você verá o JSON com 20 produtos.
3. **Edit Fields (Set)** — para ficar só com o que importa:
   - `title`  → `produto`
   - `price`  → `preco`
   - `category` → `categoria`
   - `rating` → `nota`
4. **Saída** — adicione um node "Google Sheets" (ou "Convert to File" → CSV) e
   salve o resultado.

Clique em **Execute workflow**. O dado fluiu da API até a planilha.

> Os produtos da DummyJSON têm preço, categoria e avaliação — a mesma estrutura
> do Olist da Aula 1. Você acabou de montar um mini-Olist coletado por você.

---

## 4. Workflow 2 — Rodar sozinho todo dia (agendado)

Troque o **Manual Trigger** por um **Schedule Trigger**:

- Trigger Interval: `Days`
- Hora: `08:00`

Agora o workflow roda todo dia às 8h, coleta os dados e salva — sem você abrir nada.
**Isso é um pipeline de verdade.**

---

## 5. Workflow 3 — Tratar dados sujos

Dados de API quase sempre vêm com problema. Adicione tratamentos:

| Problema | Como tratar no n8n |
|----------|--------------------|
| Campos nulos | node "Filter" para remover linhas vazias |
| Texto com acento quebrado | configurar encoding UTF-8 no HTTP Request |
| Datas em formatos diferentes | node "Edit Fields" com expressão de data |
| Duplicados | node "Remove Duplicates" |

Regra de ouro: **valide antes de salvar**. Pipeline bom falha cedo e avisa, em vez
de salvar lixo silenciosamente.

---

## 6. Workflow 4 — Usar o NOSSO modelo (o capstone)

Este junta tudo da aula: o modelo treinado vira um serviço, e o n8n o consome.

> Pré-requisito: a API do modelo rodando (veja a pasta `api-do-modelo/`).

### Passo a passo

1. **Trigger** — Webhook (recebe "nova avaliação") ou Schedule.
2. **HTTP Request** — chama a API do modelo:
   - Method: `POST`
   - URL: `http://localhost:8000/prever` (ou a URL pública, se hospedado)
   - Body Content Type: `JSON`
   - Body:
     ```json
     { "texto": "{{ $json.comentario }}" }
     ```
3. **IF** — ramifica pelo resultado:
   - condição: `{{ $json.satisfeito }}` é `false`
4. **Ação** (no ramo "insatisfeito"):
   - criar uma tarefa, mandar alerta no Slack, ou e-mail para o time.
5. **Saída** — salvar tudo no Postgres / planilha.

Resultado: toda avaliação nova é classificada pelo modelo automaticamente, e o time
é avisado só quando um cliente fica insatisfeito.

---

## 7. Versionar o workflow

Seu workflow é código — versione!

1. No n8n: menu do workflow → **Download** → salva um arquivo `.json`.
2. Commite esse `.json` no GitHub.

Assim você tem histórico, backup e pode compartilhar com o time.

---

## Resumo

| Workflow | O que ensina |
|----------|--------------|
| 1. Coletar | a estrutura básica: trigger → API → transforma → salva |
| 2. Agendado | automação: rodar sozinho |
| 3. Dados sujos | qualidade: tratar antes de salvar |
| 4. Modelo | o capstone: n8n consome a API do nosso modelo |

Na **Aula 3**, esse dado coletado vai para um banco de verdade (Postgres) e vira
um dashboard.
