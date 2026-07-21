# Introdução a Interfaces Gráficas e Tkinter

## Objetivos

Neste capítulo, você dará os primeiros passos no desenvolvimento de interfaces gráficas com Python. Os objetivos são:

- Compreender o que é uma Interface Gráfica do Usuário (GUI) e suas vantagens em relação à linha de comando.
- Conhecer a biblioteca Tkinter como ferramenta nativa para criação de GUIs em Python.
- Criar uma janela principal e configurar suas propriedades básicas.
- Utilizar os widgets fundamentais: Label (rótulo), Button (botão) e Entry (caixa de entrada de texto).
- Posicionar elementos na janela usando gerenciadores de layout simples (pack e grid).
- Associar ações a botões por meio de funções de retorno (comandos).
- Construir um programa interativo que responda às entradas do usuário.

## Pré-requisitos

Antes de iniciar, você deve ter consolidado:

- Conceitos fundamentais de programação Python: variáveis, funções, estruturas de controle (if, for, while).
- Definição e chamada de funções, incluindo o uso de parâmetros e retorno.
- Manipulação de strings e conversões de tipo.
- Noções de tratamento de eventos (não obrigatório, mas útil).

Este capítulo é a porta de entrada para o Módulo 02 do curso; portanto, se você concluiu o Módulo 01, está perfeitamente preparado.

## Motivação

Até agora, todos os nossos programas interagiam com o usuário por meio do terminal: um console preto (ou branco) onde os dados são digitados e as respostas exibidas em texto puro. Embora essa abordagem seja eficiente e essencial para muitas tarefas, a maioria dos usuários de software está acostumada com janelas, ícones, botões e campos de texto — ou seja, uma interface gráfica.

Imagine um sistema de cadastro de clientes, um editor de notas ou um reprodutor de música. Poder clicar em botões, ver informações organizadas visualmente e navegar por menus torna a experiência muito mais agradável e produtiva.

O Tkinter é a biblioteca padrão do Python para criação de GUIs. Ela é leve, madura e está disponível em praticamente todas as instalações do Python, sem necessidade de instalação adicional. Com ela, você pode construir desde aplicações simples até sistemas completos, mantendo a portabilidade entre Windows, Linux e macOS.

Neste capítulo, vamos montar a base sólida para que você possa, nos próximos, desenvolver interfaces cada vez mais ricas e profissionais.

## Conteúdo

### O que é uma GUI?

GUI (Graphical User Interface) é a camada visual de um programa, que permite ao usuário interagir através de elementos gráficos como janelas, botões, menus, caixas de texto, entre outros. Em Python, a biblioteca Tkinter fornece um conjunto de classes e funções que encapsulam esses elementos, chamados widgets.

### Estrutura fundamental de uma aplicação Tkinter

Todo programa com Tkinter segue uma estrutura básica:

1. Importar o módulo `tkinter` (geralmente com apelido `tk`).
2. Criar a janela principal (instância de `Tk`).
3. Definir propriedades da janela (título, tamanho, etc.).
4. Adicionar widgets à janela.
5. Iniciar o loop principal (`mainloop()`), que mantém a janela aberta e aguarda eventos (cliques, digitação, etc.).

Vamos ao exemplo mais simples possível:

```python
import tkinter as tk

# Cria a janela principal
janela = tk.Tk()
janela.title("Minha Primeira GUI")  # Título da janela
janela.geometry("300x200")          # Largura x Altura em pixels

# Inicia o loop de eventos
janela.mainloop()
```

!!! note "O que é o mainloop()?"
    O `mainloop()` é um método que entra em um laço infinito, esperando por eventos do usuário (como cliques ou teclas pressionadas) e os despacha para os widgets correspondentes. Sem ele, a janela é exibida e desaparece instantaneamente. Ele só é encerrado quando a janela é fechada.

### Widgets básicos: Label, Button, Entry

Os widgets são os blocos de construção de uma GUI. Os três mais fundamentais são:

- **Label:** exibe um texto ou imagem. O usuário não pode editar.
- **Button:** exibe um botão clicável que dispara uma ação.
- **Entry:** caixa de entrada de texto de linha única.

Para criar um widget, primeiro instanciamos sua classe passando a janela pai (ou um frame) como primeiro argumento, e depois utilizamos um gerenciador de layout para posicioná-lo.

```python
import tkinter as tk

janela = tk.Tk()
janela.title("Widgets Básicos")

# Rótulo
rotulo = tk.Label(janela, text="Olá, mundo!")
rotulo.pack()

# Botão (sem ação por enquanto)
botao = tk.Button(janela, text="Clique aqui")
botao.pack()

# Entrada de texto
entrada = tk.Entry(janela)
entrada.pack()

janela.mainloop()
```

O método `pack()` posiciona os widgets empilhados verticalmente (um abaixo do outro), na ordem em que foram criados. Veremos outros gerenciadores de layout adiante.

### Adicionando interação: comandos em botões

Para que um botão faça algo quando clicado, associamos uma função ao parâmetro `command`. Essa função é chamada sem argumentos (a menos que usemos `lambda` ou `partial` para personalizar).

```python
import tkinter as tk

def cumprimentar():
    # Obtém o texto do Entry e exibe no Label
    nome = entrada.get()
    rotulo_saida.config(text=f"Olá, {nome}!")

janela = tk.Tk()
janela.title("Saudação")

entrada = tk.Entry(janela)
entrada.pack()

botao = tk.Button(janela, text="Cumprimentar", command=cumprimentar)
botao.pack()

rotulo_saida = tk.Label(janela, text="")
rotulo_saida.pack()

janela.mainloop()
```

Aqui, `entrada.get()` recupera o conteúdo digitado pelo usuário. `rotulo_saida.config(text=...)` altera o texto exibido pelo Label dinamicamente.

!!! tip "Use config() para atualizar widgets"
    Widgets podem ter suas propriedades alteradas após a criação usando o método `config()` ou acessando diretamente seus atributos (ex.: `widget['text'] = 'Novo texto'`).

### Gerenciadores de layout

Posicionar widgets manualmente com coordenadas é impraticável. O Tkinter oferece três gerenciadores de layout:

- `pack()`: empilha widgets horizontal ou verticalmente, preenchendo o espaço disponível.
- `grid()`: organiza em uma grade (linhas e colunas), como uma tabela.
- `place()`: posicionamento absoluto (x, y) ou relativo — menos flexível e não recomendado para interfaces responsivas.

Vamos focar no `grid()` por sua versatilidade. Ele aceita parâmetros `row` (linha) e `column` (coluna), além de `padx`/`pady` (espaçamento externo) e `sticky` (alinhamento).

```python
import tkinter as tk

janela = tk.Tk()
janela.title("Grid Layout")

# Rótulo na linha 0, coluna 0
tk.Label(janela, text="Usuário:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
# Entry na linha 0, coluna 1
tk.Entry(janela).grid(row=0, column=1, padx=5, pady=5)

tk.Label(janela, text="Senha:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
tk.Entry(janela, show="*").grid(row=1, column=1, padx=5, pady=5)

# Botão que ocupa duas colunas (mesclando)
tk.Button(janela, text="Login").grid(row=2, column=0, columnspan=2, pady=10)

janela.mainloop()
```

Aqui `sticky="e"` alinha o texto à direita (leste). `columnspan=2` faz o botão ocupar duas colunas, centralizando-o.

### Eventos e validação simples

Além do comando de botão, podemos associar funções a eventos como pressionar uma tecla no Entry. O método `bind()` permite isso:

```python
def verificar(event):
    if len(entrada.get()) > 5:
        rotulo_status.config(text="OK")
    else:
        rotulo_status.config(text="Mínimo 6 caracteres")

entrada.bind("<KeyRelease>", verificar)
```

A cada tecla solta, a função `verificar` é chamada com um objeto `event` (que podemos ignorar). Isso torna a interface mais responsiva.

### Janelas secundárias (top level)

O Tkinter permite criar janelas adicionais com `Toplevel`. São úteis para diálogos, configurações ou ajuda.

```python
def abrir_sobre():
    janela_sobre = tk.Toplevel()
    janela_sobre.title("Sobre")
    tk.Label(janela_sobre, text="Meu App v1.0").pack()
    tk.Button(janela_sobre, text="Fechar", command=janela_sobre.destroy).pack()
```

O método `destroy()` fecha a janela secundária.

### Boas práticas iniciais

- Sempre centralize o loop principal em uma função `main()` e proteja com `if __name__ == "__main__":`.
- Evite lógica de negócios dentro das funções de interface: separe em módulos.
- Nomeie os widgets de forma descritiva.
- Use constantes para cores, tamanhos e textos repetidos.

## Exemplos

??? example "Exemplo 1: Janela com botão que muda o texto do Label"
    === "Código"
        ```python
        import tkinter as tk

        def alternar_texto():
            if rotulo.cget("text") == "Texto inicial":
                rotulo.config(text="Texto alterado!")
            else:
                rotulo.config(text="Texto inicial")

        janela = tk.Tk()
        janela.title("Exemplo Simples")
        janela.geometry("300x150")

        rotulo = tk.Label(janela, text="Texto inicial", font=("Arial", 14))
        rotulo.pack(pady=20)

        botao = tk.Button(janela, text="Alterar texto", command=alternar_texto)
        botao.pack(pady=10)

        janela.mainloop()
        ```

    === "Resultado"
        Ao executar, uma janela aparece com o rótulo "Texto inicial". Cada clique no botão alterna entre "Texto inicial" e "Texto alterado!".

    === "Explicação"
        Usamos o método `cget()` para obter o valor atual do atributo `text`. A função `alternar_texto` verifica qual texto está atualmente e muda para o outro. `pack(pady=20)` adiciona espaçamento vertical.

??? example "Exemplo 2: Conversor de Unidades (metros para centímetros)"
    === "Código"
        ```python
        import tkinter as tk

        def converter():
            try:
                metros = float(entrada_metros.get())
                centimetros = metros * 100
                saida.config(text=f"{metros} m = {centimetros:.2f} cm")
            except ValueError:
                saida.config(text="Digite um número válido.")

        janela = tk.Tk()
        janela.title("Conversor m -> cm")
        janela.geometry("350x150")

        tk.Label(janela, text="Metros:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        entrada_metros = tk.Entry(janela, width=20)
        entrada_metros.grid(row=0, column=1, padx=10, pady=5)

        tk.Button(janela, text="Converter", command=converter).grid(row=1, column=0, columnspan=2, pady=10)

        saida = tk.Label(janela, text="", fg="blue")
        saida.grid(row=2, column=0, columnspan=2)

        janela.mainloop()
        ```

    === "Resultado"
        O usuário digita um valor numérico em metros, clica "Converter" e o resultado em centímetros aparece abaixo. Se a entrada não for numérica, exibe "Digite um número válido."

    === "Explicação"
        Utilizamos `grid()` para um layout mais organizado: label e campo na mesma linha. O botão ocupa duas colunas com `columnspan=2`. A função tenta converter a string para `float`; se falhar, captura `ValueError` e informa o erro. O resultado é formatado com duas casas decimais.

??? example "Exemplo 3: Validação de senha com KeyRelease"
    === "Código"
        ```python
        import tkinter as tk

        def validar(event):
            senha = entrada.get()
            if len(senha) < 6:
                status.config(text="Fraca", fg="red")
            elif len(senha) < 10:
                status.config(text="Média", fg="orange")
            else:
                status.config(text="Forte", fg="green")

        janela = tk.Tk()
        janela.title("Validador de Senha")
        janela.geometry("300x150")

        tk.Label(janela, text="Senha:").pack(pady=5)
        entrada = tk.Entry(janela, show="*")
        entrada.pack(pady=5)
        entrada.bind("<KeyRelease>", validar)

        status = tk.Label(janela, text="", font=("Arial", 12, "bold"))
        status.pack(pady=10)

        janela.mainloop()
        ```

    === "Resultado"
        Conforme o usuário digita a senha, o texto abaixo muda de "Fraca" (vermelho, menos de 6 caracteres), "Média" (laranja, entre 6 e 9) para "Forte" (verde, 10 ou mais).

    === "Explicação"
        `bind("<KeyRelease>", validar)` associa a função ao evento de soltar uma tecla. A função lê o conteúdo do Entry e atualiza o Label status com texto e cor via `fg`. Note que não precisamos usar o parâmetro `event`, mas ele está disponível.

## Exercícios

### Básico (fixação)

1. Crie uma janela com título "Meu Primeiro App", tamanho 400x300 e um Label no centro com a mensagem "Bem-vindo ao Tkinter!". Use `pack()`.
2. Adicione um botão com texto "Fechar" que encerra a aplicação (use `janela.destroy`).
3. Posicione um Label e um Entry lado a lado usando `grid()`. O Label deve ter o texto "Nome:".

### Intermediário (aplicação)

Construa um conversor de temperatura (Celsius ↔ Fahrenheit). A interface deve ter:

- Um campo de entrada para o valor.
- Dois botões: "Celsius para Fahrenheit" e "Fahrenheit para Celsius".
- Um Label que mostra o resultado.
- Trate entradas inválidas com `try/except`.
- Utilize `grid()` para organizar os widgets e `command` para associar funções distintas a cada botão.

### Avançado (desafio)

Desenvolva uma mini calculadora de IMC (Índice de Massa Corporal). Requisitos:

- Campos de entrada para peso (kg) e altura (m).
- Botão "Calcular" que computa o IMC e exibe o valor e a classificação (Abaixo do peso, Normal, Sobrepeso, Obesidade) conforme tabela padrão.
- Um botão "Limpar" que apaga os campos e o resultado.
- A interface deve usar `grid()` com alinhamento e espaçamento adequados.
- Valide os campos para aceitar apenas números positivos e trate erros de conversão.

## Projeto Prático

### Cadastro de Usuário

Desenvolva uma aplicação gráfica que simula um formulário de cadastro de usuário. A interface deve conter:

- Campos de entrada: Nome, E-mail, Senha (com máscara), Confirmação de Senha.
- Botão "Cadastrar": ao clicar, verifica:
    - Se todos os campos estão preenchidos.
    - Se o e-mail contém `@` e `.`.
    - Se as duas senhas são iguais e têm pelo menos 6 caracteres.
- Se todos os critérios forem atendidos, exibe um Label com "Cadastro realizado com sucesso!" em verde.
- Caso contrário, exibe mensagens de erro específicas em vermelho.
- Botão "Limpar" para resetar todos os campos e mensagens.

**Orientações de implementação:**

- Organize os widgets com `grid()`, com labels na coluna 0 e entradas na coluna 1.
- Crie funções `cadastrar()` e `limpar()`.
- Na função `cadastrar()`, use `get()` para obter os valores, valide com `if` e `try/except` se necessário.
- Para exibir mensagens, utilize um Label que inicialmente está vazio e é atualizado via `config(text=..., fg=...)`.
- Envolva tudo em uma classe `CadastroApp` para praticar orientação a objetos (opcional, mas recomendado).

**Exemplo de código parcial (para referência):**

```python
import tkinter as tk

class CadastroApp:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Cadastro de Usuário")
        self.janela.geometry("400x300")
        self.criar_widgets()

    def criar_widgets(self):
        # Labels e Entries
        tk.Label(self.janela, text="Nome:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.entrada_nome = tk.Entry(self.janela, width=30)
        self.entrada_nome.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.janela, text="E-mail:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entrada_email = tk.Entry(self.janela, width=30)
        self.entrada_email.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.janela, text="Senha:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entrada_senha = tk.Entry(self.janela, show="*", width=30)
        self.entrada_senha.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.janela, text="Confirmar Senha:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.entrada_confirma = tk.Entry(self.janela, show="*", width=30)
        self.entrada_confirma.grid(row=3, column=1, padx=10, pady=5)

        # Botões
        tk.Button(self.janela, text="Cadastrar", command=self.cadastrar).grid(row=4, column=0, padx=5, pady=15, sticky="e")
        tk.Button(self.janela, text="Limpar", command=self.limpar).grid(row=4, column=1, padx=5, pady=15, sticky="w")

        # Mensagem
        self.mensagem = tk.Label(self.janela, text="", fg="red")
        self.mensagem.grid(row=5, column=0, columnspan=2)

    def cadastrar(self):
        nome = self.entrada_nome.get()
        email = self.entrada_email.get()
        senha = self.entrada_senha.get()
        confirma = self.entrada_confirma.get()

        if not all([nome, email, senha, confirma]):
            self.mensagem.config(text="Preencha todos os campos.", fg="red")
            return
        if "@" not in email or "." not in email.split("@")[-1]:
            self.mensagem.config(text="E-mail inválido.", fg="red")
            return
        if senha != confirma:
            self.mensagem.config(text="Senhas não conferem.", fg="red")
            return
        if len(senha) < 6:
            self.mensagem.config(text="Senha deve ter 6+ caracteres.", fg="red")
            return

        self.mensagem.config(text="Cadastro realizado com sucesso!", fg="green")

    def limpar(self):
        self.entrada_nome.delete(0, tk.END)
        self.entrada_email.delete(0, tk.END)
        self.entrada_senha.delete(0, tk.END)
        self.entrada_confirma.delete(0, tk.END)
        self.mensagem.config(text="")

    def iniciar(self):
        self.janela.mainloop()

if __name__ == "__main__":
    app = CadastroApp()
    app.iniciar()
```

Este projeto integra todos os widgets aprendidos e ainda reforça validação e programação orientada a objetos.

## Resumo

Neste capítulo, você aprendeu que:

- Uma GUI é composta por janelas e widgets.
- O Tkinter é a biblioteca padrão do Python para interfaces gráficas, disponível sem instalação extra.
- A estrutura básica envolve criar a janela principal (`Tk`), adicionar widgets e iniciar o `mainloop()`.
- Os widgets fundamentais são Label, Button e Entry.
- Os gerenciadores de layout `pack()` e `grid()` organizam os widgets na janela.
- Botões disparam ações através do parâmetro `command`.
- É possível capturar eventos do teclado e mouse com `bind()`.
- Sempre separe a lógica da interface e trate erros de entrada do usuário.

Com essas ferramentas, você já pode construir aplicações com janelas reais, coletar dados e fornecer respostas visuais. Esse é o primeiro passo rumo a sistemas desktop completos.

## Próximo Capítulo

No próximo capítulo, aprofundaremos no **Gerenciamento de Layout**, entendendo melhor as peculiaridades do `pack`, `grid` e `place`, e aprenderemos a organizar as interfaces de forma flexível e expansível usando **Frames**.
