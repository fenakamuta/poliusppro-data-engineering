"""Gera o olist_com_risco.parquet — o dado da Aula 3 (script do professor).

Treina o mesmo modelo combinado da Aula 2 (texto + tabela) e usa a previsao
para preencher a coluna risco_review: True quando o modelo preve cliente
INsatisfeito. E o "presente pronto" que os alunos baixam do Release.

Rodar (uma vez, antes da aula):
    python gerar_parquet_risco.py
Publicar:
    gh release create aula3-olist-risco-2026-v1 olist_com_risco.parquet \
       --title "Aula 3 — Olist com risco_review" \
       --notes "Olist deduplicado por pedido + coluna risco_review prevista pelo modelo da Aula 2."
"""
import pathlib
import urllib.request

import pandas as pd

OLIST_URL = ("https://github.com/fenakamuta/poliusppro-data-engineering/"
             "releases/download/aula1-olist-2026-v1/olist.parquet")
OLIST_PATH = pathlib.Path("olist.parquet")
OUT_PATH = pathlib.Path("olist_com_risco.parquet")


def treinar_modelo(df):
    """A mesma receita da api-do-modelo da Aula 2."""
    from sklearn.compose import ColumnTransformer
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder, StandardScaler

    dados = pd.DataFrame({
        "texto": df["review_comment_message"].fillna("").str.lower()
                   .str.replace(r"[^a-zà-ú0-9 ]", "", regex=True),
        "preco": df["price"], "frete": df["freight_value"],
        "dias_entrega": df["delivery_days"], "dias_estimado": df["estimated_delivery_days"],
        "atrasou": df["delivered_late"].astype("Int64").fillna(0),
        "estado": df["customer_state"],
        "categoria": df["product_category_en"].fillna("desconhecida"),
    })
    y = (df["review_score"] >= 4).astype(int)

    NUM = ["preco", "frete", "dias_entrega", "dias_estimado", "atrasou"]
    CAT = ["estado", "categoria"]
    pre = ColumnTransformer([
        ("texto", TfidfVectorizer(max_features=5000, ngram_range=(1, 2), min_df=3), "texto"),
        ("num", Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler())]), NUM),
        ("cat", OneHotEncoder(handle_unknown="ignore", min_frequency=30), CAT),
    ])
    modelo = Pipeline([("f", pre),
                       ("clf", LogisticRegression(max_iter=1000, class_weight="balanced"))])
    modelo.fit(dados, y)
    return modelo, dados


def main():
    if not OLIST_PATH.exists():
        print("Baixando o Olist...")
        urllib.request.urlretrieve(OLIST_URL, OLIST_PATH)

    df = pd.read_parquet(OLIST_PATH)
    # um pedido por linha: a tabela tem PRIMARY KEY em pedido_id
    df = df.drop_duplicates(subset="order_id", keep="first").dropna(subset=["delivery_days"])

    print(f"Treinando o modelo em {len(df)} pedidos...")
    modelo, dados = treinar_modelo(df)
    prob_satisfeito = modelo.predict_proba(dados)[:, 1]
    risco_prob = (1 - prob_satisfeito).round(4)  # prob. de review RUIM (0 a 1)

    out = pd.DataFrame({
        "pedido_id": df["order_id"],
        "estado": df["customer_state"],
        "categoria": df["product_category_en"],
        "preco": df["price"],
        "prazo_dias": df["delivery_days"].astype("Int64"),
        "delivered_late": df["delivered_late"].astype("boolean"),
        "review_score": df["review_score"].astype("Int64"),
        "risco_prob": risco_prob,           # o termometro: quao arriscado
        "risco_review": risco_prob >= 0.5,  # o alarme: age ou nao age
    })
    out.to_parquet(OUT_PATH, index=False)

    total, risco = len(out), int(out["risco_review"].sum())
    print(f"OK: {OUT_PATH} — {total} pedidos, {risco} em risco ({risco / total:.1%}).")


if __name__ == "__main__":
    main()
