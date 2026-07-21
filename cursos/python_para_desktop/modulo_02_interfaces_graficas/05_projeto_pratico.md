# Projeto Prático: Dashboard Financeiro Desktop

## Objetivos

Neste capítulo, você aplicará de forma integrada todos os conhecimentos do Módulo 02 para construir um Dashboard Financeiro Desktop. Os objetivos são:

- Projetar e implementar uma aplicação desktop completa com múltiplas abas, combinando Tkinter, CustomTkinter e matplotlib.
- Aplicar gerenciadores de layout (`pack`, `grid`) e contêineres (`Frame`, `CTkFrame`) para estruturar interfaces complexas.
- Utilizar variáveis de controle (`StringVar`, `DoubleVar`) e eventos (`bind`, `command`, `trace`) para criar interatividade dinâmica.
- Integrar gráficos (pizza, barras) no ambiente Tkinter para visualização de dados financeiros.
- Implementar persistência de dados com arquivos JSON, carregando e salvando transações automaticamente.
- Tratar exceções e validar entradas do usuário para garantir robustez.
- Modularizar o código em classes e funções, seguindo boas práticas de organização.

## Pré-requisitos

Antes de iniciar, você deve dominar:

- Tkinter básico: `Tk`, `Label`, `Button`, `Entry`, `Frame`, `Toplevel`.
- CustomTkinter: `CTk`, `CTkButton`, `CTkEntry`, `CTkLabel`, `CTkFrame`, `CTkTabview` (abas).
- Gerenciadores de layout: `pack()`, `grid()`, aninhamento de frames.
- Eventos e variáveis de controle: `bind()`, `command`, `StringVar`, `IntVar`, `DoubleVar`, `trace_add`.
- Manipulação de arquivos e JSON: `json.dump`, `json.load`, `pathlib`.
- Tratamento de exceções: `try`/`except`.
- Conceitos de módulos e funções, incluindo orientação a objetos básica.
- Matplotlib: instalação (`pip install matplotlib`) e conhecimentos básicos de gráficos (opcional, abordaremos a integração).

Se algum desses temas não estiver consolidado, revise os capítulos anteriores.

## Motivação

Um dashboard financeiro pessoal é uma ferramenta extremamente útil para controlar receitas e despesas, visualizar para onde vai o dinheiro e planejar o futuro. Construir o seu próprio oferece a vantagem de ser totalmente personalizável, além de consolidar todo o aprendizado de interfaces gráficas, manipulação de dados e eventos.

Neste projeto, vamos além de simples formulários: usaremos abas para organizar diferentes visões (visão geral, lista de transações, relatórios gráficos), integraremos gráficos de pizza e barras usando matplotlib, e implementaremos persistência em JSON para que os dados sejam mantidos entre sessões. O visual será moderno com CustomTkinter, demonstrando como entregar uma aplicação desktop com aparência profissional.

Ao final, você terá um software completo que poderá usar no seu dia a dia e que servirá como portfólio.

## Conteúdo

### Visão geral do projeto

O Dashboard Financeiro permitirá:

- Registrar transações com descrição, valor (positivo para receita, negativo para despesa), categoria e data.
- Visualizar o saldo atual, total de receitas e total de despesas na aba "Visão Geral".
- Listar todas as transações em uma tabela na aba "Transações", com possibilidade de remoção.
- Gerar gráficos na aba "Relatórios": um gráfico de pizza com distribuição de gastos por categoria e um gráfico de barras com evolução do saldo ao longo dos meses (simulado).
- Persistir os dados em um arquivo `financas.json`.
- Interface com abas usando `CTkTabview`.

### Estrutura de arquivos sugerida

```text
dashboard_financeiro/
├── main.py               # Ponto de entrada e classe principal da aplicação
├── modelos.py            # Definição da classe Transacao e funções auxiliares
├── persistencia.py       # Funções para carregar/salvar dados em JSON
├── interface/
│   ├── __init__.py
│   ├── aba_visao_geral.py
│   ├── aba_transacoes.py
│   └── aba_relatorios.py
└── financas.json         # Gerado automaticamente
```

Neste capítulo, para facilitar a compreensão, apresentaremos o código de forma concentrada em um único arquivo, mas ressaltaremos os módulos e como separá-los.

### Modelagem dos dados

Cada transação será representada por um dicionário com as chaves:

- `id`: inteiro único.
- `descricao`: string.
- `valor`: float (positivo = receita, negativo = despesa).
- `categoria`: string (ex.: "Alimentação", "Transporte", "Lazer", "Salário", "Outros").
- `data`: string no formato "YYYY-MM-DD".

Exemplo de lista de transações:

```python
transacoes = [
    {"id": 1, "descricao": "Salário", "valor": 5000.0, "categoria": "Salário", "data": "2025-07-01"},
    {"id": 2, "descricao": "Supermercado", "valor": -350.0, "categoria": "Alimentação", "data": "2025-07-03"},
]
```

### Persistência em JSON

Criaremos funções `carregar_dados(caminho)` e `salvar_dados(caminho, transacoes)`. Trataremos exceções como `FileNotFoundError` e `JSONDecodeError` para iniciar com lista vazia.

```python
import json
from pathlib import Path

def carregar_dados(caminho="financas.json"):
    if not Path(caminho).exists():
        return []
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def salvar_dados(transacoes, caminho="financas.json"):
    try:
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(transacoes, f, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"Erro ao salvar: {e}")
```

### Interface gráfica com CustomTkinter

Utilizaremos `CTk` para a janela principal e `CTkTabview` para as abas. Cada aba será um frame adicionado ao tabview.

**Estrutura básica com abas**

```python
import customtkinter as ctk

class DashboardApp:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.janela = ctk.CTk()
        self.janela.title("Dashboard Financeiro")
        self.janela.geometry("800x600")

        # Tabview para as abas
        self.tabview = ctk.CTkTabview(self.janela)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        self.tabview.add("Visão Geral")
        self.tabview.add("Transações")
        self.tabview.add("Relatórios")

        # Criar conteúdo das abas
        self.criar_aba_visao_geral()
        self.criar_aba_transacoes()
        self.criar_aba_relatorios()

    def criar_aba_visao_geral(self):
        aba = self.tabview.tab("Visão Geral")
        # ... widgets

    # ... outras abas

    def iniciar(self):
        self.janela.mainloop()

if __name__ == "__main__":
    app = DashboardApp()
    app.iniciar()
```

### Aba "Visão Geral"

Exibirá cartões com saldo atual, receitas totais e despesas totais. Utilizaremos `CTkFrame` com cantos arredondados e labels de destaque. Os valores serão atualizados sempre que a aba for selecionada (usando evento `<<NotebookTabChanged>>` ou, de forma mais simples, recarregando ao exibir). Podemos usar o método `configure` dos labels ou variáveis de controle `StringVar`.

### Aba "Transações"

Conterá:

- Formulário para adicionar transação: `CTkEntry` para descrição e valor, `CTkOptionMenu` para categoria e `CTkEntry` para data (ou `CTkDateEntry` se quisermos, mas não é nativo; manteremos texto).
- Botão "Adicionar".
- Uma área rolável (`CTkScrollableFrame`) exibindo cada transação com um botão "Remover". Ao remover, atualizar lista e persistir.
- Validação: valor deve ser numérico, campos não vazios, data no formato correto.

### Aba "Relatórios"

Integrará gráficos do matplotlib embutidos em um `CTkFrame`. Usaremos `FigureCanvasTkAgg` para exibir os gráficos. Incluirá:

- Gráfico de pizza: distribuição de despesas por categoria (valores negativos agrupados por categoria, somados em valor absoluto).
- Gráfico de barras: evolução do saldo acumulado mês a mês (precisaremos de dados históricos; podemos simular agrupando transações por mês).

### Eventos e interatividade

- Ao adicionar ou remover transações, a lista em memória é atualizada e os dados são salvos automaticamente.
- As abas "Visão Geral" e "Relatórios" precisam refletir as mudanças. Usaremos um método `atualizar_interface` que recarrega os labels e redesenha gráficos, chamado sempre que uma transação é adicionada/removida ou quando a aba é selecionada. Podemos vincular um evento ao tabview ou usar callbacks após cada ação.
- Para capturar a mudança de aba, o `CTkTabview` possui um comando `configure(command=funcao)` que é executado ao trocar de aba.

### Integração com Matplotlib

Instale matplotlib:

```bash
pip install matplotlib
```

Exemplo de gráfico de pizza:

```python
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def criar_grafico_pizza(frame, dados):
    # Supondo que 'dados' seja um dicionário {categoria: valor_absoluto}
    fig, ax = plt.subplots(figsize=(4,3), dpi=100)
    ax.pie(dados.values(), labels=dados.keys(), autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
```

Lembre-se de destruir o canvas anterior ao atualizar, ou limpar a figura.

### Tratamento de erros e validações

- Entrada de valor: usar `try: float(...)` e capturar `ValueError`.
- Data: validar formato com `datetime.strptime(data, "%Y-%m-%d")`.
- Categoria: garantir que não está vazia.
- Exceções de arquivo ao salvar/carregar.

### Boas práticas

- Separar a lógica de negócios (cálculo de saldos, agrupamentos) em funções puras, independentes da interface.
- Utilizar variáveis de controle para labels que mudam frequentemente.
- Fechar figuras do matplotlib ao sair para liberar memória.
- Usar constantes para categorias e configurações.
- Comentar as seções do código.

## Exemplos

??? example "Exemplo 1: Estrutura da aba Visão Geral"
    === "Código"
        ```python
        def criar_aba_visao_geral(self):
            aba = self.tabview.tab("Visão Geral")
            # Frame para os cartões
            frame_cartoes = ctk.CTkFrame(aba)
            frame_cartoes.pack(fill="x", padx=20, pady=20)

            # Saldo
            self.saldo_var = ctk.StringVar(value="R$ 0.00")
            cartao_saldo = ctk.CTkFrame(frame_cartoes, fg_color="#2E7D32", corner_radius=10)
            cartao_saldo.pack(side="left", expand=True, fill="both", padx=10, pady=10)
            ctk.CTkLabel(cartao_saldo, text="Saldo Atual", font=("Arial", 14)).pack(pady=5)
            ctk.CTkLabel(cartao_saldo, textvariable=self.saldo_var, font=("Arial", 24, "bold")).pack(pady=5)

            # Receitas
            self.receitas_var = ctk.StringVar(value="R$ 0.00")
            cartao_receitas = ctk.CTkFrame(frame_cartoes, fg_color="#1565C0", corner_radius=10)
            cartao_receitas.pack(side="left", expand=True, fill="both", padx=10, pady=10)
            ctk.CTkLabel(cartao_receitas, text="Receitas Totais", font=("Arial", 14)).pack(pady=5)
            ctk.CTkLabel(cartao_receitas, textvariable=self.receitas_var, font=("Arial", 24, "bold")).pack(pady=5)

            # Despesas
            self.despesas_var = ctk.StringVar(value="R$ 0.00")
            cartao_despesas = ctk.CTkFrame(frame_cartoes, fg_color="#C62828", corner_radius=10)
            cartao_despesas.pack(side="left", expand=True, fill="both", padx=10, pady=10)
            ctk.CTkLabel(cartao_despesas, text="Despesas Totais", font=("Arial", 14)).pack(pady=5)
            ctk.CTkLabel(cartao_despesas, textvariable=self.despesas_var, font=("Arial", 24, "bold")).pack(pady=5)

        def atualizar_visao_geral(self):
            receitas = sum(t['valor'] for t in self.transacoes if t['valor'] > 0)
            despesas = sum(t['valor'] for t in self.transacoes if t['valor'] < 0)
            saldo = receitas + despesas
            self.saldo_var.set(f"R$ {saldo:,.2f}")
            self.receitas_var.set(f"R$ {receitas:,.2f}")
            self.despesas_var.set(f"R$ {despesas:,.2f}")
        ```

    === "Resultado"
        Três cartões lado a lado, com cores distintas, exibindo saldo, receitas e despesas formatados. Os valores são atualizados automaticamente sempre que `atualizar_visao_geral()` é chamado.

    === "Explicação"
        Usamos `CTkFrame` como cartão, definindo `fg_color` para cada um. Variáveis `StringVar` são vinculadas aos labels de valor. O método `atualizar_visao_geral` itera sobre a lista de transações (atributo `self.transacoes`) e atualiza as variáveis. Essa função será chamada após qualquer modificação nas transações e ao selecionar a aba.

??? example "Exemplo 2: Adicionando transação com validação"
    === "Código"
        ```python
        def adicionar_transacao(self):
            desc = self.entry_desc.get().strip()
            valor_str = self.entry_valor.get().strip()
            categoria = self.opcao_categoria.get()
            data_str = self.entry_data.get().strip()

            # Validações
            if not desc:
                messagebox.showwarning("Aviso", "Descrição é obrigatória.")
                return
            try:
                valor = float(valor_str)
            except ValueError:
                messagebox.showwarning("Aviso", "Valor deve ser numérico (use ponto para decimais).")
                return
            if categoria == "":
                messagebox.showwarning("Aviso", "Selecione uma categoria.")
                return
            # Validar data
            from datetime import datetime
            try:
                datetime.strptime(data_str, "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning("Aviso", "Data inválida. Use AAAA-MM-DD.")
                return

            # Criar transação
            novo_id = max((t['id'] for t in self.transacoes), default=0) + 1
            nova = {
                "id": novo_id,
                "descricao": desc,
                "valor": valor,
                "categoria": categoria,
                "data": data_str
            }
            self.transacoes.append(nova)
            self.salvar_dados()
            self.atualizar_interface()
            # Limpar campos
            self.entry_desc.delete(0, "end")
            self.entry_valor.delete(0, "end")
            self.entry_data.delete(0, "end")
            messagebox.showinfo("Sucesso", "Transação adicionada.")
        ```

    === "Resultado"
        Após preencher os campos e clicar em Adicionar, a transação é inserida na lista, o arquivo JSON é atualizado e a interface reflete as mudanças (visão geral e lista de transações). Se algum campo for inválido, um aviso é exibido.

    === "Explicação"
        Implementamos validações sequenciais, retornando cedo se algo falhar. A geração de ID é feita pegando o maior ID atual +1. Após adicionar, os campos são limpos e uma mensagem de confirmação é mostrada. O método `atualizar_interface` será responsável por recarregar todas as abas (visão geral, lista de transações, gráficos).

??? example "Exemplo 3: Gráfico de pizza na aba Relatórios"
    === "Código"
        ```python
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        def criar_grafico_pizza(self, frame):
            # Agrupar despesas por categoria (valores negativos)
            despesas = [t for t in self.transacoes if t['valor'] < 0]
            if not despesas:
                ctk.CTkLabel(frame, text="Nenhuma despesa registrada.").pack()
                return
            categorias = {}
            for t in despesas:
                cat = t['categoria']
                categorias[cat] = categorias.get(cat, 0) + abs(t['valor'])

            fig, ax = plt.subplots(figsize=(4,3), dpi=100)
            ax.pie(categorias.values(), labels=categorias.keys(), autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            ax.set_title("Distribuição de Despesas")

            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            # Armazenar referência para evitar garbage collection
            self.canvas_pizza = canvas
        ```

    === "Resultado"
        Um gráfico de pizza é exibido na aba Relatórios, mostrando o percentual de cada categoria de despesa. Se não houver despesas, uma mensagem é mostrada.

    === "Explicação"
        Filtramos transações com valor negativo, agrupamos por categoria somando os valores absolutos. Criamos a figura matplotlib e a embutimos no frame usando `FigureCanvasTkAgg`. É importante manter uma referência ao canvas (ex.: `self.canvas_pizza`) para que não seja destruído pelo garbage collector.

## Exercícios

### Básico (fixação)

1. Execute o código base do Dashboard (disponível no Projeto Prático) e adicione algumas transações. Verifique se o arquivo `financas.json` é criado e se os dados persistem ao fechar e reabrir o programa.
2. Altere as cores dos cartões na aba "Visão Geral" para tons de sua preferência.
3. Adicione uma validação extra: o valor não pode ser zero.

### Intermediário (aplicação)

1. Adicione uma nova aba "Orçamento Mensal" que permita definir um limite de gastos por categoria e exiba um alerta visual (ex.: label vermelho) se as despesas naquele mês ultrapassarem o limite. Utilize dicionários para armazenar os limites e persista essas configurações em um arquivo separado ou dentro do mesmo JSON.
2. Na aba "Transações", implemente um filtro por categoria usando um `CTkOptionMenu`. Ao selecionar uma categoria, exiba apenas as transações correspondentes na lista rolável.

### Avançado (desafio)

1. Substitua a entrada manual de data por um widget de calendário (use `tkcalendar` ou `CTkDatePicker` se disponível, ou adapte com Entry). Garanta que o formato seja mantido.
2. Adicione um gráfico de linha na aba "Relatórios" que mostre a evolução do saldo acumulado dia a dia, baseado na ordem cronológica das transações. Para isso, ordene as transações por data, calcule o saldo acumulado e plote com matplotlib. Atualize o gráfico sempre que houver mudanças.

## Projeto Prático

### Guia Passo a Passo para Construir o Dashboard

Vamos construir o Dashboard Financeiro do zero. Siga cada etapa.

#### 1. Configuração do ambiente

Instale customtkinter e matplotlib:

```bash
pip install customtkinter matplotlib
```

Crie um diretório `dashboard_financeiro` e dentro dele um arquivo `main.py`.

#### 2. Estrutura inicial e carregamento de dados

No `main.py`, importe os módulos necessários e defina as funções de persistência conforme mostrado na seção de Conteúdo.

#### 3. Classe principal DashboardApp

- No `__init__`, configure a aparência (dark, dark-blue), crie a janela e o `CTkTabview` com as três abas.
- Carregue as transações do arquivo chamando `self.transacoes = carregar_dados()`.
- Crie as três abas (métodos `criar_aba_visao_geral`, `criar_aba_transacoes`, `criar_aba_relatorios`).
- Após criar as abas, chame `self.atualizar_interface()` para preencher os dados iniciais.
- Configure o comando de mudança de aba: `self.tabview.configure(command=self.ao_mudar_aba)` (defina um método que chama `atualizar_interface`).

#### 4. Aba "Visão Geral"

- Crie três `CTkFrame` como cartões, usando `side="left"` dentro de um frame horizontal.
- Associe `StringVar` para saldo, receitas e despesas.
- Implemente `atualizar_visao_geral` conforme exemplo.

#### 5. Aba "Transações"

- Crie um frame superior com `CTkEntry` para descrição, valor e data, e `CTkOptionMenu` para categorias (valores: "Alimentação", "Transporte", "Lazer", "Salário", "Outros").
- Adicione um botão "Adicionar" que chama `adicionar_transacao` (veja exemplo).
- Abaixo, crie um `CTkScrollableFrame` que conterá os itens das transações. No método `atualizar_lista_transacoes`, limpe esse frame e recrie os widgets para cada transação. Cada linha terá labels e um botão "Remover" que chama `remover_transacao(id)`.
- O método `remover_transacao` remove o item da lista, salva e atualiza a interface.

#### 6. Aba "Relatórios"

- Adicione um frame para o gráfico de pizza. No método `atualizar_relatorios`, destrua o canvas anterior (se existir) e recrie o gráfico com os dados atuais.
- Opcionalmente, adicione um gráfico de barras com a evolução mensal: agrupe transações por mês (formato "YYYY-MM"), calcule receitas e despesas mensais, e plote barras agrupadas.

#### 7. Métodos de atualização e salvamento

- `salvar_dados()`: chama a função de persistência com `self.transacoes`.
- `atualizar_interface()`: chama `atualizar_visao_geral()`, `atualizar_lista_transacoes()`, `atualizar_relatorios()`.
- `ao_mudar_aba()`: apenas chama `atualizar_interface()` para garantir que os dados estejam frescos.

#### 8. Integração com Matplotlib

- No `atualizar_relatorios`, se houver canvas antigo, destrua com `canvas.get_tk_widget().destroy()` e limpe a figura (`plt.close()`).
- Crie nova figura e canvas, empacote no frame.

#### 9. Tratamento de exceções

- Ao carregar dados, retorne lista vazia em caso de arquivo corrompido.
- Ao salvar, capture `IOError` e exiba mensagem com `messagebox` se desejar.

#### 10. Testes e melhorias

- Execute o programa, adicione transações variadas, alterne entre abas, remova itens, feche e reabra para verificar a persistência.
- Verifique se os gráficos atualizam corretamente.
- Ajuste cores, fontes e espaçamentos conforme sua preferência.

### Código completo (esqueleto expandido)

Fornecemos abaixo um esqueleto mais detalhado para orientar a implementação. As partes críticas estão comentadas para você completar.

```python
import customtkinter as ctk
from tkinter import messagebox
import json
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ---------- Persistência ----------
def carregar_dados(caminho="financas.json"):
    if not Path(caminho).exists():
        return []
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def salvar_dados(transacoes, caminho="financas.json"):
    try:
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(transacoes, f, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"Erro ao salvar: {e}")

# ---------- Classe Principal ----------
class DashboardApp:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.janela = ctk.CTk()
        self.janela.title("Dashboard Financeiro")
        self.janela.geometry("800x600")

        self.transacoes = carregar_dados()

        # Tabview
        self.tabview = ctk.CTkTabview(self.janela)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        self.tabview.add("Visão Geral")
        self.tabview.add("Transações")
        self.tabview.add("Relatórios")
        self.tabview.configure(command=self.ao_mudar_aba)

        # Construir abas
        self.criar_aba_visao_geral()
        self.criar_aba_transacoes()
        self.criar_aba_relatorios()

        self.atualizar_interface()

    # ---------- Aba Visão Geral ----------
    def criar_aba_visao_geral(self):
        aba = self.tabview.tab("Visão Geral")
        frame_cartoes = ctk.CTkFrame(aba)
        frame_cartoes.pack(fill="x", padx=20, pady=20)

        # Cartão Saldo
        self.saldo_var = ctk.StringVar(value="R$ 0.00")
        cartao_saldo = ctk.CTkFrame(frame_cartoes, fg_color="#2E7D32", corner_radius=10)
        cartao_saldo.pack(side="left", expand=True, fill="both", padx=10, pady=10)
        ctk.CTkLabel(cartao_saldo, text="Saldo Atual", font=("Arial", 14)).pack(pady=5)
        ctk.CTkLabel(cartao_saldo, textvariable=self.saldo_var, font=("Arial", 24, "bold")).pack(pady=5)

        # Cartão Receitas
        self.receitas_var = ctk.StringVar(value="R$ 0.00")
        cartao_receitas = ctk.CTkFrame(frame_cartoes, fg_color="#1565C0", corner_radius=10)
        cartao_receitas.pack(side="left", expand=True, fill="both", padx=10, pady=10)
        ctk.CTkLabel(cartao_receitas, text="Receitas Totais", font=("Arial", 14)).pack(pady=5)
        ctk.CTkLabel(cartao_receitas, textvariable=self.receitas_var, font=("Arial", 24, "bold")).pack(pady=5)

        # Cartão Despesas
        self.despesas_var = ctk.StringVar(value="R$ 0.00")
        cartao_despesas = ctk.CTkFrame(frame_cartoes, fg_color="#C62828", corner_radius=10)
        cartao_despesas.pack(side="left", expand=True, fill="both", padx=10, pady=10)
        ctk.CTkLabel(cartao_despesas, text="Despesas Totais", font=("Arial", 14)).pack(pady=5)
        ctk.CTkLabel(cartao_despesas, textvariable=self.despesas_var, font=("Arial", 24, "bold")).pack(pady=5)

    def atualizar_visao_geral(self):
        receitas = sum(t['valor'] for t in self.transacoes if t['valor'] > 0)
        despesas = sum(t['valor'] for t in self.transacoes if t['valor'] < 0)
        saldo = receitas + despesas
        self.saldo_var.set(f"R$ {saldo:,.2f}")
        self.receitas_var.set(f"R$ {receitas:,.2f}")
        self.despesas_var.set(f"R$ {abs(despesas):,.2f}")

    # ---------- Aba Transações ----------
    def criar_aba_transacoes(self):
        aba = self.tabview.tab("Transações")
        # Frame de formulário
        form = ctk.CTkFrame(aba)
        form.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(form, text="Descrição:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_desc = ctk.CTkEntry(form, width=200)
        self.entry_desc.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(form, text="Valor (+/-):").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.entry_valor = ctk.CTkEntry(form, width=100)
        self.entry_valor.grid(row=0, column=3, padx=5, pady=5)

        ctk.CTkLabel(form, text="Categoria:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.opcao_categoria = ctk.CTkOptionMenu(form, values=["Alimentação", "Transporte", "Lazer", "Salário", "Outros"])
        self.opcao_categoria.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(form, text="Data (AAAA-MM-DD):").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.entry_data = ctk.CTkEntry(form, width=100)
        self.entry_data.grid(row=1, column=3, padx=5, pady=5)

        ctk.CTkButton(form, text="Adicionar", command=self.adicionar_transacao).grid(row=2, column=0, columnspan=4, pady=10)

        # Área de lista de transações
        self.frame_lista = ctk.CTkScrollableFrame(aba)
        self.frame_lista.pack(fill="both", expand=True, padx=20, pady=10)

    def adicionar_transacao(self):
        desc = self.entry_desc.get().strip()
        valor_str = self.entry_valor.get().strip()
        categoria = self.opcao_categoria.get()
        data_str = self.entry_data.get().strip()

        # Validações
        if not desc:
            messagebox.showwarning("Aviso", "Descrição é obrigatória.")
            return
        try:
            valor = float(valor_str)
        except ValueError:
            messagebox.showwarning("Aviso", "Valor deve ser numérico (use ponto para decimais).")
            return
        if categoria == "":
            messagebox.showwarning("Aviso", "Selecione uma categoria.")
            return
        
        try:
            datetime.strptime(data_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Aviso", "Data inválida. Use AAAA-MM-DD.")
            return

        # Criar transação
        novo_id = max((t['id'] for t in self.transacoes), default=0) + 1
        nova = {
            "id": novo_id,
            "descricao": desc,
            "valor": valor,
            "categoria": categoria,
            "data": data_str
        }
        self.transacoes.append(nova)
        salvar_dados(self.transacoes)
        self.atualizar_interface()
        
        # Limpar campos
        self.entry_desc.delete(0, "end")
        self.entry_valor.delete(0, "end")
        self.entry_data.delete(0, "end")
        messagebox.showinfo("Sucesso", "Transação adicionada.")

    def remover_transacao(self, id_transacao):
        self.transacoes = [t for t in self.transacoes if t['id'] != id_transacao]
        salvar_dados(self.transacoes)
        self.atualizar_interface()

    def atualizar_lista_transacoes(self):
        # Limpar frame lista
        for widget in self.frame_lista.winfo_children():
            widget.destroy()
        # Recriar widgets para cada transação
        for t in self.transacoes:
            frame_item = ctk.CTkFrame(self.frame_lista)
            frame_item.pack(fill="x", padx=5, pady=2)
            ctk.CTkLabel(frame_item, text=f"{t['data']} - {t['descricao']}").pack(side="left", padx=5)
            cor = "green" if t['valor'] >= 0 else "red"
            ctk.CTkLabel(frame_item, text=f"R$ {t['valor']:,.2f}", text_color=cor).pack(side="left", padx=10)
            ctk.CTkLabel(frame_item, text=t['categoria']).pack(side="left", padx=10)
            ctk.CTkButton(frame_item, text="Remover", width=60, command=lambda id=t['id']: self.remover_transacao(id)).pack(side="right", padx=5)

    # ---------- Aba Relatórios ----------
    def criar_aba_relatorios(self):
        aba = self.tabview.tab("Relatórios")
        self.frame_grafico = ctk.CTkFrame(aba)
        self.frame_grafico.pack(fill="both", expand=True, padx=20, pady=20)
        self.canvas_pizza = None

    def atualizar_relatorios(self):
        # Destruir canvas anterior
        if self.canvas_pizza:
            self.canvas_pizza.get_tk_widget().destroy()
            self.canvas_pizza = None
            plt.close('all')

        # Filtrar despesas
        despesas = [t for t in self.transacoes if t['valor'] < 0]
        if not despesas:
            ctk.CTkLabel(self.frame_grafico, text="Nenhuma despesa registrada.").pack()
            return

        categorias = {}
        for t in despesas:
            cat = t['categoria']
            categorias[cat] = categorias.get(cat, 0) + abs(t['valor'])

        fig, ax = plt.subplots(figsize=(4,3), dpi=100)
        ax.pie(categorias.values(), labels=categorias.keys(), autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        ax.set_title("Distribuição de Despesas")

        self.canvas_pizza = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        self.canvas_pizza.draw()
        self.canvas_pizza.get_tk_widget().pack(fill="both", expand=True)

    # ---------- Métodos de atualização geral ----------
    def atualizar_interface(self):
        self.atualizar_visao_geral()
        self.atualizar_lista_transacoes()
        self.atualizar_relatorios()

    def ao_mudar_aba(self):
        self.atualizar_interface()

    def iniciar(self):
        self.janela.mainloop()

if __name__ == "__main__":
    app = DashboardApp()
    app.iniciar()
```

Complete os métodos `adicionar_transacao` e `remover_transacao` conforme os exemplos anteriores. Certifique-se de chamar `salvar_dados` e `atualizar_interface` após modificações.

## Resumo

Neste capítulo, você desenvolveu um Dashboard Financeiro Desktop completo, integrando:

- CustomTkinter: janelas modernas, abas, cartões estilizados.
- Gerenciadores de layout: `pack` e `grid` para organizar os componentes.
- Eventos e variáveis de controle: atualização dinâmica da interface em resposta a ações do usuário e mudanças de aba.
- Persistência de dados: leitura e escrita de arquivo JSON, garantindo que as informações sejam mantidas.
- Validação e tratamento de erros: entradas numéricas, datas, campos obrigatórios.
- Integração com Matplotlib: gráficos de pizza incorporados na interface Tkinter.
- Modularização: separação conceitual em métodos e classes, preparando o terreno para organização em múltiplos arquivos.

O resultado é uma aplicação profissional que pode ser utilizada no dia a dia e serve como base para projetos mais avançados.
