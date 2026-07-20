# 09. Manipulação de Arquivos e Pastas

## Objetivos
Neste capítulo, você aprenderá a:
- Compreender os fundamentos da persistência de dados em arquivos de texto.
- Utilizar o gerenciador de contexto `with` para abrir e fechar arquivos automaticamente.
- Ler, escrever e anexar conteúdo em arquivos de texto com os modos de abertura apropriados.
- Tratar erros comuns, como arquivos não encontrados ou permissões insuficientes.
- Empregar a biblioteca `pathlib` para manipular caminhos e diretórios de forma elegante e multiplataforma.
- Criar, listar, renomear e remover arquivos e pastas de maneira segura.
- Desenvolver programas que armazenam e recuperam dados do sistema de arquivos, essenciais para aplicações desktop.

## Pré-requisitos
Antes de prosseguir, verifique se você domina:
- Tipos de dados básicos, variáveis e operadores.
- Estruturas de controle (`if`, `for`, `while`).
- Funções: definição, parâmetros, retorno de valores.
- Coleções (listas, dicionários) e manipulação de strings.
- Conceitos básicos de exceções (opcional, mas útil).

Se algum desses temas não estiver consolidado, revise os capítulos anteriores.

## Motivação
Imagine que você acabou de desenvolver um editor de notas ou um gerenciador de contatos. O usuário insere informações, mas quando o programa é fechado, tudo desaparece. Para evitar essa frustração, é indispensável persistir os dados — ou seja, salvá-los em disco para que possam ser recuperados posteriormente.

A manipulação de arquivos e pastas é a porta de entrada para transformar scripts descartáveis em aplicações reais. Seja para guardar preferências de usuário, gerar relatórios, armazenar registros de log ou organizar documentos, você precisará ler e escrever no sistema de arquivos.

Python oferece ferramentas poderosas e intuitivas para essas tarefas: o gerenciador de contexto `with` simplifica a abertura e o fechamento seguro dos arquivos, e a moderna biblioteca `pathlib` unifica o tratamento de caminhos, tornando o código compatível com Windows, Linux e macOS sem esforço adicional.

Ao final deste capítulo, você será capaz de criar programas que interagem com o ambiente de arquivos, salvando e carregando informações de forma robusta e profissional.

## Conteúdo

### A função open() e os modos de abertura
A função embutida `open()` é o ponto de partida para trabalhar com arquivos. Ela recebe o caminho do arquivo e um modo de abertura, representado por uma string:

| Modo | Significado |
| :--- | :--- |
| `'r'` | Leitura (read). O arquivo deve existir; erro caso contrário. |
| `'w'` | Escrita (write). Cria o arquivo se não existir; sobrescreve o conteúdo existente. |
| `'a'` | Anexar (append). Cria o arquivo se não existir; adiciona conteúdo ao final. |
| `'x'` | Criação exclusiva. Falha se o arquivo já existir. |
| `'b'` | Modo binário (ex.: `'rb'`, `'wb'`). |
| `'t'` | Modo texto (padrão, ex.: `'rt'`). |

```python
# Abre um arquivo para leitura (modo texto, padrão)
arquivo = open('dados.txt', 'r', encoding='utf-8')
conteudo = arquivo.read()
arquivo.close()  # O fechamento manual é obrigatório!
```

Esquecer de fechar o arquivo pode causar vazamento de recursos e perda de dados. É por isso que o gerenciador de contexto `with` é a forma recomendada.

### O gerenciador de contexto with
O bloco `with` garante que o arquivo seja fechado automaticamente ao final, mesmo que ocorra uma exceção. A sintaxe é limpa e segura:

```python
with open('dados.txt', 'r', encoding='utf-8') as arquivo:
    conteudo = arquivo.read()
# Aqui o arquivo já está fechado
```

!!! note "Vantagens do with"
    - Código mais conciso e legível.
    - Fechamento garantido, dispensando `close()` explícito.
    - Menor risco de esquecimento e de bugs relacionados a recursos abertos.

### Lendo arquivos de texto
Existem três métodos principais para leitura:
- `read()`: lê todo o conteúdo de uma só vez (retorna uma string).
- `readline()`: lê uma única linha, incluindo o caractere de nova linha `\n`.
- `readlines()`: retorna uma lista de strings, cada uma representando uma linha.

```python
with open('exemplo.txt', 'r', encoding='utf-8') as f:
    print("Conteúdo inteiro:")
    print(f.read())

# Leitura linha a linha (mais eficiente para arquivos grandes)
with open('exemplo.txt', 'r', encoding='utf-8') as f:
    for linha in f:
        print(linha.strip())  # strip() remove \n e espaços extras
```

!!! tip "Itere diretamente sobre o arquivo"
    O próprio objeto arquivo é um iterável que produz linhas. Usar `for linha in arquivo` é mais econômico em memória do que `readlines()`, pois não carrega todas as linhas de uma vez.

### Escrevendo em arquivos
Para escrita, usamos os métodos `write()` e `writelines()`.

```python
linhas = ['Primeira linha\n', 'Segunda linha\n', 'Terceira linha\n']

with open('saida.txt', 'w', encoding='utf-8') as f:
    f.write('Este é um cabeçalho.\n')
    f.writelines(linhas)
```

O modo `'w'` sobrescreve o conteúdo anterior. Se o arquivo não existir, será criado.

Para acrescentar dados ao final, utilize o modo `'a'` (append):

```python
with open('saida.txt', 'a', encoding='utf-8') as f:
    f.write('Nova linha adicionada.\n')
```

!!! warning "Cuidado ao abrir no modo escrita"
    Abrir um arquivo com `'w'` apaga imediatamente seu conteúdo. Sempre verifique se não perderá informações importantes. Uma abordagem segura é usar `'x'` para criação exclusiva, que evita sobrescrever acidentalmente.

### Codificação de caracteres
Sempre especifique o argumento `encoding='utf-8'`. Isso garante que caracteres acentuados, emojis e símbolos sejam tratados corretamente. Omitir a codificação pode resultar em `UnicodeEncodeError` ou `UnicodeDecodeError`, especialmente no Windows, onde a codificação padrão pode não ser UTF-8.

### Tratamento de exceções comuns
Ao manipular arquivos, diversas situações podem gerar exceções:
- `FileNotFoundError`: o arquivo não existe.
- `PermissionError`: falta de permissão para ler/gravar.
- `IsADirectoryError`: tentativa de abrir um diretório como arquivo.
- `IOError` / `OSError`: outros erros de entrada/saída.

Envolva operações de arquivo com blocos `try/except` para tornar seu programa resiliente:

```python
try:
    with open('dados.txt', 'r', encoding='utf-8') as f:
        conteudo = f.read()
except FileNotFoundError:
    print("Arquivo 'dados.txt' não encontrado.")
except PermissionError:
    print("Sem permissão para ler o arquivo.")
```

### Introdução ao pathlib
A biblioteca `pathlib`, introduzida no Python 3.4, oferece uma abordagem orientada a objetos para manipular caminhos. Ela abstrai as diferenças entre sistemas operacionais, substituindo as funções tradicionais do módulo `os.path` por uma interface mais intuitiva.

A classe principal é `Path`:

```python
from pathlib import Path

# Cria um objeto Path para o diretório atual
caminho_atual = Path.cwd()
print(caminho_atual)  # Ex: /home/usuario/projetos

# Caminho absoluto para um arquivo
arquivo = Path('/home/usuario/documentos/notas.txt')
# Ou usando o operador / para concatenar
arquivo = Path.home() / 'documentos' / 'notas.txt'
```

!!! note "O operador / com Path"
    `Path` sobrecarrega o operador de divisão, permitindo concatenar segmentos de caminho de forma natural: `Path('pasta') / 'subpasta' / 'arquivo.txt'`. Isso é muito mais elegante que `os.path.join()`.

### Criando e removendo diretórios
Com `pathlib`, criar uma árvore de diretórios é trivial:

```python
from pathlib import Path

pasta = Path('meu_projeto') / 'dados' / 'csv'
pasta.mkdir(parents=True, exist_ok=True)  # Cria diretórios pais se necessário
```

- `parents=True`: cria todos os diretórios intermediários.
- `exist_ok=True`: não gera erro se o diretório já existir.

Para remover um arquivo ou diretório vazio:

```python
arquivo = Path('saida.txt')
if arquivo.exists():
    arquivo.unlink()  # remove o arquivo

pasta_vazia = Path('pasta_temporaria')
if pasta_vazia.exists():
    pasta_vazia.rmdir()  # remove diretório vazio
```

Para remover diretórios não vazios, é necessário usar `shutil.rmtree()`.

### Listando e pesquisando arquivos
O método `iterdir()` lista o conteúdo de um diretório. Já `glob()` permite filtrar com padrões:

```python
pasta = Path('.')
# Lista todos os arquivos .txt no diretório atual
for arquivo in pasta.glob('*.txt'):
    print(arquivo.name)

# Pesquisa recursiva (inclui subpastas) com '**'
for arquivo in pasta.glob('**/*.txt'):
    print(arquivo)
```

!!! tip "Prefira glob com Path"
    O `glob` do `pathlib` é mais moderno e retorna objetos `Path`, o que permite encadear operações como `arquivo.read_text()` diretamente.

### Lendo e escrevendo com Path
A classe `Path` também oferece atalhos para ler e gravar conteúdo textual de forma concisa:

```python
caminho = Path('dados.txt')

# Leitura completa como string
try:
    texto = caminho.read_text(encoding='utf-8')
    print(texto)
except FileNotFoundError:
    print(f"Arquivo {caminho} não encontrado.")

# Escrita (sobrescreve)
caminho.write_text('Novo conteúdo\n', encoding='utf-8')

# Anexar conteúdo (append) – use open() com 'a', pois write_text sobrescreve
with caminho.open('a', encoding='utf-8') as f:
    f.write('Mais uma linha.\n')
```

!!! note "Quando usar read_text/write_text"
    Esses métodos são convenientes para arquivos pequenos e de código. Para arquivos grandes ou quando é necessário processamento incremental, o `open()` tradicional com `with` continua sendo a melhor escolha.

### Informações sobre arquivos
Objetos `Path` expõem diversas propriedades:

```python
arquivo = Path('dados.txt')
if arquivo.exists():
    print(f"Nome: {arquivo.name}")
    print(f"Tamanho: {arquivo.stat().st_size} bytes")
    print(f"Modificado em: {arquivo.stat().st_mtime}")
    print(f"É arquivo? {arquivo.is_file()}")
    print(f"É diretório? {arquivo.is_dir()}")
```

### Boas práticas
- Sempre utilize `with` ao abrir arquivos.
- Especifique `encoding='utf-8'` para evitar problemas com acentos.
- Ao lidar com caminhos, prefira `pathlib` em vez de strings brutas ou `os.path`.
- Verifique a existência com `Path.exists()` antes de tentar abrir.
- Trate exceções (`FileNotFoundError`, `PermissionError`) para tornar o programa mais robusto.
- Evite carregar arquivos enormes inteiramente na memória com `read()`; processe linha a linha.
- Use `parents=True` e `exist_ok=True` ao criar diretórios, garantindo que a estrutura desejada seja criada sem erros.

## Exemplos

??? example "Exemplo 1: Lendo e exibindo um arquivo de configuração"
    === "Código"
        ```python
        from pathlib import Path

        config_path = Path('config.ini')

        if config_path.exists():
            try:
                conteudo = config_path.read_text(encoding='utf-8')
                print("Conteúdo do arquivo de configuração:")
                print(conteudo)
            except Exception as e:
                print(f"Erro ao ler o arquivo: {e}")
        else:
            print("Arquivo de configuração não encontrado. Criando um padrão...")
            config_path.write_text("[Geral]\nidioma = pt-BR\n", encoding='utf-8')
            print("Arquivo criado com valores padrão.")
        ```

    === "Resultado"
        Supondo primeira execução:
        ```text
        Arquivo de configuração não encontrado. Criando um padrão...
        Arquivo criado com valores padrão.
        ```

    === "Explicação"
        O exemplo usa `Path` para verificar a existência e ler/escrever texto. Se o arquivo não existe, criamos um com conteúdo padrão. O `try/except` captura qualquer erro durante a leitura. `read_text` e `write_text` oferecem concisão.

??? example "Exemplo 2: Registro de log com append e timestamp"
    === "Código"
        ```python
        from datetime import datetime
        from pathlib import Path

        log_path = Path('app.log')

        def adicionar_log(mensagem):
            agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            linha = f"[{agora}] {mensagem}\n"
            with log_path.open('a', encoding='utf-8') as f:
                f.write(linha)

        # Simulando eventos da aplicação
        adicionar_log("Aplicação iniciada.")
        adicionar_log("Usuário 'joao' fez login.")
        adicionar_log("Operação concluída com sucesso.")

        # Lendo e exibindo o log gerado
        if log_path.exists():
            print("Log atual:")
            print(log_path.read_text(encoding='utf-8'))
        ```

    === "Resultado"
        ```text
        Log atual:
        [2025-07-20 15:30:01] Aplicação iniciada.
        [2025-07-20 15:30:01] Usuário 'joao' fez login.
        [2025-07-20 15:30:01] Operação concluída com sucesso.
        ```

    === "Explicação"
        A função `adicionar_log` abre o arquivo em modo append (`'a'`) usando `with` e escreve uma linha com timestamp. O `Path.open()` é uma forma alternativa de obter um gerenciador de contexto. A leitura final com `read_text` exibe o conteúdo completo.

??? example "Exemplo 3: Organizador de arquivos por extensão"
    === "Código"
        ```python
        from pathlib import Path

        pasta_origem = Path('.')  # diretório atual
        pasta_base = Path('organizado')
        pasta_base.mkdir(exist_ok=True)

        for item in pasta_origem.iterdir():
            if item.is_file():
                # Obtém a extensão (sem o ponto) ou 'sem_extensao'
                ext = item.suffix[1:] if item.suffix else 'sem_extensao'
                pasta_destino = pasta_base / ext
                pasta_destino.mkdir(exist_ok=True)

                # Move o arquivo para a subpasta (renomeando)
                novo_caminho = pasta_destino / item.name
                item.rename(novo_caminho)
                print(f"Movido: {item.name} -> {pasta_destino}/")

        print("Organização concluída!")
        ```

    === "Resultado"
        Supondo que existam 'foto.jpg', 'relatorio.pdf', 'script.py':
        ```text
        Movido: foto.jpg -> organizado/jpg/
        Movido: relatorio.pdf -> organizado/pdf/
        Movido: script.py -> organizado/py/
        Organização concluída!
        ```

    === "Explicação"
        O script percorre todos os itens do diretório atual. Se for um arquivo, extrai a extensão (sufixo) e cria uma subpasta correspondente dentro de `organizado`. Em seguida, renomeia (move) o arquivo para lá usando `Path.rename()`. Note que `suffix` retorna a extensão com ponto (ex.: `.jpg`), por isso removemos o primeiro caractere.

## Exercícios

### Básico (fixação)
1. Crie um programa que grave três frases digitadas pelo usuário em um arquivo `frases.txt`, cada uma em uma linha. Utilize o modo de escrita `'w'` e o gerenciador de contexto `with`.
2. Leia o arquivo `frases.txt` gerado e exiba seu conteúdo numerando as linhas (ex.: "1: primeira frase"). Use `readlines()` ou iteração direta.
3. Usando `pathlib`, crie uma pasta chamada `backup` no diretório atual. Verifique se ela existe antes de criar (use `exists()` e `mkdir()`).

### Intermediário (aplicação)
Crie um programa que gerencie um arquivo de tarefas (`tarefas.txt`). Cada linha terá uma tarefa e seu status no formato `tarefa|status`, onde status é `pendente` ou `concluida`. O programa deve:
- Adicionar uma nova tarefa (sempre como pendente).
- Listar todas as tarefas com seus status.
- Marcar uma tarefa como concluída (pelo número da linha, começando em 1).
- As alterações devem ser salvas no arquivo.

Utilize `pathlib` para o caminho do arquivo e manipulação de leitura/escrita com `with`. Implemente funções separadas para cada operação.

### Avançado (desafio)
Desenvolva um utilitário de backup que copie todos os arquivos `.txt` de uma pasta de origem para uma pasta de destino, mas apenas se o arquivo de origem for mais recente que o de destino (ou se o destino não existir). Requisitos:
- Use `pathlib` para caminhos e obtenção de datas de modificação (`stat().st_mtime`).
- A origem e destino devem ser informados pelo usuário (ou usar diretório atual e `backup_txt` como padrão).
- Crie a estrutura de destino se não existir.
- Exiba um resumo de arquivos copiados, ignorados (por serem mais novos no destino) e erros.
- Trate exceções (permissão, arquivo inexistente, etc.).

## Projeto Prático: Diário Pessoal com Arquivos de Texto
Desenvolva um programa de diário pessoal que armazena cada entrada em um arquivo de texto dentro de uma pasta organizada por ano e mês. O usuário poderá escrever uma nova entrada e visualizar entradas de uma data específica.

**Estrutura de diretórios:**
```text
diario/
   2025/
     07/
       20.txt   (conteúdo: linha com hora e texto da entrada)
       21.txt
     08/
       15.txt
```

**Requisitos:**
1. Ao iniciar, o programa exibe um menu:
    ```text
    1. Nova entrada
    2. Visualizar entrada
    3. Sair
    ```
2. **Nova entrada**: pergunta pela data (padrão: hoje) e pelo texto da entrada. Salva no arquivo correspondente ao dia, dentro da pasta `diario/ano/mes/`. Cada linha do arquivo deve começar com o horário da entrada (ex.: `14:35 - ...`). Use append para permitir múltiplas entradas no mesmo dia.
3. **Visualizar entrada**: solicita uma data e exibe todas as entradas daquele dia, se existirem. Se o arquivo não existir, informa que não há entradas.
4. Utilize `pathlib` para construir os caminhos, criar os diretórios necessários (`parents=True`, `exist_ok=True`) e ler/escrever os arquivos.
5. Trate exceções (arquivo não encontrado, erros de permissão) e valide o formato da data (use `datetime.strptime` ou simples validação manual).
6. O programa deve ser modular, com funções para `escrever_entrada`, `ler_entradas`, `criar_menu`, etc.

**Exemplo de execução:**
```text
=== Diário Pessoal ===
1. Nova entrada
2. Visualizar entrada
3. Sair
Escolha: 1
Data (DD/MM/AAAA) [padrão hoje]: 20/07/2025
Digite sua entrada: Hoje aprendi manipulação de arquivos com Python!
Entrada adicionada com sucesso.
...
Visualizar entrada:
Data (DD/MM/AAAA): 20/07/2025
Entradas do dia 20/07/2025:
  14:30 - Hoje aprendi manipulação de arquivos com Python!
```

Este projeto solidifica o uso de `pathlib`, gerenciador de contexto, modos de abertura, e organização de arquivos em diretórios, preparando você para aplicações desktop reais que precisam persistir dados.

## Resumo
Neste capítulo, você aprendeu:
- A função `open()` e os modos de leitura (`'r'`), escrita (`'w'`) e anexação (`'a'`).
- O gerenciador de contexto `with` garante o fechamento automático dos arquivos.
- Métodos de leitura como `read()`, `readline()`, `readlines()` e iteração direta.
- Métodos de escrita `write()` e `writelines()`, além do cuidado com sobrescrita.
- A importância da codificação UTF-8.
- Tratamento básico de exceções de arquivo.
- A biblioteca `pathlib` oferece uma API orientada a objetos para manipular caminhos, diretórios e arquivos de forma portável.
- Operações como criar pastas (`mkdir`), listar conteúdo (`iterdir`, `glob`), ler/escrever com `read_text`/`write_text` e obter informações de arquivos.

Agora você é capaz de dar persistência aos seus programas, salvar configurações, registrar logs e organizar dados em disco, habilidades imprescindíveis para qualquer desenvolvedor Python desktop.
