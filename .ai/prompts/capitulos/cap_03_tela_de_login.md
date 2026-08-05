# Prompt — Capítulo 03: Tela de Login

> **Instruções de uso:**
> 1. Cole o conteúdo de `.ai/prompts/project-mode.md` no DeepSeek como primeira mensagem
> 2. Em seguida, cole este prompt

---

## Dados do Capítulo

| Campo | Valor |
|---|---|
| **Curso** | Python para Desktop |
| **Módulo** | 04 — Projeto Finalizador |
| **Capítulo** | 03 — Tela de Login |
| **Arquivo de destino** | `03_tela_de_login.md` |
| **Palavras mínimas** | 2000 |

## Objetivo

Implementar a tela de autenticação do Sistema Escolar com campos de usuário e senha, validação de credenciais e feedback visual ao usuário.

## Contexto

- **Capítulo anterior:** 02 — Arquitetura do Sistema
- **O que foi feito:** Estrutura de pastas criada (`views/`, `controllers/`, `database/`, `utils/`), `main.py` funcional abrindo janela 800x600 centralizada
- **Estado do código:** `main.py` existe com janela principal vazia. Pastas criadas com `__init__.py`.

## Competências a Desenvolver

- Criação de formulários com Tkinter (Label, Entry, Button)
- Mascaramento de senha com `show="*"`
- Validação de entrada do usuário
- Feedback com `messagebox`
- Separação de responsabilidades (View vs Controller)
- Organização em módulos (`views/login.py`, `controllers/auth.py`)

## Resultado Esperado

Ao final deste capítulo, o aluno terá:
- `views/login.py` com a tela de login completa
- `controllers/auth.py` com a lógica de autenticação
- Campos: Usuário (Entry) e Senha (Entry com `show="*"`)
- Botão "Entrar" que valida credenciais
- Credenciais hardcoded em dicionário (provisório — será migrado para banco)
- Messagebox de erro para credenciais inválidas
- `main.py` atualizado para abrir a tela de login ao iniciar

## Tópicos Obrigatórios

1. Criar `views/login.py` — Frame com formulário centralizado
2. Criar `controllers/auth.py` — função `validar_login(usuario, senha)`
3. Labels descritivos: "Usuário:" e "Senha:"
4. Entry para usuário e Entry com `show="*"` para senha
5. Botão "Entrar" com callback de validação
6. Dicionário de credenciais (admin/admin por enquanto)
7. `messagebox.showerror()` para credenciais inválidas
8. Atualizar `main.py` para importar e exibir a tela de login
9. Preparar para transição ao menu (sem implementar a transição ainda)

## Regras Especiais deste Capítulo

- O código parte do `main.py` do capítulo anterior — mostrar o que já existe antes de adicionar
- Comentários didáticos: "Eu sou o campo de senha", "Eu escondo os caracteres com asteriscos"
- Explicar que as credenciais hardcoded são provisórias e serão migradas para banco no Capítulo 07
- A "Missão da Equipe" deve ser: criar a tela de login do projeto da equipe, adaptando o visual e as credenciais
- O "Desafio" deve ser: adicionar um botão "Mostrar/Ocultar Senha"

## Próximo Capítulo

**Capítulo 04 — Menu Principal:** Após o login, o sistema precisa de um menu central. O aluno criará a tela de navegação com botões para cada funcionalidade.

---

**GERE O CAPÍTULO COMPLETO SEGUINDO TODAS AS REGRAS DO PROMPT MESTRE.**
