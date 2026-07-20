# 05. Funções

## Objetivos
Neste capítulo, você aprenderá a:
- Compreender a importância das funções para a modularização do código.
- Definir funções em Python com a palavra reservada `def`.
- Utilizar parâmetros para tornar as funções flexíveis e reutilizáveis.
- Devolver resultados com a instrução `return`.
- Distinguir entre parâmetros obrigatórios e opcionais (com valores padrão).
- Entender o conceito de escopo de variáveis (locais e globais).
- Documentar suas funções de forma profissional com docstrings.
- Aplicar boas práticas para criar código legível, reutilizável e de fácil manutenção.

## Pré-requisitos
Antes de prosseguir, você deve dominar:
- Variáveis e tipos de dados (int, float, str, bool, listas).
- Operadores aritméticos, de comparação e lógicos.
- Estruturas condicionais (`if`, `elif`, `else`).
- Estruturas de repetição (`for`, `while`).

Se algum desses tópicos ainda não estiver consolidado, revise os capítulos anteriores para acompanhar com segurança.

## Motivação
Conforme seus programas crescem, você perceberá que certas tarefas se repetem: validar um CPF, calcular um desconto, exibir um menu, ordenar uma lista. Copiar e colar o mesmo trecho de código várias vezes torna o programa difícil de manter — qualquer alteração exige que você modifique todas as cópias, aumentando o risco de erros.

As funções são a solução. Elas permitem encapsular um bloco de código que realiza uma tarefa específica, dando-lhe um nome. Em vez de repetir a lógica, você simplesmente chama a função. Isso torna o código:
- **Modular**: dividido em partes menores e independentes.
- **Reutilizável**: uma função escrita uma vez pode ser usada em vários lugares.
- **Legível**: o nome da função descreve o que ela faz.
- **Testável**: cada função pode ser testada isoladamente.

Neste capítulo, você vai construir sua caixa de ferramentas pessoal, aprendendo a criar funções que estruturam o código de forma profissional.

## Conteúdo

### Definindo uma função
A sintaxe básica para criar uma função é:

```python
def nome_da_funcao(parametros):
    """Docstring: descrição do que a função faz."""
    # corpo da função
    return valor  # opcional
```

- `def` é a palavra reservada que inicia a definição.
- O nome da função segue as mesmas regras de nomenclatura de variáveis: letras minúsculas, sublinhados para separar palavras (snake_case).
- Os parênteses após o nome podem conter zero ou mais parâmetros.
- O corpo da função é indentado (4 espaços).
- A instrução `return` é opcional e devolve um valor ao chamador.

Exemplo simples:

```python
def saudacao():
    """Exibe uma saudação amigável."""
    print("Olá! Seja bem-vindo(a)!")

# Chamando a função
saudacao()
```

!!! note "Funções são objetos"
    Em Python, funções são objetos de primeira classe. Isso significa que você pode atribuí-las a variáveis, passá-las como argumentos para outras funções e armazená-las em estruturas de dados. Por enquanto, foque em defini-las e chamá-las.

### Parâmetros e argumentos
Parâmetros são variáveis listadas na definição da função. Quando chamamos a função, passamos argumentos — os valores reais que os parâmetros receberão.

```python
def exibir_mensagem(nome, mensagem):
    """Exibe uma mensagem personalizada."""
    print(f"{nome}, {mensagem}")

exibir_mensagem("João", "sua conta está pronta.")
# Saída: João, sua conta está pronta.
```

Os argumentos podem ser passados por posição (como acima) ou por nome (argumentos nomeados), que deixam o código mais claro:

```python
exibir_mensagem(mensagem="bom dia", nome="Maria")
```

### Parâmetros com valor padrão (opcionais)
Podemos atribuir um valor padrão a um parâmetro. Assim, se o argumento não for fornecido, o valor padrão será usado. Parâmetros opcionais devem vir depois dos obrigatórios.

```python
def saudacao_horario(nome, periodo="dia"):
    """Exibe saudação de acordo com o período."""
    print(f"Bom {periodo}, {nome}!")

saudacao_horario("Ana")           # Bom dia, Ana!
saudacao_horario("Carlos", "tarde")  # Bom tarde, Carlos!
```

!!! warning "Cuidado com valores padrão mutáveis"
    Evite usar listas ou dicionários como valores padrão, pois eles são criados uma única vez e compartilhados entre todas as chamadas. Se necessário, use `None` como padrão e crie uma nova lista dentro da função:
    ```python
    def adicionar_item(item, lista=None):
        if lista is None:
            lista = []
        lista.append(item)
        return lista
    ```

### Retornando valores com return
A instrução `return` devolve um resultado para quem chamou a função. Se não houver `return` explícito, a função retorna `None` automaticamente.

```python
def somar(a, b):
    """Retorna a soma de dois números."""
    return a + b

resultado = somar(5, 3)
print(resultado)  # 8
```

Uma função pode retornar múltiplos valores, que são empacotados em uma tupla:

```python
def calcular_retangulo(base, altura):
    """Retorna área e perímetro de um retângulo."""
    area = base * altura
    perimetro = 2 * (base + altura)
    return area, perimetro

a, p = calcular_retangulo(5, 3)
print(f"Área: {a}, Perímetro: {p}")  # Área: 15, Perímetro: 16
```

!!! tip "Múltiplos retornos e desempacotamento"
    O retorno múltiplo é na verdade uma tupla. Você pode tratá-lo como tal: `dados = calcular_retangulo(5,3)` e acessar `dados[0]` e `dados[1]`. O desempacotamento em variáveis separadas é mais legível.

### Escopo de variáveis
O escopo define onde uma variável é acessível. Python tem dois escopos principais:
- **Variável local**: definida dentro de uma função. Só pode ser acessada dentro dela.
- **Variável global**: definida fora de todas as funções. Pode ser lida em qualquer lugar, mas para modificá-la dentro de uma função é necessário declarar `global`.

```python
total = 0  # variável global

def adicionar(valor):
    global total  # informa que usaremos a variável global
    total += valor

adicionar(10)
print(total)  # 10
```

No entanto, o uso excessivo de variáveis globais é desencorajado, pois dificulta o rastreamento de efeitos colaterais. Prefira passar valores como argumentos e retornar resultados.

### Docstrings
Docstrings são textos delimitados por três aspas duplas que descrevem o propósito da função, seus parâmetros e valor de retorno. Elas são acessíveis via `help(nome_da_funcao)` e por ferramentas de documentação automática.

```python
def dividir(dividendo, divisor):
    """
    Realiza a divisão de dois números.

    Args:
        dividendo (float): O número a ser dividido.
        divisor (float): O número pelo qual dividir.

    Returns:
        float: O resultado da divisão, ou None se divisor for zero.
    """
    if divisor == 0:
        print("Erro: divisão por zero.")
        return None
    return dividendo / divisor
```

!!! note "Estilo de docstring"
    Existem vários estilos (Google, NumPy, Sphinx). O importante é ser consistente e incluir descrição, parâmetros e retorno. O exemplo acima segue o estilo Google.

### Funções como abstração
Funções não servem apenas para reuso, mas também para abstrair complexidade. Ao nomear um bloco de código com um verbo descritivo (`calcular_imc`, `validar_cpf`, `carregar_configuracao`), você cria uma camada de legibilidade que permite entender o programa sem mergulhar nos detalhes de implementação.

### Boas práticas
- **Nomes descritivos**: prefira `calcular_media` a `calc_med` ou `f1`.
- **Funções pequenas**: cada função deve fazer uma única coisa bem definida.
- **Evite efeitos colaterais**: uma função idealmente não modifica variáveis globais nem imprime diretamente (a menos que seu propósito seja esse). Prefira retornar valores.
- **Documente**: use docstrings, especialmente se a função for exposta a outros desenvolvedores.
- **Teste**: escreva chamadas de teste para verificar se a função se comporta como esperado.

## Exemplos

??? example "Exemplo 1: Conversor de temperatura com função"
    === "Código"
        ```python
        def celsius_para_fahrenheit(celsius):
            """Converte temperatura de Celsius para Fahrenheit."""
            return celsius * 9/5 + 32

        def fahrenheit_para_celsius(fahrenheit):
            """Converte temperatura de Fahrenheit para Celsius."""
            return (fahrenheit - 32) * 5/9

        # Testando as funções
        temp_c = 25
        temp_f = celsius_para_fahrenheit(temp_c)
        print(f"{temp_c}°C = {temp_f:.1f}°F")

        temp_f2 = 98.6
        temp_c2 = fahrenheit_para_celsius(temp_f2)
        print(f"{temp_f2}°F = {temp_c2:.1f}°C")
        ```

    === "Resultado"
        ```text
        25°C = 77.0°F
        98.6°F = 37.0°C
        ```

    === "Explicação"
        Duas funções independentes realizam a conversão entre escalas. Cada uma recebe um valor numérico e retorna o resultado. O programa chama as funções e exibe os resultados formatados. A lógica fica encapsulada e pode ser reutilizada em qualquer parte do código.

??? example "Exemplo 2: Validador de CPF simplificado"
    === "Código"
        ```python
        def formatar_cpf(cpf):
            """Remove caracteres não numéricos do CPF."""
            return ''.join(c for c in cpf if c.isdigit())

        def validar_tamanho(cpf_limpo):
            """Verifica se o CPF tem 11 dígitos."""
            return len(cpf_limpo) == 11

        def exibir_resultado(cpf, valido):
            """Exibe o resultado da validação."""
            if valido:
                print(f"CPF {cpf} é válido (tamanho correto).")
            else:
                print(f"CPF {cpf} é inválido.")

        # Fluxo principal
        entrada = input("Digite o CPF: ")
        cpf_limpo = formatar_cpf(entrada)
        tamanho_ok = validar_tamanho(cpf_limpo)
        exibir_resultado(entrada, tamanho_ok)
        ```

    === "Resultado"
        Supondo entrada "123.456.789-09":
        ```text
        Digite o CPF: 123.456.789-09
        CPF 123.456.789-09 é válido (tamanho correto).
        ```

    === "Explicação"
        O problema foi decomposto em funções com responsabilidades únicas: limpar a string, validar a quantidade de dígitos e exibir o resultado. Isso facilita a manutenção e os testes. Note que a validação completa de CPF envolveria dígitos verificadores, mas o exemplo ilustra a modularização.

??? example "Exemplo 3: Função com valor padrão e múltiplo retorno"
    === "Código"
        ```python
        def calcular_desconto(preco, percentual=5):
            """
            Calcula o valor do desconto e o preço final.

            Args:
                preco (float): Preço original do produto.
                percentual (float): Percentual de desconto (padrão 5).

            Returns:
                tuple: (valor_desconto, preco_final)
            """
            desconto = preco * percentual / 100
            preco_final = preco - desconto
            return desconto, preco_final

        # Chamadas
        preco1 = 200.00
        desc, final = calcular_desconto(preco1)
        print(f"Preço: R${preco1:.2f}, Desconto: R${desc:.2f}, Final: R${final:.2f}")

        # Especificando o percentual
        desc2, final2 = calcular_desconto(350.00, 15)
        print(f"Preço: R$350.00, Desconto: R${desc2:.2f}, Final: R${final2:.2f}")
        ```

    === "Resultado"
        ```text
        Preço: R$200.00, Desconto: R$10.00, Final: R$190.00
        Preço: R$350.00, Desconto: R$52.50, Final: R$297.50
        ```

    === "Explicação"
        A função `calcular_desconto` tem um parâmetro opcional `percentual` com valor padrão 5. Quando chamada sem o segundo argumento, aplica 5%. O retorno múltiplo permite obter tanto o valor do desconto quanto o preço final de uma só vez. O desempacotamento em `desc, final` torna o código limpo.

## Exercícios

### Básico (fixação)
- Escreva uma função chamada `dobro(numero)` que receba um número inteiro e retorne o dobro dele. Teste-a com alguns valores.
- Crie uma função `exibir_nome_idade(nome, idade)` que imprima: "Nome: ..., Idade: ...". Chame-a com seus dados.
- Defina uma função `e_par(numero)` que retorna `True` se o número for par e `False` caso contrário. Utilize-a em um programa que percorra números de 1 a 10 e imprima se cada um é par ou ímpar.

### Intermediário (aplicação)
Desenvolva uma função `calcular_media(notas)` que receba uma lista de notas (números) e retorne a média aritmética. Em seguida, crie outra função `situacao(media)` que retorne "Aprovado" (média >= 7), "Recuperação" (5 <= média < 7) ou "Reprovado" (média < 5). Escreva um programa que leia 3 notas, calcule a média usando essas funções e exiba a situação do aluno.

### Avançado (desafio)
Implemente um sistema de conversão de unidades com as seguintes funções:
- `metros_para_km(metros)`: converte metros para quilômetros.
- `km_para_milhas(km)`: converte quilômetros para milhas.
- `milhas_para_pes(milhas)`: converte milhas para pés.
- `pes_para_metros(pes)`: converte pés para metros.

Crie também uma função `converter(valor, unidade_origem, unidade_destino)` que, com base em strings ("m", "km", "mi", "ft"), escolhe automaticamente a combinação de funções adequada e retorna o valor convertido. Se a conversão não for suportada, retorne `None`. Documente cada função com docstrings. Exemplo de uso: `converter(1000, "m", "km")` deve retornar `1.0`.

## Projeto Prático: Calculadora Modular com Funções
Desenvolva uma calculadora de console que ofereça operações matemáticas básicas e avançadas, toda estruturada em funções.

**Requisitos:**
1. Crie uma função para cada operação: `somar(a, b)`, `subtrair(a, b)`, `multiplicar(a, b)`, `dividir(a, b)`, `potencia(a, b)`.
2. A função `dividir` deve tratar divisão por zero e retornar `None` nesse caso, exibindo uma mensagem de erro.
3. Crie uma função `exibir_menu()` que mostre as opções disponíveis e retorne a escolha do usuário.
4. Implemente a função `executar_calculadora()` que:
    - Chama `exibir_menu()` para obter a operação.
    - Solicita os dois números.
    - Chama a função correspondente e exibe o resultado formatado.
    - Pergunta se o usuário deseja continuar. Se sim, repete o processo; senão, encerra.
5. Use um laço `while` e controle com `break`/`continue` conforme necessário.
6. Todas as funções devem ter docstrings.
7. O programa deve ser robusto contra entradas inválidas (ex.: usuário digitar texto em vez de número) — use `try/except` se já conhecer, ou valide de forma simples com condicionais.

**Esqueleto inicial:**
```python
def somar(a, b):
    """Retorna a soma de a e b."""
    return a + b

# ... implementar demais funções

def exibir_menu():
    print("\n1. Somar\n2. Subtrair\n...\n5. Sair")
    return input("Escolha: ")

def executar_calculadora():
    while True:
        opcao = exibir_menu()
        if opcao == "5":
            print("Encerrando...")
            break
        # solicitar números e chamar função apropriada

if __name__ == "__main__":
    executar_calculadora()
```

Complete o projeto, garantindo que a modularização facilite a leitura e futuras expansões (como adicionar raiz quadrada ou funções trigonométricas).

## Resumo
Neste capítulo, você aprendeu que:
- Funções são blocos nomeados de código reutilizável, definidos com `def`.
- Parâmetros permitem que as funções recebam dados; argumentos são os valores passados na chamada.
- Parâmetros com valor padrão tornam alguns argumentos opcionais.
- A instrução `return` devolve um resultado; sem ela, a função retorna `None`.
- Variáveis dentro de funções são locais; para modificar uma global, use `global`.
- Docstrings documentam a função e são acessíveis via `help()`.
- Boas práticas incluem funções pequenas, com um único propósito, e nomes descritivos.

As funções são a espinha dorsal da programação procedural. Agora você pode decompor problemas em partes menores, reutilizar lógica e tornar seu código muito mais organizado.
