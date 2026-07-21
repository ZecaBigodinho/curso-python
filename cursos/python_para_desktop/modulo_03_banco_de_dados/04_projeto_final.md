# Projeto Final: Arquitetura Completa

## Objetivos

Ao final deste capítulo, você terá integrado todos os conhecimentos do curso em um projeto de arquitetura profissional. Especificamente, você aprenderá a:

- Estruturar um projeto Python desktop em diretórios com separação de responsabilidades (Model, View, Controller).
- Aplicar o padrão MVC (Model-View-Controller) adaptado para aplicações com Tkinter/CustomTkinter.
- Utilizar CustomTkinter para uma interface moderna e responsiva.
- Implementar a camada de persistência com SQLite, centralizando o acesso a dados em classes de modelo.
- Carregar configurações sensíveis de um arquivo `.env` com `python-dotenv`, garantindo segurança e portabilidade.
- Tratar erros de forma global, protegendo a interface e fornecendo feedback claro ao usuário.
- Empacotar a aplicação final com PyInstaller, gerando um executável independente para distribuição.
- Compreender a importância da modularização e da organização de código para manutenção e escalabilidade.

## Pré-requisitos

Este capítulo assume que você domina todos os tópicos anteriores do curso, incluindo:

- Python básico e intermediário (variáveis, funções, coleções, strings, exceções).
- Tkinter e CustomTkinter (widgets, layouts, eventos, variáveis de controle).
- Banco de dados SQLite e módulo `sqlite3` (CRUD, parâmetros, integridade).
- Variáveis de ambiente com `python-dotenv` e arquivo `.env`.
- Manipulação de arquivos e diretórios (`pathlib`, `os`).
- Princípios de modularização e importação de módulos.
- Uso básico de terminal para instalação de pacotes e execução de scripts.

Se algum desses temas ainda não está consolidado, revise os capítulos correspondentes antes de prosseguir.

## Motivação

Projetos reais de software não são escritos em um único arquivo com centenas de linhas. À medida que a complexidade aumenta, torna-se impossível manter o código organizado sem uma arquitetura bem definida. Imagine um sistema de controle de estoque, clientes e vendas: misturar interface gráfica, consultas SQL e regras de negócio em um só lugar transforma qualquer alteração em um pesadelo.

A arquitetura Model-View-Controller (MVC) oferece uma solução testada e aprovada. Ela separa a aplicação em três camadas:

- **Model (Modelo)**: gerencia os dados e a lógica de negócio (banco de dados, validações, regras).
- **View (Visão)**: cuida da interface gráfica, exibindo informações e capturando ações do usuário.
- **Controller (Controlador)**: faz a ponte, recebendo eventos da View, acionando o Model e atualizando a View.

Essa separação facilita manutenção, testes e colaboração em equipe. Embora o MVC seja frequentemente associado a aplicações web, ele se adapta perfeitamente ao desktop. Neste capítulo, vamos implementar um sistema completo — um **Gerenciador de Produtos** — utilizando essa arquitetura, junto com CustomTkinter, SQLite, variáveis de ambiente e, ao final, empacotaremos o projeto em um executável. Será o coroamento do seu aprendizado.

## Conteúdo

### Estrutura de diretórios proposta

Organizaremos o projeto da seguinte forma:

```text
gerenciador_produtos/
├── app.py                  # Ponto de entrada da aplicação
├── config.py               # Carrega configurações do .env
├── .env                    # Variáveis de ambiente (NÃO versionado)
├── .env.example            # Template para desenvolvedores
├── .gitignore
├── requirements.txt        # Dependências do projeto
├── models/
│   ├── __init__.py
│   ├── database.py         # Conexão e inicialização do SQLite
│   └── produto.py          # Classe Produto e operações CRUD
├── views/
│   ├── __init__.py
│   ├── main_view.py        # Janela principal e layout
│   └── widgets.py          # Componentes reutilizáveis (se necessário)
├── controllers/
│   ├── __init__.py
│   └── produto_controller.py  # Controlador para operações de produto
└── utils/
    ├── __init__.py
    └── exceptions.py       # Exceções personalizadas
```

Essa estrutura pode ser expandida com novas entidades (clientes, vendas) seguindo o mesmo padrão. O arquivo `app.py` é mínimo: cria a aplicação e inicia o controlador principal.

### Camada de Configuração (config.py e .env)

Seguindo as boas práticas do capítulo anterior, centralizamos as configurações em `config.py`:

```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Caminho do banco de dados (com valor padrão)
DB_PATH = os.getenv("DB_PATH", "produtos.db")

# Tema da interface
TEMA = os.getenv("TEMA", "dark")
COR_TEMA = os.getenv("COR_TEMA", "blue")

# Título da aplicação
TITULO_APP = os.getenv("TITULO_APP", "Gerenciador de Produtos")

# Outras configurações podem ser adicionadas
```

O arquivo `.env` conterá:

```env
DB_PATH=produtos.db
TEMA=dark
COR_TEMA=dark-blue
TITULO_APP=Gerenciador de Produtos
```

E o `.env.example` orientará outros desenvolvedores.

### Camada Model: banco de dados e entidades

Em `models/database.py`, gerenciamos a conexão com SQLite e a criação das tabelas:

```python
# models/database.py
import sqlite3
from config import DB_PATH

def obter_conexao():
    """Retorna uma conexão com o banco de dados."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def inicializar_banco():
    """Cria as tabelas se não existirem."""
    with obter_conexao() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT,
                preco REAL NOT NULL CHECK(preco >= 0),
                quantidade INTEGER NOT NULL DEFAULT 0
            );
        """)
```

Em `models/produto.py`, definimos a classe `Produto` e as operações CRUD:

```python
# models/produto.py
from models.database import obter_conexao

class Produto:
    def __init__(self, id=None, nome="", descricao="", preco=0.0, quantidade=0):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.quantidade = quantidade

    @classmethod
    def listar_todos(cls):
        """Retorna uma lista de objetos Produto."""
        with obter_conexao() as conn:
            rows = conn.execute("SELECT * FROM produtos ORDER BY nome").fetchall()
            return [cls(**dict(row)) for row in rows]

    @classmethod
    def buscar_por_id(cls, produto_id):
        with obter_conexao() as conn:
            row = conn.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,)).fetchone()
            return cls(**dict(row)) if row else None

    def salvar(self):
        """Insere ou atualiza o produto no banco."""
        with obter_conexao() as conn:
            if self.id:
                conn.execute(
                    "UPDATE produtos SET nome=?, descricao=?, preco=?, quantidade=? WHERE id=?",
                    (self.nome, self.descricao, self.preco, self.quantidade, self.id)
                )
            else:
                cursor = conn.execute(
                    "INSERT INTO produtos (nome, descricao, preco, quantidade) VALUES (?, ?, ?, ?)",
                    (self.nome, self.descricao, self.preco, self.quantidade)
                )
                self.id = cursor.lastrowid

    def excluir(self):
        """Remove o produto do banco."""
        if self.id:
            with obter_conexao() as conn:
                conn.execute("DELETE FROM produtos WHERE id = ?", (self.id,))
```

!!! note "Model com classe vs. dicionários"
    Utilizar uma classe enriquece a legibilidade e permite adicionar métodos de validação ou regras de negócio posteriormente. O uso de `@classmethod` para listar e buscar permite instanciar objetos diretamente.

### Camada View: interface com CustomTkinter

`views/main_view.py` contém a construção da janela principal, frames e widgets. A View **nunca acessa o banco de dados diretamente**; ela apenas exibe dados e captura eventos, delegando ao Controller.

```python
# views/main_view.py
import customtkinter as ctk
from tkinter import ttk, messagebox

class MainView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gerenciador de Produtos")
        self.geometry("800x500")
        self._criar_widgets()

    def _criar_widgets(self):
        # Frame de formulário
        form = ctk.CTkFrame(self)
        form.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(form, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_nome = ctk.CTkEntry(form, width=200)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(form, text="Preço:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.entry_preco = ctk.CTkEntry(form, width=100)
        self.entry_preco.grid(row=0, column=3, padx=5, pady=5)

        ctk.CTkLabel(form, text="Qtd:").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.entry_quantidade = ctk.CTkEntry(form, width=60)
        self.entry_quantidade.grid(row=0, column=5, padx=5, pady=5)

        # Botões (comandos serão vinculados pelo Controller)
        self.btn_adicionar = ctk.CTkButton(form, text="Adicionar")
        self.btn_adicionar.grid(row=0, column=6, padx=10, pady=5)
        self.btn_atualizar = ctk.CTkButton(form, text="Atualizar", state="disabled")
        self.btn_atualizar.grid(row=0, column=7, padx=5, pady=5)
        self.btn_excluir = ctk.CTkButton(form, text="Excluir", state="disabled")
        self.btn_excluir.grid(row=0, column=8, padx=5, pady=5)
        self.btn_limpar = ctk.CTkButton(form, text="Limpar")
        self.btn_limpar.grid(row=0, column=9, padx=5, pady=5)

        # Treeview para listagem
        colunas = ("id", "nome", "preco", "quantidade")
        self.tree = ttk.Treeview(self, columns=colunas, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("preco", text="Preço (R$)")
        self.tree.heading("quantidade", text="Qtd")
        self.tree.column("id", width=50)
        self.tree.column("preco", width=100)
        self.tree.column("quantidade", width=80)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Barra de rolagem
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
```

A View expõe os widgets como atributos públicos para que o Controller possa acessá-los e associar eventos. Outra abordagem é usar métodos `set_controller` e chamar callbacks; aqui, faremos a ligação diretamente.

### Camada Controller: a orquestração

O `produto_controller.py` instancia a View e o Model, conecta eventos e implementa a lógica de interação:

```python
# controllers/produto_controller.py
from tkinter import messagebox
import sqlite3
from models.produto import Produto
from views.main_view import MainView

class ProdutoController:
    def __init__(self):
        self.view = MainView()
        self._conectar_eventos()
        self._atualizar_lista()
        self.id_edicao = None

    def _conectar_eventos(self):
        self.view.btn_adicionar.configure(command=self.adicionar)
        self.view.btn_atualizar.configure(command=self.atualizar)
        self.view.btn_excluir.configure(command=self.excluir)
        self.view.btn_limpar.configure(command=self.limpar)
        self.view.tree.bind("<<TreeviewSelect>>", self._ao_selecionar)

    def _ao_selecionar(self, event):
        selecionado = self.view.tree.selection()
        if selecionado:
            valores = self.view.tree.item(selecionado)["values"]
            self.id_edicao = valores[0]
            self.view.entry_nome.delete(0, "end")
            self.view.entry_nome.insert(0, valores[1])
            self.view.entry_preco.delete(0, "end")
            self.view.entry_preco.insert(0, valores[2])
            self.view.entry_quantidade.delete(0, "end")
            self.view.entry_quantidade.insert(0, valores[3])
            self.view.btn_atualizar.configure(state="normal")
            self.view.btn_excluir.configure(state="normal")
            self.view.btn_adicionar.configure(state="disabled")
        else:
            self.limpar()

    def _validar_campos(self):
        nome = self.view.entry_nome.get().strip()
        preco_str = self.view.entry_preco.get().strip()
        qtd_str = self.view.entry_quantidade.get().strip()
        if not nome:
            raise ValueError("Nome do produto é obrigatório.")
        try:
            preco = float(preco_str)
            if preco < 0:
                raise ValueError
        except ValueError:
            raise ValueError("Preço deve ser um número positivo.")
        try:
            qtd = int(qtd_str)
            if qtd < 0:
                raise ValueError
        except ValueError:
            raise ValueError("Quantidade deve ser um número inteiro não negativo.")
        return nome, preco, qtd

    def adicionar(self):
        try:
            nome, preco, qtd = self._validar_campos()
            produto = Produto(nome=nome, preco=preco, quantidade=qtd)
            produto.salvar()
            self._atualizar_lista()
            self.limpar()
            messagebox.showinfo("Sucesso", "Produto adicionado com sucesso.")
        except ValueError as e:
            messagebox.showerror("Erro de validação", str(e))
        except sqlite3.Error as e:
            messagebox.showerror("Erro no banco de dados", f"Não foi possível salvar.\n{e}")

    def atualizar(self):
        if not self.id_edicao:
            return
        try:
            nome, preco, qtd = self._validar_campos()
            produto = Produto(id=self.id_edicao, nome=nome, preco=preco, quantidade=qtd)
            produto.salvar()
            self._atualizar_lista()
            self.limpar()
            messagebox.showinfo("Sucesso", "Produto atualizado.")
        except ValueError as e:
            messagebox.showerror("Erro de validação", str(e))
        except sqlite3.Error as e:
            messagebox.showerror("Erro no banco de dados", str(e))

    def excluir(self):
        if not self.id_edicao:
            return
        if messagebox.askyesno("Confirmar", "Excluir o produto selecionado?"):
            try:
                produto = Produto(id=self.id_edicao)
                produto.excluir()
                self._atualizar_lista()
                self.limpar()
                messagebox.showinfo("Sucesso", "Produto excluído.")
            except sqlite3.Error as e:
                messagebox.showerror("Erro", str(e))

    def limpar(self):
        self.view.entry_nome.delete(0, "end")
        self.view.entry_preco.delete(0, "end")
        self.view.entry_quantidade.delete(0, "end")
        self.id_edicao = None
        self.view.btn_adicionar.configure(state="normal")
        self.view.btn_atualizar.configure(state="disabled")
        self.view.btn_excluir.configure(state="disabled")
        self.view.tree.selection_remove(self.view.tree.selection())

    def _atualizar_lista(self):
        for item in self.view.tree.get_children():
            self.view.tree.delete(item)
        for produto in Produto.listar_todos():
            self.view.tree.insert("", "end", values=(
                produto.id,
                produto.nome,
                f"{produto.preco:.2f}",
                produto.quantidade
            ))

    def iniciar(self):
        self.view.mainloop()
```

### Tratamento de erros centralizado

Acrescentamos uma camada extra de segurança capturando exceções específicas (`ValueError` para validação, `sqlite3.Error` para banco) e exibindo mensagens adequadas. Poderíamos também criar um decorador para capturar erros e logá-los, mas o padrão atual já é robusto.

### Empacotamento com PyInstaller

Para distribuir a aplicação como um executável, utilizamos o PyInstaller. Primeiro, instale:

```bash
pip install pyinstaller
```

Dentro da pasta do projeto, execute:

```bash
pyinstaller --onefile --windowed --name "GerenciadorProdutos" app.py
```

- `--onefile`: gera um único arquivo executável.
- `--windowed`: evita abrir uma janela de console no Windows.
- `--name`: define o nome do executável.

Isso criará uma pasta `dist` contendo o executável. No entanto, o arquivo `.env` não será incluído automaticamente. Precisamos de uma estratégia:

1. **Opção recomendada**: não empacotar o `.env`; em vez disso, solicitar as configurações na primeira execução ou usar valores padrão. O aplicativo pode criar um `.env` se não existir, com opções básicas.
2. **Incluir o `.env` como dado**: adicionar `--add-data ".env;."` no Windows ou `--add-data ".env:."` no Linux/macOS. Entretanto, isso incluiria as credenciais do desenvolvedor, o que é perigoso.

Para nosso caso, podemos modificar ligeiramente o `config.py` para aceitar a ausência do `.env` e carregar padrões, ou buscar o `.env` no diretório do executável. Uma solução elegante é:

```python
import sys
from pathlib import Path
from dotenv import load_dotenv

# Determina o caminho base (funciona tanto em desenvolvimento quanto no executável)
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).parent

load_dotenv(BASE_DIR / ".env")
```

E não empacotar o `.env`. Ao executar pela primeira vez, o programa pode mostrar uma janela de configuração ou criar um `.env` vazio.

No nosso projeto, vamos adotar a abordagem de não incluir o `.env` no pacote; os valores padrão em `config.py` garantem o funcionamento básico.

!!! tip "Testando o executável"
    Após gerar o executável, sempre teste em uma máquina limpa (ou máquina virtual) para verificar se todas as dependências foram incluídas. O PyInstaller geralmente detecta imports automaticamente, mas bibliotecas como `customtkinter` podem precisar de ajustes. Consulte a documentação do PyInstaller se houver problemas.

### Integrando tudo: o arquivo app.py

```python
# app.py
from models.database import inicializar_banco
from controllers.produto_controller import ProdutoController

if __name__ == "__main__":
    inicializar_banco()
    app = ProdutoController()
    app.iniciar()
```

Simples e claro: a criação da aplicação é delegada ao Controller, que por sua vez cria a View e gerencia as interações.

## Exemplos

??? example "Exemplo 1: Estrutura de diretórios e imports"
    === "Estrutura"
        ```text
        gerenciador_produtos/
        ├── app.py
        ├── config.py
        ├── models/
        │   ├── __init__.py
        │   ├── database.py
        │   └── produto.py
        ├── views/
        │   ├── __init__.py
        │   └── main_view.py
        └── controllers/
            ├── __init__.py
            └── produto_controller.py
        ```

    === "Explicação"
        Cada pacote (`models`, `views`, `controllers`) tem um arquivo `__init__.py` vazio para ser reconhecido como módulo Python. Os imports seguem a hierarquia: `controllers` importa de `views` e `models`; `models` importa de `config`; `views` não importa de `models` nem de `controllers`.

??? example "Exemplo 2: Validando e salvando produto"
    === "Código (trecho do controller)"
        ```python
        def adicionar(self):
            try:
                nome, preco, qtd = self._validar_campos()
                produto = Produto(nome=nome, preco=preco, quantidade=qtd)
                produto.salvar()
                # Atualiza a lista e limpa formulário...
            except ValueError as e:
                messagebox.showerror("Erro", str(e))
        ```

    === "Resultado"
        Se o campo "Preço" estiver vazio ou contiver letras, a validação levanta `ValueError` e uma caixa de erro é exibida ao usuário, sem travar a aplicação.

    === "Explicação"
        A validação ocorre no Controller, que conhece as regras de negócio (preço positivo, nome obrigatório). O Model recebe dados já validados.

??? example "Exemplo 3: Empacotamento com PyInstaller"
    === "Comando"
        ```bash
        pyinstaller --onefile --windowed --name "GerenciadorProdutos" app.py
        ```

    === "Saída esperada"
        O PyInstaller analisa os imports, coleta bibliotecas e gera `dist/GerenciadorProdutos.exe` (no Windows) ou executável equivalente no Linux/macOS.

    === "Explicação"
        `--windowed` suprime o console. Se houver erros de módulo não encontrado, podemos usar `--hidden-import`. Para CustomTkinter, geralmente não é necessário, mas podemos adicionar `--hidden-import customtkinter` por segurança.

## Exercícios

### Básico (fixação)

1. Reproduza a estrutura de diretórios mostrada e implemente o Gerenciador de Produtos conforme o código fornecido. Execute e teste todas as operações CRUD.
2. Altere o esquema de cores no `.env` para `green` e o tema para `light`. Verifique se a interface reflete as mudanças após reiniciar.
3. Adicione uma coluna `descricao` na Treeview e no formulário, permitindo visualizar e editar a descrição do produto.

### Intermediário (aplicação)

1. Crie uma nova entidade `Categoria` com tabela `categorias` (id, nome). Relacione `produto` com `categoria` (chave estrangeira). Atualize a interface para selecionar a categoria em um `CTkOptionMenu`. Implemente as classes Model, View e Controller para Categoria.
2. Adicione uma funcionalidade de busca por nome na listagem de produtos: um campo de entrada e botão que filtram a Treeview usando `SELECT ... WHERE nome LIKE ?`. Lembre-se de recarregar a lista completa ao limpar a busca.

### Avançado (desafio)

1. Empacote o projeto com PyInstaller. Teste o executável em outro computador (ou máquina virtual) sem Python instalado. Resolva eventuais problemas de dependências. Inclua a biblioteca `customtkinter` explicitamente se necessário.
2. Implemente um sistema de logs usando o módulo `logging` do Python. Configure-o via `.env` (nível de log, arquivo de saída). Substitua os `print` e adicione logs em pontos estratégicos (erros de banco, ações do usuário). Exiba as mensagens de log também em uma barra de status na interface.

## Projeto Prático

### Sistema de Controle de Estoque com Arquitetura MVC

Vamos projetar um sistema completo de controle de estoque, aplicando tudo o que aprendemos. O escopo será:

- **Entidades**: Produto, Categoria, Movimentação (entrada/saída de estoque).
- **Funcionalidades**:
    - CRUD de produtos e categorias.
    - Registro de movimentações, com data e quantidade.
    - Tela de dashboard com resumo (total de produtos, valor em estoque, movimentações recentes).
    - Abas usando `CTkTabview`.
- **Arquitetura**: MVC rigorosa.
- **Persistência**: SQLite com chaves estrangeiras e integridade referencial.
- **Configuração**: `.env` para caminho do banco, tema e título.
- **Tratamento de erros**: validações na camada de modelo, exceções personalizadas.
- **Empacotamento**: executável final com PyInstaller, sem console, com teste em máquina limpa.

**Etapas:**

1. **Definição da estrutura:**
    ```text
    estoque_app/
    ├── app.py
    ├── config.py
    ├── .env
    ├── .env.example
    ├── models/
    │   ├── database.py
    │   ├── produto.py
    │   ├── categoria.py
    │   └── movimentacao.py
    ├── views/
    │   ├── main_view.py
    │   ├── produto_view.py
    │   ├── categoria_view.py
    │   └── dashboard_view.py
    ├── controllers/
    │   ├── produto_controller.py
    │   ├── categoria_controller.py
    │   └── dashboard_controller.py
    └── utils/
        ├── exceptions.py
        └── logger.py
    ```

2. **Modelos**:
    - `database.py`: conexão, inicialização de todas as tabelas com FOREIGN KEY.
    - `produto.py`: classe Produto com CRUD e método `valor_total_estoque()`.
    - `categoria.py`: classe Categoria.
    - `movimentacao.py`: classe Movimentacao com atributos id, produto_id, tipo (entrada/saída), quantidade, data.

3. **Views**:
    - `main_view.py`: janela principal com `CTkTabview` contendo abas "Dashboard", "Produtos", "Categorias", "Movimentações".
    - Cada aba é um frame (poderia ser uma classe separada) construído na própria view ou importado.
    - Uso de `CTkFrame`, `CTkEntry`, `CTkButton`, Treeview (dentro de frames específicos).

4. **Controllers**:
    - Um controller para cada entidade, responsável por ligar eventos da view correspondente e chamar métodos do modelo.
    - `DashboardController`: atualiza labels com resumo, consultando os modelos.

5. **Tratamento de erros**:
    - Exceções personalizadas como `EstoqueInsuficienteError`, `CategoriaNaoEncontradaError`.
    - Captura genérica nos controllers para exibir messagebox.

6. **Empacotamento**:
    - Após testes, rodar PyInstaller com `--add-data` para incluir a pasta models, views, etc., se necessário. Normalmente o `--onefile` já embute tudo.
    - Criar um instalador com NSIS ou Inno Setup (opcional, mas mencionado).

**Cronograma sugerido:** 2 a 3 dias de trabalho dedicado. O importante é a organização e a aplicação do padrão MVC.

Esse projeto será o seu cartão de visitas como desenvolvedor Python desktop. Capriche na documentação e nos comentários.

## Resumo

Neste capítulo, você concluiu a jornada de aprendizado integrando todos os pilares do desenvolvimento desktop com Python:

- **Arquitetura MVC**: separação clara entre dados (Model), interface (View) e controle (Controller), facilitando manutenção e escalabilidade.
- **CustomTkinter**: interface moderna com temas e widgets estilizados.
- **SQLite**: persistência robusta com modelo orientado a objetos, incluindo chaves estrangeiras e validações.
- **Variáveis de ambiente**: segurança e portabilidade com `.env` e `python-dotenv`.
- **Tratamento de erros**: feedback amigável ao usuário e estabilidade da aplicação.
- **Empacotamento com PyInstaller**: geração de executáveis para distribuição profissional.

Agora você detém o conhecimento necessário para projetar, implementar e distribuir aplicações desktop completas em Python. O céu é o limite!
