-- JOGO: Quebre o banco  (Bloco 2, depois de "O banco se defende do lixo")
-- A turma inventa INSERTs para passar lixo; o professor digita, o banco julga.
-- Tentativas classicas (todas testadas):

-- 1) sem id -> RECUSADO (NOT NULL)
INSERT INTO pedidos (pedido_id, estado) VALUES (NULL, 'SP');

-- 2) id repetido -> RECUSADO na 2a vez (PRIMARY KEY)
INSERT INTO pedidos (pedido_id, estado) VALUES ('jogo-1', 'SP');
INSERT INTO pedidos (pedido_id, estado) VALUES ('jogo-1', 'RJ');

-- 3) texto onde devia ser numero -> RECUSADO (tipo)
INSERT INTO pedidos (pedido_id, estado, preco) VALUES ('jogo-2', 'SP', 'caro');

-- 4) ...ate alguem tentar um ABSURDO VALIDO. Estes tres PASSAM:
INSERT INTO pedidos (pedido_id, estado, preco)      VALUES ('jogo-3', 'SP', -50);
INSERT INTO pedidos (pedido_id, estado)             VALUES ('jogo-4', 'XX');
INSERT INTO pedidos (pedido_id, estado, prazo_dias) VALUES ('jogo-5', 'SP', 9999);

-- A REVELACAO: o banco so defende as regras que voce DECLAROU.
-- Preco negativo nao viola tipo nenhum — falta um contrato:
ALTER TABLE pedidos ADD CONSTRAINT preco_positivo CHECK (preco >= 0);

-- agora o mesmo INSERT e RECUSADO:
INSERT INTO pedidos (pedido_id, estado, preco) VALUES ('jogo-6', 'SP', -50);

-- limpeza (pode deixar o CHECK criado; ele nao atrapalha o resto da aula)
DELETE FROM pedidos WHERE pedido_id LIKE 'jogo-%';
