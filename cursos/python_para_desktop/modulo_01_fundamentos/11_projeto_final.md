# 11. Projeto Integrador

## Objetivos
Neste capítulo, você aplicará todos os conhecimentos adquiridos no Módulo 01 para construir um projeto completo. Os objetivos são:
- Integrar variáveis, operadores, condicionais, repetições, funções, módulos, coleções, strings, arquivos e tratamento de exceções em uma única aplicação.
- Planejar a arquitetura de um programa de linha de comando (CLI) antes de codificá-lo.
- Organizar o código em módulos reutilizáveis, seguindo boas práticas.
- Implementar persistência de dados utilizando arquivos JSON.
- Tratar erros de forma robusta, validando entradas do usuário e prevenindo falhas.
- Produzir um sistema funcional — um Gerenciador de Tarefas ou um Controle Financeiro Pessoal — que possa ser expandido e utilizado no dia a dia.

## Pré-requisitos
Para aproveitar ao máximo este capítulo, você deve dominar os tópicos do Módulo 01:
- Variáveis e tipos de dados: `int`, `float`, `str`, `bool`.
- Operadores: aritméticos, de comparação, lógicos e de atribuição.
- Estruturas de controle: `if`, `elif`, `else` e laços `for` e `while` (incluindo `break` e `continue`).
- Funções: definição com `def`, parâmetros, retorno com `return`, escopo e `docstrings`.
- Módulos: importação de módulos padrão (`json`, `datetime`, `pathlib`) e criação de módulos próprios.
- Coleções: listas, tuplas e dicionários, com seus métodos principais.
- Strings: manipulação, formatação (f-strings), busca e validação.
- Arquivos e pastas: leitura e escrita com `with open()`, uso de `pathlib` para caminhos.
- Exceções: blocos `try/except/else/finally` e criação de exceções personalizadas.

Se algum desses assuntos ainda gerar dúvidas, revise os capítulos anteriores antes de prosseguir.

## Motivação
Aprender conceitos isolados é fundamental, mas o verdadeiro poder da programação se revela quando combinamos esses conceitos para resolver problemas reais. Um projeto integrador é a ponte entre a teoria e a prática: ele simula o desenvolvimento de uma aplicação completa, desde o planejamento até a entrega.

Imagine que você precisa organizar suas tarefas diárias ou controlar seus gastos pessoais. Em vez de depender de aplicativos de terceiros, você pode criar o seu próprio, adaptado exatamente às suas necessidades — e ainda praticar Python de forma significativa. Neste capítulo, vamos construir juntos um Gerenciador de Tarefas por linha de comando. Ao final, você terá um software funcional e a confiança para projetar suas próprias soluções.

## Conteúdo

### Planejamento do projeto
Antes de escrever uma linha de código, é essencial definir o escopo e a arquitetura. Nosso Gerenciador de Tarefas terá as seguintes funcionalidades:
- Adicionar uma nova tarefa com descrição, prioridade (alta, média, baixa) e status inicial "pendente".
- Listar todas as tarefas, com opção de filtrar por status (pendente, em andamento, concluída).
- Atualizar o status de uma tarefa (marcar como "em andamento" ou "concluída").
- Remover uma tarefa.
- Persistir os dados em um arquivo `tarefas.json`, para que as tarefas sejam mantidas entre execuções.

A estrutura de pastas será:
```text
gerenciador_tarefas/
├── main.py          # Script principal, com o menu e laço de interação
├── tarefas.py       # Módulo com funções de manipulação das tarefas
├── persistencia.py  # Módulo para salvar e carregar dados do arquivo JSON
├── validacao.py     # Módulo com funções de validação de entrada
└── excecoes.py      # Definições de exceções personalizadas (opcional)
```
Cada módulo agrupa responsabilidades coesas, facilitando manutenção e testes.

### Modelo de dados
Uma tarefa será representada por um dicionário com as chaves:
- `id`: número inteiro único (gerado automaticamente).
- `descricao`: string não vazia.
- `prioridade`: string, um dos valores "alta", "média" ou "baixa".
- `status`: string, um dos valores "pendente", "em andamento" ou "concluída".
- `data_criacao`: string no formato "YYYY-MM-DD", obtida com `datetime`.

```python
tarefa = {
    "id": 1,
    "descricao": "Estudar Python",
    "prioridade": "alta",
    "status": "pendente",
    "data_criacao": "2025-07-20"
}
```
A lista de tarefas será uma lista de dicionários.

### Módulo de validação (validacao.py)
Aqui concentramos funções que verificam a integridade dos dados fornecidos pelo usuário, retornando `True` ou `False`, ou levantando exceções personalizadas.

```python
# validacao.py
def validar_descricao(descricao):
    """Retorna True se a descrição não for vazia e tiver pelo menos 3 caracteres."""
    return bool(descricao) and len(descricao.strip()) >= 3

def validar_prioridade(prioridade):
    """Retorna True se prioridade for 'alta', 'média' ou 'baixa'."""
    return prioridade in ("alta", "média", "baixa")

def validar_status(status):
    """Retorna True se status for válido."""
    return status in ("pendente", "em andamento", "concluída")
```

### Módulo de persistência (persistencia.py)
Responsável por salvar e carregar a lista de tarefas do arquivo JSON, com tratamento de exceções.

```python
# persistencia.py
import json
from pathlib import Path

CAMINHO_ARQUIVO = Path("tarefas.json")

def carregar_tarefas():
    """Carrega a lista de tarefas do arquivo JSON. Retorna lista vazia se arquivo não existir."""
    if not CAMINHO_ARQUIVO.exists():
        return []
    try:
        with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Erro ao ler arquivo de tarefas: {e}. Iniciando vazio.")
        return []

def salvar_tarefas(tarefas):
    """Salva a lista de tarefas no arquivo JSON."""
    try:
        with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as f:
            json.dump(tarefas, f, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"Erro ao salvar tarefas: {e}")
```

### Módulo de lógica de tarefas (tarefas.py)
Contém funções que operam sobre a lista de tarefas: adicionar, listar, atualizar, remover. Utiliza funções de validação e persistência.

```python
# tarefas.py
from datetime import date
from validacao import validar_descricao, validar_prioridade, validar_status

def adicionar_tarefa(tarefas, descricao, prioridade="média"):
    """Adiciona uma nova tarefa à lista e retorna a tarefa criada ou None se inválida."""
    if not validar_descricao(descricao):
        print("Erro: descrição inválida.")
        return None
    if not validar_prioridade(prioridade):
        print("Erro: prioridade deve ser alta, média ou baixa.")
        return None

    novo_id = max((t["id"] for t in tarefas), default=0) + 1
    tarefa = {
        "id": novo_id,
        "descricao": descricao.strip(),
        "prioridade": prioridade,
        "status": "pendente",
        "data_criacao": str(date.today())
    }
    tarefas.append(tarefa)
    return tarefa

def listar_tarefas(tarefas, status=None):
    """Retorna lista de tarefas, filtradas por status se fornecido."""
    if status:
        return [t for t in tarefas if t["status"] == status]
    return tarefas

def atualizar_status(tarefas, id_tarefa, novo_status):
    """Atualiza o status de uma tarefa. Retorna True se bem-sucedido."""
    if not validar_status(novo_status):
        print("Status inválido.")
        return False
    for tarefa in tarefas:
        if tarefa["id"] == id_tarefa:
            tarefa["status"] = novo_status
            return True
    print(f"Tarefa com ID {id_tarefa} não encontrada.")
    return False

def remover_tarefa(tarefas, id_tarefa):
    """Remove tarefa pelo ID. Retorna True se removida."""
    for i, tarefa in enumerate(tarefas):
        if tarefa["id"] == id_tarefa:
            del tarefas[i]
            return True
    print(f"Tarefa com ID {id_tarefa} não encontrada.")
    return False
```

### Script principal (main.py)
Integra todos os módulos, apresenta um menu e mantém o laço principal.

```python
# main.py
from persistencia import carregar_tarefas, salvar_tarefas
import tarefas as tm

def exibir_menu():
    print("\n=== Gerenciador de Tarefas ===")
    print("1. Adicionar tarefa")
    print("2. Listar tarefas")
    print("3. Atualizar status")
    print("4. Remover tarefa")
    print("5. Sair")

def main():
    lista = carregar_tarefas()
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            desc = input("Descrição: ")
            prio = input("Prioridade (alta/média/baixa) [média]: ") or "média"
            if tm.adicionar_tarefa(lista, desc, prio):
                salvar_tarefas(lista)
                print("Tarefa adicionada com sucesso.")
        elif opcao == "2":
            filtro = input("Filtrar por status? (pendente/em andamento/concluída/todos): ").strip()
            if filtro in ("", "todos"):
                resultado = tm.listar_tarefas(lista)
            else:
                resultado = tm.listar_tarefas(lista, filtro)
            if not resultado:
                print("Nenhuma tarefa encontrada.")
            else:
                for t in resultado:
                    print(f"[{t['id']}] {t['descricao']} ({t['prioridade']}) - {t['status']} - {t['data_criacao']}")
        elif opcao == "3":
            try:
                tid = int(input("ID da tarefa: "))
                novo = input("Novo status (pendente/em andamento/concluída): ")
                if tm.atualizar_status(lista, tid, novo):
                    salvar_tarefas(lista)
                    print("Status atualizado.")
            except ValueError:
                print("ID inválido.")
        elif opcao == "4":
            try:
                tid = int(input("ID da tarefa a remover: "))
                if tm.remover_tarefa(lista, tid):
                    salvar_tarefas(lista)
                    print("Tarefa removida.")
            except ValueError:
                print("ID inválido.")
        elif opcao == "5":
            print("Encerrando...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
```

!!! tip "Separação de responsabilidades"
    Observe como o código está organizado: cada arquivo tem uma finalidade clara. Isso facilita a manutenção e permite que você reaproveite as funções de validação ou persistência em outros projetos.

### Aplicando exceções personalizadas
Para tornar o tratamento de erros mais semântico, podemos definir exceções em `excecoes.py` e usá-las nas funções de validação ou manipulação. Exemplo:

```python
# excecoes.py
class DescricaoInvalidaError(Exception):
    pass

class PrioridadeInvalidaError(Exception):
    pass

class StatusInvalidoError(Exception):
    pass
```
Em `validacao.py`, em vez de retornar `False`, podemos levantar a exceção apropriada, e o `main.py` captura com `try/except`. Essa abordagem é mais avançada, mas melhora a legibilidade e o desacoplamento.

### Tratamento de erros no carregamento
Se o arquivo JSON estiver corrompido, `carregar_tarefas` captura `JSONDecodeError` e inicia com lista vazia, avisando o usuário. Isso evita que o programa quebre, mantendo a robustez.

### Possíveis expansões
- Adicionar data de conclusão ao marcar como "concluída".
- Ordenar tarefas por prioridade ou data.
- Pesquisar tarefas por palavra-chave.
- Exportar tarefas para CSV.

## Exemplos

??? example "Exemplo 1: Adicionando e listando tarefas"
    === "Código"
        ```python
        # Suponha que a lista já contenha algumas tarefas
        from tarefas import adicionar_tarefa, listar_tarefas

        lista = []
        adicionar_tarefa(lista, "Comprar pão", "alta")
        adicionar_tarefa(lista, "Estudar para a prova", "alta")
        adicionar_tarefa(lista, "Lavar o carro", "baixa")

        print("Todas as tarefas:")
        for t in listar_tarefas(lista):
            print(f"{t['id']}: {t['descricao']} - {t['status']}")
        ```

    === "Resultado"
        ```text
        Todas as tarefas:
        1: Comprar pão - pendente
        2: Estudar para a prova - pendente
        3: Lavar o carro - pendente
        ```

    === "Explicação"
        Utilizamos a função `adicionar_tarefa` do módulo `tarefas`, que gera IDs automaticamente e atribui o status "pendente". Em seguida, `listar_tarefas` retorna a lista completa. Note como o código principal fica limpo, delegando a lógica ao módulo.

??? example "Exemplo 2: Atualizando status e salvando"
    === "Código"
        ```python
        from persistencia import salvar_tarefas
        from tarefas import atualizar_status, listar_tarefas

        # Após adicionar tarefas, marcamos a primeira como concluída
        sucesso = atualizar_status(lista, 1, "concluída")
        if sucesso:
            salvar_tarefas(lista)
            print("Status atualizado e salvo.")
        print("Tarefas pendentes:")
        for t in listar_tarefas(lista, "pendente"):
            print(t['descricao'])
        ```

    === "Resultado"
        ```text
        Status atualizado e salvo.
        Tarefas pendentes:
        Estudar para a prova
        Lavar o carro
        ```

    === "Explicação"
        `atualizar_status` modifica a lista em memória; depois chamamos `salvar_tarefas` para persistir a alteração no disco. O filtro por status "pendente" omite a tarefa concluída. Isso mostra a integração entre os módulos de lógica e persistência.

## Exercícios

### Básico (fixação)
1. Execute o Gerenciador de Tarefas e realize as seguintes operações: adicione três tarefas, liste todas, altere o status de uma delas para "concluída" e liste apenas as pendentes. Verifique o arquivo `tarefas.json` gerado.
2. Modifique a função `validar_descricao` para aceitar descrições com pelo menos 5 caracteres. Teste o sistema com descrições curtas e observe o comportamento.
3. Adicione uma opção no menu para exibir a quantidade total de tarefas cadastradas (use `len`).

### Intermediário (aplicação)
Implemente uma nova funcionalidade: pesquisar tarefas por palavra-chave. O usuário digita um termo e o sistema exibe todas as tarefas cuja descrição contenha esse termo (use o operador `in` e `lower()` para busca case-insensitive). Crie uma função `buscar_tarefas(tarefas, termo)` no módulo `tarefas.py` e integre ao menu.

### Avançado (desafio)
Transforme o Gerenciador de Tarefas em um Controle Financeiro Pessoal simples, com as seguintes adaptações:
- Cada registro será uma transação: `id`, `descricao`, `valor` (`float`, positivo para receita, negativo para despesa), `categoria` (ex.: alimentação, transporte, lazer) e `data`.
- Persista em `financas.json`.
- Funcionalidades: adicionar transação, listar todas, exibir saldo atual (soma de valores), listar por categoria e excluir transação.
- Valide valor como número, categoria não vazia e data no formato DD/MM/AAAA (use `datetime.strptime` para validar e converter).
- Trate exceções para entradas inválidas e problemas de arquivo.

## Projeto Prático: Guia passo a passo para o Gerenciador de Tarefas
Agora, vamos construir o projeto do zero. Siga estas etapas:

1. **Crie a estrutura de diretórios:**
    ```bash
    mkdir gerenciador_tarefas
    cd gerenciador_tarefas
    touch main.py tarefas.py persistencia.py validacao.py
    ```
2. **Implemente `validacao.py`** com as três funções de validação mostradas no conteúdo.
3. **Implemente `persistencia.py`** com `carregar_tarefas` e `salvar_tarefas`, usando `pathlib.Path` e `json`.
4. **Implemente `tarefas.py`** com `adicionar_tarefa`, `listar_tarefas`, `atualizar_status` e `remover_tarefa`, importando validações e `datetime`.
5. **Implemente `main.py`** com o menu, laço `while True`, e as chamadas às funções dos módulos.
6. **Teste cada funcionalidade** executando `python main.py`:
    - Adicione tarefas com diferentes prioridades.
    - Liste todas e veja se os IDs estão corretos.
    - Atualize um status e confira no arquivo JSON.
    - Remova uma tarefa e verifique a persistência.
    - Teste entradas inválidas: descrição vazia, prioridade inexistente, ID inexistente.
7. **Tratamento de erros adicionais:** No `main.py`, envolva a conversão de ID em `try/except ValueError`. No carregamento, trate `JSONDecodeError`.
8. **Melhorias opcionais:**
    - Use cores no terminal com `colorama` (instale com `pip install colorama`).
    - Adicione confirmação antes de remover.
    - Implemente backup automático do JSON antes de salvar.

Esse projeto prático consolida todos os conceitos do módulo. Ao terminá-lo, você terá um software completo, modular e robusto.

## Resumo
Neste capítulo, você:
- Integrou variáveis, operadores, condicionais, laços, funções, módulos, coleções, strings, manipulação de arquivos e tratamento de exceções em um único sistema.
- Planejou e implementou um Gerenciador de Tarefas com persistência em JSON.
- Aprendeu a separar responsabilidades em módulos coesos.
- Aplicou validações de entrada e tratamento de erros para garantir robustez.
- Desenvolveu um projeto do início ao fim, vivenciando o ciclo real de desenvolvimento de software.

O projeto integrador não apenas reforça o aprendizado técnico, mas também desenvolve habilidades de organização, depuração e pensamento sistêmico.
