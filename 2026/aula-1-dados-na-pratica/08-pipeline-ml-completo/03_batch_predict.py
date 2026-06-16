"""
Etapa 3 do pipeline: Predição em batch (DuckDB ↔ sklearn ↔ DuckDB).

Entrada:  ../data/features_olist.parquet
          ../data/model_review_positivo.joblib
Saída:    ../data/predictions_olist.parquet

Demonstra o ciclo de produção:
- DuckDB lê o batch de features
- sklearn aplica o modelo
- DuckDB escreve as predições em Parquet

Como rodar:
    python 03_batch_predict.py
"""
from pathlib import Path
import time

import duckdb
import joblib
import pandas as pd

FEATURES = Path("../data/features_olist.parquet")
MODEL = Path("../data/model_review_positivo.joblib")
PREDICTIONS = Path("../data/predictions_olist.parquet")

NUMERIC = [
    "price", "freight_value", "product_weight_g",
    "product_length_cm", "product_height_cm", "product_width_cm",
    "product_photos_qty", "payment_installments", "payment_value",
    "delivery_days", "estimated_delivery_days",
    "delivery_diff", "freight_ratio", "delivered_late_int",
]
CATEG = [
    "customer_state", "seller_state", "payment_type",
    "product_category_en", "same_state",
]


def main() -> None:
    if not FEATURES.exists() or not MODEL.exists():
        raise FileNotFoundError(
            "Rode antes 01_features.py e 02_train.py."
        )

    print("Etapa 3 — predição em batch")
    print("-" * 60)

    con = duckdb.connect()
    batch = con.execute(
        f"""
        SELECT order_id, {", ".join(NUMERIC + CATEG)}
        FROM '{FEATURES}'
        """
    ).df()
    print(f"  Linhas carregadas: {len(batch):,}")

    model = joblib.load(MODEL)
    t0 = time.time()
    proba = model.predict_proba(batch[NUMERIC + CATEG])[:, 1]
    labels = model.predict(batch[NUMERIC + CATEG])
    print(f"  Predição:          {time.time()-t0:.2f}s")

    result = pd.DataFrame({
        "order_id": batch["order_id"],
        "probabilidade_positivo": proba,
        "predicao": labels,
        "predicao_humana": [
            "POSITIVO" if x == 1 else "NEGATIVO" for x in labels
        ],
    })

    con.register("res", result)
    con.execute(
        f"COPY res TO '{PREDICTIONS}' (FORMAT PARQUET, COMPRESSION ZSTD)"
    )
    print(f"  Saída:             {PREDICTIONS} ({PREDICTIONS.stat().st_size/1024:.1f} KB)")


if __name__ == "__main__":
    main()
