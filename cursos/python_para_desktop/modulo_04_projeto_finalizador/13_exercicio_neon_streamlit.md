# 13 — Exercício Prático: Banco em Nuvem com Neon + Streamlit

## 🎯 Objetivo

Neste capítulo-exercício você vai construir um **app web de gerenciamento de tarefas** usando Python, Streamlit e um banco de dados PostgreSQL em nuvem (Neon Database).

Ao final, você terá:

- Um projeto no Neon Database com banco PostgreSQL funcionando na nuvem
- Tabelas `usuarios` e `tarefas` criadas com SQL real (PostgreSQL)
- Um sistema de **cadastro e login** de usuários com hash de senha
- Um **CRUD completo de tarefas** com status (Em Aberto, Realizando, Em Atraso)
- Controle de **datas** (criação e prazo limite) com detecção automática de atraso
- O arquivo `.env` protegendo as credenciais do banco
- A experiência de usar **Python na web** com Streamlit

!!! note "Por que este exercício?"
    Nos capítulos anteriores você construiu o Sistema Escolar como uma aplicação **desktop** com Tkinter e SQLite. Agora, vamos mudar o cenário: em vez de desktop, vamos para a **web**. Em vez de SQLite local, vamos usar um **banco de dados PostgreSQL em nuvem**. Isso mostra a versatilidade do Python — a mesma linguagem que você já domina serve para desktop, web, automação, ciência de dados e muito mais.

## 📍 Contextualização

Você já domina Python, já construiu interfaces gráficas com Tkinter, já conectou ao SQLite, já fez CRUD completo e já sincronizou com banco em nuvem (Firebase). Agora, vamos expandir seu repertório com duas ferramentas poderosas do ecossistema Python:

**Streamlit** — uma biblioteca que transforma scripts Python em aplicações web interativas. Sem precisar de HTML, CSS ou JavaScript. Você escreve Python puro e o Streamlit gera a interface web automaticamente.

**Neon Database** — um serviço de banco de dados PostgreSQL 100% em nuvem, com plano gratuito generoso. Diferente do Firebase (que usa JSON), o Neon usa SQL real — o mesmo SQL que você aprendeu com o SQLite, mas agora rodando em um servidor remoto acessível de qualquer lugar.

**Progresso do Sistema:**

```text
✅ Capítulo 01 — Introdução e Planejamento
✅ Capítulo 02 — Arquitetura do Sistema
✅ Capítulo 03 — Tela de Login
✅ Capítulo 04 — Menu Principal
✅ Capítulo 05 — Múltiplas Janelas
✅ Capítulo 06 — Cadastro de Alunos
✅ Capítulo 07 — SQLite
✅ Capítulo 08 — CRUD Completo
✅ Capítulo 09 — Banco em Nuvem
✅ Capítulo 10 — Integração
✅ Capítulo 11 — Refatoração
✅ Capítulo 12 — Projeto Final
🔨 Exercício: Neon + Streamlit ← VOCÊ ESTÁ AQUI
```

!!! tip "Dica Profissional"
    No mercado de trabalho, saber conectar Python a bancos em nuvem é uma das habilidades mais requisitadas. Empresas como Nubank, iFood e Mercado Livre usam PostgreSQL em nuvem para suas aplicações. O Neon Database é a versão moderna e serverless desse mesmo PostgreSQL.

## ✅ Resultado Esperado

Ao final do exercício, você terá um app web rodando no navegador com este visual:

```text
┌─────────────────────────────────────────────────────────┐
│  🗂️ Gerenciador de Tarefas            [Olá, João! Sair]│
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─ Nova Tarefa ──────────────────────────────────────┐ │
│  │  Título:     [Estudar PostgreSQL_________]         │ │
│  │  Descrição:  [Revisar JOINs e subqueries]          │ │
│  │  Prazo:      [15/08/2026]                          │ │
│  │  [➕ Criar Tarefa]                                 │ │
│  └────────────────────────────────────────────────────┘ │
│                                                         │
│  ┌─ 📋 Em Aberto (2) ────────────────────────────────┐ │
│  │  • Estudar PostgreSQL     Prazo: 15/08  [▶][🗑️]   │ │
│  │  • Fazer relatório        Prazo: 20/08  [▶][🗑️]   │ │
│  └────────────────────────────────────────────────────┘ │
│                                                         │
│  ┌─ ⏳ Realizando (1) ───────────────────────────────┐ │
│  │  • Revisar código         Prazo: 10/08  [✅][🗑️]  │ │
│  └────────────────────────────────────────────────────┘ │
│                                                         │
│  ┌─ 🔴 Em Atraso (1) ────────────────────────────────┐ │
│  │  • Entregar projeto       Prazo: 01/08  [✅][🗑️]  │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

Comportamento esperado:

- O usuário se cadastra com nome, e-mail e senha
- Após o login, acessa o painel de tarefas (apenas as suas)
- Pode criar tarefas com título, descrição e prazo
- Pode mover tarefas entre status: Em Aberto → Realizando → Concluída
- Tarefas cujo prazo já passou são marcadas automaticamente como "Em Atraso"
- Pode excluir tarefas com confirmação
- Tudo é salvo no banco PostgreSQL na nuvem (Neon)

Estrutura do projeto:

```text
exercicio_tarefas/
├── .env                  # Credenciais do Neon (NÃO versionado)
├── .env.example          # Template sem valores sensíveis
├── .gitignore            # Ignora .env e __pycache__
├── app.py                # App principal Streamlit
├── database.py           # Conexão e operações com Neon
└── requirements.txt      # Dependências do projeto
```

| Arquivo | Descrição |
|---|---|
| `.env` | Connection string do Neon Database |
| `.env.example` | Template para outros desenvolvedores |
| `.gitignore` | Protege o `.env` e arquivos temporários |
| `app.py` | Interface web com Streamlit |
| `database.py` | Módulo de conexão e operações SQL |
| `requirements.txt` | Lista de pacotes necessários |

## 💻 Implementação Guiada

### Passo 1 — Criando o projeto no Neon Database

O Neon é um serviço de banco de dados PostgreSQL serverless. Vamos criar uma conta e um projeto.

1. Acesse **neon.tech** no navegador
2. Clique em **Sign Up** — pode usar conta do Google ou GitHub
3. Após o login, clique em **Create Project**
4. Dê o nome **exercicio-tarefas** ao projeto
5. Escolha a região mais próxima (ex: **São Paulo** se disponível, ou **US East**)
6. Clique em **Create Project**

Após criar, o Neon mostrará a **connection string** — uma URL que contém todas as informações para conectar ao banco. Ela se parece com isto:

```text
postgresql://usuario:senha@ep-xxxx-yyyy.us-east-2.aws.neon.tech/neondb?sslmode=require
```

!!! danger "Erro Crítico"
    Copie essa connection string e guarde em um lugar seguro. Ela contém sua senha! Nunca cole no código-fonte diretamente — vamos usar o `.env` para protegê-la.

!!! note "Conceito Importante"
    O PostgreSQL é o banco de dados relacional mais avançado do mundo open-source. Diferente do SQLite (que é um arquivo local), o PostgreSQL roda em um servidor e aceita conexões remotas. O Neon oferece isso gratuitamente na nuvem com 0.5 GB de armazenamento — mais do que suficiente para nosso exercício.

### Passo 2 — Preparando o ambiente do projeto

Crie a pasta do exercício e os arquivos de configuração:

```bash
mkdir exercicio_tarefas
cd exercicio_tarefas
```

Instale as dependências necessárias:

```bash
pip install streamlit psycopg2-binary python-dotenv
```

- `streamlit` — framework web para Python
- `psycopg2-binary` — driver PostgreSQL para Python
- `python-dotenv` — carrega variáveis de ambiente do `.env`

Crie o arquivo `requirements.txt`:

```text
streamlit
psycopg2-binary
python-dotenv
```

Crie o arquivo `.env` na raiz do projeto:

```text
# ===== CREDENCIAIS DO NEON DATABASE =====
# ATENÇÃO: Este arquivo NÃO deve ser versionado!
DATABASE_URL=postgresql://usuario:senha@ep-xxxx.us-east-2.aws.neon.tech/neondb?sslmode=require
```

Substitua o valor de `DATABASE_URL` pela connection string que você copiou no Passo 1.

Crie o arquivo `.env.example` (este será versionado):

```text
# Copie este arquivo para .env e preencha com seus dados
DATABASE_URL=postgresql://usuario:senha@host/banco?sslmode=require
```

Crie o arquivo `.gitignore`:

```text
.env
__pycache__/
*.pyc
```

!!! warning "Atenção"
    Lembre-se: o `.env` contém a senha do seu banco. Se você usar Git, NUNCA faça commit dele. O `.gitignore` garante que o Git vai ignorar esse arquivo automaticamente.

### Passo 3 — Módulo de conexão com o banco (database.py)

Crie o arquivo `database.py`. Ele será responsável por toda a comunicação com o Neon Database.

Comece com a conexão e a criação das tabelas:

```python
# ======================================================================
# database.py — Conexão e operações com Neon Database
# ======================================================================
# Eu sou responsável por toda a comunicação com o banco PostgreSQL
# na nuvem. Uso o psycopg2 para conectar e executar SQL.
# ======================================================================

import os
import hashlib
from datetime import date, datetime
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

# Eu carrego as variáveis de ambiente do arquivo .env.
load_dotenv()


def conectar():
    """
    Eu abro uma conexão com o banco Neon Database.
    Retorno a conexão pronta para uso.
    """
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError(
            "DATABASE_URL não encontrada. "
            "Verifique o arquivo .env"
        )
    # Eu conecto usando a URL completa do Neon.
    # O RealDictCursor retorna resultados como dicionários.
    conn = psycopg2.connect(database_url)
    return conn
```

!!! note "Conceito Importante"
    O `psycopg2` é o driver mais usado para conectar Python ao PostgreSQL. A connection string (`DATABASE_URL`) contém tudo: usuário, senha, host, porta e nome do banco. O `sslmode=require` garante que a conexão é criptografada — essencial para bancos em nuvem.

Agora, adicione a função que cria as tabelas:

```python
def criar_tabelas():
    """
    Eu crio as tabelas no banco se elas ainda não existirem.
    Uso IF NOT EXISTS para evitar erros na segunda execução.
    """
    conn = conectar()
    cursor = conn.cursor()

    # Eu crio a tabela de usuários.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            email VARCHAR(150) UNIQUE NOT NULL,
            senha VARCHAR(255) NOT NULL,
            data_cadastro TIMESTAMP DEFAULT NOW()
        )
    """)

    # Eu crio a tabela de tarefas.
    # Cada tarefa pertence a um usuário (usuario_id).
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id SERIAL PRIMARY KEY,
            titulo VARCHAR(200) NOT NULL,
            descricao TEXT,
            status VARCHAR(20) DEFAULT 'Em Aberto',
            data_criacao TIMESTAMP DEFAULT NOW(),
            data_limite DATE,
            usuario_id INTEGER REFERENCES usuarios(id)
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()
```

!!! tip "Dica Profissional"
    No PostgreSQL, `SERIAL` gera IDs automáticos (equivalente ao `INTEGER PRIMARY KEY AUTOINCREMENT` do SQLite). O `REFERENCES usuarios(id)` cria uma chave estrangeira — o banco garante que toda tarefa pertence a um usuário válido. Se tentar inserir uma tarefa com um `usuario_id` inexistente, o banco rejeita.

### Passo 4 — Funções de usuário (cadastro e login)

Continue no `database.py`. Adicione as funções de cadastro e autenticação:

```python
def hash_senha(senha):
    """
    Eu transformo a senha em um hash SHA-256.
    Assim, a senha real nunca é armazenada no banco.
    """
    return hashlib.sha256(senha.encode()).hexdigest()


def cadastrar_usuario(nome, email, senha):
    """
    Eu cadastro um novo usuário no banco.
    A senha é armazenada como hash, nunca em texto puro.
    Retorno True se sucesso, False se o email já existe.
    """
    conn = conectar()
    cursor = conn.cursor()
    try:
        senha_hash = hash_senha(senha)
        cursor.execute("""
            INSERT INTO usuarios (nome, email, senha)
            VALUES (%s, %s, %s)
        """, (nome, email, senha_hash))
        conn.commit()
        return True
    except psycopg2.errors.UniqueViolation:
        # O email já está cadastrado no banco.
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()
```

!!! note "Conceito Importante"
    O `hash_senha` transforma "minha_senha_123" em algo como "a1b2c3d4e5f6...". Mesmo que alguém acesse o banco, não conseguirá descobrir a senha original. O hash é uma via de mão única — não é possível reverter.

Agora, a função de login:

```python
def autenticar_usuario(email, senha):
    """
    Eu verifico se o email e a senha correspondem
    a um usuário cadastrado no banco.
    Retorno os dados do usuário se autenticado, None se não.
    """
    conn = conectar()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    senha_hash = hash_senha(senha)

    cursor.execute("""
        SELECT id, nome, email FROM usuarios
        WHERE email = %s AND senha = %s
    """, (email, senha_hash))

    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    return usuario
```

Perceba que no PostgreSQL usamos `%s` como placeholder (no SQLite, usamos `?`). O funcionamento é o mesmo: protege contra SQL Injection.

### Passo 5 — Funções de tarefas (CRUD)

Continue no `database.py`. Adicione as operações CRUD para tarefas:

```python
def criar_tarefa(titulo, descricao, data_limite, usuario_id):
    """
    Eu insiro uma nova tarefa no banco.
    O status inicial é sempre 'Em Aberto'.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tarefas
            (titulo, descricao, data_limite, usuario_id)
        VALUES (%s, %s, %s, %s)
    """, (titulo, descricao, data_limite, usuario_id))
    conn.commit()
    cursor.close()
    conn.close()


def listar_tarefas(usuario_id):
    """
    Eu busco todas as tarefas de um usuário específico.
    Retorno como lista de dicionários, ordenadas por data.
    """
    conn = conectar()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        SELECT * FROM tarefas
        WHERE usuario_id = %s
        ORDER BY data_criacao DESC
    """, (usuario_id,))
    tarefas = cursor.fetchall()
    cursor.close()
    conn.close()
    return tarefas
```

Agora, as funções de atualizar e excluir:

```python
def atualizar_status(tarefa_id, novo_status):
    """
    Eu altero o status de uma tarefa.
    Os status possíveis: 'Em Aberto', 'Realizando', 'Concluída'.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tarefas SET status = %s WHERE id = %s
    """, (novo_status, tarefa_id))
    conn.commit()
    cursor.close()
    conn.close()


def excluir_tarefa(tarefa_id):
    """
    Eu removo uma tarefa do banco permanentemente.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM tarefas WHERE id = %s",
        (tarefa_id,)
    )
    conn.commit()
    cursor.close()
    conn.close()
```

Com isso, o módulo `database.py` está completo. Ele contém: conexão, criação de tabelas, cadastro/login de usuários e CRUD de tarefas.

### Passo 6 — Interface web com Streamlit (app.py — Login e Cadastro)

Agora vamos criar o `app.py` — o coração do nosso app web.

O Streamlit funciona de forma diferente do Tkinter. Em vez de criar janelas e widgets manualmente, você chama funções como `st.text_input()`, `st.button()` e `st.write()` — e o Streamlit gera a página web automaticamente.

Comece o arquivo `app.py`:

```python
# ======================================================================
# app.py — Gerenciador de Tarefas (Streamlit + Neon)
# ======================================================================
# Eu sou o app principal. Uso o Streamlit para criar a interface
# web e o database.py para comunicar com o banco na nuvem.
# ======================================================================

import streamlit as st
from datetime import date, datetime
import database as db

# Eu crio as tabelas no banco na primeira execução.
db.criar_tabelas()

# ---------- CONFIGURAÇÃO DA PÁGINA ----------
st.set_page_config(
    page_title="Gerenciador de Tarefas",
    page_icon="🗂️",
    layout="centered"
)
```

!!! note "Conceito Importante"
    O `st.session_state` é como o Streamlit "lembra" informações entre interações. Cada vez que o usuário clica em algo, o Streamlit reexecuta o script inteiro. Sem o `session_state`, todas as variáveis seriam perdidas. Ele funciona como uma memória persistente durante a sessão do usuário.

Adicione a função de tela de login e cadastro:

```python
def tela_autenticacao():
    """
    Eu exibo as abas de Login e Cadastro.
    Quando o usuário se autentica, salvo os dados na sessão.
    """
    st.title("🗂️ Gerenciador de Tarefas")
    st.markdown("---")

    # Eu crio duas abas: uma para Login, outra para Cadastro.
    aba_login, aba_cadastro = st.tabs(
        ["🔑 Login", "📝 Cadastro"]
    )

    # ---------- ABA DE LOGIN ----------
    with aba_login:
        st.subheader("Acesse sua conta")
        email_login = st.text_input(
            "E-mail", key="email_login"
        )
        senha_login = st.text_input(
            "Senha", type="password", key="senha_login"
        )

        if st.button("Entrar", key="btn_login"):
            if not email_login or not senha_login:
                st.error("Preencha todos os campos!")
            else:
                usuario = db.autenticar_usuario(
                    email_login, senha_login
                )
                if usuario:
                    # Eu salvo o usuário na sessão.
                    st.session_state["usuario"] = usuario
                    st.success(f"Bem-vindo, {usuario['nome']}!")
                    st.rerun()
                else:
                    st.error("E-mail ou senha incorretos!")
```

Continue no mesmo arquivo — a aba de cadastro:

```python
    # ---------- ABA DE CADASTRO ----------
    with aba_cadastro:
        st.subheader("Crie sua conta")
        nome_cad = st.text_input(
            "Nome completo", key="nome_cad"
        )
        email_cad = st.text_input(
            "E-mail", key="email_cad"
        )
        senha_cad = st.text_input(
            "Senha", type="password", key="senha_cad"
        )
        senha_conf = st.text_input(
            "Confirmar senha", type="password",
            key="senha_conf"
        )

        if st.button("Cadastrar", key="btn_cadastro"):
            # Eu valido os campos antes de cadastrar.
            if not all([nome_cad, email_cad, senha_cad]):
                st.error("Preencha todos os campos!")
            elif senha_cad != senha_conf:
                st.error("As senhas não conferem!")
            elif len(senha_cad) < 6:
                st.error("A senha deve ter no mínimo 6 caracteres!")
            else:
                sucesso = db.cadastrar_usuario(
                    nome_cad, email_cad, senha_cad
                )
                if sucesso:
                    st.success(
                        "Conta criada! Vá para a aba Login."
                    )
                else:
                    st.error("Este e-mail já está cadastrado!")
```

### Passo 7 — Interface web (app.py — Painel de Tarefas)

Agora vamos criar a tela principal — o painel onde o usuário gerencia suas tarefas. Continue no `app.py`:

```python
def tela_tarefas():
    """
    Eu exibo o painel de tarefas do usuário logado.
    Mostro as tarefas separadas por status.
    """
    usuario = st.session_state["usuario"]

    # ---------- CABEÇALHO ----------
    col_titulo, col_sair = st.columns([4, 1])
    with col_titulo:
        st.title("🗂️ Gerenciador de Tarefas")
    with col_sair:
        st.write("")  # Eu avanço uma linha para alinhar.
        st.write(f"Olá, **{usuario['nome']}**!")
        if st.button("🚪 Sair"):
            del st.session_state["usuario"]
            st.rerun()

    st.markdown("---")

    # ---------- FORMULÁRIO DE NOVA TAREFA ----------
    with st.expander("➕ Nova Tarefa", expanded=False):
        titulo = st.text_input("Título da tarefa")
        descricao = st.text_area("Descrição (opcional)")
        data_limite = st.date_input(
            "Prazo limite",
            min_value=date.today()
        )

        if st.button("Criar Tarefa"):
            if not titulo:
                st.error("O título é obrigatório!")
            else:
                db.criar_tarefa(
                    titulo, descricao,
                    data_limite, usuario["id"]
                )
                st.success(f"Tarefa '{titulo}' criada!")
                st.rerun()
```

Agora, a parte mais importante — a listagem de tarefas separadas por status:

```python
    # ---------- LISTAGEM DE TAREFAS ----------
    tarefas = db.listar_tarefas(usuario["id"])

    # Eu verifico quais tarefas estão em atraso.
    # Se a data_limite já passou e o status não é 'Concluída',
    # eu marco como 'Em Atraso'.
    for tarefa in tarefas:
        if (tarefa["data_limite"]
                and tarefa["data_limite"] < date.today()
                and tarefa["status"] not in
                    ["Concluída", "Em Atraso"]):
            db.atualizar_status(tarefa["id"], "Em Atraso")
            tarefa["status"] = "Em Atraso"

    # Eu separo as tarefas por status.
    em_aberto = [t for t in tarefas
                 if t["status"] == "Em Aberto"]
    realizando = [t for t in tarefas
                  if t["status"] == "Realizando"]
    em_atraso = [t for t in tarefas
                 if t["status"] == "Em Atraso"]
    concluidas = [t for t in tarefas
                  if t["status"] == "Concluída"]
```

!!! tip "Dica Profissional"
    A detecção automática de atraso é um padrão muito usado em sistemas de gerenciamento de projetos (como Jira, Trello, Asana). Toda vez que a página carrega, verificamos se o prazo passou — se sim, atualizamos o status. Isso garante que o usuário sempre veja a situação real das tarefas.

Agora, vamos exibir cada grupo de tarefas:

```python
    # ---------- EXIBIR TAREFAS POR STATUS ----------
    def exibir_grupo(titulo_grupo, icone, tarefas_grupo,
                     cor, proximo_status=None,
                     icone_acao=None):
        """
        Eu exibo um grupo de tarefas com o mesmo status.
        Cada tarefa tem botões de ação.
        """
        st.subheader(
            f"{icone} {titulo_grupo} ({len(tarefas_grupo)})"
        )
        if not tarefas_grupo:
            st.caption("Nenhuma tarefa nesta categoria.")
            return

        for tarefa in tarefas_grupo:
            with st.container():
                c1, c2, c3 = st.columns([5, 1, 1])
                with c1:
                    prazo = ""
                    if tarefa["data_limite"]:
                        prazo = tarefa["data_limite"].strftime(
                            "%d/%m/%Y"
                        )
                    st.markdown(
                        f"**{tarefa['titulo']}** — "
                        f"Prazo: {prazo}"
                    )
                    if tarefa["descricao"]:
                        st.caption(tarefa["descricao"])

                with c2:
                    if (proximo_status and
                            st.button(
                                icone_acao,
                                key=f"acao_{tarefa['id']}"
                            )):
                        db.atualizar_status(
                            tarefa["id"], proximo_status
                        )
                        st.rerun()

                with c3:
                    if st.button(
                        "🗑️",
                        key=f"del_{tarefa['id']}"
                    ):
                        db.excluir_tarefa(tarefa["id"])
                        st.rerun()
```

Por fim, chame a função para cada grupo:

```python
    # Eu exibo cada grupo de tarefas.
    exibir_grupo(
        "Em Aberto", "📋", em_aberto, "blue",
        "Realizando", "▶️"
    )
    exibir_grupo(
        "Realizando", "⏳", realizando, "orange",
        "Concluída", "✅"
    )
    exibir_grupo(
        "Em Atraso", "🔴", em_atraso, "red",
        "Concluída", "✅"
    )
    exibir_grupo(
        "Concluídas", "✅", concluidas, "green"
    )
```

### Passo 8 — Fluxo principal do app

Para fechar o `app.py`, adicione o fluxo principal que decide qual tela exibir:

```python
# ============================================================
# FLUXO PRINCIPAL
# ============================================================
# Eu decido qual tela exibir baseado na sessão do usuário.
# Se está logado → painel de tarefas.
# Se não está → tela de login/cadastro.
# ============================================================

if "usuario" in st.session_state:
    tela_tarefas()
else:
    tela_autenticacao()
```

!!! note "Conceito Importante"
    O fluxo do Streamlit é linear: o script roda de cima para baixo toda vez que o usuário interage. O `session_state` é o que permite manter o estado entre as execuções. Quando o usuário clica em "Entrar", salvamos o usuário no `session_state`. Quando o script reexecuta, ele vê que há um usuário logado e mostra a tela de tarefas.

### Passo 9 — Executando e testando

Para rodar o app, abra o terminal na pasta do projeto e execute:

```bash
streamlit run app.py
```

O Streamlit abrirá automaticamente o navegador em `http://localhost:8501`.

**Roteiro de teste:**

1. Na aba **Cadastro**, crie uma conta com nome, e-mail e senha
2. Vá para a aba **Login** e entre com o e-mail e senha cadastrados
3. No painel, crie 3 tarefas com prazos diferentes (uma no passado para testar atraso)
4. Clique em ▶️ para mover uma tarefa de "Em Aberto" para "Realizando"
5. Clique em ✅ para concluir uma tarefa
6. Verifique que a tarefa com prazo no passado aparece em "Em Atraso"
7. Clique em 🗑️ para excluir uma tarefa
8. Clique em "Sair" e faça login novamente — suas tarefas devem estar lá (estão no banco na nuvem!)

!!! tip "Dica Profissional"
    Para verificar os dados diretamente no banco, acesse o painel do Neon (**console.neon.tech**) → seu projeto → **SQL Editor**. Lá você pode executar consultas como `SELECT * FROM tarefas;` e ver os dados que foram inseridos pelo app.

```text
┌────────────────────────────────────────────────────┐
│  Console do Neon — SQL Editor                       │
│                                                    │
│  > SELECT * FROM tarefas;                          │
│                                                    │
│  id │ titulo           │ status     │ data_limite  │
│  ───┼──────────────────┼────────────┼──────────── │
│  1  │ Estudar Python   │ Realizando │ 2026-08-15  │
│  2  │ Fazer relatório  │ Em Aberto  │ 2026-08-20  │
│  3  │ Entregar projeto │ Em Atraso  │ 2026-08-01  │
└────────────────────────────────────────────────────┘
```

## 📝 Exercício

**Tempo estimado:** 15-20 minutos

**Tarefa:** Adicione um campo de **prioridade** às tarefas. A prioridade pode ser: "Baixa", "Média" ou "Alta". Modifique o banco, o formulário e a listagem para exibir a prioridade ao lado do título.

??? hint "Dica"
    Você precisará:
    
    1. Adicionar uma coluna à tabela: `ALTER TABLE tarefas ADD COLUMN prioridade VARCHAR(10) DEFAULT 'Média';`
    2. Modificar a função `criar_tarefa` para receber o parâmetro `prioridade`
    3. No `app.py`, adicionar um `st.selectbox("Prioridade", ["Baixa", "Média", "Alta"])` no formulário
    4. Na listagem, exibir um emoji antes do título: 🟢 Baixa, 🟡 Média, 🔴 Alta

??? success "Solução resumida"
    No `database.py`, modifique a criação da tabela adicionando a coluna (ou execute o ALTER TABLE):
    
    ```python
    # Na função criar_tabelas, adicione após CREATE TABLE tarefas:
    cursor.execute("""
        ALTER TABLE tarefas
        ADD COLUMN IF NOT EXISTS prioridade
        VARCHAR(10) DEFAULT 'Média'
    """)
    ```
    
    Modifique `criar_tarefa`:
    
    ```python
    def criar_tarefa(titulo, descricao, data_limite,
                     usuario_id, prioridade="Média"):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tarefas
                (titulo, descricao, data_limite,
                 usuario_id, prioridade)
            VALUES (%s, %s, %s, %s, %s)
        """, (titulo, descricao, data_limite,
              usuario_id, prioridade))
        conn.commit()
        cursor.close()
        conn.close()
    ```
    
    No `app.py`, no formulário:
    
    ```python
    prioridade = st.selectbox(
        "Prioridade", ["Baixa", "Média", "Alta"]
    )
    # E passe para a função:
    db.criar_tarefa(
        titulo, descricao, data_limite,
        usuario["id"], prioridade
    )
    ```
    
    Na listagem, mapeie prioridade → emoji:
    
    ```python
    icones_prioridade = {
        "Baixa": "🟢", "Média": "🟡", "Alta": "🔴"
    }
    icone_p = icones_prioridade.get(
        tarefa.get("prioridade", "Média"), "🟡"
    )
    st.markdown(
        f"{icone_p} **{tarefa['titulo']}** — "
        f"Prazo: {prazo}"
    )
    ```

## 🏆 Missão da Equipe

**Tempo estimado:** 30-45 minutos

**Tarefa:** Adaptem o Gerenciador de Tarefas para o contexto do **projeto da equipe**. Em vez de tarefas genéricas, gerenciem as tarefas reais do Projeto Final.

**Entregável:** O app Streamlit rodando localmente com:

- Conta de cada membro da equipe cadastrada
- No mínimo 5 tarefas reais do Projeto Final cadastradas
- Tarefas distribuídas entre os status (Em Aberto, Realizando, Concluída)
- Prazos reais definidos para cada tarefa

**Checklist da Missão:**

- [ ] Todos os membros criaram conta no app
- [ ] No mínimo 5 tarefas reais do projeto foram cadastradas
- [ ] As tarefas possuem prazos reais
- [ ] Cada membro consegue ver apenas suas tarefas
- [ ] O sistema detecta automaticamente tarefas em atraso
- [ ] Todos os membros demonstraram login e CRUD funcionando
- [ ] O professor verificou o app rodando e os dados no Neon

!!! important "Nota para o Professor"
    Verifique: Cada equipe deve demonstrar o app completo rodando. Peça que um membro cadastre uma tarefa na frente da turma. Depois, peça que outro membro (em outro navegador, se possível) faça login e veja que sua conta é independente. Acesse o console do Neon e mostre os dados na tabela. Isso reforça o conceito de banco em nuvem.

## ⚡ Desafio

**Vá além:** Implemente um painel de **estatísticas** na tela principal que mostra:

- Total de tarefas por status (gráfico de pizza ou barras)
- Percentual de conclusão (barra de progresso)
- Próxima tarefa a vencer (a mais urgente)

Dica: O Streamlit possui funções nativas para gráficos. Use `st.bar_chart()` ou `st.metric()` para exibir números de forma visual. Para a barra de progresso, use `st.progress(percentual)`.

```python
# Exemplo de métricas no Streamlit:
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Em Aberto", len(em_aberto))
with col2:
    st.metric("Realizando", len(realizando))
with col3:
    st.metric("Concluídas", len(concluidas))

total = len(tarefas)
if total > 0:
    progresso = len(concluidas) / total
    st.progress(progresso)
    st.caption(
        f"{progresso:.0%} das tarefas concluídas"
    )
```

**Desafio extra:** Deploy no **Streamlit Community Cloud** (gratuito):

1. Suba o código para um repositório GitHub (sem o `.env`!)
2. Acesse **share.streamlit.io**
3. Conecte o repositório e configure a `DATABASE_URL` nos "Secrets" do Streamlit Cloud
4. Agora o app estará acessível por qualquer navegador, em qualquer lugar!

## ⚠️ Erros Comuns

!!! danger "Connection string inválida ou ausente"
    **Sintoma:** `ValueError: DATABASE_URL não encontrada` ou `psycopg2.OperationalError: could not connect to server`.
    
    **Causa:** O arquivo `.env` não existe, está vazio, ou a connection string está incorreta. Outra causa comum: copiar a URL com espaços extras.
    
    **Solução:** Verifique se o arquivo `.env` está na mesma pasta do `app.py`. Abra o `.env` e confirme que a `DATABASE_URL` está preenchida corretamente. Copie a URL novamente do painel do Neon. Não use aspas ao redor da URL no `.env`.

!!! warning "Erro de SSL ao conectar ao Neon"
    **Sintoma:** `psycopg2.OperationalError: SSL SYSCALL error`.
    
    **Causa:** A connection string não inclui `?sslmode=require` ou a rede está bloqueando conexões SSL (comum em redes corporativas/escolares).
    
    **Solução:** Confirme que a URL termina com `?sslmode=require`. Se estiver em uma rede restritiva, tente usar uma rede diferente (hotspot do celular, por exemplo). O Neon exige SSL obrigatoriamente.

!!! warning "E-mail duplicado no cadastro"
    **Sintoma:** `psycopg2.errors.UniqueViolation: duplicate key value violates unique constraint`.
    
    **Causa:** Tentou cadastrar com um e-mail que já existe. Nossa função já trata isso, mas se você não usou o `try/except`, o erro aparece.
    
    **Solução:** Verifique se a função `cadastrar_usuario` tem o bloco `except psycopg2.errors.UniqueViolation` que retorna `False`. No app, exiba uma mensagem amigável ao usuário.

!!! danger "Session state perdido ao atualizar a página"
    **Sintoma:** O usuário faz login, mas ao pressionar F5 (atualizar a página) é deslogado.
    
    **Causa:** O `session_state` do Streamlit só persiste durante a sessão ativa no navegador. Atualizar a página reinicia a sessão.
    
    **Solução:** Este é o comportamento esperado do Streamlit. Para uma solução mais robusta, seria necessário usar cookies ou tokens JWT — mas isso está além do escopo deste exercício. Informe os alunos que é normal.

!!! warning "Tarefas não aparecem após criar"
    **Sintoma:** O formulário confirma "Tarefa criada!", mas a tarefa não aparece na lista.
    
    **Causa:** O `st.rerun()` não foi chamado após a inserção, ou a função `listar_tarefas` está filtrando por outro `usuario_id`.
    
    **Solução:** Confirme que há um `st.rerun()` logo após o `st.success()` no botão de criar. Verifique se o `usuario_id` passado para `criar_tarefa` e `listar_tarefas` é o mesmo (vindo de `st.session_state["usuario"]["id"]`).

## 💡 Boas Práticas

**1. Separação de responsabilidades**

O `database.py` cuida do banco, o `app.py` cuida da interface. Nenhum código SQL aparece no `app.py`, nenhum widget Streamlit aparece no `database.py`. Essa separação é o mesmo princípio que você aplicou no Sistema Escolar com a arquitetura MVC. No mundo real, projetos grandes têm dezenas de módulos separados.

**2. Credenciais protegidas com .env**

A `DATABASE_URL` contém sua senha. Se alguém acessar essa string, terá controle total sobre seu banco. Usar `.env` e `.gitignore` é o padrão da indústria. Serviços como Heroku, Vercel e o próprio Streamlit Cloud usam variáveis de ambiente para configuração — você já está aprendendo o jeito profissional.

**3. Hash de senhas obrigatório**

Nunca armazene senhas em texto puro. Mesmo em exercícios didáticos, usar hash ensina o hábito certo. No mercado, frameworks como Django e FastAPI fazem hash automaticamente. Neste exercício, usamos SHA-256 — em produção real, o ideal é usar `bcrypt` ou `argon2`, que são mais resistentes a ataques.

**4. SQL parametrizado contra SQL Injection**

Usamos `%s` como placeholder em vez de concatenar strings no SQL. Isso protege contra SQL Injection — um ataque onde o usuário digita código SQL malicioso no campo de entrada. Se alguém digitar `'; DROP TABLE tarefas; --` no campo de título, o `%s` trata como texto puro, não como comando SQL.

**5. Banco em nuvem vs banco local**

O SQLite é perfeito para aplicações desktop single-user. O PostgreSQL em nuvem (Neon) é ideal para apps web multi-user. Saber quando usar cada um é uma habilidade essencial para desenvolvedores. A regra geral: se mais de uma pessoa vai acessar os dados ao mesmo tempo → use um banco em nuvem.

## ☑️ Checklist

Antes de considerar o exercício concluído, confirme:

- [ ] Conta no Neon Database criada com projeto ativo
- [ ] Arquivo `.env` configurado com `DATABASE_URL` válida
- [ ] Arquivo `.env.example` criado como template
- [ ] `.gitignore` inclui `.env` e `__pycache__/`
- [ ] `requirements.txt` com as 3 dependências listadas
- [ ] Tabelas `usuarios` e `tarefas` criadas no Neon
- [ ] Cadastro de usuário funcionando (com hash de senha)
- [ ] Login validando e-mail e senha corretamente
- [ ] Criação de tarefas com título, descrição e prazo
- [ ] Listagem de tarefas separada por status
- [ ] Botão para avançar status (Em Aberto → Realizando → Concluída)
- [ ] Detecção automática de tarefas em atraso
- [ ] Exclusão de tarefas funcionando
- [ ] Cada usuário vê apenas suas próprias tarefas
- [ ] Dados persistem no Neon (fechar e reabrir o app mantém os dados)
- [ ] Minha equipe concluiu a Missão da Equipe

## ➡️ Conclusão

Parabéns! 🎉 Você acaba de construir uma **aplicação web completa** usando Python.

Compare o que você fez neste exercício com o Sistema Escolar:

| Aspecto | Sistema Escolar | Gerenciador de Tarefas |
|---|---|---|
| Interface | Tkinter (desktop) | Streamlit (web) |
| Banco de dados | SQLite (local) | PostgreSQL/Neon (nuvem) |
| Acesso | Apenas na máquina | Qualquer navegador |
| Driver Python | `sqlite3` (nativo) | `psycopg2` (instalado) |
| Placeholder SQL | `?` | `%s` |
| Multi-usuário | Não | Sim (cada um com login) |

A linguagem é a mesma — **Python**. As estruturas são as mesmas — funções, variáveis, condicionais, loops. O que mudou foi o **ecossistema**: em vez de Tkinter, usamos Streamlit; em vez de SQLite, usamos PostgreSQL. Essa é a beleza do Python: uma linguagem, múltiplos mundos.

Leve esse conhecimento para seu Projeto Final. Mesmo que o projeto use Tkinter + SQLite (como pedido), você agora sabe que existe um universo além do desktop. E quando o professor perguntar "o que você faria diferente?" — você já tem a resposta: **"Eu colocaria na web com Streamlit e banco em nuvem"**. 🚀
