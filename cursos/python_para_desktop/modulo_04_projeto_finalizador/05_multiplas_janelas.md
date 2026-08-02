# 05 — Múltiplas Janelas

## 🎯 Objetivo

Neste capítulo você vai dominar a navegação entre múltiplas janelas de forma profissional — o último passo antes de construir as telas de funcionalidade real.

Ao final, você terá:

- Refatorado a transição Login → Menu para usar `withdraw()` e `deiconify()` em vez de destruir widgets
- Criado a função `centralizar_janela` reutilizável em `utils/helpers.py`
- Implementado abertura de janelas com `Toplevel` para as telas de funcionalidade
- Controle de duplicação: impedir que a mesma janela seja aberta duas vezes
- Interceptação do botão X (`protocol("WM_DELETE_WINDOW")`) para fechar corretamente

## 📍 Contextualização

No Capítulo 04, você implementou o Menu Principal e conectou o login a ele usando callbacks. A transição funcionava, mas com uma abordagem "bruta": a função `criar_menu` destruía todos os widgets da janela e redesenhava o conteúdo.

Isso funciona para um sistema com apenas duas telas. Mas agora que o Menu terá várias opções (Cadastrar, Consultar), e cada uma abrirá uma tela diferente, precisamos de um mecanismo mais flexível: janelas independentes que abrem e fecham sem destruir a principal.

Você aprenderá os conceitos fundamentais de gerenciamento de janelas em Tkinter — habilidades que separam amadores de profissionais.

**Progresso do Sistema:**

```text
✅ Capítulo 01 — Introdução e Planejamento
✅ Capítulo 02 — Arquitetura do Sistema
✅ Capítulo 03 — Tela de Login
✅ Capítulo 04 — Menu Principal
🔨 Múltiplas Janelas ← VOCÊ ESTÁ AQUI
⬜ Cadastro de Alunos
⬜ SQLite Local
⬜ CRUD Completo
⬜ Banco em Nuvem
⬜ Integração e Testes
⬜ Refatoração e Entrega
```

## ✅ Resultado Esperado

Após este capítulo, seu sistema terá uma navegação fluida:

- A janela principal abre com a tela de login
- Ao fazer login, a janela principal é ocultada e o menu aparece
- Clicar em "Cadastrar Alunos" abre uma nova janela (Toplevel) centralizada, com título "Cadastro de Alunos"
- Fechar essa janela (pelo X ou botão "Voltar") retorna ao menu
- Se o usuário tentar abrir "Cadastrar Alunos" duas vezes, a segunda tentativa é ignorada
- O botão X de qualquer janela é tratado adequadamente

```text
┌─────────────────────────┐     ┌─────────────────────────┐
│     Janela Principal    │     │    Janela Secundária    │
│     (oculta/mostra)     │     │    (Toplevel)           │
│                         │     │                         │
│  Login ──▶ Menu         │     │  Cadastro de Alunos     │
│            │            │     │                         │
│            └────────────┼────▶│  (abre ao clicar)       │
│                         │     │                         │
│                         │     │  (fecha e volta)        │
└─────────────────────────┘     └─────────────────────────┘
```

Arquivos criados ou modificados:

| Arquivo | Ação |
|---|---|
| `utils/helpers.py` | Novo — função `centralizar_janela` reutilizável |
| `views/menu.py` | Modificado — botões agora abrem Toplevel com placeholder |
| `views/login.py` | Modificado — usa `withdraw()` em vez de `destroy()` |
| `main.py` | Modificado — refatorado para usar withdraw/deiconify, importa de utils |

## 💻 Implementação Guiada

### Passo 1 — Por que não usar múltiplas instâncias de Tk()?

Antes de programar, um conceito essencial.

`tk.Tk()` cria a janela raiz do Tkinter. Ela é única — você pode ter apenas uma instância por aplicação. Se tentar criar uma segunda:

```python
janela1 = tk.Tk()
janela2 = tk.Tk()  # ❌ ERRADO!
```

Você terá duas janelas independentes, mas com comportamentos imprevisíveis (variáveis de controle duplicadas, dois loops de eventos conflitantes, etc.). A documentação do Tkinter é clara: apenas um `Tk()` por aplicação.

A solução para janelas adicionais é o `Toplevel` — uma janela filha que compartilha o mesmo interpretador Tcl/Tk da janela principal.

```python
janela_principal = tk.Tk()        # ✅ Janela raiz
janela_cadastro = tk.Toplevel()   # ✅ Janela filha
```

!!! danger "Erro Crítico"
    Nunca crie uma segunda instância de `Tk()`. Sempre use `Toplevel` para novas janelas. Ignorar essa regra pode causar travamentos e comportamentos bizarros difíceis de depurar.

### Passo 2 — Extraindo centralizar_janela para utils/helpers.py

Atualmente, a função `centralizar_janela` está definida dentro de `main.py`. Ela será útil em todas as janelas do sistema, então merece seu próprio módulo reutilizável.

Crie o arquivo `utils/helpers.py`:

```python
# ======================================================================
# helpers.py — Funções Utilitárias
# ======================================================================
# Eu sou um módulo de funções auxiliares reutilizáveis.
# Qualquer parte do sistema pode me importar.
# ======================================================================


def centralizar_janela(janela, largura, altura):
    """
    Eu centralizo qualquer janela na tela do usuário.

    Funciono com tk.Tk() e tk.Toplevel() — ambos possuem
    os métodos winfo_screenwidth() e winfo_screenheight().

    Parâmetros:
        janela: instância de Tk ou Toplevel
        largura: largura desejada da janela (ex: 800)
        altura: altura desejada da janela (ex: 600)
    """
    # Eu obtenho a resolução do monitor do usuário.
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()

    # Eu calculo a posição X e Y para o centro.
    pos_x = (largura_tela // 2) - (largura // 2)
    pos_y = (altura_tela // 2) - (altura // 2)

    # Eu aplico a geometria no formato "LARGURAxALTURA+X+Y".
    janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")
```

Agora, onde quer que você precise centralizar uma janela, basta:

```python
from utils.helpers import centralizar_janela
centralizar_janela(minha_janela, 800, 600)
```

!!! tip "Dica Profissional"
    Centralizar funções utilitárias em um módulo `utils` é uma prática padrão na indústria. Evita duplicação de código e facilita a manutenção: se um dia você quiser melhorar a lógica de centralização, altera apenas um arquivo.

### Passo 3 — Refatorando main.py para usar withdraw/deiconify

Atualmente, a transição Login → Menu usa `widget.destroy()` dentro de `criar_menu`. Vamos substituir essa abordagem por um controle de visibilidade mais elegante.

A estratégia:

- A janela principal (`janela`) estará sempre viva, mas ora visível, ora oculta.
- `janela.withdraw()` → esconde a janela (ela continua existindo na memória).
- `janela.deiconify()` → mostra a janela novamente.
- Limpamos os widgets manualmente quando necessário, mas mantemos a janela.

Altere o arquivo `main.py`:

```python
# ======================================================================
# main.py — Ponto de Entrada do Sistema Escolar
# ======================================================================
# Eu sou o orquestrador do sistema.
# Controlo a visibilidade da janela principal e a navegação entre telas.
# ======================================================================

import tkinter as tk
from utils.helpers import centralizar_janela
from views.login import criar_tela_login
from views.menu import criar_menu


# ---------- JANELA PRINCIPAL ----------
# Eu crio a única instância de Tk() de todo o sistema.
janela = tk.Tk()
janela.title("Sistema Escolar")
centralizar_janela(janela, 800, 600)
janela.resizable(False, False)


# ---------- CALLBACKS DE NAVEGAÇÃO ----------
def abrir_menu(usuario):
    """
    Eu sou chamada após o login bem-sucedido.
    Limpo a janela principal e desenho o Menu.
    """
    # Eu removo todos os widgets da tela de login.
    for widget in janela.winfo_children():
        widget.destroy()
    # Eu desenho o menu no lugar.
    criar_menu(janela)


def voltar_login():
    """
    Eu sou chamada quando o usuário faz logout.
    Limpo a janela principal e redesenho a tela de login.
    """
    # Eu removo todos os widgets do menu.
    for widget in janela.winfo_children():
        widget.destroy()
    # Eu desenho a tela de login, passando abrir_menu como callback.
    criar_tela_login(janela, on_success=abrir_menu)


# ---------- INICIALIZAÇÃO ----------
# Eu inicio o sistema exibindo a tela de login.
criar_tela_login(janela, on_success=abrir_menu)

# Eu mantenho a janela principal sempre viva.
janela.mainloop()
```

!!! note "Mudança de filosofia"
    Antes, a função `criar_menu` limpava a janela sozinha. Agora, a responsabilidade de limpar é do `main.py` (no callback `abrir_menu`). Isso mantém as views mais puras: cada uma só desenha seu conteúdo, sem se preocupar com o que havia antes.

### Passo 4 — Refatorando views/login.py

A tela de login não precisa de grandes mudanças — a lógica de callback já está implementada. Apenas removemos qualquer `destroy()` que porventura exista dentro dela (no nosso código do Capítulo 04, o `destroy()` estava em `criar_menu`, não em `criar_tela_login`, então está ok).

Mas vamos garantir que o código esteja alinhado com a nova abordagem. O arquivo `views/login.py` permanece com a função `criar_tela_login(janela, on_success=None)` como no capítulo anterior. A diferença é que agora `on_success` será chamado pelo `main.py`, que limpará a janela antes de desenhar o menu.

Nenhuma alteração necessária em `views/login.py` neste capítulo.

### Passo 5 — Atualizando views/menu.py para abrir janelas com Toplevel

Agora o menu precisa abrir janelas secundárias para cada funcionalidade. Vamos substituir os messagebox "Em construção" por aberturas reais de Toplevel com conteúdo placeholder.

Também implementaremos controle de duplicação: se a janela já estiver aberta, não abrimos outra.

Atualize `views/menu.py`:

```python
# ======================================================================
# menu.py — Tela do Menu Principal (View)
# ======================================================================
# Eu sou a tela de Menu Principal do Sistema Escolar.
# Agora eu abro janelas Toplevel para cada funcionalidade.
# ======================================================================

import tkinter as tk
from tkinter import messagebox
from utils.helpers import centralizar_janela


# ---------- VARIÁVEL DE CONTROLE ----------
# Eu controlo se a janela de cadastro já está aberta.
# Inicialmente, nenhuma janela está aberta.
janela_cadastro_aberta = None


def criar_menu(janela):
    """
    Eu construo o Menu Principal dentro da janela fornecida.

    Parâmetros:
        janela: a instância de tk.Tk() (janela principal)
    """
    # ---------- FRAME PRINCIPAL ----------
    frame_fundo = tk.Frame(janela, bg="#e8f0fe")
    frame_fundo.pack(expand=True, fill=tk.BOTH)

    # ---------- FRAME DO MENU ----------
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
    lbl_titulo = tk.Label(
        frame_menu,
        text="MENU PRINCIPAL",
        font=("Arial", 20, "bold"),
        bg="white",
        fg="#2c3e50"
    )
    lbl_titulo.pack(pady=(0, 5))

    # ---------- SUBTÍTULO ----------
    lbl_subtitulo = tk.Label(
        frame_menu,
        text="Sistema Escolar",
        font=("Arial", 12),
        bg="white",
        fg="#7f8c8d"
    )
    lbl_subtitulo.pack(pady=(0, 30))

    # ---------- BOTÕES DE NAVEGAÇÃO ----------
    botoes_config = {
        "Cadastrar Alunos": {
            "bg": "#3498db",
            "fg": "white",
            "activebackground": "#2980b9",
            "comando": lambda: abrir_janela_cadastro(janela)
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


def abrir_janela_cadastro(janela_pai):
    """
    Eu abro a janela de Cadastro de Alunos como Toplevel.
    Se a janela já estiver aberta, eu apenas a trago para frente.
    """
    global janela_cadastro_aberta

    # Eu verifico se a janela já existe e está viva.
    if janela_cadastro_aberta is not None:
        try:
            # Tento verificar se a janela ainda existe.
            _ = janela_cadastro_aberta.winfo_exists()
            if _:
                # A janela existe — eu a trago para frente.
                janela_cadastro_aberta.lift()
                janela_cadastro_aberta.focus_force()
                return
        except tk.TclError:
            # A janela foi destruída — vou criar uma nova.
            janela_cadastro_aberta = None

    # ---------- CRIAÇÃO DA NOVA JANELA ----------
    # Eu crio um Toplevel como filho da janela principal.
    janela_cadastro = tk.Toplevel(janela_pai)
    janela_cadastro.title("Cadastro de Alunos")
    centralizar_janela(janela_cadastro, 700, 500)
    janela_cadastro.resizable(False, False)

    # ---------- INTERCEPTAÇÃO DO BOTÃO X ----------
    # Eu defino o que acontece quando o usuário clica no X da janela.
    janela_cadastro.protocol(
        "WM_DELETE_WINDOW",
        lambda: fechar_janela_cadastro(janela_cadastro)
    )

    # ---------- CONTEÚDO PLACEHOLDER ----------
    # No Capítulo 06, este conteúdo será substituído pelo formulário real.
    frame_conteudo = tk.Frame(janela_cadastro, bg="#fafafa")
    frame_conteudo.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

    lbl_placeholder = tk.Label(
        frame_conteudo,
        text="📋 Cadastro de Alunos\n\n"
             "O formulário completo será implementado no Capítulo 06.\n"
             "Por enquanto, esta janela demonstra a navegação.",
        font=("Arial", 14),
        bg="#fafafa",
        fg="#555555",
        justify=tk.CENTER
    )
    lbl_placeholder.pack(expand=True)

    # ---------- BOTÃO VOLTAR ----------
    btn_voltar = tk.Button(
        frame_conteudo,
        text="Voltar ao Menu",
        font=("Arial", 11),
        bg="#95a5a6",
        fg="white",
        activebackground="#7f8c8d",
        activeforeground="white",
        width=15,
        height=1,
        bd=0,
        cursor="hand2",
        command=lambda: fechar_janela_cadastro(janela_cadastro)
    )
    btn_voltar.pack(pady=(0, 10))

    # Eu atualizo a variável global de controle.
    janela_cadastro_aberta = janela_cadastro


def fechar_janela_cadastro(janela):
    """
    Eu fecho a janela de cadastro e libero a variável de controle.
    """
    global janela_cadastro_aberta
    janela.destroy()
    janela_cadastro_aberta = None


def ao_clicar_sair(janela):
    """
    Eu pergunto ao usuário se ele realmente deseja sair.
    Se confirmar, fecho o sistema completamente.
    """
    resposta = messagebox.askyesno(
        "Confirmar Saída",
        "Tem certeza que deseja sair do sistema?"
    )
    if resposta:
        # Eu destruo a janela principal, encerrando o mainloop.
        janela.destroy()
```

!!! note "A variável global janela_cadastro_aberta"
    Usamos uma variável global para rastrear se a janela está aberta. Em sistemas mais complexos, isso seria gerenciado por um controller ou dicionário. Para nosso escopo, é uma solução simples e eficaz. O método `winfo_exists()` verifica se a janela ainda está "viva" no Tkinter.

### Passo 6 — Testando o fluxo completo

Execute o sistema:

```bash
python main.py
```

Teste o fluxo:

- Login com admin / admin → Menu Principal aparece.
- Clique em Cadastrar Alunos → Abre janela Toplevel "Cadastro de Alunos".
- Tente clicar em Cadastrar Alunos novamente → A janela existente é trazida para frente (não duplica).
- Clique em Voltar ao Menu ou no X da janela → Fecha e volta ao menu.
- Clique em Consultar Alunos → Ainda mostra "Em breve" (será implementado no Capítulo 06).
- Clique em Sair → Confirmação, depois fecha tudo.

## 📝 Exercício

**Tempo estimado:** 15-20 minutos

**Tarefa:** Seguindo o mesmo padrão da janela de Cadastro, implemente a abertura da janela de Consulta de Alunos como Toplevel, com controle de duplicação.

Atualmente, o botão "Consultar Alunos" mostra um messagebox. Substitua esse comportamento por uma função `abrir_janela_consulta` que:

1. Cria um Toplevel com título "Consulta de Alunos", tamanho 700x500
2. Exibe um Label placeholder com o texto "🔍 Consulta de Alunos — em breve"
3. Tem botão "Voltar ao Menu"
4. Controla duplicação (não abre duas janelas iguais)
5. Trata o botão X via `protocol`

??? hint "Dica"
    Siga exatamente o mesmo padrão de `abrir_janela_cadastro`. Você precisará de uma segunda variável global (`janela_consulta_aberta`) e uma função `fechar_janela_consulta`. A estrutura é idêntica — mude apenas os textos e títulos.

??? success "Solução"
    Adicione no topo de `views/menu.py`:
    
    ```python
    janela_consulta_aberta = None
    ```
    
    Crie as funções:
    
    ```python
    def abrir_janela_consulta(janela_pai):
        global janela_consulta_aberta
        if janela_consulta_aberta is not None:
            try:
                _ = janela_consulta_aberta.winfo_exists()
                if _:
                    janela_consulta_aberta.lift()
                    janela_consulta_aberta.focus_force()
                    return
            except tk.TclError:
                janela_consulta_aberta = None
    
        janela_consulta = tk.Toplevel(janela_pai)
        janela_consulta.title("Consulta de Alunos")
        centralizar_janela(janela_consulta, 700, 500)
        janela_consulta.resizable(False, False)
        janela_consulta.protocol(
            "WM_DELETE_WINDOW",
            lambda: fechar_janela_consulta(janela_consulta)
        )
    
        frame_conteudo = tk.Frame(janela_consulta, bg="#fafafa")
        frame_conteudo.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
    
        lbl_placeholder = tk.Label(
            frame_conteudo,
            text="🔍 Consulta de Alunos\n\nEm breve...",
            font=("Arial", 14),
            bg="#fafafa",
            fg="#555555",
            justify=tk.CENTER
        )
        lbl_placeholder.pack(expand=True)
    
        btn_voltar = tk.Button(
            frame_conteudo,
            text="Voltar ao Menu",
            font=("Arial", 11),
            bg="#95a5a6",
            fg="white",
            activebackground="#7f8c8d",
            activeforeground="white",
            width=15,
            height=1,
            bd=0,
            cursor="hand2",
            command=lambda: fechar_janela_consulta(janela_consulta)
        )
        btn_voltar.pack(pady=(0, 10))
    
        janela_consulta_aberta = janela_consulta
    
    def fechar_janela_consulta(janela):
        global janela_consulta_aberta
        janela.destroy()
        janela_consulta_aberta = None
    ```
    
    No dicionário `botoes_config`, altere "Consultar Alunos":
    
    ```python
    "comando": lambda: abrir_janela_consulta(janela)
    ```

## 🏆 Missão da Equipe

**Tempo estimado:** 30-45 minutos

**Tarefa:** Implementem a navegação completa do sistema da equipe usando Toplevel para as telas de funcionalidade.

**Entregável:** O projeto da equipe com:

- `utils/helpers.py` contendo `centralizar_janela`
- `views/menu.py` abrindo janelas Toplevel para cada funcionalidade planejada
- Controle de duplicação em todas as janelas
- Interceptação do botão X em todas as janelas
- Placeholder adequado em cada janela (indicando o que será implementado depois)

**Checklist da Missão:**

- [ ] `utils/helpers.py` criado com `centralizar_janela`
- [ ] `main.py` refatorado para usar withdraw/deiconify (se aplicável ao tema)
- [ ] Menu Principal abre janelas com Toplevel para cada funcionalidade
- [ ] Nenhuma janela pode ser aberta duas vezes simultaneamente
- [ ] O botão X fecha a janela corretamente (sem travar o sistema)
- [ ] Cada janela possui um botão "Voltar ao Menu"
- [ ] O botão "Sair" fecha todo o sistema com confirmação
- [ ] O professor testou a navegação completa

!!! important "Nota para o Professor"
    Verifique: Cada equipe deve demonstrar a abertura e fechamento de pelo menos duas janelas de funcionalidade diferentes. Verifique se não há duplicação e se o botão X não trava o sistema.

## ⚡ Desafio

**Vá além:** Adicione uma animação de fade-in ao abrir as janelas Toplevel.

O Tkinter possui o método `attributes('-alpha', valor)` que controla a opacidade da janela (0.0 = transparente, 1.0 = opaco). Você pode criar um efeito de fade-in aumentando o alpha gradualmente.

Exemplo de implementação:

```python
def fade_in(janela, passo=0.05, intervalo=20):
    """
    Eu aplico um efeito de fade-in na janela.
    A opacidade começa em 0.0 e aumenta até 1.0.
    """
    janela.attributes('-alpha', 0.0)  # Começa invisível
    def aumentar(opacidade=0.0):
        if opacidade < 1.0:
            opacidade += passo
            janela.attributes('-alpha', opacidade)
            janela.after(intervalo, lambda: aumentar(opacidade))
        else:
            janela.attributes('-alpha', 1.0)  # Garante 100% opaco
    aumentar()
```

Chame `fade_in(janela_cadastro)` logo após criar o Toplevel. O efeito é sutil, mas impressionante.

## ⚠️ Erros Comuns

!!! danger "Criar múltiplas instâncias de Tk()"
    **Sintoma:** O sistema abre várias janelas principais independentes na barra de tarefas, e ao fechar uma as outras continuam rodando. Pode ocorrer TclError.
    
    **Causa:** Uso de `tk.Tk()` para criar uma segunda janela em vez de `tk.Toplevel()`.
    
    **Solução:** Substitua `tk.Tk()` por `tk.Toplevel(janela_pai)` em qualquer lugar que não seja o `main.py`. Apenas o ponto de entrada pode criar a instância raiz.

!!! warning "Esquecer de definir protocol('WM_DELETE_WINDOW')"
    **Sintoma:** Ao clicar no X de uma janela Toplevel, ela fecha, mas a variável global de controle ainda aponta para a janela destruída. Tentar abrir novamente causa erro.
    
    **Causa:** O fechamento pelo X não passa pela função de fechamento personalizada — o Tkinter destrói a janela diretamente.
    
    **Solução:** Sempre defina `janela.protocol("WM_DELETE_WINDOW", callback)` para interceptar o clique no X e executar sua função de limpeza (que atualiza a variável global).

!!! warning "Usar withdraw() sem nunca chamar deiconify()"
    **Sintoma:** A janela principal some e nunca mais reaparece.
    
    **Causa:** Após ocultar a janela com `withdraw()`, o código nunca chama `deiconify()` para mostrá-la novamente.
    
    **Solução:** Certifique-se de que, no fluxo de logout ou retorno, exista uma chamada a `janela.deiconify()`. No nosso código atual, a janela principal permanece sempre visível (a transição é feita limpando widgets, não ocultando a janela). Reserve withdraw para cenários onde você realmente quer esconder a janela principal enquanto uma secundária está aberta.

!!! danger "Janela Toplevel não centralizada"
    **Sintoma:** A janela secundária abre no canto superior esquerdo da tela.
    
    **Causa:** Esquecimento de chamar `centralizar_janela` após criar o Toplevel.
    
    **Solução:** Após criar o Toplevel e antes de adicionar widgets, chame `centralizar_janela(janela, largura, altura)`. A função foi movida para `utils/helpers.py` — importe-a.

## 💡 Boas Práticas

**1. Controle de duplicação de janelas**

Em aplicações desktop profissionais, é frustrante para o usuário abrir a mesma janela várias vezes sem querer. O padrão que implementamos (variável global + `winfo_exists()`) é simples e eficaz. Em sistemas maiores, pode-se usar um dicionário de janelas abertas gerenciado por um controller.

**2. Interceptar o botão X com protocol**

O método `protocol("WM_DELETE_WINDOW", callback)` permite que você execute código antes do fechamento — ideal para perguntar "Deseja salvar?" ou liberar recursos. É uma exigência de usabilidade em softwares comerciais.

**3. Funções utilitárias em módulo separado**

Extrair `centralizar_janela` para `utils/helpers.py` segue o princípio DRY (Don't Repeat Yourself). Se amanhã o sistema tiver 10 janelas, todas usarão a mesma função central.

**4. lift() e focus_force() para trazer a janela à frente**

Quando o usuário tenta abrir uma janela que já está aberta, usamos `lift()` (eleva a janela acima das outras) e `focus_force()` (coloca o foco do teclado nela). Isso evita que o usuário se pergunte "para onde foi a janela?".

**5. Comentários que ensinam**

Mantivemos o estilo de comentários em primeira pessoa, explicando a intenção de cada bloco. Isso ajuda futuros desenvolvedores (ou você mesmo, daqui a meses) a entender rapidamente o que cada parte faz.

## ☑️ Checklist

Antes de prosseguir para o próximo capítulo, confirme:

- [ ] `utils/helpers.py` criado com a função `centralizar_janela`
- [ ] `main.py` refatorado com callbacks `abrir_menu` e `voltar_login`
- [ ] `views/menu.py` importa `centralizar_janela` de `utils.helpers`
- [ ] Botão "Cadastrar Alunos" abre um Toplevel centralizado
- [ ] Botão "Consultar Alunos" abre um Toplevel centralizado (após exercício)
- [ ] Nenhuma janela Toplevel pode ser aberta duas vezes
- [ ] O botão X de cada Toplevel fecha corretamente e libera a variável de controle
- [ ] O botão "Sair" fecha o sistema com confirmação
- [ ] A janela principal não usa Toplevel — apenas `tk.Tk()` uma única vez
- [ ] Minha equipe concluiu a Missão da Equipe com a navegação do projeto dela

## ➡️ Próximo Capítulo

No **Capítulo 06 — Cadastro de Alunos**, você finalmente preencherá aquela janela placeholder com conteúdo real: um formulário completo (Nome, Idade, Turma) e uma tabela Treeview listando os alunos cadastrados.

Será a primeira tela de funcionalidade 100% operacional — o coração do sistema. Você usará tudo o que aprendeu até agora: organização de widgets com grid e pack, validação de campos, e a estrutura de janelas que acabou de dominar.

Prepare-se: revise o uso de Treeview, Scrollbar e validação de entrada com try/except. A parte mais desafiadora do projeto está chegando! 📝
