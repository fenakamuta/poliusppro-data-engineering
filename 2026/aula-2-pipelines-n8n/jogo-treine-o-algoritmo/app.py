"""
🎯 Treine o Algoritmo — jogo de classificação de satisfação

Aula 2 · Data Engineering · POLI USP PRO

O aluno vê uma avaliação e adivinha se o cliente ficou satisfeito.
Dois tipos de rodada:
  - COM comentário  -> a pessoa lê o texto
  - SEM comentário  -> a pessoa julga só pelos dados do pedido (tabela)

O modelo é COMBINADO (texto + tabela), então também funciona nos dois casos:
quando não há texto, ele se apoia nos dados (preço, prazo, atraso...).

ARMAZENAMENTO: Supabase (se houver credenciais em st.secrets) ou SQLite local.

Rode local:  streamlit run app.py
"""
import sqlite3
from datetime import datetime, timezone

import pandas as pd
import streamlit as st
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

st.set_page_config(page_title="Você vs a Máquina", page_icon="🎯", layout="centered")

REVIEWS_CSV = "reviews.csv"
DB_PATH = "plays.db"
COLS = ["nick", "review_idx", "texto", "verdade", "palpite",
        "modelo", "acertou", "modelo_acertou", "ts"]
NUM = ["preco", "frete", "dias_entrega", "dias_estimado", "atrasou"]
CAT = ["categoria"]


# ----------------------------------------------------------------------
# Armazenamento (Supabase OU SQLite)
# ----------------------------------------------------------------------
class SupabaseStorage:
    def __init__(self, url, key):
        from supabase import create_client
        self.client = create_client(url, key)

    def insert(self, row: dict):
        self.client.table("jogadas").insert(row).execute()

    def df(self) -> pd.DataFrame:
        res = self.client.table("jogadas").select("*").execute()
        return pd.DataFrame(res.data) if res.data else pd.DataFrame(columns=COLS)


class SQLiteStorage:
    def __init__(self, path):
        self.con = sqlite3.connect(path, check_same_thread=False)
        self.con.execute(
            "CREATE TABLE IF NOT EXISTS jogadas ("
            "nick TEXT, review_idx INTEGER, texto TEXT, verdade INTEGER, "
            "palpite INTEGER, modelo INTEGER, acertou INTEGER, "
            "modelo_acertou INTEGER, ts TEXT)")
        self.con.commit()

    def insert(self, row: dict):
        self.con.execute(
            f"INSERT INTO jogadas ({','.join(COLS)}) VALUES ({','.join(['?']*len(COLS))})",
            tuple(row[c] for c in COLS))
        self.con.commit()

    def df(self) -> pd.DataFrame:
        return pd.read_sql_query("SELECT * FROM jogadas", self.con)


@st.cache_resource
def get_storage():
    try:
        if "supabase" in st.secrets:
            sb = st.secrets["supabase"]
            return SupabaseStorage(sb["url"], sb["key"]), "Supabase"
    except Exception as e:
        st.warning(f"Supabase indisponível ({e}); usando armazenamento local.")
    return SQLiteStorage(DB_PATH), "SQLite local"


# ----------------------------------------------------------------------
# Carrega dados + treina o modelo COMBINADO (uma vez)
# ----------------------------------------------------------------------
@st.cache_resource
def carregar_e_treinar():
    df = pd.read_csv(REVIEWS_CSV)
    df["texto"] = df["texto"].fillna("")
    df["tem_texto"] = (df["texto"].str.len() > 0).astype(int)

    treino, pool = train_test_split(
        df, test_size=0.4, random_state=42, stratify=df["positivo"])

    pre = ColumnTransformer([
        ("texto", TfidfVectorizer(max_features=4000, ngram_range=(1, 2), min_df=3), "texto"),
        ("num", Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler())]), NUM),
        ("cat", OneHotEncoder(handle_unknown="ignore", min_frequency=20), CAT),
    ])
    modelo = Pipeline([("f", pre), ("clf", LogisticRegression(max_iter=1000, class_weight="balanced"))])
    modelo.fit(treino, treino["positivo"])

    pool = pool.reset_index(drop=True).copy()
    pool["modelo_pred"] = modelo.predict(pool)
    acc_modelo = (pool["modelo_pred"] == pool["positivo"]).mean()
    return pool, acc_modelo


pool, acc_modelo = carregar_e_treinar()
storage, backend = get_storage()


# ----------------------------------------------------------------------
# Estado da sessão
# ----------------------------------------------------------------------
def init_state():
    for k, v in {"nick": None, "review_atual": None, "revelado": False,
                 "vistos": [], "acertos": 0, "total": 0}.items():
        st.session_state.setdefault(k, v)


init_state()


def sortear_review():
    cand = [i for i in range(len(pool)) if i not in st.session_state["vistos"]]
    if not cand:
        st.session_state["vistos"] = []; cand = list(range(len(pool)))
    idx = cand[(hash(st.session_state["nick"]) + st.session_state["total"]) % len(cand)]
    st.session_state["review_atual"] = idx
    st.session_state["revelado"] = False


def registrar(palpite: int):
    idx = st.session_state["review_atual"]
    linha = pool.iloc[idx]
    verdade = int(linha["positivo"]); modelo = int(linha["modelo_pred"])
    storage.insert({
        "nick": st.session_state["nick"], "review_idx": int(idx),
        "texto": str(linha["texto"])[:200], "verdade": verdade, "palpite": palpite,
        "modelo": modelo, "acertou": int(palpite == verdade),
        "modelo_acertou": int(modelo == verdade),
        "ts": datetime.now(timezone.utc).isoformat(),
    })
    st.session_state["total"] += 1
    st.session_state["acertos"] += int(palpite == verdade)
    st.session_state["vistos"].append(idx)
    st.session_state["ultimo"] = {"verdade": verdade, "palpite": palpite,
                                  "modelo": modelo, "estrela": int(linha["estrela"])}
    st.session_state["revelado"] = True


# ----------------------------------------------------------------------
# Tela 1 — Boas-vindas
# ----------------------------------------------------------------------
if st.session_state["nick"] is None:
    st.title("🎯 Você vs a Máquina")
    st.markdown(
        "Você vai ver avaliações de e-commerce e adivinhar se o cliente ficou "
        "**satisfeito** ou **insatisfeito**.\n\n"
        "Em algumas rodadas você lê o **comentário**. Em outras, não há comentário "
        "e você decide só pelos **dados do pedido** (preço, prazo, atraso) — "
        "exatamente como o modelo faz.\n\n"
        "No fim: **quem acerta mais, você ou a máquina?**")
    nick = st.text_input("Seu apelido para o placar:", max_chars=20)
    if st.button("Começar", type="primary", disabled=not nick.strip()):
        st.session_state["nick"] = nick.strip(); sortear_review(); st.rerun()
    st.caption(f"Armazenamento: {backend}")
    st.stop()


# ----------------------------------------------------------------------
# Cabeçalho
# ----------------------------------------------------------------------
c1, c2, c3 = st.columns(3)
acc_h = st.session_state["acertos"] / st.session_state["total"] if st.session_state["total"] else 0
c1.metric("Você", f"{acc_h*100:.0f}%", f"{st.session_state['acertos']}/{st.session_state['total']}")
c2.metric("Modelo", f"{acc_modelo*100:.0f}%")
c3.metric("Jogadas", st.session_state["total"])
st.divider()


# ----------------------------------------------------------------------
# Tela 2 — Jogo (mostra texto OU contexto)
# ----------------------------------------------------------------------
idx = st.session_state["review_atual"]
review = pool.iloc[idx]
tem_texto = len(str(review["texto"])) > 0

st.markdown("#### Esse cliente ficou satisfeito?")

if tem_texto:
    st.info(f"💬 *{review['texto']}*")
else:
    atraso = int(review["dias_entrega"] - review["dias_estimado"])
    atraso_txt = (f"⚠️ {atraso} dias de ATRASO" if atraso > 0
                  else f"✅ {abs(atraso)} dias adiantado" if atraso < 0 else "no prazo")
    st.warning("📊 **Sem comentário escrito.** Decida pelos dados do pedido:")
    d1, d2, d3 = st.columns(3)
    d1.metric("Categoria", str(review["categoria"]))
    d2.metric("Preço", f"R$ {review['preco']:.0f}")
    d3.metric("Frete", f"R$ {review['frete']:.0f}")
    e1, e2 = st.columns(2)
    e1.metric("Dias até entregar", int(review["dias_entrega"]))
    e2.metric("Prazo prometido", int(review["dias_estimado"]))
    st.caption(f"Entrega: {atraso_txt}")

if not st.session_state["revelado"]:
    b1, b2 = st.columns(2)
    if b1.button("👎  Insatisfeito", use_container_width=True):
        registrar(0); st.rerun()
    if b2.button("👍  Satisfeito", use_container_width=True):
        registrar(1); st.rerun()
else:
    u = st.session_state["ultimo"]
    v_txt = "👍 Satisfeito" if u["verdade"] else "👎 Insatisfeito"
    m_txt = "👍 Satisfeito" if u["modelo"] else "👎 Insatisfeito"
    if u["palpite"] == u["verdade"]:
        st.success(f"✅ Você acertou!  ({u['estrela']} estrelas)")
    else:
        st.error(f"❌ Você errou.  Cliente deu {u['estrela']} estrelas → {v_txt}")
    st.caption(f"O modelo previu: {m_txt}  {'✅' if u['modelo']==u['verdade'] else '❌'}")
    if st.button("Próximo →", type="primary", use_container_width=True):
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
    st.caption(f"🤖 Modelo: {acc_modelo*100:.0f}% — bata isso!")
else:
    st.caption("Jogue pelo menos 3 rodadas para aparecer no placar.")


# ----------------------------------------------------------------------
# Professor
# ----------------------------------------------------------------------
with st.expander("⚙️ Professor — exportar dados coletados"):
    todos = storage.df()
    st.write(f"Total de jogadas: **{len(todos)}**  ·  armazenamento: **{backend}**")
    if len(todos):
        st.download_button("📥 Baixar dataset coletado (CSV)",
                           todos.to_csv(index=False).encode("utf-8"),
                           file_name="jogadas_coletadas.csv", mime="text/csv")
