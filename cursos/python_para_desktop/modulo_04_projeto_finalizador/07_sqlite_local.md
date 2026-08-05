# 07 — SQLite

## 🎯 Objetivo

Neste capítulo você vai conectar o Sistema Escolar ao banco de dados SQLite, substituindo a frágil lista em memória por persistência real. Os alunos cadastrados sobreviverão ao fechamento do programa.

Ao final, você terá:

- O módulo `database/conexao.py` com funções para conectar e inicializar o banco
- O arquivo `escola.db` criado automaticamente na primeira execução
- A tabela `alunos` com id, nome, idade e turma
- O controller `aluno.py` refatorado para usar INSERT e SELECT
- A tela de cadastro carregando os dados do banco ao abrir — sem perder nada

## 📍 Contextualização

No Capítulo 06, você construiu um formulário de cadastro completo com validação e uma tabela Treeview. Os dados ficavam em uma lista no controller `aluno.py`. Funcionava, mas ao fechar a janela ou o sistema, tudo desaparecia.

Isso é inaceitável para um software real. Um sistema de gestão escolar não pode esquecer os alunos a cada reinicialização.

Agora você integrará o SQLite — um banco de dados leve, embutido e sem servidor — que é perfeito para aplicações desktop. A migração será suave porque você seguiu o padrão MVC: a View continuará igual; apenas o Controller e o novo módulo `database` serão alterados.

**Progresso do Sistema:**

```text
✅ Capítulo 01 — Introdução e Planejamento
✅ Capítulo 02 — Arquitetura do Sistema
✅ Capítulo 03 — Tela de Login
✅ Capítulo 04 — Menu Principal
✅ Capítulo 05 — Múltiplas Janelas
✅ Capítulo 06 — Cadastro de Alunos
🔨 SQLite ← VOCÊ ESTÁ AQUI
⬜ CRUD Completo
⬜ Banco em Nuvem
⬜ Integração e Testes
⬜ Refatoração e Entrega
```

## ✅ Resultado Esperado

Após este capítulo, o sistema se comportará da seguinte maneira:

- Ao executar `python main.py`, o banco `escola.db` é criado automaticamente (se não existir) e a tabela `alunos` é preparada.
- A tela de cadastro, ao ser aberta, exibe os alunos que já estavam salvos no banco.
- Ao salvar um novo aluno, ele é inserido no banco e permanece lá após fechar e reabrir o sistema.
- A tabela `alunos` tem a estrutura: `id` (chave primária autoincrement), `nome`, `idade`, `turma`.

Aparência: A interface visual não muda. A diferença está nos bastidores.

Arquivos criados ou modificados:

| Arquivo | Ação |
|---|---|
| `database/conexao.py` | Novo — conexão e inicialização do banco |
| `controllers/aluno.py` | Modificado — lógica de persistência migrada para SQL |
| `main.py` | Modificado — chama inicialização do banco |
| `views/cadastro.py` | Pequeno ajuste — atualizar tabela ao abrir usando banco |

## 💻 Implementação Guiada

### Passo 1 — Criando o módulo de conexão

Toda interação com o banco passará por um ponto central. Crie o arquivo `database/conexao.py`:

```python
# ======================================================================
# conexao.py — Gerenciador de Conexão com SQLite
# ======================================================================
# Eu sou o responsável por conectar ao banco de dados e garantir
# que as tabelas existam antes de qualquer operação.
# ======================================================================

import sqlite3
from pathlib import Path

# ---------- CONSTANTE DO CAMINHO ----------
# Eu defino onde o arquivo do banco será salvo.
# Uso pathlib para que funcione em qualquer sistema operacional.
CAMINHO_BANCO = Path(__file__).parent.parent / "escola.db"


def conectar():
    """
    Eu crio e retorno uma conexão com o banco SQLite.

    Uso um context manager para garantir que a conexão seja
    fechada corretamente após o uso.

    Retorno:
        sqlite3.Connection: objeto de conexão ativo
    """
    conexao = sqlite3.connect(str(CAMINHO_BANCO))
    # Ativo o modo de row_factory para acessar colunas por nome.
    conexao.row_factory = sqlite3.Row
    return conexao


def inicializar_banco():
    """
    Eu crio as tabelas do sistema, caso ainda não existam.

    Esta função deve ser chamada uma vez no início do programa,
    antes de qualquer operação de leitura ou escrita.
    """
    # Eu uso 'with' para garantir que a conexão feche mesmo se houver erro.
    with conectar() as conn:
        cursor = conn.cursor()

        # ---------- TABELA DE ALUNOS ----------
        # Eu crio a tabela 'alunos' com os campos necessários.
        # Uso IF NOT EXISTS para evitar erro se a tabela já existir.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                idade INTEGER NOT NULL,
                turma TEXT NOT NULL
            )
        """)

        # O commit é automático ao sair do with (a conexão fecha).
        # Mas eu chamo explicitamente por clareza.
        conn.commit()
```

!!! note "Conceito Importante"
    `row_factory = sqlite3.Row` permite acessar os valores das colunas por nome (ex: `aluno["nome"]`) em vez de índice numérico. Isso torna o código muito mais legível.

### Passo 2 — Atualizando o main.py para inicializar o banco

O banco precisa ser inicializado antes que qualquer tela tente acessá-lo. Basta uma linha no `main.py`.

Abra `main.py` e adicione a chamada logo após criar a janela principal.

```python
# ===== CÓDIGO EXISTENTE (trecho do main.py) =====
import tkinter as tk
from utils.helpers import centralizar_janela
from views.login import criar_tela_login
from views.menu import criar_menu

janela = tk.Tk()
janela.title("Sistema Escolar")
centralizar_janela(janela, 800, 600)
janela.resizable(False, False)

# ===== CÓDIGO NOVO (adicione abaixo) =====
# Eu inicio o banco de dados assim que o programa começa.
# Isso garante que as tabelas existam antes de qualquer acesso.
from database.conexao import inicializar_banco
inicializar_banco()

# ... callbacks e chamada da tela de login permanecem iguais
```

!!! tip "Dica Profissional"
    Em projetos maiores, a inicialização do banco pode ser movida para uma função `bootstrap()` ou para o próprio `conectar()`. Para nosso escopo, essa abordagem é clara e suficiente.

### Passo 3 — Refatorando o Controller de Alunos

Esta é a migração propriamente dita. Abra `controllers/aluno.py`. O código atual usa uma lista `alunos` e funções que manipulam essa lista. Vamos substituí-lo por operações SQL.

=== "ANTES (lista em memória)"

    ```python
    # controllers/aluno.py — versão antiga
    alunos = []
    
    def salvar_aluno(nome, idade, turma):
        aluno = {"nome": nome, "idade": idade, "turma": turma}
        alunos.append(aluno)
        return aluno
    
    def listar_alunos():
        return alunos
    ```

=== "DEPOIS (SQLite)"

    ```python
    # controllers/aluno.py — versão nova
    from database.conexao import conectar
    
    def salvar_aluno(nome, idade, turma):
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO alunos (nome, idade, turma)
                VALUES (?, ?, ?)
            """, (nome, idade, turma))
            conn.commit()
            return {"nome": nome, "idade": idade, "turma": turma}
    
    def listar_alunos():
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM alunos ORDER BY nome")
            alunos = cursor.fetchall()
            return [dict(aluno) for aluno in alunos]
    ```

Crie o novo arquivo `controllers/aluno.py` com o conteúdo completo:

```python
# ======================================================================
# aluno.py — Controlador de Alunos (com SQLite)
# ======================================================================
# Eu agora persisto os dados no banco de dados SQLite.
# As funções mantêm os mesmos nomes — a View não precisa mudar.
# ======================================================================

from database.conexao import conectar


def salvar_aluno(nome, idade, turma):
    """
    Eu insiro um novo aluno na tabela 'alunos' do banco.

    Parâmetros:
        nome: string
        idade: int
        turma: string

    Retorno:
        dict com os dados do aluno inserido
    """
    # Eu uso 'with' para abrir e fechar a conexão automaticamente.
    with conectar() as conn:
        cursor = conn.cursor()
        # Query parametrizada: os '?' evitam SQL Injection.
        cursor.execute("""
            INSERT INTO alunos (nome, idade, turma)
            VALUES (?, ?, ?)
        """, (nome, idade, turma))
        # Commit: sem ele, a inserção não é salva permanentemente.
        conn.commit()

    # Retorno um dicionário para manter compatibilidade com a View.
    return {"nome": nome, "idade": idade, "turma": turma}


def listar_alunos():
    """
    Eu busco todos os alunos cadastrados, ordenados por nome.

    Retorno:
        list de dict — cada dict contém id, nome, idade, turma
    """
    with conectar() as conn:
        cursor = conn.cursor()
        # SELECT simples com ORDER BY para organização alfabética.
        cursor.execute("SELECT * FROM alunos ORDER BY nome")
        alunos = cursor.fetchall()
        # Converte cada Row em um dicionário Python.
        return [dict(aluno) for aluno in alunos]


def limpar_dados():
    """
    Eu removo todos os alunos do banco (útil para testes).
    """
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM alunos")
        conn.commit()
```

!!! danger "Erro Crítico — Nunca concatene strings para SQL"
    Nunca faça: `cursor.execute(f"INSERT INTO alunos VALUES ('{nome}', {idade}, '{turma}')")`.
    Isso abre brechas de segurança (SQL Injection) e quebra com caracteres especiais.
    Use sempre placeholders `?` e passe os valores como tupla.

### Passo 4 — Atualizando a View de Cadastro

A view `cadastro.py` do Capítulo 06 já chamava `listar_alunos()` em `atualizar_tabela()`. Como mantivemos a mesma assinatura de função, a view funciona sem nenhuma alteração. A única diferença é que agora `listar_alunos()` retorna dados do banco (incluindo o campo `id`).

Contudo, podemos fazer uma pequena melhoria: como o Treeview agora recebe o `id`, podemos armazená-lo como um valor oculto. Isso será útil no próximo capítulo para identificar qual registro editar ou excluir.

Em `views/cadastro.py`, dentro da função `atualizar_tabela()`, altere a linha do `tree.insert`:

```python
# ===== CÓDIGO EXISTENTE =====
tree.insert("", tk.END, values=(aluno["nome"], aluno["idade"], aluno["turma"]))

# ===== CÓDIGO NOVO =====
# Agora eu guardo o id do aluno como o iid da linha (primeiro argumento depois de "").
# Isso permite identificar a linha unicamente sem exibir o id na tabela.
tree.insert(
    "",
    tk.END,
    iid=aluno["id"],           # iid = identificador interno da linha
    values=(aluno["nome"], aluno["idade"], aluno["turma"])
)
```

O campo `id` não será exibido (não está nas colunas), mas cada linha do Treeview terá um identificador único que corresponde ao `id` do banco. Isso é preparação para o CRUD do Capítulo 08.

### Passo 5 — Testando a persistência

Execute o sistema:

```bash
python main.py
```

- Faça login (admin / admin).
- Abra o Cadastro de Alunos e cadastre 2 ou 3 alunos.
- Feche a janela de cadastro.
- Feche o sistema completamente.
- Execute `python main.py` novamente.
- Abra o Cadastro de Alunos.

Os alunos cadastrados ainda estarão lá. A persistência está funcionando.

Você também pode verificar o arquivo `escola.db` na raiz do projeto. Com uma ferramenta como DB Browser for SQLite, você pode abrir o arquivo e ver a tabela `alunos` com os registros.

## 📝 Exercício

**Tempo estimado:** 15-20 minutos

**Tarefa:** Adicione uma funcionalidade que exiba a quantidade total de alunos cadastrados no título do LabelFrame da listagem. Por exemplo: "Alunos Cadastrados (5)".

Dica: Use `SELECT COUNT(*) FROM alunos` no controller e um Label ou atualize o texto do LabelFrame após cada operação.

??? hint "Dica"
    Crie uma função `contar_alunos()` no controller que retorna um inteiro. Na view, após `atualizar_tabela()`, chame essa função e atualize o texto do LabelFrame usando `frame_lista.config(text=f" Alunos Cadastrados ({total}) ")`.

??? success "Solução"
    Em `controllers/aluno.py`, adicione:
    
    ```python
    def contar_alunos():
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM alunos")
            return cursor.fetchone()[0]
    ```
    
    Em `views/cadastro.py`, importe `contar_alunos` e dentro de `atualizar_tabela`, após reinserir as linhas:
    
    ```python
    total = contar_alunos()
    frame_lista.config(text=f" Alunos Cadastrados ({total}) ")
    ```
    
    Chame `atualizar_tabela()` também após salvar, para que o contador atualize.

## 🏆 Missão da Equipe

**Tempo estimado:** 30-45 minutos

**Tarefa:** Migrem o projeto da equipe para SQLite, criando o banco de dados e a(s) tabela(s) específica(s) do domínio.

**Entregável:** O sistema da equipe com persistência total em SQLite.

**Checklist da Missão:**

- [ ] Criado o módulo `database/conexao.py` com `conectar()` e `inicializar_banco()`
- [ ] A função `inicializar_banco()` cria a(s) tabela(s) com campos adequados ao domínio
- [ ] O `main.py` chama `inicializar_banco()` na inicialização
- [ ] O controller da entidade principal (ex: `livro.py`, `produto.py`) foi refatorado para usar SQL
- [ ] `salvar_*` faz INSERT com parâmetros
- [ ] `listar_*` faz SELECT e retorna lista de dicionários
- [ ] O Treeview carrega os dados do banco ao abrir a tela
- [ ] Os dados sobrevivem ao fechar e reabrir o programa
- [ ] O professor verificou o arquivo `.db` gerado

!!! important "Nota para o Professor"
    Verifique: Cada equipe deve ter um arquivo `.db` gerado após o primeiro cadastro. Peça que fechem e reabram o sistema para confirmar a persistência. Verifique se as queries são parametrizadas (sem concatenação).

## ⚡ Desafio

**Vá além:** Substitua as credenciais hardcoded do login por uma tabela `usuarios` no banco de dados.

Atualmente, `controllers/auth.py` valida o login contra um dicionário fixo. Sua missão é:

1. Adicionar em `inicializar_banco()` a criação da tabela `usuarios` com campos `id`, `usuario`, `senha`.
2. Inserir um usuário padrão (admin / admin) se a tabela estiver vazia.
3. Refatorar `validar_login` para consultar o banco: `SELECT * FROM usuarios WHERE usuario=? AND senha=?`.
4. (Opcional) No futuro, a senha deveria ser armazenada com hash — mas para este desafio, mantenha texto puro.

Dica: Use `INSERT OR IGNORE` para evitar duplicar o usuário padrão.

??? success "Solução resumida"
    Em `database/conexao.py`, adicione na `inicializar_banco()`:
    
    ```python
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    """)
    cursor.execute("""
        INSERT OR IGNORE INTO usuarios (usuario, senha)
        VALUES ('admin', 'admin')
    """)
    ```
    
    Em `controllers/auth.py`:
    
    ```python
    from database.conexao import conectar
    
    def validar_login(usuario, senha):
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM usuarios WHERE usuario=? AND senha=?",
                (usuario, senha)
            )
            if cursor.fetchone():
                return True
        messagebox.showerror("Erro de Login", "Usuário ou senha inválidos.")
        return False
    ```

## ⚠️ Erros Comuns

!!! danger "Esquecer o commit() após INSERT"
    **Sintoma:** Nenhum erro aparece, os dados parecem salvos, mas ao reabrir o sistema a tabela está vazia.
    
    **Causa:** O INSERT foi executado, mas sem `commit()` a transação não foi efetivada no disco.
    
    **Solução:** Sempre chame `conn.commit()` após operações de escrita (INSERT, UPDATE, DELETE). Com o `with conectar()`, o commit pode ser colocado dentro do bloco.

!!! danger "Concatenação de strings na query SQL"
    **Sintoma:** `sqlite3.OperationalError: near "João": syntax error` ou, pior, o sistema funciona mas é vulnerável.
    
    **Causa:** Uso de f-strings ou `+` para montar a query, como `f"INSERT INTO alunos VALUES ('{nome}', ...)"`. Se o nome tiver apóstrofo (ex: D'Artagnan), quebra a sintaxe SQL.
    
    **Solução:** Use placeholders `?` e tupla: `cursor.execute("INSERT INTO alunos (nome) VALUES (?)", (nome,))`.

!!! warning "Caminho do banco relativo incorreto"
    **Sintoma:** `sqlite3.OperationalError: unable to open database file`.
    
    **Causa:** O caminho para `escola.db` está errado ou o diretório não tem permissão de escrita. Às vezes, o programa tenta criar o banco numa pasta diferente da esperada.
    
    **Solução:** Use `pathlib.Path(__file__).parent.parent / "escola.db"` para garantir que o banco fique na raiz do projeto, independente de onde o script é executado.

!!! warning "Não chamar inicializar_banco()"
    **Sintoma:** `sqlite3.OperationalError: no such table: alunos`.
    
    **Causa:** O `main.py` não chama `inicializar_banco()` antes de usar o controller.
    
    **Solução:** Adicione `inicializar_banco()` no início de `main.py`, após a criação da janela principal.

## 💡 Boas Práticas

**1. Context Manager (with) para conexões**

Usar `with conectar() as conn:` garante que a conexão seja fechada mesmo se ocorrer uma exceção. Isso evita vazamentos de recursos e arquivos travados.

**2. Queries parametrizadas com ?**

Além de seguras, as queries parametrizadas permitem que o SQLite otimize o plano de execução. Nunca monte SQL concatenando strings do usuário.

**3. row_factory = sqlite3.Row**

Permite acessar colunas por nome (`aluno["nome"]`), tornando o código mais expressivo. Sem isso, você acessaria por índice (`aluno[1]`), o que é frágil se a ordem das colunas mudar.

**4. IF NOT EXISTS nas criações de tabela**

Evita erros se o banco já existir. É uma prática defensiva que torna o código idempotente (pode ser executado várias vezes sem efeitos colaterais).

**5. Separação clara entre database e controllers**

O módulo database sabe como conectar; o controller sabe o que fazer com os dados. Essa separação permite trocar de banco (ex: PostgreSQL) alterando apenas `database/conexao.py`.

## ☑️ Checklist

Antes de prosseguir para o próximo capítulo, confirme:

- [ ] O arquivo `database/conexao.py` existe com `conectar()` e `inicializar_banco()`
- [ ] A função `inicializar_banco()` cria a tabela `alunos` com `id`, `nome`, `idade`, `turma`
- [ ] O `main.py` chama `inicializar_banco()` antes de abrir a tela de login
- [ ] O controller `aluno.py` usa INSERT INTO e SELECT parametrizados
- [ ] A view `cadastro.py` atualiza a tabela com dados do banco (sem alterações drásticas)
- [ ] Cadastrei alunos, fechei o sistema, reabri e os alunos ainda estavam lá
- [ ] O arquivo `escola.db` foi gerado na raiz do projeto
- [ ] Nenhum código usa concatenação de strings para SQL
- [ ] Minha equipe concluiu a Missão da Equipe

## ➡️ Próximo Capítulo

No **Capítulo 08 — CRUD Completo**, você implementará as operações que faltam: Consultar com filtros, Editar um registro selecionado e Excluir com confirmação. O Treeview que você preparou com iid será a chave para identificar qual linha editar ou excluir.

O sistema passará de "cadastro simples" para um CRUD completo. É o último grande passo antes da integração com a nuvem. 🗃️
