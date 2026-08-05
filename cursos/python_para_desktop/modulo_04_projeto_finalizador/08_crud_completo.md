# 08 — CRUD Completo

## 🎯 Objetivo

Neste capítulo você vai transformar o cadastro de alunos em um CRUD completo — Create, Read, Update e Delete — com seleção na tabela, edição de registros, exclusão com confirmação e busca com filtro.

Ao final, você terá:

- O módulo `database/operacoes.py` centralizando todas as operações SQL
- Seleção de um aluno no Treeview preenchendo automaticamente o formulário
- Botão Editar que atualiza o registro selecionado no banco
- Botão Excluir que remove o registro com confirmação de segurança
- Campo de Busca por nome usando LIKE para filtrar a listagem
- Botão Novo que limpa o formulário e prepara para uma nova inserção
- Feedback com messagebox em todas as operações

## 📍 Contextualização

No Capítulo 07, você conectou o sistema ao SQLite. O cadastro passou a persistir dados — alunos sobrevivem ao fechamento do programa. Mas o sistema ainda é "cego": você só insere e lista. Não é possível corrigir um nome digitado errado, remover um aluno que saiu da escola ou buscar alguém específico no meio de dezenas de registros.

Agora você completará o ciclo. Um sistema de verdade permite gerenciar os dados — e gerenciar significa executar as quatro operações fundamentais: Criar, Ler, Atualizar e Deletar (CRUD). Você também aprenderá a selecionar uma linha na tabela e ver seus dados no formulário, um padrão de usabilidade presente em praticamente todos os softwares empresariais.

**Progresso do Sistema:**

```text
✅ Capítulo 01 — Introdução e Planejamento
✅ Capítulo 02 — Arquitetura do Sistema
✅ Capítulo 03 — Tela de Login
✅ Capítulo 04 — Menu Principal
✅ Capítulo 05 — Múltiplas Janelas
✅ Capítulo 06 — Cadastro de Alunos
✅ Capítulo 07 — SQLite
🔨 CRUD Completo ← VOCÊ ESTÁ AQUI
⬜ Banco em Nuvem
⬜ Integração e Testes
⬜ Refatoração e Entrega
```

## ✅ Resultado Esperado

A tela de cadastro ganhará novos botões e comportamentos. Visualmente:

```text
┌──────────────────────────────────────────────────────┐
│  Cadastro de Alunos                              _ □ X│
│                                                      │
│  ┌─ Dados do Aluno ────────────────────────────────┐ │
│  │  Nome:  [Maria Souza__________]                │ │
│  │  Idade: [14]  Turma: [9B▾]                     │ │
│  │                                                 │ │
│  │  [💾 Salvar] [✏️ Editar] [🗑️ Excluir]          │ │
│  │  [🧹 Limpar]                                    │ │
│  └─────────────────────────────────────────────────┘ │
│                                                      │
│  ┌─ Busca ─────────────────────────────────────────┐ │
│  │  Buscar: [______________] [🔍 Buscar]           │ │
│  └─────────────────────────────────────────────────┘ │
│                                                      │
│  ┌─ Alunos Cadastrados ────────────────────────────┐ │
│  │  Nome          │ Idade │ Turma                  │ │
│  │  ──────────────┼───────┼──────                  │ │
│  │  João Silva    │ 15    │ 9A    ← selecionado    │ │
│  │  Maria Souza   │ 14    │ 9B                     │ │
│  │                                     ▴           │ │
│  │                                     ▾           │ │
│  └─────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────┘
```

Comportamento esperado:

- Ao clicar em uma linha da tabela, os dados preenchem o formulário
- O botão Salvar insere um novo registro (modo inserção)
- O botão Editar atualiza o registro selecionado no banco (modo edição)
- O botão Excluir pergunta confirmação e remove o registro
- O botão Limpar reseta o formulário para o modo de inserção
- O campo de Busca filtra a tabela por nome (usando LIKE)
- Botões Editar e Excluir só ficam ativos quando há uma linha selecionada

Arquivos criados ou modificados:

| Arquivo | Ação |
|---|---|
| `database/operacoes.py` | Novo — funções CRUD centralizadas |
| `controllers/aluno.py` | Modificado — agora usa operacoes.py |
| `views/cadastro.py` | Modificado — novos botões, bind de seleção, busca |

## 💻 Implementação Guiada

### Passo 1 — Centralizando as operações SQL

Atualmente, as queries SQL estão espalhadas no controller `aluno.py`. Vamos extraí-las para um módulo dedicado, seguindo o princípio de responsabilidade única: o controller chama as operações, mas não escreve SQL.

Crie o arquivo `database/operacoes.py`:

```python
# ======================================================================
# operacoes.py — Operações CRUD no Banco de Dados
# ======================================================================
# Eu centralizo todas as queries SQL do sistema.
# O controller me chama — eu converso com o banco.
# ======================================================================

from database.conexao import conectar


def inserir_aluno(nome, idade, turma):
    """
    Eu insiro um novo aluno na tabela 'alunos'.

    Parâmetros:
        nome: string
        idade: int
        turma: string

    Retorno:
        int: o id do registro inserido (lastrowid)
    """
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO alunos (nome, idade, turma)
            VALUES (?, ?, ?)
        """, (nome, idade, turma))
        conn.commit()
        # Retorno o id gerado automaticamente pelo banco.
        return cursor.lastrowid


def listar_alunos(filtro_nome=None):
    """
    Eu busco todos os alunos, com opção de filtrar por nome.

    Parâmetros:
        filtro_nome: string opcional — se fornecida, filtro com LIKE

    Retorno:
        list de dict — cada dict contém id, nome, idade, turma
    """
    with conectar() as conn:
        cursor = conn.cursor()
        if filtro_nome:
            # Uso LIKE com % para busca parcial (começa com o texto).
            cursor.execute("""
                SELECT * FROM alunos
                WHERE nome LIKE ?
                ORDER BY nome
            """, (f"{filtro_nome}%",))
        else:
            cursor.execute("SELECT * FROM alunos ORDER BY nome")
        return [dict(aluno) for aluno in cursor.fetchall()]


def atualizar_aluno(id_aluno, nome, idade, turma):
    """
    Eu atualizo os dados de um aluno existente.

    Parâmetros:
        id_aluno: int — identificador do registro
        nome: string
        idade: int
        turma: string
    """
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE alunos
            SET nome = ?, idade = ?, turma = ?
            WHERE id = ?
        """, (nome, idade, turma, id_aluno))
        conn.commit()


def excluir_aluno(id_aluno):
    """
    Eu removo um aluno do banco de dados.

    Parâmetros:
        id_aluno: int — identificador do registro a ser removido
    """
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM alunos WHERE id = ?", (id_aluno,))
        conn.commit()


def contar_alunos(filtro_nome=None):
    """
    Eu retorno a quantidade total de alunos cadastrados.

    Parâmetros:
        filtro_nome: string opcional para contar apenas resultados filtrados

    Retorno:
        int: quantidade de registros
    """
    with conectar() as conn:
        cursor = conn.cursor()
        if filtro_nome:
            cursor.execute(
                "SELECT COUNT(*) FROM alunos WHERE nome LIKE ?",
                (f"{filtro_nome}%",)
            )
        else:
            cursor.execute("SELECT COUNT(*) FROM alunos")
        return cursor.fetchone()[0]
```

!!! tip "Dica Profissional"
    Centralizar queries em um módulo de operações facilita a manutenção. Se um dia você precisar alterar a estrutura da tabela ou migrar para outro banco, todas as mudanças ficam concentradas aqui. Os controllers nem precisam saber qual banco está sendo usado.

### Passo 2 — Refatorando o Controller

Agora o controller `aluno.py` se torna uma camada fina — ele apenas traduz as chamadas da View para o módulo de operações.

Substitua o conteúdo de `controllers/aluno.py`:

```python
# ======================================================================
# aluno.py — Controlador de Alunos (refatorado)
# ======================================================================
# Eu sou a ponte entre a View e as operações do banco.
# Minha responsabilidade é coordenar — não escrevo SQL diretamente.
# ======================================================================

from database.operacoes import (
    inserir_aluno,
    listar_alunos as listar_alunos_db,
    atualizar_aluno as atualizar_aluno_db,
    excluir_aluno as excluir_aluno_db,
    contar_alunos as contar_alunos_db,
)


def salvar_aluno(nome, idade, turma):
    """
    Eu insiro um novo aluno e retorno seus dados.
    """
    id_gerado = inserir_aluno(nome, idade, turma)
    return {"id": id_gerado, "nome": nome, "idade": idade, "turma": turma}


def listar_alunos(filtro_nome=None):
    """
    Eu retorno a lista de alunos, opcionalmente filtrada.
    """
    return listar_alunos_db(filtro_nome)


def editar_aluno(id_aluno, nome, idade, turma):
    """
    Eu atualizo os dados de um aluno existente.
    """
    atualizar_aluno_db(id_aluno, nome, idade, turma)


def remover_aluno(id_aluno):
    """
    Eu removo um aluno do sistema.
    """
    excluir_aluno_db(id_aluno)


def contar_alunos(filtro_nome=None):
    """
    Eu retorno o total de alunos.
    """
    return contar_alunos_db(filtro_nome)
```

!!! note "Renomeação de imports"
    Usei `as` para renomear as funções importadas e evitar conflito com os nomes das funções do controller. Isso é opcional, mas demonstra uma técnica útil quando nomes colidem.

### Passo 3 — Atualizando a View: bind de seleção no Treeview

Abra `views/cadastro.py`. Vamos fazer uma reforma significativa — novos botões, bind de seleção e campo de busca.

Substitua completamente o conteúdo de `views/cadastro.py` pelo código abaixo. Ele parte do que já tínhamos e adiciona as funcionalidades CRUD.

```python
# ======================================================================
# cadastro.py — Tela de Cadastro de Alunos (CRUD Completo)
# ======================================================================
# Eu agora suporto todas as operações: Inserir, Listar, Editar, Excluir.
# Também ofereço busca por nome para filtrar a tabela.
# ======================================================================

import tkinter as tk
from tkinter import ttk, messagebox
from utils.helpers import centralizar_janela
from controllers.aluno import (
    salvar_aluno,
    listar_alunos,
    editar_aluno,
    remover_aluno,
    contar_alunos,
)


# ---------- VARIÁVEL DE CONTROLE ----------
# Eu guardo o id do aluno atualmente selecionado para edição.
# Se for None, estamos no "modo inserção".
id_selecionado = None


def abrir_janela_cadastro(janela_pai):
    """
    Eu abro a janela de cadastro como Toplevel com CRUD completo.
    """
    global id_selecionado
    id_selecionado = None  # Reseta ao abrir a janela

    # ---------- JANELA ----------
    janela = tk.Toplevel(janela_pai)
    janela.title("Cadastro de Alunos")
    centralizar_janela(janela, 780, 600)
    janela.resizable(False, False)
    janela.configure(bg="#f5f6fa")
    janela.protocol("WM_DELETE_WINDOW", janela.destroy)

    # ---------- FRAME DO FORMULÁRIO ----------
    frame_form = tk.LabelFrame(
        janela, text=" Dados do Aluno ", font=("Arial", 12, "bold"),
        bg="#ffffff", fg="#2c3e50", bd=2, relief=tk.GROOVE, padx=15, pady=15
    )
    frame_form.pack(fill=tk.X, padx=20, pady=(20, 5))

    # ---- Campo Nome ----
    tk.Label(frame_form, text="Nome:", font=("Arial", 11),
             bg="#ffffff", fg="#333333").grid(row=0, column=0, sticky="w", pady=(0, 5))
    entry_nome = tk.Entry(frame_form, font=("Arial", 12), width=35, bd=2, relief=tk.SOLID)
    entry_nome.grid(row=0, column=1, columnspan=3, sticky="ew", padx=(10, 0), pady=(0, 5))
    entry_nome.focus_set()

    # ---- Campo Idade ----
    tk.Label(frame_form, text="Idade:", font=("Arial", 11),
             bg="#ffffff", fg="#333333").grid(row=1, column=0, sticky="w", pady=(5, 5))
    entry_idade = tk.Entry(frame_form, font=("Arial", 12), width=8, bd=2, relief=tk.SOLID)
    entry_idade.grid(row=1, column=1, sticky="w", padx=(10, 20), pady=(5, 5))

    # ---- Campo Turma ----
    tk.Label(frame_form, text="Turma:", font=("Arial", 11),
             bg="#ffffff", fg="#333333").grid(row=1, column=2, sticky="w", pady=(5, 5))
    turmas_disponiveis = [
        "6A","6B","7A","7B","8A","8B","9A","9B","1A","1B","2A","2B","3A","3B"
    ]
    combo_turma = ttk.Combobox(
        frame_form, values=turmas_disponiveis, font=("Arial", 12),
        width=6, state="readonly"
    )
    combo_turma.grid(row=1, column=3, sticky="w", padx=(10, 0), pady=(5, 5))
    combo_turma.set("")

    frame_form.columnconfigure(1, weight=1)

    # ---------- FRAME DE BOTÕES ----------
    frame_botoes = tk.Frame(frame_form, bg="#ffffff")
    frame_botoes.grid(row=2, column=0, columnspan=4, pady=(15, 0))

    # ---------- FRAME DE BUSCA ----------
    frame_busca = tk.LabelFrame(
        janela, text=" Busca ", font=("Arial", 11, "bold"),
        bg="#ffffff", fg="#2c3e50", bd=2, relief=tk.GROOVE, padx=15, pady=10
    )
    frame_busca.pack(fill=tk.X, padx=20, pady=(10, 5))

    tk.Label(frame_busca, text="Buscar por nome:", font=("Arial", 11),
             bg="#ffffff", fg="#333333").pack(side=tk.LEFT)
    entry_busca = tk.Entry(frame_busca, font=("Arial", 12), width=25, bd=2, relief=tk.SOLID)
    entry_busca.pack(side=tk.LEFT, padx=(10, 10))

    # ---------- FRAME DA LISTAGEM ----------
    frame_lista = tk.LabelFrame(
        janela, text=" Alunos Cadastrados ", font=("Arial", 12, "bold"),
        bg="#ffffff", fg="#2c3e50", bd=2, relief=tk.GROOVE, padx=15, pady=15
    )
    frame_lista.pack(fill=tk.BOTH, expand=True, padx=20, pady=(5, 20))

    # ---------- TREEVIEW ----------
    colunas = ("nome", "idade", "turma")
    tree = ttk.Treeview(frame_lista, columns=colunas, show="headings", height=10)
    tree.heading("nome", text="Nome")
    tree.heading("idade", text="Idade")
    tree.heading("turma", text="Turma")
    tree.column("nome", width=320, anchor="w")
    tree.column("idade", width=80, anchor="center")
    tree.column("turma", width=80, anchor="center")

    scrollbar = ttk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")
    frame_lista.rowconfigure(0, weight=1)
    frame_lista.columnconfigure(0, weight=1)

    # ===== FUNÇÕES AUXILIARES =====

    def atualizar_tabela(filtro_nome=None):
        """Eu recarrego a tabela com os dados do banco."""
        for item in tree.get_children():
            tree.delete(item)
        for aluno in listar_alunos(filtro_nome):
            tree.insert(
                "", tk.END,
                iid=aluno["id"],
                values=(aluno["nome"], aluno["idade"], aluno["turma"])
            )
        total = contar_alunos(filtro_nome)
        frame_lista.config(text=f" Alunos Cadastrados ({total}) ")

    def limpar_campos():
        """Eu limpo o formulário e volto ao modo inserção."""
        global id_selecionado
        id_selecionado = None
        entry_nome.delete(0, tk.END)
        entry_idade.delete(0, tk.END)
        combo_turma.set("")
        entry_nome.focus_set()
        # Desabilito botões de edição/exclusão
        btn_editar.config(state=tk.DISABLED)
        btn_excluir.config(state=tk.DISABLED)
        # Habilito botão Salvar
        btn_salvar.config(state=tk.NORMAL)

    def ao_selecionar(event):
        """Eu preencho o formulário com os dados da linha clicada."""
        global id_selecionado
        selecionado = tree.selection()
        if not selecionado:
            return  # Nenhum item selecionado
        # Pego os valores da linha selecionada
        valores = tree.item(selecionado[0], "values")
        if not valores:
            return
        # Preencho os campos
        limpar_campos_interno()
        entry_nome.insert(0, valores[0])
        entry_idade.insert(0, valores[1])
        combo_turma.set(valores[2])
        # Salvo o id para edição/exclusão
        id_selecionado = int(selecionado[0])
        # Alterno os botões
        btn_editar.config(state=tk.NORMAL)
        btn_excluir.config(state=tk.NORMAL)
        btn_salvar.config(state=tk.DISABLED)

    def limpar_campos_interno():
        """Eu limpo os campos sem mexer nos botões (uso interno)."""
        entry_nome.delete(0, tk.END)
        entry_idade.delete(0, tk.END)
        combo_turma.set("")

    # ===== VALIDAÇÃO =====

    def validar_campos(nome, idade_str, turma):
        """Eu valido os campos e retorno (valido, idade_int)."""
        if not nome or not idade_str or not turma:
            messagebox.showwarning("Campos Obrigatórios", "Preencha todos os campos.")
            return False, None
        try:
            idade = int(idade_str)
        except ValueError:
            messagebox.showerror("Erro", "Idade deve ser um número inteiro.")
            entry_idade.delete(0, tk.END)
            entry_idade.focus_set()
            return False, None
        if idade <= 0:
            messagebox.showerror("Erro", "Idade deve ser um valor positivo.")
            entry_idade.delete(0, tk.END)
            entry_idade.focus_set()
            return False, None
        return True, idade

    # ===== OPERAÇÕES CRUD =====

    def ao_clicar_salvar():
        """Eu insiro um novo aluno no banco."""
        nome = entry_nome.get().strip()
        idade_str = entry_idade.get().strip()
        turma = combo_turma.get().strip()
        valido, idade = validar_campos(nome, idade_str, turma)
        if not valido:
            return
        salvar_aluno(nome, idade, turma)
        messagebox.showinfo("Sucesso", f"Aluno '{nome}' cadastrado!")
        limpar_campos()
        atualizar_tabela()

    def ao_clicar_editar():
        """Eu atualizo o aluno selecionado no banco."""
        global id_selecionado
        if id_selecionado is None:
            messagebox.showwarning("Aviso", "Selecione um aluno para editar.")
            return
        nome = entry_nome.get().strip()
        idade_str = entry_idade.get().strip()
        turma = combo_turma.get().strip()
        valido, idade = validar_campos(nome, idade_str, turma)
        if not valido:
            return
        editar_aluno(id_selecionado, nome, idade, turma)
        messagebox.showinfo("Sucesso", f"Aluno '{nome}' atualizado!")
        limpar_campos()
        atualizar_tabela()

    def ao_clicar_excluir():
        """Eu removo o aluno selecionado após confirmação."""
        global id_selecionado
        if id_selecionado is None:
            messagebox.showwarning("Aviso", "Selecione um aluno para excluir.")
            return
        nome = entry_nome.get().strip()
        resposta = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir o aluno '{nome}'?\n\nEsta ação não pode ser desfeita."
        )
        if resposta:
            remover_aluno(id_selecionado)
            messagebox.showinfo("Excluído", f"Aluno '{nome}' removido do sistema.")
            limpar_campos()
            atualizar_tabela()

    def ao_clicar_buscar():
        """Eu filtro a tabela pelo texto digitado na busca."""
        termo = entry_busca.get().strip()
        atualizar_tabela(filtro_nome=termo if termo else None)

    # ===== BOTÕES DO FORMULÁRIO =====

    btn_salvar = tk.Button(
        frame_botoes, text="💾 Salvar", font=("Arial", 11, "bold"),
        bg="#27ae60", fg="white", activebackground="#219a52",
        activeforeground="white", width=12, height=1, bd=0,
        cursor="hand2", command=ao_clicar_salvar
    )
    btn_salvar.pack(side=tk.LEFT, padx=(0, 8))

    btn_editar = tk.Button(
        frame_botoes, text="✏️ Editar", font=("Arial", 11, "bold"),
        bg="#2980b9", fg="white", activebackground="#1c6ea4",
        activeforeground="white", width=12, height=1, bd=0,
        cursor="hand2", command=ao_clicar_editar, state=tk.DISABLED
    )
    btn_editar.pack(side=tk.LEFT, padx=(0, 8))

    btn_excluir = tk.Button(
        frame_botoes, text="🗑️ Excluir", font=("Arial", 11, "bold"),
        bg="#e74c3c", fg="white", activebackground="#c0392b",
        activeforeground="white", width=12, height=1, bd=0,
        cursor="hand2", command=ao_clicar_excluir, state=tk.DISABLED
    )
    btn_excluir.pack(side=tk.LEFT, padx=(0, 8))

    btn_limpar = tk.Button(
        frame_botoes, text="🧹 Limpar", font=("Arial", 11, "bold"),
        bg="#e67e22", fg="white", activebackground="#d35400",
        activeforeground="white", width=12, height=1, bd=0,
        cursor="hand2", command=limpar_campos
    )
    btn_limpar.pack(side=tk.LEFT)

    # ===== BOTÃO DE BUSCA =====
    btn_buscar = tk.Button(
        frame_busca, text="🔍 Buscar", font=("Arial", 11, "bold"),
        bg="#8e44ad", fg="white", activebackground="#6c3483",
        activeforeground="white", width=10, height=1, bd=0,
        cursor="hand2", command=ao_clicar_buscar
    )
    btn_buscar.pack(side=tk.LEFT)

    # Bind: Enter no campo de busca também dispara a busca
    entry_busca.bind("<Return>", lambda event: ao_clicar_buscar())

    # ===== BIND DE SELEÇÃO NO TREEVIEW =====
    tree.bind("<<TreeviewSelect>>", ao_selecionar)

    # ===== CARREGAMENTO INICIAL =====
    atualizar_tabela()
```

### Passo 4 — Entendendo o fluxo de seleção

O coração da usabilidade do CRUD está no evento `<<TreeviewSelect>>`. Quando o usuário clica em uma linha da tabela:

1. O evento dispara `ao_selecionar`.
2. `tree.selection()` retorna o `iid` da linha (que armazenamos como o `id` do banco).
3. `tree.item(selecionado[0], "values")` retorna os valores das colunas como tupla.
4. Preenchemos os campos do formulário com esses valores.
5. Guardamos `id_selecionado` para usar nas operações de Editar e Excluir.
6. Desabilitamos Salvar (não faz sentido salvar um novo registro enquanto se edita um existente).
7. Habilitamos Editar e Excluir (só fazem sentido com um registro selecionado).

O botão Limpar reverte tudo: limpa os campos, reseta `id_selecionado`, reabilita Salvar e desabilita Editar/Excluir.

Este padrão — modo inserção vs modo edição — é encontrado em praticamente todos os sistemas de cadastro do mercado.

### Passo 5 — Testando o CRUD completo

Execute o sistema:

```bash
python main.py
```

Teste cada operação:

- Inserir (já funcionava): Preencha os campos, clique em Salvar → mensagem de sucesso, tabela atualizada.
- Selecionar: Clique em uma linha da tabela → formulário preenche, Salvar desabilita, Editar e Excluir habilitam.
- Editar: Com uma linha selecionada, altere o nome, clique em Editar → mensagem "atualizado!", tabela reflete a mudança.
- Excluir: Com uma linha selecionada, clique em Excluir → confirmação → mensagem "removido!", linha some da tabela.
- Buscar: Digite um nome parcial no campo de busca e clique em Buscar → tabela mostra apenas os registros que começam com aquele texto.
- Limpar busca: Clique em Buscar com o campo vazio → tabela volta a mostrar todos os registros.
- Limpar formulário: Clique em Limpar → campos limpam, volta ao modo inserção.

## 📝 Exercício

**Tempo estimado:** 15-20 minutos

**Tarefa:** Adicione um botão "Cancelar" que aparece apenas no modo edição (quando uma linha está selecionada) e, ao ser clicado, limpa os campos sem salvar as alterações — exatamente como o botão Limpar, mas com um nome mais intuitivo para o contexto de edição.

Dica: O botão Cancelar pode ter o mesmo comportamento de `limpar_campos`. Adicione-o ao lado dos outros botões e controle seu estado (`tk.NORMAL` / `tk.DISABLED`) junto com Editar e Excluir.

??? hint "Dica"
    Crie `btn_cancelar` com `state=tk.DISABLED` inicialmente. Em `ao_selecionar`, habilite-o. Em `limpar_campos`, desabilite-o. O comando pode ser o próprio `limpar_campos`.

??? success "Solução"
    Adicione no `frame_botoes`:
    
    ```python
    btn_cancelar = tk.Button(
        frame_botoes, text="❌ Cancelar", font=("Arial", 11, "bold"),
        bg="#95a5a6", fg="white", activebackground="#7f8c8d",
        activeforeground="white", width=12, height=1, bd=0,
        cursor="hand2", command=limpar_campos, state=tk.DISABLED
    )
    btn_cancelar.pack(side=tk.LEFT)
    ```
    
    Em `ao_selecionar`, adicione: `btn_cancelar.config(state=tk.NORMAL)`
    Em `limpar_campos`, adicione: `btn_cancelar.config(state=tk.DISABLED)`

## 🏆 Missão da Equipe

**Tempo estimado:** 30-45 minutos

**Tarefa:** Implementem o CRUD completo para a entidade principal do projeto da equipe.

**Entregável:** O sistema da equipe com as quatro operações funcionais.

**Checklist da Missão:**

- [ ] `database/operacoes.py` criado com funções CRUD para a entidade do projeto
- [ ] Controller refatorado para usar o módulo de operações
- [ ] Treeview preenche o formulário ao selecionar uma linha
- [ ] Botão Salvar insere novo registro
- [ ] Botão Editar atualiza o registro selecionado
- [ ] Botão Excluir remove com confirmação
- [ ] Campo de busca funcional
- [ ] Botões Editar/Excluir iniciam desabilitados
- [ ] Modo inserção e modo edição se alternam corretamente
- [ ] O professor testou todas as operações

!!! important "Nota para o Professor"
    Verifique: Cada equipe deve demonstrar o ciclo completo: inserir um registro, selecioná-lo na tabela, editar um campo, salvar a edição e excluir outro registro. Verifique se as mensagens de feedback são adequadas e se a exclusão pede confirmação.

## ⚡ Desafio

**Vá além:** Adicione ordenação por coluna ao clicar nos cabeçalhos do Treeview.

Quando o usuário clicar no cabeçalho "Nome", a tabela ordena por nome. Clicar em "Idade" ordena por idade. Clicar novamente inverte a ordem (crescente ↔ decrescente).

Dica: Use `tree.heading("nome", command=lambda: ordenar_por("nome"))`. Crie uma função `ordenar_por(coluna)` que faz uma nova consulta ao banco com ORDER BY adequado e recarrega a tabela. Controle a direção com uma variável.

```python
# Exemplo de esqueleto:
ordem_atual = {"coluna": "nome", "direcao": "ASC"}

def ordenar_por(coluna):
    global ordem_atual
    if ordem_atual["coluna"] == coluna:
        ordem_atual["direcao"] = "DESC" if ordem_atual["direcao"] == "ASC" else "ASC"
    else:
        ordem_atual["coluna"] = coluna
        ordem_atual["direcao"] = "ASC"
    # Recarregar tabela com ORDER BY coluna direcao
```

Para isso, você precisará modificar `listar_alunos` no controller e `operacoes.py` para aceitar parâmetros de ordenação.

## ⚠️ Erros Comuns

!!! danger "Esquecer de resetar id_selecionado após excluir"
    **Sintoma:** Após excluir um aluno, o botão Editar ainda está habilitado. Ao clicar, tenta dar UPDATE em um registro que não existe mais.
    
    **Causa:** A variável `id_selecionado` não foi resetada para `None` após a exclusão.
    
    **Solução:** Na função `ao_clicar_excluir`, chame `limpar_campos()` após a exclusão (como já fizemos no código). Isso reseta o `id_selecionado` e desabilita os botões.

!!! warning "Bind <<TreeviewSelect>> disparando ao limpar a tabela"
    **Sintoma:** Ao chamar `atualizar_tabela`, o evento de seleção dispara e tenta preencher o formulário com dados que não existem mais.
    
    **Causa:** `tree.delete(item)` dentro de `atualizar_tabela` pode disparar o evento de seleção.
    
    **Solução:** A função `ao_selecionar` já verifica `if not selecionado: return`, mas se o erro persistir, adicione uma flag `_atualizando = True` durante a atualização e verifique-a no início de `ao_selecionar`.

!!! danger "Usar o índice errado para o id"
    **Sintoma:** Ao editar, o `WHERE id = ?` usa um valor errado (ex: 1 quando deveria ser 5).
    
    **Causa:** Confundir o índice da linha no Treeview com o id do banco. `tree.selection()` retorna o `iid`, que definimos como o id do banco, mas se em algum lugar você usou `tree.index(item)` em vez de `item`, receberá a posição visual, não o identificador.
    
    **Solução:** Sempre use `int(selecionado[0])` — o `iid` que foi definido no `tree.insert(..., iid=aluno["id"])`.

!!! warning "Query de busca com LIKE vazia"
    **Sintoma:** Ao clicar em Buscar com o campo vazio, a tabela fica vazia.
    
    **Causa:** Passar string vazia para o LIKE faz o banco buscar por `WHERE nome LIKE '%'`, que deveria retornar tudo, mas dependendo da implementação pode não funcionar.
    
    **Solução:** Nossa implementação já trata isso: se `filtro_nome` for vazio ou None, faz SELECT sem WHERE. Se o termo tiver valor, usa LIKE.

## 💡 Boas Práticas

**1. Centralização das queries em operacoes.py**

Extrair o SQL do controller para um módulo dedicado segue o princípio de Separation of Concerns. O controller coordena; o módulo de operações executa. Se o banco mudar (ex: de SQLite para PostgreSQL), apenas `operacoes.py` e `conexao.py` são afetados.

**2. Modo inserção vs modo edição**

Controlar o estado do formulário (inserção ou edição) através de uma variável (`id_selecionado`) e do estado dos botões (`state=tk.DISABLED`) é um padrão consagrado. Ele evita ambiguidades: o usuário sempre sabe se está criando algo novo ou modificando algo existente.

**3. Confirmação antes de ações destrutivas**

A função `ao_clicar_excluir` usa `messagebox.askyesno` antes de executar o DELETE. Isso é obrigatório em softwares profissionais — deletar dados sem confirmação é uma das reclamações mais comuns de usuários.

**4. lastrowid para obter o ID gerado**

Após um INSERT, `cursor.lastrowid` retorna o id gerado pelo AUTOINCREMENT. Isso é essencial para manter o controle do registro sem precisar fazer um SELECT adicional.

**5. LIKE com parâmetro para busca flexível**

Usar `LIKE ?` com `f"{termo}%"` permite busca parcial: digitar "Jo" encontra "João", "José", "Joaquim". O `%` no final significa "qualquer coisa depois". Para buscar em qualquer parte do nome, use `f"%{termo}%"`.

## ☑️ Checklist

Antes de prosseguir para o próximo capítulo, confirme:

- [ ] O arquivo `database/operacoes.py` existe com funções `inserir_aluno`, `listar_alunos`, `atualizar_aluno`, `excluir_aluno`
- [ ] O controller `aluno.py` foi refatorado para usar `operacoes.py`
- [ ] Ao clicar em uma linha do Treeview, o formulário é preenchido
- [ ] O botão Salvar insere um novo registro (modo inserção)
- [ ] O botão Editar atualiza o registro selecionado (modo edição)
- [ ] O botão Excluir pede confirmação e remove o registro
- [ ] O botão Limpar reseta o formulário para modo inserção
- [ ] O campo de busca filtra a tabela corretamente
- [ ] Botões Editar e Excluir estão desabilitados quando nada está selecionado
- [ ] Nenhuma query SQL usa concatenação de strings
- [ ] Minha equipe concluiu a Missão da Equipe

## ➡️ Próximo Capítulo

No **Capítulo 09 — Banco em Nuvem**, você levará o Sistema Escolar para o próximo nível: sincronização com um banco de dados remoto. Os dados não ficarão mais presos no computador local — estarão acessíveis de qualquer lugar.

Você aprenderá a:

- Configurar um banco em nuvem (Firebase ou similar)
- Criar uma camada de sincronização
- Enviar dados locais para a nuvem
- Baixar dados da nuvem para o SQLite local

O CRUD que você construiu hoje é a base — a nuvem será uma extensão, não uma substituição. ☁️
