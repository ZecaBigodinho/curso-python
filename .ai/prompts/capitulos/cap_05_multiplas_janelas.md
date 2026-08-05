# Prompt — Capítulo 05: Múltiplas Janelas

> **Instruções de uso:**
> 1. Cole o conteúdo de `.ai/prompts/project-mode.md` no DeepSeek como primeira mensagem
> 2. Em seguida, cole este prompt

---

## Dados do Capítulo

| Campo | Valor |
|---|---|
| **Curso** | Python para Desktop |
| **Módulo** | 04 — Projeto Finalizador |
| **Capítulo** | 05 — Múltiplas Janelas |
| **Arquivo de destino** | `05_multiplas_janelas.md` |
| **Palavras mínimas** | 2000 |

## Objetivo

Implementar a navegação profissional entre Login, Menu e telas de funcionalidade usando Toplevel, controle de visibilidade e destruição de janelas.

## Contexto

- **Capítulo anterior:** 04 — Menu Principal
- **O que foi feito:** Menu funcional com botões (Cadastrar, Consultar, Sair), login redireciona para menu após autenticação
- **Estado do código:** `main.py`, `views/login.py`, `views/menu.py`, `controllers/auth.py`. Login → Menu funciona, mas a navegação é rudimentar. Botões de funcionalidade mostram "Em construção".

## Competências a Desenvolver

- Toplevel vs nova instância de Tk
- `withdraw()` e `deiconify()` para controle de visibilidade
- `destroy()` para fechar janelas
- `protocol("WM_DELETE_WINDOW")` para interceptar o botão X
- Navegação bidirecional: ida e volta entre telas
- Prevenção de duplicação de janelas

## Resultado Esperado

Ao final deste capítulo, o aluno terá:
- Sistema com navegação completa: Login → Menu → [Tela Funcional] → Menu
- Janelas abrindo e fechando corretamente
- Sem duplicação (abrir a mesma tela duas vezes)
- Botão X interceptado em todas as janelas
- Janelas centralizadas na tela

## Tópicos Obrigatórios

1. Por que não criar múltiplas instâncias de `Tk()`
2. `Toplevel` como janela filha
3. `withdraw()` para ocultar e `deiconify()` para mostrar
4. `destroy()` para fechar janelas definitivamente
5. `protocol("WM_DELETE_WINDOW", callback)` em cada janela
6. Função auxiliar para centralizar janelas na tela
7. Refatorar a transição login → menu para usar withdraw/deiconify
8. Preparar a navegação menu → telas de funcionalidade (placeholder)
9. Prevenir duplicação: verificar se janela já está aberta

## Regras Especiais deste Capítulo

- Refatorar o código do capítulo anterior — a transição login → menu deve usar withdraw/deiconify
- Criar função genérica `centralizar_janela(janela, largura, altura)` em `utils/helpers.py`
- A "Missão da Equipe" deve ser: implementar a navegação completa do sistema da equipe (menu → telas das funcionalidades)
- O "Desafio" deve ser: adicionar animação de fade-in ao abrir janelas (usando `attributes('-alpha')`)
- Nos erros comuns, destacar: "Erro Tcl: abrir Tk() duas vezes"

## Próximo Capítulo

**Capítulo 06 — Cadastro de Alunos:** Com a navegação funcionando, é hora de criar a primeira tela funcional real — o formulário de cadastro com Treeview.

---

**GERE O CAPÍTULO COMPLETO SEGUINDO TODAS AS REGRAS DO PROMPT MESTRE.**
