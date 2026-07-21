# CustomTkinter e Interfaces Modernas

## Objetivos

Neste capítulo, você aprenderá a:

- Compreender as limitações visuais do Tkinter tradicional e a motivação para usar CustomTkinter.
- Instalar e configurar a biblioteca CustomTkinter em seu ambiente Python.
- Criar janelas modernas com bordas arredondadas, temas claros e escuros e esquemas de cores personalizáveis.
- Utilizar os widgets do CustomTkinter equivalentes aos do Tkinter padrão: `CTk`, `CTkButton`, `CTkLabel`, `CTkEntry`, `CTkFrame`, entre outros.
- Migrar uma aplicação Tkinter existente para CustomTkinter preservando a lógica de layout, eventos e variáveis de controle.
- Aplicar boas práticas de design visual para tornar suas interfaces mais atraentes e profissionais.

## Pré-requisitos

Antes de prosseguir, você deve ter domínio sobre:

- Criação de janelas e widgets básicos com Tkinter (`Tk`, `Label`, `Button`, `Entry`, `Frame`).
- Gerenciadores de layout `pack()` e `grid()`.
- Associação de eventos com `bind()` e uso de variáveis de controle (`StringVar`, `IntVar`, etc.).
- Estruturação de aplicações com funções ou classes.

Se necessário, revise os capítulos anteriores sobre Tkinter.

## Motivação

O Tkinter é uma biblioteca poderosa, madura e nativa do Python. No entanto, seu visual padrão reflete a estética dos sistemas operacionais dos anos 90 e início dos anos 2000: botões retangulares rígidos, cores sólidas e pouca personalização. Para aplicações modernas, os usuários esperam interfaces mais limpas, com cantos arredondados, transições suaves, temas escuros e uma aparência geral mais polida.

É nesse cenário que surge o CustomTkinter, uma biblioteca construída sobre o Tkinter que oferece widgets com visual contemporâneo, mantendo a simplicidade e a lógica de programação do Tkinter original. Com ela, você pode transformar uma interface datada em algo similar a aplicativos modernos como Discord, Spotify ou Visual Studio Code, com pouquíssimas alterações de código.

Neste capítulo, você modernizará suas habilidades, aprendendo a criar GUIs que não apenas funcionam bem, mas também impressionam visualmente.

## Conteúdo

### O que é o CustomTkinter?

CustomTkinter é uma biblioteca de terceiros desenvolvida por Tom Schimansky. Ela estende as classes base do Tkinter com novos widgets que desenham sua própria aparência utilizando o Canvas do Tkinter, ignorando os temas nativos do sistema operacional. Isso permite:

- Cantos arredondados.
- Temas claros e escuros prontos para uso.
- Cores personalizáveis globalmente.
- Widgets com estados visuais (hover, pressionado, desabilitado).
- Suporte a ícones e imagens de forma simplificada.

Apesar dessas melhorias visuais, o CustomTkinter mantém total compatibilidade com a lógica do Tkinter: você ainda usa `pack()`, `grid()`, `bind()`, `StringVar`, etc. A curva de aprendizado é mínima para quem já conhece Tkinter.

!!! note "CustomTkinter vs. Tkinter tradicional"
    O Tkinter clássico depende de temas do sistema operacional (Windows, Aqua no macOS, GTK no Linux). O CustomTkinter desenha seus próprios widgets, garantindo uma aparência consistente em qualquer plataforma. A troca é feita substituindo as classes `tk.` por `customtkinter.` (ex.: `tk.Button` → `customtkinter.CTkButton`).

### Instalação

A biblioteca está disponível no PyPI e pode ser instalada com pip:

```bash
pip install customtkinter
```

Para verificar a instalação:

```python
import customtkinter as ctk
print(ctk.__version__)
```

!!! tip "Ambiente virtual"
    Recomendo instalar em um ambiente virtual para evitar conflitos com outros projetos.

### Primeira janela com CustomTkinter

A estrutura é análoga ao Tkinter, porém usando as classes prefixadas com CTk:

```python
import customtkinter as ctk

# Configuração de aparência (tema escuro e tema de cores padrão)
ctk.set_appearance_mode("dark")  # "light", "dark" ou "system"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

janela = ctk.CTk()
janela.title("Minha Primeira Janela Moderna")
janela.geometry("400x300")

# Widgets
rotulo = ctk.CTkLabel(janela, text="Bem-vindo ao CustomTkinter!", font=("Arial", 16))
rotulo.pack(pady=20)

botao = ctk.CTkButton(janela, text="Clique aqui")
botao.pack(pady=10)

entrada = ctk.CTkEntry(janela, placeholder_text="Digite algo...")
entrada.pack(pady=10)

janela.mainloop()
```

Aqui, `set_appearance_mode` define o tema (claro, escuro ou segue o sistema operacional), e `set_default_color_theme` define o esquema de cores dos widgets (`blue`, `green`, `dark-blue`). O resultado é uma janela com visual moderno, botões arredondados e campo de entrada estilizado, praticamente com o mesmo código que usaríamos no Tkinter padrão.

### Principais widgets e suas equivalências

| Tkinter | CustomTkinter | Descrição breve |
|---|---|---|
| `tk.Tk()` | `ctk.CTk()` | Janela principal. |
| `tk.Toplevel()` | `ctk.CTkToplevel()` | Janela secundária. |
| `tk.Frame()` | `ctk.CTkFrame()` | Contêiner (pode ter bordas arredondadas). |
| `tk.Label()` | `ctk.CTkLabel()` | Rótulo de texto. |
| `tk.Button()` | `ctk.CTkButton()` | Botão com cantos arredondados e efeito hover. |
| `tk.Entry()` | `ctk.CTkEntry()` | Campo de entrada de texto (com placeholder). |
| `tk.Checkbutton()` | `ctk.CTkCheckBox()` | Caixa de seleção. |
| `tk.Radiobutton()` | `ctk.CTkRadioButton()` | Botão de opção (radio). |
| `tk.OptionMenu()` | `ctk.CTkOptionMenu()` | Menu suspenso. |
| `tk.Scale()` | `ctk.CTkSlider()` | Controle deslizante. |
| `tk.Progressbar()` | `ctk.CTkProgressBar()` | Barra de progresso. |
| `tk.Text()` | `ctk.CTkTextbox()` | Caixa de texto multilinha. |
| `tk.Scrollbar()` | `ctk.CTkScrollbar()` | Barra de rolagem. |

Todos esses widgets aceitam a maioria dos parâmetros do Tkinter original e adicionam novos, como `corner_radius`, `fg_color`, `hover_color`, `placeholder_text`, entre outros.

### Sistema de temas e cores

O CustomTkinter oferece três temas de aparência:

- `"light"`: modo claro.
- `"dark"`: modo escuro.
- `"system"`: segue a configuração do sistema operacional (padrão).

E três temas de cores embutidos:

- `"blue"`: tons de azul.
- `"green"`: tons de verde.
- `"dark-blue"`: azul escuro (padrão).

Além disso, você pode criar temas personalizados definindo um dicionário de cores e carregando com `ctk.set_default_color_theme("caminho/para/meu_tema.json")`.

Exemplo de alternância de tema em tempo real:

```python
import customtkinter as ctk

def alternar_tema():
    if ctk.get_appearance_mode() == "dark":
        ctk.set_appearance_mode("light")
    else:
        ctk.set_appearance_mode("dark")

janela = ctk.CTk()
janela.geometry("300x200")

ctk.CTkButton(janela, text="Alternar Tema", command=alternar_tema).pack(pady=50)

janela.mainloop()
```

### Migrando do Tkinter para o CustomTkinter

O processo de migração é direto e pode ser feito gradualmente:

1. **Substituir as classes:** `tk.` por `ctk.` (ex.: `tk.Tk` → `ctk.CTk`). Lembre-se de importar `customtkinter as ctk`.
2. **Ajustar parâmetros específicos:** alguns parâmetros mudam de nome ou ganham novas opções. Por exemplo, `bg` e `fg` são substituídos por `fg_color`, `text_color`, `bg_color`. Consulte a documentação oficial para cada widget.
3. **Variáveis de controle:** continuam funcionando (`tk.StringVar`, `tk.IntVar`, etc.), mas você pode usar `ctk.StringVar` se preferir (funciona de forma idêntica).
4. **Layout e eventos:** `pack()`, `grid()`, `bind()`, `command` permanecem idênticos. A lógica da sua aplicação não muda.
5. **Frames como contêineres:** `CTkFrame` é a base para organizar seções. Você pode definir `corner_radius` para bordas arredondadas e `fg_color` para cor de fundo.

!!! warning "Cuidado com parâmetros inexistentes no CustomTkinter"
    Alguns parâmetros do Tkinter clássico, como `relief`, `bd`, `highlightbackground`, não funcionam nos widgets do CustomTkinter, pois eles desenham sua própria aparência. Se seu código depende muito desses, você precisará adaptar.

### Personalização avançada de widgets

Cada widget do CustomTkinter pode ser personalizado diretamente na criação ou depois com o método `configure()`.

```python
botao = ctk.CTkButton(
    janela,
    text="Personalizado",
    fg_color="#FF5733",   # cor de fundo
    hover_color="#C70039", # cor ao passar o mouse
    text_color="white",
    corner_radius=10,     # raio dos cantos
    width=200,
    height=40,
    font=("Arial", 14, "bold")
)
```

Essa personalização granular permite criar interfaces únicas sem precisar de imagens ou estilização CSS.

### Eventos e variáveis de controle

O sistema de eventos do Tkinter funciona perfeitamente com CustomTkinter. Você pode usar `bind()`, `command` e `trace_add` da mesma forma.

Exemplo com CTkEntry e StringVar:

```python
import customtkinter as ctk

def ao_mudar(*args):
    print("Texto atual:", var_texto.get())

janela = ctk.CTk()
var_texto = ctk.StringVar()
var_texto.trace_add("write", ao_mudar)

entrada = ctk.CTkEntry(janela, textvariable=var_texto)
entrada.pack(padx=20, pady=20)

janela.mainloop()
```

Isso mostra como a transição é suave: você mantém suas funções de callback e lógica de validação, apenas com um visual renovado.

### Criando interfaces completas com CustomTkinter

Vamos estruturar uma aplicação mais complexa, combinando `CTkFrame` para seções, `CTkLabel`, `CTkEntry` e `CTkButton`, com layout `grid()`.

```python
import customtkinter as ctk

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login Moderno")
        self.geometry("400x300")
        self.criar_widgets()

    def criar_widgets(self):
        # Frame central
        frame = ctk.CTkFrame(self)
        frame.pack(expand=True)

        ctk.CTkLabel(frame, text="Login", font=("Arial", 20)).pack(pady=20)

        ctk.CTkLabel(frame, text="Usuário:").pack(anchor="w", padx=20)
        self.entrada_usuario = ctk.CTkEntry(frame, placeholder_text="Seu usuário")
        self.entrada_usuario.pack(padx=20, pady=5, fill="x")

        ctk.CTkLabel(frame, text="Senha:").pack(anchor="w", padx=20)
        self.entrada_senha = ctk.CTkEntry(frame, placeholder_text="Sua senha", show="*")
        self.entrada_senha.pack(padx=20, pady=5, fill="x")

        ctk.CTkButton(frame, text="Entrar", command=self.login).pack(pady=20)
        self.label_status = ctk.CTkLabel(frame, text="")
        self.label_status.pack()

    def login(self):
        usuario = self.entrada_usuario.get()
        senha = self.entrada_senha.get()
        if usuario == "admin" and senha == "123":
            self.label_status.configure(text="Login bem-sucedido!", text_color="green")
        else:
            self.label_status.configure(text="Usuário ou senha incorretos.", text_color="red")

if __name__ == "__main__":
    app = App()
    app.mainloop()
```

Este exemplo demonstra como uma interface de login pode ser moderna e funcional com poucas linhas.

### Boas práticas

- Use `ctk.set_appearance_mode("system")` para respeitar a preferência do usuário.
- Defina um tema de cores consistente no início do programa.
- Aproveite `CTkFrame` para agrupar componentes e criar seções visuais com bordas arredondadas.
- Mantenha a lógica de negócios separada da interface, como faria com Tkinter padrão.
- Teste o visual em diferentes sistemas operacionais; embora o CustomTkinter seja multiplataforma, pequenas variações podem ocorrer.
- Consulte a documentação oficial para explorar todos os widgets e opções disponíveis.

## Exemplos

??? example "Exemplo 1: Conversor de temperatura modernizado"
    === "Código"
        ```python
        import customtkinter as ctk

        def converter():
            try:
                celsius = float(entrada.get())
                fahrenheit = celsius * 9/5 + 32
                resultado.configure(text=f"{celsius}°C = {fahrenheit:.1f}°F")
            except ValueError:
                resultado.configure(text="Valor inválido!", text_color="red")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        janela = ctk.CTk()
        janela.title("Conversor °C → °F")
        janela.geometry("350x200")

        ctk.CTkLabel(janela, text="Temperatura em Celsius:", font=("Arial", 14)).pack(pady=10)
        entrada = ctk.CTkEntry(janela, placeholder_text="Ex: 25")
        entrada.pack(pady=5)

        ctk.CTkButton(janela, text="Converter", command=converter).pack(pady=10)
        resultado = ctk.CTkLabel(janela, text="", font=("Arial", 14, "bold"))
        resultado.pack()

        janela.mainloop()
        ```

    === "Resultado"
        Uma janela escura com tema verde, campo de entrada para Celsius, botão "Converter" e resultado exibido em destaque. Ao digitar um número e clicar no botão, a conversão aparece. Se o valor for inválido, exibe "Valor inválido!" em vermelho.

    === "Explicação"
        O código é praticamente idêntico ao que faríamos com Tkinter padrão, apenas com classes CTk. Note o uso de `configure(text=...)` para atualizar o label de resultado, que funciona da mesma forma. O tema escuro e verde dá um visual agradável.

??? example "Exemplo 2: Alternador de temas e personalização de cores"
    === "Código"
        ```python
        import customtkinter as ctk

        def alternar():
            modo = ctk.get_appearance_mode()
            ctk.set_appearance_mode("light" if modo == "dark" else "dark")
            status.configure(text=f"Modo atual: {'claro' if modo == 'dark' else 'escuro'}")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        janela = ctk.CTk()
        janela.geometry("400x250")
        janela.title("Personalização de Temas")

        # Slider para ajustar transparência (janela alpha - Windows/macOS)
        def ajustar_transparencia(valor):
            janela.attributes("-alpha", float(valor))

        ctk.CTkLabel(janela, text="CustomTkinter", font=("Arial", 20, "bold")).pack(pady=20)
        status = ctk.CTkLabel(janela, text="Modo atual: escuro")
        status.pack()

        ctk.CTkButton(janela, text="Alternar Tema", command=alternar).pack(pady=10)

        ctk.CTkLabel(janela, text="Transparência da janela:").pack()
        slider = ctk.CTkSlider(janela, from_=0.4, to=1.0, command=ajustar_transparencia)
        slider.set(1.0)
        slider.pack()

        janela.mainloop()
        ```

    === "Resultado"
        Janela com título grande, botão que alterna entre tema claro e escuro, e um slider que controla a transparência da janela (funciona no Windows e macOS). O status atualiza a cada alternância.

    === "Explicação"
        Além dos botões e labels, usamos CTkSlider para ajuste contínuo. `janela.attributes("-alpha", valor)` é uma funcionalidade do Tkinter subjacente que o CustomTkinter preserva. A função `set()` define o valor inicial do slider. Esse exemplo mostra como é fácil adicionar controles modernos com retorno imediato.

??? example "Exemplo 3: Migração de um formulário Tkinter para CustomTkinter"
    === "Código Tkinter original"
        ```python
        import tkinter as tk
        from tkinter import messagebox

        def enviar():
            nome = entry_nome.get()
            email = entry_email.get()
            if nome and email:
                messagebox.showinfo("Sucesso", f"Cadastro de {nome} realizado.")
            else:
                messagebox.showwarning("Atenção", "Preencha todos os campos.")

        janela = tk.Tk()
        janela.title("Cadastro")
        janela.geometry("300x200")

        tk.Label(janela, text="Nome:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        entry_nome = tk.Entry(janela)
        entry_nome.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(janela, text="Email:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        entry_email = tk.Entry(janela)
        entry_email.grid(row=1, column=1, padx=10, pady=5)

        tk.Button(janela, text="Enviar", command=enviar).grid(row=2, column=0, columnspan=2, pady=15)

        janela.mainloop()
        ```

    === "Código CustomTkinter equivalente"
        ```python
        import customtkinter as ctk
        from tkinter import messagebox

        def enviar():
            nome = entry_nome.get()
            email = entry_email.get()
            if nome and email:
                messagebox.showinfo("Sucesso", f"Cadastro de {nome} realizado.")
            else:
                messagebox.showwarning("Atenção", "Preencha todos os campos.")

        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        janela = ctk.CTk()
        janela.title("Cadastro")
        janela.geometry("350x250")

        # Note que usamos grid da mesma forma!
        ctk.CTkLabel(janela, text="Nome:").grid(row=0, column=0, padx=20, pady=10, sticky="e")
        entry_nome = ctk.CTkEntry(janela, placeholder_text="Seu nome completo")
        entry_nome.grid(row=0, column=1, padx=20, pady=10, sticky="ew")

        ctk.CTkLabel(janela, text="Email:").grid(row=1, column=0, padx=20, pady=10, sticky="e")
        entry_email = ctk.CTkEntry(janela, placeholder_text="seu@email.com")
        entry_email.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

        ctk.CTkButton(janela, text="Enviar", command=enviar).grid(row=2, column=0, columnspan=2, pady=20)

        janela.grid_columnconfigure(1, weight=1)  # torna a coluna da entry expansível
        janela.mainloop()
        ```

    === "Resultado"
        O formulário tem a mesma estrutura, mas visualmente os campos são arredondados, o botão tem efeito hover e a janela segue o tema do sistema. A funcionalidade é idêntica.

    === "Explicação"
        A migração envolveu basicamente substituir `tk.Label` por `ctk.CTkLabel`, `tk.Entry` por `ctk.CTkEntry`, `tk.Button` por `ctk.CTkButton`. O layout `grid()` permaneceu inalterado. Isso demonstra a facilidade de modernizar uma aplicação existente sem reescrever a lógica.

## Exercícios

### Básico (fixação)

1. Instale o CustomTkinter e crie uma janela com tema escuro e tema de cores "green". Adicione um `CTkLabel` com o texto "Aprendendo CustomTkinter" e um `CTkButton` com o texto "Fechar" que encerra a aplicação.
2. Modifique o conversor de temperatura do Exemplo 1 para incluir um campo de entrada que aceite Fahrenheit e converta para Celsius ao clicar em um segundo botão. Utilize `CTkEntry` e organize com `grid()`.
3. Crie um slider (`CTkSlider`) que varia de 0 a 100 e exiba o valor atual em um `CTkLabel` ao lado, usando `IntVar` e `trace_add` (ou `command` do slider).

### Intermediário (aplicação)

Desenvolva um formulário de avaliação com os seguintes widgets CustomTkinter:

- `CTkEntry` para nome.
- `CTkOptionMenu` para nota (valores: 1 a 5).
- `CTkCheckBox` para "Deseja receber novidades por e-mail?".
- `CTkButton` "Enviar Avaliação".

Ao clicar em Enviar, exiba uma `CTkToplevel` com um resumo dos dados preenchidos. Use `grid()` para organização e trate campos vazios com validação.

### Avançado (desafio)

Crie um editor de notas simplificado usando CustomTkinter:

- Janela principal com `CTkTextbox` ocupando a maior parte.
- Barra superior (`CTkFrame`) com botões: "Novo", "Abrir", "Salvar" (use `filedialog` do Tkinter para selecionar arquivos `.txt`).
- Ao abrir um arquivo, carregue o conteúdo no `CTkTextbox`. Ao salvar, grave o conteúdo do `CTkTextbox` no arquivo.
- Barra de status inferior (`CTkFrame`) com `CTkLabel` mostrando número de caracteres e palavras, atualizada a cada tecla pressionada (use `bind("<KeyRelease>", ...)` como no Tkinter tradicional).
- Implemente alternância de tema claro/escuro com um `CTkSwitch` no canto superior direito.
- A aparência geral deve ser moderna e profissional, com espaçamentos e cantos arredondados.

## Projeto Prático

### Modernizando o Gerenciador de Tarefas

Retome o Gerenciador de Tarefas desenvolvido no Módulo 01 (CLI) e no projeto prático de Tkinter, e transforme sua interface gráfica em uma aplicação moderna com CustomTkinter.

**Requisitos:**

- Janela principal com tema escuro ("dark") e esquema de cores "dark-blue".
- Área superior: `CTkFrame` contendo `CTkEntry` para descrição da tarefa, `CTkOptionMenu` para prioridade (alta, média, baixa) e `CTkButton` "Adicionar".
- Área central: `CTkScrollableFrame` (ou `CTkFrame` com scroll) contendo a lista de tarefas. Cada tarefa deve ser exibida em um `CTkFrame` individual, com:
    - `CTkCheckBox` para marcar como concluída (ao marcar, o texto deve ficar riscado — use `text_color` e font com `overstrike`).
    - `CTkLabel` com a descrição e prioridade.
    - `CTkButton` pequeno para remover a tarefa.
- Área inferior: `CTkFrame` com `CTkLabel` mostrando o total de tarefas e quantas estão concluídas.
- Persistência: salvar e carregar tarefas de um arquivo `tarefas.json`, como feito anteriormente.
- Funcionalidades:
    - Adicionar tarefa com validação (descrição não vazia).
    - Marcar como concluída (checkbox) atualiza o visual e a contagem.
    - Remover tarefa com confirmação via `CTkToplevel` ou `messagebox`.
    - Persistência automática ao adicionar, concluir ou remover.
- Migração: se você já tinha uma versão Tkinter, adapte os widgets para CustomTkinter. Caso contrário, construa do zero com as boas práticas aprendidas.

**Esqueleto da interface (recorte):**

```python
import customtkinter as ctk
from tkinter import messagebox
import json

class GerenciadorTarefas:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.janela = ctk.CTk()
        self.janela.title("Gerenciador de Tarefas")
        self.janela.geometry("600x450")
        self.tarefas = []
        self.carregar_tarefas()
        self.criar_widgets()
        self.atualizar_lista()

    def criar_widgets(self):
        # Frame superior
        topo = ctk.CTkFrame(self.janela)
        topo.pack(fill="x", padx=10, pady=10)
        # ... (implementar os widgets)

    # ... implementar métodos de lógica e persistência

    def iniciar(self):
        self.janela.mainloop()

if __name__ == "__main__":
    app = GerenciadorTarefas()
    app.iniciar()
```

Complete a implementação, garantindo que a interface seja moderna e funcional. Este projeto consolidará todos os conhecimentos de CustomTkinter e demonstrará como modernizar uma aplicação real.

## Resumo

Neste capítulo, você aprendeu que:

- O CustomTkinter é uma biblioteca que moderniza o Tkinter, fornecendo widgets com visual contemporâneo, bordas arredondadas e temas claros/escuros.
- A instalação é simples via pip, e a curva de aprendizado é mínima para quem já conhece Tkinter.
- A migração consiste em substituir classes `tk.` por `ctk.`, mantendo a mesma lógica de layout, eventos e variáveis de controle.
- É possível personalizar cores, cantos, fontes e temas globalmente ou por widget.
- O sistema de eventos (`bind`, `command`, `trace`) funciona de forma idêntica, garantindo que a interatividade não seja comprometida.
- A combinação de CustomTkinter com boas práticas de organização produz interfaces modernas e profissionais.

Com esse conhecimento, suas aplicações Python desktop ganharão um salto de qualidade visual, sem a complexidade de aprender um framework totalmente novo.

## Próximo Capítulo

No próximo capítulo, desenvolveremos o **Projeto Final do Módulo 02**, onde juntaremos layout, eventos, persistência e o visual do CustomTkinter para construir uma aplicação desktop completa e robusta do início ao fim.
