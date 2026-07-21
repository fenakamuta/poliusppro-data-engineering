-- DASHBOARD "Pedidos em risco" — o SQL de cada cartao, pronto para colar
-- no Metabase:  + Novo -> Consulta SQL -> cola -> Salvar -> adicionar ao dashboard
--
-- Lembrete da conexao: host = postgres (nome do servico no compose), NAO localhost.
-- Auto-refresh: no dashboard, icone de relogio -> 1 minuto.

-- ============================================================
-- CARTAO 1 — "Total de pedidos"  (visualizacao: Numero)
-- e ESTE que sobe ao vivo quando o n8n roda
-- ============================================================
SELECT count(*) FROM pedidos;

-- ============================================================
-- CARTAO 2 — "Em risco hoje"  (visualizacao: Numero)
-- ============================================================
SELECT count(*) FROM pedidos WHERE risco_review;

-- ============================================================
-- CARTAO 3 — "Risco por estado"  (visualizacao: Barra)
-- ============================================================
SELECT estado, count(*) AS risco
FROM pedidos
WHERE risco_review
GROUP BY estado
ORDER BY risco DESC;

-- ============================================================
-- CARTAO 4 — "Risco por categoria"  (visualizacao: Barra)
-- LIMIT 15 porque sao ~70 categorias; sem limite vira um pente
-- ============================================================
SELECT categoria, count(*) AS risco
FROM pedidos
WHERE risco_review
GROUP BY categoria
ORDER BY risco DESC
LIMIT 15;

-- ============================================================
-- CARTAO 5 — "Os piores — atacar amanha"  (visualizacao: Tabela)
-- ordenado pelo risco REAL previsto pelo modelo
-- ============================================================
SELECT pedido_id, estado, round(risco_prob, 2) AS risco
FROM pedidos
WHERE risco_review
ORDER BY risco_prob DESC
LIMIT 20;
