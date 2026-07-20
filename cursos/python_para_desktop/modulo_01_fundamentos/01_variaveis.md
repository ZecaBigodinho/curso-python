# 01. Variáveis

## Objetivos
Ao concluir este capítulo, você será capaz de:
- Compreender o conceito de variável como um espaço de armazenamento nomeado na memória.
- Declarar e atribuir valores a variáveis em Python.
- Reconhecer e utilizar os tipos de dados básicos: inteiro (int), ponto flutuante (float), texto (str) e booleano (bool).
- Aplicar as convenções de nomenclatura recomendadas pela comunidade Python (PEP 8).
- Realizar conversões entre tipos de dados.
- Construir programas que interajam com o usuário, armazenando informações em variáveis.

## Pré-requisitos
Nenhum conhecimento prévio de programação é exigido. Basta ter o Python instalado em seu computador e um editor de código ou ambiente de desenvolvimento (como IDLE, Thonny, VS Code ou PyCharm). É recomendável que você já tenha executado seu primeiro `print("Olá, mundo!")` e esteja confortável com a interface básica do interpretador Python.

## Motivação
Imagine que você está construindo uma aplicação de desktop para calcular o orçamento de uma obra. Você precisa guardar o valor do metro quadrado, a área total, o custo dos materiais e o nome do cliente. Sem variáveis, você teria que escrever esses valores diretamente no código e modificá-los manualmente a cada novo cálculo. Pior: o programa seria incapaz de responder a perguntas como “Qual é o nome do cliente?” ou “Qual o valor total com desconto?”.

Variáveis são o coração de qualquer programa. Elas permitem que seu código lembre de informações, transforme dados e reaja de forma dinâmica. Sem variáveis, os programas seriam estáticos e praticamente inúteis. Neste capítulo, vamos dominar os fundamentos que tornarão você capaz de armazenar e manipular qualquer tipo de informação em Python.

## Conteúdo

### O que é uma variável?
Pense em uma variável como uma caixa etiquetada onde você pode guardar um valor. A etiqueta é o nome da variável; o conteúdo da caixa é o valor armazenado. Em Python, você cria essa caixa e coloca algo dentro com o sinal de igual (`=`), que chamamos de operador de atribuição.

```python
nome = "Maria"
idade = 30
altura = 1.68
estudante = True
```

Aqui, `nome` é uma variável que guarda o texto `"Maria"`, `idade` guarda o número `30`, `altura` o número `1.68` e `estudante` o valor booleano `True`.

!!! note "Variável é uma referência a um objeto"
    Em Python, a variável não “contém” o valor diretamente; ela aponta para um objeto na memória. Quando você escreve `x = 5`, Python cria um objeto `int` com valor `5` e associa o nome `x` a esse objeto. Essa distinção será importante mais adiante, mas por ora, a metáfora da caixa etiquetada é perfeitamente adequada.

### Declaração e atribuição
Em Python, você não precisa declarar o tipo da variável explicitamente. A linguagem é dinamicamente tipada: o tipo é determinado automaticamente no momento em que o valor é atribuído. Você pode, inclusive, reatribuir uma variável com um valor de tipo diferente a qualquer momento:

```python
dado = 100       # dado é um int
dado = "cem"     # agora dado é uma str
dado = 3.14      # agora dado é um float
```

Essa flexibilidade é poderosa, mas exige cuidado para não gerar confusão. Por isso, é uma boa prática manter o tipo de uma variável consistente ao longo do programa.

### Tipos de dados básicos
Python oferece vários tipos embutidos. Vamos focar nos quatro que constituem a base de quase todo programa:

#### 1. Inteiros (int)
Representam números sem casas decimais, positivos, negativos ou zero.

```python
quantidade = 15
saldo = -200
ano = 2025
```

Você pode realizar operações aritméticas com eles: soma (`+`), subtração (`-`), multiplicação (`*`), divisão (`/`), divisão inteira (`//`), resto da divisão (`%`) e exponenciação (`**`).

#### 2. Ponto flutuante (float)
Representam números com casas decimais. São utilizados para medidas, valores monetários e cálculos científicos.

```python
preco = 19.99
temperatura = -3.5
pi = 3.14159
```

Internamente, seguem o padrão IEEE 754, o que significa que algumas operações podem gerar pequenas imprecisões. Para valores monetários, recomenda-se o uso do tipo `Decimal` (do módulo decimal) em aplicações sérias; porém, para aprendizado inicial, `float` é suficiente.

!!! warning "Cuidado com a precisão"
    Execute `0.1 + 0.2` no interpretador. O resultado não será exatamente `0.3`, e sim `0.30000000000000004`. Isso não é um erro do Python, mas uma limitação da representação binária de números decimais. Em aplicações de desktop comuns, arredondar o resultado resolve. Mas esteja ciente dessa característica.

#### 3. Cadeia de caracteres (str)
Strings são sequências de caracteres delimitadas por aspas simples (`'...'`) ou duplas (`"..."`). Use três aspas (`'''...'''` ou `"""..."""`) para textos multilinha.

```python
saudacao = "Olá, mundo!"
mensagem = 'Python é incrível'
paragrafo = """Esta é uma string
que ocupa várias linhas."""
```

Strings podem ser concatenadas com `+` e repetidas com `*`. O operador `in` verifica se uma substring está presente.

```python
nome_completo = "Ana" + " " + "Silva"  # "Ana Silva"
linha = "-" * 40                        # "----------------------------------------"
print("Silva" in nome_completo)         # True
```

#### 4. Booleanos (bool)
Armazenam apenas dois valores: `True` (verdadeiro) ou `False` (falso). São fundamentais em estruturas condicionais e laços.

```python
ligado = True
finalizado = False
```

Os valores booleanos resultam frequentemente de comparações:

```python
maior = 10 > 5          # True
igual = 7 == 3          # False
diferente = 7 != 3      # True
```

!!! note "Valores considerados falsos"
    Em contextos booleanos, além de `False`, os seguintes valores são tratados como falso: `None`, zero (`0`, `0.0`), strings vazias (`''`), listas vazias (`[]`), dicionários vazios (`{}`), entre outros. Esse comportamento é útil em condições como `if nome:`.

### Verificando o tipo de uma variável
Para saber qual o tipo de uma variável, use a função `type()`:

```python
x = 42
print(type(x))   # <class 'int'>
```

Isso ajuda a depurar o código e a entender o comportamento das operações.

### Conversão entre tipos (casting)
Muitas vezes, precisamos transformar um tipo de dado em outro. Python oferece funções integradas para isso:

| Função | Descrição | Exemplo |
|---|---|---|
| `int()` | Converte para inteiro | `int("10")` → `10` |
| `float()` | Converte para float | `float("3.14")` → `3.14` |
| `str()` | Converte para string | `str(25)` → `"25"` |
| `bool()` | Converte para booleano | `bool(0)` → `False` |

Atenção: nem toda string pode ser convertida para número; `int("abc")` gera um erro. Da mesma forma, a conversão de float para int trunca a parte decimal, sem arredondar:

```python
print(int(7.9))  # 7
```

!!! tip "Entrada de usuário é sempre string"
    A função `input()` retorna uma string, mesmo que o usuário digite um número. Para trabalhar com valores numéricos, é obrigatório usar `int()` ou `float()` para converter a entrada.

### Convenções de nomenclatura (PEP 8)
A comunidade Python adota um guia de estilo chamado PEP 8. Seguir essas convenções torna seu código mais legível e profissional. Regras fundamentais para nomes de variáveis:

- Use apenas letras minúsculas, números e sublinhados (`_`).
- Não comece o nome com um número.
- Prefira nomes descritivos: `nome_cliente` em vez de `nc`.
- Separe palavras com sublinhados (snake_case): `valor_total`, `idade_maxima`.
- Evite acentos e caracteres especiais, embora Python permita, pois podem causar problemas de compatibilidade.
- Não utilize palavras reservadas da linguagem (`if`, `for`, `while`, `class`, `import`, etc.).
- Nomes são sensíveis a maiúsculas e minúsculas: `idade` e `Idade` são variáveis diferentes.

!!! warning "Palavras reservadas não podem ser usadas"
    Tentar criar uma variável chamada `if` ou `class` resultará em erro de sintaxe. Consulte a lista de palavras reservadas com `import keyword; print(keyword.kwlist)`.

Exemplos de bons nomes:

```python
velocidade_maxima = 120
contador_de_tentativas = 0
nome_do_arquivo = "dados.csv"
```

### Atualizando variáveis
O valor de uma variável pode ser modificado ao longo do programa, inclusive com base no valor anterior:

```python
contador = 0
contador = contador + 1   # contador agora é 1
contador += 1             # forma abreviada, contador agora é 2
```

Python suporta operadores de atribuição combinados: `+=`, `-=`, `*=`, `/=`, entre outros.

### Escopo e tempo de vida (noções iniciais)
Por enquanto, suas variáveis existirão dentro do programa principal. Ao final da execução, os valores são perdidos (a menos que você os salve em arquivo, tema de capítulos futuros). É importante saber que uma variável só é acessível depois de ter recebido um valor; usar uma variável não inicializada gera um `NameError`.

## Exemplos

??? example "Exemplo 1: Criando variáveis de diferentes tipos"
    === "Código"
        ```python
        # Criação de variáveis com tipos distintos
        produto = "Notebook"
        preco_unitario = 3500.00
        quantidade = 3
        disponivel = True

        # Exibindo os valores e seus tipos
        print("Produto:", produto, "| Tipo:", type(produto))
        print("Preço unitário:", preco_unitario, "| Tipo:", type(preco_unitario))
        print("Quantidade:", quantidade, "| Tipo:", type(quantidade))
        print("Disponível:", disponivel, "| Tipo:", type(disponivel))
        ```

    === "Resultado"
        ```text
        Produto: Notebook | Tipo: <class 'str'>
        Preço unitário: 3500.0 | Tipo: <class 'float'>
        Quantidade: 3 | Tipo: <class 'int'>
        Disponível: True | Tipo: <class 'bool'>
        ```

    === "Explicação"
        Demonstra a criação de variáveis de cada um dos quatro tipos básicos e o uso da função `type()` para inspeção. Note que o número `3500.00` é automaticamente reconhecido como float, e a vírgula não deve ser usada em literais numéricos.

??? example "Exemplo 2: Nomes válidos e inválidos"
    === "Código"
        ```python
        # Nomes válidos (seguindo convenções)
        nome_completo = "João da Silva"
        idade_anos = 25
        _contador = 10          # sublinhado no início é permitido

        # Nomes inválidos (descomente para testar)
        # 1numero = 5           # não pode começar com número
        # nome@cliente = "Ana"  # caractere especial não permitido
        # class = "Python"      # palavra reservada

        print(nome_completo, idade_anos, _contador)
        ```

    === "Resultado"
        ```text
        João da Silva 25 10
        ```

    === "Explicação"
        As primeiras três linhas mostram nomes perfeitamente aceitáveis. Os comentários lembram regras de restrição. Python não permite criar variáveis cujo nome comece com dígito, contenha caracteres especiais ou conflite com palavras reservadas.

??? example "Exemplo 3: Conversão de tipos e cálculo com entrada do usuário"
    === "Código"
        ```python
        # Cálculo do valor total de uma venda
        produto = input("Nome do produto: ")
        preco_str = input("Preço unitário: R$ ")
        qtde_str = input("Quantidade: ")

        # Converte as strings para float e int
        preco = float(preco_str)
        qtde = int(qtde_str)

        total = preco * qtde

        # Exibe o resultado formatado
        print(f"Total para {qtde} unidade(s) de {produto}: R$ {total:.2f}")
        ```

    === "Resultado"
        Suponha que o usuário digite "Mouse", "49.90" e "2":
        ```text
        Nome do produto: Mouse
        Preço unitário: R$ 49.90
        Quantidade: 2
        Total para 2 unidade(s) de Mouse: R$ 99.80
        ```

    === "Explicação"
        Um exemplo prático de como variáveis intermediam a entrada, o processamento e a saída. A conversão de str para float e int é indispensável, pois `input()` sempre retorna texto. O f-string permite formatar o resultado com duas casas decimais.

## Exercícios

### Básico (fixação)
- Crie uma variável chamada `cidade` e atribua a ela o nome da cidade onde você nasceu. Crie outra variável `ano_atual` com o ano corrente. Exiba uma frase no formato: `"Eu nasci em {cidade} e estamos em {ano_atual}."`.
- Armazene os valores `10`, `20` e `30` em três variáveis distintas, `a`, `b` e `c`. Calcule a média aritmética e armazene em `media`. Exiba o resultado.
- Verifique e anote o tipo de cada uma das seguintes expressões usando `type()`: `5`, `5.0`, `"5"`, `5 > 3`, `"python"[0]`.

### Intermediário (aplicação)
Você está desenvolvendo um conversor de moedas simples. Sabendo que 1 dólar equivale a R$ 5,47 (cotação fictícia), escreva um programa que:
- Pergunte ao usuário quantos dólares ele deseja comprar.
- Armazene o valor em uma variável `dolares` (convertendo para `float`).
- Calcule o valor em reais e armazene em `reais`.
- Exiba o resultado com duas casas decimais.
- Adicionalmente, aplique um desconto de 2% se a compra for acima de 100 dólares, e exiba o novo valor.

### Avançado (desafio)
Crie um programa que simule o cadastro de um currículo básico. Ele deve solicitar ao usuário: nome, idade, altura (em metros) e se possui experiência profissional (`True`/`False`). Em seguida, exiba uma ficha resumo onde:
- A idade deve ser exibida como inteiro, mas convertida para string para concatenar com “anos”.
- A altura deve ser exibida com uma casa decimal.
- A experiência deve ser exibida como “Sim” ou “Não”.
- Calcule também o ano de nascimento aproximado (subtraia a idade do ano atual) e inclua essa informação.

Utilize variáveis com nomes significativos, conversões de tipo e f-strings para formatar a saída.

## Projeto Prático: Calculadora de IMC (Índice de Massa Corporal)
Desenvolva um programa de console que calcula o IMC de uma pessoa, seguindo estas etapas:
- Solicitar o nome do usuário.
- Solicitar o peso (em quilogramas) e a altura (em metros).
- Calcular o IMC pela fórmula: `imc = peso / (altura ** 2)`.
- Exibir o resultado formatado: `"Nome, seu IMC é XX.X. Classificação: YY"`.
- A classificação segue a tabela:
    - Abaixo de 18.5: "Abaixo do peso"
    - Entre 18.5 e 24.9: "Peso normal"
    - Entre 25.0 e 29.9: "Sobrepeso"
    - Acima de 30.0: "Obesidade"

**Diretrizes:**
- Utilize variáveis para armazenar nome, peso, altura e IMC.
- Converta as entradas para `float` (peso e altura).
- Use uma estrutura condicional (`if`/`elif`/`else`) para determinar a classificação.
- Mantenha o código dentro de uma função `main()` (opcional) e execute-a.
- Comente seu código explicando cada etapa.

**Exemplo de execução:**
```text
Nome: Ana
Peso (kg): 68
Altura (m): 1.65
Ana, seu IMC é 24.98. Classificação: Peso normal
```

Esse projeto integra declaração de variáveis, tipos de dados, conversão, entrada de usuário e lógica condicional, solidificando os conceitos fundamentais deste capítulo.

## Resumo
Neste capítulo, você construiu a base de toda a programação em Python:
- Variáveis são nomes que fazem referência a valores armazenados na memória.
- A atribuição é feita com `=`, e Python infere o tipo dinamicamente.
- Os quatro tipos de dados básicos são `int`, `float`, `str` e `bool`, cada um com operações características.
- Nomes de variáveis devem seguir o padrão snake_case, ser descritivos e evitar palavras reservadas.
- A função `type()` revela o tipo de uma variável; funções como `int()`, `float()`, `str()` e `bool()` convertem entre tipos.
- Entradas do usuário sempre vêm como string e precisam ser convertidas quando se espera números.
- Variáveis podem ser atualizadas e usadas em expressões aritméticas e lógicas.

Dominar variáveis é o primeiro passo para construir aplicações reais. Você agora é capaz de armazenar, transformar e exibir informações — e está pronto para combiná-las com operadores e estruturas de controle.
