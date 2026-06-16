# 00 — Setup do ambiente

Antes da Aula 1, prepare seu computador para acompanhar o curso.

**Tempo estimado:** 30–45 minutos.

---

## Checklist

| # | Item | Obrigatório |
|---|------|-------------|
| 1 | Python 3.10 ou superior | Sim |
| 2 | Cursor (editor com IA) | Sim |
| 3 | Bibliotecas (pandas, duckdb, jupyter) | Sim |
| 4 | Conta no GitHub + Git instalado | Sim |
| 5 | Conta gratuita no n8n cloud | Opcional (Aula 2) |

---

## Passo 1 — Instalar Python

Recomendado: **Python 3.10 ou superior**.

### Mac
```bash
python3 --version
```
Se aparecer `Python 3.10.x` ou superior, pode pular. Caso contrário, instale:
- Site oficial: https://www.python.org/downloads/macos/
- Ou via Homebrew: `brew install python`

### Windows
1. Baixe em https://www.python.org/downloads/windows/
2. **IMPORTANTE:** marque a opção "Add Python to PATH" na primeira tela
3. Confirme no PowerShell: `python --version`

### Linux
```bash
sudo apt update && sudo apt install -y python3 python3-pip
```

---

## Passo 2 — Instalar Cursor

Cursor é um editor de código gratuito (baseado no VS Code) com IA integrada.

1. Baixe em https://www.cursor.com/
2. Instale com as opções padrão
3. Na primeira abertura, faça login (pode ser com GitHub)
4. Escolha o plano **Hobby (gratuito)** — suficiente para todo o curso

### Extensões úteis
- Python (publicado pela Microsoft)
- Jupyter (publicado pela Microsoft)

### Plano B — VS Code
Se não puder usar Cursor (ex.: rede corporativa bloqueando), o VS Code padrão funciona:
- https://code.visualstudio.com/

---

## Passo 3 — Instalar bibliotecas

No terminal integrado do Cursor (Ctrl + ` ou Cmd + `), execute:

```bash
pip install -r ../requirements.txt
```

Ou minimamente:

```bash
pip install pandas duckdb jupyter notebook
```

---

## Passo 4 — Validar a instalação

Execute o script `teste_setup.py` que está nesta pasta:

```bash
python teste_setup.py
```

Você deve ver:
```
Pandas:  2.x.x
DuckDB:  1.x.x
Setup OK! Pronto para a aula.
```

Se aparecer, parabéns: ambiente pronto.

---

## Passo 5 — Conta GitHub + Git

### Conta GitHub
Crie gratuitamente em https://github.com/signup

### Git
- **Mac:** já vem instalado. Confira com `git --version`.
- **Windows:** https://git-scm.com/download/win
- **Linux:** `sudo apt install git`

### Configurar
```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"
```

(Use o mesmo email da conta GitHub.)

---

## Passo 6 (opcional) — Conta n8n para a Aula 2

Crie uma conta gratuita em https://app.n8n.cloud/register.

---

## Problemas comuns

| Erro | Solução |
|------|---------|
| `python: command not found` (Windows) | Reinstale o Python marcando "Add to PATH" |
| `pip: command not found` | Use `python -m pip install ...` |
| `ModuleNotFoundError: pandas` | No Cursor: Cmd/Ctrl + Shift + P → "Python: Select Interpreter" → escolha o Python 3.10+ |
| `Permission denied` no Mac/Linux | Use `pip install --user pandas duckdb jupyter` |
| Cursor não reconhece Python | `Python: Select Interpreter` no Cursor |
| `SSL: CERTIFICATE_VERIFY_FAILED` (Mac) | Execute `/Applications/Python\ 3.x/Install\ Certificates.command` |

---

## Próximo passo

Volte para [`../README.md`](../README.md) e abra a [`aula-1-dados-na-pratica/`](../aula-1-dados-na-pratica/).
