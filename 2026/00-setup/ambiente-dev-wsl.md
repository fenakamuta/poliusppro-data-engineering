# (Opcional) Um ambiente dev gostoso no Windows — WSL + terminal turbinado

> Nada aqui é obrigatório para o curso. É o setup para quem usa o terminal
> todo dia e quer que ele seja um lugar agradável. Tempo total: ~20 min.

---

## O que é o WSL, afinal?

**WSL (Windows Subsystem for Linux)** é um Linux completo rodando *dentro* do
Windows — sem máquina virtual pesada, sem dual boot. Você abre um terminal e
está no Ubuntu; seus arquivos do Windows aparecem em `/mnt/c/`.

Por que isso importa em dados: o mundo de dados fala Linux — servidores,
containers, a nuvem inteira. Com o WSL você usa as mesmas ferramentas e
comandos do "mundo real" sem sair do Windows. (O Docker Desktop, inclusive,
usa o WSL2 por baixo dos panos.)

**Instalar é uma linha** — PowerShell *como administrador*:

```powershell
wsl --install
```

Reinicie o computador; o Ubuntu abre e pede para criar usuário e senha. Pronto.

---

## 1. Hyper — um terminal bonito

O [Hyper](https://hyper.is) é um terminal minimalista e bonito (o Windows
Terminal, que já vem no Windows, também é ótimo — escolha um).

1. Baixe em **hyper.is** e instale.
2. Para o Hyper abrir direto no Ubuntu/WSL: menu **Edit → Preferences** e ajuste:

```js
shell: 'C:\\Windows\\System32\\wsl.exe',
shellArgs: [],
```

3. Salve e reabra. Bônus de estilo: fonte grande (`fontSize: 16`) e um tema
   (`plugins: ['hyper-one-dark']`).

---

## 2. zsh — um shell melhor que o padrão

O Ubuntu vem com **bash**. O **zsh** faz o mesmo, com autocompletar mais
esperto e um ecossistema de plugins gigante. No terminal do Ubuntu:

```bash
sudo apt update && sudo apt install -y zsh
chsh -s $(which zsh)     # torna o zsh o shell padrão
```

Feche e reabra o terminal. Na primeira vez o zsh pergunta sobre configuração —
pode responder `0` (arquivo vazio); o próximo passo cuida disso.

---

## 3. oh-my-zsh — o zsh de gente grande

O [oh-my-zsh](https://ohmyz.sh) é um "pacote de qualidade de vida" para o zsh:
temas, atalhos e plugins prontos. Uma linha:

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

Os dois plugins que valem a instalação inteira:

```bash
git clone https://github.com/zsh-users/zsh-autosuggestions \
  ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-syntax-highlighting \
  ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```

Abra o `~/.zshrc` (ex.: `nano ~/.zshrc`) e edite a linha de plugins:

```bash
plugins=(git zsh-autosuggestions zsh-syntax-highlighting)
```

Recarregue: `source ~/.zshrc`. Agora o terminal **sugere o comando enquanto
você digita** (aceite com →) e pinta de verde/vermelho o que está certo/errado.

---

## 4. Miniconda — Python sem dor

O [Miniconda](https://docs.conda.io/en/latest/miniconda.html) gerencia versões
de Python e ambientes isolados (um por projeto, sem conflito):

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh    # aceite a licença, caminho padrão
```

**O passo que todo mundo esquece** (colocar o conda no PATH do zsh):

```bash
~/miniconda3/bin/conda init zsh
source ~/.zshrc
```

E o uso no dia a dia — um ambiente para o curso:

```bash
conda create -n poliusppro python=3.12 -y
conda activate poliusppro
pip install -r requirements.txt      # na pasta 2026/ do repo
```

> Regra de ouro: `conda activate poliusppro` **em toda janela nova** antes de
> rodar Python. O `(poliusppro)` no prompt confirma que está no ambiente certo.

---

## A ordem importa

zsh **antes** do oh-my-zsh (ele se instala no shell atual) e conda **por
último** (o `conda init zsh` escreve no `.zshrc`, que precisa existir). Se
instalou fora de ordem, rode `~/miniconda3/bin/conda init zsh` de novo e
recarregue o terminal.
