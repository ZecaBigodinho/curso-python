# Prompt — Capítulo 06: Cadastro de Alunos

> **Instruções de uso:**
> 1. Cole o conteúdo de `.ai/prompts/project-mode.md` no DeepSeek como primeira mensagem
> 2. Em seguida, cole este prompt

---

## Dados do Capítulo

| Campo | Valor |
|---|---|
| **Curso** | Python para Desktop |
| **Módulo** | 04 — Projeto Finalizador |
| **Capítulo** | 06 — Cadastro de Alunos |
| **Arquivo de destino** | `06_cadastro_de_alunos.md` |
| **Palavras mínimas** | 2500 |

## Objetivo

Construir o formulário completo de cadastro de alunos com campos de entrada, validação, listagem com Treeview e operações de salvar e limpar — usando lista em memória como armazenamento provisório.

## Contexto

- **Capítulo anterior:** 05 — Múltiplas Janelas
- **O que foi feito:** Navegação profissional entre telas (Login → Menu → Telas), Toplevel, withdraw/deiconify, centralização, prevenção de duplicação
- **Estado do código:** `main.py`, `views/login.py`, `views/menu.py`, `controllers/auth.py`, `utils/helpers.py`. Sistema navega entre telas. Botões do menu ainda apontam para placeholders.

## Competências a Desenvolver

- Formulários complexos com múltiplos campos
- Validação de dados de entrada
- Treeview para exibição de dados tabulares
- Scrollbar integrado ao Treeview
- Manipulação de dados em memória (lista de dicionários)
- Separação View/Controller para cadastro
- UX: limpar campos após salvar, feedback de sucesso

## Resultado Esperado

Ao final deste capítulo, o aluno terá:
- `views/cadastro.py` com formulário completo
- `controllers/aluno.py` com lógica de negócio
- Campos: Nome (Entry), Idade (Entry), Turma (Combobox ou Entry)
- Validação: campos obrigatórios, idade deve ser numérica e positiva
- Treeview exibindo alunos cadastrados (Nome, Idade, Turma)
- Scrollbar vertical no Treeview
- Botões: "Salvar" e "Limpar"
- Dados armazenados em lista na memória (será migrado para SQLite no cap. 07)
- Menu abrindo a tela de cadastro corretamente

## Tópicos Obrigatórios

1. Criar `views/cadastro.py` — layout com LabelFrame para formulário e LabelFrame para listagem
2. Criar `controllers/aluno.py` — funções: `salvar_aluno()`, `listar_alunos()`, `limpar_campos()`
3. Labels + Entry para Nome e Idade, Combobox para Turma
4. Validação: campos vazios, idade numérica, idade > 0
5. Treeview com colunas definidas e headings
6. Scrollbar vertical vinculada ao Treeview
7. Função `salvar_aluno()` que adiciona à lista e atualiza Treeview
8. Função `limpar_campos()` que reseta todos os Entry
9. Messagebox de sucesso após salvar
10. Atualizar `views/menu.py` para o botão "Cadastrar" abrir esta tela

## Regras Especiais deste Capítulo

- Este é o capítulo mais longo e importante da primeira metade do módulo
- Criar funções separadas para cada operação (`salvar_aluno`, `listar_alunos`, `limpar_campos`) — essas funções serão reaproveitadas no CRUD
- Os dados ficam em uma lista de dicionários: `[{"nome": "Ana", "idade": 16, "turma": "A"}]`
- Incluir comentário: "No capítulo 07, eu vou trocar essa lista por um banco SQLite"
- A "Missão da Equipe" deve ser: criar o formulário de cadastro do projeto da equipe (com os campos específicos do domínio deles)
- O "Desafio" deve ser: adicionar validação de duplicidade (não permitir dois alunos com mesmo nome)

## Próximo Capítulo

**Capítulo 07 — SQLite:** Os dados ainda vivem na memória e se perdem ao fechar o sistema. É hora de persistir com SQLite.

---

**GERE O CAPÍTULO COMPLETO SEGUINDO TODAS AS REGRAS DO PROMPT MESTRE.**
