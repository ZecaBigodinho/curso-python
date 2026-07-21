# Gerenciadores de Layout (Pack, Grid, Place e Frames)

## Objetivos

Neste capítulo, você aprofundará seus conhecimentos sobre organização de interfaces gráficas com Tkinter. Os objetivos são:

- Compreender o papel dos gerenciadores de layout e quando aplicar cada um.
- Dominar o `pack()` com suas opções de alinhamento, preenchimento e expansão.
- Utilizar `grid()` para construir layouts baseados em linhas e colunas, incluindo responsividade.
- Conhecer o `place()` para posicionamento absoluto e relativo, e suas limitações.
- Empregar Frames como contêineres para agrupar widgets e compor interfaces complexas.
- Combinar diferentes gerenciadores dentro de uma mesma janela para obter layouts profissionais.
- Adotar boas práticas que resultem em interfaces estáveis e de fácil manutenção.

## Pré-requisitos

Antes de avançar, certifique-se de que você domina:

- Criação de janelas com `Tk()` e `Toplevel`.
- Widgets básicos: `Label`, `Button`, `Entry`, e seus atributos principais.
- Associação de funções a botões via `command`.
- Conceitos de programação orientada a objetos (útil, mas não obrigatório, para o uso de classes nos exemplos).

Se necessário, revise o capítulo Introdução a Interfaces Gráficas e Tkinter.

## Motivação

No capítulo anterior, você aprendeu a criar janelas e adicionar alguns widgets. Entretanto, interfaces gráficas reais possuem dezenas de elementos que precisam ser organizados de forma harmoniosa, intuitiva e, principalmente, que se adaptem ao redimensionamento da janela. Imagine um formulário de cadastro com campos de nome, endereço, telefone, e-mail, além de botões de ação; sem um layout bem planejado, os widgets ficariam amontoados ou se comportariam de maneira imprevisível quando o usuário maximizasse a janela.

Os gerenciadores de layout do Tkinter resolvem exatamente esse problema. Eles controlam automaticamente a posição e o tamanho dos widgets, seguindo regras que você define. Combinados com Frames, que funcionam como recipientes retangulares, você pode dividir a janela em seções lógicas (topo, menus, área de trabalho, barra de status) e aplicar o gerenciador mais adequado a cada uma.

Dominar `pack()`, `grid()` e `place()` é o que transforma um amontoado de componentes em uma interface profissional e agradável.

## Conteúdo

### Introdução aos gerenciadores de layout

Todo widget em Tkinter precisa ser posicionado dentro de seu contêiner (a janela principal ou um Frame) por meio de um dos três gerenciadores:

- `pack()`: organiza os widgets em blocos antes de posicioná-los, geralmente empilhando-os vertical ou horizontalmente. É simples e eficaz para layouts lineares.
- `grid()`: divide o contêiner em uma grade de linhas e colunas, oferecendo controle fino sobre alinhamento e proporções.
- `place()`: permite definir coordenadas absolutas ou relativas, mas é menos flexível e responsivo.

!!! warning "Não misture gerenciadores no mesmo contêiner"
    Um mesmo contêiner (Frame, Tk, Toplevel) deve usar apenas um tipo de gerenciador para seus filhos diretos. Tentar mesclar pack e grid no mesmo pai resultará em erro. No entanto, você pode usar diferentes gerenciadores em frames distintos que coexistem na mesma janela.

### O gerenciador pack()

O `pack()` empilha widgets. Por padrão, o preenchimento é vertical e centralizado, mas pode ser controlado por diversas opções:

| Opção | Descrição | Valores de exemplo |
|---|---|---|
| `side` | Lado onde o widget será ancorado. | `tk.TOP` (padrão), `tk.BOTTOM`, `tk.LEFT`, `tk.RIGHT` |
| `fill` | Se o widget deve se expandir para preencher o espaço disponível na direção especificada. | `tk.NONE` (padrão), `tk.X`, `tk.Y`, `tk.BOTH` |
| `expand` | Se o widget deve se expandir quando o contêiner for redimensionado. | `True` / `False` (padrão `False`) |
| `anchor` | Alinhamento do widget dentro do espaço alocado, quando fill não é usado ou não preenche. | `tk.N`, `tk.S`, `tk.E`, `tk.W`, `tk.CENTER`, etc. |
| `padx`, `pady` | Espaçamento externo horizontal/vertical entre o widget e os vizinhos. | Valor inteiro (pixels) |
| `ipadx`, `ipady` | Espaçamento interno horizontal/vertical (aumenta o tamanho do widget). | Valor inteiro (pixels) |

Exemplo básico:

```python
import tkinter as tk

janela = tk.Tk()
janela.title("Exemplo Pack")
janela.geometry("300x200")

# Widgets empilhados verticalmente
tk.Label(janela, text="Topo", bg="lightblue").pack(fill=tk.X)
tk.Label(janela, text="Centro", bg="lightgreen").pack(fill=tk.BOTH, expand=True)
tk.Label(janela, text="Rodapé", bg="lightgray").pack(side=tk.BOTTOM, fill=tk.X)

janela.mainloop()
```

Aqui, o primeiro label preenche horizontalmente; o segundo expande-se para ocupar todo o espaço restante; o terceiro ancora-se na parte inferior.

!!! tip "Use expand=True com fill=BOTH para que um widget ocupe o espaço excedente"
    Esse é o segredo para criar áreas que crescem com a janela. Normalmente, há um widget central (como um Text ou Frame) que recebe `expand=True` e `fill=BOTH`.

### O gerenciador grid()

O `grid()` posiciona os widgets em células formadas por linhas (`row`) e colunas (`column`). É o mais indicado para formulários e layouts complexos.

Principais parâmetros:

- `row`, `column`: índices da célula (base 0).
- `rowspan`, `columnspan`: número de linhas/colunas que o widget ocupa.
- `sticky`: direção em que o widget "gruda" nas bordas da célula (combinação de N, S, E, W). Exemplo: `sticky="ew"` faz o widget preencher horizontalmente.
- `padx`, `pady`: espaçamento externo.
- `ipadx`, `ipady`: espaçamento interno.

Para tornar o layout responsivo, configuramos o peso das linhas e colunas com `grid_rowconfigure` e `grid_columnconfigure`. Um peso maior indica que a linha/coluna vai se expandir proporcionalmente quando a janela for redimensionada.

```python
import tkinter as tk

janela = tk.Tk()
janela.title("Exemplo Grid Responsivo")
janela.geometry("400x300")

# Configura pesos: a linha 0 e coluna 0 não se expandem; linha 1 e coluna 1 se expandem
janela.grid_rowconfigure(1, weight=1)
janela.grid_columnconfigure(1, weight=1)

# Widgets fixos no topo
tk.Label(janela, text="Nome:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
entrada = tk.Entry(janela)
entrada.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

# Área central que se expande
texto = tk.Text(janela)
texto.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

# Botão fixo na parte inferior
tk.Button(janela, text="Enviar").grid(row=2, column=0, columnspan=2, pady=10)

janela.mainloop()
```

Neste exemplo, a Text ocupa duas colunas e expande-se em todas as direções ("nsew"). A linha 1 tem `weight=1`, portanto recebe todo o espaço vertical extra.

### O gerenciador place()

O `place()` usa coordenadas absolutas (em pixels) ou relativas (proporcionais ao tamanho do contêiner). É útil para posicionamentos precisos, sobreposições e animações simples, mas deve ser evitado para layouts de propósito geral, pois não se adapta automaticamente a redimensionamentos.

Opções principais:

- `x`, `y`: coordenadas absolutas (canto superior esquerdo).
- `relx`, `rely`: coordenadas relativas (0.0 a 1.0).
- `width`, `height`: tamanho absoluto.
- `relwidth`, `relheight`: tamanho relativo.
- `anchor`: ponto de referência (como `tk.CENTER`).

```python
import tkinter as tk

janela = tk.Tk()
janela.title("Exemplo Place")
janela.geometry("400x300")

# Label centralizado relativamente
tk.Label(janela, text="Centro", bg="yellow").place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Botão no canto inferior direito
tk.Button(janela, text="Fechar", command=janela.destroy).place(relx=1.0, rely=1.0, anchor=tk.SE)

janela.mainloop()
```

!!! note "Use place com moderação"
    `place` é excelente para posicionar um elemento fixo (como um logotipo) ou uma janela de splash, mas para formulários e painéis, prefira `grid` ou `pack`.

### Frames como contêineres

`Frame` é um widget retangular cuja única finalidade é agrupar outros widgets. Ele não tem aparência própria, mas pode receber bordas, cores e relevo. A grande vantagem é que cada Frame pode ter seu próprio gerenciador de layout, permitindo compor interfaces complexas com diferentes estratégias de organização.

```python
import tkinter as tk

janela = tk.Tk()
janela.title("Uso de Frames")
janela.geometry("500x300")

# Frame superior com pack
frame_topo = tk.Frame(janela, bg="lightblue", height=50)
frame_topo.pack(fill=tk.X)
tk.Label(frame_topo, text="Barra de ferramentas", bg="lightblue").pack(side=tk.LEFT, padx=10)

# Frame inferior com grid
frame_inferior = tk.Frame(janela)
frame_inferior.pack(fill=tk.BOTH, expand=True)

# Dentro do frame inferior, usamos grid para criar um formulário
tk.Label(frame_inferior, text="Campo A:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
tk.Entry(frame_inferior).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
tk.Label(frame_inferior, text="Campo B:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
tk.Entry(frame_inferior).grid(row=1, column=1, padx=5, pady=5, sticky="ew")

# Configura a expansão da coluna 1 no frame inferior
frame_inferior.grid_columnconfigure(1, weight=1)

janela.mainloop()
```

Neste código, a janela principal usa pack para empilhar dois frames. O primeiro contém uma barra de ferramentas (pack horizontal) e o segundo contém um formulário organizado com grid. Assim, cada região é administrada de forma independente.

### Combinação de gerenciadores: estratégia recomendada

Uma prática comum é usar `pack` para organizar frames que representam grandes seções da janela (topo, centro, rodapé), e dentro de cada frame empregar `grid` para detalhar o layout. Essa separação mantém o código compreensível e flexível.

### Responsividade e boas práticas

- Sempre defina `weight` para pelo menos uma linha e uma coluna quando usar `grid` se desejar que a janela seja redimensionável.
- No `pack`, use `expand=True` e `fill=BOTH` em pelo menos um widget (normalmente um frame central).
- Evite `place` a menos que seja absolutamente necessário.
- Utilize frames mesmo para agrupar poucos widgets; isso facilita futuras modificações.
- Dê nomes significativos aos frames (`frame_formulario`, `frame_botoes`).
- Considere encapsular seções da interface em classes que herdam de `Frame`.

## Exemplos

??? example "Exemplo 1: Layout de calculadora com grid"
    === "Código"
        ```python
        import tkinter as tk

        janela = tk.Tk()
        janela.title("Calculadora Layout")
        janela.geometry("250x300")

        # Display
        display = tk.Entry(janela, font=("Arial", 18), justify="right")
        display.grid(row=0, column=0, columnspan=4, sticky="ew", padx=5, pady=5)

        # Botões
        botoes = [
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
            ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("+", 4, 3),
        ]

        for (texto, row, col) in botoes:
            tk.Button(janela, text=texto, width=5, height=2).grid(row=row, column=col, padx=2, pady=2)

        # Configura pesos para as colunas se expandirem igualmente
        for i in range(4):
            janela.grid_columnconfigure(i, weight=1)
        for i in range(5):
            janela.grid_rowconfigure(i, weight=1)

        janela.mainloop()
        ```

    === "Resultado"
        Uma janela com um display na parte superior e uma grade 4x4 de botões, que se redimensionam suavemente ao aumentar a janela.

    === "Explicação"
        Usamos `grid` para posicionar cada botão em sua célula. `columnspan=4` faz o display ocupar toda a largura. Os pesos iguais em linhas e colunas garantem que os botões se expandam uniformemente. Esse é um exemplo clássico de layout em grade.

??? example "Exemplo 2: Interface com três áreas usando pack e frames"
    === "Código"
        ```python
        import tkinter as tk

        janela = tk.Tk()
        janela.title("Layout com Frames")
        janela.geometry("600x400")

        # Frame do topo (barra de menu simulada)
        topo = tk.Frame(janela, bg="gray20", height=40)
        topo.pack(fill=tk.X)
        tk.Label(topo, text="Arquivo  Editar  Ajuda", fg="white", bg="gray20").pack(side=tk.LEFT, padx=10)

        # Frame central (área de trabalho)
        centro = tk.Frame(janela, bg="white")
        centro.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        tk.Label(centro, text="Área de conteúdo", bg="white").pack(expand=True)

        # Frame inferior (barra de status)
        rodape = tk.Frame(janela, bg="lightgray", height=25)
        rodape.pack(fill=tk.X, side=tk.BOTTOM)
        tk.Label(rodape, text="Pronto", bg="lightgray").pack(side=tk.LEFT, padx=10)

        janela.mainloop()
        ```

    === "Resultado"
        Uma janela com barra superior escura, área central branca que se expande, e barra de status cinza na parte inferior.

    === "Explicação"
        Três frames empilhados com `pack`: topo (`fill=X`), centro (`expand=True`, `fill=BOTH`) e rodapé (`side=BOTTOM`, `fill=X`). Dentro de cada frame, o layout é simples. Essa é a estrutura básica de muitas aplicações desktop.

??? example "Exemplo 3: Formulário com grid e frames aninhados"
    === "Código"
        ```python
        import tkinter as tk

        janela = tk.Tk()
        janela.title("Formulário Completo")
        janela.geometry("450x250")

        # Frame principal do formulário
        form = tk.Frame(janela)
        form.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Campos
        campos = ["Nome:", "E-mail:", "Telefone:", "Endereço:"]
        for i, campo in enumerate(campos):
            tk.Label(form, text=campo).grid(row=i, column=0, sticky="w", pady=3)
            tk.Entry(form, width=40).grid(row=i, column=1, sticky="ew", pady=3)

        # Frame para os botões (aninhado dentro do form)
        botoes = tk.Frame(form)
        botoes.grid(row=len(campos), column=0, columnspan=2, pady=15)

        tk.Button(botoes, text="Salvar").pack(side=tk.LEFT, padx=5)
        tk.Button(botoes, text="Cancelar").pack(side=tk.LEFT, padx=5)

        # Expansão da coluna dos campos
        form.grid_columnconfigure(1, weight=1)

        janela.mainloop()
        ```

    === "Resultado"
        Um formulário com quatro linhas de label+entry, e dois botões centralizados abaixo. Ao redimensionar, os campos de entrada crescem horizontalmente.

    === "Explicação"
        O frame form contém a grade principal (labels e entries). Dentro dele, um frame botoes agrupa os botões e é posicionado com `grid`. Dentro de botoes, voltamos a usar `pack` para alinhar os botões lado a lado. Isso exemplifica a combinação de gerenciadores em níveis diferentes.

## Exercícios

### Básico (fixação)

1. Crie uma janela com três Labels: "Topo", "Centro" e "Rodapé". Use `pack()` para que o "Topo" fique no topo preenchendo a largura, o "Rodapé" na parte inferior, e o "Centro" expanda para ocupar o espaço restante.
2. Utilizando `grid()`, monte uma janela com dois Labels e dois Entries, como se fosse um login (usuário e senha). Use `sticky` e `padx`/`pady` para espaçamento.
3. Posicione um botão "Ajuda" no canto superior direito da janela usando `place()`. Dica: use `relx=1.0`, `rely=0.0` e `anchor="ne"`.

### Intermediário (aplicação)

Construa uma interface para um conversor de moedas, contendo:

- Um Frame superior onde o usuário insere o valor e seleciona a moeda de origem e destino (use OptionMenu ou Combobox se já conhecer; caso contrário, use Entry para as moedas também).
- Um Frame central onde aparece o resultado.
- Um Frame inferior com os botões "Converter" e "Limpar".
- Utilize pack para organizar os frames e grid dentro do frame superior. Garanta que o layout se ajuste ao redimensionar.

### Avançado (desafio)

Desenvolva uma interface de calculadora de IMC com a seguinte estrutura:

- A janela principal deve ter um Frame para entrada de dados (peso e altura), um Frame para exibição do resultado e classificação, e um Frame para os botões.
- Use `grid` para dispor Labels e Entries no frame de entrada.
- Use `pack` para empilhar os três frames na janela principal.
- O frame de resultado deve conter um Text ou Label que mostre o IMC e a classificação, e deve se expandir verticalmente.
- Implemente a responsividade: ao redimensionar a janela, a área de resultado deve crescer, enquanto os campos de entrada mantêm seu tamanho.
- Adicione um menu superior (com Menu) que não afete o layout (é um widget à parte). Opcional: use classes para encapsular cada seção.

## Projeto Prático

### Painel de Controle com Abas (simulado com Frames)

Construa uma aplicação que simula um painel de controle com "abas" laterais. Não usaremos o widget Notebook, mas sim botões que alternam a visibilidade de diferentes frames.

**Requisitos:**

- A janela principal contém dois frames lado a lado: uma barra lateral (largura fixa ~150px) e uma área de conteúdo (o restante).
- A barra lateral é organizada com `pack()` vertical: contém botões "Dashboard", "Configurações", "Relatórios".
- A área de conteúdo contém três frames sobrepostos (apenas um visível por vez), correspondentes às abas.
- Cada aba deve ter um layout interno diferente:
    - **Dashboard:** um Label de boas-vindas centralizado.
    - **Configurações:** um formulário com `grid()` contendo campos como "Nome do usuário", "Tema", "Notificações" (use Checkbutton).
    - **Relatórios:** uma área com Text e um botão "Gerar Relatório".
- Os botões da barra lateral devem chamar funções que escondem todos os frames de conteúdo e mostram o correspondente (use `pack_forget()` ou `grid_forget()` para esconder, e depois `pack()` ou `grid()` para mostrar novamente).

**Estrutura recomendada:**

```python
import tkinter as tk

class PainelApp:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Painel de Controle")
        self.janela.geometry("700x400")

        # Frame da barra lateral
        self.barra_lateral = tk.Frame(self.janela, bg="navy", width=150)
        self.barra_lateral.pack(side=tk.LEFT, fill=tk.Y)
        self.barra_lateral.pack_propagate(False)  # impede que o frame encolha

        # Frame de conteúdo
        self.conteudo = tk.Frame(self.janela, bg="white")
        self.conteudo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Criar as abas (frames dentro de conteúdo)
        self.aba_dashboard = tk.Frame(self.conteudo, bg="white")
        self.aba_config = tk.Frame(self.conteudo, bg="white")
        self.aba_relatorios = tk.Frame(self.conteudo, bg="white")

        # Preencher cada aba
        self._criar_dashboard()
        self._criar_config()
        self._criar_relatorios()

        # Botões da barra lateral
        tk.Button(self.barra_lateral, text="Dashboard", command=self.mostrar_dashboard).pack(fill=tk.X, pady=2)
        tk.Button(self.barra_lateral, text="Configurações", command=self.mostrar_config).pack(fill=tk.X, pady=2)
        tk.Button(self.barra_lateral, text="Relatórios", command=self.mostrar_relatorios).pack(fill=tk.X, pady=2)

        # Mostrar aba inicial
        self.mostrar_dashboard()

    def _criar_dashboard(self):
        tk.Label(self.aba_dashboard, text="Bem-vindo ao Painel", font=("Arial", 16)).pack(expand=True)

    def _criar_config(self):
        tk.Label(self.aba_config, text="Nome:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        tk.Entry(self.aba_config).grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        tk.Label(self.aba_config, text="Tema:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        tk.Entry(self.aba_config).grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        tk.Checkbutton(self.aba_config, text="Ativar notificações").grid(row=2, column=1, sticky="w")
        self.aba_config.grid_columnconfigure(1, weight=1)

    def _criar_relatorios(self):
        self.texto_relatorio = tk.Text(self.aba_relatorios)
        self.texto_relatorio.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        tk.Button(self.aba_relatorios, text="Gerar Relatório").pack(pady=5)

    def _esconder_abas(self):
        for aba in (self.aba_dashboard, self.aba_config, self.aba_relatorios):
            aba.pack_forget()

    def mostrar_dashboard(self):
        self._esconder_abas()
        self.aba_dashboard.pack(fill=tk.BOTH, expand=True)

    def mostrar_config(self):
        self._esconder_abas()
        self.aba_config.pack(fill=tk.BOTH, expand=True)

    def mostrar_relatorios(self):
        self._esconder_abas()
        self.aba_relatorios.pack(fill=tk.BOTH, expand=True)

    def iniciar(self):
        self.janela.mainloop()

if __name__ == "__main__":
    app = PainelApp()
    app.iniciar()
```

**Desafios adicionais:**

- Estilize a barra lateral com ícones (use `PhotoImage` ou apenas texto).
- Faça com que o botão da aba ativa fique destacado (mude a cor de fundo).
- Permita que o usuário alterne entre abas com atalhos de teclado (Ctrl+1, Ctrl+2, etc.) usando `bind()`.

Este projeto consolida os três gerenciadores de layout e frames, mostrando como construir uma aplicação modular e navegável.

## Resumo

Neste capítulo, você aprendeu que:

- O Tkinter possui três gerenciadores de layout: `pack`, `grid` e `place`, cada um com propósitos distintos.
- `pack` é ideal para layouts lineares simples, empilhando widgets vertical ou horizontalmente, com opções de preenchimento e expansão.
- `grid` organiza os widgets em uma grade de linhas e colunas, oferecendo controle detalhado e suporte a responsividade através da configuração de pesos.
- `place` posiciona widgets de forma absoluta ou relativa, mas deve ser usado com moderação.
- `Frame` é um contêiner essencial para agrupar widgets e combinar diferentes gerenciadores na mesma janela.
- A estratégia recomendada é usar `pack` para dividir a janela em grandes regiões e `grid` ou `pack` nos detalhes internos, com frames aninhados.
- Definir `weight` nas linhas/colunas com `grid` ou usar `expand`/`fill` com `pack` garante interfaces que se adaptam ao redimensionamento.

O domínio dos gerenciadores de layout transforma a aparência e usabilidade das suas aplicações, permitindo que você crie interfaces profissionais e responsivas.

## Próximo Capítulo

No próximo capítulo, entraremos em **Eventos e Interatividade**, onde aprenderemos a capturar cliques de mouse, movimento, atalhos de teclado avançados e a usar variáveis de controle (`tk.StringVar`, `tk.IntVar`) para sincronizar a interface com os dados do programa.
