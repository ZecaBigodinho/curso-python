# Prompt — Capítulo 02: Arquitetura do Sistema

> **Instruções de uso:**
> 1. Cole o conteúdo de `.ai/prompts/project-mode.md` no DeepSeek como primeira mensagem
> 2. Em seguida, cole este prompt

---

## Dados do Capítulo

| Campo | Valor |
|---|---|
| **Curso** | Python para Desktop |
| **Módulo** | 04 — Projeto Finalizador |
| **Capítulo** | 02 — Arquitetura do Sistema |
| **Arquivo de destino** | `02_arquitetura_do_sistema.md` |
| **Palavras mínimas** | 2000 |

## Objetivo

Planejar e criar a estrutura de pastas do projeto, compreender o padrão MVC simplificado para aplicações desktop, criar o esqueleto do sistema com `main.py` como ponto de entrada e uma janela principal vazia.

## Contexto

- **Capítulo anterior:** 01 — Introdução ao Projeto
- **O que foi feito:** Definição de escopo, requisitos funcionais, equipes formadas, cronograma estabelecido
- **Estado do código:** Nenhum código existe ainda. Este capítulo cria o primeiro código do projeto.

## Competências a Desenvolver

- Arquitetura de software para aplicações desktop
- Padrão MVC simplificado (Model-View-Controller)
- Organização de projetos com módulos Python
- Criação de pacotes com `__init__.py`
- Ponto de entrada único (`main.py`)

## Resultado Esperado

Ao final deste capítulo, o aluno terá:
- Estrutura de pastas criada: `views/`, `controllers/`, `database/`, `utils/`
- Arquivos `__init__.py` em cada pacote
- `main.py` funcional que abre uma janela Tkinter com título "Sistema Escolar", dimensões 800x600, centralizada na tela
- Compreensão de por que organizar o código desta forma

## Tópicos Obrigatórios

1. Por que não colocar tudo em um único arquivo
2. O padrão MVC explicado para desktop (não web)
3. Criação das pastas: `views/`, `controllers/`, `database/`, `utils/`
4. O papel de cada pasta no sistema
5. O que é `__init__.py` e por que é necessário
6. Criação do `main.py` — ponto de entrada
7. Janela principal: `Tk()`, `title()`, `geometry()`, `resizable()`, centralização

## Regras Especiais deste Capítulo

- Incluir diagrama ASCII da estrutura de pastas
- O `main.py` deve ser simples mas preparado para receber as telas futuras
- Comentários no estilo didático do Project Mode ("Eu sou o ponto de entrada", "Eu sou a janela principal")
- A "Missão da Equipe" deve ser: criar a mesma estrutura de pastas para o projeto da equipe, com `main.py` abrindo janela com título do projeto deles
- Falar sobre importância da organização desde o início

## Próximo Capítulo

**Capítulo 03 — Tela de Login:** O aluno irá construir a primeira tela funcional do sistema — o login com validação de credenciais.

---

**GERE O CAPÍTULO COMPLETO SEGUINDO TODAS AS REGRAS DO PROMPT MESTRE.**
