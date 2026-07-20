# 02. Operadores

## Objetivos
Neste capítulo, você aprenderá a:
- Empregar os operadores aritméticos para realizar cálculos matemáticos.
- Utilizar os operadores de comparação para testar relações entre valores.
- Aplicar os operadores lógicos para construir condições compostas.
- Dominar os operadores de atribuição simples e combinados.
- Compreender a precedência de operadores e como controlá-la com parênteses.
- Resolver problemas do mundo real combinando diferentes categorias de operadores.

## Pré-requisitos
Antes de prosseguir, você deve:
- Compreender o conceito de variáveis e saber declarar variáveis em Python.
- Conhecer os tipos de dados básicos: int, float, str e bool.
- Ter familiaridade com a função `print()` para exibir resultados.
- Saber utilizar a função `input()` para receber dados do usuário.

Se precisar revisar esses tópicos, consulte o capítulo anterior sobre Variáveis.

## Motivação
Você está construindo uma aplicação de desktop para um pequeno comércio. O programa precisa calcular descontos, verificar se um cliente atinge o valor mínimo para frete grátis, somar itens de um pedido e atualizar o estoque. Todas essas operações — somar, comparar, decidir — dependem de operadores.

Os operadores são os tijolos com os quais erguemos a lógica do programa. Sem eles, seu código seria apenas um amontoado de dados inertes. Com eles, seus programas ganham vida: tomam decisões, transformam números e produzem resultados úteis.

Ao final deste capítulo, você será capaz de escrever expressões que realizam desde simples cálculos até verificações complexas, preparando o terreno para as estruturas de controle que virão a seguir.

## Conteúdo

### Operadores aritméticos
Operadores aritméticos permitem realizar as operações matemáticas básicas. Python oferece os seguintes:

| Operador | Operação | Exemplo | Resultado |
|---|---|---|---|
| `+` | Adição | `5 + 3` | `8` |
| `-` | Subtração | `10 - 4` | `6` |
| `*` | Multiplicação | `7 * 2` | `14` |
| `/` | Divisão | `9 / 2` | `4.5` |
| `//` | Divisão inteira | `9 // 2` | `4` |
| `%` | Módulo (resto) | `9 % 2` | `1` |
| `**` | Exponenciação | `3 ** 3` | `27` |

!!! note "Divisão sempre retorna float"
    Em Python, mesmo que a divisão seja exata, o operador `/` produz um `float`. Use `//` para obter um quociente inteiro (truncado). O operador `%` é extremamente útil para saber se um número é par (`num % 2 == 0`) ou para ciclos periódicos.

```python
# Exemplos de operadores aritméticos
a = 15
b = 6

print("Adição:", a + b)            # 21
print("Subtração:", a - b)         # 9
print("Multiplicação:", a * b)     # 90
print("Divisão:", a / b)           # 2.5
print("Divisão inteira:", a // b)  # 2
print("Resto:", a % b)             # 3
print("Exponenciação:", a ** 2)    # 225
```

### Operadores de comparação (relacionais)
Comparações são a base para a tomada de decisões. Elas retornam um valor booleano (`True` ou `False`).

| Operador | Significado | Exemplo | Resultado |
|---|---|---|---|
| `==` | Igual a | `5 == 5` | `True` |
| `!=` | Diferente de | `5 != 5` | `False` |
| `>` | Maior que | `10 > 7` | `True` |
| `<` | Menor que | `3 < 1` | `False` |
| `>=` | Maior ou igual a | `8 >= 8` | `True` |
| `<=` | Menor ou igual a | `6 <= 4` | `False` |

!!! warning "Igualdade usa dois iguais"
    Um erro comum entre iniciantes é confundir `=` (atribuição) com `==` (comparação). `a = 5` atribui o valor 5 à variável `a`. `a == 5` pergunta se `a` é igual a 5.

```python
# Exemplos de comparação
idade = 18
print(idade >= 18)   # True (maior ou igual)
print(idade == 21)   # False
print(idade != 20)   # True
```

### Operadores lógicos
Os operadores lógicos permitem combinar múltiplas condições. Python oferece três: `and`, `or` e `not`.
- `and` (e): Retorna `True` se todas as condições forem verdadeiras.
- `or` (ou): Retorna `True` se pelo menos uma condição for verdadeira.
- `not` (não): Inverte o valor booleano.

| Operador | Exemplo | Resultado |
|---|---|---|
| `and` | `(5 > 3) and (4 < 6)` | `True` |
| `or` | `(5 > 10) or (3 == 3)` | `True` |
| `not` | `not (2 == 2)` | `False` |

```python
# Exemplos de operadores lógicos
tem_carteira = True
idade = 17

# Pode dirigir se tiver carteira E idade >= 18
pode_dirigir = tem_carteira and idade >= 18
print(pode_dirigir)  # False

# Entrada gratuita para menores de 12 OU maiores de 65
entrada_gratuita = idade < 12 or idade > 65
print(entrada_gratuita)  # False

# Acesso negado se NÃO for maior de idade
acesso = not (idade < 18)
print(acesso)  # False
```

!!! tip "Curto-circuito na avaliação"
    Python avalia expressões lógicas da esquerda para a direita e para assim que o resultado é determinado. Por exemplo, em `False and qualquer_coisa`, a segunda parte nunca é avaliada. Isso pode ser usado para evitar erros: `if x != 0 and 10 / x > 2`.

### Operadores de atribuição
O operador de atribuição mais básico é o `=`, que guarda um valor em uma variável. Python também oferece operadores de atribuição combinados, que realizam uma operação e atribuem o resultado de uma só vez.

| Operador | Significado | Equivalente a |
|---|---|---|
| `=` | Atribuição simples | `x = 5` |
| `+=` | Soma e atribui | `x = x + 3` |
| `-=` | Subtrai e atribui | `x = x - 3` |
| `*=` | Multiplica e atribui | `x = x * 3` |
| `/=` | Divide e atribui | `x = x / 3` |
| `//=` | Divide (int) e atribui | `x = x // 3` |
| `%=` | Módulo e atribui | `x = x % 3` |
| `**=` | Exponencia e atribui | `x = x ** 3` |

```python
# Exemplos de atribuição combinada
saldo = 1000
saldo += 200      # saldo agora é 1200 (depósito)
saldo -= 150      # saldo agora é 1050 (saque)
saldo *= 1.05     # saldo recebe 5% de juros (1050 * 1.05)
print(f"Saldo final: R$ {saldo:.2f}")  # 1102.50
```

### Precedência de operadores
Quando uma expressão combina vários operadores, Python segue uma ordem fixa de avaliação, chamada precedência. Da maior para a menor prioridade:
1. Parênteses `()`
2. Exponenciação `**`
3. Multiplicação, divisão, divisão inteira e módulo `*`, `/`, `//`, `%`
4. Adição e subtração `+`, `-`
5. Operadores de comparação `==`, `!=`, `>`, `<`, `>=`, `<=`
6. Operadores lógicos: `not`, depois `and`, depois `or`
7. Atribuição `=`, `+=`, etc.

!!! note "Use parênteses para garantir a ordem desejada"
    Não confie apenas na memória da precedência. Use parênteses generosamente para tornar suas intenções explícitas e o código mais legível.

```python
# Exemplo de precedência
resultado = 10 + 5 * 2 ** 2  # 10 + 5 * 4 = 10 + 20 = 30
print(resultado)  # 30

resultado2 = (10 + 5) * 2 ** 2  # 15 * 4 = 60
print(resultado2)  # 60
```

### Operadores de identidade e pertencimento (bônus)
Embora não façam parte do escopo principal deste capítulo, é útil conhecer dois grupos adicionais:
- **Identidade:** `is` e `is not` verificam se duas variáveis apontam para o mesmo objeto na memória.
- **Pertencimento:** `in` e `not in` verificam se um valor está contido em uma sequência (como uma string ou lista).

```python
# Pertencimento
fruta = "abacaxi"
print("bac" in fruta)   # True

# Identidade (cuidado: use is para None, não para comparar inteiros pequenos em geral)
x = None
print(x is None)  # True
```

## Exemplos

??? example "Exemplo 1: Cálculo de média e situação do aluno"
    === "Código"
        ```python
        # Notas do aluno
        nota1 = 7.5
        nota2 = 8.0
        nota3 = 6.5
        media = (nota1 + nota2 + nota3) / 3

        # Verifica se foi aprovado (média >= 7)
        aprovado = media >= 7.0

        # Exibe os resultados
        print(f"Média: {media:.2f}")
        print(f"Aprovado? {aprovado}")
        ```

    === "Resultado"
        ```text
        Média: 7.33
        Aprovado? True
        ```

    === "Explicação"
        Usamos operadores aritméticos (`+`, `/`) para calcular a média e o operador de comparação `>=` para obter um valor booleano indicando aprovação. A variável `aprovado` armazena o resultado da comparação e pode ser usada diretamente em estruturas condicionais.

??? example "Exemplo 2: Verificação de faixa etária para desconto"
    === "Código"
        ```python
        idade = int(input("Digite sua idade: "))

        # Tem direito a desconto se for jovem (até 21 anos) OU idoso (60 anos ou mais)
        tem_desconto = idade <= 21 or idade >= 60

        # É meia-entrada se tiver desconto E não for um dia promocional
        dia_promocional = False  # suponha que hoje não é dia promocional
        meia_entrada = tem_desconto and not dia_promocional

        print(f"Desconto aplicável? {tem_desconto}")
        print(f"Paga meia-entrada? {meia_entrada}")
        ```

    === "Resultado"
        Suponha que o usuário digite 17:
        ```text
        Digite sua idade: 17
        Desconto aplicável? True
        Paga meia-entrada? True
        ```

    === "Explicação"
        Aqui combinamos operadores de comparação (`<=`, `>=`) com operadores lógicos (`or`, `and`, `not`) para construir regras de negócio. A lógica é progressiva: primeiro verificamos elegibilidade geral e depois uma condição específica (não ser dia promocional).

??? example "Exemplo 3: Atualização de estoque com atribuição combinada"
    === "Código"
        ```python
        estoque = 100

        # Venda de 15 unidades
        estoque -= 15
        print(f"Após venda: {estoque}")   # 85

        # Reposição de 30 unidades
        estoque += 30
        print(f"Após reposição: {estoque}") # 115

        # Aumento de 10% no estoque por correção de inventário
        estoque *= 1.10
        print(f"Após ajuste de 10%: {estoque:.1f}") # 126.5

        # Quebra acidental de 1/5 do estoque (usando divisão inteira para exemplificar)
        estoque //= 5
        print(f"Após quebra: {estoque}")  # 25
        ```

    === "Resultado"
        ```text
        Após venda: 85
        Após reposição: 115
        Após ajuste de 10%: 126.5
        Após quebra: 25
        ```

    === "Explicação"
        Demonstração prática dos operadores de atribuição combinada. Eles tornam o código mais conciso e legível, principalmente em laços e atualizações incrementais. Note que `estoque` muda de tipo de `float` para `int` após a divisão inteira, ilustrando a tipagem dinâmica.

## Exercícios

### Básico (fixação)
- Crie duas variáveis `a = 12` e `b = 5`. Calcule e exiba o resultado das seis operações aritméticas: adição, subtração, multiplicação, divisão, divisão inteira, resto e exponenciação (`a` elevado a `b`).
- Escreva um programa que pergunte o ano de nascimento e o ano atual, calcule a idade e exiba `True` se a pessoa for maior de idade (`idade >= 18`) ou `False` caso contrário.
- Dada a string `texto = "Python"`, use o operador `in` para verificar se a letra `"y"` está presente e exiba o resultado.

### Intermediário (aplicação)
Uma loja oferece frete grátis para compras acima de R$ 150,00 ou para clientes do programa de fidelidade. Escreva um programa que:
- Pergunte o valor da compra e se o cliente é fidelizado (responda "sim" ou "não").
- Armazene o valor em `compra` (float) e a fidelidade em `fidelidade` (booleano, `True`/`False` a partir da resposta).
- Calcule se o frete será gratuito usando operadores lógicos e de comparação.
- Exiba a mensagem: `"Frete grátis: True/False"`.

### Avançado (desafio)
Crie um programa que leia três números inteiros e verifique as seguintes condições usando apenas operadores (sem usar `if`, apenas expressões booleanas armazenadas em variáveis):
- `todos_positivos`: `True` se todos os números forem maiores que zero.
- `pelo_menos_um_par`: `True` se pelo menos um dos números for par.
- `exatamente_dois_maiores_que_10`: `True` se exatamente dois dos números forem maiores que 10.

Exiba os três resultados. Dica: para verificar quantidade exata, você pode somar resultados de comparações (`True = 1`, `False = 0`): `(a > 10) + (b > 10) + (c > 10) == 2`.

## Projeto Prático: Calculadora de Orçamento de Viagem
Desenvolva um programa que ajude um usuário a planejar o orçamento de uma viagem de carro. O programa deve:
1. Perguntar a distância total a percorrer (km).
2. Perguntar o consumo médio do veículo (km por litro).
3. Perguntar o preço do litro de combustível (R$).
4. Perguntar quantos pedágios haverá e o valor unitário de cada pedágio.
5. Calcular o custo total com combustível e com pedágios.
6. Exibir o custo total da viagem (combustível + pedágios).
7. Perguntar o orçamento disponível e, usando operadores de comparação, verificar se o orçamento é suficiente (`custo_total <= orcamento`).
8. Se for suficiente, exibir quanto sobrará; se não, exibir quanto faltará. Use operadores aritméticos e de atribuição para calcular a diferença.

**Diretrizes:**
- Utilize variáveis com nomes descritivos.
- Empregue operadores aritméticos para os cálculos.
- Use operadores de comparação e lógicos para verificar a suficiência.
- Exiba os resultados com formatação em f-strings.

**Exemplo de execução:**
```text
Distância (km): 500
Consumo (km/l): 12
Preço combustível (R$/l): 5.80
Número de pedágios: 4
Valor por pedágio: 15.50
Custo combustível: R$ 241.67
Custo pedágios: R$ 62.00
Custo total: R$ 303.67
Orçamento disponível: R$ 400.00
Orçamento suficiente? True
Sobra: R$ 96.33
```

Este projeto integra todos os operadores estudados, reforça a entrada e saída de dados e prepara você para os próximos capítulos, onde adicionaremos controle de fluxo.

## Resumo
Neste capítulo, você adquiriu as ferramentas fundamentais para processar informações em Python:
- Operadores aritméticos (`+`, `-`, `*`, `/`, `//`, `%`, `**`) realizam cálculos matemáticos.
- Operadores de comparação (`==`, `!=`, `>`, `<`, `>=`, `<=`) produzem valores booleanos comparando operandos.
- Operadores lógicos (`and`, `or`, `not`) combinam e invertem expressions booleanas.
- Operadores de atribuição (`=`, `+=`, `-=`, etc.) armazenam e atualizam valores de forma concisa.
- A precedência de operadores determina a ordem de avaliação; parênteses garantem clareza e controle.
- Expressões bem construídas são o alicerce de decisões e cálculos em qualquer aplicação.

Com esse conhecimento, você já consegue escrever programas que calculam, comparam e avaliam condições — ainda que de forma linear. O próximo passo é aprender a controlar o fluxo de execução, tomando decisões e repetindo tarefas.
