# -*- coding: utf-8 -*-
"""Diagramas estilo Excalidraw (traço de mão) para o deck da Aula 3.

Gera PNGs em ./diagramas/ com matplotlib em modo xkcd + fonte Patrick Hand.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Polygon
import pathlib

FONT = pathlib.Path(__file__).parent / "fonts/PatrickHand.ttf"
if not FONT.exists():
    import urllib.request
    FONT.parent.mkdir(exist_ok=True)
    urllib.request.urlretrieve(
        "https://github.com/google/fonts/raw/main/ofl/patrickhand/PatrickHand-Regular.ttf",
        FONT)
font_manager.fontManager.addfont(str(FONT))
FAM = font_manager.FontProperties(fname=str(FONT)).get_name()

OUT = pathlib.Path(__file__).parent / "assets-slides"
OUT.mkdir(exist_ok=True)

# paleta das trilhas do deck
OLIST = "#10834A"; DOCKER = "#0C8599"; BANCO = "#1971C2"
N8N = "#D6336C"; DASH = "#7048E8"; CINZA = "#495057"; ERRO = "#E03131"

plt.xkcd(scale=1.1, length=120, randomness=1.6)
plt.rcParams["font.family"] = FAM


def fig_ax(w, h):
    f, ax = plt.subplots(figsize=(w, h), dpi=200)
    ax.set_xlim(0, 100); ax.set_ylim(0, 100 * h / w)
    ax.axis("off")
    return f, ax


def box(ax, x, y, w, h, label, cor, sub=None, lw=2.2, fs=15, subfs=10.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.6,rounding_size=1.6",
                                edgecolor=cor, facecolor=cor + "14", linewidth=lw))
    cy = y + h / 2 + (2.2 if sub else 0)
    ax.text(x + w / 2, cy, label, ha="center", va="center", fontsize=fs, color=cor)
    if sub:
        ax.text(x + w / 2, y + h / 2 - 3.4, sub, ha="center", va="center",
                fontsize=subfs, color=CINZA)


def seta(ax, x1, y1, x2, y2, label=None, cor=CINZA, fs=11.5, dy=2.6, ls="-"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=22, linewidth=2.2, color=cor,
                                 linestyle=ls, shrinkA=2, shrinkB=2))
    if label:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + dy, label, ha="center",
                fontsize=fs, color=cor)


def boneco(ax, x, y, cor=CINZA, escala=1.0, label=None):
    ax.add_patch(Circle((x, y + 6 * escala), 2.1 * escala, fill=False,
                        edgecolor=cor, linewidth=2))
    ax.plot([x, x], [y + 3.9 * escala, y - 0.5 * escala], color=cor, lw=2)
    ax.plot([x - 2.2 * escala, x, x + 2.2 * escala],
            [y + 1.2 * escala, y + 3 * escala, y + 1.2 * escala], color=cor, lw=2)
    ax.plot([x - 1.8 * escala, x, x + 1.8 * escala],
            [y - 3.6 * escala, y - 0.5 * escala, y - 3.6 * escala], color=cor, lw=2)
    if label:
        ax.text(x, y - 6.5 * escala, label, ha="center", fontsize=10.5, color=cor)


def cilindro(ax, x, y, w, h, cor, label, sub=None):
    from matplotlib.patches import Ellipse, Rectangle
    eh = h * 0.28
    ax.add_patch(Rectangle((x, y), w, h - eh / 2, edgecolor=cor,
                           facecolor=cor + "14", linewidth=2.2))
    ax.add_patch(Ellipse((x + w / 2, y + h - eh / 2), w, eh, edgecolor=cor,
                         facecolor=cor + "22", linewidth=2.2))
    ax.add_patch(Ellipse((x + w / 2, y), w, eh, edgecolor=cor,
                         facecolor="white", linewidth=2.2))
    cy = y + h / 2 - (0 if not sub else -1.5)
    ax.text(x + w / 2, cy - 2, label, ha="center", fontsize=14, color=cor)
    if sub:
        ax.text(x + w / 2, cy - 7, sub, ha="center", fontsize=10, color=CINZA)


# ============================================================
# D1 — o mapa da aula: API -> n8n -> Postgres -> Metabase -> decisão
# ============================================================
f, ax = fig_ax(13, 4.6)
H = 100 * 4.6 / 13
y0 = H / 2 - 9
box(ax, 3, y0, 15, 16, "API", OLIST, sub="os pedidos\nda empresa")
box(ax, 27, y0, 15, 16, "n8n", N8N, sub="coleta e\nentrega")
cilindro(ax, 51, y0 - 1, 14, 19, BANCO, "Postgres", "a tabela\npedidos")
box(ax, 74, y0, 15, 16, "Metabase", DASH, sub="o dashboard")
boneco(ax, 96.5, y0 + 8, cor=OLIST, escala=1.15, label="quem decide")
seta(ax, 18.6, y0 + 8, 26.4, y0 + 8, "JSON", fs=12)
seta(ax, 42.6, y0 + 8, 50.0, y0 + 8, "INSERT", fs=12)
seta(ax, 65.8, y0 + 8, 73.4, y0 + 8, "SELECT", fs=12)
seta(ax, 89.6, y0 + 8, 93.6, y0 + 8)
# relógio em cima do n8n
ax.add_patch(Circle((34.5, y0 + 23), 3.4, fill=False, edgecolor=N8N, linewidth=2))
ax.plot([34.5, 34.5], [y0 + 23, y0 + 25.2], color=N8N, lw=1.8)
ax.plot([34.5, 36.2], [y0 + 23, y0 + 23], color=N8N, lw=1.8)
ax.text(39, y0 + 22.5, "todo dia, 8h", fontsize=11, color=N8N)
ax.text(34.5, 2.5, "Bloco 2", ha="center", fontsize=11, color=N8N)
ax.text(58, 2.5, "Bloco 1", ha="center", fontsize=11, color=BANCO)
ax.text(81.5, 2.5, "Bloco 3", ha="center", fontsize=11, color=DASH)
f.savefig(OUT / "d1_mapa.png", bbox_inches="tight", transparent=True)
plt.close(f)

# ============================================================
# D2 — arquivo (um dono) vs banco (muitos donos, ao vivo)
# ============================================================
f, ax = fig_ax(12, 4.8)
H = 100 * 4.8 / 12
# esquerda: arquivo
ax.text(16, H - 5, "ARQUIVO", ha="center", fontsize=15, color=CINZA)
ax.text(16, H - 10.5, "dado parado, um dono", ha="center", fontsize=11, color=CINZA)
folha = Polygon([(10, 8), (10, 26), (19, 26), (23, 22), (23, 8)],
                closed=True, edgecolor=CINZA, facecolor="#F1F3F5", linewidth=2.2)
ax.add_patch(folha)
ax.plot([19, 19, 23], [26, 22, 22], color=CINZA, lw=2.2)
ax.text(16.5, 16.5, ".parquet", ha="center", fontsize=12, color=CINZA)
boneco(ax, 33, 16, cor=CINZA, label="só um por vez")
seta(ax, 29.5, 17, 24.5, 17)
# divisor
ax.plot([47, 47], [6, H - 4], color="#CED4DA", lw=1.6, linestyle="--")
# direita: banco
ax.text(76, H - 5, "BANCO", ha="center", fontsize=15, color=BANCO)
ax.text(76, H - 10.5, "dado vivo, muitos donos ao mesmo tempo",
        ha="center", fontsize=11, color=BANCO)
cilindro(ax, 69, 8, 14, 20, BANCO, "Postgres", "sempre\nligado")
box(ax, 52, 18, 11, 9, "n8n", N8N, fs=12)
box(ax, 52, 5, 11, 9, "você\n(psql)", CINZA, fs=11)
box(ax, 89, 18, 10.5, 9, "Metabase", DASH, fs=10.5)
boneco(ax, 94.5, 8, cor=OLIST, label="o time")
seta(ax, 63.6, 22.5, 68.3, 20.5, "escreve", cor=N8N, fs=10, dy=2)
seta(ax, 63.6, 9.5, 68.3, 12, "lê", cor=CINZA, fs=10, dy=-3)
seta(ax, 84, 20.5, 88.4, 22.5, "lê", cor=DASH, fs=10, dy=2)
f.savefig(OUT / "d2_arquivo_vs_banco.png", bbox_inches="tight", transparent=True)
plt.close(f)

# ============================================================
# D3 — imagem (molde) -> containers (caixas) + volume (o dado sobrevive)
# ============================================================
f, ax = fig_ax(12, 4.8)
H = 100 * 4.8 / 12
box(ax, 4, 12, 17, 15, "IMAGEM", DOCKER, sub="o molde\n(docker pull, 1x)")
seta(ax, 22.5, 19.5, 29, 19.5, "cria")
ax.text(46, 36, "CONTAINERS: caixas rodando, descartáveis",
        fontsize=12, color=DOCKER, ha="center")
box(ax, 31, 14, 14, 11, "container", DOCKER, fs=12)
# o container que morreu: apagado, com X
ax.add_patch(FancyBboxPatch((49, 14), 14, 11, boxstyle="round,pad=0.6,rounding_size=1.6",
                            edgecolor="#ADB5BD", facecolor="#F1F3F5",
                            linewidth=2, linestyle=(0, (4, 3))))
ax.text(56, 21.5, "container", ha="center", fontsize=12, color="#ADB5BD")
ax.text(56, 17.5, "✗ apagou, sumiu", ha="center", fontsize=10.5, color=ERRO,
        fontfamily="DejaVu Sans")
seta(ax, 40, 13, 66, 8.5, "grava em", cor=BANCO, fs=11, dy=-2.6)
cilindro(ax, 68, 3, 15, 16, BANCO, "VOLUME", "fora da caixa")
ax.text(75.5, 25, "o dado SOBREVIVE ao\ndocker compose down",
        ha="center", fontsize=11.5, color=BANCO)
ax.text(92.5, 12, "sobe de novo?\no dado está lá.", ha="center",
        fontsize=11.5, color=OLIST)
f.savefig(OUT / "d3_imagem_container_volume.png", bbox_inches="tight", transparent=True)
plt.close(f)

# ============================================================
# D4 — a pegadinha do host: dentro do Docker, localhost é você mesmo
# ============================================================
f, ax = fig_ax(12, 5.2)
H = 100 * 5.2 / 12
# a caixa grande do Docker
ax.add_patch(FancyBboxPatch((30, 5), 66, H - 12, boxstyle="round,pad=0.8,rounding_size=2",
                            edgecolor=DOCKER, facecolor=DOCKER + "0A", linewidth=2.4))
ax.text(63, H - 4.5, "Docker (na sua máquina)", ha="center", fontsize=13, color=DOCKER)
box(ax, 37, 12, 20, 15, "metabase", DASH, sub="porta 3000")
box(ax, 70, 12, 20, 15, "postgres", BANCO, sub="porta 5432")
# certo: host = postgres
seta(ax, 58.5, 21, 68.5, 21, "host = postgres", cor=OLIST, fs=12.5)
ax.text(63.5, 26.5, "✓", fontsize=20, color=OLIST, ha="center", fontfamily="DejaVu Sans")
# errado: localhost aponta para ele mesmo (laço de volta)
ax.add_patch(FancyArrowPatch((40, 11.5), (46, 11.5), connectionstyle="arc3,rad=1.4",
                             arrowstyle="-|>", mutation_scale=18, linewidth=2,
                             color=ERRO, linestyle=(0, (4, 3))))
ax.text(47.5, 7.2, "host = localhost", fontsize=11.5, color=ERRO, ha="left")
ax.text(63.5, 7.2, "(aponta para ele MESMO)", fontsize=10.5, color=ERRO, ha="left")
ax.text(60.5, 7.2, "✗", fontsize=13, color=ERRO, fontfamily="DejaVu Sans", ha="left")
# você, fora da caixa
boneco(ax, 10, 22, cor=CINZA, escala=1.2, label="você (psql, DBeaver)")
seta(ax, 14, 24, 29, 22, "localhost:5432", cor=CINZA, fs=11)
ax.text(10, 36, "FORA do Docker,\nlocalhost funciona", ha="center",
        fontsize=11, color=CINZA)
f.savefig(OUT / "d4_host_metabase.png", bbox_inches="tight", transparent=True)
plt.close(f)

# ============================================================
# D5 — o container de navio: padronizou a caixa
# ============================================================
f, ax = fig_ax(12.5, 4.6)
H = 100 * 4.6 / 12.5
# navio
casco = Polygon([(6, 10), (10, 3), (40, 3), (44, 10)], closed=True,
                edgecolor=CINZA, facecolor="#F1F3F5", linewidth=2.4)
ax.add_patch(casco)
# ondas
for x0 in range(2, 44, 9):
    ax.plot([x0, x0 + 5], [1.2, 1.2], color=DOCKER, lw=1.6, alpha=0.6)
cores = [OLIST, N8N, BANCO, DASH, DOCKER, "#E8590C"]
for i in range(3):
    for j in range(2):
        ax.add_patch(FancyBboxPatch((11 + i * 10, 11 + j * 6.5), 9, 5.5,
                                    boxstyle="round,pad=0.2,rounding_size=0.6",
                                    edgecolor=cores[i * 2 + j],
                                    facecolor=cores[i * 2 + j] + "22", linewidth=2))
ax.text(25, 28.5, "a LOGÍSTICA padronizou a caixa", ha="center", fontsize=13, color=CINZA)
ax.text(25, H - 3, "não importa o que tem dentro:\nqualquer navio leva", ha="center",
        fontsize=11, color=CINZA)
# seta de analogia
seta(ax, 47, 15, 55, 15, "mesma ideia", fs=11)
# laptop
ax.add_patch(FancyBboxPatch((60, 8), 24, 14, boxstyle="round,pad=0.5,rounding_size=1.2",
                            edgecolor=CINZA, facecolor="#F8F9FA", linewidth=2.2))
ax.add_patch(Polygon([(58, 7.8), (86, 7.8), (89, 4), (55, 4)], closed=True,
                     edgecolor=CINZA, facecolor="#F1F3F5", linewidth=2))
for i, cor in enumerate([BANCO, DASH]):
    ax.add_patch(FancyBboxPatch((63 + i * 10, 11), 8.5, 7,
                                boxstyle="round,pad=0.2,rounding_size=0.6",
                                edgecolor=cor, facecolor=cor + "22", linewidth=2))
ax.text(67.2, 14.2, "postgres", ha="center", fontsize=9, color=BANCO)
ax.text(77.4, 14.2, "metabase", ha="center", fontsize=9, color=DASH)
ax.text(72, 28.5, "o DOCKER padronizou a caixa", ha="center", fontsize=13, color=DOCKER)
ax.text(72, H - 3, "não importa o que tem dentro:\nqualquer máquina roda", ha="center",
        fontsize=11, color=DOCKER)
f.savefig(OUT / "d5_navio.png", bbox_inches="tight", transparent=True)
plt.close(f)

# ============================================================
# D6 — índice: ler o livro todo vs índice remissivo
# ============================================================
f, ax = fig_ax(12, 4.6)
H = 100 * 4.6 / 12
# sem índice: livro com muitas linhas
ax.text(22, H - 4, "SEM ÍNDICE: lê tudo (Seq Scan)", ha="center", fontsize=13, color=ERRO)
ax.add_patch(FancyBboxPatch((8, 6), 28, 22, boxstyle="round,pad=0.5,rounding_size=1",
                            edgecolor=CINZA, facecolor="white", linewidth=2.2))
for i in range(7):
    y = 25 - i * 2.9
    ax.plot([11, 33], [y, y], color="#ADB5BD", lw=1.8)
# olho passando linha a linha
for i in range(7):
    ax.text(6.2, 24.3 - i * 2.9, "→", fontsize=10, color=ERRO, fontfamily="DejaVu Sans")
ax.text(22, 2.5, "96.470 linhas, uma a uma", ha="center", fontsize=11, color=CINZA)
# com índice
ax.text(72, H - 4, "COM ÍNDICE: vai direto (Index Scan)", ha="center", fontsize=13, color=OLIST)
ax.add_patch(FancyBboxPatch((56, 16), 24, 13, boxstyle="round,pad=0.5,rounding_size=1",
                            edgecolor=BANCO, facecolor=BANCO + "0D", linewidth=2.2))
ax.text(68, 25.5, "índice remissivo", ha="center", fontsize=11, color=BANCO)
ax.text(68, 20.5, "'SP':  páginas 3, 47, 112", ha="center", fontsize=12, color=BANCO)
ax.add_patch(FancyBboxPatch((84, 6), 13, 9, boxstyle="round,pad=0.4,rounding_size=1",
                            edgecolor=OLIST, facecolor=OLIST + "14", linewidth=2.2))
ax.text(90.5, 10, "a linha\ncerta", ha="center", fontsize=10.5, color=OLIST)
ax.add_patch(FancyArrowPatch((74, 16), (86, 12), connectionstyle="arc3,rad=-0.25",
                             arrowstyle="-|>", mutation_scale=20, linewidth=2.2, color=OLIST))
ax.text(66, 9, "custa espaço; escrita um\ntiquinho mais lenta. Vale.",
        ha="center", fontsize=10, color=CINZA)
f.savefig(OUT / "d6_indice.png", bbox_inches="tight", transparent=True)
plt.close(f)

# ============================================================
# D7 — OLAP vs OLTP
# ============================================================
f, ax = fig_ax(12, 4.6)
H = 100 * 4.6 / 12
ax.text(25, H - 4, "OLAP — analítico (DuckDB, Aula 1)", ha="center", fontsize=13, color=OLIST)
ax.add_patch(FancyBboxPatch((10, 7), 30, 20, boxstyle="round,pad=0.5,rounding_size=1",
                            edgecolor=OLIST, facecolor=OLIST + "0A", linewidth=2.2))
for i in range(5):
    ax.plot([13, 37], [24 - i * 3.6, 24 - i * 3.6], color=OLIST, lw=6, alpha=0.25)
ax.add_patch(FancyArrowPatch((4, 30), (13, 22), arrowstyle="-|>", mutation_scale=22,
                             linewidth=3, color=OLIST))
ax.text(25, 2.5, "POUCAS perguntas, cada uma varre MUITO dado", ha="center",
        fontsize=10.5, color=CINZA)
ax.text(75, H - 4, "OLTP — transacional (Postgres, hoje)", ha="center", fontsize=13, color=BANCO)
ax.add_patch(FancyBboxPatch((60, 7), 30, 20, boxstyle="round,pad=0.5,rounding_size=1",
                            edgecolor=BANCO, facecolor=BANCO + "0A", linewidth=2.2))
for i in range(5):
    ax.plot([63, 87], [24 - i * 3.6, 24 - i * 3.6], color=BANCO, lw=2, alpha=0.35)
import random
random.seed(3)
for k in range(8):
    x = 56 + (k % 2) * 40
    y = 9 + random.random() * 16
    ax.add_patch(FancyArrowPatch((x - 4 if k % 2 == 0 else x + 4, y),
                                 (61 if k % 2 == 0 else 89, y), arrowstyle="-|>",
                                 mutation_scale=10, linewidth=1.5, color=BANCO, alpha=0.8))
ax.text(75, 2.5, "MUITAS operações pequenas, ao mesmo tempo", ha="center",
        fontsize=10.5, color=CINZA)
f.savefig(OUT / "d7_olap_oltp.png", bbox_inches="tight", transparent=True)
plt.close(f)

# ============================================================
# D8 — o workflow do n8n, ponta a ponta (os 4 nodes)
# ============================================================
f, ax = fig_ax(13, 4.2)
H = 100 * 4.2 / 13
y0 = H / 2 - 8
nomes = [("Manual\nTrigger", N8N, "dispara\nna mão"),
         ("HTTP\nRequest", N8N, "pede à API\n(o garçom)"),
         ("Edit\nFields", N8N, "arruma\nos campos"),
         ("Postgres", BANCO, "INSERT na\ntabela")]
for i, (nome, cor, sub) in enumerate(nomes):
    x = 5 + i * 25
    box(ax, x, y0, 16, 17, nome, cor, fs=13.5)
    ax.text(x + 8, y0 - 4.5, sub, ha="center", fontsize=10.5, color=CINZA)
    if i:
        seta(ax, x - 8.2, y0 + 8.5, x - 1.2, y0 + 8.5)
ax.text(88, y0 + 22, "troque o 1o por Schedule Trigger\ne vira um SERVIÇO",
        ha="center", fontsize=11.5, color=N8N)
ax.add_patch(Circle((72, y0 + 23), 3, fill=False, edgecolor=N8N, linewidth=2))
ax.plot([72, 72], [y0 + 23, y0 + 25], color=N8N, lw=1.6)
ax.plot([72, 73.5], [y0 + 23, y0 + 23], color=N8N, lw=1.6)
f.savefig(OUT / "d8_workflow.png", bbox_inches="tight", transparent=True)
plt.close(f)

print("diagramas gerados:")
for p in sorted(OUT.glob("*.png")):
    print(" ", p.name)

# ============================================================
# D9 — constraints: o porteiro da tabela
# ============================================================
f, ax = fig_ax(12.5, 4.8)
H = 100 * 4.8 / 12.5
# a tabela, à direita
cilindro(ax, 78, 8, 16, 20, BANCO, "tabela", "pedidos")
# a porta/porteiro
ax.add_patch(FancyBboxPatch((60, 6), 9, 26, boxstyle="round,pad=0.5,rounding_size=1.2",
                            edgecolor=BANCO, facecolor=BANCO + "10", linewidth=2.4))
ax.text(64.5, H - 4, "constraints:\no porteiro", ha="center", fontsize=11.5, color=BANCO)
ax.text(64.5, 19, "tipo\nNOT NULL\nPRIMARY\nKEY", ha="center", fontsize=9.5, color=BANCO)
# tres linhas chegando
def linha_dado(y, txt, cor):
    ax.add_patch(FancyBboxPatch((6, y), 42, 6.5, boxstyle="round,pad=0.35,rounding_size=0.9",
                                edgecolor=cor, facecolor=cor + "10", linewidth=1.8))
    ax.text(27, y + 3.2, txt, ha="center", fontsize=10.5, color=cor,
            fontfamily="monospace" if False else None)
linha_dado(28, "('a1b', 'SP', 89.90)          dado ok", OLIST)
linha_dado(17.5, "(NULL, 'SP', ...)      sem id!", ERRO)
linha_dado(7, "('a1b', 'RJ', ...)    id repetido!", ERRO)
seta(ax, 48.5, 31, 59, 27, cor=OLIST)
seta(ax, 69.5, 21, 77, 19, "entra", cor=OLIST, fs=10.5)
ax.plot([52, 56], [19, 23], color=ERRO, lw=3)
ax.plot([52, 56], [23, 19], color=ERRO, lw=3)
ax.text(54, 14.5, "recusado\nna porta", ha="center", fontsize=10, color=ERRO)
seta(ax, 48.5, 10, 51.5, 17, cor=ERRO, ls=(0, (4, 3)))
f.savefig(OUT / "d9_porteiro.png", bbox_inches="tight", transparent=True)
plt.close(f)

# ============================================================
# D10 — transação: ou tudo, ou nada
# ============================================================
f, ax = fig_ax(12.5, 4.6)
H = 100 * 4.6 / 12.5
ax.text(25, H - 3.5, "SEM transação", ha="center", fontsize=13.5, color=ERRO)
box(ax, 6, 12, 13, 11, "conta A\n-100", CINZA, fs=11.5)
box(ax, 31, 12, 13, 11, "conta B\n+100 ?", CINZA, fs=11.5)
seta(ax, 20.5, 17.5, 29.5, 17.5, cor=CINZA)
# raio no meio
ax.plot([24.2, 25.8, 24.8, 26.4], [24, 20.5, 20.5, 16.8], color="#F59F00", lw=3)
ax.text(25, 27, "a luz cai aqui…", ha="center", fontsize=10.5, color="#F59F00")
ax.text(25, 7, "o dinheiro saiu de A\ne NUNCA chegou em B", ha="center",
        fontsize=10.5, color=ERRO)
ax.plot([50, 50], [5, H - 3], color="#CED4DA", lw=1.6, linestyle="--")
ax.text(75, H - 3.5, "COM transação (BEGIN … COMMIT)", ha="center",
        fontsize=13.5, color=OLIST)
ax.add_patch(FancyBboxPatch((56, 9), 38, 17, boxstyle="round,pad=0.6,rounding_size=1.6",
                            edgecolor=OLIST, facecolor=OLIST + "08",
                            linewidth=2.2, linestyle=(0, (5, 3))))
box(ax, 59, 13, 13, 10, "conta A\n-100", OLIST, fs=11)
box(ax, 78, 13, 13, 10, "conta B\n+100", OLIST, fs=11)
seta(ax, 73.5, 18, 76.5, 18, cor=OLIST)
ax.text(75, 6, "deu problema no meio? o banco DESFAZ tudo\n(ROLLBACK) — nunca fica pela metade",
        ha="center", fontsize=10.5, color=OLIST)
f.savefig(OUT / "d10_transacao.png", bbox_inches="tight", transparent=True)
plt.close(f)

# ============================================================
# D12 — script (você aperta) vs serviço (vive sozinho)
# ============================================================
f, ax = fig_ax(12.5, 4.4)
H = 100 * 4.4 / 12.5
ax.text(25, H - 3.5, "SCRIPT: você aperta", ha="center", fontsize=13.5, color=CINZA)
boneco(ax, 12, 15, cor=CINZA, escala=1.2)
box(ax, 20, 12, 10, 7, "RUN", CINZA, fs=11)
seta(ax, 16, 16, 19.3, 15.5, cor=CINZA)
box(ax, 36, 11.5, 12, 8.5, "roda 1x\ne para", CINZA, fs=10.5)
seta(ax, 31, 15.5, 35.2, 15.5, cor=CINZA)
ax.text(25, 4.5, "esqueceu de apertar? não rodou.", ha="center", fontsize=10.5, color=CINZA)
ax.plot([50, 50], [4, H - 3], color="#CED4DA", lw=1.6, linestyle="--")
ax.text(75, H - 3.5, "SERVIÇO: vive sozinho", ha="center", fontsize=13.5, color=N8N)
ax.add_patch(Circle((61, 16), 4.6, fill=False, edgecolor=N8N, linewidth=2.4))
ax.plot([61, 61], [16, 19.2], color=N8N, lw=2)
ax.plot([61, 63.6], [16, 16], color=N8N, lw=2)
ax.text(61, 8, "todo dia, 8h", ha="center", fontsize=10.5, color=N8N)
box(ax, 71, 11.5, 21, 9, "coleta -> INSERT", N8N, fs=11.5)
seta(ax, 66.2, 16, 70.2, 16, cor=N8N)
ax.text(75, 5, "com você dormindo. Isso é um serviço.", ha="center",
        fontsize=10.5, color=N8N)
f.savefig(OUT / "d12_script_servico.png", bbox_inches="tight", transparent=True)
plt.close(f)

# ============================================================
# D14 — Metabase: a geladeira e a vitrine
# ============================================================
f, ax = fig_ax(12.5, 4.8)
H = 100 * 4.8 / 12.5
# geladeira
ax.add_patch(FancyBboxPatch((10, 6), 16, 26, boxstyle="round,pad=0.5,rounding_size=1.4",
                            edgecolor=BANCO, facecolor=BANCO + "0A", linewidth=2.4))
ax.plot([11, 25], [22, 22], color=BANCO, lw=1.8)
ax.plot([11, 25], [14.5, 14.5], color=BANCO, lw=1.8)
for x, y in [(14, 24.5), (19, 24.5), (14, 17), (21, 17), (16.5, 9.5)]:
    ax.add_patch(Circle((x, y), 1.5, edgecolor=BANCO, facecolor=BANCO + "30", linewidth=1.4))
ax.text(18, H - 3.5, "POSTGRES: a geladeira", ha="center", fontsize=12.5, color=BANCO)
ax.text(18, 2.5, "guarda o dado", ha="center", fontsize=10.5, color=BANCO)
# vitrine
ax.add_patch(FancyBboxPatch((62, 8), 30, 20, boxstyle="round,pad=0.5,rounding_size=1.4",
                            edgecolor=DASH, facecolor=DASH + "08", linewidth=2.4))
ax.plot([63, 91], [15, 15], color=DASH, lw=1.6)
# grafiquinhos na vitrine
for i, hgt in enumerate([4, 7, 5.5, 8.5]):
    ax.add_patch(FancyBboxPatch((66 + i * 6, 16.5), 4, hgt,
                                boxstyle="round,pad=0.15,rounding_size=0.5",
                                edgecolor=DASH, facecolor=DASH + "30", linewidth=1.5))
ax.text(77, 11, "dashboards, sem código", ha="center", fontsize=10, color=DASH)
ax.text(77, H - 3.5, "METABASE: a vitrine", ha="center", fontsize=12.5, color=DASH)
ax.text(77, 3.5, "mostra — não guarda nada", ha="center", fontsize=10.5, color=DASH)
seta(ax, 27.5, 19, 60.5, 19, "SELECT, sempre ao vivo", cor=CINZA, fs=11)
f.savefig(OUT / "d14_geladeira_vitrine.png", bbox_inches="tight", transparent=True)
plt.close(f)
