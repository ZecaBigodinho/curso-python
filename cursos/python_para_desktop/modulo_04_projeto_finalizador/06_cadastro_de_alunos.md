# 06 — Cadastro de Alunos

## 🎯 Objetivo

Neste capítulo você vai construir o formulário de cadastro de alunos — a primeira tela funcional completa do Sistema Escolar, com entrada de dados, validação e exibição em tabela.

Ao final, você terá:

- Um formulário com campos para Nome, Idade e Turma
- Validação inteligente: impede campos vazios, idade não numérica e idade negativa
- Uma tabela Treeview com scrollbar listando todos os alunos cadastrados
- Botões Salvar (adiciona à lista e atualiza a tabela) e Limpar (reseta o formulário)
- Dados armazenados em uma lista em memória — preparada para migração ao SQLite no próximo capítulo
- O menu principal abrindo a tela de cadastro como uma janela Toplevel totalmente funcional

## 📍 Contextualização

No Capítulo 05, você dominou a navegação entre múltiplas janelas: Toplevel, withdraw, deiconify, controle de duplicação e interceptação do botão X. As janelas de funcionalidade eram placeholders vazios — meros esqueletos.

Agora, você preencherá o esqueleto com músculos e órgãos. A janela de Cadastro de Alunos ganhará vida com widgets reais, validação de dados e uma tabela que se atualiza dinamicamente. Você também conhecerá o Treeview — o widget mais poderoso do Tkinter para exibir dados tabulares — e aprenderá a integrá-lo com uma fonte de dados (por enquanto, uma lista em memória).

Este é o capítulo mais denso da primeira metade do módulo. Respire fundo e vamos construir.

**Progresso do Sistema:**

```text
✅ Capítulo 01 — Introdução e Planejamento
✅ Capítulo 02 — Arquitetura do Sistema
✅ Capítulo 03 — Tela de Login
✅ Capítulo 04 — Menu Principal
✅ Capítulo 05 — Múltiplas Janelas
🔨 Cadastro de Alunos ← VOCÊ ESTÁ AQUI
⬜ SQLite Local
⬜ CRUD Completo
⬜ Banco em Nuvem
⬜ Integração e Testes
⬜ Refatoração e Entrega
```

## ✅ Resultado Esperado

Ao clicar em "Cadastrar Alunos" no menu, o sistema abrirá uma janela independente com este visual:

```text
┌──────────────────────────────────────────────────┐
│  Cadastro de Alunos                          _ □ X│
│                                                  │
│  ┌─ Dados do Aluno ────────────────────────────┐ │
│  │  Nome:  [________________________]          │ │
│  │  Idade: [________]  Turma: [____▾]          │ │
│  │                                             │ │
│  │  [💾 Salvar]  [🧹 Limpar]                   │ │
│  └─────────────────────────────────────────────┘ │
│                                                  │
│  ┌─ Alunos Cadastrados ────────────────────────┐ │
│  │  Nome          │ Idade │ Turma              │ │
│  │  ──────────────┼───────┼──────              │ │
│  │  João Silva    │ 15    │ 9A                 │ │
│  │  Maria Souza   │ 14    │ 9B                 │ │
│  │  ...           │ ...   │ ...                │ │
│  │                                     ▴       │ │
│  │                                     ▾       │ │
│  └─────────────────────────────────────────────┘ │
│                                                  │
└──────────────────────────────────────────────────┘
```

Comportamento esperado:

- Ao digitar dados válidos e clicar em Salvar, o aluno aparece na tabela e os campos são limpos
- Se algum campo estiver vazio, um messagebox de aviso é exibido
- Se "Idade" não for um número inteiro positivo, um messagebox de erro é exibido
- O botão Limpar apaga o conteúdo de todos os campos sem afetar a tabela
- Os dados persistem enquanto a janela estiver aberta (na memória). Ao fechar a janela, os dados se perdem — isso será resolvido com SQLite no Capítulo 07

Arquivos criados ou modificados:

| Arquivo | Ação |
|---|---|
| `controllers/aluno.py` | Novo — lógica de negócio (salvar, listar, limpar) |
| `views/cadastro.py` | Novo — formulário e Treeview |
| `views/menu.py` | Modificado — botão "Cadastrar Alunos" abre a tela real |

## 💻 Implementação Guiada

### Passo 1 — Criando o Controller de Alunos

Começamos pela camada de lógica, seguindo o padrão MVC. O controller não conhece a interface — apenas manipula os dados.

Crie o arquivo `controllers/aluno.py`:

```python
# ======================================================================
# aluno.py — Controlador de Alunos
# ======================================================================
# Eu sou responsável por gerenciar os dados dos alunos.
# Por enquanto, eu guardo tudo em uma lista na memória.
#
# ⚠️ No Capítulo 07, eu vou trocar esta lista por um banco SQLite.
#    As funções terão os mesmos nomes — só a implementação mudará.
# ======================================================================

# ---------- BANCO DE DADOS EM MEMÓRIA (PROVISÓRIO) ----------
# Eu sou a lista que armazena os alunos cadastrados.
# Cada aluno é um dicionário com as chaves: nome, idade, turma.
alunos = []


def salvar_aluno(nome, idade, turma):
    """
    Eu adiciono um novo aluno à lista em memória.

    Parâmetros:
        nome: string com o nome completo do aluno
        idade: inteiro com a idade do aluno
        turma: string com a turma (ex: '9A', '1B')

    Retorno:
        dict com os dados do aluno recém-criado
    """
    # Eu monto o dicionário que representa o aluno.
    aluno = {
        "nome": nome,
        "idade": idade,
        "turma": turma
    }
    # Eu adiciono o aluno à lista.
    alunos.append(aluno)
    # Eu retorno o aluno para que a view possa usá-lo se necessário.
    return aluno


def listar_alunos():
    """
    Eu devolvo a lista completa de alunos cadastrados.

    Retorno:
        list de dict — cada dict contém nome, idade, turma
    """
    # Simplesmente retorno a lista que está na memória.
    # No futuro, aqui haverá um SELECT no banco de dados.
    return alunos


def limpar_dados():
    """
    Eu removo todos os alunos da memória.
    Útil para testes ou para a funcionalidade de 'Resetar'.
    """
    # Esvazio a lista.
    alunos.clear()
```

!!! note "Conceito Importante"
    Repare que as funções `salvar_aluno`, `listar_alunos` e `limpar_dados` não usam Tkinter. Elas são puro Python. Isso permite testá-las isoladamente e, no futuro, trocar a implementação interna (de lista para SQLite) sem quebrar a interface.

### Passo 2 — Criando a View de Cadastro (parte 1: formulário)

Agora, a interface. Será um Toplevel com dois LabelFrame: um para o formulário de entrada e outro para a tabela de listagem.

Crie o arquivo `views/cadastro.py`. Vamos começar com a estrutura geral e o formulário:

```python
# ======================================================================
# cadastro.py — Tela de Cadastro de Alunos (View)
# ======================================================================
# Eu sou a tela de cadastro de alunos do Sistema Escolar.
# Exibo o formulário de entrada e a tabela com os dados cadastrados.
#
# Eu NÃO manipulo os dados diretamente — sempre passo pelo controller.
# ======================================================================

import tkinter as tk
from tkinter import ttk, messagebox
from controllers.aluno import salvar_aluno, listar_alunos


def abrir_janela_cadastro(janela_pai):
    """
    Eu abro a janela de cadastro como um Toplevel.

    Parâmetros:
        janela_pai: a janela principal (tk.Tk) que me chamou
    """
    # ---------- CRIAÇÃO DA JANELA ----------
    janela = tk.Toplevel(janela_pai)
    janela.title("Cadastro de Alunos")
    # Importo a função de centralização (evita dependência no topo).
    from utils.helpers import centralizar_janela
    centralizar_janela(janela, 750, 550)
    janela.resizable(False, False)
    janela.protocol("WM_DELETE_WINDOW", janela.destroy)

    # ---------- COR DE FUNDO ----------
    janela.configure(bg="#f5f6fa")

    # ---------- FRAME DO FORMULÁRIO ----------
    # Eu crio um LabelFrame com borda e título para o formulário.
    frame_form = tk.LabelFrame(
        janela,
        text=" Dados do Aluno ",
        font=("Arial", 12, "bold"),
        bg="#ffffff",
        fg="#2c3e50",
        bd=2,
        relief=tk.GROOVE,
        padx=15,
        pady=15
    )
    frame_form.pack(fill=tk.X, padx=20, pady=(20, 10))

    # ---------- CAMPO NOME ----------
    lbl_nome = tk.Label(
        frame_form,
        text="Nome:",
        font=("Arial", 11),
        bg="#ffffff",
        fg="#333333",
        anchor="w"
    )
    lbl_nome.grid(row=0, column=0, sticky="w", pady=(0, 5))

    entry_nome = tk.Entry(
        frame_form,
        font=("Arial", 12),
        width=35,
        bd=2,
        relief=tk.SOLID
    )
    entry_nome.grid(row=0, column=1, columnspan=3, sticky="ew", padx=(10, 0), pady=(0, 5))
    entry_nome.focus_set()

    # ---------- CAMPO IDADE ----------
    lbl_idade = tk.Label(
        frame_form,
        text="Idade:",
        font=("Arial", 11),
        bg="#ffffff",
        fg="#333333"
    )
    lbl_idade.grid(row=1, column=0, sticky="w", pady=(5, 5))

    entry_idade = tk.Entry(
        frame_form,
        font=("Arial", 12),
        width=8,
        bd=2,
        relief=tk.SOLID
    )
    entry_idade.grid(row=1, column=1, sticky="w", padx=(10, 20), pady=(5, 5))

    # ---------- CAMPO TURMA ----------
    lbl_turma = tk.Label(
        frame_form,
        text="Turma:",
        font=("Arial", 11),
        bg="#ffffff",
        fg="#333333"
    )
    lbl_turma.grid(row=1, column=2, sticky="w", pady=(5, 5))

    # Eu uso uma Combobox para a turma — assim o usuário escolhe de uma lista
    # predefinida, reduzindo erros de digitação.
    turmas_disponiveis = [
        "6A", "6B", "7A", "7B", "8A", "8B",
        "9A", "9B", "1A", "1B", "2A", "2B", "3A", "3B"
    ]
    combo_turma = ttk.Combobox(
        frame_form,
        values=turmas_disponiveis,
        font=("Arial", 12),
        width=6,
        state="readonly"
    )
    combo_turma.grid(row=1, column=3, sticky="w", padx=(10, 0), pady=(5, 5))
    combo_turma.set("")  # Começa vazio

    # Configuro a grid do frame_form para expandir o campo nome.
    frame_form.columnconfigure(1, weight=1)

    # ---------- FRAME DOS BOTÕES ----------
    frame_botoes = tk.Frame(frame_form, bg="#ffffff")
    frame_botoes.grid(row=2, column=0, columnspan=4, pady=(15, 0))
```

### Passo 3 — Criando a View de Cadastro (parte 2: Treeview e botões)

Continuando no mesmo arquivo `views/cadastro.py`, abaixo do código anterior, ainda dentro da função `abrir_janela_cadastro`:

```python
    # ===== CONTINUAÇÃO DENTRO DE abrir_janela_cadastro =====

    # ---------- FRAME DA LISTAGEM ----------
    frame_lista = tk.LabelFrame(
        janela,
        text=" Alunos Cadastrados ",
        font=("Arial", 12, "bold"),
        bg="#ffffff",
        fg="#2c3e50",
        bd=2,
        relief=tk.GROOVE,
        padx=15,
        pady=15
    )
    frame_lista.pack(fill=tk.BOTH, expand=True, padx=20, pady=(5, 20))

    # ---------- TREVIEW ----------
    # Eu crio a tabela que exibirá os alunos.
    # columns define as colunas visíveis (além da coluna fantasma #0).
    colunas = ("nome", "idade", "turma")
    tree = ttk.Treeview(
        frame_lista,
        columns=colunas,
        show="headings",  # Esconde a coluna fantasma #0
        height=10
    )

    # Eu configuro os cabeçalhos das colunas.
    tree.heading("nome", text="Nome")
    tree.heading("idade", text="Idade")
    tree.heading("turma", text="Turma")

    # Eu configuro a largura e o alinhamento de cada coluna.
    tree.column("nome", width=300, anchor="w")
    tree.column("idade", width=80, anchor="center")
    tree.column("turma", width=80, anchor="center")

    # ---------- SCROLLBAR ----------
    # Eu adiciono uma barra de rolagem vertical vinculada ao Treeview.
    scrollbar = ttk.Scrollbar(
        frame_lista,
        orient=tk.VERTICAL,
        command=tree.yview
    )
    tree.configure(yscrollcommand=scrollbar.set)

    # Eu posiciono a tabela e a scrollbar lado a lado.
    tree.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    # Eu configuro o frame_lista para expandir a tabela.
    frame_lista.rowconfigure(0, weight=1)
    frame_lista.columnconfigure(0, weight=1)

    # ---------- FUNÇÕES DOS BOTÕES ----------
    def ao_clicar_salvar():
        """
        Eu valido os campos, salvo o aluno e atualizo a tabela.
        """
        # Capturo e limpo os valores.
        nome = entry_nome.get().strip()
        idade_str = entry_idade.get().strip()
        turma = combo_turma.get().strip()

        # ---------- VALIDAÇÃO ----------
        # 1. Campos obrigatórios
        if not nome or not idade_str or not turma:
            messagebox.showwarning(
                "Campos Obrigatórios",
                "Por favor, preencha todos os campos antes de salvar."
            )
            return

        # 2. Idade deve ser um número inteiro
        try:
            idade = int(idade_str)
        except ValueError:
            messagebox.showerror(
                "Erro de Validação",
                "O campo 'Idade' deve ser um número inteiro.\nExemplo: 15"
            )
            entry_idade.delete(0, tk.END)
            entry_idade.focus_set()
            return

        # 3. Idade deve ser positiva
        if idade <= 0:
            messagebox.showerror(
                "Erro de Validação",
                "A idade deve ser um valor positivo maior que zero."
            )
            entry_idade.delete(0, tk.END)
            entry_idade.focus_set()
            return

        # ---------- PERSISTÊNCIA ----------
        # Passou nas validações — delego ao controller.
        salvar_aluno(nome, idade, turma)

        # ---------- FEEDBACK E ATUALIZAÇÃO ----------
        messagebox.showinfo("Sucesso", f"Aluno '{nome}' cadastrado com sucesso!")
        limpar_campos()
        atualizar_tabela()

    def limpar_campos():
        """
        Eu limpo todos os campos do formulário.
        """
        entry_nome.delete(0, tk.END)
        entry_idade.delete(0, tk.END)
        combo_turma.set("")
        entry_nome.focus_set()

    def atualizar_tabela():
        """
        Eu recarrego a tabela com os dados atuais da lista de alunos.
        """
        # Primeiro, removo todas as linhas existentes na tabela.
        for item in tree.get_children():
            tree.delete(item)

        # Depois, insiro cada aluno da lista como uma nova linha.
        for aluno in listar_alunos():
            tree.insert(
                "",
                tk.END,
                values=(aluno["nome"], aluno["idade"], aluno["turma"])
            )

    # ---------- BOTÕES DO FORMULÁRIO ----------
    btn_salvar = tk.Button(
        frame_botoes,
        text="💾 Salvar",
        font=("Arial", 11, "bold"),
        bg="#27ae60",
        fg="white",
        activebackground="#219a52",
        activeforeground="white",
        width=12,
        height=1,
        bd=0,
        cursor="hand2",
        command=ao_clicar_salvar
    )
    btn_salvar.pack(side=tk.LEFT, padx=(0, 10))

    btn_limpar = tk.Button(
        frame_botoes,
        text="🧹 Limpar",
        font=("Arial", 11, "bold"),
        bg="#e67e22",
        fg="white",
        activebackground="#d35400",
        activeforeground="white",
        width=12,
        height=1,
        bd=0,
        cursor="hand2",
        command=limpar_campos
    )
    btn_limpar.pack(side=tk.LEFT)

    # ---------- CARREGAMENTO INICIAL ----------
    # Eu preencho a tabela com os dados que já existem na memória.
    # (Útil se a janela for reaberta e houver dados de uma sessão anterior.)
    atualizar_tabela()
```

!!! tip "Dica Profissional"
    A função `atualizar_tabela` primeiro limpa todas as linhas (`tree.get_children()`) e depois reinsere cada aluno. Essa abordagem é simples e garante que a tabela sempre reflita exatamente a lista. Para tabelas muito grandes, técnicas mais eficientes existem — mas para nosso escopo, está perfeito.

### Passo 4 — Atualizando o Menu para abrir a tela real

Agora, o botão "Cadastrar Alunos" do menu deve chamar nossa nova função `abrir_janela_cadastro` em vez de exibir um placeholder.

Abra `views/menu.py` e faça as seguintes alterações:

- No topo do arquivo, adicione o import:

```python
# ===== ADICIONE ESTA LINHA no topo de views/menu.py =====
from views.cadastro import abrir_janela_cadastro
```

- No dicionário `botoes_config`, altere o comando do botão "Cadastrar Alunos":

```python
# ===== CÓDIGO EXISTENTE =====
"comando": lambda: abrir_janela_cadastro(janela)

# ===== MANTENHA ESTA LINHA (já estava assim no Capítulo 05) =====
# Agora a função abrir_janela_cadastro existe em views/cadastro.py
# e substitui o placeholder.
```

!!! note "Verificação"
    No Capítulo 05, o botão "Cadastrar Alunos" já chamava `abrir_janela_cadastro(janela)`, mas a função estava definida dentro do próprio `menu.py` como um placeholder. Agora, com o import, a chamada aponta para a função real em `views/cadastro.py`. Certifique-se de remover a função placeholder `abrir_janela_cadastro` que estava em `views/menu.py`, assim como a variável global `janela_cadastro_aberta` — essas agora são gerenciadas em `views/cadastro.py`.

Limpeza em `views/menu.py`: Remova a função `abrir_janela_cadastro` antiga, a função `fechar_janela_cadastro` antiga e a variável global `janela_cadastro_aberta`. Elas não são mais necessárias lá. (Deixe apenas os imports e o dicionário de botões apontando para a nova função.)

O controle de duplicação será tratado em `views/cadastro.py` no próximo capítulo (ou você pode adicioná-lo já, seguindo o padrão do Capítulo 05). Para manter o foco, deixaremos a duplicação como melhoria opcional.

### Passo 5 — Testando o fluxo completo

Execute o sistema:

```bash
python main.py
```

Faça o login (admin / admin) e clique em Cadastrar Alunos.

Teste os seguintes cenários:

- Salvar com campos vazios: Deixe um campo em branco e clique em Salvar → deve aparecer "Campos Obrigatórios".
- Idade não numérica: Digite "abc" em Idade e clique em Salvar → deve aparecer "O campo 'Idade' deve ser um número inteiro".
- Idade negativa: Digite "-5" em Idade e clique em Salvar → deve aparecer "A idade deve ser um valor positivo".
- Cadastro válido: Preencha Nome="João Silva", Idade="15", Turma="9A" → "Aluno 'João Silva' cadastrado com sucesso!" e a tabela se atualiza.
- Múltiplos cadastros: Cadastre 3 alunos diferentes → todos aparecem na tabela.
- Limpar: Preencha os campos e clique em Limpar → todos os campos ficam vazios, mas a tabela permanece intacta.
- Fechar e reabrir: Feche a janela de cadastro e abra novamente → a tabela estará vazia (os dados se perderam, pois estavam apenas na memória). Isso será resolvido no próximo capítulo com SQLite!

## 📝 Exercício

**Tempo estimado:** 15-20 minutos

**Tarefa:** Adicione um novo campo ao formulário: E-mail. Ele deve:

- Ser um Entry com largura 30
- Ser validado como campo obrigatório
- Ter uma validação extra: conter o caractere `@` (validação simples de e-mail)
- Aparecer como uma nova coluna no Treeview ("E-mail")
- Ser armazenado no dicionário do aluno como chave "email"

Dica: Adicione o campo no `frame_form`, atualize `colunas` do Treeview, a função `ao_clicar_salvar` e o controller `aluno.py`.

??? hint "Dica"
    No `frame_form`, adicione o campo E-mail em uma nova linha (`row=2`). A validação do `@` pode ser feita com `if "@" not in email: messagebox.showerror(...)`. Não se esqueça de adicionar "email" nas colunas do Treeview e no dicionário de `salvar_aluno`.

??? success "Solução (trechos principais)"
    Em `controllers/aluno.py`, altere `salvar_aluno`:
    
    ```python
    def salvar_aluno(nome, idade, turma, email):
        aluno = {
            "nome": nome,
            "idade": idade,
            "turma": turma,
            "email": email
        }
        alunos.append(aluno)
        return aluno
    ```
    
    Em `views/cadastro.py`, adicione o campo (dentro de `frame_form`, antes do frame de botões):
    
    ```python
    lbl_email = tk.Label(frame_form, text="E-mail:", font=("Arial", 11), bg="#ffffff", fg="#333333")
    lbl_email.grid(row=2, column=0, sticky="w", pady=(5, 5))
    entry_email = tk.Entry(frame_form, font=("Arial", 12), width=30, bd=2, relief=tk.SOLID)
    entry_email.grid(row=2, column=1, columnspan=3, sticky="ew", padx=(10, 0), pady=(5, 5))
    ```
    
    Atualize colunas do Treeview para `("nome", "idade", "turma", "email")` e os headings/columns correspondentes. Em `ao_clicar_salvar`, capture `email = entry_email.get().strip()`, valide `"@" in email`, e passe para `salvar_aluno(nome, idade, turma, email)`. Em `atualizar_tabela`, inclua `aluno["email"]` nos values.

## 🏆 Missão da Equipe

**Tempo estimado:** 30-45 minutos

**Tarefa:** Criem o formulário de cadastro do projeto da equipe, adaptando os campos ao domínio escolhido.

**Entregável:** Os arquivos `controllers/[entidade].py` e `views/cadastro.py` (ou nome equivalente) funcionais.

**Checklist da Missão:**

- [ ] Controller criado com as funções `salvar_*`, `listar_*` (ex: `salvar_livro`, `listar_livros`)
- [ ] View de cadastro com formulário contendo pelo menos 3 campos específicos do domínio
- [ ] Treeview configurado com as colunas adequadas
- [ ] Validação de campos obrigatórios implementada
- [ ] Validação de tipo (numérico, data, etc.) em pelo menos um campo
- [ ] Botões Salvar e Limpar funcionais
- [ ] A tabela atualiza automaticamente após cada cadastro
- [ ] O menu principal abre a tela de cadastro real (não placeholder)
- [ ] O professor testou o cadastro com dados de exemplo

!!! important "Nota para o Professor"
    Verifique: Cada equipe deve ter adaptado os campos ao seu domínio. Exemplos: para Biblioteca → Título, Autor, ISBN, Ano; para Estoque → Produto, Quantidade, Fornecedor, Preço. Verifique se a validação funciona (campos vazios, tipo incorreto). O Treeview deve refletir exatamente os campos do formulário.

## ⚡ Desafio

**Vá além:** Implemente validação de duplicidade — impeça que dois alunos com o mesmo nome sejam cadastrados.

Quando o usuário tentar salvar um aluno cujo nome já existe na lista, exiba um messagebox de aviso: "Já existe um aluno cadastrado com o nome 'X'." e interrompa o cadastro.

Dica: Antes de chamar `salvar_aluno`, percorra a lista de alunos com `listar_alunos()` e verifique se algum possui o mesmo nome (case-insensitive). Use `nome.lower()` para comparar ignorando maiúsculas/minúsculas.

Exemplo de implementação em `ao_clicar_salvar`:

```python
# Verifico duplicidade (case-insensitive)
for aluno_existente in listar_alunos():
    if aluno_existente["nome"].lower() == nome.lower():
        messagebox.showwarning(
            "Duplicidade",
            f"Já existe um aluno cadastrado com o nome '{nome}'."
        )
        entry_nome.focus_set()
        return
```

## ⚠️ Erros Comuns

!!! danger "Esquecer de configurar columnconfigure no frame_form"
    **Sintoma:** O campo Nome não expande horizontalmente, ficando curto mesmo com `width=35`.
    
    **Causa:** O `frame_form` não tem `columnconfigure` para dar peso à coluna do Entry.
    
    **Solução:** Adicione `frame_form.columnconfigure(1, weight=1)` após posicionar os widgets. Isso faz a coluna 1 (onde está o Entry de Nome) expandir.

!!! warning "Treeview não aparece dados após salvar"
    **Sintoma:** A mensagem de sucesso aparece, mas a tabela continua vazia.
    
    **Causa:** Ou a função `atualizar_tabela` não está sendo chamada, ou `listar_alunos` está retornando uma lista vazia.
    
    **Solução:** Verifique se `atualizar_tabela()` está dentro de `ao_clicar_salvar`, após `salvar_aluno`. Verifique também se `salvar_aluno` realmente adiciona à lista `alunos` no controller.

!!! danger "Usar tk.END no lugar de tk.END para Treeview"
    **Sintoma:** `AttributeError: module 'tkinter' has no attribute 'END'`
    
    **Causa:** Para Treeview, `tk.END` é válido, mas o erro surge quando se tenta usar `END` sem qualificação em um contexto onde não foi importado. Na verdade, `tk.END` existe e funciona. O erro mais comum aqui é digitar `END` em vez de `tk.END`.
    
    **Solução:** Sempre use `tk.END` (com o prefixo `tk.`). Não confunda com `tk.END` vs `"end"` — ambos funcionam no Treeview, mas `tk.END` é o padrão.

!!! warning "Combobox com state='readonly' não permite digitar"
    **Sintoma:** O usuário não consegue digitar uma turma personalizada, apenas selecionar da lista.
    
    **Causa:** `state="readonly"` foi usado intencionalmente para forçar o uso das opções predefinidas.
    
    **Solução:** Se o domínio exigir que o usuário possa digitar valores novos, mude para `state="normal"` ou remova o parâmetro. No nosso caso, manter `readonly` é uma decisão de design — padroniza as turmas e evita erros de digitação.

## 💡 Boas Práticas

**1. Validação em camadas**

A validação foi feita na View (`ao_clicar_salvar`), não no Controller. Isso é uma escolha arquitetural: a View é responsável pela experiência do usuário (mensagens, foco nos campos), enquanto o Controller foca na lógica de negócio. Em sistemas maiores, pode-se adicionar validação também no Controller para garantir integridade independente da interface.

**2. Combobox para valores controlados**

Usar Combobox com `state="readonly"` para o campo Turma evita que o usuário digite "9a", "9A", "nove A", etc. — todos representando a mesma turma mas com grafias diferentes. Isso simplifica consultas futuras e mantém a base de dados limpa.

**3. Treeview com show="headings"**

O parâmetro `show="headings"` esconde a coluna fantasma `#0` que o Treeview cria por padrão. Sem isso, a tabela teria uma coluna vazia extra à esquerda, desperdiçando espaço.

**4. Atualização completa da tabela**

A função `atualizar_tabela` limpa todas as linhas e as recria. Para poucos registros (centenas), isso é instantâneo e garante consistência. Se um dia o sistema tiver milhares de registros, técnicas de atualização incremental podem ser necessárias — mas comece simples.

**5. Preparação para persistência**

Os comentários no controller (⚠️ No Capítulo 07, eu vou trocar esta lista por um banco SQLite) preparam o terreno mental. A assinatura das funções (`salvar_aluno(nome, idade, turma)`) foi projetada para ser compatível com uma futura operação de INSERT. Quando migrarmos para SQLite, a View não precisará ser alterada — apenas o Controller.

## ☑️ Checklist

Antes de prosseguir para o próximo capítulo, confirme:

- [ ] O arquivo `controllers/aluno.py` existe com as funções `salvar_aluno`, `listar_alunos`
- [ ] O arquivo `views/cadastro.py` existe com `abrir_janela_cadastro`
- [ ] O formulário contém campos Nome, Idade e Turma (Combobox)
- [ ] A validação de campos vazios funciona
- [ ] A validação de idade numérica e positiva funciona
- [ ] A tabela Treeview exibe colunas Nome, Idade, Turma com headings
- [ ] A scrollbar está vinculada ao Treeview
- [ ] O botão Salvar adiciona o aluno e atualiza a tabela
- [ ] O botão Limpar limpa os campos sem afetar a tabela
- [ ] O menu principal abre a tela de cadastro real (não placeholder)
- [ ] Os comentários mencionam a migração futura para SQLite
- [ ] Minha equipe concluiu a Missão da Equipe

## ➡️ Próximo Capítulo

No **Capítulo 07 — SQLite**, você resolverá o maior problema atual: a volatilidade dos dados. Tudo o que você cadastra se perde quando a janela fecha.

Você aprenderá a:

- Criar um banco de dados SQLite (`escola.db`)
- Conectar-se a ele pelo Python (módulo `database/conexao.py`)
- Criar tabelas via SQL (`CREATE TABLE alunos`)
- Adaptar as funções do Controller para usar `INSERT`, `SELECT` e `DELETE`
- Manter os dados entre sessões

A estrutura do seu código foi projetada para essa transição: você alterará apenas o Controller. A View permanecerá intacta. Esse é o poder do MVC. 🗄️
