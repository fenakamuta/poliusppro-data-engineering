"""
Etapa 2 do pipeline: Treino do modelo (scikit-learn).

Entrada:  ../data/features_olist.parquet
Saída:    ../data/model_review_positivo.joblib

Constrói um Pipeline sklearn com pré-processamento + RandomForestClassifier.

Como rodar:
    python 02_train.py
"""
from pathlib import Path
import time

import duckdb
import joblib
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

FEATURES = Path("../data/features_olist.parquet")
MODEL = Path("../data/model_review_positivo.joblib")

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
TARGET = "y_review_positivo"


def main() -> None:
    if not FEATURES.exists():
        raise FileNotFoundError(
            f"{FEATURES} não existe. Rode antes 01_features.py."
        )

    print("Etapa 2 — treino do modelo (RandomForest)")
    print("-" * 60)

    # 1) Carregar features
    df = duckdb.sql(f"SELECT * FROM '{FEATURES}'").df()
    X = df[NUMERIC + CATEG]
    y = df[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 2) Construir o Pipeline
    pre = ColumnTransformer(
        transformers=[
            (
                "num",
                Pipeline([
                    ("imp", SimpleImputer(strategy="median")),
                    ("sc", StandardScaler()),
                ]),
                NUMERIC,
            ),
            (
                "cat",
                Pipeline([
                    ("imp", SimpleImputer(strategy="most_frequent")),
                    ("oh", OneHotEncoder(handle_unknown="ignore", min_frequency=20)),
                ]),
                CATEG,
            ),
        ]
    )
    pipe = Pipeline([
        ("prep", pre),
        ("clf", RandomForestClassifier(
            n_estimators=200, max_depth=12, n_jobs=-1, random_state=42
        )),
    ])

    # 3) Treinar
    t0 = time.time()
    pipe.fit(X_train, y_train)
    print(f"  Treino:   {time.time()-t0:.1f}s")

    # 4) Avaliar no holdout
    y_pred = pipe.predict(X_test)
    y_proba = pipe.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, y_proba)
    acc = accuracy_score(y_test, y_pred)
    print(f"  AUC:      {auc:.3f}")
    print(f"  Accuracy: {acc:.3f}")
    print()
    print(classification_report(
        y_test, y_pred, target_names=["NEGATIVO", "POSITIVO"]
    ))

    # 5) Salvar modelo
    joblib.dump(pipe, MODEL)
    print(f"  Modelo salvo em {MODEL} ({MODEL.stat().st_size/1024:.1f} KB)")


if __name__ == "__main__":
    main()
