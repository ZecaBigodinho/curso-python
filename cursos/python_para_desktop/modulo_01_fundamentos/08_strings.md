# 08. Manipulação de Strings

## Objetivos
Neste capítulo, você aprenderá a:
- Compreender que strings são sequências imutáveis de caracteres.
- Acessar caracteres individuais e fatiar strings para extrair trechos.
- Concatenar, repetir e interpolar strings de forma eficiente.
- Utilizar os principais métodos de string para limpar, modificar e inspecionar textos.
- Realizar buscas e substituições dentro de strings.
- Aplicar formatação moderna com f-strings para criar saídas profissionais.
- Validar padrões simples, como formatos de CPF, e-mail ou telefone, usando métodos nativos.

## Pré-requisitos
Antes de prosseguir, certifique-se de que você domina:
- Tipos de dados básicos (int, float, str, bool).
- Operadores aritméticos, de comparação e lógicos.
- Estruturas condicionais e laços de repetição.
- Listas e tuplas (conceitos básicos de indexação e iteração).

Esses fundamentos garantirão um aproveitamento completo dos tópicos abordados.

## Motivação
Em aplicações desktop, o processamento de texto é onipresente: ler dados de formulários, exibir relatórios, salvar configurações em arquivos, validar entradas do usuário, gerar e-mails automáticos. Saber manipular strings com destreza é tão essencial quanto calcular números. Um nome mal formatado, um CPF com pontuação incorreta ou um arquivo CSV com campos desalinhados podem comprometer toda uma aplicação.

Felizmente, Python oferece um conjunto riquíssimo de ferramentas para trabalhar com texto. Você aprenderá a fatiar, formatar, limpar e validar strings de maneira expressiva e eficiente. Ao final deste capítulo, você será capaz de domar até mesmo os dados textuais mais bagunçados e transformá-los em informação útil e confiável.

## Conteúdo

### Strings como sequências
Em Python, uma string é uma sequência ordenada e **imutável** de caracteres Unicode. Isso significa que cada caractere ocupa uma posição (índice) e que, uma vez criada, a string não pode ser alterada — qualquer operação que pareça modificar uma string na verdade gera uma nova.

```python
texto = "Python"
print(texto[0])   # 'P'
print(texto[-1])  # 'n'
print(len(texto)) # 6
```

### Indexação e fatiamento
Podemos acessar caracteres individuais com índices (iniciando em 0) e extrair substrings com a notação de fatiamento `[inicio:fim:passo]`.

```python
frase = "Aprendendo Python"
print(frase[0:10])    # 'Aprendendo' (caracteres 0 a 9)
print(frase[11:])     # 'Python' (do índice 11 até o final)
print(frase[:10])     # 'Aprendendo' (do início ao 9)
print(frase[::2])     # 'Arned yhn' (a cada 2 caracteres)
print(frase[::-1])    # 'nohtyP odnednerpA' (string invertida)
```

!!! note "Fatiamento não gera erro com índices fora do intervalo"
    Ao contrário da indexação direta (`texto[100]` gera `IndexError`), o fatiamento retorna uma string vazia se os limites estiverem fora do tamanho, o que é muito conveniente.

### Concatenação e repetição
- **Concatenação**: `+` junta duas strings.
- **Repetição**: `*` repete uma string várias vezes.

```python
nome = "João"
sobrenome = "Silva"
nome_completo = nome + " " + sobrenome  # 'João Silva'
linha = "-" * 30  # '------------------------------'
```

!!! warning "Evite concatenar muitas strings em laços"
    Como strings são imutáveis, cada concatenação cria uma nova string, o que pode ser ineficiente. Prefira usar `''.join(lista)` para construir strings longas.

### Métodos de string
Python oferece mais de 40 métodos para objetos do tipo `str`. Vamos agrupar os mais úteis por categoria.

#### Transformação de maiúsculas/minúsculas
- `upper()`: todas maiúsculas.
- `lower()`: todas minúsculas.
- `capitalize()`: primeira letra maiúscula, resto minúsculo.
- `title()`: primeira letra de cada palavra maiúscula.
- `swapcase()`: inverte maiúsculas/minúsculas.

```python
s = "pYthon é INCRÍVEL"
print(s.lower())       # 'python é incrível'
print(s.title())       # 'Python É Incrível'
```

#### Remoção de espaços
- `strip()`: remove espaços do início e fim.
- `lstrip()`: remove do início.
- `rstrip()`: remove do fim.

```python
entrada = "   Maria   "
print(entrada.strip())  # 'Maria'
```

#### Substituição
- `replace(antigo, novo, contagem)`: substitui trechos.

```python
frase = "banana, maçã, banana"
print(frase.replace("banana", "laranja"))  # 'laranja, maçã, laranja'
print(frase.replace("banana", "laranja", 1))  # 'laranja, maçã, banana'
```

#### Divisão e junção
- `split(separador)`: divide a string em uma lista de substrings.
- `join(iteravel)`: junta elementos de um iterável em uma string, usando a string original como separador.

```python
dados = "João,25,SP"
partes = dados.split(",")
print(partes)  # ['João', '25', 'SP']

lista = ["Python", "é", "legal"]
frase = " ".join(lista)
print(frase)  # 'Python é legal'
```

!!! tip "O poder do join"
    `join` é extremamente rápido e deve ser usado sempre que você precisar combinar muitas strings.

#### Busca e contagem
- `find(sub)`: retorna o índice da primeira ocorrência de `sub`, ou `-1` se não encontrado.
- `rfind(sub)`: busca da direita para a esquerda.
- `index(sub)`: similar ao `find`, mas gera `ValueError` se não encontrar.
- `count(sub)`: conta quantas vezes `sub` aparece.
- `startswith(prefixo)` e `endswith(sufixo)`: verificam início/fim da string.

```python
texto = "abacaxi"
print(texto.find("ca"))      # 3
print(texto.count("a"))      # 3
print(texto.startswith("aba")) # True
print(texto.endswith("xi"))   # True
```

#### Validação de conteúdo
Estes métodos retornam `True` ou `False`, sendo úteis para validar dados de entrada:
- `isalpha()`: todos os caracteres são letras.
- `isdigit()`: todos os caracteres são dígitos.
- `isalnum()`: todos são letras ou dígitos.
- `isspace()`: só espaços em branco.
- `islower()` / `isupper()`: todas minúsculas/maiúsculas.
- `istitle()`: formato título.

```python
print("123".isdigit())      # True
print("abc".isalpha())      # True
print("abc123".isalnum())   # True
print("   ".isspace())      # True
```

!!! warning "Limitações dos métodos is"
    `isalpha()` retorna False se houver acentos? Não, em Python 3, caracteres acentuados são considerados letras. Teste `"café".isalpha()` → `True`. Isso é bom para português. Porém, `"123".isdigit()` é True mas `"12.5".isdigit()` é False por causa do ponto.

### Formatação de strings
Formatar strings é inserir valores de variáveis dentro de um texto de maneira controlada.

#### f-strings (Python 3.6+)
A forma moderna, legível e eficiente:

```python
nome = "Ana"
idade = 28
print(f"{nome} tem {idade} anos e no próximo ano fará {idade + 1}.")
```

É possível formatar números:

```python
preco = 19.999
print(f"Preço: R$ {preco:.2f}")  # 'Preço: R$ 19.99'
percentual = 0.255
print(f"Desconto: {percentual:.1%}")  # 'Desconto: 25.5%'
```

Alinhamento e preenchimento:

```python
produto = "Café"
preco = 12.5
print(f"{produto:<10} R$ {preco:>6.2f}")  # alinhado à esquerda (10) e à direita (6)
```

#### Método format()
Método tradicional, ainda muito usado:

```python
print("{} tem {} anos".format(nome, idade))
print("{nome} tem {idade} anos".format(nome="João", idade=25))
```

#### Formatação com % (estilo antigo)
Menos recomendado, mas você pode encontrar em código legado:

```python
print("%s tem %d anos" % (nome, idade))
```

Hoje, prefira **f-strings** por sua clareza e desempenho.

### Validação de padrões com métodos nativos
Podemos combinar métodos para validar formatos comuns sem usar regex.

Exemplo: verificar se uma string contém exatamente 11 dígitos (CPF sem pontuação):

```python
def cpf_valido(cpf):
    return cpf.isdigit() and len(cpf) == 11
```

Ou validar um e-mail simplificado (contém `@` e `.` após `@`):

```python
def email_valido(email):
    if "@" in email:
        partes = email.split("@")
        return len(partes) == 2 and "." in partes[1]
    return False
```

Essas validações são ingênuas, mas funcionam como ponto de partida. Para produção, utilize `re` ou bibliotecas especializadas.

### Imutabilidade e boas práticas
- Strings são imutáveis: qualquer método retorna uma **nova** string; a original permanece inalterada.
- Use `join` para concatenar múltiplas strings, evitando `+` em laços.
- Aproveite métodos encadeados: `texto.strip().lower().replace(" ", "_")`.
- Documente padrões de validação com comentários.
- Para processamento de arquivos grandes, considere iterar linha a linha sem carregar tudo na memória.

## Exemplos

??? example "Exemplo 1: Limpeza de dados de formulário"
    === "Código"
        ```python
        # Simula entrada de usuário com espaços e maiúsculas inconsistentes
        nome = "  MARIA DA SILVA  "
        email = "Maria@Exemplo.Com"

        # Limpeza e padronização
        nome_limpo = nome.strip().title()  # 'Maria Da Silva'
        email_limpo = email.strip().lower()  # 'maria@exemplo.com'

        print(f"Nome formatado: '{nome_limpo}'")
        print(f"E-mail normalizado: '{email_limpo}'")
        ```

    === "Resultado"
        ```text
        Nome formatado: 'Maria Da Silva'
        E-mail normalizado: 'maria@exemplo.com'
        ```

    === "Explicação"
        `strip()` remove espaços extras das bordas. `title()` capitaliza cada palavra, embora "da" também vire maiúscula — um tratamento mais fino exigiria lista de preposições. `lower()` uniformiza o e-mail para minúsculas, prática comum em cadastros.

??? example "Exemplo 2: Análise e formatação de dados brutos"
    === "Código"
        ```python
        # Dados brutos de um arquivo CSV simulado
        linha = "123,João,joao@exemplo.com, 1500.50"
        partes = linha.split(",")

        # Extrai e converte campos
        id_cliente = int(partes[0])
        nome = partes[1].strip()
        email = partes[2].strip()
        saldo = float(partes[3].strip())

        # Exibe relatório formatado
        print(f"ID: {id_cliente:04d}")
        print(f"Nome: {nome}")
        print(f"E-mail: {email}")
        print(f"Saldo: R$ {saldo:,.2f}")  # vírgulas de milhar
        ```

    === "Resultado"
        ```text
        ID: 0123
        Nome: João
        E-mail: joao@exemplo.com
        Saldo: R$ 1,500.50
        ```

    === "Explicação"
        `split(",")` quebra a linha em campos. Cada campo é limpo com `strip()` e convertido ao tipo adequado. Na formatação, `04d` preenche com zeros à esquerda, e `:,.2f` insere separadores de milhar e duas casas decimais, tudo com f-string.

??? example "Exemplo 3: Validação de senha com métodos"
    === "Código"
        ```python
        def validar_senha(senha):
            """Valida se a senha atende critérios mínimos."""
            problemas = []
            if len(senha) < 8:
                problemas.append("Mínimo 8 caracteres")
            if not any(c.isupper() for c in senha):
                problemas.append("Ao menos uma maiúscula")
            if not any(c.isdigit() for c in senha):
                problemas.append("Ao menos um dígito")
            if senha.isalnum():
                problemas.append("Deve conter caractere especial")
            return problemas

        # Teste
        senhas = ["abc", "ABCDEFGH", "abc12345", "Abc@1234"]
        for s in senhas:
            erros = validar_senha(s)
            print(f"Senha '{s}': {'Válida' if not erros else erros}")
        ```

    === "Resultado"
        ```text
        Senha 'abc': ['Mínimo 8 caracteres', 'Ao menos uma maiúscula', 'Ao menos um dígito', 'Deve conter caractere especial']
        Senha 'ABCDEFGH': ['Ao menos um dígito', 'Deve conter caractere especial']
        Senha 'abc12345': ['Ao menos uma maiúscula', 'Deve conter caractere especial']
        Senha 'Abc@1234': Válida
        ```

    === "Explicação"
        A função `validar_senha` utiliza métodos `isupper()`, `isdigit()`, `isalnum()` e a função embutida `any()` para verificar a presença de tipos de caracteres. Os problemas são coletados em uma lista e exibidos. Note que `isalnum()` é falso se houver caractere especial, então exigimos que a senha não seja alfanumérica pura. A lógica é simples e não requer regex.

## Exercícios

### Básico (fixação)
- Peça ao usuário seu nome completo e exiba:
    - O nome em maiúsculas.
    - O nome em minúsculas.
    - O número de caracteres (sem espaços).
    - O primeiro nome (dica: use `split`).
- Solicite uma frase e conte quantas vezes a letra "a" (minúscula ou maiúscula) aparece nela. Exiba o resultado.
- Dada a string `" Python é demais "`, remova os espaços extras, substitua "demais" por "incrível" e exiba a nova string toda em maiúsculas.

### Intermediário (aplicação)
Crie uma função `formatar_nome(nome)` que receba um nome completo e retorne no formato "SOBRENOME, Nome". Exemplo: "Maria da Silva Santos" → "SANTOS, Maria". Considere que o sobrenome é a última palavra. Trate entradas com espaços extras. Utilize métodos de string como `strip`, `split`, `upper`, etc.

### Avançado (desafio)
Desenvolva uma função `validar_cpf(cpf)` que verifique se o CPF (string) possui formato válido e dígitos verificadores corretos. O formato pode conter pontos e traço (ex.: "123.456.789-09"). A validação deve:
1. Remover caracteres não numéricos.
2. Verificar se possui 11 dígitos.
3. Calcular os dois dígitos verificadores conforme algoritmo oficial.
4. Retornar `True` se válido, `False` caso contrário.

Use apenas métodos de string e operações aritméticas (sem regex). Documente a função com docstring.

## Projeto Prático: Processador de Cadastros
Você receberá um arquivo de texto `cadastros.txt` (simulado como string longa no código) com linhas no formato:
```text
nome;email;telefone;cidade
```
Exemplo de conteúdo:
```text
João Silva;joao@email.com;(11) 91234-5678;São Paulo
Maria Oliveira;maria@email.com;(21)99876-5432;Rio de Janeiro
...
```

**Requisitos do programa:**
1. Leia todas as linhas (use `splitlines()`).
2. Para cada linha:
    - Separe os campos usando `;`.
    - Limpe espaços extras (`strip`).
    - Formate o nome para título (`title`).
    - Normalize o e-mail para minúsculas.
    - Extraia apenas os dígitos do telefone (remova parênteses, espaços, traços) e formate como `(XX) XXXXX-XXXX`.
    - Capitalize a cidade.
3. Armazene os registros processados em uma lista de dicionários.
4. Exiba um relatório formatado, com colunas alinhadas (use f-strings com largura fixa).
5. Identifique e exiba registros inválidos:
    - E-mail sem `@`.
    - Telefone sem 11 dígitos após limpeza.
    - Campos vazios.

Este projeto integra fatiamento, métodos de string, formatação, validação e organização de dados, oferecendo uma experiência completa de manipulação textual.

## Resumo
Neste capítulo, você aprendeu que:
- Strings são sequências imutáveis que podem ser indexadas e fatiadas.
- Métodos como `upper`, `lower`, `strip`, `replace`, `split` e `join` permitem transformar e limpar textos.
- **f-strings** são a forma moderna e expressiva de formatar strings com variáveis, incluindo controle de alinhamento e casas decimais.
- Métodos como `isalpha`, `isdigit`, `startswith` e `endswith` ajudam na validação de padrões simples.
- A combinação dessas técnicas viabiliza o processamento robusto de dados textuais em aplicações desktop.

Dominar strings é um passo fundamental para qualquer desenvolvedor. Você agora está equipado para lidar com entradas do usuário, gerar relatórios elegantes e validar informações com confiança.
