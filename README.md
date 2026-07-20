# 🚀 CourseForge — IA Handoff & Deployment Guide

> **ATENÇÃO IA SUCESSORA:** Se você está lendo este documento, você acabou de assumir o desenvolvimento ou a produção de conteúdo do **CourseForge**. Leia atentamente as instruções abaixo para entender o estado da arte do projeto e o que deve ser feito em seguida.

O CourseForge é uma plataforma profissional de geração de cursos estáticos baseada em Python e **MkDocs Material**. Ele abstrai a criação de diretórios, formatação de Markdown, geração de prompts de IA e construção do site.

---

## 🤖 1. Contexto para a Nova IA (Handoff)

### O que já foi construído:
- **Arquitetura Sólida:** O código segue princípios Clean Code e SOLID. Tudo é roteado pelo `main.py` e orquestrado dentro da pasta `generators/` e `models/`.
- **CLI Rápida:** É possível rodar `python main.py gerar-capitulo` para pular o menu interativo e focar só na criação, e `python main.py publicar` para build com verificação `--strict`.
- **Templates Profissionais (MkDocs Material):** Os arquivos base (em `templates/`) usam admonitions (`!!! note`), abas de código e details (`??? success`).
- **Conversor HTML Legado:** Em `converter/`, a plataforma já sabe fatiar (`MarkdownSplitter`) e converter HTMLs antigos para Markdown perfeitamente preservando a estrutura.
- **Produção Atual:** Já validamos a geração massiva de conteúdo (Capítulo 1 de Python com +12.000 palavras gerado com extrema profundidade).

### Qual é o seu papel agora?
Seu objetivo primário provavelmente será **Produção de Conteúdo** ou **Setup de Deploy**. Nunca gere conteúdo raso. Use exemplos práticos, projetos reais e formatação MkDocs avançada. Não crie soluções temporárias ou quebre a arquitetura de pastas existente (tudo vai dentro de `cursos/`).

---

## 💻 2. Setup Rápido em um Novo PC

Se o usuário acabou de baixar este projeto em um novo computador, siga os passos no terminal para ele:

```bash
# 1. Crie o ambiente virtual
python -m venv venv

# 2. Ative o ambiente
# No Windows:
.\venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate

# 3. Instale as dependências rigorosamente
pip install -r requirements.txt
pip install mkdocs-material  # Obrigatório para a compilação
```

---

## 🌍 3. Como Colocar o Site no Ar DE GRAÇA (Para Alunos)

A forma mais robusta, profissional e 100% gratuita de hospedar este curso para que os alunos acessem pelo PC ou Celular é usando o **GitHub Pages**. O MkDocs Material é responsivo por natureza.

### Passo a Passo para Hospedagem:

1. **Crie um repositório no GitHub:**
   - Peça ao usuário para criar um repositório vazio no GitHub (ex: `curso-python-gratuito`).
   
2. **Suba os arquivos da pasta `CourseForge` para o repositório:**
   ```bash
   git init
   git add .
   git commit -m "Primeiro commit do curso"
   git branch -M main
   git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
   git push -u origin main
   ```

3. **Implante o site automaticamente com o MkDocs:**
   O MkDocs possui um comando nativo que compila os arquivos e publica o site diretamente no GitHub Pages em segundos. Basta rodar:
   ```bash
   # Certifique-se de que o diretório atual é a raiz do CourseForge
   python -m mkdocs gh-deploy -f mkdocs/mkdocs.yml --force
   ```

4. **Acesse o link:**
   - O site estará disponível instantaneamente (ou em até 2 minutos) no endereço:  
     `https://SEU_USUARIO.github.io/SEU_REPOSITORIO/`
   - Toda vez que a IA ou o usuário gerar novos capítulos, basta rodar o comando `mkdocs gh-deploy` novamente para que a atualização vá para o ar no celular de todos os alunos!

---

## 🗂️ 4. Estrutura do Projeto (Guia de Pastas)

- `main.py`: O coração do sistema. Pode rodar interativo ou via argumentos (`publicar`, `gerar-capitulo`).
- `config/`: Configurações globais em YAML.
- `templates/`: Base visual dos Markdowns. Se precisar mudar o design padrão dos capítulos, mexa aqui.
- `models/`: Entidades de domínio (Course, Module, Chapter).
- `generators/`: A lógica pesada de automação (Cria os arquivos, atualiza o mkdocs.yml, cria prompts).
- `converter/`: Transforma HTML sujo em Markdown purificado.
- `utils/`: Operações de sistema de arquivos (FileManager) e terminal (UI).
- `mkdocs/`: Pasta onde o arquivo oficial `mkdocs.yml` reside.
- `cursos/`: **A mina de ouro.** Aqui ficam os Markdowns gerados.

Boa sorte na nova máquina! Mantenha a barra de qualidade lá em cima! 🚀
