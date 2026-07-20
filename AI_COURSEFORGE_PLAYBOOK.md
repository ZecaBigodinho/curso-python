# 🤖 AI CourseForge Playbook

> **Aviso para a IA:** Leia este documento atentamente antes de processar solicitações de criação de conteúdo para a plataforma CourseForge. Este guia define o seu comportamento automatizado para que o usuário tenha o mínimo de trabalho possível.

## 🎯 Seu Objetivo
Sua principal função neste fluxo é atuar como o orquestrador do sistema **CourseForge**. O usuário atuará apenas como uma "ponte" entre você e o modelo DeepSeek (que possui a especialidade de redigir o conteúdo final). Você deve preparar tudo, entregar o texto para o usuário copiar, receber a resposta e finalizar a publicação.

---

## 🔄 O Fluxo de Trabalho (Step-by-Step)

Sempre que o usuário pedir para **"preparar um novo capítulo"** ou **"inserir o retorno do DeepSeek"**, siga estritamente estas etapas:

### FASE 1: Preparação e Geração do Prompt (Você faz)

Quando o usuário informar o tema do novo capítulo, o curso e o módulo:

1. **Crie a Estrutura (Via Script):**
   Como interagir com CLIs interativas via ferramentas de terminal pode ser falho para uma IA, crie e execute um script Python temporário (ex: `_temp_gen.py`) que utilize as classes do sistema para gerar o capítulo e o prompt programaticamente.
   
   *Exemplo de script que você deve executar:*
   ```python
   import sys
   sys.path.insert(0, '.')
   from models.chapter import Chapter
   from models.enums import NivelDificuldade, TipoPrompt
   from utils.file_manager import FileManager
   from utils.template_engine import TemplateEngine
   from generators.gerar_capitulo import ChapterGenerator
   from generators.gerar_prompt import PromptGenerator
   from utils.constants import DIR_CURSOS
   from pathlib import Path

   fm = FileManager(Path('.'))
   te = TemplateEngine(Path('templates'))
   chap_gen = ChapterGenerator(fm, te)
   prompt_gen = PromptGenerator(fm, te)

   # Ajuste os dados conforme o pedido do usuário
   curso_slug = "python_para_desktop"
   modulo_dir = "modulo_01_fundamentos"
   numero = 12 # Descubra o próximo número lendo o diretório ou pergunte ao usuário
   nome = "TEMA DO CAPÍTULO"
   objetivo = "OBJETIVO DO CAPÍTULO"
   nivel = NivelDificuldade.INTERMEDIARIO

   meta_curso = fm.ler_metadados_curso(fm.path(DIR_CURSOS) / curso_slug)
   chapter = Chapter(nome=nome, curso_slug=curso_slug, modulo_dir=modulo_dir, numero=numero, objetivo=objetivo, nivel=nivel)
   
   # Cria o arquivo placeholder e atualiza metadados
   cap_path = chap_gen.criar(chapter, meta_curso)

   # Gera o prompt
   contexto = {
       "curso": meta_curso.get("nome", curso_slug),
       "tema": chapter.nome,
       "nivel": chapter.nivel.value,
       "capitulo": chapter.nome,
       "objetivo": chapter.objetivo,
       "palavras_minimas": 1500,
   }
   prompt = prompt_gen.gerar(TipoPrompt.CAPITULO, contexto)
   
   print(f"PATH_DO_ARQUIVO: {cap_path}")
   print("=== PROMPT START ===")
   print(prompt)
   print("=== PROMPT END ===")
   ```

2. **Entregue o Prompt ao Usuário:**
   Após executar o script e capturar a saída, mostre o prompt gerado em um bloco de código Markdown fácil de copiar e diga:
   > *"Por favor, copie o texto abaixo, cole no DeepSeek e me envie a resposta completa que ele gerar."*

3. **Guarde o Caminho:**
   Lembre-se do `PATH_DO_ARQUIVO` gerado no passo 1. Você precisará dele na Fase 2.

---

### FASE 2: Inserção e Publicação (Você faz)

Quando o usuário colar a resposta (o conteúdo em Markdown) gerada pelo DeepSeek:

1. **Substitua o Arquivo:**
   Use sua ferramenta de edição de arquivos (`write_to_file` ou equivalente com overwrite) para **substituir integralmente** o conteúdo do arquivo `.md` correspondente (aquele caminho salvo na Fase 1) pelo conteúdo que o usuário colou. Não tente fazer *merge* com o placeholder; o DeepSeek já gera a estrutura correta.

2. **Valide a Integração:**
   Execute o seguinte comando no terminal na raiz do projeto (`e:\chave\curso\CourseForge`):
   ```bash
   python main.py publicar
   ```
   *Este comando atualiza o `mkdocs.yml`, constrói o site e valida se há links quebrados.* 
   Analise a saída do terminal. Se houver erros, corrija os links no arquivo markdown automaticamente.

3. **Publique o Site (Deploy):**
   Se o passo anterior retornar sucesso (`[OK] Build finalizado com sucesso!`), execute o deploy para o GitHub Pages:
   ```bash
   python -m mkdocs gh-deploy -f mkdocs/mkdocs.yml --force
   ```

4. **Confirme o Sucesso:**
   Responda ao usuário com uma mensagem de comemoração informando que o capítulo foi inserido, validado e o site foi publicado com sucesso.

---

## ⚠️ Regras Críticas para a IA

- **Codificação (Encoding):** O projeto utiliza UTF-8. Ao usar `write_to_file`, garanta que a integridade dos caracteres acentuados seja mantida. O código do sistema já foi corrigido para suportar `sys.stdin` em utf-8, então não se preocupe com erros de CLI, mas priorize a edição direta de arquivos.
- **Nível de Dificuldade (Enum):** Sempre passe `nivel.value` (ex: `"intermediário"`) e nunca a representação do Enum (`NivelDificuldade.INTERMEDIARIO`) para templates ou contexto Jinja2. Isso também já está corrigido na base, mas mantenha em mente ao criar scripts temporários.
- **Não pergunte desnecessariamente:** Se você puder deduzir o próximo número do capítulo listando os arquivos do diretório (ex: `list_dir`), faça isso autonomamente. Reduza a carga cognitiva do usuário.
- **Limpeza:** Sempre exclua os scripts Python temporários (como `_temp_gen.py`) após utilizá-los para manter o diretório limpo.
