# 03. Condicionais (if/else)

## Objetivos
Ao final deste capítulo, você estará apto a:
- Compreender o papel das estruturas condicionais no controle do fluxo de execução.
- Utilizar a instrução `if` para executar blocos de código com base em uma condição.
- Combinar `if` com `else` para criar caminhos alternativos.
- Encadear múltiplas condições com `elif`.
- Construir condicionais aninhadas para cenários mais complexos.
- Empregar o operador ternário para expressões condicionais compactas.
- Reconhecer valores considerados verdadeiros ou falsos em Python.
- Aplicar boas práticas para escrever código condicional legível e eficiente.

## Pré-requisitos
Antes de mergulhar nas estruturas condicionais, é fundamental que você domine:
- Criação e uso de variáveis (int, float, str, bool).
- Operadores de comparação (`==`, `!=`, `>`, `<`, `>=`, `<=`) e lógicos (`and`, `or`, `not`).
- Entrada de dados com `input()` e exibição com `print()`.
- Conversão entre tipos (`int()`, `float()`, `str()`, `bool()`).

Caso algum desses tópicos ainda não esteja claro, releia os capítulos anteriores sobre Variáveis e Operadores.

## Motivação
Até agora, escrevemos programas lineares: cada linha é executada na ordem, do início ao fim. Mas aplicações reais precisam tomar decisões. Um aplicativo de banco deve permitir saque apenas se o saldo for suficiente. Um jogo precisa reagir de forma diferente se o jogador acertar ou errar. Um sistema de login deve validar credenciais e negar acesso se estiverem incorretas.

As estruturas condicionais permitem que seu programa decida qual caminho seguir. Elas são o cérebro da lógica — sem elas, seu código seria um robô que nunca se adapta. Neste capítulo, você aprenderá a implementar tomadas de decisão e começará a construir programas realmente interativos e inteligentes.

## Conteúdo

### O que são estruturas condicionais?
Uma estrutura condicional avalia uma expressão booleana (que resulta em `True` ou `False`) e, com base nesse resultado, executa ou ignora um bloco de instruções. Python implementa isso com as palavras reservadas `if`, `elif` e `else`.

### A instrução if
A forma mais simples de condicional é o `if` isolado. Se a condição for verdadeira, o bloco indentado será executado; caso contrário, será ignorado.

```python
idade = 20
if idade >= 18:
    print("Você é maior de idade.")
    print("Já pode tirar a carteira de motorista.")
```

O bloco dentro do `if` deve ser indentado (recomenda-se 4 espaços). Python usa indentação para definir blocos — não chaves como em outras linguagens.

!!! warning "Indentação é obrigatória"
    Todo bloco após `if`, `elif` ou `else` precisa estar indentado consistentemente. Misturar espaços e tabulações gera erros. A convenção oficial (PEP 8) é usar 4 espaços por nível.

### A instrução if/else
Quando queremos executar um bloco se a condição for verdadeira e outro bloco caso contrário, usamos `else`.

```python
nota = 5.5
if nota >= 7.0:
    print("Aprovado")
else:
    print("Reprovado")
```

O `else` não possui condição própria — ele cobre todos os casos em que o `if` (e eventuais `elif`) falham.

### A instrução if/elif/else
Muitas situações exigem mais de duas ramificações. Para isso, usamos `elif` (contração de "else if"). Podemos encadear quantos `elif` forem necessários. Apenas o primeiro bloco cuja condição for verdadeira será executado; os demais são ignorados.

```python
media = 8.5
if media >= 9.0:
    conceito = "A"
elif media >= 7.5:
    conceito = "B"
elif media >= 6.0:
    conceito = "C"
elif media >= 4.0:
    conceito = "D"
else:
    conceito = "F"

print(f"Conceito final: {conceito}")
```

Neste exemplo, a condição `media >= 9.0` é falsa, mas `media >= 7.5` é verdadeira — conceito será `"B"`. As condições seguintes nem são avaliadas.

!!! note "A ordem das condições importa"
    Coloque as condições mais restritivas primeiro. Se começarmos testando `media >= 4.0`, o programa nunca alcançaria as faixas superiores, pois 8.5 também é >= 4.0.

### Condicionais aninhadas
Podemos colocar estruturas condicionais dentro de outras. Isso é útil quando uma decisão depende de múltiplos fatores hierárquicos.

```python
tem_cartao = True
valor_compra = 80

if tem_cartao:
    if valor_compra >= 100:
        desconto = 0.15
    else:
        desconto = 0.05
else:
    if valor_compra >= 100:
        desconto = 0.05
    else:
        desconto = 0.0

print(f"Desconto de {desconto * 100:.0f}%")
```

Embora funcione, aninhamentos profundos podem prejudicar a legibilidade. Muitas vezes, é possível reescrever usando operadores lógicos para simplificar.

### Operador ternário (expressão condicional)
Python oferece uma forma compacta de escrever um `if/else` simples em uma única linha. Sua sintaxe é:

```python
variavel = valor_se_verdadeiro if condicao else valor_se_falso
```

Exemplo:

```python
idade = 16
status = "Maior de idade" if idade >= 18 else "Menor de idade"
print(status)  # Menor de idade
```

!!! tip "Use o ternário com moderação"
    O operador ternário é elegante para atribuições condicionais simples, mas evite encadeá-lo múltiplas vezes — isso torna o código difícil de ler.

### Verdade e falsidade em Python
Em Python, qualquer objeto pode ser testado como booleano. São considerados falsos (`False`) os seguintes valores:
- `False`
- `None`
- Zero numérico: `0`, `0.0`, `0j`
- Sequências vazias: `''`, `[]`, `()`, `{}`, `set()`, `range(0)`

Todos os demais valores são considerados verdadeiros (`True`). Isso permite escrever verificações concisas:

```python
nome = input("Digite seu nome: ")
if nome:  # Equivalente a if nome != ""
    print(f"Olá, {nome}!")
else:
    print("Nome não informado.")
```

Aqui, `nome` será `True` se o usuário digitar algo, e `False` se ele pressionar Enter sem digitar.

### Boas práticas
- Mantenha as condições simples e legíveis. Extraia expressões complexas para variáveis nomeadas.
- Prefira `if/elif` em vez de longos aninhamentos.
- Evite comparações desnecessárias com `True`/`False`: escreva `if condicao:` em vez de `if condicao == True:`.
- Use parênteses para agrupar subexpressões e melhorar a clareza.
- Documente condições não óbvias com comentários.

## Exemplos

??? example "Exemplo 1: Classificação etária"
    === "Código"
        ```python
        idade = int(input("Digite sua idade: "))

        if idade < 0:
            categoria = "Idade inválida"
        elif idade <= 12:
            categoria = "Criança"
        elif idade <= 17:
            categoria = "Adolescente"
        elif idade <= 59:
            categoria = "Adulto"
        else:
            categoria = "Idoso"

        print(f"Categoria: {categoria}")
        ```

    === "Resultado"
        Supondo entrada 16:
        ```text
        Digite sua idade: 16
        Categoria: Adolescente
        ```

    === "Explicação"
        O código testa faixas etárias com `elif`. A primeira condição captura entradas negativas. Como a ordem importa, mesmo que `16 <= 59` seja verdadeiro, o bloco Adolescente é o primeiro a corresponder (`16 <= 17`) e os demais são ignorados.

??? example "Exemplo 2: Calculadora de tarifa de estacionamento"
    === "Código"
        ```python
        horas = float(input("Horas estacionadas: "))

        # Tarifa: até 1h = R$5, até 3h = R$10, acima = R$3 por hora adicional
        if horas <= 0:
            print("Tempo inválido.")
        elif horas <= 1:
            valor = 5.00
        elif horas <= 3:
            valor = 10.00
        else:
            # Horas adicionais além das 3 primeiras
            horas_extras = horas - 3
            valor = 10.00 + horas_extras * 3.00

        if horas > 0:
            print(f"Valor a pagar: R$ {valor:.2f}")
        ```

    === "Resultado"
        Supondo entrada 4.5:
        ```text
        Horas estacionadas: 4.5
        Valor a pagar: R$ 14.50
        ```

    === "Explicação"
        Observe o uso de `float` para aceitar frações de hora. O `if` mais externo trata valores não positivos. O bloco `else` calcula o excedente. Por fim, um `if` adicional garante que a mensagem de valor só seja exibida se as horas foram válidas.

??? example "Exemplo 3: Validador de senha com múltiplos critérios"
    === "Código"
        ```python
        senha = input("Crie uma senha: ")

        # Critérios: pelo menos 8 caracteres, contém número, contém letra maiúscula
        tem_tamanho = len(senha) >= 8
        tem_numero = any(c.isdigit() for c in senha)
        tem_maiuscula = any(c.isupper() for c in senha)

        if tem_tamanho and tem_numero and tem_maiuscula:
            print("Senha forte! Registrada com sucesso.")
        else:
            print("Senha fraca. Problemas:")
            if not tem_tamanho:
                print("- Mínimo de 8 caracteres.")
            if not tem_numero:
                print("- Deve conter pelo menos um número.")
            if not tem_maiuscula:
                print("- Deve conter pelo menos uma letra maiúscula.")
        ```

    === "Resultado"
        Supondo senha "abc123":
        ```text
        Crie uma senha: abc123
        Senha fraca. Problemas:
        - Mínimo de 8 caracteres.
        - Deve conter pelo menos uma letra maiúscula.
        ```

    === "Explicação"
        Cada critério é armazenado em uma variável booleana, melhorando a legibilidade. O primeiro `if` usa `and` para exigir todos os critérios. No `else`, condicionais aninhadas independentes informam ao usuário exatamente quais requisitos não foram atendidos. A função `any()` com gerador avalia se há dígito ou maiúscula.

## Exercícios

### Básico (fixação)
- Escreva um programa que leia um número inteiro e exiba se ele é par ou ímpar. Use o operador módulo `%`.
- Solicite ao usuário sua idade e verifique se ele já pode votar (`idade >= 16`). Exiba "Pode votar" ou "Não pode votar".
- Peça um número e diga se ele é positivo, negativo ou zero, utilizando `if/elif/else`.

### Intermediário (aplicação)
Uma empresa de energia elétrica cobra R$ 0,50 por kWh para os primeiros 200 kWh e R$ 0,75 para o consumo excedente. Escreva um programa que:
- Pergunte o consumo em kWh.
- Calcule o valor da conta.
- Aplique um desconto de 10% se o consumo for inferior a 100 kWh.
- Exiba o valor final com duas casas decimais.

Use apenas estruturas condicionais e operadores aprendidos.

### Avançado (desafio)
Crie um sistema simples de notas escolares que:
- Leia três notas (0 a 10).
- Calcule a média aritmética.
- Determine a situação do aluno conforme a tabela:
    - Média >= 7.0: Aprovado
    - Média entre 5.0 e 6.9: Recuperação
    - Média < 5.0: Reprovado
- Adicionalmente, em caso de Recuperação, verifique se a nota mais baixa é menor que 4.0. Se for, a situação muda para "Recuperação com risco" e exiba essa informação.
- Exiba a média, a situação e, se for o caso, a nota que puxou a média para baixo.

## Projeto Prático: Mini Calculadora com Menu
Desenvolva uma calculadora que opera com dois números e um operador escolhido pelo usuário. O programa deve:
1. Exibir um menu com as opções: `+`, `-`, `*`, `/` e `S` (sair).
2. Solicitar a operação desejada.
3. Se a operação for válida (`+`, `-`, `*`, `/`), solicitar dois números (`float`).
4. Realizar a operação e exibir o resultado.
5. Tratar divisão por zero: se o operador for `/` e o segundo número for zero, exibir "Erro: divisão por zero".
6. Se a opção for `S`, encerrar o programa com uma mensagem de despedida.
7. Se a opção for inválida (diferente de `+`, `-`, `*`, `/`, `S`), exibir "Operação inválida." e voltar ao menu.

Use estruturas `if/elif/else` para selecionar a operação e condicionais aninhadas para tratar a divisão por zero. O menu pode ser implementado com um laço `while` (se já tiver visto) ou, alternativamente, execute o programa uma única vez para cada operação (sem laço), focando na lógica condicional.

**Exemplo de execução:**
```text
Escolha uma operação (+, -, *, /, S): /
Número 1: 10
Número 2: 0
Erro: divisão por zero.
```

**Desafio extra:** Acrescente a operação `**` (exponenciação) e `%` (resto). Permita que o usuário continue operando até escolher `S`, usando um laço `while True` com `break`.

## Resumo
Neste capítulo, você aprendeu a controlar o fluxo de seus programas com estruturas condicionais:
- O `if` executa um bloco quando uma condição é verdadeira.
- O `else` oferece um caminho alternativo quando a condição é falsa.
- O `elif` permite encadear múltiplas verificações, avaliando-as sequencialmente até que uma seja verdadeira.
- Condicionais podem ser aninhadas para decisões hierárquicas.
- O operador ternário fornece uma sintaxe concisa para `if/else` simples.
- Python trata muitos valores como verdadeiros ou falsos, simplificando verificações como `if variavel:`.
- Seguir boas práticas mantém o código condicional legível e menos propenso a erros.

Dominar `if/elif/else` é um divisor de águas: a partir de agora, seus programas podem reagir a dados, validar entradas e implementar regras de negócio. Você está no caminho para criar software que realmente interage com o usuário.
