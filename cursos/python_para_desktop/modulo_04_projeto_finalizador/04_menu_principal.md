# 04 — Menu Principal

## 🎯 Objetivo

Neste capítulo você vai construir o Menu Principal do Sistema Escolar — a central de navegação que aparece logo após o login bem-sucedido.

Ao final, você terá:

- Uma tela de menu com botões para Cadastrar Alunos, Consultar Alunos e Sair
- Um botão Sair que pergunta confirmação antes de fechar o sistema
- A transição completa: Login → Menu Principal
- O código organizado no novo módulo `views/menu.py`
- A função de criação de tela de login agora aceita um callback de sucesso, permitindo que o `main.py` decida o que fazer após a autenticação

## 📍 Contextualização

No Capítulo 03, você criou a tela de login com campos de usuário e senha. A autenticação funcionava, mas ao fazer login correto o sistema apenas exibia um messagebox de boas-vindas. Faltava o próximo passo: levar o usuário para a área de trabalho do sistema.

Agora, você construirá essa área de trabalho — o Menu Principal. Ele será o centro de comando do Sistema Escolar: todos os caminhos (cadastrar, consultar, sair) partem daqui.

Você também aprenderá a conectar duas telas dentro da mesma janela, usando um padrão profissional: callback de navegação.

**Progresso do Sistema:**

```text
✅ Capítulo 01 — Introdução e Planejamento
✅ Capítulo 02 — Arquitetura do Sistema
✅ Capítulo 03 — Tela de Login
🔨 Menu Principal ← VOCÊ ESTÁ AQUI
⬜ Múltiplas Janelas
⬜ Cadastro de Alunos
⬜ SQLite Local
⬜ CRUD Completo
⬜ Banco em Nuvem
⬜ Integração e Testes
⬜ Refatoração e Entrega
```

## ✅ Resultado Esperado

Após o login com admin / admin, a janela será limpa e o Menu Principal aparecerá. Visualmente:

```text
┌──────────────────────────────────────────────┐
│  Sistema Escolar                         _ □ X│
│                                              │
│           ┌────────────────────────┐         │
│           │  MENU PRINCIPAL        │         │
│           │  Sistema Escolar       │         │
│           │                        │         │
│           │  ┌──────────────────┐  │         │
│           │  │ Cadastrar Alunos │  │         │
│           │  └──────────────────┘  │         │
│           │  ┌──────────────────┐  │         │
│           │  │ Consultar Alunos │  │         │
│           │  └──────────────────┘  │         │
│           │  ┌──────────────────┐  │         │
│           │  │      Sair        │  │         │
│           │  └──────────────────┘  │         │
│           └────────────────────────┘         │
│                                              │
└──────────────────────────────────────────────┘
```

Comportamento esperado:

- Ao clicar em Cadastrar Alunos: exibe um messagebox informando "Funcionalidade em construção" (será implementada no Capítulo 06).
- Ao clicar em Consultar Alunos: mesma mensagem.
- Ao clicar em Sair: abre uma caixa de confirmação. Se o usuário confirmar, o sistema fecha completamente.

Arquivos criados ou modificados:

| Arquivo | Ação |
|---|---|
| `views/menu.py` | Novo — tela do menu principal |
| `views/login.py` | Modificado — adiciona parâmetro `on_success` |
| `main.py` | Modificado — implementa transição Login → Menu |

## 💻 Implementação Guiada

### Passo 1 — Criando a tela do Menu Principal

O menu será um Frame que ocupa a janela e exibe botões grandes e bem organizados. Cada botão terá uma cor e um tamanho que transmitam profissionalismo.

Crie o arquivo `views/menu.py`:

```python
# ======================================================================
# menu.py — Tela do Menu Principal (View)
# ======================================================================
# Eu sou a tela de Menu Principal do Sistema Escolar.
# Minha responsabilidade é exibir as opções de navegação
# e direcionar o usuário para a funcionalidade desejada.
#
# Por enquanto, apenas o botão "Sair" tem ação real.
# Os demais serão conectados nos próximos capítulos.
# ======================================================================

import tkinter as tk
from tkinter import messagebox


def criar_menu(janela):
    """
    Eu construo o Menu Principal dentro da janela fornecida.

    Limpo qualquer widget existente na janela e desenho
    o menu com título e botões de navegação.

    Parâmetros:
        janela: a instância de tk.Tk() que me contém
    """
    # ---------- LIMPEZA DA JANELA ----------
    # Eu removo todos os widgets que estavam na janela antes.
    # Isso garante que, ao fazer login, a tela de login suma
    # e o menu ocupe o espaço inteiro.
    for widget in janela.winfo_children():
        widget.destroy()

    # ---------- FRAME PRINCIPAL ----------
    # Eu sou o container que preenche toda a janela.
    frame_fundo = tk.Frame(janela, bg="#e8f0fe")
    frame_fundo.pack(expand=True, fill=tk.BOTH)

    # ---------- FRAME DO MENU ----------
    # Eu centralizo o menu visualmente dentro da janela.
    frame_menu = tk.Frame(
        frame_fundo,
        bg="white",
        bd=2,
        relief=tk.RIDGE,
        padx=40,
        pady=40
    )
    frame_menu.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # ---------- TÍTULO ----------
    # Eu sou o título do menu, com fonte grande e cor sóbria.
    lbl_titulo = tk.Label(
        frame_menu,
        text="MENU PRINCIPAL",
        font=("Arial", 20, "bold"),
        bg="white",
        fg="#2c3e50"
    )
    lbl_titulo.pack(pady=(0, 5))

    # ---------- SUBTÍTULO ----------
    # Eu reforço qual sistema está sendo utilizado.
    lbl_subtitulo = tk.Label(
        frame_menu,
        text="Sistema Escolar",
        font=("Arial", 12),
        bg="white",
        fg="#7f8c8d"
    )
    lbl_subtitulo.pack(pady=(0, 30))

    # ---------- BOTÕES DE NAVEGAÇÃO ----------
    # Cada botão é um caminho para uma funcionalidade do sistema.
    # Eu uso um dicionário para definir as propriedades dos botões
    # e depois os crio em um loop — mais limpo e fácil de manter.

    botoes_config = {
        "Cadastrar Alunos": {
            "bg": "#3498db",
            "fg": "white",
            "activebackground": "#2980b9",
            "comando": lambda: messagebox.showinfo(
                "Em breve",
                "Funcionalidade de Cadastro será implementada no Capítulo 06."
            )
        },
        "Consultar Alunos": {
            "bg": "#2ecc71",
            "fg": "white",
            "activebackground": "#27ae60",
            "comando": lambda: messagebox.showinfo(
                "Em breve",
                "Funcionalidade de Consulta será implementada no Capítulo 06."
            )
        },
        "Sair": {
            "bg": "#e74c3c",
            "fg": "white",
            "activebackground": "#c0392b",
            "comando": lambda: ao_clicar_sair(janela)
        }
    }

    for texto, config in botoes_config.items():
        btn = tk.Button(
            frame_menu,
            text=texto,
            font=("Arial", 13, "bold"),
            bg=config["bg"],
            fg=config["fg"],
            activebackground=config["activebackground"],
            activeforeground="white",
            width=25,
            height=2,
            bd=0,
            cursor="hand2",
            command=config["comando"]
        )
        btn.pack(pady=8)


def ao_clicar_sair(janela):
    """
    Eu pergunto ao usuário se ele realmente deseja sair.
    Se confirmar, fecho o sistema completamente.
    """
    # Eu exibo uma caixa de diálogo Sim/Não.
    resposta = messagebox.askyesno(
        "Confirmar Saída",
        "Tem certeza que deseja sair do sistema?"
    )
    if resposta:
        # Eu destruo a janela principal, encerrando o mainloop.
        janela.destroy()
```

!!! tip "Dica Profissional"
    O uso de um dicionário (`botoes_config`) para definir as propriedades de cada botão evita repetição de código. À medida que o sistema crescer, fica fácil adicionar novos botões apenas inserindo uma nova entrada no dicionário.

### Passo 2 — Preparando o Login para a transição

Atualmente, a função `criar_tela_login` em `views/login.py` mostra um messagebox quando o login é bem-sucedido. Precisamos modificar essa função para que ela aceite um callback — uma função que será chamada em caso de sucesso. Assim, quem decide o que acontece depois do login é o `main.py`, não a própria tela de login.

Abra `views/login.py`. Vamos modificar a assinatura da função e o corpo de `ao_clicar_entrar`.

Trecho a ser alterado — assinatura da função (linha ~14):

```python
# ===== CÓDIGO EXISTENTE =====
def criar_tela_login(janela):

# ===== CÓDIGO NOVO (modifique a assinatura) =====
def criar_tela_login(janela, on_success=None):
    """
    Eu construo a tela de login dentro da janela principal.

    Parâmetros:
        janela: a instância de tk.Tk() que me contém
        on_success: função opcional a ser chamada após login bem-sucedido.
                    Se fornecida, recebe o nome de usuário como argumento.
    """
```

Trecho a ser alterado — `ao_clicar_entrar` (dentro da função, substitua):

```python
# ===== CÓDIGO EXISTENTE (trecho) =====
        if validar_login(usuario, senha):
            # Login bem-sucedido.
            from tkinter import messagebox
            messagebox.showinfo(
                "Sucesso",
                f"Bem-vindo(a), {usuario}!"
            )

# ===== CÓDIGO NOVO (substitua a partir do if) =====
        if validar_login(usuario, senha):
            # Login bem-sucedido! Eu verifico se alguém me passou
            # uma função para executar após o sucesso.
            if on_success is not None:
                # Eu chamo a função de callback, passando o nome do usuário.
                # Isso permite que o main.py decida o que fazer (ex: abrir menu).
                on_success(usuario)
            else:
                # Comportamento padrão: apenas uma mensagem de boas-vindas.
                # Isso mantém a tela de login funcional mesmo sem callback.
                from tkinter import messagebox
                messagebox.showinfo(
                    "Sucesso",
                    f"Bem-vindo(a), {usuario}!"
                )
```

!!! note "Conceito Importante"
    O parâmetro `on_success` é um callback — uma função passada como argumento. Esse padrão é extremamente comum em interfaces gráficas: a view não sabe o que fazer com o resultado, apenas notifica quem a chamou.

### Passo 3 — Atualizando o main.py para orquestrar a transição

Agora o `main.py` será o maestro. Ele criará a tela de login e, quando o login for bem-sucedido, chamará a função que desenha o menu.

Abra `main.py` e modifique-o conforme abaixo. O código existente do Capítulo 03 continua, apenas adicionamos a função `abrir_menu` e alteramos a chamada de `criar_tela_login`.

```python
# ===== CÓDIGO EXISTENTE (Capítulo 03) =====
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
# Eu importo as funções que criam as telas.
from views.login import criar_tela_login
from views.menu import criar_menu


# Eu defino a função que será chamada após o login bem-sucedido.
def abrir_menu(usuario):
    """
    Eu sou a função de callback.
    Quando o login for bem-sucedido, eu:
      1. Limpo a janela (removendo a tela de login)
      2. Desenho o Menu Principal
    Parâmetros:
        usuario: nome do usuário que acabou de logar (string)
    """
    # Eu delego a criação do menu para a view correspondente.
    criar_menu(janela)


# Eu inicio o sistema exibindo a tela de login.
# Passo a função 'abrir_menu' como callback — ela será chamada
# automaticamente pela tela de login quando as credenciais estiverem corretas.
criar_tela_login(janela, on_success=abrir_menu)


# ===== LOOP PRINCIPAL (permanece igual) =====
janela.mainloop()
```

### Passo 4 — Executando e testando o fluxo completo

Execute o sistema:

```bash
python main.py
```

Teste o fluxo:

- A tela de login aparece normalmente.
- Digite admin / admin e clique em Entrar.
- A tela de login desaparece e o Menu Principal ocupa a janela.
- Clique em Cadastrar Alunos → mensagem "Em breve".
- Clique em Consultar Alunos → mensagem "Em breve".
- Clique em Sair → pergunta "Tem certeza que deseja sair?".
    - Se clicar Sim, a janela fecha.
    - Se clicar Não, nada acontece e o menu permanece.

Parabéns! Você acaba de implementar a navegação básica do sistema usando callback — um padrão que será reutilizado em todas as transições de tela.

## 📝 Exercício

**Tempo estimado:** 15-20 minutos

**Tarefa:** Modifique o menu para que, ao invés de mostrar messagebox "Em construção", o botão Cadastrar Alunos volte para a tela de login (como se fosse um "logout").

Dica: Dentro do dicionário `botoes_config`, altere o comando do botão "Cadastrar Alunos" para chamar uma função que limpa a janela e chama `criar_tela_login` novamente. Lembre-se de que você precisará importar `criar_tela_login` no `menu.py` ou passar uma referência.

??? hint "Dica"
    Uma solução simples é fazer o `main.py` passar uma função `voltar_login` para `criar_menu`, assim como passamos `abrir_menu` para `criar_tela_login`. Mas para este exercício, pode criar a função diretamente no `menu.py` usando `from views.login import criar_tela_login` e chamá-la com `criar_tela_login(janela)`. Isso fará o login reaparecer.

??? success "Solução"
    Em `views/menu.py`, adicione no topo:
    
    ```python
    from views.login import criar_tela_login
    ```
    
    Depois, crie uma função auxiliar antes de `criar_menu`:
    
    ```python
    def voltar_login(janela):
        # Limpa e exibe a tela de login novamente.
        criar_tela_login(janela)
    ```
    
    No dicionário `botoes_config`, altere o comando de "Cadastrar Alunos":
    
    ```python
    "Cadastrar Alunos": {
        "bg": "#3498db",
        "fg": "white",
        "activebackground": "#2980b9",
        "comando": lambda: voltar_login(janela)
    },
    ```
    
    Agora, ao clicar em "Cadastrar Alunos", a tela de login reaparece. Note que o callback `on_success` não foi passado, então o login usará o comportamento padrão (messagebox).

## 🏆 Missão da Equipe

**Tempo estimado:** 30-45 minutos

**Tarefa:** Criem o Menu Principal para o projeto da equipe, com botões que reflitam as funcionalidades do sistema de vocês.

**Entregável:** O arquivo `views/menu.py` funcional e o `main.py` atualizado com a transição Login → Menu.

**Checklist da Missão:**

- [ ] O arquivo `views/menu.py` existe e contém a função `criar_menu`
- [ ] O menu possui botões adequados ao tema da equipe (ex: "Cadastrar Livros", "Consultar Livros", "Sair")
- [ ] O botão Sair pergunta confirmação antes de fechar
- [ ] O `main.py` implementa a função de callback para abrir o menu
- [ ] O fluxo completo funciona: Login → Menu → Sair
- [ ] Os botões que ainda não têm funcionalidade mostram uma mensagem adequada
- [ ] O visual está adaptado (cores, títulos, ícones)
- [ ] O professor executou e testou o menu da equipe

!!! important "Nota para o Professor"
    Verifique: Cada equipe deve ter um menu com botões que correspondam às funcionalidades planejadas. O fluxo Login → Menu deve estar completo. Observe se a transição está sendo feita com callback, e não com abertura de novas janelas Toplevel (isso será abordado no próximo capítulo, mas o ideal é limpar e redesenhar na mesma janela).

## ⚡ Desafio

**Vá além:** Adicione ao menu um label de boas-vindas que exiba o nome do usuário que acabou de fazer login.

Por exemplo: "Bem-vindo, admin!" abaixo do subtítulo.

Para isso, você precisará:

- Modificar a função `criar_menu` para receber o nome do usuário como parâmetro (`criar_menu(janela, usuario)`)
- No `main.py`, em `abrir_menu(usuario)`, passar `usuario` para `criar_menu(janela, usuario)`
- No `menu.py`, criar um Label adicional com o texto formatado.

Exemplo de implementação do Label:

```python
lbl_boasvindas = tk.Label(
    frame_menu,
    text=f"Bem-vindo, {usuario}!",
    font=("Arial", 12, "italic"),
    bg="white",
    fg="#27ae60"
)
lbl_boasvindas.pack(pady=(0, 20))
```

Isso torna o sistema mais pessoal e profissional.

## ⚠️ Erros Comuns

!!! danger "Esquecer de limpar a janela antes de desenhar o menu"
    **Sintoma:** Os widgets da tela de login aparecem misturados com os do menu — uma bagunça visual.
    
    **Causa:** A função `criar_menu` não chama `widget.destroy()` nos filhos da janela antes de criar o novo Frame.
    
    **Solução:** Inclua sempre o loop `for widget in janela.winfo_children(): widget.destroy()` no início de `criar_menu`. Isso garante uma janela limpa.

!!! warning "Callback não executado porque on_success é None"
    **Sintoma:** Após login bem-sucedido, nada acontece — nem mensagem, nem menu.
    
    **Causa:** O `main.py` esqueceu de passar o argumento `on_success=abrir_menu` ao chamar `criar_tela_login`.
    
    **Solução:** Verifique a chamada: `criar_tela_login(janela, on_success=abrir_menu)`. O parâmetro `on_success` deve estar presente.

!!! danger "Fechar a janela errada com destroy()"
    **Sintoma:** Ao clicar em "Sair", o sistema fecha, mas aparece um erro `_tkinter.TclError: invalid command name`.
    
    **Causa:** O código tenta interagir com a janela depois que ela foi destruída, ou o mainloop continua tentando processar eventos.
    
    **Solução:** O `janela.destroy()` deve ser a última ação antes do término do mainloop. Não coloque código depois dele. No nosso caso, a função `ao_clicar_sair` é acionada por um botão, e depois que a janela é destruída, o mainloop encerra naturalmente.

!!! warning "Importações circulares entre login.py e menu.py"
    **Sintoma:** `ImportError: cannot import name 'criar_menu' from partially initialized module 'views.menu'`.
    
    **Causa:** O arquivo `login.py` importa algo de `menu.py` e `menu.py` importa algo de `login.py`, criando um ciclo.
    
    **Solução:** Mantenha a dependência em uma única direção: `login.py` não deve conhecer `menu.py`. Apenas o `main.py` (ou um controller) conhece ambas as views e faz a orquestração. No nosso código, `menu.py` importa de `login.py` apenas no exercício — para produção, o ideal é usar callback.

## 💡 Boas Práticas

**1. Callbacks desacoplam as views**

O padrão de passar uma função como argumento (`on_success`) permite que a tela de login não precise saber o que vem depois dela. Isso facilita a manutenção: se amanhã você quiser que, após o login, o sistema vá direto para uma tela de dashboard, basta trocar a função callback no `main.py`. A view de login permanece inalterada.

**2. Um único ponto de orquestração (main.py)**

O `main.py` é o único lugar que conhece todas as telas e decide a ordem de navegação. Isso evita que as views se importem mutuamente e criem dependências cíclicas. Esse princípio é chamado de Inversão de Controle.

**3. Limpeza explícita da janela**

Destruir os widgets antigos antes de criar novos garante que não haja vazamento de memória (memory leak) e que o layout fique sempre limpo. Em sistemas maiores, pode-se usar `pack_forget()` para esconder em vez de destruir, mas `destroy()` é mais simples e seguro para o nosso escopo.

**4. Confirmação antes de ações destrutivas**

O botão "Sair" utiliza `messagebox.askyesno` para confirmar a ação. Isso é uma regra de ouro de usabilidade: qualquer ação que resulte em perda de dados ou fechamento do sistema deve ser confirmada pelo usuário.

**5. Dicionários para configuração de widgets**

Usar um dicionário para definir as propriedades dos botões torna o código mais legível e fácil de modificar. Adicionar um novo botão é apenas uma questão de adicionar uma entrada, sem precisar repetir toda a estrutura de criação do Button.

## ☑️ Checklist

Antes de prosseguir para o próximo capítulo, confirme:

- [ ] O arquivo `views/menu.py` existe e contém a função `criar_menu`
- [ ] O menu exibe três botões: Cadastrar Alunos, Consultar Alunos, Sair
- [ ] O botão Sair exibe confirmação e fecha o sistema se confirmado
- [ ] Os botões Cadastrar e Consultar exibem mensagem "Em construção"
- [ ] O arquivo `views/login.py` foi modificado para aceitar o callback `on_success`
- [ ] O `main.py` define `abrir_menu` e a passa para `criar_tela_login`
- [ ] O fluxo Login → Menu funciona sem erros
- [ ] A tela de login é removida antes de desenhar o menu
- [ ] Os comentários do código explicam a intenção
- [ ] Minha equipe concluiu a Missão da Equipe

## ➡️ Próximo Capítulo

No **Capítulo 05 — Múltiplas Janelas**, você aprenderá a gerenciar aberturas de telas em janelas separadas (usando `Toplevel`) e a controlar o fluxo de navegação de forma profissional. Isso preparará o terreno para a tela de Cadastro, que exigirá uma janela independente com formulário e tabela.

Até lá, revise o que é `Toplevel` e como passar dados entre janelas. O sistema está ganhando forma! 🧩
