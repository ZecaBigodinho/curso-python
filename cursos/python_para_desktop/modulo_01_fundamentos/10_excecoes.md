# 10. Tratamento de Erros e Exceções

## Objetivos
Neste capítulo, você aprenderá a:
- Compreender a diferença entre erros de sintaxe e exceções.
- Utilizar os blocos `try`, `except`, `else` e `finally` para capturar e tratar exceções.
- Identificar e capturar exceções específicas, evitando o uso indiscriminado de `except` genérico.
- Criar suas próprias classes de exceção para representar situações de erro específicas da sua aplicação.
- Compreender a importância de não silenciar erros e de registrar informações úteis para depuração.
- Desenvolver programas mais robustos e previsíveis, capazes de lidar com entradas inválidas e falhas inesperadas.

## Pré-requisitos
Antes de prosseguir, certifique-se de que você domina:
- Fundamentos da linguagem Python: variáveis, tipos de dados e operadores.
- Estruturas de controle (`if`, `elif`, `else`, `for`, `while`).
- Definição e uso de funções.
- Manipulação de arquivos e conceitos de entrada e saída.
- Noções básicas de orientação a objetos (para a seção de exceções personalizadas).

Se algum desses tópicos ainda não estiver consolidado, reserve um momento para revisá-los.

## Motivação
Até agora, escrevemos programas que funcionam bem quando tudo ocorre conforme o esperado: o usuário digita um número quando pedimos um número, o arquivo que tentamos abrir existe, a divisão que realizamos não é por zero. Mas a realidade das aplicações é diferente. Usuários cometem erros, arquivos são movidos ou deletados, conexões de rede falham, dados externos vêm corrompidos. Se o programa não estiver preparado para essas situações, ele simplesmente trava, exibindo uma mensagem de erro críptica e encerrando de forma abrupta. Em um software profissional, isso é inaceitável.

O tratamento de exceções permite que seu programa anticipe problemas e responda a eles de maneira controlada. Em vez de travar, você pode exibir uma mensagem amigável, tentar uma ação alternativa, registrar o erro para análise posterior ou, no pior caso, encerrar de forma graciosa, salvando os dados do usuário. Essa capacidade de lidar com o inesperado é o que separa um script frágil de uma aplicação robusta.

Neste capítulo, você dominará os mecanismos que Python oferece para detectar, capturar e reagir a erros em tempo de execução, além de aprender a criar suas próprias exceções para tornar o código ainda mais expressivo e seguro.

## Conteúdo

### Erros versus exceções
Em Python, é importante distinguir dois tipos de problemas:
- **Erros de sintaxe (`SyntaxError`)**: ocorrem quando o código não segue as regras gramaticais da linguagem. O programa nem chega a ser executado. Exemplo: esquecer dois-pontos após um `if`.
- **Exceções**: ocorrem durante a execução, mesmo que a sintaxe esteja correta. Exemplos: tentar abrir um arquivo que não existe (`FileNotFoundError`), dividir por zero (`ZeroDivisionError`), acessar um índice inválido em uma lista (`IndexError`).

São as exceções que podemos — e devemos — tratar.

### A estrutura try/except
A forma básica de capturar uma exceção é com o bloco `try/except`:

```python
try:
    # Código que pode gerar uma exceção
    numero = int(input("Digite um número: "))
    resultado = 10 / numero
    print(f"Resultado: {resultado}")
except:
    # Código executado se qualquer exceção ocorrer no bloco try
    print("Ocorreu um erro. Tente novamente.")
```

Esse `except` vazio captura *qualquer* exceção, mas é uma prática desencorajada, pois pode esconder erros inesperados e dificultar a depuração.

### Capturando exceções específicas
O ideal é especificar o tipo de exceção que queremos tratar:

```python
try:
    numero = int(input("Digite um número inteiro: "))
    resultado = 10 / numero
    print(f"10 dividido por {numero} é {resultado}")
except ValueError:
    print("Erro: você não digitou um número inteiro válido.")
except ZeroDivisionError:
    print("Erro: não é possível dividir por zero.")
```

Podemos ter múltiplos blocos `except`, cada um tratando uma exceção diferente. Python executa o primeiro `except` cujo tipo corresponda à exceção levantada.

!!! note "Hierarquia de exceções"
    As exceções em Python formam uma hierarquia de classes. Por exemplo, `ZeroDivisionError` é uma subclasse de `ArithmeticError`, que é subclasse de `Exception`. Capturar uma exceção pai captura também todas as suas subclasses. Por isso, `except Exception` captura a maioria das exceções (mas não `SystemExit`, `KeyboardInterrupt` ou `GeneratorExit`).

### Acessando o objeto da exceção
Podemos capturar o objeto exceção com a palavra `as` e obter detalhes sobre o erro:

```python
try:
    lista = [1, 2, 3]
    indice = int(input("Índice: "))
    print(lista[indice])
except IndexError as e:
    print(f"Erro de índice: {e}")
except ValueError as e:
    print(f"Erro de valor: {e}")
```

### O bloco else
Opcionalmente, podemos incluir um bloco `else` após todos os `except`. Ele é executado somente se **nenhuma** exceção ocorrer no bloco `try`.

```python
try:
    arquivo = open("dados.txt", "r", encoding="utf-8")
except FileNotFoundError:
    print("Arquivo não encontrado.")
else:
    conteudo = arquivo.read()
    arquivo.close()
    print(f"Conteúdo: {conteudo}")
```

O `else` é útil para separar o código que pode gerar exceção do código que depende do sucesso da operação, mantendo o `try` enxuto.

### O bloco finally
O bloco `finally` é executado sempre, independentemente de ter ocorrido exceção ou não. É o local ideal para ações de limpeza, como fechar arquivos ou conexões.

```python
arquivo = None
try:
    arquivo = open("dados.txt", "r", encoding="utf-8")
    # processa o arquivo
except FileNotFoundError:
    print("Arquivo não encontrado.")
finally:
    if arquivo:
        arquivo.close()
        print("Arquivo fechado.")
```

!!! tip "Use with em vez de finally para arquivos"
    O gerenciador de contexto `with open(...) as f:` já garante o fechamento automático, substituindo a necessidade de `finally` nesse caso específico. Porém, `finally` permanece essencial para outros recursos que não possuem gerenciador de contexto.

### Levantando exceções com raise
Podemos provocar intencionalmente uma exceção usando a palavra `raise`. Isso é comum em funções que precisam sinalizar que um argumento é inválido:

```python
def calcular_raiz_quadrada(numero):
    if numero < 0:
        raise ValueError("Não é possível calcular raiz quadrada de número negativo.")
    return numero ** 0.5
```

### Criando exceções personalizadas
Para representar situações de erro específicas do domínio da aplicação, podemos criar nossas próprias classes de exceção, herdando de `Exception`:

```python
class SaldoInsuficienteError(Exception):
    """Exceção lançada quando há tentativa de saque com saldo insuficiente."""
    def __init__(self, saldo, valor):
        self.saldo = saldo
        self.valor = valor
        mensagem = f"Saldo insuficiente: R${saldo:.2f} para sacar R${valor:.2f}"
        super().__init__(mensagem)

class ContaBancaria:
    def __init__(self, saldo_inicial=0):
        self.saldo = saldo_inicial

    def sacar(self, valor):
        if valor > self.saldo:
            raise SaldoInsuficienteError(self.saldo, valor)
        self.saldo -= valor
        return self.saldo
```

Assim, quem chama `sacar` pode capturar `SaldoInsuficienteError` especificamente e tomar decisões adequadas.

### Exceções comuns em Python

| Exceção | Causa típica |
| :--- | :--- |
| `ValueError` | Função recebe argumento com valor inadequado. |
| `TypeError` | Operação com tipo incompatível. |
| `IndexError` | Acesso a índice inexistente em sequência. |
| `KeyError` | Acesso a chave inexistente em dicionário. |
| `FileNotFoundError` | Arquivo ou diretório não encontrado. |
| `ZeroDivisionError` | Divisão ou módulo por zero. |
| `AttributeError` | Tentativa de acessar atributo inexistente. |
| `ImportError` | Falha ao importar módulo. |
| `PermissionError` | Sem permissão para operação de arquivo. |

### Boas práticas
- Seja específico nos `except`: capture apenas as exceções que você sabe tratar.
- Não use `except:` puro (sem tipo). Se precisar de um genérico, use `except Exception:` e registre o erro.
- Nunca silencie exceções sem registro: `except: pass` é perigoso, pois esconde bugs.
- Use `else` para código que deve rodar apenas se não houve erro.
- Use `finally` para liberar recursos (se não estiver usando gerenciador de contexto).
- Crie exceções personalizadas para tornar o código mais expressivo.
- Registre erros com `logging` em vez de apenas imprimir no console.
- Valide dados cedo: quanto antes você detectar e lançar uma exceção, mais fácil será rastrear o problema.

!!! warning "Não transforme exceções em fluxo normal de controle"
    Exceções devem ser usadas para situações excepcionais. Se uma condição é esperada (ex.: fim de arquivo), utilize um `if` em vez de capturar `StopIteration`. Exceções têm custo de desempenho e tornam o código mais difícil de seguir.

## Exemplos

??? example "Exemplo 1: Calculadora segura com tratamento de erros"
    === "Código"
        ```python
        def calculadora():
            while True:
                print("\n--- Calculadora Segura ---")
                try:
                    # Entrada dos números
                    a = float(input("Primeiro número: "))
                    b = float(input("Segundo número: "))
                    operador = input("Operação (+, -, *, /) ou 'sair': ")

                    if operador.lower() == 'sair':
                        print("Encerrando calculadora.")
                        break

                    # Realiza a operação
                    if operador == '+':
                        resultado = a + b
                    elif operador == '-':
                        resultado = a - b
                    elif operador == '*':
                        resultado = a * b
                    elif operador == '/':
                        resultado = a / b
                    else:
                        print("Operação inválida. Use +, -, * ou /.")
                        continue

                    print(f"{a} {operador} {b} = {resultado:.2f}")

                except ValueError:
                    print("Erro: Digite apenas números válidos.")
                except ZeroDivisionError:
                    print("Erro: Divisão por zero não é permitida.")
                except Exception as e:
                    print(f"Erro inesperado: {e}")

        # Chame a função para testar (descomente)
        # calculadora()
        ```

    === "Resultado"
        ```text
        --- Calculadora Segura ---
        Primeiro número: 10
        Segundo número: 0
        Operação (+, -, *, /) ou 'sair': /
        Erro: Divisão por zero não é permitida.

        --- Calculadora Segura ---
        Primeiro número: 10
        Segundo número: abc
        Erro: Digite apenas números válidos.
        ```

    === "Explicação"
        O laço `while True` mantém a calculadora ativa. O bloco `try` envolve toda a lógica de entrada e cálculo. Capturamos `ValueError` para entradas não numéricas e `ZeroDivisionError` para divisões por zero. Um `except Exception` genérico captura qualquer outro erro inesperado, exibindo a mensagem. A palavra `continue` volta ao início do laço após um erro de operação, sem encerrar o programa.

??? example "Exemplo 2: Leitura segura de arquivo de configuração"
    === "Código"
        ```python
        def carregar_configuracao(caminho):
            config = {}
            try:
                with open(caminho, 'r', encoding='utf-8') as arquivo:
                    for linha in arquivo:
                        linha = linha.strip()
                        if not linha or linha.startswith('#'):
                            continue  # ignora linhas vazias e comentários
                        chave, valor = linha.split('=', 1)
                        config[chave.strip()] = valor.strip()
            except FileNotFoundError:
                print(f"Aviso: Arquivo '{caminho}' não encontrado. Usando padrões.")
            except PermissionError:
                print(f"Erro: Sem permissão para ler '{caminho}'.")
                raise  # relança a exceção para o chamador decidir
            except ValueError:
                print(f"Erro: Linha mal formatada em '{caminho}'.")
            else:
                print(f"Configuração carregada com sucesso: {len(config)} chaves.")
            return config

        # Uso
        config = carregar_configuracao("app.conf")
        print("Configurações:", config)
        ```

    === "Resultado"
        Supondo que o arquivo não exista:
        ```text
        Aviso: Arquivo 'app.conf' não encontrado. Usando padrões.
        Configurações: {}
        ```

    === "Explicação"
        A função tenta abrir e processar um arquivo de configuração (formato `chave=valor`). Cada situação de erro é tratada separadamente: `FileNotFoundError` avisa e retorna dicionário vazio; `PermissionError` relança a exceção para que o chamador decida; `ValueError` captura linhas mal formatadas. O bloco `else` é executado apenas se o `try` for bem-sucedido, exibindo a contagem de chaves.

??? example "Exemplo 3: Validação com exceção personalizada"
    === "Código"
        ```python
        class IdadeInvalidaError(Exception):
            """Exceção para idades fora do intervalo permitido."""
            pass

        def validar_idade(idade):
            if not isinstance(idade, int):
                raise TypeError("Idade deve ser um número inteiro.")
            if idade < 0 or idade > 150:
                raise IdadeInvalidaError(f"Idade {idade} fora do intervalo 0-150.")
            return True

        def cadastrar_usuario(nome, idade):
            try:
                validar_idade(idade)
            except TypeError as e:
                print(f"Erro de tipo: {e}")
                return False
            except IdadeInvalidaError as e:
                print(f"Erro de validação: {e}")
                return False
            else:
                print(f"Usuário '{nome}', {idade} anos, cadastrado com sucesso.")
                return True

        # Testes
        cadastrar_usuario("Ana", 25)     # sucesso
        cadastrar_usuario("João", -5)    # idade inválida
        cadastrar_usuario("Bia", "trinta")  # erro de tipo
        ```

    === "Resultado"
        ```text
        Usuário 'Ana', 25 anos, cadastrado com sucesso.
        Erro de validação: Idade -5 fora do intervalo 0-150.
        Erro de tipo: Idade deve ser um número inteiro.
        ```

    === "Explicação"
        A classe `IdadeInvalidaError` herda de `Exception` e representa uma regra de negócio violada. A função `validar_idade` usa `raise` para sinalizar erros de tipo e de valor. O chamador `cadastrar_usuario` captura cada exceção separadamente, fornecendo feedback adequado ao usuário. Note como o código fica expressivo e modular.

## Exercícios

### Básico (fixação)
1. Escreva um programa que peça ao usuário dois números e exiba a divisão do primeiro pelo segundo. Use `try/except` para tratar `ZeroDivisionError` e `ValueError`.
2. Crie uma lista com 5 números e peça ao usuário um índice para acessar. Trate `IndexError` se o índice for inválido e `ValueError` se a entrada não for um número inteiro.
3. Simule a abertura de um arquivo: use `try` para abrir um arquivo inexistente e capture `FileNotFoundError`, exibindo uma mensagem amigável. Inclua um bloco `finally` que imprima "Operação finalizada.".

### Intermediário (aplicação)
Desenvolva uma função `converter_para_numero(valor)` que recebe uma string e tenta convertê-la para `int` ou `float`, retornando o número convertido. Se a string não for um número válido, a função deve lançar um `ValueError` com uma mensagem específica. Em seguida, crie um programa que use essa função para somar números digitados pelo usuário em uma única linha separados por espaços (ex.: "10 20 30"). Trate exceções para que o programa não quebre com entradas inválidas.

### Avançado (desafio)
Crie um sistema de reserva de assentos para um teatro. A classe `Teatro` deve ter uma matriz (lista de listas) representando os assentos (ocupado `True`/livre `False`). Regras:
1. O teatro tem 10 fileiras (A-J) e 15 assentos por fileira (1-15).
2. A função `reservar(fileira, assento)` deve levantar exceções personalizadas:
    - `FileiraInvalidaError` se a fileira não for A-J.
    - `AssentoInvalidoError` se o assento não for 1-15.
    - `AssentoOcupadoError` se o assento já estiver reservado.
3. O programa deve oferecer um menu para reservar, cancelar (liberar assento) e visualizar o mapa de assentos (com `[X]` para ocupado e `[ ]` para livre).
4. Utilize tratamento de exceções adequado para todas as operações.

## Projeto Prático: Gerenciador de Contatos com Persistência Segura
Desenvolva uma aplicação de console para gerenciar contatos, com persistência em arquivo JSON, tratamento robusto de exceções e validação de dados.

**Requisitos:**
1. **Modelo de dados:**
    - Cada contato é um dicionário com nome, telefone e email.
    - A lista de contatos é salva em `contatos.json` usando o módulo `json`.
2. **Funcionalidades:**
    - Menu: [1] Adicionar, [2] Listar, [3] Buscar, [4] Remover, [5] Sair.
3. **Tratamento de exceções:**
    - Ao carregar `contatos.json`, trate `FileNotFoundError` (inicia com lista vazia) e `json.JSONDecodeError` (arquivo corrompido, inicia vazio e alerta).
    - Ao salvar, trate `PermissionError` e `OSError`.
    - Valide os dados de entrada com exceções personalizadas:
        - `NomeInvalidoError`: nome vazio ou com menos de 3 caracteres.
        - `TelefoneInvalidoError`: telefone que não contenha apenas dígitos (após limpeza) e que não tenha 10 ou 11 dígitos.
        - `EmailInvalidoError`: e-mail sem `@` ou sem `.` após o `@`.
4. **Implementação:**
    - Crie as classes de exceção em um módulo `excecoes.py`.
    - Crie funções para validar cada campo, levantando as exceções apropriadas.
    - O programa principal (`main.py`) deve usar blocos `try/except` para capturar essas exceções e exibir mensagens amigáveis, sem travar.
    - Use `with` ao manipular o arquivo JSON.
    - Inclua blocos `finally` onde achar necessário (ex.: ao carregar, garantir que a variável de contatos seja inicializada).
5. **Extras:**
    - Adicione uma opção [6] Exportar vCard que gera um arquivo `.vcf` simples. Trate exceções de escrita.
    - Use `logging` para registrar erros inesperados em um arquivo `erros.log`.

**Esqueleto das exceções (`excecoes.py`):**
```python
class NomeInvalidoError(Exception):
    pass

class TelefoneInvalidoError(Exception):
    pass

class EmailInvalidoError(Exception):
    pass
```

Este projeto consolida o tratamento de exceções em um cenário realista, integrando manipulação de arquivos, validação de dados e modularização.

## Resumo
Neste capítulo, você aprendeu que:
- Exceções são eventos que interrompem o fluxo normal do programa; erros de sintaxe impedem a execução.
- O bloco `try/except` captura e trata exceções, permitindo resposta controlada a falhas.
- Capturar exceções específicas (`ValueError`, `FileNotFoundError`, etc.) é melhor do que `except:` genérico.
- O objeto exceção, acessado com `as`, fornece detalhes sobre o erro.
- Os blocos `else` (sem erro) e `finally` (sempre executa) complementam o tratamento.
- A instrução `raise` lança exceções, inclusive de classes personalizadas, para sinalizar violações de regras de negócio.
- Boas práticas incluem não silenciar exceções, usar `with` para recursos, e validar dados cedo.

O tratamento de exceções é um pilar da programação profissional. A partir de agora, seus programas não apenas funcionam no cenário ideal, mas resistem às adversidades do mundo real, mantendo a integridade dos dados e proporcionando uma experiência de usuário muito mais confiável.
