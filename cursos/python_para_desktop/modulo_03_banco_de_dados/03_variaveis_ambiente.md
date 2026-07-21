# Variáveis de Ambiente com .env

## Objetivos

Neste capítulo, você aprenderá a:

- Compreender o que são variáveis de ambiente e sua importância na segurança de aplicações.
- Identificar informações sensíveis que jamais devem ser fixadas diretamente no código-fonte.
- Utilizar a biblioteca `python-dotenv` para carregar configurações a partir de um arquivo `.env`.
- Acessar variáveis de ambiente com `os.getenv()` de forma segura e com valores padrão.
- Aplicar boas práticas, como a criação de arquivos `.env.example` e a exclusão do `.env` do controle de versão.
- Separar configurações sensíveis da lógica da aplicação, facilitando a portabilidade e a manutenção.

## Pré-requisitos

Antes de prosseguir, você deve ter familiaridade com:

- Fundamentos de Python: variáveis, funções, módulos e importações.
- Manipulação de arquivos e diretórios (leitura e escrita).
- Uso de terminal (prompt de comando) para instalar pacotes com `pip`.
- Noções básicas de sistemas de controle de versão como Git (conceito de repositório e commits).

Se você ainda não viu algum desses tópicos, recomendo revisar os capítulos anteriores.

## Motivação

Imagine que você desenvolveu um sistema de controle financeiro que se conecta a um banco de dados SQLite, mas no código-fonte você deixou o caminho do arquivo do banco escrito diretamente. Até aí, nenhum grande problema. Agora, imagine que seu sistema evoluiu e passou a se integrar com uma API de cotação de moedas, exigindo uma chave de API secreta para autenticação. Se você colocar essa chave diretamente no código, qualquer pessoa que tiver acesso ao seu repositório Git — seja um colega de equipe, um estagiário ou um invasor que consiga acesso ao seu código — terá a chave em mãos. Essa chave pode ser usada para fazer requisições em seu nome, gerar cobranças indevidas ou até derrubar sua conta.

Além do problema de segurança, valores fixos no código, também chamados de hardcoded, dificultam a manutenção: toda vez que você precisar mudar uma senha, uma URL ou um caminho de arquivo, terá que alterar o código-fonte e redistribuir a aplicação.

As variáveis de ambiente resolvem essas duas questões de forma elegante. Elas permitem que você mantenha configurações e segredos fora do código, carregando-os do ambiente do sistema operacional ou de um arquivo `.env` durante a execução. Neste capítulo, vamos dominar essa técnica usando a biblioteca `python-dotenv`, que se tornou o padrão da indústria para gerenciamento de configurações em Python.

## Conteúdo

### O que são variáveis de ambiente?

Variáveis de ambiente são pares de `chave=valor` definidos no sistema operacional e que podem ser acessados por processos em execução. Em Python, o módulo `os` fornece o dicionário `os.environ` e a função `os.getenv()` para lê-las.

```bash
# No terminal (Linux/macOS) ou prompt (Windows):
export BANCO_CAMINHO="meu_banco.db"
export API_KEY="sk-123456"
```

Dentro do Python:

```python
import os
caminho = os.getenv("BANCO_CAMINHO")
print(caminho)  # meu_banco.db
```

No entanto, definir essas variáveis manualmente toda vez que o sistema é executado é trabalhoso e propenso a erros. É aí que entra o arquivo `.env`.

### Arquivo .env

Um arquivo `.env` é um simples arquivo de texto, sem extensão, onde cada linha contém uma variável no formato `CHAVE=valor`. Por exemplo:

```env
# Banco de dados
DB_HOST=localhost
DB_NAME=financeiro.db
DB_USER=admin
DB_PASSWORD=senhaSuperSecreta123

# API externa
API_KEY=sk-abcdefghijklmnop
API_URL=https://api.exemplo.com/v2
```

Esse arquivo deve ser carregado pela aplicação e nunca versionado no controle de código-fonte (Git), pois contém segredos.

### A biblioteca python-dotenv

A biblioteca `python-dotenv` lê o arquivo `.env` e automaticamente define as variáveis de ambiente para o processo Python, como se tivessem sido exportadas no terminal. Para instalar:

```bash
pip install python-dotenv
```

O uso básico é extremamente simples:

```python
from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env na pasta atual
load_dotenv()

# Agora podemos acessar normalmente
senha = os.getenv("DB_PASSWORD")
print(f"A senha do banco é: {senha}")
```

O `load_dotenv()` procura automaticamente por um arquivo chamado `.env` no diretório corrente. Se o arquivo estiver em outro local, podemos passar o caminho: `load_dotenv("/caminho/para/config/.env")`.

!!! note "Ordem de precedência"
    As variáveis de ambiente já definidas no sistema operacional não são sobrescritas pelo `load_dotenv()` por padrão. Isso permite que você tenha um `.env` com valores de desenvolvimento, mas em produção as variáveis reais sejam definidas no ambiente sem risco de substituição. Se precisar sobrescrever, use `load_dotenv(override=True)`.

### Acessando variáveis com segurança

Use `os.getenv("CHAVE")` em vez de `os.environ["CHAVE"]`, pois o segundo lança uma exceção `KeyError` se a variável não existir, enquanto `getenv` retorna `None` (ou um valor padrão que você pode definir).

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Com valor padrão: se API_KEY não existir, usa "chave_padrao_dev"
api_key = os.getenv("API_KEY", "chave_padrao_dev")
```

Para variáveis obrigatórias, você pode fazer uma validação:

```python
db_password = os.getenv("DB_PASSWORD")
if not db_password:
    raise ValueError("Variável DB_PASSWORD não definida. Verifique o arquivo .env.")
```

### Estrutura recomendada do projeto

```text
meu_projeto/
├── .env                  # NÃO versionado, contém valores reais
├── .env.example          # Versionado, contém a lista de variáveis sem valores sensíveis
├── .gitignore            # Deve incluir .env
├── config.py             # Módulo que carrega as configurações
├── main.py
└── requirements.txt
```

O arquivo `.env.example` serve como documentação para outros desenvolvedores. Ele lista todas as variáveis que a aplicação espera, mas com valores vazios ou de placeholder:

```env
# Exemplo de configuração - copie para .env e preencha com seus dados
DB_HOST=localhost
DB_NAME=
DB_USER=
DB_PASSWORD=
API_KEY=
API_URL=https://api.exemplo.com/v2
```

!!! tip "Sempre forneça um .env.example"
    Ao compartilhar seu código no GitHub ou com colegas, o `.env.example` informa quais variáveis precisam ser configuradas, sem expor suas credenciais pessoais. É uma prática essencial em projetos profissionais.

### Configurando o .gitignore

Adicione a seguinte linha ao seu arquivo `.gitignore`:

```text
.env
```

Assim, o Git ignorará completamente o arquivo `.env`, impedindo que seja enviado acidentalmente ao repositório remoto.

!!! warning "Cuidado: não comite o .env!"
    Mesmo que o repositório seja privado, é uma péssima prática versionar segredos. Se um dia o código for tornado público ou um acesso indevido ocorrer, todos os segredos estarão expostos.

### Separando configurações em um módulo config.py

Uma excelente prática é criar um módulo central de configurações que carrega o `.env` e expõe as variáveis como constantes Python, possivelmente com conversão de tipo:

```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Banco de dados
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "padrao.db")
DB_USER = os.getenv("DB_USER", "usuario")
DB_PASSWORD = os.getenv("DB_PASSWORD", "senha123")

# API
API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL", "https://api.exemplo.com/v1")

# Convertendo para int
MAX_CONEXOES = int(os.getenv("MAX_CONEXOES", "10"))

# Booleanos: converte string "True"/"False"
MODO_DEBUG = os.getenv("MODO_DEBUG", "False").lower() == "true"
```

Depois, em qualquer parte do código, você importa e usa:

```python
from config import DB_NAME, API_KEY
```

Isso torna o código limpo, sem chamadas `os.getenv` espalhadas, e facilita a manutenção.

### Considerações de segurança

- Nunca inclua o `.env` em imagens Docker, pacotes distribuíveis ou instalações.
- Em ambientes de produção (servidores, containers), defina as variáveis diretamente no ambiente (ex.: secrets do Kubernetes, variáveis de ambiente do Heroku, AWS Parameter Store) em vez de depender de um arquivo `.env`.
- Use `os.urandom()` ou bibliotecas como `secrets` para gerar chaves secretas, nunca as invente manualmente.

### Uso em aplicações desktop

Em aplicações desktop, o arquivo `.env` normalmente fica no mesmo diretório do executável ou no diretório de dados do usuário. O importante é não expor credenciais que possam ser extraídas do código-fonte. Para distribuição, você pode até criptografar o `.env` ou solicitar as credenciais na primeira execução, salvando-as de forma segura com `keyring`. Mas isso é assunto para tópicos mais avançados.

## Exemplos

??? example "Exemplo 1: Carregando configurações do .env"
    === "Código"
        ```python
        import os
        from dotenv import load_dotenv

        # Carrega variáveis do arquivo .env
        load_dotenv()

        # Lê variáveis com valor padrão
        banco = os.getenv("DB_NAME", "padrao.db")
        host = os.getenv("DB_HOST", "localhost")
        usuario = os.getenv("DB_USER", "root")
        senha = os.getenv("DB_PASSWORD")

        print(f"Conectando ao banco {banco} em {host} como {usuario}")
        if senha:
            print(f"Senha configurada: {'*' * len(senha)}")
        else:
            print("AVISO: Nenhuma senha definida no .env")
        ```

    === "Arquivo .env"
        ```env
        DB_HOST=192.168.1.100
        DB_NAME=clientes.db
        DB_USER=admin
        DB_PASSWORD=minhaSenha@2025
        ```

    === "Resultado"
        ```text
        Conectando ao banco clientes.db em 192.168.1.100 como admin
        Senha configurada: *************
        ```

    === "Explicação"
        O `load_dotenv()` lê as variáveis do `.env` e as torna acessíveis via `os.getenv`. Caso uma variável não exista, podemos fornecer um valor padrão (ex.: "padrao.db"). A senha é exibida mascarada apenas para demonstração; em código real, nunca imprima senhas.

??? example "Exemplo 2: Módulo de configuração centralizado"
    === "Código (config.py)"
        ```python
        import os
        from dotenv import load_dotenv

        load_dotenv()

        # Configurações do aplicativo
        TITULO_APP = os.getenv("TITULO_APP", "Minha Aplicação")
        VERSAO = os.getenv("VERSAO", "1.0.0")

        # Banco de dados
        DB_PATH = os.getenv("DB_PATH", "dados.db")

        # Segurança
        CHAVE_SECRETA = os.getenv("CHAVE_SECRETA")
        if not CHAVE_SECRETA:
            raise RuntimeError("CHAVE_SECRETA é obrigatória. Defina no .env")

        # Tema da interface
        TEMA = os.getenv("TEMA", "dark")
        COR_PRIMARIA = os.getenv("COR_PRIMARIA", "blue")
        ```

    === "Código (main.py)"
        ```python
        from config import TITULO_APP, DB_PATH, TEMA, COR_PRIMARIA
        import customtkinter as ctk

        print(f"Iniciando {TITULO_APP}...")
        print(f"Banco de dados: {DB_PATH}")
        print(f"Tema: {TEMA}, Cor: {COR_PRIMARIA}")

        # Configuração da interface com os valores do .env
        ctk.set_appearance_mode(TEMA)
        ctk.set_default_color_theme(COR_PRIMARIA)
        # ... resto da aplicação
        ```

    === "Resultado"
        ```text
        Iniciando Meu Sistema Financeiro...
        Banco de dados: financas.db
        Tema: dark, Cor: green
        ```

    === "Explicação"
        Centralizamos todas as configurações em `config.py`. O `main.py` importa as constantes e as utiliza. Se uma variável obrigatória como `CHAVE_SECRETA` não for definida, o programa levanta um erro claro na inicialização, evitando comportamentos imprevisíveis mais tarde.

??? example "Exemplo 3: Usando .env.example e validação"
    === "Estrutura de arquivos"
        ```text
        projeto/
        ├── .env.example
        ├── .gitignore
        ├── config.py
        └── app.py
        ```

    === "Conteúdo do .env.example"
        ```env
        # Banco de dados
        DB_HOST=localhost
        DB_PORT=5432
        DB_NAME=meu_banco
        DB_USER=postgres
        DB_PASSWORD=

        # Serviço externo
        API_KEY=
        API_URL=https://api.exemplo.com
        ```

    === "Código de validação (config.py)"
        ```python
        import os
        from dotenv import load_dotenv

        load_dotenv()

        # Lista de variáveis obrigatórias
        OBRIGATORIAS = ["DB_NAME", "DB_USER", "DB_PASSWORD", "API_KEY"]

        ausentes = [v for v in OBRIGATORIAS if not os.getenv(v)]
        if ausentes:
            raise EnvironmentError(
                f"Variáveis obrigatórias não definidas: {', '.join(ausentes)}. "
                "Copie .env.example para .env e preencha os valores."
            )

        DB_NAME = os.getenv("DB_NAME")
        DB_USER = os.getenv("DB_USER")
        DB_PASSWORD = os.getenv("DB_PASSWORD")
        API_KEY = os.getenv("API_KEY")
        API_URL = os.getenv("API_URL", "https://api.exemplo.com")
        ```

    === "Resultado (se faltarem variáveis)"
        ```text
        EnvironmentError: Variáveis obrigatórias não definidas: DB_PASSWORD, API_KEY. Copie .env.example para .env e preencha os valores.
        ```

    === "Explicação"
        Validamos que todas as variáveis obrigatórias estão presentes logo após carregar o `.env`. Se alguma faltar, uma mensagem clara orienta o desenvolvedor a copiar o `.env.example` e preenchê-lo. Isso torna o setup do projeto muito mais amigável.

## Exercícios

### Básico (fixação)

1. Instale a biblioteca `python-dotenv` e crie um arquivo `.env` com uma variável `NOME_USUARIO`. Em um script Python, carregue o `.env` e exiba uma saudação "Olá, {NOME_USUARIO}!". Teste com seu nome.
2. Adicione ao `.env` uma variável `CAMINHO_BANCO` apontando para `meu_app.db`. No Python, use `os.getenv` para obter o caminho e imprimir "Banco de dados em: {caminho}". Se a variável não existir, o programa deve usar "padrao.db".
3. Crie um arquivo `.env.example` listando as variáveis do exercício 2, mas com valores vazios. Explique em um comentário a finalidade desse arquivo.

### Intermediário (aplicação)

1. Você está desenvolvendo um aplicativo de notas que usa um arquivo de configuração `config.ini` e também uma chave de API para sincronização. Atualmente, o caminho do arquivo e a chave estão hardcoded no código. Refatore a aplicação:
    - Crie um arquivo `.env` com `CAMINHO_CONFIG` e `API_KEY`.
    - Crie um módulo `config.py` que carregue essas variáveis e exporte como constantes.
    - No módulo principal, importe essas constantes e utilize-as.
    - Adicione validação para que `API_KEY` seja obrigatória (lance erro se não definida).
    - Crie o `.env.example` e configure o `.gitignore`.

### Avançado (desafio)

1. Desenvolva um pequeno utilitário de linha de comando chamado `gerenciador_env` que:
    - Aceita os argumentos `--init` e `--check`.
    - `--init`: procura um arquivo `.env.example` no diretório atual, lê suas variáveis, e pergunta ao usuário (via `input()`) o valor de cada uma, gerando um `.env` completo. Use `os.path.exists` para não sobrescrever um `.env` existente sem confirmação.
    - `--check`: verifica se todas as variáveis presentes no `.env.example` estão definidas no `.env`, exibindo um relatório de quais estão faltando e quais estão presentes.
    - Utilize `python-dotenv` para carregar e `os` para manipulação de arquivos.
    - Documente o código com docstrings e inclua um `.env.example` de exemplo para testes.

## Projeto Prático

### Protegendo as Configurações do Dashboard Financeiro

Retome o Dashboard Financeiro desenvolvido no Módulo 02 e aplique os conceitos de variáveis de ambiente para remover todas as configurações hardcoded.

**Requisitos:**

- **Identifique configurações sensíveis ou variáveis:**
    - Caminho do banco de dados SQLite (`financas.db`).
    - Tema da interface (`dark`, `light`, `system`).
    - Esquema de cores do CustomTkinter (`blue`, `green`, `dark-blue`).
    - Título da janela.
    - (Simule) uma `API_KEY` para um serviço futuro de cotação, mesmo que não seja utilizada de fato.

- **Crie o arquivo `.env` com essas variáveis e preencha com valores reais. Exemplo:**
    ```env
    DB_PATH=financas.db
    TEMA=dark
    COR_TEMA=dark-blue
    TITULO_APP=Meu Dashboard Financeiro
    API_KEY=sk-1234567890
    ```

- **Crie o módulo `config.py` que carregue o `.env`, valide as variáveis obrigatórias e exporte constantes.**

- **Modifique a aplicação principal para importar as configurações de `config.py` em vez de usar strings literais. Substitua `"financas.db"` por `config.DB_PATH`, `"dark"` por `config.TEMA`, etc.**

- **Crie o arquivo `.env.example` com a lista das variáveis e valores de exemplo ou vazios.**

- **Configure o `.gitignore` para ignorar o `.env`.**

- **Teste:**
    - Execute o dashboard e verifique se as configurações são aplicadas corretamente.
    - Altere o tema no `.env` para `light`, reinicie e confira se a interface muda.
    - Renomeie o `.env` temporariamente e execute o programa: ele deve exibir um erro claro informando quais variáveis faltam (ou usar valores padrão seguros).

- **Documentação:** Adicione um `README.md` (ou seção no próprio projeto) explicando como configurar o ambiente, copiando `.env.example` para `.env`.

**Desafio extra (opcional):**
- Implemente um modo de "primeira execução" que, se o `.env` não existir, copia automaticamente o `.env.example` para `.env` e orienta o usuário a preenchê-lo.
- Utilize `keyring` para armazenar a `API_KEY` de forma ainda mais segura, carregando-a de lá se disponível, com fallback para o `.env`.

## Resumo

Neste capítulo, você aprendeu que:

- Variáveis de ambiente permitem separar configurações e segredos do código-fonte, aumentando a segurança e a portabilidade.
- O arquivo `.env` armazena essas variáveis em formato `CHAVE=valor`.
- A biblioteca `python-dotenv` carrega automaticamente as variáveis do `.env` com `load_dotenv()`.
- Deve-se usar `os.getenv("CHAVE", valor_padrao)` para acesso seguro, e validar a presença de variáveis obrigatórias.
- O `.env` nunca deve ser versionado; o `.env.example` serve como template para outros desenvolvedores.
- Centralizar configurações em um módulo `config.py` mantém o código limpo e facilita a manutenção.
- As mesmas práticas são aplicáveis em projetos desktop, tornando-os profissionais e prontos para distribuição.

Com esses conhecimentos, você adiciona uma camada essencial de profissionalismo e segurança às suas aplicações Python.
