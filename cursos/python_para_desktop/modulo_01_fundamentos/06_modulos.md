# 06. Módulos e Bibliotecas

## Objetivos
Neste capítulo, você aprenderá a:
- Compreender o conceito de módulo e biblioteca em Python.
- Importar módulos embutidos da biblioteca padrão (`math`, `random`, `datetime`, entre outros).
- Utilizar diferentes formas de importação: `import`, `from ... import` e `import ... as`.
- Criar seus próprios módulos e organizar funções em arquivos separados.
- Entender o funcionamento da variável `__name__` e a proteção de código com `if __name__ == "__main__"`.
- Explorar o ecossistema de bibliotecas externas e o gerenciador de pacotes `pip`.

## Pré-requisitos
Para acompanhar este capítulo, é necessário que você tenha domínio sobre:
- Definição e chamada de funções (`def`, `return`).
- Tipos de dados básicos e coleções (listas, dicionários).
- Estruturas de controle (`if`, `for`, `while`).
- Manipulação de arquivos (opcional, mas útil para criar módulos).

Se algum desses tópicos não estiver claro, revise os capítulos anteriores.

## Motivação
Você já percebeu que, ao longo dos capítulos anteriores, utilizamos algumas ferramentas que não definimos diretamente? Por exemplo, `print()`, `input()`, `len()`, `range()`. Essas são funções embutidas (built-in), disponíveis automaticamente. Mas o poder do Python vai muito além delas: a linguagem oferece uma vasta biblioteca padrão com módulos prontos para matemática, datas, aleatoriedade, arquivos, internet e muito mais.

Imagine que você precise calcular a raiz quadrada, gerar um número aleatório ou saber a data e hora atual. Você poderia escrever tudo do zero, mas isso seria reinventar a roda — e provavelmente de forma menos eficiente e mais propensa a erros. Os módulos existem justamente para encapsular funcionalidades reutilizáveis, escritas por especialistas e testadas pela comunidade.

Além de consumir módulos existentes, você aprenderá a criar seus próprios módulos, transformando seus scripts em bibliotecas reutilizáveis. Essa é a chave para projetos Python organizados, escaláveis e profissionais.

## Conteúdo

### O que é um módulo?
Um módulo em Python é simplesmente um arquivo com extensão `.py` contendo definições e instruções. O nome do arquivo (sem a extensão) é o nome do módulo. Qualquer arquivo Python que você escreve já é um módulo em potencial.

**Biblioteca** é um termo mais amplo: pode se referir a um conjunto de módulos relacionados. A *biblioteca padrão* do Python é o conjunto de módulos que acompanham a instalação da linguagem.

### Importando módulos
Para acessar funções, classes e variáveis definidas em outro módulo, usamos a instrução `import`.

```python
import math
```

Isso carrega o módulo `math` e torna seu conteúdo acessível através da notação de ponto: `math.funcao()`.

```python
import math
raiz = math.sqrt(25)
print(raiz)  # 5.0
```

#### Formas de importação

| Sintaxe | Descrição |
| :--- | :--- |
| `import modulo` | Importa o módulo inteiro. Acesso: `modulo.item`. |
| `from modulo import item` | Importa apenas o item especificado. Acesso direto: `item`. |
| `from modulo import *` | Importa todos os itens públicos. Não recomendado (polui o namespace). |
| `import modulo as apelido` | Importa o módulo com um nome alternativo. |
| `from modulo import item as ap` | Importa um item com apelido. |

```python
# Exemplos de importação
from math import pi, cos
print(pi)               # 3.141592653589793
print(cos(0))           # 1.0

import datetime as dt
hoje = dt.date.today()
print(hoje)             # 2025-07-20
```

!!! tip "Prefira importar módulos inteiros ou itens específicos"
    `from modulo import *` é desencorajado porque pode sobrescrever nomes existentes e dificulta saber de onde cada função veio. Utilize com moderação, apenas em módulos projetados para isso (ex.: `from tkinter import *` em programas GUI simples).

### Módulos embutidos essenciais
Vamos explorar três módulos poderosos da biblioteca padrão: `math`, `random` e `datetime`.

#### Módulo math
Oferece funções matemáticas e constantes.

```python
import math

print(math.pi)           # 3.141592653589793
print(math.e)            # 2.718281828459045
print(math.ceil(4.2))    # 5 (arredonda para cima)
print(math.floor(4.9))   # 4 (arredonda para baixo)
print(math.gcd(12, 8))   # 4 (máximo divisor comum)
print(math.log(10))      # logaritmo natural
```

#### Módulo random
Geração de números pseudoaleatórios.

```python
import random

# Número float aleatório entre 0 e 1
print(random.random())  # Ex: 0.724...

# Inteiro aleatório entre 1 e 10 (inclusive)
print(random.randint(1, 10))

# Escolha aleatória de uma lista
cores = ['azul', 'verde', 'amarelo']
print(random.choice(cores))

# Embaralhar uma lista (modifica a lista original)
numeros = [1, 2, 3, 4, 5]
random.shuffle(numeros)
print(numeros)
```

!!! warning "Resultados aleatórios"
    Os números gerados não são verdadeiramente aleatórios, mas sim pseudoaleatórios. A semente (seed) pode ser fixada com `random.seed(42)` para obter resultados reproduzíveis — útil para testes.

#### Módulo datetime
Manipulação de datas e horas.

```python
from datetime import date, datetime, timedelta

# Data atual
hoje = date.today()
print(hoje)  # 2025-07-20

# Data e hora específicas
agora = datetime.now()
print(agora.strftime("%d/%m/%Y %H:%M:%S"))  # 20/07/2025 15:30:00

# Operações com datas: diferença
data_passada = date(2025, 1, 1)
diferenca = hoje - data_passada
print(diferenca.days)  # número de dias

# Adicionar dias
amanha = hoje + timedelta(days=1)
print(amanha)
```

### Criando seu próprio módulo
Qualquer arquivo `.py` pode ser importado como módulo. Suponha um arquivo `utilidades.py`:

```python
# utilidades.py
def saudacao(nome):
    return f"Olá, {nome}!"

def fatorial(n):
    if n == 0:
        return 1
    return n * fatorial(n-1)

PI = 3.14
```

Em outro arquivo no mesmo diretório, podemos importá-lo:

```python
# programa.py
import utilidades

print(utilidades.saudacao("Maria"))
print(utilidades.fatorial(5))
print(utilidades.PI)
```

!!! note "O Python busca módulos em diretórios específicos"
    Para importar um módulo, o Python procura no diretório atual, nos diretórios da variável de ambiente PYTHONPATH e nos caminhos padrão. Você pode ver os locais com `import sys; print(sys.path)`. Para módulos fora desses locais, manipule `sys.path` ou use pacotes.

### A variável \_\_name\_\_ e o bloco if \_\_name\_\_ == "\_\_main\_\_"
Quando um módulo é executado diretamente, Python define sua variável especial `__name__` como `__main__`. Quando ele é importado, `__name__` recebe o nome do arquivo (sem `.py`). Isso permite que um mesmo arquivo funcione tanto como script quanto como módulo.

```python
# meu_modulo.py
def funcao():
    print("Função executada")

if __name__ == "__main__":
    print("Executando como script principal")
    funcao()
else:
    print(f"Importado como módulo: {__name__}")
```

Se rodarmos `python meu_modulo.py`, veremos "Executando como script principal". Se importarmos em outro lugar (`import meu_modulo`), veremos a mensagem de importação e a função não será executada automaticamente.

!!! tip "Sempre use essa proteção em módulos"
    Isso evita que código de teste ou demonstração seja executado quando seu módulo é importado. Coloque a lógica principal do script dentro desse bloco.

### Explorando a biblioteca padrão
A biblioteca padrão do Python é riquíssima. Alguns módulos que você pode explorar:
- `os` e `sys`: interação com sistema operacional.
- `json`, `csv`: leitura e escrita de dados estruturados.
- `re`: expressões regulares.
- `time`: funções relacionadas a tempo.
- `turtle`: gráficos simples para aprendizado.

Para conhecer o que cada módulo oferece, use `help(nome_do_modulo)` no interpretador interativo ou consulte a documentação oficial.

### Bibliotecas externas e o pip
Além da biblioteca padrão, existe um imenso ecossistema de bibliotecas de terceiros disponível no PyPI (Python Package Index). O gerenciador de pacotes `pip` permite instalar essas bibliotecas com facilidade:

```bash
pip install nome_da_biblioteca
```

Exemplos de bibliotecas populares:
- `requests`: realizar requisições HTTP.
- `pandas`: análise de dados.
- `flask`: desenvolvimento web.
- `pillow`: manipulação de imagens.
- `pygame`: desenvolvimento de jogos.

Para usar uma biblioteca externa, instale-a com pip e importe-a como faria com qualquer módulo.

!!! warning "Ambientes virtuais"
    Ao trabalhar em projetos, é altamente recomendável utilizar ambientes virtuais (`python -m venv venv`) para isolar dependências. Isso evita conflitos entre versões de bibliotecas.

### Boas práticas
- Mantenha seus módulos focados em um único propósito.
- Use nomes de arquivo descritivos e em snake_case.
- Documente o módulo e suas funções com docstrings.
- Utilize `if __name__ == "__main__"` para código de teste.
- Não dependa de efeitos colaterais na importação; evite executar código no escopo global além de definições.
- Agrupe módulos relacionados em pacotes (diretórios com `__init__.py`).

## Exemplos

??? example "Exemplo 1: Gerador de números da sorte"
    === "Código"
        ```python
        import random

        def gerar_mega_sena():
            """Gera 6 números aleatórios entre 1 e 60, sem repetição."""
            numeros = random.sample(range(1, 61), 6)
            return sorted(numeros)

        # Programa principal
        if __name__ == "__main__":
            print("Números da Mega Sena:", gerar_mega_sena())
        ```

    === "Resultado"
        ```text
        Números da Mega Sena: [7, 15, 23, 34, 48, 55]
        ```

    === "Explicação"
        Utilizamos `random.sample()` para obter números únicos de uma população, e `sorted()` para ordená-los. O bloco `if __name__ == "__main__"` permite testar o módulo diretamente, mas se importado, a função ficará disponível sem executar automaticamente.

??? example "Exemplo 2: Registro de eventos com timestamp"
    === "Código"
        ```python
        from datetime import datetime

        def registrar_evento(mensagem):
            """Registra um evento com data e hora."""
            agora = datetime.now()
            timestamp = agora.strftime("%Y-%m-%d %H:%M:%S")
            return f"[{timestamp}] {mensagem}"

        # Testando
        print(registrar_evento("Sistema iniciado."))
        print(registrar_evento("Usuário fez login."))
        ```

    === "Resultado"
        ```text
        [2025-07-20 14:35:22] Sistema iniciado.
        [2025-07-20 14:35:22] Usuário fez login.
        ```

    === "Explicação"
        A função obtém a data/hora atual com `datetime.now()` e formata como string legível usando `strftime`. Esse padrão é útil para logs em aplicações desktop.

??? example "Exemplo 3: Módulo próprio de validação"
    === "Código"
        **Arquivo `validadores.py`:**
        ```python
        # validadores.py
        import re

        def email_valido(email):
            """Verifica se o e-mail possui formato básico válido."""
            padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            return re.match(padrao, email) is not None

        def cpf_tamanho_ok(cpf):
            """Verifica se o CPF possui 11 dígitos após limpeza."""
            numeros = ''.join(filter(str.isdigit, cpf))
            return len(numeros) == 11
        ```

        **Arquivo `cadastro.py` que importa:**
        ```python
        # cadastro.py
        from validadores import email_valido, cpf_tamanho_ok

        email = input("E-mail: ")
        cpf = input("CPF: ")

        if email_valido(email) and cpf_tamanho_ok(cpf):
            print("Dados válidos! Cadastro realizado.")
        else:
            print("Dados inválidos. Verifique e tente novamente.")
        ```

    === "Resultado"
        Supondo entradas válidas:
        ```text
        E-mail: joao@exemplo.com
        CPF: 123.456.789-09
        Dados válidos! Cadastro realizado.
        ```

    === "Explicação"
        Criamos um módulo `validadores.py` com funções específicas. O programa principal importa apenas as funções necessárias. Essa separação mantém o código organizado e as validações reaproveitáveis em diversos projetos.

## Exercícios

### Básico (fixação)
- Importe o módulo `math` e calcule a raiz quadrada de 144 e o seno de 30 graus (converta para radianos com `math.radians`).
- Use `random.randint` para simular o lançamento de um dado de 6 faces por 5 vezes, exibindo os resultados.
- Com o módulo `datetime`, exiba a data e hora atuais no formato "DD/MM/AAAA HH:MM".

### Intermediário (aplicação)
Crie um módulo chamado `conversores.py` contendo as funções:
- `kg_para_libras(kg)` que retorna `kg * 2.20462`.
- `libras_para_kg(lb)` que retorna `lb / 2.20462`.

Em um programa separado, importe esse módulo e crie um conversor de peso que pergunta ao usuário o valor e a unidade de origem, exibindo o resultado convertido. Utilize `if __name__ == "__main__"` no programa principal para testes.

### Avançado (desafio)
Desenvolva um módulo `estatisticas.py` que contenha as funções:
- `media(lista)`: retorna a média aritmética.
- `mediana(lista)`: retorna a mediana (valor central após ordenação).
- `moda(lista)`: retorna o(s) valor(es) mais frequente(s) (dica: use `collections.Counter` do módulo embutido `collections`).

Em seguida, crie um script que gera 1000 números aleatórios entre 1 e 100, e utilize seu módulo para calcular e exibir a média, mediana e moda desses números. Proteja o script com `if __name__ == "__main__"`.

## Projeto Prático: Diário de Bordo com Módulos
Crie uma aplicação de diário de bordo que salva entradas em um arquivo de texto, com registro de data/hora, utilizando módulos personalizados.

**Estrutura do projeto:**
- `diario.py` – módulo principal com a lógica de entrada e exibição.
- `registro.py` – módulo que contém funções para salvar e ler entradas do diário.
- `utils.py` – módulo com funções utilitárias, como obter timestamp formatado.

**Requisitos:**
1. **Módulo `utils.py`:**
    - Função `obter_timestamp()` que retorna string com data e hora atual no formato `[AAAA-MM-DD HH:MM:SS]`.
2. **Módulo `registro.py`:**
    - Função `adicionar_entrada(arquivo, texto)` que abre o arquivo em modo append, escreve o timestamp seguido do texto e pula linha.
    - Função `ler_entradas(arquivo)` que lê e exibe todas as entradas do arquivo. Se o arquivo não existir, exibe "Diário vazio.".
3. **Módulo `diario.py`:**
    - Apresenta um menu: [1] Nova entrada, [2] Ver diário, [3] Sair.
    - Usa as funções dos outros módulos.
    - O nome do arquivo pode ser fixo (`diario.txt`).
    - Deve rodar em laço até o usuário sair.
    - Utilize `if __name__ == "__main__"` para iniciar o menu.

**Desafio extra:** Permita que o usuário escolha o nome do arquivo ao iniciar o programa, passando-o como argumento para as funções.

Esse projeto consolida a criação e uso de módulos próprios, importação, organização de código e interação com arquivos.

## Resumo
Neste capítulo, você aprendeu que:
- Módulos são arquivos `.py` que contêm código reutilizável; bibliotecas são conjuntos de módulos.
- A biblioteca padrão do Python fornece muitos módulos embutidos (ex.: `math`, `random`, `datetime`).
- A importação pode ser feita de várias formas: `import modulo`, `from modulo import item`, e com apelidos (`as`).
- Você pode criar seus próprios módulos e importá-los em outros scripts.
- A variável `__name__` permite distinguir se o módulo está sendo executado como script principal ou importado.
- O ecossistema Python conta com milhares de bibliotecas externas, instaláveis via `pip`.
- Boas práticas incluem organização, documentação e uso do bloco `if __name__ == "__main__"`.

Com módulos, você transcende scripts monolíticos e constrói sistemas modulares, escaláveis e fáceis de manter. A reutilização de código dá um salto de produtividade.
