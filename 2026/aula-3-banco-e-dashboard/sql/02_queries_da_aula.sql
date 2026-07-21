-- Aula 3 — todas as queries, na ordem em que aparecem na aula.
-- Cole bloco a bloco no psql (ou no editor SQL do seu cliente).

-- ============================================================
-- BLOCO 1
-- ============================================================

-- A query da Aula 1 — a mesma que revelou "atraso -> review ruim".
-- So mudou o FROM: la era o arquivo, aqui e a tabela.
SELECT delivered_late, round(avg(review_score), 2) AS score
FROM pedidos
GROUP BY delivered_late;

-- Indice: antes, veja o plano do banco (Seq Scan = le tudo)
EXPLAIN ANALYZE SELECT * FROM pedidos WHERE estado = 'SP';

CREATE INDEX idx_estado ON pedidos(estado);

-- ...e depois: o Seq Scan some (aparece Bitmap Index Scan)
EXPLAIN ANALYZE SELECT * FROM pedidos WHERE estado = 'SP';

-- ============================================================
-- BLOCO 2
-- ============================================================

-- O momento ao vivo: rode ANTES de executar o workflow no n8n...
SELECT count(*) FROM pedidos;
-- ...execute o workflow... e rode DE NOVO. O numero subiu.

-- O banco se defende do lixo (os dois ERROS abaixo sao o ponto):
INSERT INTO pedidos (pedido_id, estado)
VALUES (NULL, 'SP');      -- ERRO: viola NOT NULL

INSERT INTO pedidos (pedido_id, estado)
VALUES ('abc', 'SP');     -- ok da 1a vez...

INSERT INTO pedidos (pedido_id, estado)
VALUES ('abc', 'SP');     -- ERRO: PRIMARY KEY duplicada

-- limpe o teste:
DELETE FROM pedidos WHERE pedido_id = 'abc';

-- Transacao (slide "A transferencia que nao pode dar errado"):
-- NAO RODE — a tabela contas e ilustracao classica, nao existe no banco olist.
--   BEGIN;
--   UPDATE contas SET saldo = saldo - 100 WHERE id = 1;
--   UPDATE contas SET saldo = saldo + 100 WHERE id = 2;
--   COMMIT;

-- ============================================================
-- BLOCO 3 — o SQL dos cartoes do dashboard "Pedidos em risco"
-- (versao dedicada, pronta para o Metabase: 05_dashboard_queries.sql)
-- ============================================================

-- 1) total de pedidos  (e ESTE que sobe no momento ao vivo)
SELECT count(*) FROM pedidos;

-- 2) total em risco
SELECT count(*) FROM pedidos WHERE risco_review;

-- 3) risco por estado  (no cartao seguinte, troque estado por categoria)
SELECT estado, count(*) AS risco FROM pedidos
WHERE risco_review GROUP BY estado ORDER BY risco DESC;

-- 4) os piores, para o time atacar amanha (ordenado pelo risco REAL)
SELECT pedido_id, estado, round(risco_prob, 2) AS risco FROM pedidos
WHERE risco_review ORDER BY risco_prob DESC LIMIT 20;
