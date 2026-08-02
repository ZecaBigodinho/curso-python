# 02 — Arquitetura do Sistema

## 🎯 Objetivo

Neste capítulo você vai criar a arquitetura do Sistema Escolar — a estrutura de pastas e arquivos que organizará todo o desenvolvimento futuro.

Ao final, você terá:

- Compreendido o padrão MVC simplificado para aplicações desktop
- Criado a estrutura de pastas do projeto: `views/`, `controllers/`, `database/`, `utils/`
- Transformado cada pasta em um pacote Python com `__init__.py`
- Escrito o `main.py` — ponto de entrada que abre uma janela Tkinter centralizada
- Visualizado a janela principal com título "Sistema Escolar", 800x600, não redimensionável

## 📍 Contextualização

No Capítulo 01, você definiu o escopo do Sistema Escolar, levantou 18 requisitos funcionais e formou sua equipe. Foi um capítulo de planejamento puro — essencial, mas sem código.

Agora, o projeto começa a tomar forma. Você vai criar os alicerces sobre os quais todas as telas, lógicas e conexões serão construídas. Assim como uma casa precisa de fundação antes das paredes, um sistema profissional precisa de uma arquitetura sólida antes do primeiro botão.

**Progresso do Sistema:**

```text
✅ Capítulo 01 — Introdução e Planejamento
🔨 Arquitetura do Sistema ← VOCÊ ESTÁ AQUI
⬜ Tela de Login
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

Ao final deste capítulo, você terá uma estrutura de pastas e um arquivo `main.py` que, quando executado, exibe uma janela como esta:

```text
┌─────────────────────────────────────────┐
│  Sistema Escolar                    _ □ X│
│                                         │
│                                         │
│            (janela vazia)               │
│             800 x 600                   │
│         centralizada na tela            │
│                                         │
│                                         │
│                                         │
└─────────────────────────────────────────┘
```

E sua árvore de projeto estará assim:

```text
sistema_escolar/
├── main.py              ← ponto de entrada (funcional)
├── views/               ← telas do sistema
│   └── __init__.py
├── controllers/         ← lógica de negócio
│   └── __init__.py
├── database/            ← conexão e operações
│   └── __init__.py
└── utils/               ← funções auxiliares
    └── __init__.py
```

Parece simples? É simples mesmo — e é exatamente essa simplicidade que permite que sistemas complexos cresçam sem virar uma bagunça.

## 💻 Implementação Guiada

### Passo 1 — Por que não colocar tudo em um único arquivo?

Antes de criar qualquer pasta, entenda o problema que estamos resolvendo.

Imagine que você escreva todas as funcionalidades do sistema em um único arquivo `sistema.py`:

- Código da tela de login
- Código do menu
- Código do cadastro
- Conexão com banco
- Queries SQL
- Tratamento de erros

O que acontece? O arquivo teria centenas (talvez milhares) de linhas. Ficaria difícil de:

- Encontrar um bug
- Adicionar uma nova funcionalidade
- Dividir o trabalho entre a equipe
- Reaproveitar código em outro projeto

A solução: separar responsabilidades em módulos.

!!! note "Conceito Importante"
    Módulo, em Python, é simplesmente um arquivo `.py`. Pacote é uma pasta contendo um arquivo `__init__.py`. Isso permite usar `import`. Não há mágica — é só organização.

### Passo 2 — O padrão MVC para aplicações desktop

MVC significa Model-View-Controller. É um padrão arquitetural que separa o sistema em três camadas:

| Camada | Responsabilidade | No nosso projeto |
|---|---|---|
| **Model** | Dados e regras de negócio | `database/` (conexão, queries) |
| **View** | Tudo que o usuário vê | `views/` (telas, janelas, botões) |
| **Controller** | Ponte entre View e Model | `controllers/` (autenticação, lógica de aluno) |

Acrescentamos uma quarta camada auxiliar:

| **Utils** | Funções genéricas reutilizáveis | `utils/` (centralizar janela, validar campos) |

O `main.py` fica fora das camadas. Ele é o ponto de entrada — o arquivo que você executa para iniciar o sistema.

```text
┌─────────────────────────────────────────┐
│                main.py                  │
│          (ponto de entrada)             │
└──────────────────┬──────────────────────┘
                   │
      ┌────────────┼────────────┐
      ▼            ▼            ▼
┌──────────┐ ┌───────────┐ ┌──────────┐
│  views/  │ │controllers│ │database/ │
│ (telas)  │ │ (lógica)  │ │ (dados)  │
└──────────┘ └───────────┘ └──────────┘
```

No nosso caso, o `main.py` criará a janela principal e, futuramente, orquestrará a transição entre telas. As views cuidarão de cada tela específica. Os controllers processarão os dados. O database fará a persistência.

### Passo 3 — Criando a estrutura de pastas

Agora, mãos à obra. Crie uma pasta chamada `sistema_escolar` no seu computador. Dentro dela, crie as subpastas conforme o comando abaixo.

Abra o terminal na pasta `sistema_escolar` e execute:

```bash
# No Windows (PowerShell) ou Linux/macOS
mkdir views controllers database utils
```

Ou, se preferir, crie as pastas manualmente pelo explorador de arquivos ou pelo VS Code (clique com botão direito → Nova Pasta).

Sua estrutura agora está assim:

```text
sistema_escolar/
├── views/           (vazia)
├── controllers/     (vazia)
├── database/        (vazia)
└── utils/           (vazia)
```

### Passo 4 — Transformando pastas em pacotes Python

Para que o Python reconheça essas pastas como pacotes importáveis, cada uma precisa de um arquivo especial chamado `__init__.py`.

Esse arquivo pode estar completamente vazio. Sua presença é o que diz ao Python: "Esta pasta é um pacote, você pode importar módulos daqui".

Crie manualmente um arquivo `__init__.py` vazio dentro de cada pasta:

```text
sistema_escolar/
├── views/
│   └── __init__.py       ← arquivo vazio
├── controllers/
│   └── __init__.py       ← arquivo vazio
├── database/
│   └── __init__.py       ← arquivo vazio
└── utils/
    └── __init__.py       ← arquivo vazio
```

!!! tip "Dica Profissional"
    No VS Code, você pode criar um arquivo diretamente: clique com botão direito na pasta → New File → digite `__init__.py`. O atalho de teclado Ctrl+N também funciona — só lembre de salvar dentro da pasta correta.

Agora seu projeto já é um pacote Python corretamente estruturado. Falta o arquivo principal.

### Passo 5 — Criando o main.py

O `main.py` é o coração do sistema — é o arquivo que você executará para iniciar tudo.

Crie o arquivo `main.py` na raiz do projeto (`sistema_escolar/main.py`) e adicione o código abaixo.

```python
# ======================================================================
# main.py — Ponto de Entrada do Sistema Escolar
# ======================================================================
# Eu sou o ponto de entrada do Sistema Escolar.
# Tudo começa aqui. Quando você me executa, eu:
#   1. Crio a janela principal
#   2. Configuro o título e o tamanho
#   3. Centralizo a janela na tela do usuário
#   4. Entro no loop principal de eventos
#
# Nos próximos capítulos, eu serei responsável por orquestrar
# a transição entre as telas (Login → Menu → Cadastro).
# ======================================================================

import tkinter as tk


# ---------- FUNÇÃO AUXILIAR ----------
def centralizar_janela(janela, largura, altura):
    """
    Eu centralizo a janela na tela do usuário.
    
    Calculo a posição X e Y com base na resolução do monitor
    para que a janela apareça exatamente no centro.
    
    Parâmetros:
        janela: a instância de tk.Tk() ou tk.Toplevel()
        largura: largura desejada da janela (ex: 800)
        altura: altura desejada da janela (ex: 600)
    """
    # Eu obtenho a resolução da tela.
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()

    # Eu calculo a posição X e Y para centralizar.
    pos_x = (largura_tela // 2) - (largura // 2)
    pos_y = (altura_tela // 2) - (altura // 2)

    # Eu aplico a geometria: "LARGURAxALTURA+X+Y".
    janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")


# ---------- JANELA PRINCIPAL ----------
# Eu crio a janela principal do sistema.
# Toda aplicação Tkinter começa com uma instância de Tk().
janela = tk.Tk()

# Eu defino o título que aparece na barra superior da janela.
# É a identidade visual do sistema.
janela.title("Sistema Escolar")

# Eu chamo a função que centraliza a janela.
# Passei 800x600 como tamanho inicial.
centralizar_janela(janela, 800, 600)

# Eu impeço que o usuário redimensione a janela.
# Isso garante que o layout das telas futuras não quebre.
janela.resizable(False, False)

# ---------- LOOP PRINCIPAL ----------
# Eu inicio o loop principal de eventos.
# A partir daqui, o Tkinter fica "escutando" cliques, teclas, etc.
# Tudo o que acontece no sistema passa por este loop.
janela.mainloop()
```

!!! note "Observação sobre os comentários"
    Repare que os comentários não repetem a sintaxe do Python. Eles explicam a intenção por trás de cada linha. É assim que um código profissional deve ser documentado.

### Passo 6 — Executando o sistema

Abra o terminal, navegue até a pasta `sistema_escolar` e execute:

```bash
python main.py
```

**Resultado esperado:**

- Uma janela se abre centralizada na tela
- Título: "Sistema Escolar"
- Tamanho fixo: 800x600
- A janela não pode ser redimensionada
- O interior está vazio (ainda!)

```text
┌─────────────────────────────────────────┐
│  Sistema Escolar                    _ □ X│
├─────────────────────────────────────────┤
│                                         │
│                                         │
│            (janela vazia)               │
│             800 x 600                   │
│         centralizada na tela            │
│                                         │
│                                         │
│                                         │
└─────────────────────────────────────────┘
```

Parabéns! O esqueleto do Sistema Escolar está vivo.

## 📝 Exercício

**Tempo estimado:** 15-20 minutos

**Tarefa:** Reforce seu entendimento sobre centralização de janelas.

1. Modifique o `main.py` para abrir uma janela de 600x400 em vez de 800x600.
2. Altere o título para "Minha Primeira Janela".
3. Teste se a centralização funciona corretamente.
4. Agora, crie uma segunda janela (sem apagar a primeira) usando `tk.Toplevel()`, com título "Janela Secundária", tamanho 300x200, também centralizada e não redimensionável.

Dica: `tk.Toplevel()` é como `tk.Tk()`, mas para janelas filhas. A função `centralizar_janela` funciona com ambas.

??? hint "Dica"
    Você já tem a função `centralizar_janela(janela, largura, altura)`. Use-a para centralizar a nova janela também. E para Toplevel, `resizable(False, False)` funciona da mesma forma.

??? success "Solução"
    ```python
    import tkinter as tk

    def centralizar_janela(janela, largura, altura):
        largura_tela = janela.winfo_screenwidth()
        altura_tela = janela.winfo_screenheight()
        pos_x = (largura_tela // 2) - (largura // 2)
        pos_y = (altura_tela // 2) - (altura // 2)
        janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

    # Janela principal
    janela = tk.Tk()
    janela.title("Minha Primeira Janela")
    centralizar_janela(janela, 600, 400)
    janela.resizable(False, False)

    # Janela secundária
    janela2 = tk.Toplevel()
    janela2.title("Janela Secundária")
    centralizar_janela(janela2, 300, 200)
    janela2.resizable(False, False)

    janela.mainloop()
    ```

Execute e veja as duas janelas centralizadas.

## 🏆 Missão da Equipe

**Tempo estimado:** 30-45 minutos

**Tarefa:** Criem a mesma estrutura de arquitetura para o projeto da equipe de vocês.

**Entregável:** A estrutura de pastas criada e o `main.py` funcional com:

- Janela com o título do projeto da equipe (ex: "Biblioteca Fácil", "Controle de Estoque", etc.)
- Tamanho 800x600 centralizado
- Não redimensionável
- Função `centralizar_janela` incluída

**Checklist da Missão:**

- [ ] Pasta do projeto criada com o nome do sistema da equipe
- [ ] Subpastas `views/`, `controllers/`, `database/`, `utils/` criadas
- [ ] Arquivos `__init__.py` em cada subpasta
- [ ] `main.py` funcional com a janela principal
- [ ] Título da janela corresponde ao nome do projeto da equipe
- [ ] Janela centralizada e não redimensionável
- [ ] Todos os integrantes conseguem executar o `main.py` em suas máquinas
- [ ] Professor validou a estrutura

!!! important "Nota para o Professor"
    Verifique: Cada equipe deve ter a estrutura de pastas idêntica à do Sistema Escolar. O único arquivo com código deve ser o `main.py`. Os `__init__.py` devem existir (mesmo vazios). Execute o `main.py` de cada equipe para confirmar que a janela abre com o título correto.

## ⚡ Desafio

**Vá além:** Crie um script que gere automaticamente a estrutura de pastas.

Crie um arquivo chamado `criar_estrutura.py` (fora do projeto) que, quando executado, cria todas as pastas e arquivos `__init__.py` automaticamente. Use `os.makedirs()` e `pathlib.Path`.

```python
import os
from pathlib import Path

# Nome do projeto (pode ser alterado conforme a equipe)
nome_projeto = "meu_sistema"

# Pastas a serem criadas
pastas = ["views", "controllers", "database", "utils"]

# Criar a pasta raiz
Path(nome_projeto).mkdir(exist_ok=True)

# Criar as subpastas e os __init__.py
for pasta in pastas:
    caminho = Path(nome_projeto) / pasta
    caminho.mkdir(exist_ok=True)
    # Criar arquivo __init__.py vazio
    (caminho / "__init__.py").touch()

print(f"Estrutura do projeto '{nome_projeto}' criada com sucesso!")
```

Isso economiza tempo e evita erros de digitação ao criar muitos arquivos.

## ⚠️ Erros Comuns

!!! danger "Esquecer o __init__.py"
    **Sintoma:** Ao tentar importar um módulo de dentro de `views/`, o Python lança `ModuleNotFoundError: No module named 'views'`.
    
    **Causa:** A pasta não contém o arquivo `__init__.py`, então o Python não a reconhece como pacote.
    
    **Solução:** Verifique se cada subpasta (`views`, `controllers`, `database`, `utils`) possui um arquivo `__init__.py` — mesmo que vazio.

!!! warning "Colocar main.py dentro de uma subpasta"
    **Sintoma:** Ao executar, o terminal diz `python: can't open file 'main.py'`.
    
    **Causa:** O arquivo `main.py` foi criado dentro de `views/` ou outra subpasta, e não na raiz do projeto.
    
    **Solução:** O `main.py` deve ficar na raiz do projeto, ao lado das pastas `views`, `controllers`, etc. Ele é o ponto de entrada.

!!! warning "Não usar if __name__ == '__main__': ainda"
    **Sintoma:** Não é exatamente um erro, mas cria complexidade desnecessária neste momento.
    
    **Causa:** Alunos que já conhecem a boa prática tentam aplicá-la precocemente.
    
    **Solução:** Neste capítulo, mantenha o código simples. O `main.py` só será importado por outros módulos em capítulos avançados. Por enquanto, `janela.mainloop()` direto funciona perfeitamente.

!!! danger "Hardcodar o caminho do Python"
    **Sintoma:** No terminal, o comando `python main.py` não funciona, mas `python3 main.py` ou `py main.py` funciona.
    
    **Causa:** Diferentes sistemas operacionais e instalações do Python.
    
    **Solução:** Use o comando que funciona na sua máquina. No Windows, geralmente é `python`. No Linux/macOS, pode ser `python3`. O importante é que o arquivo execute.

## 💡 Boas Práticas

**1. Estrutura de pacotes desde o primeiro dia**

No mercado, todo projeto começa com a definição da arquitetura. Ninguém espera o código crescer para depois organizar. Criar as pastas e `__init__.py` desde o início é um hábito profissional.

**2. main.py como orquestrador**

O `main.py` não deve conter lógica de negócio, queries SQL ou criação de widgets complexos. Ele é o orquestrador — cria a janela principal e delega o resto para os módulos. Mantenha-o enxuto.

**3. Nomes de pastas no plural**

É uma convenção comum em Python: `views` (não view), `controllers`, `models`, `utils`. Facilita a leitura e sinaliza que a pasta contém múltiplos módulos relacionados.

**4. Comentários que explicam a intenção**

Repare nos comentários do `main.py`. Eles não dizem "importa o tkinter" — isso é óbvio pela sintaxe. Eles dizem "Eu sou o ponto de entrada". Comentários devem explicar por que, não o que.

**5. Centralização como função reutilizável**

Colocamos `centralizar_janela` como uma função separada, não como código solto. Isso permite reutilizá-la em qualquer janela (Login, Menu, Cadastro) sem repetir código. No futuro, podemos movê-la para `utils/helpers.py`.

## ☑️ Checklist

Antes de prosseguir para o próximo capítulo, confirme:

- [ ] A pasta `sistema_escolar` existe e contém as subpastas `views`, `controllers`, `database`, `utils`
- [ ] Cada subpasta possui um arquivo `__init__.py` (mesmo que vazio)
- [ ] O arquivo `main.py` está na raiz do projeto
- [ ] O `main.py` abre uma janela com título "Sistema Escolar"
- [ ] A janela tem tamanho 800x600 e aparece centralizada
- [ ] A janela não pode ser redimensionada
- [ ] Executei `python main.py` e vi a janela abrir sem erros
- [ ] Entendi o papel de cada camada (View, Controller, Model, Utils)
- [ ] Minha equipe criou a mesma estrutura para o projeto dela
- [ ] O `main.py` da equipe abre com o título do projeto deles

## ➡️ Próximo Capítulo

No **Capítulo 03 — Tela de Login**, você construirá a primeira tela funcional do sistema: o formulário de autenticação.

Aprenderá a criar uma nova janela com campos de usuário e senha, validar credenciais contra um dicionário (que depois será substituído pelo banco de dados) e fazer a transição para o Menu Principal após login bem-sucedido.

Prepare-se: revise a criação de widgets (Entry, Label, Button), o gerenciador `grid` e o uso de `messagebox` para exibir mensagens de erro. Tudo isso será colocado em prática.

A arquitetura que você criou hoje é a fundação. A partir de agora, cada tijolo que colocarmos tornará o sistema mais completo. 🧱
