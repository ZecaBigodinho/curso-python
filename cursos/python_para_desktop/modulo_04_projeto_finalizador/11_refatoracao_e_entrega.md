# 11 — Refatoração

## 🎯 Objetivo

Neste capítulo você vai refatorar o código do Sistema Escolar — não para adicionar funcionalidades, mas para torná-lo mais limpo, legível e profissional, pronto para ser apresentado e mantido no futuro.

Ao final, você terá:

- Código livre de duplicações (princípio DRY)
- Docstrings no padrão Google em todas as funções e módulos
- Nomes de variáveis e funções revisados e descritivos
- Arquivo `README.md` completo com descrição, instruções e tecnologias
- Arquivo `requirements.txt` com todas as dependências
- Código formatado segundo a PEP 8
- Nenhum print() de debug ou código comentado sem propósito

## 📍 Contextualização

No Capítulo 10, você concluiu a integração de todas as funcionalidades. O sistema está completo: Login, Menu, CRUD, SQLite, Nuvem, atalhos de teclado, barra de status, tratamento de erros. Tudo funciona.

Mas pare por um momento e olhe seu código. Provavelmente você encontrará:

- Trechos repetidos em lugares diferentes
- Algumas funções longas que fazem "coisas demais"
- Variáveis com nomes como `x`, `temp`, `val`
- Comentários que explicam o óbvio ou, pior, código comentado que sobrou de testes

Refatorar é o processo de melhorar a estrutura interna do código sem alterar seu comportamento. É como arrumar a casa depois de uma grande obra: tudo já funciona, mas você quer que fique bonito, organizado e fácil de manter.

**Progresso do Sistema:**

```text
✅ Capítulos 01 a 10 — Construção e Integração
🔨 Refatoração ← VOCÊ ESTÁ AQUI
⬜ Projeto Final (Apresentação)
```

## ✅ Resultado Esperado

Ao final deste capítulo, o comportamento do sistema será exatamente o mesmo de antes. A diferença estará na qualidade do código:

- Antes: Funções de 40 linhas, lógica de validação repetida, comentários esparsos.
- Depois: Funções enxutas (máximo 20 linhas), validação extraída para função reutilizável, docstrings em todos os módulos.

Arquivos modificados:

Todos os arquivos `.py` do projeto serão revisados. Além disso, dois novos arquivos serão criados:

| Arquivo | Descrição |
|---|---|
| `README.md` | Documento de apresentação do projeto |
| `requirements.txt` | Lista de dependências Python |

## 💻 Implementação Guiada

### Passo 1 — O que é (e o que não é) refatoração

Antes de mexer no código, entenda os limites:

- ✅ **Refatoração é:** Renomear variáveis, extrair funções, remover duplicações, adicionar docstrings, formatar código.
- ❌ **Refatoração não é:** Adicionar novas funcionalidades, mudar o comportamento do sistema, reescrever do zero.

A regra de ouro: **teste após cada mudança**. Se o sistema parar de funcionar, volte atrás imediatamente. Refatoração sem testes é como fazer malabarismo com facas — impressionante até dar errado.

### Passo 2 — Identificando e eliminando duplicações

O princípio DRY (Don't Repeat Yourself) diz que cada pedaço de conhecimento deve ter uma representação única no código. Vamos caçar duplicações.

**Exemplo 1: Validação de campos repetida**

No nosso `views/cadastro.py`, a validação de campos vazios e idade aparece duas vezes — em `ao_clicar_salvar` e `ao_clicar_editar`. Já extraímos para `validar_campos` no Capítulo 10, mas vamos verificar se está realmente sendo usada em ambos os lugares.

=== "ANTES (duplicação)"

    ```python
    def ao_clicar_salvar():
        nome = entry_nome.get().strip()
        idade_str = entry_idade.get().strip()
        turma = combo_turma.get().strip()
        # Validação repetida...
        if not nome or not idade_str or not turma:
            messagebox.showwarning(...)
            return
        try:
            idade = int(idade_str)
        except ValueError:
            messagebox.showerror(...)
            return
        # ... resto da função
    
    def ao_clicar_editar():
        nome = entry_nome.get().strip()
        idade_str = entry_idade.get().strip()
        turma = combo_turma.get().strip()
        # MESMA validação repetida...
        if not nome or not idade_str or not turma:
            messagebox.showwarning(...)
            return
        try:
            idade = int(idade_str)
        except ValueError:
            messagebox.showerror(...)
            return
        # ... resto da função
    ```

=== "DEPOIS (DRY)"

    ```python
    def validar_campos(nome, idade_str, turma):
        """Valida os campos e retorna (valido, idade_int)."""
        if not nome or not idade_str or not turma:
            messagebox.showwarning("⚠️ Atenção", "Preencha todos os campos.")
            return False, None
        try:
            idade = int(idade_str)
        except ValueError:
            messagebox.showerror("❌ Erro", "Idade deve ser um número inteiro.")
            entry_idade.delete(0, tk.END)
            entry_idade.focus_set()
            return False, None
        if idade <= 0:
            messagebox.showerror("❌ Erro", "Idade deve ser um valor positivo.")
            entry_idade.delete(0, tk.END)
            entry_idade.focus_set()
            return False, None
        return True, idade
    
    def ao_clicar_salvar():
        nome = entry_nome.get().strip()
        idade_str = entry_idade.get().strip()
        turma = combo_turma.get().strip()
        valido, idade = validar_campos(nome, idade_str, turma)
        if not valido:
            return
        # ... resto da função (sem validação repetida)
    
    def ao_clicar_editar():
        nome = entry_nome.get().strip()
        idade_str = entry_idade.get().strip()
        turma = combo_turma.get().strip()
        valido, idade = validar_campos(nome, idade_str, turma)
        if not valido:
            return
        # ... resto da função (sem validação repetida)
    ```

Verifique se seu código já está assim. Se não estiver, esta é a hora de ajustar.

**Exemplo 2: Criação de botões estilizados**

Se você criou vários botões manualmente com os mesmos parâmetros de fonte, borda e cursor, considere extrair uma função fábrica:

```python
# Em utils/helpers.py (ou no próprio arquivo da view)

def criar_botao(pai, texto, cor_fundo, comando, largura=12, altura=1):
    """
    Eu crio um botão padronizado com os estilos do sistema.
    Evita repetir os mesmos parâmetros em cada Button.
    """
    return tk.Button(
        pai,
        text=texto,
        font=("Arial", 11, "bold"),
        bg=cor_fundo,
        fg="white",
        activebackground=_escurecer_cor(cor_fundo),
        activeforeground="white",
        width=largura,
        height=altura,
        bd=0,
        cursor="hand2",
        command=comando
    )
```

!!! tip "Dica Profissional"
    Se você se pegar copiando e colando mais de 3 linhas de código, pergunte-se: "Isso pode virar uma função?" Na maioria das vezes, a resposta é sim.

### Passo 3 — Adicionando docstrings em todo o código

Docstrings são strings de documentação colocadas logo após a definição de módulos, classes e funções. Elas explicam o que a função faz, quais parâmetros recebe e o que retorna.

Adote o padrão Google para docstrings. Exemplo:

```python
def salvar_aluno(nome, idade, turma):
    """
    Insere um novo aluno no banco de dados.

    Args:
        nome (str): Nome completo do aluno.
        idade (int): Idade do aluno em anos.
        turma (str): Turma do aluno (ex: '9A').

    Returns:
        dict: Dicionário com os dados do aluno inserido,
              incluindo o 'id' gerado pelo banco.

    Raises:
        Exception: Se ocorrer um erro de conexão com o banco.
    """
    # ... implementação
```

Roteiro para adicionar docstrings:

1. Abra cada arquivo `.py` do seu projeto.
2. Para cada função, verifique se há uma docstring.
3. Se não houver, adicione uma seguindo o padrão acima.
4. Não exagere: funções internas muito simples (ex: `lambda`) não precisam de docstring completa.

### Passo 4 — Revisando nomes de variáveis e funções

Nomes ruins são o maior inimigo da legibilidade. Faça uma varredura:

| Nome atual | Problema | Nome sugerido |
|---|---|---|
| `x`, `y` | Genérico demais | `pos_x`, `pos_y` |
| `temp` | Não diz o que armazena | `aluno_temp` ou `dados_temporarios` |
| `val` | Abreviação ambígua | `valor` ou `resultado` |
| `conn` | Aceitável (convenção) | Pode manter |
| `cur` | Abreviação desnecessária | `cursor` |

Regras para bons nomes:

- **Funções:** Verbo + substantivo → `salvar_aluno()`, `buscar_por_nome()`
- **Variáveis booleanas:** Prefixo `is_` ou `tem_` → `is_online`, `tem_erro`
- **Listas:** Plural → `alunos`, `botoes_config`
- **Constantes:** MAIÚSCULAS → `CAMINHO_BANCO`, `TURMAS_DISPONIVEIS`

### Passo 5 — Criando o README.md

O `README.md` é o cartão de visitas do seu projeto. Crie-o na raiz do projeto (`sistema_escolar/README.md`):

```markdown
# 🏫 Sistema Escolar

Sistema desktop para gestão de alunos desenvolvido em Python como
projeto final do curso **Python para Desktop — CourseForge**.

## ✨ Funcionalidades

- 🔐 Login com autenticação
- 📋 Cadastro completo de alunos (CRUD)
- 🔍 Busca por nome
- 💾 Persistência local com SQLite
- ☁️ Sincronização com banco em nuvem (Firebase)
- 🖥️ Interface gráfica com Tkinter
- ⌨️ Atalhos de teclado (Enter, Escape)

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python 3.10+ | Linguagem principal |
| Tkinter | Interface gráfica |
| SQLite | Banco de dados local |
| Firebase Realtime Database | Banco em nuvem |
| python-dotenv | Variáveis de ambiente |

## 📦 Como Instalar e Executar

### 1. Clone o repositório
\`\`\`bash
git clone https://github.com/seu-usuario/sistema-escolar.git
cd sistema-escolar
\`\`\`

### 2. Crie um ambiente virtual (opcional, mas recomendado)
\`\`\`bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
\`\`\`

### 3. Instale as dependências
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Configure as credenciais do Firebase
- Crie um projeto no Firebase Console
- Baixe o arquivo JSON de credenciais e coloque em `database/`
- Copie o arquivo `.env.exemplo` para `.env` e preencha com suas credenciais

### 5. Execute
\`\`\`bash
python main.py
\`\`\`

**Credenciais padrão**
- Usuário: `admin`
- Senha: `admin`

## 📁 Estrutura do Projeto
\`\`\`text
sistema_escolar/
├── main.py                 # Ponto de entrada
├── README.md               # Este arquivo
├── requirements.txt        # Dependências
├── .env                    # Credenciais (não versionado)
├── database/
│   ├── conexao.py          # Conexão com SQLite
│   ├── operacoes.py        # Operações CRUD
│   └── nuvem.py            # Sincronização com Firebase
├── views/
│   ├── login.py            # Tela de login
│   ├── menu.py             # Menu principal
│   └── cadastro.py         # Tela de cadastro (CRUD)
├── controllers/
│   ├── auth.py             # Lógica de autenticação
│   └── aluno.py            # Lógica de negócio
└── utils/
    └── helpers.py          # Funções utilitárias
\`\`\`

## 👥 Autores

| Nome | Papel |
|---|---|
| [Seu Nome] | Desenvolvedor(a) |

*Projeto desenvolvido como parte do Módulo 04 — Projeto Finalizador do curso Python para Desktop (CourseForge).*
```

### Passo 6 — Criando o `requirements.txt`

O `requirements.txt` lista todas as bibliotecas externas necessárias. Crie-o na raiz do projeto.

**Método automático (recomendado):**

```bash
pip freeze > requirements.txt
```

Depois, edite o arquivo e remova bibliotecas que não são usadas diretamente pelo projeto (ex: pip, setuptools e outras dependências automáticas do ambiente). O arquivo final deve conter apenas:

```text
firebase-admin==6.x.x
python-dotenv==1.x.x
```

(Ou os nomes sem versão fixa, se preferir.)

**Método manual (se souber exatamente o que usa):**

Crie o arquivo e adicione linha por linha:

```text
firebase-admin
python-dotenv
```

!!! tip "Dica Profissional"
    Versões fixas (`==6.5.0`) garantem que o projeto funcione exatamente igual em qualquer máquina. Versões abertas (`>=6.0`) permitem atualizações automáticas, mas podem quebrar o código. Para um projeto de entrega, prefira versões fixas.

### Passo 7 — Verificando a PEP 8

A PEP 8 é o guia de estilo oficial do Python. Verifique os pontos principais:

- [ ] Indentação: 4 espaços (nunca tabs)
- [ ] Linhas em branco: 2 linhas entre funções de módulo, 1 linha entre métodos de classe
- [ ] Espaços: Após vírgulas (`x, y`), ao redor de operadores (`a = b + c`)
- [ ] Comprimento de linha: Máximo 79 caracteres (ou 100, se o time concordar)
- [ ] Imports: Um por linha, organizados em: bibliotecas padrão → bibliotecas externas → módulos locais

Exemplo de imports organizados:

```python
# Biblioteca padrão
import os
from pathlib import Path

# Bibliotecas externas
import tkinter as tk
from tkinter import ttk, messagebox

# Módulos locais
from utils.helpers import centralizar_janela
from controllers.aluno import salvar_aluno
```

### Passo 8 — Removendo código morto

Código morto é qualquer trecho que nunca é executado:

- ❌ `print("debug: chegou aqui")` — remova todos
- ❌ Código comentado em bloco (`# def funcao_antiga...`) — remova
- ❌ Funções que não são chamadas em lugar nenhum — remova
- ❌ Imports não utilizados — remova

Se algo for realmente útil para debug futuro, substitua por logging (veja o desafio do Capítulo 10).

### Passo 9 — Teste final

Após todas as refatorações, execute o roteiro de testes do Capítulo 10 novamente. O sistema deve se comportar exatamente como antes. Se algo quebrou, volte atrás na última refatoração e descubra o que mudou.

## 📝 Exercício

**Tempo estimado:** 20-25 minutos

**Tarefa:** Pegue uma função longa do seu projeto (mais de 25 linhas) e a divida em funções menores, cada uma com uma responsabilidade única.

Exemplo: Se `abrir_janela_cadastro` tem 80 linhas, extraia partes como:
- `_criar_formulario(janela)` → cria o frame do formulário
- `_criar_tabela(janela)` → cria o Treeview e scrollbar
- `_criar_barra_status(janela)` → cria a barra de status

O ideal é que cada função faça uma coisa e a faça bem.

??? hint "Dica"
    Use o método "extrair função": selecione um bloco coeso de código, recorte-o, crie uma nova função com ele e chame-a de onde foi removido. Passe as variáveis necessárias como parâmetros.

??? success "Exemplo"
    **Antes:**
    ```python
    def abrir_janela_cadastro(janela_pai):
        # 30 linhas criando formulário...
        # 20 linhas criando Treeview...
        # 10 linhas criando barra de status...
        # 20 linhas de funções internas...
    ```
    
    **Depois:**
    ```python
    def abrir_janela_cadastro(janela_pai):
        janela = _criar_janela(janela_pai)
        entry_nome, entry_idade, combo_turma = _criar_formulario(janela)
        tree = _criar_tabela(janela)
        lbl_status = _criar_barra_status(janela)
        _configurar_eventos(janela, entry_nome, entry_idade, combo_turma, tree, lbl_status)
        _carregar_dados_iniciais(tree, lbl_status)
    ```
    Cada função interna tem no máximo 15 linhas e um nome que explica o que ela cria ou configura.

## 🏆 Missão da Equipe

**Tempo estimado:** 30-45 minutos

**Tarefa:** Refatorem o código do projeto da equipe e preparem a documentação para entrega.

**Entregável:** O projeto da equipe com:

- Código refatorado (DRY, nomes claros, funções enxutas)
- Docstrings em todas as funções e módulos
- `README.md` completo e personalizado
- `requirements.txt` com as dependências
- Código formatado seguindo PEP 8
- Nenhum `print()` de debug ou código comentado

**Checklist da Missão:**

- [ ] Nenhuma duplicação de código (validações, criação de widgets repetidos)
- [ ] Todas as funções têm docstrings no padrão Google
- [ ] Nomes de variáveis e funções são descritivos e em português
- [ ] O `README.md` contém: descrição, funcionalidades, tecnologias, instruções de instalação, estrutura de pastas e autores
- [ ] O `requirements.txt` lista todas as dependências necessárias
- [ ] O código segue PEP 8 (indentação, espaços, imports organizados)
- [ ] Não há `print()` de debug nem código comentado
- [ ] O sistema foi testado após a refatoração e continua funcionando
- [ ] O professor revisou o código refatorado

!!! important "Nota para o Professor"
    Verifique: A refatoração é subjetiva — o critério principal é legibilidade. Um código bem refatorado pode ser lido em voz alta e fazer sentido. Verifique se os READMEs estão completos e personalizados (não apenas cópia do exemplo). Peça que expliquem uma função que foi extraída durante a refatoração.

## ⚡ Desafio

**Vá além:** Use uma ferramenta de análise estática para verificar automaticamente a qualidade do código.

Instale o Flake8:

```bash
pip install flake8
```

Execute na raiz do projeto:

```bash
flake8 . --max-line-length=100 --exclude=venv,.git,__pycache__
```

O Flake8 apontará problemas como:

- `E501: line too long` → linha muito longa
- `W291: trailing whitespace` → espaços no final da linha
- `F401: imported but unused` → import não utilizado

Corrija todos os problemas apontados (exceto os que você considerar aceitáveis, como linhas de 100 caracteres se o time concordar).

Você também pode usar o Black para formatar automaticamente:

```bash
pip install black
black . --line-length=100
```

## ⚠️ Erros Comuns

!!! danger "Refatorar sem testar"
    **Sintoma:** Após várias mudanças, o sistema não abre ou uma funcionalidade quebra. Você não sabe qual mudança causou o problema.
    
    **Causa:** Acumular muitas refatorações sem testar entre elas.
    
    **Solução:** Refatore uma coisa por vez e teste imediatamente. Use `git commit` após cada refatoração bem-sucedida. Se algo quebrar, `git diff` mostra exatamente o que mudou.

!!! warning "Renomear variável e esquecer referências"
    **Sintoma:** `NameError: name 'nova_variavel' is not defined.`
    
    **Causa:** Você renomeou uma variável na definição, mas esqueceu de atualizar todos os lugares onde ela é usada.
    
    **Solução:** Use a funcionalidade "Rename Symbol" do VS Code (F2 sobre o nome da variável) — ela atualiza todas as referências automaticamente. Se fizer manualmente, use "Find in Files" (Ctrl+Shift+F) para encontrar todas as ocorrências.

!!! danger "Remover código que parece morto, mas não é"
    **Sintoma:** Uma funcionalidade para de funcionar após remover uma função que "não era chamada em lugar nenhum".
    
    **Causa:** A função era chamada indiretamente (ex: via string de configuração, callback armazenado em dicionário, ou `getattr`).
    
    **Solução:** Antes de remover, faça uma busca no projeto inteiro pelo nome da função. Verifique também dicionários de configuração como `botoes_config` — o nome pode estar como valor de uma chave.

## 💡 Boas Práticas

**1. Commits frequentes durante a refatoração**

Faça um commit a cada pequena melhoria: "extrai função de validação", "adiciona docstrings em views", "renomeia variáveis no controller". Se algo der errado, você pode voltar atrás sem perder todo o trabalho.

**2. O princípio do escoteiro**

"Sempre deixe o acampamento mais limpo do que você encontrou." Se você abrir um arquivo para corrigir um bug e encontrar uma variável com nome ruim, renomeie-a. Pequenas melhorias acumuladas tornam o código saudável.

**3. Docstrings como documentação viva**

Docstrings não são apenas para outras pessoas — são para você mesmo daqui a 6 meses. Quando você voltar ao código e não lembrar o que uma função faz, a docstring estará lá.

**4. README.md bem escrito abre portas**

Em processos seletivos e entrevistas, o README é a primeira coisa que recrutadores veem no seu GitHub. Um README claro, com instruções de instalação e demonstração das funcionalidades, causa uma impressão muito melhor do que um repositório sem documentação.

**5. PEP 8 não é opcional**

Seguir o guia de estilo da comunidade torna seu código familiar para qualquer pessoa Python. Ferramentas como `flake8` e `black` automatizam essa verificação — use-as.

## ☑️ Checklist

Antes de prosseguir para o próximo capítulo, confirme:

- [ ] Todas as duplicações de código foram eliminadas (validações, criação de widgets)
- [ ] Todas as funções possuem docstrings no padrão Google
- [ ] Nomes de variáveis, funções e arquivos estão descritivos e em português
- [ ] O `README.md` está completo e personalizado
- [ ] O `requirements.txt` lista todas as dependências
- [ ] O código segue PEP 8 (ou foi verificado com flake8/black)
- [ ] Não há `print()` de debug, código comentado ou imports não utilizados
- [ ] O sistema foi testado após a refatoração e funciona exatamente como antes
- [ ] Minha equipe concluiu a Missão da Equipe

## ➡️ Próximo Capítulo

No **Capítulo 12 — Projeto Final**, você entregará o sistema, apresentará para a turma e celebrará a conclusão do curso Python para Desktop.

Depois de 11 capítulos intensos — do planejamento à refatoração, passando por interfaces gráficas, banco de dados e nuvem — você tem em mãos um sistema desktop completo, funcional e profissional.

Prepare-se para brilhar na apresentação! 🎓🚀
