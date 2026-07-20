# 04. Repetições (for/while)

## Objetivos
Neste capítulo, você vai aprender a:
- Compreender o propósito das estruturas de repetição em programação.
- Utilizar o laço `while` para executar blocos enquanto uma condição for verdadeira.
- Utilizar o laço `for` para iterar sobre sequências como strings, listas e intervalos numéricos.
- Dominar a função `range()` para gerar sequências de números.
- Controlar o fluxo da repetição com as instruções `break` e `continue`.
- Reconhecer e evitar laços infinitos.
- Aplicar boas práticas para escrever laços claros e eficientes.

## Pré-requisitos
Antes de começar, certifique-se de que você domina:
- Variáveis e tipos de dados básicos (int, float, str, bool).
- Operadores de comparação e lógicos.
- Estruturas condicionais `if`, `elif`, `else`.
- Entrada e saída de dados com `input()` e `print()`.

Se algum desses tópicos não estiver consolidado, revise os capítulos anteriores.

## Motivação
Imagine que você precisa exibir na tela todos os números de 1 a 100. Com o que aprendemos até agora, você teria que escrever cem linhas de `print(1)`, `print(2)`, ... `print(100)`. Isso é inviável. E se a quantidade dependesse do usuário? Seria impossível prever quantas linhas escrever.

As estruturas de repetição resolvem exatamente esse problema: elas permitem que um bloco de código seja executado várias vezes, sob controle de uma condição ou percorrendo uma sequência. Com poucas linhas, você processa listas inteiras de clientes, valida entradas repetidamente até que o usuário forneça um valor correto, cria menus interativos e constrói animações simples. Dominar `for` e `while` é essencial para escrever programas dinâmicos e eficientes.

## Conteúdo

### O que são laços de repetição?
Um laço de repetição (ou loop) é uma estrutura que repete um conjunto de instruções. O número de repetições pode ser conhecido previamente ou determinado por uma condição. Python oferece dois laços principais:
- `while`: repete enquanto uma condição booleana for verdadeira.
- `for`: itera sobre cada item de uma sequência (string, lista, intervalo, etc.).

### O laço while
A sintaxe do `while` é simples:

```python
while condicao:
    # bloco de código a ser repetido
```

Enquanto `condicao` for avaliada como `True`, o bloco indentado é executado. A cada repetição, chamada de *iteração*, a condição é reavaliada. Quando ela se torna `False`, o laço termina e o programa prossegue para a próxima linha após o bloco.

```python
contador = 1
while contador <= 5:
    print(contador)
    contador += 1
print("Fim do laço")
```

Neste exemplo, `contador` começa em 1. A condição `contador <= 5` é verdadeira, então o laço imprime o valor e incrementa o contador. Quando `contador` atinge 6, a condição é falsa e o laço termina.

!!! warning "Cuidado com o laço infinito"
    Se a condição nunca se tornar falsa, o programa entrará em um laço infinito. Isso pode travar o terminal. Sempre garanta que a variável de controle será atualizada dentro do laço para que a condição eventualmente falhe. Exemplo de laço infinito (não execute sem saber parar):
    ```python
    x = 1
    while x > 0:  # condição sempre verdadeira
        print(x)
        x += 1
    ```

O laço `while` é ideal quando não sabemos quantas iterações serão necessárias, como ao validar entrada do usuário:

```python
resposta = ""
while resposta != "sair":
    resposta = input("Digite algo (ou 'sair' para terminar): ")
    print(f"Você digitou: {resposta}")
```

### O laço for e a função range()
O laço `for` é usado para percorrer uma sequência (qualquer objeto iterável): cada item da sequência é atribuído a uma variável, e o bloco é executado uma vez para cada item.

```python
frutas = ["maçã", "banana", "laranja"]
for fruta in frutas:
    print(fruta)
```

O exemplo acima percorre a lista `frutas` e imprime cada elemento. Também podemos iterar sobre strings:

```python
for letra in "Python":
    print(letra)
```

Agora, se quisermos repetir um bloco um número fixo de vezes, usamos a função `range()`. Ela gera uma sequência de números inteiros.
- `range(n)` gera números de `0` a `n-1`.
- `range(inicio, fim)` gera de `inicio` até `fim-1`.
- `range(inicio, fim, passo)` gera com o intervalo especificado.

```python
# Imprimindo os números de 0 a 9
for i in range(10):
    print(i)

# Números pares de 2 a 10
for i in range(2, 11, 2):
    print(i)
```

!!! tip "Quando usar while vs for"
    Use `while` quando a repetição depende de uma condição dinâmica (ex.: enquanto o usuário não acertar a senha). Use `for` quando o número de iterações é conhecido ou quando você precisa percorrer os itens de uma coleção.

### Controlando o laço: break e continue
Python oferece duas instruções especiais para alterar o fluxo normal de um laço:
- `break`: interrompe imediatamente o laço, saindo dele. O programa continua após o bloco do laço.
- `continue`: pula para a próxima iteração, ignorando o restante do bloco atual.

Exemplo com `break`:

```python
# Procura um número negativo em uma lista; ao encontrar, para.
numeros = [5, 8, -1, 7, 2]
for n in numeros:
    if n < 0:
        print(f"Encontrado negativo: {n}. Interrompendo.")
        break
    print(f"Processando {n}")
```

Exemplo com `continue`:

```python
# Imprime apenas os números pares, ignorando os ímpares
for i in range(1, 11):
    if i % 2 != 0:  # se for ímpar
        continue    # pula para a próxima iteração
    print(i)
```

!!! note "Uso em laços aninhados"
    `break` e `continue` afetam apenas o laço mais interno onde estão. Se você tiver um `for` dentro de outro `for`, um `break` no interno sairá apenas desse laço, não do externo.

### Laços aninhados
Podemos colocar um laço dentro de outro. Isso é útil para percorrer matrizes (listas de listas) ou gerar combinações.

```python
# Tabuada do 1 ao 5
for i in range(1, 6):
    for j in range(1, 11):
        print(f"{i} x {j} = {i * j}")
    print("-----------")
```

Cuidado com o desempenho: laços aninhados multiplicam o número total de iterações.

### O else nos laços (bônus)
Uma peculiaridade do Python: laços `while` e `for` podem ter uma cláusula `else`. O bloco `else` é executado quando o laço termina normalmente (sem ser interrompido por `break`). É pouco usado, mas pode ser útil em buscas.

```python
for item in [1, 3, 5]:
    if item == 2:
        print("Encontrado")
        break
else:
    print("Não encontrado")
```

### Boas práticas
- Mantenha o corpo do laço curto e focado.
- Utilize variáveis de controle com nomes descritivos.
- Evite modificar a sequência sobre a qual está iterando (pode causar comportamentos imprevisíveis). Se precisar, itere sobre uma cópia.
- Cuidado com laços infinitos: sempre teste com um contador limitado durante o desenvolvimento.
- Utilize `for` com `range` quando souber o número de repetições.
- Prefira `for item in sequencia` ao invés de usar índices `range(len(seq))` quando não precisar do índice.

## Exemplos

??? example "Exemplo 1: Validação de senha com while"
    === "Código"
        ```python
        # Senha secreta
        SENHA = "1234"
        tentativa = ""

        # Enquanto o usuário não acertar, continua perguntando
        while tentativa != SENHA:
            tentativa = input("Digite a senha: ")
            if tentativa != SENHA:
                print("Senha incorreta. Tente novamente.")

        print("Acesso concedido!")
        ```

    === "Resultado"
        Suponha que o usuário digite "1111", depois "1234":
        ```text
        Digite a senha: 1111
        Senha incorreta. Tente novamente.
        Digite a senha: 1234
        Acesso concedido!
        ```

    === "Explicação"
        O laço `while` é executado enquanto a condição `tentativa != SENHA` for verdadeira. Assim que o usuário acerta, a condição torna-se falsa e o laço termina. Esse padrão é clássico para validação de entrada.

??? example "Exemplo 2: Cálculo de fatorial com for"
    === "Código"
        ```python
        # Calcula o fatorial de um número
        numero = int(input("Número: "))
        fatorial = 1

        # Multiplica de 1 até numero
        for i in range(1, numero + 1):
            fatorial *= i

        print(f"{numero}! = {fatorial}")
        ```

    === "Resultado"
        Supondo entrada 5:
        ```text
        Número: 5
        5! = 120
        ```

    === "Explicação"
        O laço `for` percorre cada inteiro de 1 até o número fornecido. A variável `fatorial` acumula o produto. `range(1, numero + 1)` assegura que o último valor incluído seja o próprio número.

??? example "Exemplo 3: Menu interativo com while True e break"
    === "Código"
        ```python
        # Menu que repete até o usuário escolher sair
        while True:
            print("\n--- MENU ---")
            print("1. Somar")
            print("2. Subtrair")
            print("3. Sair")
            opcao = input("Escolha: ")

            if opcao == "1":
                a = float(input("Primeiro número: "))
                b = float(input("Segundo número: "))
                print(f"Resultado: {a + b}")
            elif opcao == "2":
                a = float(input("Primeiro número: "))
                b = float(input("Segundo número: "))
                print(f"Resultado: {a - b}")
            elif opcao == "3":
                print("Encerrando...")
                break  # interrompe o laço
            else:
                print("Opção inválida.")
        ```

    === "Resultado"
        Usuário escolhe 1, depois 3:
        ```text
        --- MENU ---
        1. Somar
        2. Subtrair
        3. Sair
        Escolha: 1
        Primeiro número: 10
        Segundo número: 5
        Resultado: 15.0

        --- MENU ---
        1. Somar
        2. Subtrair
        3. Sair
        Escolha: 3
        Encerrando...
        ```

    === "Explicação"
        O `while True` cria um laço que, em teoria, seria infinito. A única forma de sair é através do `break`, que é acionado quando o usuário escolhe a opção 3. Esse padrão é muito utilizado para menus em aplicações de console.

## Exercícios

### Básico (fixação)
- Usando o laço `while`, imprima todos os números de 10 a 1 (contagem regressiva) em ordem decrescente.
- Com o laço `for`, imprima os números pares de 0 a 20, inclusive.
- Escreva um programa que peça ao usuário para digitar uma letra. Continue pedindo até que ele digite a letra "x". Use `while`.

### Intermediário (aplicação)
Uma livraria deseja um programa para calcular o total de uma venda. O usuário insere o preço de cada livro. O programa deve somar os valores até que o usuário digite 0 para encerrar. Ao final, exiba:
- A quantidade de livros comprados.
- O valor total da compra.
- A média de preço por livro.

Utilize um laço `while` para receber os preços. Valide que o preço seja um valor positivo (se for negativo, peça novamente).

### Avançado (desafio)
Crie um programa que simule um caixa eletrônico simples. O programa inicia com um saldo de R$ 1000,00 e oferece um menu com as opções: [1] Depositar, [2] Sacar, [3] Saldo, [4] Sair. O menu deve reaparecer até o usuário escolher Sair. Regras:
- Não permitir saque maior que o saldo.
- Não permitir saque com valor negativo ou zero.
- Depósito deve ser um valor positivo.
- Após cada operação, exibir o saldo atualizado.
- Use `while True` e `break` para controlar o menu.
- Utilize `continue` para voltar ao início do laço quando uma operação falhar (ex.: tentativa de saque inválido).
- Mostre uma mensagem de despedida ao final.

## Projeto Prático: Jogo de Adivinhação com Tentativas
Desenvolva um jogo em que o computador escolhe um número aleatório entre 1 e 100, e o jogador tenta adivinhar. O programa deve:
1. Gerar o número secreto usando `random.randint(1, 100)` (importe `random`).
2. Dar as boas-vindas e informar que o número está entre 1 e 100.
3. Usar um laço `while` para receber palpites até que o jogador acerte.
4. A cada palpite, informar se o número secreto é maior ou menor que o chute.
5. Contar o número de tentativas.
6. Quando acertar, exibir uma mensagem de parabéns e o número de tentativas.
7. Perguntar se o jogador deseja jogar novamente. Se sim, gerar um novo número e reiniciar o contador; caso contrário, encerrar.

**Esqueleto do código:**
```python
import random

def jogar():
    numero_secreto = random.randint(1, 100)
    tentativas = 0
    acertou = False

    while not acertou:
        chute = int(input("Seu palpite: "))
        tentativas += 1
        # completar a lógica
    # exibir resultado

# loop principal para jogar novamente
```

Implemente o jogo completo, aplicando os conceitos de `while`, `if/else` e controle de fluxo. Inclua comentários que expliquem cada bloco.

## Resumo
Neste capítulo, você aprendeu que:
- Laços de repetição permitem executar blocos de código múltiplas vezes.
- O laço `while` repete enquanto uma condição for verdadeira, sendo ideal para situações com número incerto de iterações.
- O laço `for` percorre cada item de uma sequência (listas, strings, intervalos) e é a melhor opção quando se sabe exatamente sobre quais elementos iterar.
- A função `range()` gera sequências de números e é comumente usada com `for` para repetições contadas.
- As instruções `break` e `continue` oferecem controle refinado: `break` sai do laço; `continue` pula para a próxima iteração.
- É fundamental evitar laços infinitos não intencionais e manter o código do laço organizado.

Com esses recursos, seus programas ganham a capacidade de processar dados em massa, validar entradas e criar interações contínuas — uma habilidade essencial para qualquer desenvolvedor Python.
