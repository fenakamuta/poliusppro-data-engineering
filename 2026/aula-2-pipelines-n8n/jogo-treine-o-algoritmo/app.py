"""
🎯 Você vs a Máquina — jogo de classificação de satisfação

Aula 2 · Data Engineering · POLI USP PRO

O aluno vê uma avaliação e adivinha se o cliente ficou satisfeito.
- COM comentário  -> lê o texto (+ resumo dos dados)
- SEM comentário  -> decide só pelos dados do pedido (atraso, preço, etc.)

Modelo COMBINADO (texto + tabela): funciona nos dois casos.
Armazenamento: Supabase (st.secrets) ou SQLite local.
"""
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

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

# Caminhos relativos AO ARQUIVO (no Streamlit Cloud o CWD é a raiz do repo, não esta pasta)
BASE_DIR = Path(__file__).parent
REVIEWS_CSV = str(BASE_DIR / "reviews.csv")
DB_PATH = str(BASE_DIR / "plays.db")
COLS = ["nick", "review_idx", "texto", "verdade", "palpite",
        "modelo", "acertou", "modelo_acertou", "ts"]
NUM = ["preco", "frete", "dias_entrega", "dias_estimado", "atrasou", "parcelas", "fotos"]
CAT = ["categoria", "pagamento", "estado"]

# ----------------------------------------------------------------------
# Design tokens
# ----------------------------------------------------------------------
P = {
    "bg": "#0E1117", "card": "#1A1D27", "card_alt": "#222633", "border": "#2B2F3D",
    "txt": "#E6E8EE", "dim": "#8B90A0",
    "verde": "#34D399", "verde_bg": "rgba(52,211,153,0.12)",
    "verm": "#F87171", "verm_bg": "rgba(248,113,113,0.13)",
    "ambar": "#FBBF24", "ambar_bg": "rgba(251,191,36,0.12)",
    "azul": "#60A5FA", "azul_bg": "rgba(96,165,250,0.10)",
}

CAT_PT = {
    "cama_mesa_banho": "Cama, Mesa e Banho", "beleza_saude": "Beleza e Saúde",
    "esporte_lazer": "Esporte e Lazer", "moveis_decoracao": "Móveis e Decoração",
    "informatica_acessorios": "Informática e Acessórios", "relogios_presentes": "Relógios e Presentes",
    "utilidades_domesticas": "Utilidades Domésticas", "telefonia": "Telefonia",
    "automotivo": "Automotivo", "cool_stuff": "Cool Stuff", "brinquedos": "Brinquedos",
    "ferramentas_jardim": "Ferramentas e Jardim", "perfumaria": "Perfumaria",
    "bebes": "Bebês", "eletronicos": "Eletrônicos", "papelaria": "Papelaria",
    "fashion_bolsas_e_acessorios": "Moda e Acessórios", "pet_shop": "Pet Shop",
    "moveis_escritorio": "Móveis de Escritório", "consoles_games": "Games e Consoles",
}
PGTO_PT = {"credit_card": "Cartão", "boleto": "Boleto", "voucher": "Voucher",
           "debit_card": "Débito", "na": "—"}


def cat_pt(raw):
    raw = str(raw)
    return CAT_PT.get(raw, raw.replace("_", " ").title())


def pgto_pt(raw, parcelas):
    nome = PGTO_PT.get(str(raw), str(raw).title())
    try:
        p = int(parcelas)
    except Exception:
        p = 1
    return f"{nome} · {p}x" if p > 1 else nome


# ----------------------------------------------------------------------
# Componentes visuais (HTML)
# ----------------------------------------------------------------------
def css_global():
    st.markdown(f"""<style>
      footer {{visibility:hidden;}}  /* esconde só o rodapé; mantém o header (botão Deploy) */
      .block-container {{padding:1rem 1rem 3rem !important; max-width:520px;}}
      .stButton>button {{border-radius:14px; font-weight:700; font-size:1.05rem;
         padding:0.7rem 1rem; min-height:54px;}}
      .stApp {{background:
         radial-gradient(circle at 20% 0%, rgba(96,165,250,0.06), transparent 40%),
         {P['bg']};}}
      div[data-testid="column"]:nth-of-type(1) .stButton>button {{
         background:{P['verm_bg']}; color:{P['verm']}; border:1.5px solid {P['verm']}66;}}
      div[data-testid="column"]:nth-of-type(2) .stButton>button {{
         background:{P['verde_bg']}; color:{P['verde']}; border:1.5px solid {P['verde']}66;}}
    </style>""", unsafe_allow_html=True)


def card_entrega(atraso, prazo, real):
    if atraso > 0:
        cor, bg, icone, tit = P["verm"], P["verm_bg"], "⏱️", "ENTREGA ATRASADA"
        dest = f"{atraso} {'dia' if atraso==1 else 'dias'} de atraso"
    elif atraso < 0:
        cor, bg, icone, tit = P["verde"], P["verde_bg"], "🚀", "CHEGOU ANTES"
        dest = f"{abs(atraso)} {'dia' if abs(atraso)==1 else 'dias'} adiantado"
    else:
        cor, bg, icone, tit = P["ambar"], P["ambar_bg"], "🎯", "ENTREGA NO PRAZO"
        dest = "Em cima do prazo"
    return f"""<div style="background:{bg};border:1px solid {cor}55;border-left:5px solid {cor};
      border-radius:18px;padding:20px;margin:8px 0 14px;text-align:center;box-shadow:0 4px 24px {cor}22;">
      <div style="font-size:0.76rem;letter-spacing:0.14em;color:{P['dim']};font-weight:600;">{icone}&nbsp; {tit}</div>
      <div style="font-size:2.3rem;line-height:1.1;font-weight:800;color:{cor};margin:6px 0 2px;">{dest}</div>
      <div style="font-size:0.9rem;color:{P['dim']};">prometido <b style="color:{P['txt']}">{prazo}d</b>
      &nbsp;·&nbsp; levou <b style="color:{P['txt']}">{real}d</b></div></div>"""


def evidencia(icone, rotulo, valor, largura="100%"):
    return f"""<div style="background:{P['card']};border:1px solid {P['border']};border-radius:12px;
      padding:11px 14px;margin-bottom:8px;width:{largura};box-sizing:border-box;">
      <div style="font-size:0.7rem;letter-spacing:0.08em;color:{P['dim']};text-transform:uppercase;margin-bottom:3px;">{icone} {rotulo}</div>
      <div style="font-size:1.02rem;color:{P['txt']};font-weight:600;white-space:normal;line-height:1.3;word-break:break-word;">{valor}</div></div>"""


def par(c1, c2):
    return f'<div style="display:flex;gap:8px;margin-bottom:8px;">{c1}{c2}</div>'


def chip(txt):
    return f"""<span style="display:inline-block;background:{P['card_alt']};border:1px solid {P['border']};
      border-radius:999px;padding:4px 12px;font-size:0.8rem;color:{P['dim']};margin:2px 4px 2px 0;">{txt}</span>"""


def balao(texto):
    return f"""<div style="margin:8px 0 12px;">
      <div style="font-size:0.74rem;color:{P['dim']};margin-bottom:6px;letter-spacing:0.06em;">💬 O CLIENTE ESCREVEU</div>
      <div style="background:{P['azul_bg']};border:1px solid {P['azul']}40;border-left:4px solid {P['azul']};
      border-radius:4px 16px 16px 16px;padding:14px 16px;color:{P['txt']};font-size:1.05rem;line-height:1.5;font-style:italic;">"{texto}"</div></div>"""


def tira_resumo(atraso, categoria, pagamento, parcelas, preco, frete):
    cor = P["verm"] if atraso > 0 else (P["verde"] if atraso < 0 else P["ambar"])
    sinal = f"{atraso}d atraso" if atraso > 0 else (f"{abs(atraso)}d adiantado" if atraso < 0 else "no prazo")
    return f"""<div style="display:flex;gap:6px;overflow-x:auto;padding-bottom:4px;flex-wrap:wrap;">
      {chip(f'<b style="color:{cor}">⏱️ {sinal}</b>')}{chip(f'🏷️ {cat_pt(categoria)}')}
      {chip(f'💳 {pgto_pt(pagamento, parcelas)}')}{chip(f'📦 R$ {preco:.0f} + frete R$ {frete:.0f}')}</div>"""


# ----------------------------------------------------------------------
# Armazenamento
# ----------------------------------------------------------------------
class SupabaseStorage:
    def __init__(self, url, key):
        from supabase import create_client
        self.client = create_client(url, key)

    def insert(self, row):
        self.client.table("jogadas").insert(row).execute()

    def df(self):
        r = self.client.table("jogadas").select("*").execute()
        return pd.DataFrame(r.data) if r.data else pd.DataFrame(columns=COLS)


class SQLiteStorage:
    def __init__(self, path):
        # timeout + WAL deixam o SQLite aguentar acesso simultâneo bem melhor:
        # WAL permite leitores e escritor ao mesmo tempo; busy_timeout espera em vez de dar erro.
        self.con = sqlite3.connect(path, check_same_thread=False, timeout=15)
        self.con.execute("PRAGMA journal_mode=WAL")
        self.con.execute("PRAGMA busy_timeout=8000")
        self.con.execute("PRAGMA synchronous=NORMAL")
        self.con.execute("CREATE TABLE IF NOT EXISTS jogadas (nick TEXT,review_idx INTEGER,texto TEXT,"
                         "verdade INTEGER,palpite INTEGER,modelo INTEGER,acertou INTEGER,modelo_acertou INTEGER,ts TEXT)")
        self.con.commit()

    def insert(self, row):
        self.con.execute(f"INSERT INTO jogadas ({','.join(COLS)}) VALUES ({','.join(['?']*len(COLS))})",
                         tuple(row[c] for c in COLS)); self.con.commit()

    def df(self):
        return pd.read_sql_query("SELECT * FROM jogadas", self.con)


@st.cache_resource
def get_storage():
    # Tenta Supabase em silêncio; se não houver secrets, cai no SQLite local sem alarde.
    try:
        if "supabase" in st.secrets:
            sb = st.secrets["supabase"]
            return SupabaseStorage(sb["url"], sb["key"]), "Supabase"
    except Exception:
        pass
    return SQLiteStorage(DB_PATH), "SQLite local"


@st.cache_resource
def carregar_e_treinar():
    df = pd.read_csv(REVIEWS_CSV)
    df["texto"] = df["texto"].fillna("")
    treino, pool = train_test_split(df, test_size=0.4, random_state=42, stratify=df["positivo"])
    pre = ColumnTransformer([
        ("texto", TfidfVectorizer(max_features=4000, ngram_range=(1, 2), min_df=3), "texto"),
        ("num", Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler())]), NUM),
        ("cat", OneHotEncoder(handle_unknown="ignore", min_frequency=20), CAT)])
    modelo = Pipeline([("f", pre), ("clf", LogisticRegression(max_iter=1000, class_weight="balanced"))])
    modelo.fit(treino, treino["positivo"])
    pool = pool.reset_index(drop=True).copy()
    pool["modelo_pred"] = modelo.predict(pool)
    return pool, (pool["modelo_pred"] == pool["positivo"]).mean()


@st.cache_data(ttl=4, show_spinner=False)
def ler_jogadas(_storage):
    """Lê o placar no máximo 1x a cada 4s (em vez de a cada clique de qualquer aluno).
    Reduz muito a pressão no banco quando a turma toda está jogando junta."""
    return _storage.df()


css_global()
pool, acc_modelo = carregar_e_treinar()
storage, backend = get_storage()


# ----------------------------------------------------------------------
# Página SECRETA do professor — acesse com  ?prof=poli2026  na URL
# ----------------------------------------------------------------------
PROF_TOKEN = "poli2026"
if st.query_params.get("prof") == PROF_TOKEN:
    st.title("📊 Painel do Professor")
    if st.button("🔄 Atualizar dados", type="primary"):
        st.rerun()

    dados = storage.df()
    if len(dados) == 0:
        st.info("Ainda não há jogadas registradas.")
        st.caption(f"Armazenamento: {backend}")
        st.stop()

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Jogadas", len(dados))
    m2.metric("Alunos", dados["nick"].nunique())
    m3.metric("Acurácia turma", f"{dados['acertou'].mean()*100:.0f}%")
    m4.metric("Acurácia modelo", f"{acc_modelo*100:.0f}%")

    st.subheader("🏆 Placar")
    placar = (dados.groupby("nick")
              .agg(Jogadas=("acertou", "size"), Acu=("acertou", "mean"))
              .reset_index())
    placar["Acu"] = (placar["Acu"] * 100).round(1)
    placar = placar.sort_values("Acu", ascending=False)
    placar.columns = ["Apelido", "Jogadas", "Acurácia (%)"]
    st.dataframe(placar, hide_index=True, use_container_width=True)

    st.subheader("📋 Todas as jogadas")
    st.dataframe(dados, use_container_width=True, height=320)

    st.download_button("📥 Baixar CSV completo",
                       dados.to_csv(index=False).encode("utf-8"),
                       file_name="jogadas_coletadas.csv", mime="text/csv", type="primary")
    st.caption(f"Armazenamento: {backend}  ·  atualizado a cada clique em Atualizar")
    st.stop()


def init_state():
    for k, v in {"nick": None, "review_atual": None, "revelado": False,
                 "vistos": [], "acertos": 0, "total": 0}.items():
        st.session_state.setdefault(k, v)


init_state()


def sortear():
    cand = [i for i in range(len(pool)) if i not in st.session_state["vistos"]]
    if not cand:
        st.session_state["vistos"] = []; cand = list(range(len(pool)))
    st.session_state["review_atual"] = cand[(hash(st.session_state["nick"]) + st.session_state["total"]) % len(cand)]
    st.session_state["revelado"] = False


def registrar(palpite):
    idx = st.session_state["review_atual"]; linha = pool.iloc[idx]
    verdade = int(linha["positivo"]); modelo = int(linha["modelo_pred"])
    storage.insert({"nick": st.session_state["nick"], "review_idx": int(idx),
        "texto": str(linha["texto"])[:200], "verdade": verdade, "palpite": palpite, "modelo": modelo,
        "acertou": int(palpite == verdade), "modelo_acertou": int(modelo == verdade),
        "ts": datetime.now(timezone.utc).isoformat()})
    st.session_state["total"] += 1; st.session_state["acertos"] += int(palpite == verdade)
    st.session_state["vistos"].append(idx)
    st.session_state["ultimo"] = {"verdade": verdade, "palpite": palpite, "modelo": modelo, "estrela": int(linha["estrela"])}
    st.session_state["revelado"] = True


# ----------------------------------------------------------------------
# Tela 1 — Boas-vindas
# ----------------------------------------------------------------------
if st.session_state["nick"] is None:
    st.title("🎯 Você vs a Máquina")
    st.markdown("Veja avaliações de e-commerce e adivinhe se o cliente ficou **satisfeito**. "
                "Às vezes você lê o comentário; às vezes decide só pelos **dados do pedido** — "
                "como o modelo faz. No fim: **quem acerta mais, você ou a máquina?**")
    nick = st.text_input("Seu apelido para o placar:", max_chars=20)
    if st.button("Começar", type="primary", disabled=not nick.strip()):
        st.session_state["nick"] = nick.strip(); sortear(); st.rerun()
    st.caption(f"Armazenamento: {backend}")
    st.stop()


# ----------------------------------------------------------------------
# Cabeçalho
# ----------------------------------------------------------------------
c1, c2, c3 = st.columns(3)
acc_h = st.session_state["acertos"] / st.session_state["total"] if st.session_state["total"] else 0
c1.metric("Você", f"{acc_h*100:.0f}%", f"{st.session_state['acertos']}/{st.session_state['total']}")
c2.metric("Modelo", f"{acc_modelo*100:.0f}%")
c3.metric("Rodadas", st.session_state["total"])
st.divider()


# ----------------------------------------------------------------------
# Tela 2 — Jogo
# ----------------------------------------------------------------------
idx = st.session_state["review_atual"]
r = pool.iloc[idx]
tem_texto = len(str(r["texto"])) > 0
atraso = int(r["dias_entrega"] - r["dias_estimado"])

st.markdown("#### Esse cliente ficou satisfeito?")

if tem_texto:
    # Texto é o herói; dados num resumo compacto
    st.markdown(balao(r["texto"]), unsafe_allow_html=True)
    st.markdown(tira_resumo(atraso, r["categoria"], r["pagamento"], r["parcelas"], r["preco"], r["frete"]),
                unsafe_allow_html=True)
else:
    # Sem texto: o atraso é o herói + evidências
    st.markdown(f'<div style="font-size:0.82rem;color:{P["dim"]};margin-bottom:4px;">📊 Sem comentário — julgue pelos dados</div>',
                unsafe_allow_html=True)
    st.markdown(card_entrega(atraso, int(r["dias_estimado"]), int(r["dias_entrega"])), unsafe_allow_html=True)
    st.markdown(evidencia("🏷️", "Categoria", cat_pt(r["categoria"])), unsafe_allow_html=True)
    preco_val = f"R$ {r['preco']:.0f} <span style='color:{P['dim']};font-weight:400'>+ frete R$ {r['frete']:.0f}</span>"
    st.markdown(par(evidencia("📦", "Produto", preco_val, "50%"),
                    evidencia("💳", "Pagamento", pgto_pt(r["pagamento"], r["parcelas"]), "50%")),
                unsafe_allow_html=True)
    chip_estado = chip("📍 " + str(r["estado"]))
    chip_fotos = chip("🖼️ " + str(int(r["fotos"])) + " fotos")
    st.markdown(f'<div style="margin-top:2px">{chip_estado}{chip_fotos}</div>', unsafe_allow_html=True)

st.write("")

if not st.session_state["revelado"]:
    b1, b2 = st.columns(2)
    if b1.button("😠 Insatisfeito", use_container_width=True):
        registrar(0); st.rerun()
    if b2.button("😊 Satisfeito", use_container_width=True):
        registrar(1); st.rerun()
else:
    u = st.session_state["ultimo"]
    v_txt = "satisfeito 👍" if u["verdade"] else "insatisfeito 👎"
    if u["palpite"] == u["verdade"]:
        st.success(f"✅ Você acertou!  (cliente deu {u['estrela']} estrelas)")
    else:
        st.error(f"❌ Você errou.  Cliente deu {u['estrela']} estrelas → {v_txt}")
    if u["modelo"] == u["verdade"] and u["palpite"] != u["verdade"]:
        st.caption("🤖 A máquina acertou essa. 1 ponto pra ela.")
    elif u["modelo"] != u["verdade"] and u["palpite"] == u["verdade"]:
        st.caption("🏆 Você acertou e a máquina errou!")
    else:
        st.caption(f"🤖 A máquina previu: {'satisfeito' if u['modelo'] else 'insatisfeito'} ({'✅' if u['modelo']==u['verdade'] else '❌'})")
    if st.button("Próximo →", type="primary", use_container_width=True):
        sortear(); st.rerun()


# ----------------------------------------------------------------------
# Leaderboard
# ----------------------------------------------------------------------
st.divider()
st.markdown("### 🏆 Placar da turma")
dados = ler_jogadas(storage)
if len(dados):
    placar = (dados.groupby("nick").agg(Jogadas=("acertou", "size"), Acuracia=("acertou", "mean")).reset_index())
    placar = placar[placar["Jogadas"] >= 3].copy()
    placar["Acuracia"] = (placar["Acuracia"] * 100).round(1)
    placar = placar.sort_values("Acuracia", ascending=False).head(10)
    placar.columns = ["Apelido", "Jogadas", "Acurácia (%)"]
    st.dataframe(placar, hide_index=True, use_container_width=True)
    st.caption(f"🤖 Modelo: {acc_modelo*100:.0f}% — bata isso!")
else:
    st.caption("Jogue pelo menos 3 rodadas para aparecer no placar.")
