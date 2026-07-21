-- CHEATSHEET psql — os comandos de sobrevivência da Aula 3
-- (dentro do psql: docker compose exec postgres psql -U aluno -d olist)

-- ============================================================
-- Comandos do psql: começam com \ e NÃO levam ponto e vírgula
-- ============================================================
-- \dt            quais tabelas existem no banco
-- \d pedidos     estrutura da tabela: colunas, tipos, constraints e índices
-- \l             quais bancos existem no servidor
-- \du            usuários
-- \x             modo expandido (linha vira ficha vertical; rode de novo p/ desligar)
-- \timing        mostra o tempo de cada query
-- \?             ajuda de todos os comandos \
-- \q             sair

-- ============================================================
-- SQL básico: termina com ;
-- ============================================================

-- as primeiras linhas (o "head" do banco)
SELECT * FROM pedidos LIMIT 5;

-- quantas linhas tem
SELECT count(*) FROM pedidos;

-- só algumas colunas
SELECT pedido_id, estado, preco FROM pedidos LIMIT 10;

-- valores únicos de uma coluna
SELECT DISTINCT estado FROM pedidos;

-- o classicão: contagem por grupo, do maior pro menor
SELECT estado, count(*) AS pedidos
FROM pedidos
GROUP BY estado
ORDER BY pedidos DESC;

-- filtro + ordenação
SELECT pedido_id, preco, prazo_dias
FROM pedidos
WHERE estado = 'SP' AND preco > 500
ORDER BY preco DESC
LIMIT 10;

-- quanto a tabela ocupa em disco
SELECT pg_size_pretty(pg_total_relation_size('pedidos'));
