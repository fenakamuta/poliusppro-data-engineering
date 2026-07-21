-- Aula 3 — Bloco 1: a tabela onde o Olist aterrissa.
-- Rode no psql:  docker compose exec postgres psql -U aluno -d olist
-- (ou cole no editor SQL do DBeaver/TablePlus/pgAdmin)

CREATE TABLE pedidos (
    pedido_id       text     PRIMARY KEY,  -- identidade unica
    estado          text     NOT NULL,     -- obrigatorio
    categoria       text,
    preco           numeric,
    prazo_dias      integer,
    delivered_late  boolean,               -- atrasou? (aula 1)
    review_score    integer,               -- a nota do cliente
    risco_review    boolean                -- veio do modelo (aula 2)
);
