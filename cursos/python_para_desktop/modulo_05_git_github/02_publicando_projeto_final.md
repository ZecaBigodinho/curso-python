# 02 — Publicando o Projeto Final

## 🎯 Objetivo

Neste capítulo você vai transformar o repositório do seu Projeto Final em algo **profissional e digno de portfólio** — com README completo, badges, screenshots, release versionada e documentação gerada com ajuda de IA.

Ao final, você terá:

- Commits organizados com mensagens profissionais padronizadas
- Um README.md completo com badges, screenshots, tabela de tecnologias e instruções
- Uma release v1.0.0 publicada no GitHub
- Documentação de qualidade gerada com auxílio de Inteligência Artificial
- O perfil do GitHub configurado como portfólio profissional
- O repositório 100% pronto para ser apresentado a um recrutador

## 📍 Contextualização

No capítulo anterior, você criou o repositório, aprendeu Git e toda a equipe está fazendo commits. O fluxo técnico funciona. Mas se um recrutador acessar seu GitHub agora, o que ele vai ver?

Provavelmente: um README com uma linha, commits com mensagens como "update" e "fix", e nenhuma organização visual. Isso é como entregar um currículo escrito à mão em papel amassado — o conteúdo pode ser bom, mas a apresentação mata.

Neste capítulo, vamos polir tudo. No mercado de trabalho, o GitHub é o seu **portfólio vivo**. Recrutadores técnicos olham seus repositórios antes mesmo de ligar para uma entrevista. Um projeto bem documentado comunica: "essa pessoa é organizada, profissional e se importa com qualidade".

## ✅ Resultado Esperado

Ao final deste capítulo, seu README.md será assim:

```text
┌──────────────────────────────────────────────────────────┐
│                                                          │
│  # 🎓 Sistema Escolar                                    │
│                                                          │
│  [badge: Python 3.10+] [badge: Status: Concluído]       │
│  [badge: License: MIT] [badge: Version: v1.0.0]         │
│                                                          │
│  > Sistema desktop para gerenciamento de alunos com      │
│  > interface gráfica, banco de dados e sincronização     │
│  > em nuvem.                                             │
│                                                          │
│  [📸 Screenshot do sistema]                              │
│                                                          │
│  ## ✨ Funcionalidades                                    │
│  - ✅ Login com autenticação                              │
│  - ✅ CRUD completo de alunos                            │
│  - ✅ Banco SQLite + sincronização Firebase              │
│  ...                                                     │
│                                                          │
│  ## 🚀 Como executar                                     │
│  1. Clone o repositório                                  │
│  2. Instale as dependências                              │
│  3. Configure o .env                                     │
│  4. Execute: python main.py                              │
│                                                          │
│  ## 🛠️ Tecnologias                                      │
│  Python | Tkinter | SQLite | Firebase                    │
│                                                          │
│  ## 👥 Autores                                           │
│  João Silva — Maria Santos — Pedro Oliveira              │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

E a aba **Releases** mostrará:

```text
v1.0.0 — Sistema Escolar (Versão Final)
Publicada em: Agosto 2026

📋 O que está incluído:
- Tela de login com validação
- CRUD completo de alunos
- Banco de dados SQLite
- Sincronização com Firebase
- Interface CustomTkinter
```

## 💻 Implementação Guiada

### Passo 1 — Commits profissionais

Até agora, você fez commits com mensagens simples. No mercado, existe um padrão chamado **Conventional Commits** que organiza as mensagens por tipo:

```text
tipo: descrição curta do que foi feito

Tipos mais comuns:
  feat:   → Nova funcionalidade
  fix:    → Correção de bug
  docs:   → Documentação
  style:  → Formatação (sem mudar lógica)
  refactor: → Refatoração de código
  test:   → Adição de testes
  chore:  → Tarefas de manutenção
```

Exemplos reais para o Projeto Final:

```bash
git commit -m "feat: adiciona tela de cadastro de alunos"
git commit -m "fix: corrige validação de idade negativa"
git commit -m "docs: atualiza README com instruções de uso"
git commit -m "style: organiza imports do módulo views"
git commit -m "refactor: separa lógica de CRUD em módulo próprio"
```

!!! tip "Dica Profissional"
    Se você olhar os repositórios de grandes projetos open-source (React, Django, Linux), todos seguem esse padrão. Adotá-lo agora cria um hábito que vai te acompanhar por toda a carreira.

**Revisando o histórico:**

Para ver todos os commits do projeto:

```bash
# No terminal:
git log --oneline

# Resultado:
# a1b2c3d feat: adiciona sincronização com Firebase
# e4f5g6h feat: implementa CRUD completo
# i7j8k9l feat: conecta SQLite ao cadastro
# m0n1o2p feat: cria tela de cadastro de alunos
# q3r4s5t feat: adiciona código inicial do projeto
```

No GitHub, vá na aba **Commits** para ver o histórico visual com autor, data e mensagem de cada commit.

### Passo 2 — Organizando o repositório

Antes de montar o README, garanta que o repositório está organizado:

```text
sistema-escolar/
├── .env.example          # ← Template do .env (sem senhas)
├── .gitignore            # ← Arquivos ignorados
├── LICENSE               # ← Licença MIT
├── README.md             # ← Documentação principal
├── requirements.txt      # ← Dependências do projeto
├── main.py               # ← Ponto de entrada
├── controllers/          # ← Lógica de negócio
│   ├── __init__.py
│   ├── auth.py
│   └── aluno.py
├── database/             # ← Persistência de dados
│   ├── __init__.py
│   ├── conexao.py
│   └── operacoes.py
├── views/                # ← Interface gráfica
│   ├── __init__.py
│   ├── login.py
│   ├── menu.py
│   └── cadastro.py
└── utils/                # ← Funções auxiliares
    ├── __init__.py
    └── helpers.py
```

Verifique que o `requirements.txt` lista todas as dependências:

```text
customtkinter>=5.0.0
python-dotenv>=1.0.0
firebase-admin>=6.0.0
```

E que o `.env.example` existe como template:

```text
# Copie este arquivo para .env e preencha
FIREBASE_DATABASE_URL=
FIREBASE_CREDENTIALS=
```

### Passo 3 — README profissional (template completo)

Substitua o conteúdo do `README.md` pelo template abaixo, adaptando para o projeto da sua equipe:

```markdown
# 🎓 Sistema Escolar

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Concluído-00bfa5?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)

> Sistema desktop para gerenciamento de alunos
> com interface gráfica moderna, banco de dados
> local e sincronização em nuvem.

## 📸 Screenshots

<!-- Insira imagens aqui -->
<!-- ![Tela de Login](screenshots/login.png) -->
<!-- ![Cadastro](screenshots/cadastro.png) -->

## ✨ Funcionalidades

- 🔐 Login com autenticação de usuário
- 📋 Menu principal com navegação
- 📝 Cadastro completo de alunos (CRUD)
- 🔍 Busca com filtro por nome
- 💾 Persistência local com SQLite
- ☁️ Sincronização com Firebase
- 🎨 Interface moderna com CustomTkinter

## 🚀 Como executar

### Pré-requisitos
- Python 3.10 ou superior
- pip atualizado

### Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/sistema-escolar.git
   cd sistema-escolar
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure as variáveis de ambiente:
   ```bash
   cp .env.example .env
   # Edite o .env com suas credenciais
   ```

4. Execute o sistema:
   ```bash
   python main.py
   ```

## 🛠️ Tecnologias

| Tecnologia | Uso |
|------------|-----|
| Python 3.10+ | Linguagem principal |
| CustomTkinter | Interface gráfica |
| SQLite | Banco de dados local |
| Firebase | Banco de dados em nuvem |
| python-dotenv | Variáveis de ambiente |

## 📂 Estrutura do Projeto

```text
sistema-escolar/
├── main.py
├── controllers/
├── database/
├── views/
└── utils/
```

## 👥 Autores

| Nome | GitHub |
|------|--------|
| João Silva | [@joaosilva](https://github.com/joaosilva) |
| Maria Santos | [@mariasantos](https://github.com/mariasantos) |

## 📝 Licença

Este projeto está sob a licença MIT.
Veja [LICENSE](LICENSE) para mais detalhes.
```

!!! note "Conceito Importante"
    O README é renderizado automaticamente pelo GitHub na página principal do repositório. Ele aceita Markdown — a mesma formatação que você usou durante todo o curso para ler o material. Tudo que aparece no site do curso (títulos, tabelas, blocos de código, emojis) funciona no README.

### Passo 4 — Badges (selos visuais)

Badges são aqueles selos coloridos no topo do README. Eles comunicam informações rapidamente:

```text
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
```

O site **shields.io** gera badges personalizados. A estrutura da URL é:

```text
https://img.shields.io/badge/TEXTO-VALOR-COR?style=ESTILO&logo=LOGO

Exemplos prontos para copiar:

# Linguagem
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)

# Status do projeto
![Status](https://img.shields.io/badge/Status-Concluído-00bfa5?style=flat-square)
![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow?style=flat-square)

# Licença
![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)

# Versão
![Version](https://img.shields.io/badge/Version-1.0.0-orange?style=flat-square)
```

!!! tip "Dica Profissional"
    Não exagere nos badges — 3 a 5 é o ideal. Os mais importantes são: linguagem, status e licença. Badges demais poluem o README e perdem o efeito visual.

### Passo 5 — Screenshots e imagens

Um README com imagens é muito mais atrativo. Para adicionar screenshots:

1. Crie uma pasta `screenshots/` no repositório
2. Tire prints do sistema funcionando (login, cadastro, listagem)
3. Salve como `.png` na pasta `screenshots/`
4. No README, use:

```markdown
## 📸 Screenshots

### Tela de Login
![Tela de Login](screenshots/login.png)

### Cadastro de Alunos
![Cadastro](screenshots/cadastro.png)
```

**Como tirar screenshots no Windows:**

- `Win + Shift + S` → selecione a área → cole no Paint → salve como PNG
- Ou use a Ferramenta de Captura (Snipping Tool)

### Passo 6 — Criando uma Release (v1.0.0)

Uma **Release** é uma versão oficial do projeto, empacotada e marcada. No mercado, é assim que softwares são distribuídos.

No GitHub:

1. Vá na aba **Releases** (lado direito da página do repositório)
2. Clique em **Create a new release**
3. Em **Tag version**, digite: `v1.0.0`
4. Em **Release title**, digite: `v1.0.0 — Sistema Escolar`
5. Na descrição, liste as funcionalidades:

```markdown
## 🎉 Primeira versão do Sistema Escolar

### ✨ Funcionalidades
- 🔐 Tela de login com autenticação
- 📋 Menu principal com navegação entre telas
- 📝 Cadastro completo de alunos (CRUD)
- 🔍 Busca com filtro por nome
- 💾 Persistência local com SQLite
- ☁️ Sincronização com Firebase

### 🛠️ Tecnologias
- Python 3.10+
- CustomTkinter
- SQLite / Firebase

### 👥 Equipe
- João Silva
- Maria Santos
- Pedro Oliveira

### 📦 Como usar
1. Baixe o código-fonte (Source code .zip)
2. Extraia e execute: `python main.py`
```

6. Clique em **Publish release**

!!! note "Conceito Importante"
    **Versionamento semântico** (SemVer) usa o formato `vMAJOR.MINOR.PATCH`:
    
    - `v1.0.0` → Primeira versão estável
    - `v1.1.0` → Nova funcionalidade adicionada
    - `v1.0.1` → Correção de bug na versão 1.0.0
    - `v2.0.0` → Mudanças grandes e incompatíveis
    
    Para o Projeto Final, `v1.0.0` é perfeito.

### Passo 7 — Usando IA para gerar documentação

Uma das habilidades mais valiosas de um desenvolvedor moderno é saber **usar IA como ferramenta de produtividade**. Gerar documentação é um dos melhores casos de uso.

**Prompt para gerar README:**

Copie e cole o template abaixo em qualquer IA (ChatGPT, Gemini, Claude, DeepSeek):

```text
Eu criei um projeto em Python chamado [NOME DO PROJETO].

Aqui está a estrutura de arquivos:
[COLE A SAÍDA DE: tree /f OU liste os arquivos]

Aqui está o main.py:
[COLE O CÓDIGO DO MAIN.PY]

Gere um README.md profissional em português com:
- Título com emoji
- Badges (Python, Status, License)
- Descrição do projeto (2-3 linhas)
- Lista de funcionalidades com emojis
- Instruções de instalação e execução
- Tabela de tecnologias utilizadas
- Estrutura do projeto
- Seção de autores
- Licença MIT

Use Markdown formatado para GitHub.
```

!!! tip "Dica Profissional"
    A IA gera um **rascunho excelente** em segundos. Mas sempre revise: corrija nomes, verifique se as instruções realmente funcionam, e personalize o texto. A IA é sua assistente, não sua substituta.

**Prompt para gerar docstrings:**

```text
Adicione docstrings profissionais em português para
todas as funções do seguinte código Python.
Use o formato Google Style.
Explique o que cada função faz, seus parâmetros e
o que retorna.

[COLE O CÓDIGO]
```

**Prompt para gerar comentários:**

```text
Adicione comentários explicativos em português para
o seguinte código Python.
Os comentários devem explicar a INTENÇÃO do código
(por que ele faz isso), não a sintaxe.
Use o estilo de primeira pessoa: "Eu faço X porque Y".

[COLE O CÓDIGO]
```

**Prompt para gerar .env.example:**

```text
Analise o seguinte código Python e identifique todas
as variáveis de ambiente usadas (os.getenv ou
os.environ). Gere um arquivo .env.example com todas
as variáveis listadas, valores de placeholder e
comentários explicando cada uma.

[COLE O CÓDIGO]
```

### Passo 8 — Criando seu README Pessoal de Perfil

Seu perfil do GitHub é seu **cartão de visita profissional**. Recrutadores olham seu perfil antes de ligar para uma entrevista. Vamos configurá-lo:

**Configuração básica do perfil:**

1. **Foto de perfil** — use uma foto profissional ou um avatar decente
2. **Bio** — escreva uma frase sobre você: "Estudante de Desenvolvimento de Sistemas | Python | Desktop & Web"
3. **Repositórios fixados (Pinned)** — no seu perfil, clique em "Customize your pins" e selecione os melhores projetos (máximo 6). Coloque o Projeto Final em primeiro!

**Criando o README especial de perfil:**

O GitHub permite criar um README que aparece na página principal do seu perfil. Para isso:

1. Crie um repositório com o **mesmo nome do seu usuário** (ex: se seu usuário é `joaosilva`, crie o repositório `joaosilva`)
2. O GitHub mostrará: *"joaosilva/joaosilva is a ✨ special ✨ repository"*
3. Marque **Add a README file** e clique em **Create repository**
4. Edite o `README.md` com o template abaixo

**Template completo com gráficos e stats:**

```markdown
<div align="center">

# Olá! 👋 Eu sou [Seu Nome]

🎓 Estudante de Desenvolvimento de Sistemas
🐍 Apaixonado por Python | 💻 Desktop & Web

</div>

---

## 🚀 Sobre mim

- 🔭 Estou trabalhando no **Sistema Escolar** (Python + Tkinter + SQLite)
- 🌱 Estou aprendendo **Python, Git, Banco de Dados e Interfaces Gráficas**
- 💬 Pergunte-me sobre **Python, Tkinter e CustomTkinter**
- 📫 Como me encontrar: **seu@email.com**

---

## 🔧 Tecnologias e Ferramentas

![Python](https://img.shields.io/badge/-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Git](https://img.shields.io/badge/-Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/-GitHub-181717?style=for-the-badge&logo=github&logoColor=white)
![VS Code](https://img.shields.io/badge/-VS_Code-007ACC?style=for-the-badge&logo=visual-studio-code&logoColor=white)

---

## 📊 GitHub Stats

<div align="center">

![GitHub Stats](https://github-readme-stats.vercel.app/api?username=SEU_USUARIO&show_icons=true&theme=tokyonight&hide_border=true&count_private=true)

![Top Languages](https://github-readme-stats.vercel.app/api/top-langs/?username=SEU_USUARIO&layout=compact&theme=tokyonight&hide_border=true)

</div>

---

## 🔥 Streak de Commits

<div align="center">

![GitHub Streak](https://streak-stats.demolab.com/?user=SEU_USUARIO&theme=tokyonight&hide_border=true)

</div>

---

## 📌 Projetos em Destaque

<div align="center">

[![Sistema Escolar](https://github-readme-stats.vercel.app/api/pin/?username=SEU_USUARIO&repo=sistema-escolar&theme=tokyonight&hide_border=true)](https://github.com/SEU_USUARIO/sistema-escolar)

[![Gerenciador de Tarefas](https://github-readme-stats.vercel.app/api/pin/?username=SEU_USUARIO&repo=gerenciador-tarefas&theme=tokyonight&hide_border=true)](https://github.com/SEU_USUARIO/gerenciador-tarefas)

</div>

---

## 📈 Gráfico de Atividade

![Activity Graph](https://github-readme-activity-graph.vercel.app/graph?username=SEU_USUARIO&theme=tokyo-night&hide_border=true)

---

## 📫 Contato

[![Email](https://img.shields.io/badge/-Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:seu@email.com)
[![LinkedIn](https://img.shields.io/badge/-LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/seu-perfil)

---

<div align="center">

![Visitors](https://komarev.com/ghpvc/?username=SEU_USUARIO&color=blueviolet&style=flat-square)

</div>
```

!!! warning "Importante"
    Substitua **`SEU_USUARIO`** pelo seu nome de usuário do GitHub em **todos** os lugares do template. Se seu usuário é `joaosilva`, troque `SEU_USUARIO` por `joaosilva`.

**O que cada card faz:**

| Card | O que mostra | Serviço |
|------|-------------|---------|
| **GitHub Stats** | Total de commits, PRs, issues, stars e contribuições | `github-readme-stats` |
| **Top Languages** | Linguagens mais usadas nos seus repositórios | `github-readme-stats` |
| **Streak** | Dias consecutivos com commits (sequência atual e recorde) | `streak-stats.demolab.com` |
| **Pin Cards** | Cartões clicáveis dos seus repositórios (como botões) | `github-readme-stats` |
| **Activity Graph** | Gráfico de ondas com sua atividade dos últimos 30 dias | `github-readme-activity-graph` |
| **Visitors** | Contador de visitas ao seu perfil | `komarev.com` |

!!! tip "Dica Profissional"
    Os temas disponíveis para os cards incluem: `tokyonight`, `dracula`, `radical`, `merko`, `gruvbox`, `onedark`, `dark`. Experimente trocar `theme=tokyonight` por outro tema para personalizar o visual. A lista completa está em [github-readme-stats themes](https://github.com/anuraghazra/github-readme-stats/blob/master/themes/README.md).

**Prompt para a IA gerar seu README de perfil:**

```text
Crie um README.md para meu perfil pessoal do GitHub.

Meu nome: [SEU NOME]
Meu usuário GitHub: [SEU_USUARIO]
Meu curso: Desenvolvimento de Sistemas
Tecnologias que sei: Python, Tkinter, CustomTkinter, SQLite, Git
Meus projetos:
- Sistema Escolar (repo: sistema-escolar) — App desktop com CRUD e banco
- Gerenciador de Tarefas (repo: gerenciador-tarefas) — App web com Streamlit

Inclua:
- Saudação com emoji
- Seção "Sobre mim" com bullets
- Badges de tecnologias (style=for-the-badge)
- GitHub Stats card (github-readme-stats, theme tokyonight)
- Top Languages card (layout compact)
- GitHub Streak (streak-stats.demolab.com)
- Pin cards clicáveis para cada projeto
- Activity Graph (github-readme-activity-graph)
- Seção de contato com badges de email e LinkedIn
- Contador de visitas (komarev.com)
- Tudo centralizado com <div align="center">
- Use Markdown formatado para GitHub

Escreva em português do Brasil.
```

### Passo 9 — Checklist final de entrega do projeto

Antes de considerar o projeto "entregue", passe por este checklist completo:

**Código:**

- [ ] O sistema executa sem erros (`python main.py`)
- [ ] Todas as funcionalidades estão implementadas
- [ ] O login funciona com credenciais válidas
- [ ] O CRUD completo funciona (criar, ler, editar, excluir)
- [ ] O `.env` está configurado corretamente
- [ ] Não há senhas ou credenciais no código-fonte

**Repositório:**

- [ ] README.md completo com badges, descrição e instruções
- [ ] .gitignore configurado (`.env`, `__pycache__/`, `*.db`)
- [ ] .env.example presente como template
- [ ] LICENSE MIT presente
- [ ] requirements.txt com todas as dependências
- [ ] Screenshots na pasta `screenshots/`
- [ ] Release v1.0.0 publicada

**Histórico:**

- [ ] Commits com mensagens descritivas (não "update" ou "fix")
- [ ] Todos os membros da equipe têm commits no histórico
- [ ] Nenhum arquivo sensível no histórico (`.env`, credenciais)

**Apresentação:**

- [ ] Cada membro sabe explicar sua parte do código
- [ ] O sistema pode ser demonstrado ao vivo
- [ ] O repositório está público (ou pronto para ser tornado público)

!!! warning "Atenção"
    O professor vai verificar o repositório no GitHub. Além do código funcionando, a qualidade do repositório (README, organização, commits) faz parte da avaliação. Capriche!

## 📝 Exercício

**Tempo estimado:** 15-20 minutos

**Tarefa:** Use uma IA (ChatGPT, Gemini, Claude ou DeepSeek) para gerar o README do seu Projeto Final. Siga estas etapas:

1. Copie a estrutura de arquivos do seu projeto (`tree /f` no terminal)
2. Copie o código do `main.py`
3. Use o prompt do Passo 7 para pedir o README à IA
4. Revise o resultado: corrija nomes, verifique instruções, personalize
5. Substitua o README.md do repositório
6. Faça commit: `docs: adiciona README profissional gerado com IA`
7. Faça push e verifique no GitHub

??? hint "Dica"
    Se a IA gerar um README em inglês, adicione ao prompt: "Escreva 100% em português do Brasil." Se o resultado for muito genérico, cole mais código (não apenas o main.py) para dar mais contexto. Quanto mais informação a IA receber, melhor será o resultado.

??? success "Solução resumida"
    O README gerado pela IA será um bom ponto de partida. Ajustes comuns que você precisará fazer:
    
    - Corrigir o nome do projeto e dos autores
    - Ajustar as instruções de instalação para seu caso específico
    - Adicionar ou remover funcionalidades da lista
    - Substituir placeholders de screenshots por imagens reais
    - Verificar se os badges estão com as informações corretas
    
    Após revisar, faça o commit e push normalmente.

## 🏆 Missão da Equipe

**Tempo estimado:** 30-45 minutos

**Tarefa:** Finalizem o repositório do Projeto Final com qualidade profissional.

**Entregável:** Repositório no GitHub com:

- README.md completo (badges, screenshots, instruções, autores)
- Release v1.0.0 publicada
- Todos os membros com commits significativos
- Código organizado e funcional

**Checklist da Missão:**

- [ ] README.md reescrito com template profissional
- [ ] Pelo menos 3 badges no README (Python, Status, License)
- [ ] Pelo menos 1 screenshot do sistema no README
- [ ] Instruções de instalação testadas (outro membro seguiu e funcionou)
- [ ] requirements.txt atualizado
- [ ] .env.example presente
- [ ] Release v1.0.0 criada com descrição das funcionalidades
- [ ] Todos os commits seguem o padrão `tipo: descrição`
- [ ] Repositório organizado (sem arquivos soltos na raiz)
- [ ] O professor verificou o repositório e aprovou

!!! important "Nota para o Professor"
    Verifique: Acesse o repositório de cada equipe no GitHub. O README deve renderizar corretamente com badges visíveis, instruções claras e screenshots. Na aba Releases, deve haver pelo menos a v1.0.0. No histórico de commits, todos os membros devem ter contribuições. Peça que um membro clone o repositório "do zero" em outra pasta e siga as instruções do README — se funcionar, a documentação está boa.

## ⚡ Desafio

**Vá além:** Crie o README especial do seu perfil no GitHub.

1. Crie um repositório com o **mesmo nome do seu usuário** no GitHub
2. Adicione um `README.md` com sua apresentação pessoal
3. Inclua badges das tecnologias que você sabe
4. Liste seus projetos em destaque (com links)
5. Adicione formas de contato (e-mail, LinkedIn)

Quando alguém acessar `github.com/seu-usuario`, verá essa apresentação. É o seu cartão de visita para o mundo tech.

**Desafio extra:** Use a IA para gerar também:

- Docstrings para todas as funções do seu projeto
- Um arquivo `CONTRIBUTING.md` explicando como contribuir
- Um `CHANGELOG.md` listando todas as versões e mudanças

## ⚠️ Erros Comuns

!!! danger "README não renderiza corretamente"
    **Sintoma:** Badges aparecem como texto, tabelas desformatadas, imagens quebradas.
    
    **Causa:** Erro de sintaxe Markdown — falta de linha em branco entre seções, URL incorreta nos badges, ou caminho errado para imagens.
    
    **Solução:** Verifique a prévia no GitHub (aba "Preview" ao editar o README). Cada seção precisa de uma linha em branco antes e depois. URLs de badges devem começar com `https://img.shields.io/badge/`. Caminhos de imagens devem ser relativos à raiz do repositório (ex: `screenshots/login.png`).

!!! warning "Screenshots muito grandes ou pesadas"
    **Sintoma:** As imagens demoram para carregar ou aparecem gigantes no README.
    
    **Causa:** Screenshots em resolução muito alta (4K) ou formato BMP/TIFF.
    
    **Solução:** Use PNG para screenshots e redimensione para no máximo 800px de largura. Ferramentas online como tinypng.com comprimem imagens sem perder qualidade.

!!! warning "Release sem tag ou com tag errada"
    **Sintoma:** A release não aparece na aba Releases ou mostra a tag errada.
    
    **Causa:** A tag não foi criada corretamente. O formato deve ser `v1.0.0` (com o "v" minúsculo).
    
    **Solução:** Ao criar a release no GitHub, o campo "Tag version" cria a tag automaticamente. Digite exatamente `v1.0.0`. Se errou, pode deletar a release e criar novamente.

!!! danger "IA gerou informações incorretas no README"
    **Sintoma:** O README menciona funcionalidades que não existem, bibliotecas que não são usadas, ou instruções que não funcionam.
    
    **Causa:** A IA gera texto plausível, não necessariamente correto. Ela "inventa" detalhes quando não tem contexto suficiente.
    
    **Solução:** SEMPRE revise o que a IA gerar. Teste as instruções de instalação. Verifique se as funcionalidades listadas realmente existem. A IA é uma ferramenta, não uma autoridade — a responsabilidade final é sua.

## 💡 Boas Práticas

**1. O README é a porta de entrada**

Um recrutador gasta em média 30 segundos olhando um repositório. Se o README estiver vazio ou confuso, ele fecha a aba. Se estiver bonito, organizado e com screenshots — ele continua lendo. Invista tempo no README.

**2. Commits contam uma história**

O histórico de commits de um projeto mostra como ele evoluiu. Commits claros e bem escritos demonstram maturidade profissional. Um recrutador que olha o histórico e vê `feat: adiciona validação de e-mail` pensa diferente de quem vê `asdfgh`.

**3. IA como aceleradora, não substituta**

Use IA para gerar rascunhos de documentação, sugerir melhorias e automatizar tarefas repetitivas. Mas nunca publique algo gerado por IA sem revisar. A IA erra, inventa e alucina — e a responsabilidade pelo código publicado é sempre sua.

**4. Portfólio é construção contínua**

Não espere ter 10 projetos para começar a montar seu portfólio. Um único projeto bem documentado vale mais que 20 repositórios vazios. Comece com o Projeto Final e vá adicionando projetos ao longo da sua carreira.

**5. Torne público quando estiver pronto**

Mantenha o repositório privado durante o desenvolvimento. Quando estiver com README completo, código organizado e release publicada — torne público. Primeira impressão importa, e não dá para "des-publicar" um repositório bagunçado.

## ☑️ Checklist

Antes de considerar este módulo concluído, confirme:

- [ ] Todos os commits seguem o padrão `tipo: descrição`
- [ ] README.md completo com badges, descrição e instruções
- [ ] Pelo menos 1 screenshot do sistema no README
- [ ] Tabela de tecnologias presente no README
- [ ] Seção de autores com links do GitHub de cada membro
- [ ] .env.example presente como template
- [ ] requirements.txt atualizado com todas as dependências
- [ ] Release v1.0.0 publicada com descrição das funcionalidades
- [ ] Repositório organizado (pastas controllers/, database/, views/, utils/)
- [ ] Nenhum arquivo sensível exposto (`.env`, credenciais, `.db`)
- [ ] Perfil do GitHub com foto, bio e repositório fixado
- [ ] Minha equipe concluiu a Missão da Equipe
- [ ] O repositório está pronto para ser mostrado a um recrutador 🎯

## ➡️ Conclusão

Parabéns! 🎉 Você concluiu o Módulo Bônus de Git & GitHub.

Vamos recapitular o que você conquistou ao longo de todo o curso:

| Módulo | O que você aprendeu |
|--------|-------------------|
| 01 — Fundamentos | Programar em Python com confiança |
| 02 — Interfaces | Criar aplicações desktop com Tkinter |
| 03 — Banco de Dados | Persistir dados com SQLite e .env |
| 04 — Projeto Final | Construir um sistema completo do zero |
| 05 — Git & GitHub | Versionar, colaborar e apresentar seu trabalho |

Você entrou no curso sem saber o que era uma variável. Agora tem um **sistema desktop funcional**, hospedado num **repositório profissional**, com **release publicada** e pronto para o seu **portfólio**.

O mercado de trabalho está esperando por você. O primeiro passo já foi dado — agora é continuar construindo. 🚀

!!! tip "Próximos passos"
    - Mantenha o GitHub ativo — contribua para projetos, mesmo que pequenos
    - Aprenda **GitHub Actions** para automatizar testes e deploys
    - Explore **branches** e **Pull Requests** para fluxos de trabalho avançados
    - Considere aprender **Docker** para empacotar suas aplicações
    - Construa mais projetos e adicione ao seu portfólio
