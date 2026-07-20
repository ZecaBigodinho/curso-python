# 07. Coleções (Listas, Tuplas e Dicionários)

## Objetivos
Neste capítulo, você aprenderá a:
- Compreender a necessidade de estruturas de dados para armazenar múltiplos valores.
- Criar e manipular listas: coleções ordenadas e mutáveis.
- Criar e utilizar tuplas: coleções ordenadas e imutáveis.
- Trabalhar com dicionários: estruturas de mapeamento chave-valor.
- Selecionar a coleção mais adequada para cada situação.
- Aplicar métodos e operações comuns de cada tipo de coleção.
- Iterar eficientemente sobre esses contêineres com laços `for`.

## Pré-requisitos
Para acompanhar este capítulo, você deve estar familiarizado com:
- Variáveis e tipos de dados básicos (int, float, str, bool).
- Operadores aritméticos, de comparação e lógicos.
- Estruturas de controle (`if`, `elif`, `else`).
- Laços de repetição (`for`, `while`).
- Definição e chamada de funções.

Caso algum desses tópicos ainda não esteja claro, revise os capítulos anteriores.

## Motivação
Até agora, armazenamos valores em variáveis independentes. Mas o que acontece quando você precisa guardar as notas de 30 alunos? Criar 30 variáveis `nota1`, `nota2`, ... `nota30` é impraticável. Pior ainda se o número de alunos for desconhecido.

As coleções resolvem exatamente esse problema. Elas permitem agrupar múltiplos elementos em uma única estrutura, tratando-os como um conjunto. Python oferece três coleções fundamentais que cobrem a grande maioria das necessidades:
- **Listas**: para armazenar sequências de itens que podem ser alterados (ex.: carrinho de compras).
- **Tuplas**: para agrupar dados que não devem mudar (ex.: coordenadas geográficas).
- **Dicionários**: para associar informações por meio de chaves únicas (ex.: cadastro de clientes por CPF).

Dominar essas estruturas é o que separa um programador iniciante de um desenvolvedor capaz de modelar dados do mundo real. Neste capítulo, vamos explorar cada uma delas a fundo.

## Conteúdo

### Listas (list)
Uma lista é uma coleção ordenada e mutável de itens. Ela pode conter elementos de qualquer tipo, inclusive outras listas. Os itens são acessados por um índice numérico que começa em 0.

#### Criando listas

```python
# Lista vazia
vazia = []

# Lista de números
notas = [7.5, 8.0, 6.5, 9.2]

# Lista mista (strings, int, float)
registro = ["João", 28, 1.75]

# Lista de listas (matriz)
matriz = [[1, 2], [3, 4], [5, 6]]
```

#### Acessando elementos e fatiamento

```python
frutas = ["maçã", "banana", "laranja", "uva"]

print(frutas[0])      # maçã
print(frutas[-1])     # uva (último elemento)
print(frutas[1:3])    # ['banana', 'laranja'] (sub-lista do índice 1 ao 2)
```

!!! tip "Índices negativos"
    Python permite índices negativos para acessar a partir do final. `lista[-1]` é o último elemento, `lista[-2]` é o penúltimo, e assim por diante.

#### Modificando listas (mutabilidade)
Listas são mutáveis: podemos alterar, adicionar e remover itens depois de criadas.

```python
compras = ["pão", "leite"]
compras[0] = "pão integral"   # substitui o primeiro item
compras.append("café")        # adiciona ao final
compras.insert(1, "manteiga") # insere na posição 1
compras.remove("leite")       # remove o valor "leite"
ultimo = compras.pop()        # remove e retorna o último item
print(compras)                # ['pão integral', 'manteiga']
```

**Métodos importantes de listas:**

| Método | Descrição |
| :--- | :--- |
| `append(x)` | Adiciona `x` ao final. |
| `insert(i, x)` | Insere `x` na posição `i`. |
| `remove(x)` | Remove a primeira ocorrência de `x`. |
| `pop(i)` | Remove e retorna o elemento no índice `i` (padrão: último). |
| `sort()` | Ordena a lista in-place. |
| `reverse()` | Inverte a ordem dos elementos in-place. |
| `index(x)` | Retorna o índice da primeira ocorrência de `x`. |
| `count(x)` | Conta quantas vezes `x` aparece. |
| `extend(iteravel)` | Adiciona todos os elementos de um iterável. |

!!! warning "Cuidado com cópias de listas"
    Atribuir uma lista a outra variável (`b = a`) não cria uma cópia, mas sim uma nova referência ao mesmo objeto. Para criar uma cópia independente, use `b = a.copy()` ou `b = list(a)`.

#### Iterando sobre listas

```python
nomes = ["Ana", "Bruno", "Carla"]
for nome in nomes:
    print(f"Olá, {nome}!")
```

### Tuplas (tuple)
Uma tupla é semelhante a uma lista: ordenada, mas **imutável**. Uma vez criada, não pode ser alterada (sem adições, remoções ou modificações de itens). Essa característica é útil para dados que devem permanecer constantes, como coordenadas, configurações ou registros que representam uma entidade fixa.

#### Criando tuplas

```python
# Tupla com parênteses
coordenadas = (10, 20)

# Tupla sem parênteses (empacotamento)
ponto = 3, 4

# Tupla de um único elemento (vírgula obrigatória)
unico = (42,)
```

#### Acessando elementos
Os elementos são acessados por índice, da mesma forma que listas.

```python
cores = ("vermelho", "verde", "azul")
print(cores[0])     # vermelho
print(cores[-1])    # azul
print(cores[0:2])   # ('vermelho', 'verde')
```

#### Por que usar tuplas?
- **Proteção contra alterações acidentais**: a imutabilidade garante que os dados permaneçam íntegros.
- **Desempenho**: tuplas são ligeiramente mais rápidas que listas.
- **Chaves de dicionário**: Podem ser usadas como chaves de dicionários (listas não podem).
- **Semântica**: comunicam a intenção de que a sequência é fixa.

```python
# Exemplo: retorno múltiplo de função (na verdade, uma tupla)
def min_max(lista):
    return min(lista), max(lista)  # retorna uma tupla

resultado = min_max([3, 1, 4, 1, 5])
print(resultado)       # (1, 5)
print(resultado[0])    # 1
```

### Dicionários (dict)
Um dicionário é uma coleção não ordenada (a partir do Python 3.7, mantém a ordem de inserção) de pares **chave-valor**. As chaves devem ser objetos imutáveis (strings, números, tuplas) e são únicas. Os valores podem ser de qualquer tipo e podem se repetir.

#### Criando dicionários

```python
# Dicionário vazio
vazio = {}

# Com chaves e valores
aluno = {
    "nome": "Maria",
    "idade": 21,
    "curso": "Engenharia"
}

# Usando a função dict()
produto = dict(nome="Caneta", preco=2.50, estoque=100)
```

#### Acessando e modificando valores

```python
print(aluno["nome"])        # Maria

# Adicionar ou alterar
aluno["nota"] = 8.5         # nova chave
aluno["idade"] = 22         # altera valor existente

# Remover
del aluno["curso"]
nota = aluno.pop("nota")    # remove e retorna o valor
```

Se tentarmos acessar uma chave inexistente com `[]`, ocorre um `KeyError`. Para evitar isso, use o método `get()`:

```python
telefone = aluno.get("telefone", "Não informado")
print(telefone)  # Não informado
```

#### Métodos úteis

| Método | Descrição |
| :--- | :--- |
| `keys()` | Retorna uma visão das chaves. |
| `values()` | Retorna uma visão dos valores. |
| `items()` | Retorna uma visão de pares (chave, valor). |
| `update(dict)` | Atualiza o dicionário com outro dicionário ou iterável. |
| `clear()` | Remove todos os itens. |

#### Iterando sobre dicionários

```python
for chave, valor in aluno.items():
    print(f"{chave}: {valor}")
```

!!! tip "Use in para verificar se uma chave existe"
    `if "nome" in aluno:` é a forma correta de testar a presença de uma chave.

### Comparativo e escolha da coleção

| Característica | Lista | Tupla | Dicionário |
| :--- | :--- | :--- | :--- |
| Ordenada | Sim | Sim | Sim (3.7+) |
| Mutável | Sim | Não | Sim (valores) |
| Acesso por índice | Sim | Sim | Não (chave) |
| Acesso por chave | Não | Não | Sim |
| Aceita duplicatas | Sim | Sim | Chaves únicas |
| Uso típico | Coleção de itens homogêneos ou variados, que podem sofrer alterações. | Registro fixo, coordenadas, retorno de múltiplos valores. | Cadastros, configurações, contadores. |

- Use **lista** quando precisar de uma sequência dinâmica e mutável.
- Use **tupla** quando os dados não devem ser alterados ou quando precisar de chave de dicionário.
- Use **dicionário** quando a informação for melhor acessada por um identificador (nome, CPF, código) do que por posição numérica.

### Boas práticas
- Nomeie listas no plural: `nomes`, `produtos`, `notas`.
- Para dicionários, use chaves significativas e constantes para evitar erros de digitação.
- Evite modificar uma lista enquanto itera sobre ela; se necessário, itere sobre uma cópia.
- Prefira tuplas para estruturas fixas; a imutabilidade ajuda a prevenir bugs.
- Aproveite a função `enumerate()` para obter índice e valor ao percorrer listas.

```python
for i, nome in enumerate(nomes):
    print(f"{i}: {nome}")
```

## Exemplos

??? example "Exemplo 1: Lista de tarefas"
    === "Código"
        ```python
        # Simulação de uma lista de tarefas
        tarefas = ["Estudar Python", "Fazer exercícios", "Ler documentação"]

        # Adiciona nova tarefa
        tarefas.append("Revisar anotações")

        # Marca a primeira tarefa como concluída (remove)
        concluida = tarefas.pop(0)
        print(f"Tarefa concluída: {concluida}")

        # Exibe as tarefas restantes numeradas
        print("\nTarefas pendentes:")
        for i, tarefa in enumerate(tarefas, 1):
            print(f"{i}. {tarefa}")
        ```

    === "Resultado"
        ```text
        Tarefa concluída: Estudar Python

        Tarefas pendentes:
        1. Fazer exercícios
        2. Ler documentação
        3. Revisar anotações
        ```

    === "Explicação"
        Uma lista gerencia dinamicamente as tarefas. `append` adiciona ao final, `pop(0)` remove do início (FIFO simples). `enumerate` com argumento 1 inicia a numeração a partir de 1, tornando a saída mais amigável.

??? example "Exemplo 2: Tupla como registro imutável"
    === "Código"
        ```python
        # Representa um ponto geográfico (latitude, longitude)
        ponto = (-23.5505, -46.6333)  # São Paulo

        # Desempacotamento de tupla
        lat, lon = ponto
        print(f"Latitude: {lat}, Longitude: {lon}")

        # Tentativa de alteração gera erro (descomente para testar)
        # ponto[0] = 0   # TypeError: 'tuple' object does not support item assignment

        # Tupla como chave de dicionário (lista não seria permitida)
        cidades = {
            ponto: "São Paulo",
            (-22.9068, -43.1729): "Rio de Janeiro"
        }
        print(cidades[ponto])  # São Paulo
        ```

    === "Resultado"
        ```text
        Latitude: -23.5505, Longitude: -46.6333
        São Paulo
        ```

    === "Explicação"
        A tupla `ponto` armazena coordenadas fixas. O desempacotamento permite obter cada valor diretamente. Como tuplas são imutáveis e hasháveis, podem ser usadas como chaves de dicionário, algo impossível com listas. Isso é útil para mapear coordenadas a nomes de cidades.

??? example "Exemplo 3: Dicionário de estoque"
    === "Código"
        ```python
        # Estoque de produtos
        estoque = {
            "caneta": 50,
            "caderno": 30,
            "borracha": 100
        }

        # Venda de 10 canetas
        produto = "caneta"
        if produto in estoque and estoque[produto] >= 10:
            estoque[produto] -= 10
            print(f"Venda realizada. Estoque de {produto}: {estoque[produto]}")
        else:
            print("Produto indisponível ou quantidade insuficiente.")

        # Relatório completo
        print("\nRelatório de estoque:")
        for item, qtd in estoque.items():
            print(f"{item.capitalize()}: {qtd} unidades")
        ```

    === "Resultado"
        ```text
        Venda realizada. Estoque de caneta: 40

        Relatório de estoque:
        Caneta: 40 unidades
        Caderno: 30 unidades
        Borracha: 100 unidades
        ```

    === "Explicação"
        O dicionário mapeia cada produto à sua quantidade. A condicional verifica existência e quantidade antes de deduzir. O método `items()` permite iterar sobre chaves e valores simultaneamente, gerando um relatório legível. `capitalize()` formata a primeira letra em maiúscula.

## Exercícios

### Básico (fixação)
- Crie uma lista com os nomes de 5 amigos. Exiba o primeiro e o último nome da lista. Em seguida, adicione um novo nome ao final e remova o segundo nome. Exiba a lista final.
- Crie uma tupla com os meses do ano. Tente alterar o mês de "Janeiro" para "janeiro" e observe o erro. Use um laço `for` para imprimir cada mês.
- Construa um dicionário com informações de um livro: título, autor, ano de publicação e número de páginas. Acesse e imprima o autor. Adicione uma chave "gênero" com valor "Ficção Científica" e remova a chave "número de páginas". Exiba o dicionário resultante.

### Intermediário (aplicação)
Você é responsável por controlar as notas de uma turma. Crie uma lista de listas onde cada sublista contém o nome do aluno (string) e suas três notas (floats). Exemplo: `[["João", 7.0, 8.5, 9.0], ["Maria", 6.0, 7.0, 8.0]]`. Para cada aluno, calcule a média e exiba: "Nome: Média X.X - Aprovado" (média >= 7.0) ou "Reprovado". Armazene os resultados em um dicionário no formato `{nome: media}`.

### Avançado (desafio)
Implemente um sistema simples de agenda telefônica usando um dicionário. O programa deve oferecer um menu:
1. **Adicionar contato**: solicita nome e telefone; se o nome já existir, pergunta se deseja sobrescrever.
2. **Buscar contato**: solicita nome e exibe o telefone, ou "Contato não encontrado".
3. **Listar contatos**: exibe todos os contatos em ordem alfabética.
4. **Sair**.

Utilize funções para cada operação. Armazene os contatos em um dicionário aninhado onde o nome é a chave e o valor é outro dicionário contendo "telefone" e "data_criacao" (use `datetime`). A data de criação deve ser uma tupla com dia, mês e ano, para ser imutável. Trate entradas inválidas e mantenha o programa em execução até o usuário escolher sair.

## Projeto Prático: Gerenciador de Alunos e Notas
Desenvolva um programa que gerencie uma turma de alunos, suas notas e estatísticas, utilizando listas, tuplas e dicionários.

**Requisitos:**
1. O programa armazena os alunos em uma lista chamada `turma`. Cada elemento da lista é um dicionário representando um aluno, com as chaves:
    - `"nome"` (string)
    - `"matricula"` (int)
    - `"notas"` (lista de floats)
    - `"dados_pessoais"` (tupla com data de nascimento no formato `(dia, mês, ano)`)
2. Ofereça um menu com opções:
    - **[1] Cadastrar aluno**: solicita nome, matrícula, data de nascimento (3 inteiros) e 3 notas. Cria o dicionário correspondente e adiciona à lista `turma`.
    - **[2] Exibir médias**: para cada aluno, calcula a média das notas e exibe nome, matrícula e média formatada. Ao final, exiba a média geral da turma.
    - **[3] Buscar por matrícula**: solicita matrícula e exibe todos os dados do aluno (nome, notas, data de nascimento). Se não encontrado, exiba mensagem apropriada.
    - **[4] Relatório de aprovação**: exibe quantos alunos foram aprovados (média >= 7), quantos em recuperação (5 <= média < 7) e quantos reprovados. Use um dicionário para agrupar essas contagens.
    - **[5] Sair**.
3. Implemente cada funcionalidade como uma função separada. Use `if __name__ == "__main__"` para executar o menu.

**Exemplo de execução:**
```text
--- Menu ---
1. Cadastrar aluno
2. Exibir médias
3. Buscar por matrícula
4. Relatório de aprovação
5. Sair
Escolha: 1
Nome: Ana
Matrícula: 123
Data nascimento (DD MM AAAA): 15 08 2001
Nota 1: 8
Nota 2: 7.5
Nota 3: 9
Aluno cadastrado.
```

Este projeto solidifica a manipulação de listas (turma), dicionários (dados do aluno) e tuplas (data de nascimento imutável), além de integrar condicionais, laços e funções.

## Resumo
Neste capítulo, você aprendeu que:
- **Listas** são coleções ordenadas e mutáveis, ideais para sequências dinâmicas.
- **Tuplas** são ordenadas e imutáveis, perfeitas para registros fixos e chaves de dicionários.
- **Dicionários** mapeiam chaves a valores, permitindo acesso rápido por identificadores.
- Cada estrutura tem seus métodos específicos (`append`, `pop`, `items`, `get`, etc.) e pode ser iterada com `for`.
- A escolha entre elas depende da necessidade de mutabilidade, da forma de acesso (índice vs. chave) e do significado dos dados.

Com essas ferramentas, você pode modelar uma vasta gama de problemas do mundo real. Seus programas agora são capazes de armazenar e processar dados de forma estruturada e eficiente.
