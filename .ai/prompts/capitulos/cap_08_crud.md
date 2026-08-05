# Prompt — Capítulo 08: CRUD

> **Instruções de uso:**
> 1. Cole o conteúdo de `.ai/prompts/project-mode.md` no DeepSeek como primeira mensagem
> 2. Em seguida, cole este prompt

---

## Dados do Capítulo

| Campo | Valor |
|---|---|
| **Curso** | Python para Desktop |
| **Módulo** | 04 — Projeto Finalizador |
| **Capítulo** | 08 — CRUD |
| **Arquivo de destino** | `08_crud.md` |
| **Palavras mínimas** | 2500 |

## Objetivo

Implementar as quatro operações fundamentais do CRUD — Inserir (já feito), Consultar com filtros, Atualizar registros e Excluir com confirmação — conectando completamente a interface ao banco SQLite.

## Contexto

- **Capítulo anterior:** 07 — SQLite
- **O que foi feito:** Banco `escola.db` criado, tabela `alunos` com id/nome/idade/turma, INSERT e SELECT funcionando, dados persistem entre execuções
- **Estado do código:** `main.py`, `views/login.py`, `views/menu.py`, `views/cadastro.py`, `controllers/auth.py`, `controllers/aluno.py`, `database/conexao.py`, `utils/helpers.py`. O sistema já insere e lista alunos no banco. Faltam: editar, excluir e buscar.

## Competências a Desenvolver

- CRUD completo (Create, Read, Update, Delete)
- UPDATE com WHERE parametrizado
- DELETE com WHERE parametrizado
- Seleção de itens no Treeview (`bind("<<TreeviewSelect>>")`)
- Preenchimento de formulário a partir de seleção
- Busca/filtro com SQL LIKE
- Confirmação de exclusão com messagebox
- Operações parametrizadas (segurança contra SQL injection)

## Resultado Esperado

Ao final deste capítulo, o aluno terá:
- `database/operacoes.py` com todas as funções CRUD centralizadas
- Seleção no Treeview preenche o formulário automaticamente
- Botão "Editar" que faz UPDATE no banco e atualiza o Treeview
- Botão "Excluir" com confirmação que faz DELETE e atualiza o Treeview
- Campo de busca por nome (filtro com LIKE)
- Feedback com messagebox em todas as operações
- Botão "Novo" para limpar o formulário e preparar para nova inserção

## Tópicos Obrigatórios

1. Criar `database/operacoes.py` com funções: `inserir_aluno()`, `buscar_alunos()`, `atualizar_aluno()`, `excluir_aluno()`
2. Refatorar `controllers/aluno.py` para usar `database/operacoes.py`
3. Bind no Treeview: `treeview.bind("<<TreeviewSelect>>", ao_selecionar)`
4. Função `ao_selecionar()`: pega dados do item selecionado e preenche os Entry
5. Botão "Editar": `UPDATE alunos SET nome=?, idade=?, turma=? WHERE id=?`
6. Botão "Excluir": `messagebox.askyesno()` → `DELETE FROM alunos WHERE id=?`
7. Campo de busca: Entry + botão "Buscar" → `SELECT ... WHERE nome LIKE ?`
8. Botão "Novo" / "Limpar": reseta o formulário para modo de inserção
9. Atualizar layout da `views/cadastro.py` com os novos botões
10. Todos os botões desabilitados quando nenhum item está selecionado (UX)

## Regras Especiais deste Capítulo

- Este é o capítulo mais técnico e denso — dividir em passos bem claros
- Mostrar o fluxo completo: selecionar → editar → salvar → atualizar Treeview
- Usar o `id` armazenado (coluna oculta do Treeview) para UPDATE e DELETE
- Nunca concatenar valores no SQL — SEMPRE queries parametrizadas
- Explicar o conceito de "modo inserção" vs "modo edição" no formulário
- A "Missão da Equipe" deve ser: implementar CRUD completo para a entidade principal do projeto da equipe
- O "Desafio" deve ser: adicionar ordenação clicando nos cabeçalhos do Treeview

## Próximo Capítulo

**Capítulo 09 — Banco em Nuvem:** O sistema já funciona localmente. Agora vamos sincronizar com um banco em nuvem para acesso remoto.

---

**GERE O CAPÍTULO COMPLETO SEGUINDO TODAS AS REGRAS DO PROMPT MESTRE.**
