"""
🎯 Treine o Algoritmo — jogo de classificação de sentimento

Aula 2 · Data Engineering · POLI USP PRO

Como funciona:
  1. O aluno lê um review de e-commerce (em português)
  2. Chuta se o cliente ficou satisfeito (👍) ou não (👎)
  3. O sistema revela a verdade (a estrela que o cliente deu) e
     o que o MODELO previu para o mesmo review
  4. Cada jogada é gravada — vira o "dataset" que o professor
     usa para treinar um modelo ao vivo na aula

Rode local:   streamlit run app.py
Deploy:       Streamlit Community Cloud (veja README.md)
"""
import sqlite3
from datetime import datetime, timezone

import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

# ----------------------------------------------------------------------
# Configuração
# ----------------------------------------------------------------------
st.set_page_config(page_title="Treine o Algoritmo", page_icon="🎯", layout="centered")

REVIEWS_CSV = "reviews.csv"
DB_PATH = "plays.db"


# ----------------------------------------------------------------------
# Carrega dados + treina o modelo (uma vez, cacheado)
# ----------------------------------------------------------------------
@st.cache_resource
def carregar_e_treinar():
    df = pd.read_csv(REVIEWS_CSV)
    # Treina o modelo em 60% e deixa 40% como "pool de jogo" (reviews
    # que o modelo nunca viu — comparação justa entre humano e máquina)
    treino, pool = train_test_split(
        df, test_size=0.4, random_state=42, stratify=df["positivo"]
    )
    modelo = Pipeline([
        ("tfidf", TfidfVectorizer(max_features=5000, ngram_range=(1, 2), min_df=3)),
        ("clf", LogisticRegression(max_iter=1000, class_weight="balanced")),
    ])
    modelo.fit(treino["texto"], treino["positivo"])

    pool = pool.reset_index(drop=True).copy()
    pool["modelo_pred"] = modelo.predict(pool["texto"])
    # Acurácia do modelo no pool de jogo (a "barra a ser batida")
    acc_modelo = (pool["modelo_pred"] == pool["positivo"]).mean()
    return pool, acc_modelo


@st.cache_resource
def get_db():
    con = sqlite3.connect(DB_PATH, check_same_thread=False)
    con.execute("""
        CREATE TABLE IF NOT EXISTS jogadas (
            nick TEXT, review_idx INTEGER, texto TEXT,
            verdade INTEGER, palpite INTEGER, modelo INTEGER,
            acertou INTEGER, modelo_acertou INTEGER, ts TEXT
        )
    """)
    con.commit()
    return con


pool, acc_modelo = carregar_e_treinar()
con = get_db()


# ----------------------------------------------------------------------
# Estado da sessão
# ----------------------------------------------------------------------
def init_state():
    st.session_state.setdefault("nick", None)
    st.session_state.setdefault("review_atual", None)
    st.session_state.setdefault("revelado", False)
    st.session_state.setdefault("vistos", [])
    st.session_state.setdefault("acertos", 0)
    st.session_state.setdefault("total", 0)


init_state()


def sortear_review():
    """Sorteia um review do pool que esse aluno ainda não viu."""
    candidatos = [i for i in range(len(pool)) if i not in st.session_state["vistos"]]
    if not candidatos:
        st.session_state["vistos"] = []
        candidatos = list(range(len(pool)))
    import random as _r
    # Semente baseada no nick + total visto (varia sem usar random global proibido)
    idx = candidatos[(hash(st.session_state["nick"]) + st.session_state["total"]) % len(candidatos)]
    st.session_state["review_atual"] = idx
    st.session_state["revelado"] = False


def registrar(palpite: int):
    idx = st.session_state["review_atual"]
    linha = pool.iloc[idx]
    verdade = int(linha["positivo"])
    modelo = int(linha["modelo_pred"])
    acertou = int(palpite == verdade)
    modelo_acertou = int(modelo == verdade)

    con.execute(
        "INSERT INTO jogadas VALUES (?,?,?,?,?,?,?,?,?)",
        (st.session_state["nick"], int(idx), linha["texto"], verdade,
         palpite, modelo, acertou, modelo_acertou,
         datetime.now(timezone.utc).isoformat()),
    )
    con.commit()

    st.session_state["total"] += 1
    st.session_state["acertos"] += acertou
    st.session_state["vistos"].append(idx)
    st.session_state["ultimo"] = {
        "verdade": verdade, "palpite": palpite, "modelo": modelo,
        "estrela": int(linha["estrela"]),
    }
    st.session_state["revelado"] = True


# ----------------------------------------------------------------------
# Tela 1 — Boas-vindas / nickname
# ----------------------------------------------------------------------
if st.session_state["nick"] is None:
    st.title("🎯 Treine o Algoritmo")
    st.markdown(
        "Você vai ler **avaliações reais de e-commerce** e adivinhar se o "
        "cliente ficou **satisfeito** ou **insatisfeito** — a mesma tarefa "
        "que um modelo de Machine Learning faz.\n\n"
        "No fim, vamos comparar: **quem é mais preciso, você ou a máquina?**"
    )
    nick = st.text_input("Escolha um apelido para o placar:", max_chars=20)
    if st.button("Começar", type="primary", disabled=not nick.strip()):
        st.session_state["nick"] = nick.strip()
        sortear_review()
        st.rerun()
    st.stop()


# ----------------------------------------------------------------------
# Cabeçalho com placar pessoal
# ----------------------------------------------------------------------
col1, col2, col3 = st.columns(3)
acc_humano = (st.session_state["acertos"] / st.session_state["total"]
              if st.session_state["total"] else 0)
col1.metric("Você", f"{acc_humano*100:.0f}%", f"{st.session_state['acertos']}/{st.session_state['total']}")
col2.metric("Modelo", f"{acc_modelo*100:.0f}%")
col3.metric("Jogadas", st.session_state["total"])

st.divider()


# ----------------------------------------------------------------------
# Tela 2 — Jogo
# ----------------------------------------------------------------------
idx = st.session_state["review_atual"]
review = pool.iloc[idx]

st.markdown("#### O que esse cliente achou?")
st.info(f"💬 *{review['texto']}*")

if not st.session_state["revelado"]:
    c1, c2 = st.columns(2)
    if c1.button("👎  Insatisfeito", use_container_width=True):
        registrar(0)
        st.rerun()
    if c2.button("👍  Satisfeito", use_container_width=True):
        registrar(1)
        st.rerun()
else:
    u = st.session_state["ultimo"]
    verdade_txt = "👍 Satisfeito" if u["verdade"] else "👎 Insatisfeito"
    palpite_txt = "👍 Satisfeito" if u["palpite"] else "👎 Insatisfeito"
    modelo_txt = "👍 Satisfeito" if u["modelo"] else "👎 Insatisfeito"

    if u["palpite"] == u["verdade"]:
        st.success(f"✅ Você acertou!  ({u['estrela']} estrelas)")
    else:
        st.error(f"❌ Você errou.  Cliente deu {u['estrela']} estrelas → {verdade_txt}")

    modelo_ok = "✅" if u["modelo"] == u["verdade"] else "❌"
    st.caption(f"O modelo previu: {modelo_txt}  {modelo_ok}")

    if st.button("Próximo review →", type="primary", use_container_width=True):
        sortear_review()
        st.rerun()


# ----------------------------------------------------------------------
# Leaderboard
# ----------------------------------------------------------------------
st.divider()
st.markdown("### 🏆 Placar da turma")

placar = pd.read_sql_query(
    """
    SELECT nick AS Apelido,
           COUNT(*) AS Jogadas,
           ROUND(AVG(acertou) * 100, 1) AS "Acurácia (%)"
    FROM jogadas
    GROUP BY nick
    HAVING Jogadas >= 3
    ORDER BY "Acurácia (%)" DESC
    LIMIT 10
    """,
    con,
)
if len(placar):
    st.dataframe(placar, hide_index=True, use_container_width=True)
    st.caption(f"🤖 Modelo de referência: {acc_modelo*100:.0f}% de acurácia — bata isso!")
else:
    st.caption("Jogue pelo menos 3 reviews para aparecer no placar.")


# ----------------------------------------------------------------------
# Rodapé (admin) — exportar dados coletados para treinar ao vivo
# ----------------------------------------------------------------------
with st.expander("⚙️ Professor — exportar dados coletados"):
    dados = pd.read_sql_query("SELECT * FROM jogadas", con)
    st.write(f"Total de jogadas registradas: **{len(dados)}**")
    st.download_button(
        "📥 Baixar dataset coletado (CSV)",
        dados.to_csv(index=False).encode("utf-8"),
        file_name="jogadas_coletadas.csv",
        mime="text/csv",
    )
