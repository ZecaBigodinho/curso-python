# 01 — Criando um Projeto Profissional

## 🎯 Objetivo

Neste capítulo você vai aprender a usar **Git e GitHub** para versionar, organizar e compartilhar o código do seu projeto — da mesma forma que desenvolvedores profissionais fazem no mercado de trabalho.

Ao final, você terá:

- Uma conta no GitHub configurada
- Um repositório profissional criado para o Projeto Final da equipe
- O arquivo `README.md` descrevendo o projeto
- O `.gitignore` protegendo arquivos desnecessários
- A `LICENSE` definindo os termos de uso
- O GitHub Desktop instalado e configurado
- Os 5 comandos essenciais do Git dominados no terminal
- Todos os membros da equipe com acesso ao repositório
- O primeiro commit e push realizados

## 📍 Contextualização

Até agora, todo o código que você escreveu ficou salvo apenas no seu computador. Se o HD queimar, se você acidentalmente apagar uma pasta, ou se quiser compartilhar o projeto com um colega — não tem como. Além disso, quando duas pessoas trabalham no mesmo projeto, como garantir que uma não apague o código da outra?

Essas são exatamente as dores que o **Git** resolve. E o **GitHub** leva isso para a nuvem — permitindo que equipes inteiras trabalhem no mesmo projeto, de qualquer lugar, com histórico completo de todas as mudanças.

Toda empresa de tecnologia usa Git. Não importa se é uma startup de 3 pessoas ou uma big tech como Google, Meta ou Nubank — Git é o padrão universal. Aprender a usá-lo agora é investir diretamente na sua empregabilidade.

## ✅ Resultado Esperado

Ao final deste capítulo, seu repositório no GitHub terá esta estrutura:

```text
projeto-final-equipe/
├── .gitignore          # Arquivos ignorados pelo Git
├── LICENSE             # Licença do projeto
├── README.md           # Descrição do projeto
├── requirements.txt    # Dependências Python
├── main.py             # Ponto de entrada
├── database/           # Módulo de banco de dados
├── views/              # Módulo de interface
├── controllers/        # Módulo de lógica
└── utils/              # Módulo de utilitários
```

E a página do repositório no GitHub mostrará:

```text
┌──────────────────────────────────────────────────────────┐
│  📂 projeto-final-equipe                                 │
│  ★ 0  🔀 0  📋 MIT License                              │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  📁 controllers/                                         │
│  📁 database/                                            │
│  📁 utils/                                               │
│  📁 views/                                               │
│  📄 .gitignore                                           │
│  📄 LICENSE                                              │
│  📄 README.md                                            │
│  📄 main.py                                              │
│  📄 requirements.txt                                     │
│                                                          │
│  ──────────────────────────────────────────────────────── │
│                                                          │
│  # 🎓 Sistema Escolar                                    │
│  Aplicação desktop para gerenciamento de alunos...       │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

## 💻 Implementação Guiada

### Passo 1 — O que é Git?

Imagine que você está escrevendo um TCC. No primeiro dia, você salva o arquivo como `tcc_v1.docx`. No segundo dia, faz alterações e salva como `tcc_v2.docx`. No terceiro dia, `tcc_final.docx`. No quarto, `tcc_final_revisado.docx`. No quinto, `tcc_FINAL_DEFINITIVO_v3.docx`.

Parece familiar? Esse é o "controle de versão manual" — e é um desastre.

O **Git** resolve isso de forma profissional:

```text
Sem Git (caos):                    Com Git (profissional):
                                   
tcc_v1.docx                        tcc.docx  ← um único arquivo
tcc_v2.docx                          │
tcc_final.docx                       ├── commit 1: "Versão inicial"
tcc_final_revisado.docx               ├── commit 2: "Adiciona capítulo 2"
tcc_FINAL_DEFINITIVO_v3.docx          ├── commit 3: "Corrige referências"
tcc_AGORA_VAI.docx                    └── commit 4: "Versão final"
```

Com o Git, você mantém **um único arquivo** e registra cada mudança como um **commit** — um ponto de salvamento com data, autor e descrição. Pode voltar a qualquer versão anterior a qualquer momento.

!!! note "Conceito Importante"
    **Git** é um sistema de controle de versão distribuído. Ele roda no seu computador (local) e registra o histórico completo de todas as alterações do projeto. Foi criado em 2005 por Linus Torvalds — o mesmo criador do Linux.

### Passo 2 — O que é GitHub?

Se o Git é o **caderno de anotações** (local, no seu computador), o GitHub é a **nuvem** onde você guarda uma cópia desse caderno — acessível de qualquer lugar.

```text
┌──────────────┐         ┌──────────────┐
│  Seu PC      │  push   │   GitHub     │
│              │────────▶│              │
│  Git (local) │         │  Git (nuvem) │
│              │◀────────│              │
│              │  pull   │              │
└──────────────┘         └──────────────┘
```

- **push** = enviar suas mudanças para o GitHub
- **pull** = baixar as mudanças que outros fizeram

!!! tip "Dica Profissional"
    GitHub não é o único serviço desse tipo. Existem GitLab, Bitbucket e Azure DevOps. Mas o GitHub é o mais popular — com mais de 100 milhões de desenvolvedores. É onde recrutadores procuram candidatos e onde empresas hospedam projetos open-source.

### Passo 3 — Criando sua conta no GitHub

1. Acesse **github.com**
2. Clique em **Sign up**
3. Preencha: e-mail, senha e nome de usuário
4. Escolha um nome de usuário profissional (evite nomes como "xX_gamer_2010_Xx")
5. Complete a verificação e confirme o e-mail

!!! warning "Atenção"
    O nome de usuário do GitHub é o seu **nome profissional na internet**. Recrutadores vão acessar `github.com/seunome`. Escolha algo limpo e memorável — de preferência seu nome real ou uma variação profissional.

### Passo 4 — Criando o repositório do Projeto Final

No GitHub, clique no botão **"+"** → **New repository** e configure:

| Campo | Valor recomendado |
|-------|-------------------|
| **Repository name** | `sistema-escolar` (ou o nome do projeto da equipe) |
| **Description** | "Aplicação desktop para gerenciamento de alunos" |
| **Visibility** | **Public** (para portfólio) ou **Private** (durante desenvolvimento) |
| **Add a README** | ✅ Marcar |
| **Add .gitignore** | Selecionar template **Python** |
| **Choose a license** | Selecionar **MIT License** |

Clique em **Create repository**.

!!! note "Conceito Importante"
    **Público vs Privado** — Repositórios públicos são visíveis para todos. Ideais para portfólio e projetos open-source. Repositórios privados são visíveis apenas para você e colaboradores convidados. Use privado durante o desenvolvimento e mude para público quando estiver pronto para mostrar.

### Passo 5 — Entendendo os 3 arquivos essenciais

Todo repositório profissional tem pelo menos estes 3 arquivos na raiz:

**README.md** — O cartão de visita do projeto. É a primeira coisa que aparece quando alguém acessa seu repositório. Por enquanto, o GitHub criou um básico. No próximo capítulo, vamos transformá-lo em algo profissional.

**.gitignore** — Lista de arquivos que o Git deve **ignorar**. O template Python que selecionamos já inclui:

```text
# Exemplos do .gitignore para Python:
__pycache__/         # Cache do Python (gerado automaticamente)
*.pyc                # Bytecode compilado
.env                 # Variáveis de ambiente (senhas!)
*.db                 # Banco de dados local
.venv/               # Ambiente virtual
.vscode/             # Configurações do editor
```

!!! danger "Erro Crítico"
    Nunca versione o `.env` (contém senhas), arquivos `.db` (banco local) ou `__pycache__/` (cache). O `.gitignore` existe para proteger você de si mesmo — respeite-o.

**LICENSE** — Define o que outras pessoas podem fazer com seu código. A **MIT License** é a mais permissiva e popular: permite que qualquer pessoa use, copie e modifique seu código, desde que mantenha o aviso de copyright.

### Passo 6 — Instalando e configurando o GitHub Desktop

O **GitHub Desktop** é a forma mais fácil de usar Git — tudo visual, sem terminal.

1. Acesse **desktop.github.com** e baixe o instalador
2. Instale e abra o programa
3. Faça login com sua conta do GitHub
4. O GitHub Desktop vai mostrar seus repositórios

**Clonando o repositório:**

No GitHub Desktop, clique em **File → Clone Repository**. Selecione o repositório que você criou e escolha a pasta local onde quer salvar (ex: `C:\Projetos\sistema-escolar`).

```text
Clonar = baixar o repositório do GitHub para o seu computador.

GitHub (nuvem)  ──clone──▶  Seu PC (local)
```

Pronto! A pasta do projeto está no seu computador com todos os arquivos (`README.md`, `.gitignore`, `LICENSE`).

### Passo 7 — Git no Terminal (5 comandos essenciais)

O GitHub Desktop é ótimo para começar, mas no mercado de trabalho o terminal é mais usado. Aqui estão os **5 comandos que cobrem 90% do uso diário**:

```bash
# 1. CLONE — Baixar um repositório do GitHub
git clone https://github.com/seu-usuario/sistema-escolar.git

# 2. ADD — Marcar arquivos modificados para o próximo commit
git add .                    # Adiciona TODOS os arquivos modificados
git add main.py              # Adiciona apenas um arquivo específico

# 3. COMMIT — Salvar um ponto de versão com mensagem
git commit -m "Adiciona tela de login"

# 4. PUSH — Enviar commits locais para o GitHub
git push

# 5. PULL — Baixar atualizações do GitHub
git pull
```

!!! tip "Dica Profissional"
    O fluxo do dia a dia é sempre o mesmo: **editar → add → commit → push**. Pense no `add` como "preparar a mala", no `commit` como "fechar a mala com uma etiqueta", e no `push` como "despachar a mala". O `pull` é "receber a mala de volta com coisas novas que outros colocaram".

**Verificando o status (comando bônus):**

```bash
# Ver quais arquivos foram modificados
git status

# Resultado típico:
# modified:   main.py          ← arquivo alterado
# new file:   views/login.py   ← arquivo novo
# deleted:    temp.py           ← arquivo removido
```

### Passo 8 — Fazendo o primeiro commit real

Vamos fazer o ciclo completo. Copie os arquivos do seu Projeto Final para a pasta clonada do repositório.

**Via GitHub Desktop:**

1. Copie os arquivos do projeto para a pasta do repositório
2. O GitHub Desktop mostrará todos os arquivos novos em verde
3. Na parte inferior, escreva a mensagem: `feat: adiciona código inicial do projeto`
4. Clique em **Commit to main**
5. Clique em **Push origin** (ícone de seta para cima)

**Via Terminal:**

```bash
# Navegue até a pasta do repositório
cd C:\Projetos\sistema-escolar

# Verifique o que mudou
git status

# Adicione todos os arquivos
git add .

# Faça o commit com mensagem descritiva
git commit -m "feat: adiciona código inicial do projeto"

# Envie para o GitHub
git push
```

Abra o GitHub no navegador — seus arquivos estarão lá!

### Passo 9 — Adicionando colaboradores (equipe)

Para que todos os membros da equipe possam contribuir:

1. No repositório no GitHub, vá em **Settings → Collaborators**
2. Clique em **Add people**
3. Digite o nome de usuário de cada membro da equipe
4. Cada pessoa receberá um convite por e-mail — deve aceitar

Após aceitar, cada membro clona o repositório no seu computador:

```bash
git clone https://github.com/usuario-lider/sistema-escolar.git
```

!!! note "Conceito Importante"
    Cada membro trabalha na sua cópia local. Quando termina uma tarefa, faz `commit` e `push`. Quando quer ver o que os outros fizeram, faz `pull`. É como um Google Docs para código — mas com mais controle.

### Passo 10 — Fluxo de trabalho da equipe

O fluxo recomendado para equipes iniciantes:

```text
┌─────────────────────────────────────────────────────┐
│              FLUXO DE TRABALHO DA EQUIPE            │
│                                                     │
│  1. git pull          ← Antes de começar, SEMPRE    │
│  2. Editar código     ← Trabalhar na sua parte      │
│  3. git add .         ← Preparar as mudanças        │
│  4. git commit -m ""  ← Salvar com mensagem clara   │
│  5. git push          ← Enviar para o GitHub        │
│                                                     │
│  ⚠️ REGRA DE OURO: Sempre faça PULL antes de PUSH  │
└─────────────────────────────────────────────────────┘
```

**Dividindo o trabalho:**

| Membro | Responsabilidade | Arquivos |
|--------|-----------------|----------|
| Membro A | Interface (views) | `views/*.py` |
| Membro B | Banco de dados | `database/*.py` |
| Membro C | Lógica / Controllers | `controllers/*.py` |

Quando cada membro trabalha em **arquivos diferentes**, conflitos são raros. Combinem antes quem mexe em quê.

### Passo 11 — Resolução básica de conflitos

Um conflito acontece quando **duas pessoas editam a mesma linha do mesmo arquivo** ao mesmo tempo. O Git não sabe qual versão manter — e pede para você decidir.

```text
Cenário de conflito:

  João editou a linha 5 do main.py: janela.title("Sistema v1")
  Maria editou a linha 5 do main.py: janela.title("Sistema Escolar")
  
  João fez push primeiro ✅
  Maria tenta push → CONFLITO ❌
```

Quando isso acontece, o Git marca o arquivo assim:

```python
<<<<<<< HEAD
janela.title("Sistema v1")        # Versão do João (no GitHub)
=======
janela.title("Sistema Escolar")   # Versão da Maria (local)
>>>>>>> sua-branch
```

**Para resolver:**

1. Abra o arquivo conflitante
2. Escolha qual versão manter (ou combine as duas)
3. Remova os marcadores `<<<<<<<`, `=======` e `>>>>>>>`
4. Salve o arquivo
5. Faça `git add .`, `git commit -m "resolve conflito"` e `git push`

No GitHub Desktop, o programa mostra os conflitos visualmente e facilita a resolução.

!!! tip "Dica Profissional"
    A melhor forma de evitar conflitos é **comunicação**. Antes de começar a trabalhar, faça `git pull` para ter a versão mais recente. E combinem com a equipe quem mexe em quais arquivos. Conflitos são normais — não entre em pânico. Todo desenvolvedor lida com isso diariamente.

## 📝 Exercício

**Tempo estimado:** 15-20 minutos

**Tarefa:** Individualmente, cada aluno deve criar um repositório pessoal no GitHub chamado `meu-primeiro-repo` e:

1. Criar com README, .gitignore (Python) e LICENSE (MIT)
2. Clonar para o computador (via GitHub Desktop ou terminal)
3. Criar um arquivo `sobre_mim.py` com:
   - Uma variável `nome` com seu nome
   - Uma variável `curso` com "Python para Desktop"
   - Um `print()` que exibe uma apresentação
4. Fazer commit com mensagem: `feat: adiciona apresentação pessoal`
5. Fazer push
6. Verificar no GitHub que o arquivo aparece

??? hint "Dica"
    O arquivo `sobre_mim.py` pode ser simples:
    
    ```python
    nome = "João Silva"
    curso = "Python para Desktop"
    turma = "2026"
    
    print(f"Olá! Eu sou {nome}")
    print(f"Estou no curso {curso}, turma {turma}")
    print("Este é meu primeiro repositório no GitHub!")
    ```
    
    Depois de salvar, use `git add .`, `git commit -m "feat: adiciona apresentação pessoal"` e `git push`.

??? success "Solução resumida"
    ```bash
    # No terminal:
    git clone https://github.com/seu-usuario/meu-primeiro-repo.git
    cd meu-primeiro-repo
    
    # Crie o arquivo sobre_mim.py com o conteúdo acima
    
    git add .
    git commit -m "feat: adiciona apresentação pessoal"
    git push
    ```
    
    Ou no GitHub Desktop: os arquivos aparecem automaticamente na aba "Changes". Escreva a mensagem de commit e clique em "Commit to main" → "Push origin".

## 🏆 Missão da Equipe

**Tempo estimado:** 30-45 minutos

**Tarefa:** Criem o repositório oficial do Projeto Final da equipe no GitHub e configurem o ambiente de trabalho colaborativo.

**Entregável:** Repositório no GitHub com:

- Todos os membros como colaboradores
- Código do projeto já no repositório (primeiro commit)
- Cada membro com pelo menos 1 commit próprio

**Checklist da Missão:**

- [ ] Repositório criado no GitHub (público ou privado)
- [ ] README.md com nome do projeto e integrantes
- [ ] .gitignore com template Python configurado
- [ ] LICENSE MIT adicionada
- [ ] Todos os membros adicionados como colaboradores
- [ ] Todos clonaram o repositório no seu computador
- [ ] Código do projeto copiado para o repositório
- [ ] Primeiro commit realizado pelo líder: `feat: adiciona código inicial`
- [ ] Cada membro fez pelo menos 1 commit (modificar algo e fazer push)
- [ ] Cada membro fez `git pull` e viu o commit dos colegas
- [ ] O professor verificou o repositório no GitHub

!!! important "Nota para o Professor"
    Verifique: Acesse o repositório de cada equipe no GitHub. Na aba "Commits", devem aparecer commits de todos os membros. Peça que um membro faça uma alteração ao vivo, commit e push — e que outro membro faça pull e mostre a alteração no seu computador. Isso valida que o fluxo colaborativo está funcionando.

## ⚡ Desafio

**Vá além:** Crie um conflito proposital e resolva-o.

1. Dois membros da equipe editam a mesma linha do `README.md` simultaneamente
2. O primeiro faz push (funciona normalmente)
3. O segundo tenta push → conflito!
4. O segundo resolve o conflito, faz commit e push
5. Ambos fazem pull e verificam que está tudo correto

Isso pode parecer assustador, mas é melhor treinar agora em ambiente controlado do que travar no meio de uma entrega real.

## ⚠️ Erros Comuns

!!! danger "Push rejeitado: 'Updates were rejected'"
    **Sintoma:** `! [rejected] main -> main (fetch first)` ao tentar push.
    
    **Causa:** O GitHub tem commits que você não tem localmente. Alguém fez push antes de você.
    
    **Solução:** Faça `git pull` primeiro para baixar as atualizações, depois tente `git push` novamente. Se houver conflito, resolva-o conforme o Passo 11.

!!! warning "Arquivo .env foi commitado acidentalmente"
    **Sintoma:** O arquivo `.env` aparece no repositório do GitHub com suas senhas.
    
    **Causa:** O `.gitignore` não estava configurado antes do primeiro commit, ou o `.env` foi adicionado com `git add .` antes de criar o `.gitignore`.
    
    **Solução:** Remova do Git (sem apagar o arquivo local): `git rm --cached .env`, depois faça commit. Mas atenção: o histórico ainda contém o arquivo. Para segredos vazados, **troque todas as senhas imediatamente**.

!!! warning "GitHub Desktop não mostra alterações"
    **Sintoma:** Você editou arquivos mas o GitHub Desktop mostra "0 changed files".
    
    **Causa:** Você está editando arquivos fora da pasta do repositório clonado. Ou o repositório correto não está selecionado no GitHub Desktop.
    
    **Solução:** Verifique no GitHub Desktop qual repositório está ativo (canto superior esquerdo). Confirme que seus arquivos estão dentro da pasta que aparece em "Repository → Show in Explorer".

!!! danger "Conflito de merge assustador"
    **Sintoma:** O terminal mostra linhas com `<<<<<<<`, `=======` e `>>>>>>>` dentro dos seus arquivos.
    
    **Causa:** Duas pessoas editaram a mesma linha. É normal e esperado em equipes.
    
    **Solução:** Não entre em pânico. Abra o arquivo, escolha qual versão manter, remova os marcadores, salve, faça `git add .` e `git commit -m "resolve conflito"`. No GitHub Desktop, o programa guia você visualmente.

## 💡 Boas Práticas

**1. Commit cedo, commit sempre**

Não espere terminar tudo para fazer um commit. Commits pequenos e frequentes são mais fáceis de entender, revisar e reverter. Se algo quebrar, você perde apenas o último commit — não uma semana de trabalho.

**2. Mensagens de commit descritivas**

Uma boa mensagem de commit explica **o quê** e **por quê**:

```text
❌ Ruim:  "atualização"
❌ Ruim:  "fix"
❌ Ruim:  "asdkjasd"

✅ Bom:   "feat: adiciona validação de e-mail no cadastro"
✅ Bom:   "fix: corrige erro ao salvar aluno sem turma"
✅ Bom:   "docs: atualiza README com instruções de instalação"
```

**3. Pull antes de push**

Antes de enviar seu código, sempre faça `git pull` para baixar o que os outros fizeram. Isso reduz drasticamente a chance de conflitos.

**4. Um repositório por projeto**

Não coloque todos os exercícios do curso num único repositório. Cada projeto merece seu próprio repositório — isso facilita a organização e fica melhor no portfólio.

**5. .gitignore desde o início**

Configure o `.gitignore` **antes** do primeiro commit. Se você commitar um arquivo sensível e depois adicionar ao `.gitignore`, o arquivo continua no histórico. Prevenir é muito mais fácil que remediar.

## ☑️ Checklist

Antes de prosseguir para o próximo capítulo, confirme:

- [ ] Conta no GitHub criada com nome de usuário profissional
- [ ] Repositório do Projeto Final criado no GitHub
- [ ] README.md presente no repositório
- [ ] .gitignore com template Python configurado
- [ ] LICENSE MIT adicionada
- [ ] GitHub Desktop instalado e autenticado
- [ ] Repositório clonado para o computador local
- [ ] Primeiro commit realizado com sucesso
- [ ] Primeiro push enviado para o GitHub
- [ ] Todos os membros da equipe adicionados como colaboradores
- [ ] Cada membro clonou, commitou e fez push com sucesso
- [ ] Minha equipe concluiu a Missão da Equipe

## ➡️ Próximo Capítulo

No **Capítulo 02 — Publicando o Projeto Final**, você vai transformar seu repositório em algo digno de portfólio profissional:

- Commits com mensagens padronizadas
- README completo com badges, screenshots e instruções
- Release versionada (v1.0.0) 
- Documentação gerada com ajuda de IA
- Repositório pronto para mostrar a um recrutador

O Git já está funcionando. Agora, vamos deixar bonito! 🎨
