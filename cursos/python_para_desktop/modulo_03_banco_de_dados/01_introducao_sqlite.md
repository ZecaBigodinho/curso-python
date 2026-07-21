# Introdução a Banco de Dados com SQLite

## Objetivos

Neste capítulo, você aprenderá a:

- Compreender os conceitos fundamentais de bancos de dados relacionais: tabelas, registros, colunas e chaves primárias.
- Conhecer o SQLite como um banco de dados leve, embutido e sem servidor, ideal para aplicações desktop.
- Utilizar o módulo `sqlite3` da biblioteca padrão do Python para conectar e operar um banco de dados SQLite.
- Criar tabelas e definir suas estruturas com comandos SQL (`CREATE TABLE`).
- Realizar as quatro operações básicas de persistência — CRUD: Criar (`INSERT`), Ler (`SELECT`), Atualizar (`UPDATE`) e Excluir (`DELETE`).
- Empregar parâmetros em consultas para prevenir injeção de SQL e garantir segurança.
- Tratar exceções e gerenciar conexões e cursores de forma adequada.
- Integrar SQLite em aplicações Python desktop, substituindo arquivos JSON ou CSV por uma solução mais robusta e escalável.

## Pré-requisitos

Antes de prosseguir, certifique-se de que você domina:

- Python básico: variáveis, tipos de dados, estruturas de controle (`if`, `for`, `while`).
- Funções: definição, parâmetros e retorno.
- Manipulação de strings e formatação.
- Coleções: listas, tuplas e dicionários.
- Manipulação de arquivos (leitura e escrita) e tratamento de exceções (`try`/`except`).

Nenhum conhecimento prévio de SQL é exigido; os comandos serão explicados ao longo do capítulo.

## Motivação

Até o momento, utilizamos arquivos de texto ou JSON para armazenar dados em nossas aplicações. Embora funcionais para pequenos volumes, essas abordagens se tornam limitadas quando precisamos fazer buscas complexas, evitar duplicidades, garantir integridade ou relacionar diferentes conjuntos de informações. Imagine um sistema de vendas: como cruzar os dados de clientes, produtos e pedidos usando apenas arquivos JSON? As operações se tornariam lentas e o código, excessivamente complexo.

Bancos de dados resolvem esses problemas. Eles são projetados para armazenar, organizar e recuperar informações de forma eficiente e confiável. O SQLite ocupa um lugar especial: é um banco de dados relacional completo, mas que dispensa a instalação de um servidor — todo o banco fica contido em um único arquivo. É a escolha perfeita para aplicações desktop, aplicativos mobile e protótipos.

Neste capítulo, você dará um passo fundamental rumo ao desenvolvimento profissional, aprendendo a integrar SQLite com Python e a executar as operações essenciais de qualquer sistema: criar, ler, atualizar e excluir registros.

## Conteúdo

### O que é um banco de dados relacional?

Um banco de dados relacional organiza as informações em tabelas (como planilhas), onde cada linha representa um registro e cada coluna representa um campo (atributo). As tabelas podem se relacionar entre si através de chaves. A linguagem padrão para interagir com esses bancos é a SQL (Structured Query Language).

Exemplo de tabela clientes:

| id | nome | email | idade |
|---|---|---|---|
| 1 | Ana Silva | ana@email.com | 28 |
| 2 | Bruno Costa | bruno@email.com | 35 |
| 3 | Carla Mendes | carla@email.com | 22 |

Aqui, `id` é a chave primária — um identificador único para cada registro.

### Por que SQLite?

SQLite é um mecanismo de banco de dados que:

- Não requer servidor: o banco é um único arquivo (`.db` ou `.sqlite`).
- É autocontido e leve: ideal para aplicações locais.
- Suporta a maior parte do SQL padrão.
- Está incluído na biblioteca padrão do Python (módulo `sqlite3`).
- É amplamente utilizado: Firefox, Chrome, Android, iOS e muitos outros softwares o empregam.

!!! note "SQLite vs. outros bancos"
    SQLite é excelente para aplicações desktop de usuário único ou com poucos acessos simultâneos. Para sistemas web com muitos usuários concorrentes, bancos como PostgreSQL ou MySQL são mais adequados. Mas para nossos projetos Python desktop, o SQLite é perfeito.

### Conectando ao banco de dados com sqlite3

O módulo `sqlite3` fornece a conexão e o cursor. O padrão básico é:

```python
import sqlite3

# Conexão com o banco (cria o arquivo se não existir)
conexao = sqlite3.connect("meu_banco.db")

# Cursor para executar comandos SQL
cursor = conexao.cursor()

# ... operações ...

# Salvar (confirmar) as alterações e fechar
conexao.commit()
conexao.close()
```

O método `commit()` efetiva as mudanças (`INSERT`, `UPDATE`, `DELETE`). Sem ele, as alterações são descartadas ao fechar a conexão.

!!! tip "Use gerenciador de contexto"
    O módulo `sqlite3` suporta o protocolo `with`, que faz commit automaticamente em caso de sucesso e rollback (desfaz) se ocorrer uma exceção. É a forma recomendada:
    ```python
    with sqlite3.connect("banco.db") as conn:
        cursor = conn.cursor()
        # comandos SQL
    # commit e close automáticos
    ```

### Criando tabelas (CREATE TABLE)

Para armazenar dados, primeiro definimos a estrutura da tabela com `CREATE TABLE`. Cada coluna tem um nome, tipo de dado e restrições (opcionais).

```python
import sqlite3

with sqlite3.connect("clientes.db") as conn:
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            idade INTEGER
        )
    """)
```

- `IF NOT EXISTS`: evita erro se a tabela já existir.
- `INTEGER PRIMARY KEY AUTOINCREMENT`: chave primária com incremento automático.
- `NOT NULL`: campo obrigatório.
- `UNIQUE`: valor não pode se repetir na tabela.

Os tipos principais no SQLite são: `INTEGER`, `REAL` (float), `TEXT`, `BLOB` (binário) e `NULL`.

### Inserindo dados (INSERT)

Usamos `INSERT INTO` para adicionar registros.

```python
with sqlite3.connect("clientes.db") as conn:
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO clientes (nome, email, idade) VALUES (?, ?, ?)",
        ("Ana Silva", "ana@email.com", 28)
    )
    # O ? é um placeholder que será substituído pelos valores da tupla
```

Para inserir vários registros de uma vez:

```python
dados = [
    ("Bruno Costa", "bruno@email.com", 35),
    ("Carla Mendes", "carla@email.com", 22),
]
cursor.executemany("INSERT INTO clientes (nome, email, idade) VALUES (?, ?, ?)", dados)
```

!!! warning "Nunca use concatenação de strings para montar SQL"
    Fazer `f"INSERT INTO clientes VALUES ('{nome}', '{email}', {idade})"` é perigoso e vulnerável a injeção de SQL. Sempre use placeholders `?` ou `:nome` para passar parâmetros.

### Consultando dados (SELECT)

O comando `SELECT` recupera registros. Os resultados podem ser obtidos com `fetchone()`, `fetchall()` ou iterando sobre o cursor.

```python
with sqlite3.connect("clientes.db") as conn:
    cursor = conn.cursor()

    # Seleciona todos os registros
    cursor.execute("SELECT * FROM clientes")
    todos = cursor.fetchall()
    for linha in todos:
        print(linha)  # Cada linha é uma tupla

    # Seleciona com filtro
    cursor.execute("SELECT nome, email FROM clientes WHERE idade >= ?", (30,))
    resultado = cursor.fetchall()
    print(resultado)
```

### Atualizando dados (UPDATE)

`UPDATE` modifica registros existentes. Sempre use `WHERE` para limitar quais registros serão afetados; caso contrário, todos serão alterados.

```python
with sqlite3.connect("clientes.db") as conn:
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE clientes SET idade = ? WHERE nome = ?",
        (29, "Ana Silva")
    )
    print(f"Registros afetados: {cursor.rowcount}")
```

### Excluindo dados (DELETE)

`DELETE FROM` remove registros. O `WHERE` também é crucial aqui.

```python
with sqlite3.connect("clientes.db") as conn:
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = ?", (3,))
    print(f"Registros excluídos: {cursor.rowcount}")
```

### Tratamento de exceções

Operações com banco de dados podem falhar (ex.: violação de chave única, tabela inexistente). Envolva em `try`/`except`:

```python
import sqlite3

try:
    with sqlite3.connect("clientes.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO clientes (nome, email, idade) VALUES (?, ?, ?)",
                       ("Ana Silva", "ana@email.com", 28))
except sqlite3.IntegrityError:
    print("Erro: e-mail duplicado.")
except sqlite3.Error as e:
    print(f"Erro no banco de dados: {e}")
```

### Estruturando o acesso ao banco em funções

Para manter o código organizado, encapsule as operações em funções:

```python
def criar_cliente(nome, email, idade):
    try:
        with sqlite3.connect("clientes.db") as conn:
            conn.execute(
                "INSERT INTO clientes (nome, email, idade) VALUES (?, ?, ?)",
                (nome, email, idade)
            )
        return True
    except sqlite3.IntegrityError:
        return False

def listar_clientes():
    with sqlite3.connect("clientes.db") as conn:
        return conn.execute("SELECT * FROM clientes").fetchall()
```

Essa separação é o primeiro passo para um módulo de persistência bem estruturado.

### Boas práticas

- Sempre use `with sqlite3.connect(...) as conn:` para garantir fechamento e transações controladas.
- Use parâmetros (`?` ou `:nome`) para evitar injeção de SQL.
- Defina a estrutura da tabela com `IF NOT EXISTS` no início do programa.
- Feche cursores se não usar `with` (com `with` o fechamento é automático).
- Trate exceções específicas (`IntegrityError`, `OperationalError`).
- Mantenha as operações de banco em funções ou classes separadas da interface gráfica.

## Exemplos

??? example "Exemplo 1: Criando tabela e inserindo dados"
    === "Código"
        ```python
        import sqlite3

        # Conexão com o banco (cria se não existir)
        with sqlite3.connect("exemplo.db") as conn:
            cursor = conn.cursor()

            # Cria a tabela produtos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS produtos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    preco REAL NOT NULL,
                    quantidade INTEGER DEFAULT 0
                )
            """)

            # Insere alguns produtos
            produtos = [
                ("Caneta", 2.50, 100),
                ("Caderno", 15.90, 50),
                ("Borracha", 1.20, 200),
            ]
            cursor.executemany(
                "INSERT INTO produtos (nome, preco, quantidade) VALUES (?, ?, ?)",
                produtos
            )

        print("Tabela criada e dados inseridos com sucesso.")
        ```

    === "Resultado"
        ```text
        Tabela criada e dados inseridos com sucesso.
        ```
        Um arquivo `exemplo.db` é gerado no diretório atual com os dados persistidos.

    === "Explicação"
        Usamos `CREATE TABLE IF NOT EXISTS` para garantir idempotência. `executemany` insere vários registros de uma só vez, o que é mais eficiente do que múltiplas chamadas a `execute`. O gerenciador `with` faz o commit automático.

??? example "Exemplo 2: Consultando com filtro e ordenação"
    === "Código"
        ```python
        import sqlite3

        def listar_produtos_em_falta(limite=50):
            with sqlite3.connect("exemplo.db") as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT nome, quantidade FROM produtos
                    WHERE quantidade < ?
                    ORDER BY quantidade ASC
                """, (limite,))
                return cursor.fetchall()

        resultado = listar_produtos_em_falta()
        print("Produtos com estoque abaixo de 50:")
        for nome, qtd in resultado:
            print(f"{nome}: {qtd} unidades")
        ```

    === "Resultado"
        ```text
        Produtos com estoque abaixo de 50:
        Caneta: 100 unidades
        Caderno: 50 unidades
        Borracha: 200 unidades
        ```
        *(Neste caso, nenhum está abaixo de 50, então a lista ficaria vazia se o limite fosse menor; ajuste o exemplo conforme os dados inseridos.)*

    === "Explicação"
        A função recebe um parâmetro (`limite`) e usa um placeholder `?` para comparar. A ordenação é feita com `ORDER BY`. Note que a consulta retorna uma lista de tuplas. Funções como essa facilitam a reutilização.

??? example "Exemplo 3: Atualização e exclusão com tratamento de erro"
    === "Código"
        ```python
        import sqlite3

        def atualizar_preco(produto_id, novo_preco):
            try:
                with sqlite3.connect("exemplo.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE produtos SET preco = ? WHERE id = ?",
                        (novo_preco, produto_id)
                    )
                    if cursor.rowcount == 0:
                        print(f"Nenhum produto com ID {produto_id} encontrado.")
                    else:
                        print(f"Preço do produto {produto_id} atualizado para R$ {novo_preco:.2f}")
            except sqlite3.Error as e:
                print(f"Erro: {e}")

        def excluir_produto(produto_id):
            try:
                with sqlite3.connect("exemplo.db") as conn:
                    conn.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
                    print("Produto excluído.")
            except sqlite3.Error as e:
                print(f"Erro: {e}")

        # Testes
        atualizar_preco(1, 2.99)
        excluir_produto(2)
        ```

    === "Resultado"
        ```text
        Preço do produto 1 atualizado para R$ 2.99
        Produto excluído.
        ```
        O arquivo `exemplo.db` reflete as alterações.

    === "Explicação"
        `cursor.rowcount` retorna o número de linhas afetadas pelo último comando. Isso permite verificar se a atualização atingiu algum registro. As operações são encapsuladas em funções e tratam exceções genéricas do SQLite, aumentando a robustez.

## Exercícios

### Básico (fixação)

1. Crie um banco de dados `biblioteca.db` com uma tabela `livros` contendo as colunas: `id` (chave primária, autoincremento), `titulo` (texto, obrigatório), `autor` (texto, obrigatório) e `ano` (inteiro). Insira três livros de sua preferência.
2. Escreva uma função `buscar_por_autor(autor)` que retorne todos os livros de um determinado autor. Teste com um dos autores inseridos.
3. Escreva uma função `atualizar_ano(titulo, novo_ano)` que atualiza o ano de um livro pelo título exato.

### Intermediário (aplicação)

1. Desenvolva um módulo `estoque.py` que gerencia um banco de dados SQLite para uma loja. A tabela `produtos` deve ter: `codigo` (chave primária, texto, único), `descricao`, `preco` (real), `quantidade` (inteiro). Implemente funções:
    - `adicionar_produto(codigo, descricao, preco, quantidade)`: retorna `True` se bem-sucedido, `False` se código duplicado.
    - `vender(codigo, quantidade_vendida)`: reduz a quantidade em estoque; se não houver estoque suficiente, retorna `False`.
    - `relatorio_estoque_baixo(limite)`: retorna lista de produtos com quantidade abaixo de `limite`.
   
   Utilize tratamento de exceções e placeholders.

### Avançado (desafio)

1. Crie um sistema de pedidos com duas tabelas relacionadas: `clientes` (`id`, `nome`, `email`) e `pedidos` (`id`, `id_cliente`, `data`, `valor_total`). A tabela `pedidos` deve ter uma chave estrangeira (`FOREIGN KEY`) referenciando `clientes(id)`. Implemente:
    - Criação das tabelas com `PRAGMA foreign_keys = ON`.
    - Função `criar_pedido(id_cliente, data, valor)`: insere um pedido; se o cliente não existir, levanta uma exceção personalizada `ClienteInexistenteError`.
    - Função `relatorio_pedidos_por_cliente(id_cliente)`: retorna todos os pedidos de um cliente.
   
   Teste as operações e demonstre o funcionamento da integridade referencial.

## Projeto Prático

### Migrando o Gerenciador de Tarefas para SQLite

Retome o Gerenciador de Tarefas desenvolvido nos módulos anteriores e substitua a persistência baseada em JSON por um banco de dados SQLite.

**Requisitos:**

- **Modelo de dados:** Crie uma tabela `tarefas` com as colunas:
    - `id` (`INTEGER PRIMARY KEY AUTOINCREMENT`)
    - `descricao` (`TEXT NOT NULL`)
    - `prioridade` (`TEXT NOT NULL`, valores: "alta", "média", "baixa")
    - `status` (`TEXT NOT NULL`, padrão "pendente")
    - `data_criacao` (`TEXT NOT NULL`, formato "YYYY-MM-DD")

- **Módulo de persistência (`persistencia_db.py`):**
    - Função `inicializar_banco()`: conecta ao banco `tarefas.db`, cria a tabela se não existir e ativa `PRAGMA foreign_keys = ON` (se usar chaves estrangeiras no futuro).
    - Função `adicionar_tarefa(descricao, prioridade, data)`: insere nova tarefa e retorna o ID gerado.
    - Função `listar_tarefas(status=None)`: retorna lista de dicionários com todas as tarefas; se status for informado, filtra.
    - Função `atualizar_status(id_tarefa, novo_status)`: atualiza status de uma tarefa, retornando `True` se o ID existir.
    - Função `remover_tarefa(id_tarefa)`: remove tarefa pelo ID.

- **Integração com a interface:**
    - Substitua as chamadas ao módulo `persistencia.py` (JSON) pelas novas funções. A interface (Tkinter ou CustomTkinter) deve continuar funcionando exatamente da mesma forma; apenas o backend muda.
    - A função `listar_tarefas` deve retornar dicionários com as mesmas chaves que antes (`id`, `descricao`, `prioridade`, `status`, `data_criacao`), garantindo compatibilidade.

- **Tratamento de exceções:**
    - Capture `sqlite3.Error` e exiba mensagens apropriadas via `messagebox` na interface.
    - Ao inicializar o banco, se o arquivo estiver corrompido, exiba um aviso e recrie a tabela (ou simplesmente encerre de forma graciosa).

**Bônus (opcional):**
- Adicione uma função `buscar_por_palavra_chave(palavra)` que use `LIKE` para pesquisar tarefas cuja descrição contenha o termo.
- Implemente ordenação por prioridade ou data diretamente na consulta SQL.

**Orientações de implementação:**
- Mantenha o código da interface separado do código de acesso a dados.
- Use `with sqlite3.connect(...)` em todas as funções.
- Lembre-se de que, após migrar, o arquivo `tarefas.json` não será mais utilizado. Você pode excluí-lo ou mantê-lo como backup.

Este projeto demonstra como uma mudança na camada de persistência pode ser feita de forma transparente para o resto da aplicação, uma das grandes vantagens da modularização.

## Resumo

Neste capítulo, você aprendeu que:

- Bancos de dados relacionais organizam informações em tabelas e usam SQL para manipulação.
- SQLite é um banco leve, sem servidor, integrado ao Python via módulo `sqlite3`.
- O CRUD consiste em `INSERT`, `SELECT`, `UPDATE` e `DELETE`.
- Parâmetros com `?` previnem injeção de SQL e devem sempre ser usados.
- O gerenciador de contexto `with` gerencia transações automaticamente (commit/rollback).
- Exceções como `sqlite3.IntegrityError` devem ser tratadas para garantir robustez.
- Encapsular operações de banco em funções mantém o código organizado e reutilizável.

A integração de SQLite eleva suas aplicações desktop a um novo patamar de profissionalismo, permitindo lidar com volumes maiores de dados, buscas complexas e integridade referencial.
