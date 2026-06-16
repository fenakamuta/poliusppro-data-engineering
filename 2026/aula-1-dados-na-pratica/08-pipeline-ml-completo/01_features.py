"""
Etapa 1 do pipeline: Feature engineering em SQL puro (DuckDB).

Entrada:  ../data/olist.parquet
Saída:    ../data/features_olist.parquet

A ideia é deixar claro que o engenheiro de dados **prepara as features em SQL**.
O cientista de dados (ou o modelo) recebe um dataset pronto para treinar.

Como rodar:
    python 01_features.py
"""
from pathlib import Path
import duckdb

INPUT = Path("../data/olist.parquet")
OUTPUT = Path("../data/features_olist.parquet")


def main() -> None:
    if not INPUT.exists():
        raise FileNotFoundError(
            f"{INPUT} não existe. Rode antes o notebook 07 (que baixa o dataset)."
        )

    print("Etapa 1 — feature engineering via DuckDB SQL")
    print("-" * 60)

    con = duckdb.connect()
    con.execute(
        f"""
        COPY (
            SELECT
                order_id,

                -- Numéricas brutas
                price,
                freight_value,
                product_weight_g,
                product_length_cm,
                product_height_cm,
                product_width_cm,
                product_photos_qty,
                payment_installments,
                payment_value,
                delivery_days,
                estimated_delivery_days,

                -- Derivadas
                (delivery_days - estimated_delivery_days)  AS delivery_diff,
                freight_value / NULLIF(price, 0)            AS freight_ratio,
                CASE WHEN delivered_late THEN 1 ELSE 0 END  AS delivered_late_int,

                -- Categóricas
                customer_state,
                seller_state,
                payment_type,
                product_category_en,
                (customer_state = seller_state) AS same_state,

                -- Target binário (vai ser o y do modelo)
                CASE WHEN review_positivo THEN 1 ELSE 0 END AS y_review_positivo
            FROM '{INPUT}'
            WHERE review_positivo IS NOT NULL
              AND delivery_days IS NOT NULL
        )
        TO '{OUTPUT}' (FORMAT PARQUET, COMPRESSION ZSTD)
        """
    )
    n = con.execute(f"SELECT COUNT(*) FROM '{OUTPUT}'").fetchone()[0]
    prevalencia = con.execute(
        f"SELECT AVG(y_review_positivo) FROM '{OUTPUT}'"
    ).fetchone()[0]
    print(f"  Linhas:                    {n:,}")
    print(f"  Prevalência (positivos):   {prevalencia*100:.1f}%")
    print(f"  Saída:                     {OUTPUT}  ({OUTPUT.stat().st_size/1e6:.1f} MB)")


if __name__ == "__main__":
    main()
