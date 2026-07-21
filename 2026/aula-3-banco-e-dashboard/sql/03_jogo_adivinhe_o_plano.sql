-- JOGO: Adivinhe o plano  (Bloco 1, depois do slide de EXPLAIN)
-- A turma vota ANTES de cada EXPLAIN: indice ou tabela inteira (Seq Scan)?
-- Gabarito testado no dado real da aula (96.470 linhas, indice idx_estado criado).

-- RODADA 1 — WHERE em coluna COM indice
-- gabarito: INDICE (aparece Bitmap Index Scan on idx_estado)
EXPLAIN SELECT * FROM pedidos WHERE estado = 'SP';

-- RODADA 2 — WHERE na chave primaria
-- gabarito: INDICE (Index Scan using pedidos_pkey — toda PRIMARY KEY
-- ganha um indice de graca, ninguem criou ele na mao)
EXPLAIN SELECT * FROM pedidos
WHERE pedido_id = (SELECT pedido_id FROM pedidos LIMIT 1);

-- RODADA 3 — WHERE em coluna SEM indice
-- gabarito: SEQ SCAN (nao existe indice em preco; o banco le tudo)
EXPLAIN SELECT * FROM pedidos WHERE preco > 1000;

-- RODADA 4 — duas condicoes, so uma tem indice
-- gabarito: INDICE do estado + filtro de preco por cima
-- (o banco usa o que tem e filtra o resto)
EXPLAIN SELECT * FROM pedidos WHERE estado = 'AC' AND preco > 1000;

-- RODADA 5 — a pegadinha
-- gabarito: SEQ SCAN — count(*) sem WHERE precisa contar TODAS as
-- linhas; nenhum indice resolve isso de graca
EXPLAIN SELECT count(*) FROM pedidos;

-- Moral do jogo: o banco ESCOLHE o plano sozinho, e o EXPLAIN
-- mostra a escolha. Indice ajuda a ACHAR, nao a ler tudo.
