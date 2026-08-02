# Prompt — Capítulo 04: Menu Principal

> **Instruções de uso:**
> 1. Cole o conteúdo de `.ai/prompts/project-mode.md` no DeepSeek como primeira mensagem
> 2. Em seguida, cole este prompt

---

## Dados do Capítulo

| Campo | Valor |
|---|---|
| **Curso** | Python para Desktop |
| **Módulo** | 04 — Projeto Finalizador |
| **Capítulo** | 04 — Menu Principal |
| **Arquivo de destino** | `04_menu_principal.md` |
| **Palavras mínimas** | 2000 |

## Objetivo

Criar o menu de navegação central do sistema com botões para cada funcionalidade e conectar o login ao menu após autenticação bem-sucedida.

## Contexto

- **Capítulo anterior:** 03 — Tela de Login
- **O que foi feito:** Tela de login funcional com validação de credenciais, `views/login.py` e `controllers/auth.py` criados
- **Estado do código:** `main.py` abre o login. Login valida credenciais e mostra messagebox de erro. Falta a transição para o menu após login bem-sucedido.

## Competências a Desenvolver

- Design de menus de navegação
- Organização de botões com grid layout
- Callback de botões para navegação
- Confirmação de saída com `messagebox.askyesno`
- Conexão entre telas (login → menu)

## Resultado Esperado

Ao final deste capítulo, o aluno terá:
- `views/menu.py` com a tela de menu completa
- Botões organizados: "Cadastrar Alunos", "Consultar Alunos", "Sair"
- Login redireciona para o menu após autenticação
- Botão "Sair" pergunta confirmação antes de fechar
- Layout visualmente organizado e profissional

## Tópicos Obrigatórios

1. Criar `views/menu.py` — layout do menu com Frame
2. Título do menu: "Menu Principal — Sistema Escolar"
3. Botões organizados em grid: Cadastrar, Consultar, Sair
4. Estilização dos botões (cores, fontes, tamanhos)
5. Callback do botão "Sair" com `messagebox.askyesno`
6. Conectar login → menu: após validação OK, ocultar login e mostrar menu
7. Atualizar `main.py` para suportar a transição

## Regras Especiais deste Capítulo

- O código parte do `views/login.py` e `main.py` do capítulo anterior
- Mostrar como ocultar a janela de login e abrir o menu (preparação para o cap. 05)
- Os botões de Cadastrar e Consultar ainda não fazem nada (serão implementados nos próximos capítulos) — podem mostrar messagebox "Em construção"
- A "Missão da Equipe" deve ser: criar o menu do projeto da equipe com os botões específicos do sistema deles
- O "Desafio" deve ser: adicionar um label de boas-vindas mostrando o nome do usuário logado

## Próximo Capítulo

**Capítulo 05 — Múltiplas Janelas:** O sistema já tem login e menu, mas a navegação ainda é frágil. O aluno aprenderá a gerenciar múltiplas janelas de forma profissional.

---

**GERE O CAPÍTULO COMPLETO SEGUINDO TODAS AS REGRAS DO PROMPT MESTRE.**
