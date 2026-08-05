# 🗺️ Roadmap — Módulo 04: Projeto Finalizador

> **Curso:** Python para Desktop
> **Módulo:** 04 — Projeto Finalizador
> **Total de Capítulos:** 12
> **Metodologia:** Project Based Learning (PBL)
> **Prazo Final:** 20 de agosto
> **Projeto Base:** Sistema Escolar

---

## Visão Geral da Sequência

```
Cap 01 → Cap 02 → Cap 03 → Cap 04 → Cap 05 → Cap 06
  │        │        │        │        │        │
Escopo   Pastas    Login    Menu    Janelas  Cadastro
                                              │
Cap 12 ← Cap 11 ← Cap 10 ← Cap 09 ← Cap 08 ← Cap 07
  │        │        │        │        │        │
Entrega  Refator  Integrar  Nuvem   CRUD    SQLite
```

---

## Capítulo 01 — Introdução ao Projeto

| Campo | Descrição |
|---|---|
| **Arquivo** | `01_introducao_ao_projeto.md` |
| **Objetivo** | Compreender o escopo do Sistema Escolar, definir requisitos funcionais, conhecer a metodologia PBL e organizar as equipes de desenvolvimento |
| **Pré-requisitos** | Módulos 01, 02 e 03 concluídos |
| **Competências Desenvolvidas** | Levantamento de requisitos, planejamento de projeto, trabalho em equipe, visão sistêmica |
| **Resultado Esperado** | Documento de requisitos do sistema definido, equipes formadas, escopo do projeto da equipe definido |
| **Depende de** | Nenhum (primeiro capítulo do módulo) |

**Tópicos obrigatórios:**
- O que é um sistema de gestão
- Requisitos funcionais do Sistema Escolar
- Fluxo completo do sistema (Login → Menu → CRUD → Banco → Entrega)
- Formação das equipes e definição dos projetos
- Cronograma até o prazo final
- Diferença entre programar e desenvolver sistemas

---

## Capítulo 02 — Arquitetura do Sistema

| Campo | Descrição |
|---|---|
| **Arquivo** | `02_arquitetura_do_sistema.md` |
| **Objetivo** | Planejar a estrutura de pastas do projeto, compreender o padrão MVC simplificado, criar o esqueleto do sistema e o ponto de entrada `main.py` |
| **Pré-requisitos** | Capítulo 01 concluído |
| **Competências Desenvolvidas** | Arquitetura de software, organização de projetos, modularização, pensamento estrutural |
| **Resultado Esperado** | Estrutura de pastas criada (`views/`, `controllers/`, `database/`, `utils/`), `main.py` funcional que abre uma janela vazia com título e dimensões |
| **Depende de** | Capítulo 01 (escopo e requisitos) |

**Tópicos obrigatórios:**
- Por que organizar o código em pastas
- Padrão MVC simplificado para desktop
- Criação da estrutura: `views/`, `controllers/`, `database/`, `utils/`
- Arquivos `__init__.py`
- Criação do `main.py` como ponto de entrada
- Janela principal com Tkinter (esqueleto)

---

## Capítulo 03 — Tela de Login

| Campo | Descrição |
|---|---|
| **Arquivo** | `03_tela_de_login.md` |
| **Objetivo** | Implementar a tela de autenticação do sistema com campos de usuário e senha, validação de credenciais e transição para o menu principal |
| **Pré-requisitos** | Capítulo 02 concluído (estrutura de pastas e main.py existem) |
| **Competências Desenvolvidas** | Criação de formulários, validação de dados, controle de fluxo entre telas, tratamento de erros com messagebox |
| **Resultado Esperado** | Tela de login funcional com campos Entry, botão de entrar, validação de credenciais (hardcoded por enquanto), e messagebox de erro para credenciais inválidas |
| **Depende de** | Capítulo 02 (estrutura de pastas, main.py, janela principal) |

**Tópicos obrigatórios:**
- Criar `views/login.py`
- Criar `controllers/auth.py`
- Frame centralizado com campos de usuário e senha
- Entry com `show="*"` para senha
- Função de validação (credenciais em dicionário por enquanto)
- Messagebox para feedback de erro
- Preparar a transição para o Menu (sem implementar ainda)

---

## Capítulo 04 — Menu Principal

| Campo | Descrição |
|---|---|
| **Arquivo** | `04_menu_principal.md` |
| **Objetivo** | Criar o menu de navegação central do sistema com botões para cada funcionalidade e conectar o login ao menu |
| **Pré-requisitos** | Capítulo 03 concluído (login funcional) |
| **Competências Desenvolvidas** | Design de interfaces de navegação, organização de menus, UX básico, callback de botões |
| **Resultado Esperado** | Tela de menu com botões organizados (Cadastrar, Consultar, Sair), login redireciona para o menu após autenticação bem-sucedida |
| **Depende de** | Capítulo 03 (tela de login, autenticação) |

**Tópicos obrigatórios:**
- Criar `views/menu.py`
- Layout do menu com botões organizados em grid
- Botões: Cadastrar Alunos, Consultar Alunos, Sair
- Conectar login → menu (após autenticação)
- Botão Sair com confirmação (`messagebox.askyesno`)
- Estilização básica dos botões

---

## Capítulo 05 — Múltiplas Janelas

| Campo | Descrição |
|---|---|
| **Arquivo** | `05_multiplas_janelas.md` |
| **Objetivo** | Implementar a navegação entre Login, Menu e telas de funcionalidade usando Toplevel e controle de visibilidade |
| **Pré-requisitos** | Capítulo 04 concluído (login e menu funcionais) |
| **Competências Desenvolvidas** | Gerenciamento de janelas, Toplevel, withdraw/deiconify, destruição de janelas, fluxo de navegação |
| **Resultado Esperado** | Sistema com navegação completa: Login → Menu → [Tela Funcional] → Menu, com janelas abrindo e fechando corretamente sem duplicação |
| **Depende de** | Capítulo 04 (menu principal com botões) |

**Tópicos obrigatórios:**
- `Toplevel` vs nova `Tk()`
- `withdraw()` e `deiconify()` para ocultar/mostrar
- `destroy()` para fechar janelas
- `protocol("WM_DELETE_WINDOW")` para interceptar o X
- Navegação: Login → Menu → Tela → Menu
- Evitar duplicação de janelas
- Centralização de janelas na tela

---

## Capítulo 06 — Cadastro de Alunos

| Campo | Descrição |
|---|---|
| **Arquivo** | `06_cadastro_de_alunos.md` |
| **Objetivo** | Construir o formulário completo de cadastro de alunos com campos, validação e listagem usando Treeview |
| **Pré-requisitos** | Capítulo 05 concluído (navegação entre janelas funcional) |
| **Competências Desenvolvidas** | Formulários complexos, validação de entrada, Treeview para listagem, manipulação de dados em memória, UX de formulários |
| **Resultado Esperado** | Tela de cadastro com formulário (Nome, Idade, Turma), Treeview listando alunos cadastrados, botões Salvar e Limpar, dados armazenados em lista (memória) |
| **Depende de** | Capítulo 05 (navegação entre janelas, menu abre tela de cadastro) |

**Tópicos obrigatórios:**
- Criar `views/cadastro.py`
- Criar `controllers/aluno.py`
- Frame de formulário: Labels + Entry para Nome, Idade, Turma
- Validação: campos obrigatórios, idade numérica
- Treeview com colunas (Nome, Idade, Turma)
- Scrollbar vertical no Treeview
- Função `salvar_aluno()` (lista em memória por enquanto)
- Função `limpar_campos()`
- Atualizar Treeview após cadastro

---

## Capítulo 07 — SQLite

| Campo | Descrição |
|---|---|
| **Arquivo** | `07_sqlite.md` |
| **Objetivo** | Conectar o sistema ao banco de dados SQLite, criar as tabelas necessárias e migrar o cadastro de memória para persistência |
| **Pré-requisitos** | Capítulo 06 concluído (cadastro funcional em memória) |
| **Competências Desenvolvidas** | Conexão com banco de dados, criação de tabelas, INSERT, SELECT, cursor, commit, context manager |
| **Resultado Esperado** | Banco `escola.db` criado automaticamente, tabela `alunos` com campos (id, nome, idade, turma), cadastro agora persiste no banco, Treeview carrega dados do banco ao abrir |
| **Depende de** | Capítulo 06 (formulário de cadastro, Treeview, funções de salvar) |

**Tópicos obrigatórios:**
- Criar `database/conexao.py`
- `sqlite3.connect()` com context manager
- Criação automática da tabela `alunos` (`CREATE TABLE IF NOT EXISTS`)
- Migrar `salvar_aluno()` de lista para INSERT
- Migrar carregamento do Treeview de lista para SELECT
- Função `inicializar_banco()`
- Chamar inicialização no `main.py`

---

## Capítulo 08 — CRUD

| Campo | Descrição |
|---|---|
| **Arquivo** | `08_crud.md` |
| **Objetivo** | Implementar as quatro operações fundamentais — Inserir, Consultar, Atualizar e Excluir — conectando a interface ao banco de dados |
| **Pré-requisitos** | Capítulo 07 concluído (SQLite conectado, INSERT e SELECT funcionando) |
| **Competências Desenvolvidas** | CRUD completo, UPDATE, DELETE, seleção no Treeview, edição de registros, exclusão com confirmação, operações parametrizadas |
| **Resultado Esperado** | Sistema com CRUD completo: selecionar aluno no Treeview preenche o formulário, botão Editar atualiza o registro, botão Excluir remove com confirmação, busca por nome funciona |
| **Depende de** | Capítulo 07 (banco SQLite, tabela alunos, INSERT e SELECT) |

**Tópicos obrigatórios:**
- Criar `database/operacoes.py` com funções CRUD
- Seleção no Treeview: `bind("<<TreeviewSelect>>")` → preencher formulário
- Botão **Editar**: UPDATE no banco + atualizar Treeview
- Botão **Excluir**: confirmação + DELETE no banco + atualizar Treeview
- Campo de busca por nome (filtro com LIKE)
- Queries parametrizadas (nunca concatenar strings SQL)
- Feedback com messagebox para cada operação

---

## Capítulo 09 — Banco em Nuvem

| Campo | Descrição |
|---|---|
| **Arquivo** | `09_banco_em_nuvem.md` |
| **Objetivo** | Integrar o sistema a um banco de dados em nuvem para sincronização e acesso remoto dos dados |
| **Pré-requisitos** | Capítulo 08 concluído (CRUD completo com SQLite) |
| **Competências Desenvolvidas** | APIs REST, banco em nuvem, sincronização de dados, variáveis de ambiente, autenticação com chave API |
| **Resultado Esperado** | Sistema salva dados tanto no SQLite local quanto no banco em nuvem, botão de sincronizar, indicador de status de conexão |
| **Depende de** | Capítulo 08 (CRUD completo, todas as operações funcionando localmente) |

**Tópicos obrigatórios:**
- Conceito de banco local vs nuvem
- Escolha e configuração do serviço de nuvem
- Variáveis de ambiente para credenciais (`.env`)
- Funções de sincronização
- Botão "Sincronizar" na interface
- Indicador de status (online/offline)
- Fallback para SQLite quando sem internet
- Tratamento de erros de conexão

---

## Capítulo 10 — Integração

| Campo | Descrição |
|---|---|
| **Arquivo** | `10_integracao.md` |
| **Objetivo** | Conectar todas as telas e funcionalidades, criar um fluxo completo e coeso do login à saída do sistema |
| **Pré-requisitos** | Capítulo 09 concluído (banco local e nuvem funcionando) |
| **Competências Desenvolvidas** | Integração de sistemas, testes de fluxo, tratamento de exceções global, logging, experiência do usuário |
| **Resultado Esperado** | Sistema integrado: Login → Menu → Cadastro → CRUD → Sincronização, todos os fluxos funcionando sem erros, mensagens de feedback em todas as operações |
| **Depende de** | Capítulo 09 (todos os componentes existem, falta conectar) |

**Tópicos obrigatórios:**
- Revisão de todos os fluxos
- Testes manuais de cada funcionalidade
- Tratamento de exceções em pontos críticos
- Mensagens de feedback completas
- Barra de status ou rodapé informativo
- Menu completo com todas as opções ativas
- Atalhos de teclado (Enter para login, Esc para sair)

---

## Capítulo 11 — Refatoração

| Campo | Descrição |
|---|---|
| **Arquivo** | `11_refatoracao.md` |
| **Objetivo** | Reorganizar o código seguindo boas práticas profissionais, eliminar duplicações, documentar e preparar o projeto para entrega |
| **Pré-requisitos** | Capítulo 10 concluído (sistema integrado e funcional) |
| **Competências Desenvolvidas** | Refatoração, DRY, documentação, docstrings, código limpo, revisão de código, preparação para produção |
| **Resultado Esperado** | Código limpo, documentado, sem duplicações, com docstrings em todas as funções, README.md do projeto, arquivo requirements.txt |
| **Depende de** | Capítulo 10 (sistema completo e integrado) |

**Tópicos obrigatórios:**
- O que é refatoração e por que é importante
- Identificar código duplicado e extrair funções
- Adicionar docstrings em todas as funções
- Criar `README.md` do projeto do aluno
- Criar `requirements.txt`
- Revisão de nomes de variáveis e funções
- Verificação de PEP 8
- Remoção de código morto e prints de debug

---

## Capítulo 12 — Projeto Final

| Campo | Descrição |
|---|---|
| **Arquivo** | `12_projeto_final.md` |
| **Objetivo** | Finalizar o sistema, preparar a apresentação, documentar as funcionalidades e entregar o Projeto Final para avaliação |
| **Pré-requisitos** | Capítulo 11 concluído (código refatorado e documentado) |
| **Competências Desenvolvidas** | Entrega de projetos, apresentação técnica, documentação final, auto-avaliação, trabalho em equipe |
| **Resultado Esperado** | Projeto Final completo e entregue: sistema funcional, código documentado, apresentação preparada, checklist de entrega verificado |
| **Depende de** | Capítulo 11 (código limpo e documentado) |

**Tópicos obrigatórios:**
- Checklist final de funcionalidades obrigatórias
- Roteiro de apresentação
- Critérios de avaliação
- Como demonstrar o sistema ao professor
- Autoavaliação da equipe
- Registro de aprendizados (o que funcionou, o que foi difícil)
- Sugestões de melhorias futuras

---

## Mapa de Dependências

```
01 Introdução
 └──▶ 02 Arquitetura
       └──▶ 03 Login
             └──▶ 04 Menu
                   └──▶ 05 Janelas
                         └──▶ 06 Cadastro
                               └──▶ 07 SQLite
                                     └──▶ 08 CRUD
                                           └──▶ 09 Nuvem
                                                 └──▶ 10 Integração
                                                       └──▶ 11 Refatoração
                                                             └──▶ 12 Final
```

**Cada capítulo depende exclusivamente do anterior.** A cadeia é linear — não há ramificações.

---

## Cronograma Sugerido

| Semana | Aulas (Ter-Sex) | Capítulos | Entregas |
|---|---|---|---|
| Semana 1 | 4 aulas | Cap 01, 02, 03, 04 | Login + Menu funcionais |
| Semana 2 | 4 aulas | Cap 05, 06, 07, 08 | CRUD completo com SQLite |
| Semana 3 | 2-3 aulas | Cap 09, 10, 11 | Sistema integrado e refatorado |
| Entrega | Última aula | Cap 12 | **Projeto Final entregue** |
