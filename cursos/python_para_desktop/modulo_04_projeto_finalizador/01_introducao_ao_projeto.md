# 1. Introdução ao Projeto

## 🎯 Objetivo

Neste capítulo você vai conhecer o Sistema Escolar, o projeto completo que será construído ao longo de todo o módulo.

Ao final, você terá:

- Compreendido o escopo completo de um sistema de gestão escolar
- Definido os requisitos funcionais (Login, Menu, Cadastro, CRUD, Banco)
- Entendido a diferença entre programar exercícios e desenvolver um sistema real
- Formado sua equipe de desenvolvimento e escolhido o tema do projeto
- Visualizado o cronograma até a entrega final (20 de agosto)

## 📍 Contextualização

Você acaba de concluir três módulos intensos: Fundamentos do Python, Interfaces Gráficas com Tkinter e CustomTkinter e Banco de Dados com SQLite. Sabe criar variáveis, funções, classes, conectar-se a um banco e construir janelas com botões e tabelas.

Agora chegou o momento de abandonar os exercícios isolados e pensar como um desenvolvedor de verdade.

Durante o Módulo 04 — Projeto Finalizador, você não fará mais mini-programas nem exemplos didáticos. Cada linha de código contribuirá para um sistema completo. Ao final, você terá um software funcional pronto para usar, testar e mostrar em uma entrevista de emprego.

**Progresso do Sistema:**

```text
✅ Módulo 01 — Fundamentos do Python
✅ Módulo 02 — Interfaces Gráficas (Tkinter/CustomTkinter)
✅ Módulo 03 — Banco de Dados com SQLite
🔨 Introdução ao Projeto ← VOCÊ ESTÁ AQUI
⬜ Arquitetura do Sistema
⬜ Tela de Login
⬜ Menu Principal
⬜ Múltiplas Janelas
⬜ Cadastro de Alunos
⬜ SQLite Local
⬜ CRUD Completo
⬜ Banco em Nuvem
⬜ Integração e Testes
⬜ Refatoração e Entrega
```

!!! note "Aviso"
    Este é o único capítulo predominantemente conceitual do módulo. Ele estabelece as bases para todas as implementações futuras. A partir do próximo capítulo, mão no código!

## ✅ Resultado Esperado

Ao final deste capítulo, você não terá modificado o código (ainda!), mas terá uma visão cristalina do sistema que construirá. Saberá exatamente:

- O que cada tela fará
- Como os componentes se conectam
- Quando cada parte será desenvolvida

O sistema final terá este fluxo:

```text
┌─────────────────────────────────────────────────┐
│                  SISTEMA ESCOLAR                │
│                                                 │
│  ┌──────────┐    autenticação    ┌───────────┐  │
│  │  LOGIN   │ ─────────────────▶ │   MENU    │  │
│  │usuário   │                    │ PRINCIPAL │  │
│  │senha     │                    │┌──┐┌──┐┌─┐│  │
│  └──────────┘                    ││Cad││Con││Sai│  │
│                                  │└──┘└──┘└─┘│  │
│                                  └─────┬─────┘  │
│                                        │        │
│                               navegação│        │
│                                        ▼        │
│  ┌──────────────────────────────────────────┐   │
│  │         TELA DE CADASTRO (CRUD)          │   │
│  │                                          │   │
│  │  ┌────────────────────────────┐          │   │
│  │  │     FORMULÁRIO             │          │   │
│  │  │  Nome:  [____________]     │          │   │
│  │  │  Idade: [____________]     │          │   │
│  │  │  Turma: [____________]     │          │   │
│  │  └────────────────────────────┘          │   │
│  │                                          │   │
│  │  ┌────────────────────────────┐          │   │
│  │  │  LISTAGEM (Treeview)       │          │   │
│  │  │  Nome    │ Idade │ Turma   │          │   │
│  │  │  ────────┼───────┼───────  │          │   │
│  │  │  João    │ 15    │ 9A      │          │   │
│  │  │  Maria   │ 14    │ 9B      │          │   │
│  │  └────────────────────────────┘          │   │
│  │                                          │   │
│  │  [💾 Salvar] [✏️ Editar]                 │   │
│  │  [🗑️ Excluir] [🧹 Limpar]               │   │
│  └──────────────────┬───────────────────────┘   │
│                     │                           │
│          persistência                           │
│                     ▼                           │
│  ┌──────────────────────────────────────────┐   │
│  │          BANCO DE DADOS                  │   │
│  │  ┌─────────────┐   ┌──────────────┐      │   │
│  │  │   SQLite    │   │  API Nuvem   │      │   │
│  │  │  (escola.db)│   │ (Firebase)   │      │   │
│  │  └─────────────┘   └──────────────┘      │   │
│  └──────────────────────────────────────────┘   │
│                                                 │
└─────────────────────────────────────────────────┘
```

## 💻 Planejamento Guiado

!!! important "Atenção"
    Neste capítulo, a seção de "Implementação" é substituída pelo planejamento detalhado do sistema. Não escreveremos código hoje, mas definiremos cada detalhe que guiará o desenvolvimento.

### Passo 1 — Entendendo o que é um Sistema de Gestão Escolar

Um sistema de gestão escolar é um software que automatiza as tarefas administrativas de uma escola. O nosso sistema focará no módulo de cadastro de alunos, permitindo que um secretário ou coordenador:

- Faça login com credenciais seguras
- Visualize um menu principal com opções de navegação
- Cadastre novos alunos (nome, idade, turma)
- Consulte a lista de alunos cadastrados
- Edite dados de um aluno existente
- Exclua um registro do sistema
- Tenha os dados salvos localmente (SQLite) e sincronizados com uma base em nuvem

É um sistema aparentemente simples, mas que exercita todos os conceitos que você aprendeu: variáveis, funções, classes, interfaces gráficas, banco de dados e arquitetura de software.

!!! note "Conceito Importante"
    Um sistema não é um programa. Um programa resolve um problema pontual. Um sistema é composto de múltiplas partes que interagem entre si (autenticação, navegação, persistência, interface) e atende a um fluxo de trabalho real.

### Passo 2 — Levantando os Requisitos Funcionais

Em desenvolvimento de software, requisitos funcionais descrevem o que o sistema deve fazer, do ponto de vista do usuário. São frases no formato: "O sistema deve...".

Vamos levantar os nossos requisitos:

**Tabela de Requisitos Funcionais (RF)**

| Código | Descrição | Módulo |
|---|---|---|
| RF01 | O sistema deve ter uma tela de login com campos de usuário e senha | Autenticação |
| RF02 | O sistema deve validar as credenciais e negar acesso em caso de erro | Autenticação |
| RF03 | O sistema deve exibir uma mensagem de erro se usuário ou senha estiverem incorretos | Autenticação |
| RF04 | Após login bem-sucedido, o sistema deve abrir o Menu Principal | Autenticação |
| RF05 | O Menu Principal deve ter botões para Cadastro, Consulta e Sair | Navegação |
| RF06 | O botão "Cadastro" deve abrir a tela de Cadastro de Alunos | Navegação |
| RF07 | O botão "Consulta" deve abrir a tela de Consulta de Alunos | Navegação |
| RF08 | O botão "Sair" deve encerrar o sistema | Navegação |
| RF09 | A tela de Cadastro deve ter um formulário com campos: Nome, Idade, Turma | CRUD |
| RF10 | A tela de Cadastro deve ter botões: Salvar, Editar, Excluir, Limpar | CRUD |
| RF11 | A tela de Cadastro deve ter uma tabela (Treeview) listando todos os alunos | CRUD |
| RF12 | O botão Salvar deve inserir um novo registro no banco de dados | CRUD |
| RF13 | O botão Editar deve permitir modificar um registro selecionado na tabela | CRUD |
| RF14 | O botão Excluir deve remover um registro selecionado com confirmação | CRUD |
| RF15 | O botão Limpar deve limpar todos os campos do formulário | CRUD |
| RF16 | Os dados devem ser persistidos em banco SQLite local (escola.db) | Persistência |
| RF17 | O sistema deve ter uma funcionalidade de sincronização com banco em nuvem | Persistência |
| RF18 | O sistema deve ser organizado em módulos separados por responsabilidade | Arquitetura |

!!! tip "Dica Profissional"
    No mercado, o levantamento de requisitos é a etapa mais crítica. Um erro aqui pode custar semanas de retrabalho. Preste atenção nos detalhes: é exatamente isso que diferencia um programador de um engenheiro de software.

### Passo 3 — O Caminho do Desenvolvimento

Construiremos o sistema de forma incremental. Cada aula adicionará uma nova camada. Ao final, tudo estará integrado. Este é o nosso roteiro:

```text
Aula 01 (hoje)      → Introdução e Planejamento
Aula 02             → Arquitetura (pastas, módulos, esqueleto MVC)
Aula 03             → Tela de Login com validação
Aula 04             → Menu Principal e navegação entre janelas
Aula 05             → Múltiplas janelas com transição controlada
Aula 06             → Tela de Cadastro com formulário e Treeview
Aula 07             → Integração com SQLite (conexão e primeiras queries)
Aula 08             → CRUD Completo (Create, Read, Update, Delete)
Aula 09             → Sincronização com banco em nuvem (Firebase)
Aula 10             → Integração final e testes
Aula 11             → Refatoração, polimento e preparação para entrega
Aula 12 (20/08)     → Apresentação dos Projetos Finais
```

!!! note "Datas importantes"
    A entrega final será no dia 20 de agosto. Guarde essa data. Tudo o que você fizer até lá contribuirá para o seu projeto.

### Passo 4 — Metodologia PBL (Project Based Learning)

Nosso curso adota o PBL — Aprendizado Baseado em Projetos. Isso significa que você não aprenderá "sobre botões" para depois usar um botão. Você aprenderá a criar o menu do sistema, e o botão fará parte natural desse processo.

```text
❌ Abordagem tradicional:  "Aula de Entry" → cria campo de texto solto
✅ Abordagem PBL:          "Vamos validar o login" → Entry faz parte da tela

❌ Abordagem tradicional:  "Aula de Treeview" → cria tabela genérica
✅ Abordagem PBL:          "Vamos listar alunos" → Treeview mostra dados reais
```

Cada capítulo deste módulo é um passo na construção do sistema. Nenhum código será descartado. Tudo o que você escrever hoje será usado amanhã e expandido depois de amanhã.

### Passo 5 — Formação das Equipes

Você trabalhará em equipe para construir o Projeto Final. Este projeto será uma adaptação do Sistema Escolar para um domínio diferente.

Exemplos de temas que as equipes podem escolher:

- Sistema de Gestão de Biblioteca (livros, autores, empréstimos)
- Sistema de Cadastro de Clientes (clientes, telefones, endereços)
- Sistema de Controle de Estoque (produtos, quantidades, fornecedores)
- Sistema de Agendamento de Consultas (pacientes, médicos, horários)
- Sistema de Gerenciamento de Tarefas (tarefas, prioridades, status)

Cada equipe deve ter 2 a 4 integrantes. Definam os papéis iniciais (quem cuidará de qual parte), mas lembrem-se: todos devem programar. Não existe "só a pessoa que digita".

!!! warning "Atenção"
    O sistema da sua equipe seguirá a mesma arquitetura do Sistema Escolar (Login, Menu, CRUD, SQLite, Nuvem). A diferença estará apenas no domínio (o que será cadastrado) e nos campos específicos. A estrutura, o fluxo e a tecnologia serão idênticas.

## 📝 Exercício

**Tempo estimado:** 15-20 minutos

**Tarefa:** Analise os requisitos funcionais (RF01 a RF18) e identifique quais funcionalidades podem ser mapeadas diretamente para os conceitos que você aprendeu nos módulos anteriores.

Preencha a tabela abaixo no seu caderno ou arquivo de anotações:

| Requisito | Conceito relacionado | Exemplo |
|---|---|---|
| RF01 — Tela de Login | Tkinter, Entry, Label, Button, grid/pack | Criar janela, posicionar widgets |
| RF... | ... | ... |
| ... | ... | ... |

**Objetivo:** Reforçar que você já possui as ferramentas necessárias para construir este sistema. Basta organizá-las.

??? hint "Dica"
    Reveja os conteúdos dos módulos 02 (Interfaces Gráficas) e 03 (Banco de Dados). Tudo o que está listado nos requisitos usa exatamente o que você já estudou: janelas, widgets, eventos, conexão SQLite, queries SQL.

??? success "Solução (exemplo)"
    | Requisito | Conceito relacionado | Exemplo |
    |---|---|---|
    | RF01 — Tela de Login | Tkinter, Entry, Label, Button, grid | `tk.Entry(janela, show="*")` |
    | RF02 — Validar credenciais | Funções, condicionais, messagebox | `if usuario == "admin" and senha == "123":` |
    | RF04 — Abrir Menu Principal | Toplevel, transição de janelas | `MenuPrincipal()` |
    | RF09 — Formulário de Cadastro | Entry, Label, Frame, grid | Campos posicionados com grid |
    | RF11 — Tabela de alunos | Treeview, Scrollbar | `ttk.Treeview(janela, columns=("nome", "idade"))` |
    | RF12 — Salvar no banco | INSERT SQL, sqlite3.connect | `cursor.execute("INSERT INTO alunos...")` |
    | RF16 — SQLite local | sqlite3, criar tabelas, CRUD | `conexao = sqlite3.connect("escola.db")` |

## 🏆 Missão da Equipe

**Tempo estimado:** 30-45 minutos

**Tarefa:** Definam o tema do Projeto Final da equipe e levantem os requisitos funcionais adaptados.

**Entregável:** Um documento (pode ser um arquivo `.md` ou uma folha de papel) contendo:

- Nome do projeto
- Nome dos integrantes e seus papéis iniciais
- Tema escolhido com breve descrição (2-3 frases)
- Lista de requisitos funcionais adaptados (mínimo 15 requisitos)

**Checklist da Missão:**

- [ ] Nome do projeto definido
- [ ] Integrantes listados (2 a 4 pessoas)
- [ ] Tema claramente descrito
- [ ] Pelo menos 15 requisitos funcionais listados
- [ ] Os requisitos cobrem Login, Menu, Cadastro, CRUD, Banco
- [ ] O professor validou o tema e os requisitos

**Exemplo de adaptação dos requisitos (Sistema de Biblioteca):**

| Código original | Adaptação |
|---|---|
| RF09 — Campos: Nome, Idade, Turma | RF09 — Campos: Título, Autor, ISBN, Ano |
| RF16 — Tabela alunos | RF16 — Tabela livros |

!!! important "Nota para o Professor"
    Verifique: Cada equipe deve ter tema único, requisitos coerentes e todos os integrantes devem saber explicar o sistema proposto.

## ⚡ Desafio

**Vá além:** Crie um fluxograma do sistema da sua equipe.

Você pode fazer isso:

- No papel, com lápis e borracha
- No computador, usando o draw.io (gratuito)

O fluxograma deve mostrar:

- Tela de Login → Menu Principal → Tela de Cadastro
- As opções do menu
- As ações disponíveis na tela de cadastro
- A conexão com o banco de dados

**Dica:** use o diagrama ASCII que vimos no capítulo como inspiração. O importante é visualizar o fluxo completo antes de começar a programar.

## ⚠️ Erros Comuns

!!! danger "Pular o planejamento"
    **Sintoma:** A equipe quer começar a programar imediatamente, sem definir requisitos.
    
    **Causa:** Ansiedade para "fazer algo" e subestimar a importância do planejamento.
    
    **Solução:** Lembre-se: 1 hora de planejamento economiza 10 horas de programação. Defina os requisitos primeiro. Eles serão seu mapa. Sem mapa, você se perde.

!!! warning "Escolher tema complexo demais"
    **Sintoma:** A equipe decide fazer um sistema com 20 telas, gráficos, relatórios, etc.
    
    **Causa:** Empolgação inicial e vontade de impressionar.
    
    **Solução:** Mantenha a mesma estrutura do Sistema Escolar (Login + Menu + CRUD + Banco). Troque apenas o domínio. A complexidade virá naturalmente. Um sistema que funciona é melhor que um sistema "incrível" que nunca fica pronto.

!!! warning "Não entender o fluxo completo"
    **Sintoma:** Aluno pergunta "Mas por que precisamos de login?" ou "O banco não pode esperar?"
    
    **Causa:** Visão fragmentada — pensar em "aulas" em vez de "sistema".
    
    **Solução:** Volte ao diagrama de fluxo deste capítulo sempre que tiver dúvidas. Cada peça tem um propósito. O login protege os dados. O menu organiza o acesso. O banco persiste as informações. Nada é opcional.

!!! danger "Má distribuição de tarefas na equipe"
    **Sintoma:** Um integrante programa tudo e os outros só assistem.
    
    **Causa:** Falta de definição clara de papéis.
    
    **Solução:** Definam quem será responsável por cada módulo (views, controllers, database), mas façam rotação. Todos devem passar por todas as camadas. O objetivo é que todos aprendam tudo.

## 💡 Boas Práticas

**1. Comece pelo "O QUÊ", depois vá para o "COMO"**

Antes de escrever uma linha de código, saiba o que o sistema deve fazer. Os requisitos funcionais são o seu contrato. No mercado, desenvolvedores que ignoram requisitos entregam software que ninguém pediu.

**2. Documente desde o início**

Sua equipe deve manter um arquivo `README.md` na raiz do projeto. Nele, registrem:

- O objetivo do sistema
- Os integrantes
- Os requisitos funcionais
- O cronograma da equipe

Isso é o que empresas esperam de um desenvolvedor profissional.

**3. Mantenha o escopo sob controle**

É tentador adicionar "funcionalidades extras". Resista. Primeiro, faça o básico funcionar perfeitamente. Depois, se houver tempo, adicione melhorias. Um sistema simples que funciona vale mais que um sistema complexo e quebrado.

**4. Use controle de versão (Git)**

Se possível, criem um repositório no GitHub para o projeto da equipe. Façam commits frequentes. Isso evita perda de código e ensina o fluxo de trabalho profissional.

**5. Comunicação constante**

Conversem sobre o que estão fazendo. Se alguém travou, peça ajuda. Se alguém terminou, ajude o colega. No mercado, ninguém trabalha isolado.

## ☑️ Checklist

Antes de prosseguir para o próximo capítulo, confirme:

- [ ] Entendi o escopo completo do Sistema Escolar
- [ ] Li e compreendi todos os 18 requisitos funcionais
- [ ] Sei a diferença entre programar exercícios e desenvolver um sistema
- [ ] Entendi como a metodologia PBL funciona neste módulo
- [ ] Minha equipe está formada (2 a 4 integrantes)
- [ ] Definimos o tema do Projeto Final da equipe
- [ ] Listamos pelo menos 15 requisitos funcionais adaptados
- [ ] O professor validou nosso tema e requisitos
- [ ] Tenho anotada a data de entrega: 20 de agosto
- [ ] Compreendi o cronograma das próximas aulas

## ➡️ Próximo Capítulo

No **Capítulo 02 — Arquitetura do Sistema**, você finalmente colocará a mão no código!

Vamos criar a estrutura de pastas do projeto, entender o padrão MVC (Model-View-Controller) e construir o esqueleto que sustentará todo o desenvolvimento futuro. Você aprenderá por que separar o código em módulos não é frescura — é necessidade.

Prepare-se: revise o conceito de imports em Python, criação de pacotes (`__init__.py`) e o básico de classes. Tudo isso será usado já na próxima aula.

Até lá, mantenha o foco. Você está a um passo de se tornar um desenvolvedor de verdade. 🚀
