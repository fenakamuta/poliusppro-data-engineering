"""
API do modelo de satisfacao — Aula 2, Data Engineering POLI USP PRO.

Transforma o modelo combinado (texto + tabela) num SERVICO que qualquer
sistema pode chamar via HTTP — inclusive o n8n.

Como rodar:
    pip install -r requirements.txt
    uvicorn main:app --reload

Depois acesse http://localhost:8000/docs para testar pelo navegador.

Como o n8n usa (HTTP Request node):
    Method: POST
    URL:    http://localhost:8000/prever     (ou a URL publica, se hospedado)
    Body (JSON):
        { "texto": "produto excelente, chegou antes do prazo" }
    Resposta:
        { "satisfeito": true, "probabilidade": 0.97 }
"""
import pathlib
import urllib.request

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

MODELO_PATH = pathlib.Path("modelo_combinado.joblib")
OLIST_URL = "https://github.com/fenakamuta/poliusppro-data-engineering/releases/download/aula1-olist-2026-v1/olist.parquet"
OLIST_PATH = pathlib.Path("olist.parquet")

app = FastAPI(title="API do Modelo de Satisfacao", version="1.0")
modelo = None


def treinar_modelo():
    """Treina o modelo combinado a partir do Olist (roda uma vez)."""
    from sklearn.compose import ColumnTransformer
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.preprocessing import StandardScaler, OneHotEncoder
    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import Pipeline

    if not OLIST_PATH.exists():
        print("Baixando Olist...")
        urllib.request.urlretrieve(OLIST_URL, OLIST_PATH)

    df = pd.read_parquet(OLIST_PATH)
    dados = pd.DataFrame({
        "texto": df["review_comment_message"].fillna("").str.lower().str.replace(r"[^a-zà-ú0-9 ]", "", regex=True),
        "preco": df["price"], "frete": df["freight_value"],
        "dias_entrega": df["delivery_days"], "dias_estimado": df["estimated_delivery_days"],
        "atrasou": df["delivered_late"].astype("Int64").fillna(0),
        "estado": df["customer_state"], "categoria": df["product_category_en"].fillna("desconhecida"),
    })
    y = (df["review_score"] >= 4).astype(int)
    dados = dados.dropna(subset=["dias_entrega"])
    y = y.loc[dados.index]

    NUM = ["preco", "frete", "dias_entrega", "dias_estimado", "atrasou"]
    CAT = ["estado", "categoria"]
    pre = ColumnTransformer([
        ("texto", TfidfVectorizer(max_features=5000, ngram_range=(1, 2), min_df=3), "texto"),
        ("num", Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler())]), NUM),
        ("cat", OneHotEncoder(handle_unknown="ignore", min_frequency=30), CAT),
    ])
    m = Pipeline([("f", pre), ("clf", LogisticRegression(max_iter=1000, class_weight="balanced"))])
    m.fit(dados, y)
    joblib.dump(m, MODELO_PATH)
    print("Modelo treinado e salvo.")
    return m


@app.on_event("startup")
def carregar():
    global modelo
    if MODELO_PATH.exists():
        modelo = joblib.load(MODELO_PATH)
        print("Modelo carregado do arquivo.")
    else:
        print("Modelo nao encontrado — treinando (pode levar alguns segundos)...")
        modelo = treinar_modelo()


class Pedido(BaseModel):
    """Os dados de um pedido. So o texto e obrigatorio; o resto tem padrao."""
    texto: str = ""
    preco: float = 100.0
    frete: float = 15.0
    dias_entrega: int = 12
    dias_estimado: int = 15
    atrasou: int = 0
    estado: str = "SP"
    categoria: str = "desconhecida"


@app.get("/")
def home():
    return {"servico": "API do Modelo de Satisfacao", "use": "POST /prever"}


@app.post("/prever")
def prever(pedido: Pedido):
    """Recebe um pedido e devolve se o cliente ficou satisfeito."""
    linha = pd.DataFrame([{
        "texto": pedido.texto.lower(),
        "preco": pedido.preco, "frete": pedido.frete,
        "dias_entrega": pedido.dias_entrega, "dias_estimado": pedido.dias_estimado,
        "atrasou": pedido.atrasou, "estado": pedido.estado, "categoria": pedido.categoria,
    }])
    prob = float(modelo.predict_proba(linha)[0][1])
    return {
        "satisfeito": prob >= 0.5,
        "probabilidade": round(prob, 3),
        "usou_texto": len(pedido.texto.strip()) > 0,
    }
