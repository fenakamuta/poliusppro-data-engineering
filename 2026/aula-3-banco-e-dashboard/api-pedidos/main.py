"""API de pedidos — Aula 3, Data Engineering POLI USP PRO.

Simula o sistema da empresa: a cada chamada devolve pedidos NOVOS
(amostrados do Olist real, com id novo), prontos para o n8n inserir
no Postgres.

Como rodar:
    pip install -r requirements.txt
    uvicorn main:app --port 8001

Como o n8n usa (HTTP Request node):
    Method: GET
    URL:    http://localhost:8001/pedidos
    Resposta: lista de pedidos —
        [{ "id": "novo-a1b2c3...", "customer_state": "SP",
           "category": "housewares", "price": 89.9, "delivery_days": 9 }, ...]

O n8n transforma a lista em um item por pedido automaticamente.
"""
import pathlib
import urllib.request
import uuid

import pandas as pd
from fastapi import FastAPI

OLIST_URL = ("https://github.com/fenakamuta/poliusppro-data-engineering/"
             "releases/download/aula1-olist-2026-v1/olist.parquet")
OLIST_PATH = pathlib.Path("olist.parquet")

app = FastAPI(title="API de Pedidos (Aula 3)", version="1.0")
base = None


@app.on_event("startup")
def carregar():
    global base
    if not OLIST_PATH.exists():
        print("Baixando o Olist (uma vez so)...")
        urllib.request.urlretrieve(OLIST_URL, OLIST_PATH)
    base = pd.read_parquet(
        OLIST_PATH,
        columns=["customer_state", "product_category_en", "price", "delivery_days"],
    ).dropna()
    print(f"API pronta: {len(base)} pedidos na base.")


@app.get("/")
def home():
    return {"servico": "API de Pedidos da Aula 3", "use": "GET /pedidos"}


@app.get("/pedidos")
def pedidos(n: int = 10):
    """Devolve n pedidos novos (id inedito a cada chamada)."""
    amostra = base.sample(min(n, 100))
    return [
        {
            "id": f"novo-{uuid.uuid4().hex[:12]}",
            "customer_state": linha.customer_state,
            "category": linha.product_category_en,
            "price": round(float(linha.price), 2),
            "delivery_days": int(linha.delivery_days),
        }
        for linha in amostra.itertuples()
    ]
