# 03 — Tela de Login

## 🎯 Objetivo

Neste capítulo você vai construir a Tela de Login do Sistema Escolar, a primeira interface funcional que o usuário encontrará ao abrir o sistema.

Ao final, você terá:

- Um formulário centralizado com campos de usuário e senha
- Um campo de senha que oculta os caracteres digitados com asteriscos
- Um botão Entrar que valida as credenciais do usuário
- Feedback visual de erro usando messagebox quando as credenciais forem inválidas
- O código organizado em dois novos módulos: `views/login.py` e `controllers/auth.py`

## 📍 Contextualização

No Capítulo 02, você criou a arquitetura do projeto: as pastas `views/`, `controllers/`, `database/` e `utils/` com seus respectivos `__init__.py`, além do `main.py` que abre uma janela vazia de 800x600 centralizada. Foi a fundação do sistema.

Agora, essa janela vazia ganhará vida. Você construirá a primeira tela real — o Login — e a conectará a uma lógica de autenticação separada da interface. É o primeiro exemplo concreto de como as camadas View e Controller se comunicam.

**Progresso do Sistema:**

```text
✅ Capítulo 01 — Introdução e Planejamento
✅ Capítulo 02 — Arquitetura do Sistema
🔨 Tela de Login ← VOCÊ ESTÁ AQUI
⬜ Menu Principal
⬜ Múltiplas Janelas
⬜ Cadastro de Alunos
⬜ SQLite Local
⬜ CRUD Completo
⬜ Banco em Nuvem
⬜ Integração e Testes
⬜ Refatoração e Entrega
```

## ✅ Resultado Esperado

Ao executar `python main.py`, o sistema abrirá uma janela com o formulário de login centralizado. Visualmente, será assim:

```text
┌──────────────────────────────────────────────┐
│  Sistema Escolar                         _ □ X│
│                                              │
│                                              │
│           ┌─────────────────────┐            │
│           │    🔐 Acesso        │            │
│           │                     │            │
│           │  Usuário:           │            │
│           │  ┌───────────────┐  │            │
│           │  │               │  │            │
│           │  └───────────────┘  │            │
│           │                     │            │
│           │  Senha:             │            │
│           │  ┌───────────────┐  │            │
│           │  │ ****          │  │            │
│           │  └───────────────┘  │            │
│           │                     │            │
│           │  ┌───────────────┐  │            │
│           │  │    Entrar     │  │            │
│           │  └───────────────┘  │            │
│           └─────────────────────┘            │
│                                              │
│                                              │
└──────────────────────────────────────────────┘
```

Comportamento esperado:

- O campo Usuário aceita texto livre
- O campo Senha exibe asteriscos no lugar dos caracteres
- Clicar em Entrar com usuário admin e senha admin exibe um messagebox de sucesso (por enquanto — a transição para o menu virá no próximo capítulo)
- Clicar em Entrar com qualquer outra combinação exibe um messagebox de erro: "Usuário ou senha inválidos."

Arquivos criados ou modificados:

| Arquivo | Ação |
|---|---|
| `controllers/auth.py` | Novo — função de validação de login |
| `views/login.py` | Novo — tela de login com formulário |
| `main.py` | Modificado — agora importa e exibe a tela de login |

## 💻 Implementação Guiada

### Passo 1 — Criando a lógica de autenticação

Antes de desenhar a tela, vamos criar a camada que decide se o login é válido ou não. Isso pertence ao Controller.

Crie o arquivo `controllers/auth.py`:

```python
# ======================================================================
# auth.py — Controlador de Autenticação
# ======================================================================
# Eu sou responsável por validar as credenciais do usuário.
# Por enquanto, as credenciais estão em um dicionário fixo.
# No Capítulo 07, eu vou consultar o banco de dados SQLite.
# ======================================================================

from tkinter import messagebox

# ---------- CREDENCIAIS (PROVISÓRIO) ----------
# Eu guardo os usuários e senhas válidos do sistema.
# No futuro, estes dados estarão na tabela "usuarios" do banco.
USUARIOS = {
    "admin": "admin",
    "professor": "1234",
}


def validar_login(usuario, senha):
    """
    Eu valido as credenciais do usuário.

    Verifico se o usuário existe no dicionário e se a senha
    fornecida corresponde à senha cadastrada.

    Parâmetros:
        usuario: string com o nome de usuário digitado
        senha: string com a senha digitada

    Retorno:
        True se o login for válido, False caso contrário
    """
    # Eu verifico se o usuário existe no dicionário.
    if usuario in USUARIOS:
        # Eu comparo a senha digitada com a senha cadastrada.
        if USUARIOS[usuario] == senha:
            # Credenciais corretas!
            return True

    # Se cheguei até aqui, algo está errado.
    # Eu exibo uma mensagem de erro para o usuário.
    messagebox.showerror(
        "Erro de Login",
        "Usuário ou senha inválidos. Tente novamente."
    )
    return False
```

!!! note "Conceito Importante"
    Repare que a função `validar_login` não sabe nada sobre a interface. Ela não conhece Entry, Button ou Tkinter (exceto pelo messagebox). Isso é intencional: se amanhã você trocar Tkinter por outra biblioteca gráfica, a lógica de autenticação continua funcionando.

### Passo 2 — Criando a tela de login (View)

Agora vamos construir a interface. A tela de login será um Frame que preenche a janela principal e exibe o formulário centralizado.

Crie o arquivo `views/login.py`:

```python
# ======================================================================
# login.py — Tela de Login (View)
# ======================================================================
# Eu sou a tela de login do Sistema Escolar.
# Minha responsabilidade é exibir o formulário e capturar
# os dados digitados pelo usuário.
#
# Eu NÃO tomo decisões sobre autenticação — apenas repasso
# os dados para o controller (auth.py).
# ======================================================================

import tkinter as tk
from controllers.auth import validar_login


def criar_tela_login(janela):
    """
    Eu construo a tela de login dentro da janela principal.

    Crio um Frame que ocupa todo o espaço disponível e centralizo
    os widgets do formulário (Labels, Entries, Button) dentro dele.

    Parâmetros:
        janela: a instância de tk.Tk() ou tk.Toplevel() que me contém
    """
    # ---------- FRAME PRINCIPAL ----------
    # Eu sou o container que ocupa toda a janela.
    # Uso 'expand=True' e 'fill=tk.BOTH' para preencher todo o espaço.
    frame_fundo = tk.Frame(janela, bg="#f0f0f0")
    frame_fundo.pack(expand=True, fill=tk.BOTH)

    # ---------- FRAME DO FORMULÁRIO ----------
    # Eu sou o quadro branco que envolve o formulário.
    # Dou destaque visual com borda e fundo claro.
    frame_form = tk.Frame(
        frame_fundo,
        bg="white",
        bd=2,
        relief=tk.RIDGE,
        padx=30,
        pady=30
    )
    # Eu fico centralizado dentro do frame de fundo.
    frame_form.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # ---------- TÍTULO ----------
    # Eu sou o título do formulário, com fonte maior e em negrito.
    lbl_titulo = tk.Label(
        frame_form,
        text="🔐 Acesso ao Sistema",
        font=("Arial", 16, "bold"),
        bg="white",
        fg="#333333"
    )
    lbl_titulo.pack(pady=(0, 20))

    # ---------- CAMPO USUÁRIO ----------
    # Eu sou o label que identifica o campo de usuário.
    lbl_usuario = tk.Label(
        frame_form,
        text="Usuário:",
        font=("Arial", 11),
        bg="white",
        fg="#555555",
        anchor="w"
    )
    lbl_usuario.pack(fill=tk.X)

    # Eu sou o campo onde o usuário digita o nome.
    # Sou um Entry comum — aceito qualquer texto.
    entry_usuario = tk.Entry(
        frame_form,
        font=("Arial", 12),
        width=25,
        bd=2,
        relief=tk.SOLID
    )
    entry_usuario.pack(pady=(2, 12))
    # Eu coloco o foco automaticamente aqui quando a tela abre.
    entry_usuario.focus_set()

    # ---------- CAMPO SENHA ----------
    # Eu sou o label que identifica o campo de senha.
    lbl_senha = tk.Label(
        frame_form,
        text="Senha:",
        font=("Arial", 11),
        bg="white",
        fg="#555555",
        anchor="w"
    )
    lbl_senha.pack(fill=tk.X)

    # Eu sou o campo de senha.
    # A mágica está em show="*": cada caractere digitado aparece
    # como um asterisco, protegendo a senha de olhares curiosos.
    entry_senha = tk.Entry(
        frame_form,
        font=("Arial", 12),
        width=25,
        bd=2,
        relief=tk.SOLID,
        show="*"
    )
    entry_senha.pack(pady=(2, 20))

    # ---------- FUNÇÃO DE LOGIN ----------
    def ao_clicar_entrar():
        """
        Eu sou chamada quando o usuário clica no botão Entrar.

        Capturo os valores digitados, removo espaços extras
        e envio para o controller validar.
        """
        usuario = entry_usuario.get().strip()
        senha = entry_senha.get().strip()

        # Eu delego a validação para o controller.
        # A view não sabe COMO validar — apenas QUEM sabe.
        if validar_login(usuario, senha):
            # Login bem-sucedido.
            # Por enquanto, apenas mostro uma mensagem.
            # No Capítulo 04, aqui chamaremos a tela do Menu Principal.
            from tkinter import messagebox
            messagebox.showinfo(
                "Sucesso",
                f"Bem-vindo(a), {usuario}!"
            )

    # ---------- BOTÃO ENTRAR ----------
    # Eu sou o botão que dispara a autenticação.
    # Tenho uma cor de destaque e um padding interno confortável.
    btn_entrar = tk.Button(
        frame_form,
        text="Entrar",
        font=("Arial", 12, "bold"),
        bg="#4CAF50",
        fg="white",
        activebackground="#45a049",
        activeforeground="white",
        width=20,
        height=2,
        bd=0,
        cursor="hand2",
        command=ao_clicar_entrar
    )
    btn_entrar.pack(pady=(10, 0))

    # ---------- BIND DA TECLA ENTER ----------
    # Eu permito que o usuário pressione Enter no campo de senha
    # para acionar o login, sem precisar clicar no botão.
    entry_senha.bind("<Return>", lambda event: ao_clicar_entrar())
```

!!! tip "Dica Profissional"
    Note que o botão tem `cursor="hand2"`. Isso faz o cursor virar uma mãozinha ao passar sobre ele — um detalhe sutil de usabilidade que usuários esperam em sistemas modernos.

### Passo 3 — Atualizando o main.py

Agora precisamos conectar a tela de login ao ponto de entrada. O `main.py` deve importar e chamar a função `criar_tela_login`.

Abra o arquivo `main.py` que criamos no capítulo anterior. Vamos modificá-lo.

O código atual do `main.py` é:

```python
# ===== CÓDIGO EXISTENTE (Capítulo 02) =====
import tkinter as tk


def centralizar_janela(janela, largura, altura):
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    pos_x = (largura_tela // 2) - (largura // 2)
    pos_y = (altura_tela // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")


janela = tk.Tk()
janela.title("Sistema Escolar")
centralizar_janela(janela, 800, 600)
janela.resizable(False, False)

janela.mainloop()
```

Adicione a linha de import e a chamada da tela de login antes do `mainloop()`:

```python
# ===== CÓDIGO EXISTENTE (não altere) =====
import tkinter as tk


def centralizar_janela(janela, largura, altura):
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    pos_x = (largura_tela // 2) - (largura // 2)
    pos_y = (altura_tela // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")


janela = tk.Tk()
janela.title("Sistema Escolar")
centralizar_janela(janela, 800, 600)
janela.resizable(False, False)

# ===== CÓDIGO NOVO (adicione abaixo) =====
# Eu importo a função que constrói a tela de login.
from views.login import criar_tela_login

# Eu chamo a função, passando a janela principal como container.
# A tela de login será desenhada DENTRO desta janela.
criar_tela_login(janela)

# ===== LOOP PRINCIPAL (permanece igual) =====
janela.mainloop()
```

!!! note "A importação no meio do arquivo"
    Normalmente, imports ficam no topo. Colocamos aqui por questões didáticas — para destacar o que foi adicionado. No código final, sinta-se à vontade para mover o `from views.login import criar_tela_login` para o topo, junto com `import tkinter as tk`.

### Passo 4 — Executando e testando

Chegou a hora de ver o login em ação. No terminal, navegue até a pasta `sistema_escolar` e execute:

```bash
python main.py
```

Teste os seguintes cenários:

- Login correto: Digite `admin` / `admin` e clique em Entrar. Deve aparecer: "Bem-vindo(a), admin!"
- Login incorreto: Digite qualquer outra combinação. Deve aparecer: "Usuário ou senha inválidos."
- Segundo usuário: Digite `professor` / `1234`. Também deve funcionar.
- Campo vazio: Deixe os campos em branco e clique em Entrar. Deve exibir erro de login.
- Tecla Enter: Digite as credenciais e pressione Enter no campo de senha. O login deve ser acionado.

## 📝 Exercício

**Tempo estimado:** 15-20 minutos

**Tarefa:** Melhore a experiência do usuário adicionando uma validação extra: impeça que o usuário clique em "Entrar" com os campos vazios.

Em vez de depender apenas da mensagem de erro do controller, faça a própria view verificar se os campos estão preenchidos antes de chamar `validar_login`. Se algum campo estiver vazio, exiba um `messagebox.showwarning` pedindo para preencher todos os campos.

Dica: Modifique a função `ao_clicar_entrar()` dentro de `views/login.py`.

??? hint "Dica"
    Use `entry_usuario.get().strip()` e `entry_senha.get().strip()`. Se qualquer um dos dois for uma string vazia `("")`, exiba o aviso e interrompa a função com `return`.

??? success "Solução"
    Dentro de `views/login.py`, altere a função `ao_clicar_entrar`:
    
    ```python
    def ao_clicar_entrar():
        usuario = entry_usuario.get().strip()
        senha = entry_senha.get().strip()
    
        # ===== VALIDAÇÃO DE CAMPOS VAZIOS (novo) =====
        # Eu impeço que o usuário envie o formulário incompleto.
        if not usuario or not senha:
            messagebox.showwarning(
                "Campos Obrigatórios",
                "Por favor, preencha todos os campos antes de entrar."
            )
            return  # Interrompe a função aqui — não chama o controller.
        # =============================================
    
        if validar_login(usuario, senha):
            messagebox.showinfo(
                "Sucesso",
                f"Bem-vindo(a), {usuario}!"
            )
    ```
    
    Lembre-se de que `messagebox` já está importado no escopo da função (foi importado dentro dela no código original) ou você pode movê-lo para o topo do arquivo.

## 🏆 Missão da Equipe

**Tempo estimado:** 30-45 minutos

**Tarefa:** Criem a tela de login para o projeto da equipe de vocês.

**Entregável:** Os seguintes arquivos no projeto da equipe:

- `controllers/auth.py` — com dicionário de credenciais da equipe e função `validar_login`
- `views/login.py` — com a tela de login adaptada visualmente ao tema
- `main.py` — atualizado para exibir a tela de login ao iniciar

**Checklist da Missão:**

- [ ] O arquivo `controllers/auth.py` existe e contém pelo menos 2 usuários
- [ ] O arquivo `views/login.py` existe com formulário funcional
- [ ] O título do formulário reflete o nome do projeto da equipe
- [ ] O `main.py` importa e exibe a tela de login
- [ ] Login com credenciais corretas mostra mensagem de sucesso
- [ ] Login com credenciais erradas mostra mensagem de erro
- [ ] Os campos vazios são tratados (após o exercício)
- [ ] O professor executou e testou o login da equipe

**Sugestões de adaptação visual:**

- Mude o ícone ou texto do título (🔐 Acesso ao Sistema → 📚 Biblioteca Fácil, 📦 Controle de Estoque)
- Altere as cores dos botões e do fundo para combinar com o tema
- Adicione um logo ou nome do sistema fictício

!!! important "Nota para o Professor"
    Verifique: Cada equipe deve ter a tela de login funcional. Teste com credenciais corretas e erradas. Confira se os arquivos estão organizados nas pastas corretas e se a estrutura MVC está sendo seguida.

## ⚡ Desafio

**Vá além:** Adicione um botão "Mostrar/Ocultar Senha" ao lado do campo de senha.

Funcionalidade esperada:

- Um pequeno botão ou checkbox que, quando pressionado, revela a senha digitada (remove `show="*"`)
- Quando solto ou desmarcado, volta a ocultar com asteriscos
- Dica: use `entry_senha.config(show="")` para mostrar e `entry_senha.config(show="*")` para ocultar

Exemplo de implementação com botão que alterna:

```python
# Variável de controle (adicione antes da função ao_clicar_entrar)
senha_visivel = False

def alternar_visibilidade():
    nonlocal senha_visivel
    senha_visivel = not senha_visivel
    if senha_visivel:
        entry_senha.config(show="")
        btn_olho.config(text="🙈")
    else:
        entry_senha.config(show="*")
        btn_olho.config(text="👁️")

# Botão ao lado do campo de senha
btn_olho = tk.Button(frame_form, text="👁️", command=alternar_visibilidade, ...)
```

## ⚠️ Erros Comuns

!!! danger "Esquecer de criar os arquivos nas pastas corretas"
    **Sintoma:** `ModuleNotFoundError: No module named 'controllers.auth'` ao executar `main.py`.
    
    **Causa:** Os arquivos `auth.py` e `login.py` foram criados na raiz do projeto, e não dentro das pastas `controllers/` e `views/`.
    
    **Solução:** Verifique se `auth.py` está dentro de `sistema_escolar/controllers/` e `login.py` dentro de `sistema_escolar/views/`. O caminho no import deve corresponder exatamente à localização do arquivo.

!!! warning "Import circular"
    **Sintoma:** `ImportError: cannot import name 'validar_login' from partially initialized module`.
    
    **Causa:** O arquivo `login.py` importa de `auth.py` e `auth.py` tenta importar algo de `login.py` (direta ou indiretamente).
    
    **Solução:** Mantenha o fluxo de dependência em um único sentido: View → Controller → Model. A View pode importar do Controller, mas o Controller nunca deve importar da View.

!!! danger "Não usar show='*' no campo de senha"
    **Sintoma:** A senha aparece em texto legível na tela — qualquer pessoa ao lado pode vê-la.
    
    **Causa:** O parâmetro `show` foi esquecido ao criar o Entry da senha.
    
    **Solução:** Sempre defina `show="*"` ao criar campos de senha. É uma linha que faz toda a diferença em segurança visual.

!!! warning "Limpar os campos após erro"
    **Sintoma:** Após uma tentativa de login incorreta, o campo de senha mantém o valor digitado.
    
    **Causa:** A função de validação não limpa os campos em caso de falha.
    
    **Solução:** Dentro de `ao_clicar_entrar`, após chamar `validar_login`, se o retorno for `False`, limpe o campo de senha com `entry_senha.delete(0, tk.END)` e coloque o foco de volta com `entry_senha.focus_set()`. É uma melhoria de usabilidade.

## 💡 Boas Práticas

**1. Separação clara entre View e Controller**

A função `criar_tela_login` (View) não sabe validar credenciais. A função `validar_login` (Controller) não sabe que existe uma Entry. Essa separação permite que você modifique a interface sem afetar a lógica, e vice-versa. No mercado, essa é a base de arquiteturas como MVC, MVP e MVVM.

**2. Credenciais em dicionário (por enquanto)**

Deixamos explícito nos comentários que o dicionário `USUARIOS` é provisório. Isso prepara mentalmente você para a migração ao banco de dados. Em projetos reais, nunca se deve hardcodar senhas — mas para este estágio de protótipo, é aceitável.

**3. Tratamento de entradas com .strip()**

Usamos `.strip()` nos valores de `entry_usuario.get()` e `entry_senha.get()`. Isso remove espaços em branco acidentais que o usuário possa digitar no início ou fim do campo. É um detalhe que demonstra preocupação com a experiência do usuário.

**4. Bind da tecla Enter**

Adicionar `entry_senha.bind("<Return>", ...)` permite que o usuário faça login pressionando Enter. É um padrão esperado em formulários e reduz o atrito da navegação mouse-teclado.

**5. Cores e cursores**

Usamos `bg="#4CAF50"` (verde) para o botão de ação principal e `cursor="hand2"` para feedback visual. São microinterações que, somadas, tornam o sistema mais profissional. Frameworks como CustomTkinter levam isso ainda mais longe, mas Tkinter puro já permite esse polimento.

## ☑️ Checklist

Antes de prosseguir para o próximo capítulo, confirme:

- [ ] O arquivo `controllers/auth.py` existe e contém a função `validar_login`
- [ ] O arquivo `views/login.py` existe e contém a função `criar_tela_login`
- [ ] O `main.py` importa e chama `criar_tela_login(janela)`
- [ ] A tela de login abre centralizada dentro da janela principal
- [ ] O campo de senha exibe asteriscos ao digitar
- [ ] Login com admin / admin mostra mensagem de sucesso
- [ ] Login com credenciais erradas mostra mensagem de erro
- [ ] Pressionar Enter no campo de senha aciona o login
- [ ] Os comentários explicam a intenção do código, não a sintaxe
- [ ] Minha equipe concluiu a Missão da Equipe para o projeto dela

## ➡️ Próximo Capítulo

No **Capítulo 04 — Menu Principal**, você construirá a central de navegação do sistema. Após o login bem-sucedido, a tela de login será substituída por um menu com botões para Cadastro, Consulta e Sair.

Você aprenderá a fazer transição entre telas — ou seja, como "apagar" a tela de login e "desenhar" o menu no mesmo espaço. Esse é o primeiro passo para criar um sistema com múltiplas telas sem abrir janelas pop-up descontroladas.

Prepare-se: revise a criação de botões (`Button`) e o método `pack_forget()` ou `destroy()` para remover widgets. A mágica da navegação está logo ali. 🧭
