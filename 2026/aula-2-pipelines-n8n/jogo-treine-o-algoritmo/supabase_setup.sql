-- Treine o Algoritmo — criação da tabela no Supabase
-- Cole isto no SQL Editor do Supabase (https://app.supabase.com -> SQL Editor) e rode.

create table if not exists jogadas (
  id              bigint generated always as identity primary key,
  nick            text,
  review_idx      int,
  texto           text,
  verdade         int,
  palpite         int,
  modelo          int,
  acertou         int,
  modelo_acertou  int,
  ts              timestamptz default now()
);

-- Dados de jogo, sem informação sensível: liberamos leitura/escrita.
-- (desliga o Row Level Security para a chave anônima poder inserir e ler)
alter table jogadas disable row level security;
