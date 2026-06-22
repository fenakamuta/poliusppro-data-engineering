"""
🎯 Treine o Algoritmo — jogo de classificação de sentimento

Aula 2 · Data Engineering · POLI USP PRO

O aluno lê uma avaliação (texto PT-BR) e adivinha se o cliente ficou satisfeito.
Compara sua acurácia com a de um modelo. Cada jogada é gravada.

ARMAZENAMENTO:
  - Se houver credenciais do Supabase em st.secrets -> grava no Supabase (Postgres,
    permanente, lê de qualquer lugar).
  - Senão -> grava num SQLite local (plays.db). Bom para rodar/testar local.

Rode local:  streamlit run app.py
Deploy:      Streamlit Community Cloud (veja README.md)
"""
import sqlite3
from datetime import datetime, timezone

import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

st.set_page_config(page_title="Treine o Algoritmo", page_icon="🎯", layout="centered")

REVIEWS_CSV = "reviews.csv"
DB_PATH = "plays.db"
COLS = ["nick", "review_idx", "texto", "verdade", "palpite",
        "modelo", "acertou", "modelo_acertou", "ts"]


# ----------------------------------------------------------------------
# Camada de armazenamento (Supabase OU SQLite)
# ----------------------------------------------------------------------
class SupabaseStorage:
    """Grava as jogadas numa tabela 'jogadas' do Supabase (Postgres)."""

    def __init__(self, url, key):
        from supabase import create_client
        self.client = create_client(url, key)

    def insert(self, row: dict):
        self.client.table("jogadas").insert(row).execute()

    def df(self) -> pd.DataFrame:
        res = self.client.table("jogadas").select("*").execute()
        return pd.DataFrame(res.data) if res.data else pd.DataFrame(columns=COLS)


class SQLiteStorage:
    """Fallback local: grava num arquivo SQLite."""

    def __init__(self, path):
        self.con = sqlite3.connect(path, check_same_thread=False)
        self.con.execute(
            "CREATE TABLE IF NOT EXISTS jogadas ("
            "nick TEXT, review_idx INTEGER, texto TEXT, verdade INTEGER, "
            "palpite INTEGER, modelo INTEGER, acertou INTEGER, "
            "modelo_acertou INTEGER, ts TEXT)"
        )
        self.con.commit()

    def insert(self, row: dict):
        self.con.execute(
            f"INSERT INTO jogadas ({','.join(COLS)}) VALUES ({','.join(['?']*len(COLS))})",
            tuple(row[c] for c in COLS),
        )
        self.con.commit()

    def df(self) -> pd.DataFrame:
        return pd.read_sql_query("SELECT * FROM jogadas", self.con)


@st.cache_resource
def get_storage():
    """Escolhe o backend: Supabase se houver segredos, senão SQLite."""
    try:
        if "supabase" in st.secrets:
            sb = st.secrets["supabase"]
            return SupabaseStorage(sb["url"], sb["key"]), "Supabase"
    except Exception as e:
        st.warning(f"Supabase indisponível ({e}); usando armazenamento local.")
    return SQLiteStorage(DB_PATH), "SQLite local"


# ----------------------------------------------------------------------
# Carrega dados + treina o modelo (uma vez, cacheado)
# ----------------------------------------------------------------------
@st.cache_resource
def carregar_e_treinar():
    df = pd.read_csv(REVIEWS_CSV)
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
    acc_modelo = (pool["modelo_pred"] == pool["positivo"]).mean()
    return pool, acc_modelo


pool, acc_modelo = carregar_e_treinar()
storage, backend = get_storage()


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
    candidatos = [i for i in range(len(pool)) if i not in st.session_state["vistos"]]
    if not candidatos:
        st.session_state["vistos"] = []
        candidatos = list(range(len(pool)))
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

    storage.insert({
        "nick": st.session_state["nick"], "review_idx": int(idx),
        "texto": linha["texto"], "verdade": verdade, "palpite": palpite,
        "modelo": modelo, "acertou": acertou, "modelo_acertou": modelo_acertou,
        "ts": datetime.now(timezone.utc).isoformat(),
    })

    st.session_state["total"] += 1
    st.session_state["acertos"] += acertou
    st.session_state["vistos"].append(idx)
    st.session_state["ultimo"] = {
        "verdade": verdade, "palpite": palpite, "modelo": modelo,
        "estrela": int(linha["estrela"]),
    }
    st.session_state["revelado"] = True


# ----------------------------------------------------------------------
# Tela 1 — Boas-vindas
# ----------------------------------------------------------------------
if st.session_state["nick"] is None:
    st.title("🎯 Treine o Algoritmo")
    st.markdown(
        "Você vai ler **avaliações reais de e-commerce** e adivinhar se o "
        "cliente ficou **satisfeito** ou **insatisfeito** — a mesma tarefa "
        "que um modelo de Machine Learning faz.\n\n"
        "No fim, comparamos: **quem é mais preciso, você ou a máquina?**"
    )
    nick = st.text_input("Escolha um apelido para o placar:", max_chars=20)
    if st.button("Começar", type="primary", disabled=not nick.strip()):
        st.session_state["nick"] = nick.strip()
        sortear_review()
        st.rerun()
    st.caption(f"Armazenamento: {backend}")
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
        registrar(0); st.rerun()
    if c2.button("👍  Satisfeito", use_container_width=True):
        registrar(1); st.rerun()
else:
    u = st.session_state["ultimo"]
    verdade_txt = "👍 Satisfeito" if u["verdade"] else "👎 Insatisfeito"
    modelo_txt = "👍 Satisfeito" if u["modelo"] else "👎 Insatisfeito"
    if u["palpite"] == u["verdade"]:
        st.success(f"✅ Você acertou!  ({u['estrela']} estrelas)")
    else:
        st.error(f"❌ Você errou.  Cliente deu {u['estrela']} estrelas → {verdade_txt}")
    modelo_ok = "✅" if u["modelo"] == u["verdade"] else "❌"
    st.caption(f"O modelo previu: {modelo_txt}  {modelo_ok}")
    if st.button("Próximo review →", type="primary", use_container_width=True):
        sortear_review(); st.rerun()


# ----------------------------------------------------------------------
# Leaderboard
# ----------------------------------------------------------------------
st.divider()
st.markdown("### 🏆 Placar da turma")
dados = storage.df()
if len(dados):
    placar = (dados.groupby("nick")
              .agg(Jogadas=("acertou", "size"), Acuracia=("acertou", "mean"))
              .reset_index())
    placar = placar[placar["Jogadas"] >= 3].copy()
    placar["Acuracia"] = (placar["Acuracia"] * 100).round(1)
    placar = placar.sort_values("Acuracia", ascending=False).head(10)
    placar.columns = ["Apelido", "Jogadas", "Acurácia (%)"]
    st.dataframe(placar, hide_index=True, use_container_width=True)
    st.caption(f"🤖 Modelo de referência: {acc_modelo*100:.0f}% — bata isso!")
else:
    st.caption("Jogue pelo menos 3 reviews para aparecer no placar.")


# ----------------------------------------------------------------------
# Rodapé (professor)
# ----------------------------------------------------------------------
with st.expander("⚙️ Professor — exportar dados coletados"):
    todos = storage.df()
    st.write(f"Total de jogadas: **{len(todos)}**  ·  armazenamento: **{backend}**")
    if len(todos):
        st.download_button(
            "📥 Baixar dataset coletado (CSV)",
            todos.to_csv(index=False).encode("utf-8"),
            file_name="jogadas_coletadas.csv", mime="text/csv",
        )
