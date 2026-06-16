"""
Etapa 4 do pipeline: Avaliação via DuckDB SQL.

Lê predições + verdade do Olist e compara acurácia por UF.

Como rodar:
    python 04_evaluate.py
"""
from pathlib import Path
import duckdb

OLIST = Path("../data/olist.parquet")
PREDICTIONS = Path("../data/predictions_olist.parquet")


def main() -> None:
    if not OLIST.exists() or not PREDICTIONS.exists():
        raise FileNotFoundError(
            "Rode antes os notebooks/scripts anteriores."
        )

    print("Etapa 4 — avaliação por UF")
    print("-" * 60)

    df = duckdb.sql(
        f"""
        SELECT
            o.customer_state AS uf,
            COUNT(*)                                                         AS pedidos,
            ROUND(AVG(p.probabilidade_positivo) * 100, 1)                    AS prob_positivo_media,
            ROUND(AVG(CASE WHEN o.review_positivo THEN 1 ELSE 0 END) * 100, 1) AS pct_real_positivo,
            ROUND(
                AVG(
                    CASE
                        WHEN p.predicao = CASE WHEN o.review_positivo THEN 1 ELSE 0 END
                        THEN 1 ELSE 0
                    END
                ) * 100, 1
            )                                                                AS acuracia_pct
        FROM '{OLIST}' o
        INNER JOIN '{PREDICTIONS}' p USING (order_id)
        GROUP BY uf
        HAVING pedidos >= 100
        ORDER BY pedidos DESC
        LIMIT 15
        """
    ).df()

    print(df.to_string(index=False))
    print()

    geral = duckdb.sql(
        f"""
        SELECT
            ROUND(
                AVG(
                    CASE
                        WHEN p.predicao = CASE WHEN o.review_positivo THEN 1 ELSE 0 END
                        THEN 1 ELSE 0
                    END
                ) * 100, 1
            ) AS acuracia_geral_pct
        FROM '{OLIST}' o
        INNER JOIN '{PREDICTIONS}' p USING (order_id)
        """
    ).fetchone()[0]
    print(f"Acurácia geral do modelo: {geral}%")


if __name__ == "__main__":
    main()
