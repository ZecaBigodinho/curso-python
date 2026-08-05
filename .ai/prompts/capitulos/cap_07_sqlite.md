# Prompt — Capítulo 07: SQLite

> **Instruções de uso:**
> 1. Cole o conteúdo de `.ai/prompts/project-mode.md` no DeepSeek como primeira mensagem
> 2. Em seguida, cole este prompt

---

## Dados do Capítulo

| Campo | Valor |
|---|---|
| **Curso** | Python para Desktop |
| **Módulo** | 04 — Projeto Finalizador |
| **Capítulo** | 07 — SQLite |
| **Arquivo de destino** | `07_sqlite.md` |
| **Palavras mínimas** | 2500 |

## Objetivo

Conectar o sistema ao banco de dados SQLite, criar as tabelas necessárias e migrar o cadastro de alunos da memória (lista) para persistência real.

## Contexto

- **Capítulo anterior:** 06 — Cadastro de Alunos
- **O que foi feito:** Formulário de cadastro completo com validação, Treeview com listagem, botões Salvar e Limpar. Dados armazenados em lista na memória.
- **Estado do código:** `main.py`, `views/login.py`, `views/menu.py`, `views/cadastro.py`, `controllers/auth.py`, `controllers/aluno.py`, `utils/helpers.py`. Sistema funcional mas dados se perdem ao fechar.

## Competências a Desenvolver

- `sqlite3` — módulo nativo do Python
- Conexão com banco usando context manager
- Criação de tabelas com `CREATE TABLE IF NOT EXISTS`
- INSERT com parâmetros (`?`) para segurança
- SELECT para carregar dados
- Inicialização automática do banco
- Migração de lista para banco sem quebrar a interface

## Resultado Esperado

Ao final deste capítulo, o aluno terá:
- `database/conexao.py` com função de conexão e inicialização
- Banco `escola.db` criado automaticamente na primeira execução
- Tabela `alunos` com campos: `id INTEGER PRIMARY KEY AUTOINCREMENT`, `nome TEXT NOT NULL`, `idade INTEGER NOT NULL`, `turma TEXT NOT NULL`
- `controllers/aluno.py` refatorado: `salvar_aluno()` faz INSERT, `listar_alunos()` faz SELECT
- Treeview carrega dados do banco ao abrir a tela
- Dados persistem entre execuções do programa

## Tópicos Obrigatórios

1. Criar `database/conexao.py` — funções `conectar()` e `inicializar_banco()`
2. Usar `sqlite3.connect()` com context manager (`with`)
3. `CREATE TABLE IF NOT EXISTS alunos (...)`
4. Chamar `inicializar_banco()` no `main.py` (antes de abrir a janela)
5. Refatorar `controllers/aluno.py`:
   - `salvar_aluno()`: trocar `lista.append()` por `INSERT INTO`
   - `listar_alunos()`: trocar iteração na lista por `SELECT * FROM`
6. Queries parametrizadas: `cursor.execute("INSERT INTO alunos VALUES (?, ?, ?)", (nome, idade, turma))`
7. `commit()` após INSERT
8. Atualizar `views/cadastro.py` para carregar dados do banco ao abrir

## Regras Especiais deste Capítulo

- Este capítulo é uma MIGRAÇÃO — o sistema já funciona, estamos apenas trocando o backend de "lista em memória" para "SQLite"
- Mostrar o código ANTES (lista) e DEPOIS (SQLite) em tabs comparativas
- Nunca usar concatenação de strings para SQL — sempre queries parametrizadas
- O Treeview agora deve exibir o `id` como coluna oculta (para uso futuro no CRUD)
- A tabela `alunos` deve incluir campo `id` autoincrement
- A "Missão da Equipe" deve ser: criar o banco de dados do projeto da equipe com as tabelas específicas do domínio deles
- O "Desafio" deve ser: adicionar uma tabela `usuarios` para substituir as credenciais hardcoded do login

## Próximo Capítulo

**Capítulo 08 — CRUD:** Com o banco funcionando, é hora de implementar as quatro operações completas: Consultar, Atualizar e Excluir (além do Inserir que já funciona).

---

**GERE O CAPÍTULO COMPLETO SEGUINDO TODAS AS REGRAS DO PROMPT MESTRE.**
