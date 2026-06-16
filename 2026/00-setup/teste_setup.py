"""
Teste rápido do ambiente.

Rode no terminal:
    python teste_setup.py

Se aparecer "Setup OK!" no final, seu ambiente está pronto para a Aula 1.
"""
import sys


def main() -> int:
    print("Testando ambiente para Data Engineering — POLI USP PRO 2026")
    print("-" * 60)

    # Versão do Python
    py = sys.version_info
    print(f"Python:  {py.major}.{py.minor}.{py.micro}")
    if (py.major, py.minor) < (3, 10):
        print("⚠️  Python 3.10 ou superior é recomendado.")
        return 1

    # Bibliotecas obrigatórias
    libs = [("pandas", "pd"), ("duckdb", None)]
    for lib_name, _ in libs:
        try:
            mod = __import__(lib_name)
            version = getattr(mod, "__version__", "?")
            print(f"{lib_name.capitalize():<8} {version}")
        except ImportError:
            print(f"❌ {lib_name} não está instalado.")
            print(f"   Rode: pip install {lib_name}")
            return 1

    # Teste rápido: pandas + duckdb conversando
    import pandas as pd
    import duckdb

    df = pd.DataFrame(
        {
            "cidade": ["São Paulo", "Rio", "Belo Horizonte"],
            "vendas": [1500, 800, 600],
        }
    )
    total = duckdb.sql("SELECT SUM(vendas) AS total FROM df").fetchone()[0]
    if total == 2900:
        print("-" * 60)
        print("Setup OK! Pronto para a aula.")
        return 0

    print("❌ Algo deu errado no teste pandas+duckdb. Verifique a instalação.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
