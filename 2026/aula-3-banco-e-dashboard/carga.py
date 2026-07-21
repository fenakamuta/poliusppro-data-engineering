"""Aula 3 — carrega o Olist (com a coluna risco_review) na tabela pedidos.

Pre-requisitos:
    1. A stack no ar:          docker compose up -d
    2. A tabela criada:        sql/01_create_table.sql no psql
    3. Dependencias Python:    pip install -r ../requirements.txt

O Parquet e baixado sozinho do Release do GitHub na primeira execucao.

Rodar:
    python carga.py
"""
import pathlib
import urllib.request

import pandas as pd
import psycopg2                       # psycopg2 = quem fala Postgres
from psycopg2.extras import execute_values

PARQUET_URL = ("https://github.com/fenakamuta/poliusppro-data-engineering/"
               "releases/download/aula3-olist-risco-2026-v1/olist_com_risco.parquet")
PARQUET_PATH = pathlib.Path("olist_com_risco.parquet")

cols = ['pedido_id', 'estado', 'categoria', 'preco', 'prazo_dias',
        'delivered_late', 'review_score', 'risco_review']

if not PARQUET_PATH.exists():
    print("Baixando o Parquet do Release do GitHub (~2 MB)...")
    urllib.request.urlretrieve(PARQUET_URL, PARQUET_PATH)

df = pd.read_parquet(PARQUET_PATH)[cols]                # ordem do CREATE TABLE!
df = df.astype(object).where(pd.notnull(df), None)      # NaN -> NULL

conn = psycopg2.connect(host='localhost', port=5432,
                        user='aluno', password='aula3', dbname='olist')
with conn.cursor() as cur:            # cursor = por onde o SQL passa
    sql = f'INSERT INTO pedidos ({", ".join(cols)}) VALUES %s'
    execute_values(cur, sql, df.values.tolist(), page_size=5000)
conn.commit()                         # so agora esta gravado

with conn.cursor() as cur:
    cur.execute('SELECT count(*) FROM pedidos;')
    total = cur.fetchone()[0]
conn.close()
print(f"Carga concluida: {total} pedidos na tabela.")
