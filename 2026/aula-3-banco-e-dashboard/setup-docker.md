# Pré-Aula 3 | Docker — Requisitos para a Aula

**MBA Data Science & Analytics para Operações**
**Professor:** Fernando Henrique Vilella Nakamuta
**Data da aula:** 21/07/2026 (terça-feira, 19h–23h)
**Tempo de setup estimado:** 30–45 minutos

---

## Antes de começar

Na Aula 3 vamos subir um **banco de dados Postgres** e um **dashboard Metabase** na sua
máquina. Os dois rodam dentro do **Docker**.

Faça este tutorial **alguns dias antes do dia 21**. Diferente das aulas anteriores, aqui
baixamos ~1,5 GB de imagens — na Wi-Fi do estúdio, com a turma toda baixando ao mesmo
tempo, isso não termina a tempo. **Quem chegar com as imagens já baixadas começa a aula
rodando.**

A seção "Problemas comuns" no final cobre os erros mais frequentes.

---

## Checklist resumido

| # | Item | Tempo | Obrigatório |
|---|------|-------|-------------|
| 1 | Docker instalado | 15–20 min | Sim |
| 2 | Validar com `hello-world` | 2 min | Sim |
| 3 | Baixar as imagens (Postgres + Metabase) | 10 min | **Sim — não deixe para o dia** |
| 4 | Teste final: subir a stack e abrir o Metabase | 10 min | Sim |

**Requisitos da máquina:** 8 GB de RAM (mínimo) e **5 GB de disco livre**.

---

## O que é Docker (em uma frase)

Uma ferramenta que roda programas dentro de **caixas isoladas** (containers), já com tudo
que eles precisam dentro.

Instalar Postgres e Metabase na mão levaria uma aula inteira e daria errado em metade das
máquinas — cada uma com um sistema, uma versão, um conflito. Com Docker, **um comando sobe
os dois**, igual em todo mundo.

> É a mesma ideia do `pip install` da Aula 1, mas para programas inteiros em vez de
> bibliotecas Python.

---

## Passo 1 — Instalar o Docker

> **Qual Docker instalar? A resposta fácil:**
> **Mac e Windows → Docker Desktop.** É o mais simples: baixa, instala com clique, tem
> interface gráfica e cuida de tudo sozinho. É o que a maioria de vocês vai usar.
> **Linux → Docker Engine** (um comando no terminal, sem interface — instruções abaixo).
>
> Achou a sua situação? Vá direto para a sua seção. Só leia as outras se algo der errado.

### Mac

1. Baixe o **Docker Desktop** em https://www.docker.com/products/docker-desktop/
2. **Atenção ao chip:** escolha "Mac with Apple Silicon" (M1/M2/M3/M4) ou "Mac with Intel
   Chip". Se baixar o errado, não instala. Para descobrir: menu  → "Sobre este Mac".
3. Abra o `.dmg` e arraste o Docker para a pasta Aplicativos.
4. Abra o Docker Desktop e aceite os termos. Na primeira vez ele demora ~1 minuto.
5. Quando o ícone da baleia 🐳 aparecer na barra superior, está rodando.

### Windows

O Docker no Windows precisa do **WSL2** (o Linux que roda dentro do Windows).

1. Abra o **PowerShell como Administrador** (botão direito → "Executar como
   administrador") e rode:
   ```powershell
   wsl --install
   ```
2. **Reinicie o computador.** Esse passo não é opcional.
3. Baixe o **Docker Desktop** em https://www.docker.com/products/docker-desktop/
4. Instale com as opções padrão. Mantenha marcada a opção **"Use WSL 2 instead of
   Hyper-V"**.
5. Abra o Docker Desktop. Quando o ícone da baleia 🐳 ficar estável na bandeja do sistema
   (perto do relógio), está rodando.

> Se o `wsl --install` reclamar de virtualização desativada, veja "Problemas comuns".

### Linux (Ubuntu/Debian)

No Linux não precisa do Docker Desktop — o Docker Engine é mais leve e suficiente:

```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
```

Depois **feche e reabra o terminal** (ou reinicie a sessão) para o seu usuário entrar no
grupo `docker`. Sem isso, todo comando vai pedir `sudo`.

---

## Passo 2 — Validar a instalação

Abra o terminal (no Windows: **PowerShell**, não o CMD) e rode:

```bash
docker --version
docker compose version
```

Devem aparecer duas versões, algo como `Docker version 27.x.x` e `Docker Compose version
v2.x.x`.

Agora o teste de verdade:

```bash
docker run hello-world
```

Se aparecer:

```
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

**Está tudo certo.** Esse é o sinal de que você está pronto para o Passo 3.

---

## Passo 3 — Baixar as imagens (não deixe para o dia da aula)

Este é **o passo mais importante deste tutorial**. São ~1,5 GB.

```bash
docker pull postgres:16
docker pull metabase/metabase:latest
```

Vai demorar alguns minutos. Quando terminar, confirme:

```bash
docker images
```

Você deve ver as duas imagens listadas:

```
REPOSITORY          TAG       SIZE
postgres            16        ~430MB
metabase/metabase   latest    ~1.1GB
```

> Fez isso em casa? Na aula, subir a stack leva **10 segundos** em vez de 20 minutos.

---

## Passo 4 — Teste final: subir a stack

Vamos subir o Postgres e o Metabase uma vez, só para confirmar que funciona.

### 4.1 — Pegar o `docker-compose.yml`

Se você já clonou o repositório do curso, ele está em
`2026/aula-3-banco-e-dashboard/docker-compose.yml`. Entre nessa pasta:

```bash
cd 2026/aula-3-banco-e-dashboard
```

Se ainda não clonou:

```bash
git clone https://github.com/fenakamuta/poliusppro-data-engineering.git
cd poliusppro-data-engineering/2026/aula-3-banco-e-dashboard
```

### 4.2 — Subir

```bash
docker compose up -d
```

O `-d` faz rodar em segundo plano (você continua usando o terminal). Confirme:

```bash
docker compose ps
```

Os dois containers devem aparecer como `running`.

### 4.3 — Abrir o Metabase

No navegador, acesse:

```
http://localhost:3000
```

**Na primeira vez o Metabase demora 1–2 minutos** para responder — ele está se preparando.
Se der erro na hora, espere um pouco e recarregue. Quando aparecer a tela de boas-vindas
("Bem-vindo ao Metabase"), **funcionou**.

> Não precisa criar conta nem configurar nada agora. Faremos isso juntos na aula.
> Se quiser conferir o Postgres também: ele está em `localhost:5432` (usuário `aluno`,
> senha `aula3`, banco `olist`).

### 4.4 — Derrubar

```bash
docker compose down
```

Pronto. Está tudo validado e você pode fechar o Docker até o dia da aula.

---

## Problemas comuns

| Erro / sintoma | Causa provável | Solução |
|---|---|---|
| `docker: command not found` | Docker Desktop não está aberto, ou o terminal foi aberto antes da instalação | Abra o Docker Desktop e espere a baleia 🐳 estabilizar. Feche e reabra o terminal. |
| `Cannot connect to the Docker daemon` | O Docker está instalado mas não está **rodando** | Abra o Docker Desktop. No Linux: `sudo systemctl start docker` |
| `The command 'docker' could not be found in this WSL 2 distro` (Windows) | O Docker Desktop está instalado, mas a integração com o WSL está desligada — acontece quando você roda o terminal do Ubuntu/WSL (inclusive dentro do Cursor) | Docker Desktop → ⚙️ Settings → **Resources** → **WSL Integration** → ative a sua distro → **Apply & Restart**. Feche e reabra o terminal. |
| `permission denied while trying to connect to the Docker daemon` (Linux) | Seu usuário não está no grupo `docker` | `sudo usermod -aG docker $USER` e **reabra o terminal** |
| `WSL 2 installation is incomplete` (Windows) | WSL2 não instalado ou máquina não reiniciada | `wsl --install` no PowerShell **como administrador** e reinicie |
| `Virtualization is not enabled` / `Hardware assisted virtualization not available` (Windows) | Virtualização desligada na BIOS | Reinicie, entre na BIOS/UEFI (F2, F10 ou Del) e ative **Intel VT-x** ou **AMD-V** |
| `port is already allocated` / `bind: address already in use` na porta 5432 | Você já tem um Postgres instalado na máquina | Pare o Postgres local, **ou** troque `"5432:5432"` por `"5433:5432"` no `docker-compose.yml` (avise na aula que você mudou) |
| Mesmo erro na porta 3000 | Outro programa usando a 3000 (comum com Node/React) | Feche o outro programa, ou troque `"3000:3000"` por `"3001:3000"` |
| `localhost:3000` não abre / fica carregando | Metabase ainda está iniciando | Espere 2 minutos e recarregue. Veja o progresso com `docker compose logs -f metabase` |
| Docker Desktop pede login/licença ou a empresa bloqueia | Docker Desktop é pago para empresas grandes (250+ funcionários ou US$ 10M+ de receita) | **Plano B (Windows):** instale o Docker Engine dentro do WSL2 — abra o Ubuntu do WSL e rode o comando do Linux (Passo 1). Não precisa do Docker Desktop nem de licença. |
| Máquina muito lenta depois de instalar | Docker Desktop consome RAM em segundo plano | Feche o Docker Desktop quando não estiver usando. Ele só precisa estar aberto durante a aula. |
| `no space left on device` | Disco cheio | Libere espaço. As imagens precisam de ~2 GB; deixe 5 GB livres. `docker system prune` limpa restos antigos. |

---

## Antes da aula, garanta

- [ ] `docker run hello-world` imprime "Hello from Docker!"
- [ ] `docker images` lista **postgres:16** e **metabase/metabase**
- [ ] `docker compose up -d` sobe os dois containers
- [ ] `http://localhost:3000` abre a tela de boas-vindas do Metabase
- [ ] Você rodou `docker compose down` no final
- [ ] Pelo menos 5 GB de disco livre

---

## Sites de referência

Caso queira aprofundar antes da aula:

- Docker — o que é um container: https://docs.docker.com/get-started/
- Docker Compose — visão geral: https://docs.docker.com/compose/
- Postgres — documentação oficial: https://www.postgresql.org/docs/
- Metabase — primeiros passos: https://www.metabase.com/docs/latest/

---

## Última verificação rápida

Antes do dia 21/07, faça o teste final: rode `docker compose up -d` e veja se o Metabase
abre em `http://localhost:3000`. **Se abrir, você está pronto.**

Se travar em qualquer passo, me chame **antes** da aula — resolvemos com calma, em vez de
gastar o primeiro bloco com suporte técnico.

Nos vemos no estúdio dia 21/07.
