"""
CourseForge — main.py
Ponto de entrada da plataforma.

Responsabilidade ÚNICA: inicializar dependências e rotear escolhas de menu ou CLI.
Nunca contém lógica de negócio.
"""
from __future__ import annotations

import io
import sys
import subprocess
from pathlib import Path

# ------------------------------------------------------------------ #
# Configurar UTF-8 ANTES de qualquer outro import                     #
# ------------------------------------------------------------------ #
if sys.platform == "win32":
    try:
        sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8", errors="replace")
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
    except AttributeError:
        pass  # Ambiente sem buffer (IDE, redirect)

# Garantir que a raiz do projeto está no sys.path
PROJECT_ROOT = Path(__file__).parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

from utils.logger import configurar_logging, get_logger
from utils.config_loader import ConfigLoader
from utils.file_manager import FileManager
from utils.template_engine import TemplateEngine
from utils.cli_ui import UI, console
from utils.constants import DIR_CURSOS, DIR_MKDOCS, DIR_CONVERTIDOS, DIR_PROMPTS_GERADOS
from generators.gerar_curso import CourseGenerator
from generators.gerar_modulo import ModuleGenerator
from generators.gerar_capitulo import ChapterGenerator
from generators.gerar_exercicio import ExercicioGenerator
from generators.gerar_projeto import ProjetoGenerator
from generators.atualizar_mkdocs import MkDocsUpdater
from generators.gerar_prompt import PromptGenerator
from converter.html_to_markdown import HtmlToMarkdown
from converter.markdown_splitter import MarkdownSplitter

# Logger deste módulo (configurado em _inicializar)
logger = get_logger(__name__)

# ------------------------------------------------------------------ #
# Opções do menu principal                                            #
# ------------------------------------------------------------------ #
_MENU_OPCOES = [
    ("1", "Criar Curso"),
    ("2", "Criar Módulo"),
    ("3", "Criar Capítulo"),
    ("4", "Criar Exercícios"),
    ("5", "Criar Projeto Prático"),
    ("6", "Gerar Prompt para IA"),
    ("7", "Atualizar mkdocs.yml"),
    ("8", "Converter HTML para Markdown"),
    ("9", "Dividir HTML em Capítulos"),
    ("0", "Sair"),
]


# ------------------------------------------------------------------ #
# Classe principal                                                    #
# ------------------------------------------------------------------ #

class CourseForgeApp:
    """
    Orquestrador principal da plataforma CourseForge.

    Por que uma classe e não funções globais?
        Facilita futura migração para GUI (Tkinter) ou API (FastAPI):
        apenas a camada de apresentação muda — a inicialização e
        o roteamento permanecem os mesmos.
    """

    def __init__(self) -> None:
        self.root = PROJECT_ROOT
        self._inicializar()

    def _inicializar(self) -> None:
        """Inicializa todas as dependências em ordem correta."""
        # 1. Logging
        configurar_logging(self.root)

        # 2. Configuração com validação e defaults
        config_path = self.root / "config" / "config.yaml"
        self.config_loader = ConfigLoader(config_path)

        # 3. Gerenciador de arquivos
        self.fm = FileManager(self.root)

        # 4. Garantir diretórios obrigatórios
        for d in (DIR_CURSOS, DIR_MKDOCS, DIR_CONVERTIDOS, DIR_PROMPTS_GERADOS):
            self.fm.criar_diretorio(self.fm.path(d))

        # 5. Motor de templates
        self.te = TemplateEngine(self.root / "templates")

        # 6. Geradores (injeção de dependências)
        config_dict = self.config_loader.as_dict()
        self.course_gen = CourseGenerator(self.fm, self.te)
        self.module_gen = ModuleGenerator(self.fm, self.te)
        self.chapter_gen = ChapterGenerator(self.fm, self.te)
        self.exercicio_gen = ExercicioGenerator(self.fm, self.te)
        self.projeto_gen = ProjetoGenerator(self.fm, self.te)
        self.mkdocs_upd = MkDocsUpdater(self.fm, config_dict)
        self.prompt_gen = PromptGenerator(self.fm, self.te)

        # 7. Conversores
        self.html_conv = HtmlToMarkdown(self.fm)
        self.splitter = MarkdownSplitter(self.fm)

        logger.info("CourseForge inicializado em: %s", self.root)

    # ------------------------------------------------------------------ #
    # Loop principal                                                       #
    # ------------------------------------------------------------------ #

    def executar(self) -> None:
        """Inicia o loop principal da aplicação."""
        versao = self.config_loader.get("plataforma", "versao", default="1.0.0")
        UI.banner()
        UI.info(f"Plataforma inicializada em: {self.root}")
        UI.info(f"Versão: {versao}")

        while True:
            try:
                self._mostrar_menu()
                escolha = UI.perguntar("Escolha uma opcao", padrao="0")
                self._rotear(escolha.strip())
            except KeyboardInterrupt:
                console.print("\n")
                UI.aviso("Interrompido pelo usuario.")
                break
            except FileExistsError as e:
                UI.erro(str(e))
                logger.warning("FileExistsError: %s", e)
                UI.aguardar_enter()
            except FileNotFoundError as e:
                UI.erro(str(e))
                logger.error("FileNotFoundError: %s", e)
                UI.aguardar_enter()
            except ValueError as e:
                UI.erro(str(e))
                logger.warning("ValueError: %s", e)
                UI.aguardar_enter()
            except Exception as e:
                UI.erro(f"Erro inesperado: {type(e).__name__}: {e}")
                logger.exception("Erro inesperado na execução do menu.")
                import traceback
                traceback.print_exc()
                UI.aguardar_enter()

    # ------------------------------------------------------------------ #
    # Fluxos Automatizados (CLI)                                           #
    # ------------------------------------------------------------------ #

    def fluxo_publicar(self) -> None:
        """Executa a publicação automática (atualizar nav, validar links, build)."""
        UI.banner()
        UI.secao("PUBLICAR CURSOS")

        # 1. Atualizar mkdocs.yml silenciosamente
        self.mkdocs_upd.atualizar(silencioso=True)
        UI.sucesso("Navegação do mkdocs.yml atualizada.")

        # 2. Executar mkdocs build --strict
        UI.info("Iniciando build do MkDocs com validação de links (--strict)...")
        try:
            with UI.progresso_spinner("Construindo site estático...") as p:
                p.add_task("", total=None)
                # Executa subprocesso. O cwd é a raiz do projeto.
                resultado = subprocess.run(
                    [sys.executable, "-m", "mkdocs", "build", "--strict", "-f", "mkdocs/mkdocs.yml"],
                    cwd=str(self.root),
                    capture_output=True,
                    text=True,
                    check=True
                )
            
            UI.sucesso("Build finalizado com sucesso! Sem links quebrados.")
            logger.info("MkDocs build concluído com sucesso.")
            
        except subprocess.CalledProcessError as e:
            UI.erro("Ocorreram erros durante o build do MkDocs (links quebrados ou sintaxe):")
            # Mostrar os erros reportados pelo mkdocs
            console.print(f"[error]{e.stderr}[/error]")
            logger.error("Falha no mkdocs build. Code: %s, Stderr: %s", e.returncode, e.stderr)
            sys.exit(1)
        except FileNotFoundError:
            UI.erro("Comando 'mkdocs' não encontrado. Certifique-se de que ele está instalado (pip install mkdocs-material).")
            sys.exit(1)

    def fluxo_gerar_capitulo(self) -> None:
        """Assistente ultrarrápido para criar capítulo, prompt e atualizar mkdocs."""
        UI.banner()
        UI.secao("ASSISTENTE DE CAPÍTULO EXPRESSO")

        from utils.selectors import selecionar_curso, selecionar_modulo
        
        curso_slug = selecionar_curso(self.fm)
        if not curso_slug:
            return

        modulo_dir_nome = selecionar_modulo(self.fm, curso_slug)
        if not modulo_dir_nome:
            return

        # Para obter próximo número, chamamos diretamente a lógica de detecção
        proximo_numero = self.chapter_gen._detectar_proximo_numero(curso_slug, modulo_dir_nome)
        
        # Coleta das entradas essenciais
        try:
            numero = UI.perguntar_numero("Número do capítulo", padrao=proximo_numero)
            nome = self.chapter_gen._pedir_nome()
            objetivo = self.chapter_gen._pedir_objetivo()
            nivel = self.chapter_gen._pedir_nivel()
        except KeyboardInterrupt:
            console.print()
            UI.aviso("Cancelado pelo usuário.")
            return

        from models.chapter import Chapter
        from models.enums import TipoPrompt
        
        # 1. Gerar Markdown
        meta_curso = self.fm.ler_metadados_curso(self.fm.path(DIR_CURSOS) / curso_slug)
        chapter = Chapter(
            nome=nome,
            curso_slug=curso_slug,
            modulo_dir=modulo_dir_nome,
            numero=numero,
            objetivo=objetivo,
            nivel=nivel,
        )
        cap_path = self.chapter_gen.criar(chapter, meta_curso)
        UI.sucesso(f"Capítulo '{chapter.nome}' salvo em {cap_path.name}")

        # 2. Gerar Prompt (sem perguntar tudo de novo)
        contexto_prompt = {
            "curso": meta_curso.get("nome", curso_slug) if meta_curso else curso_slug,
            "tema": chapter.nome,
            "nivel": chapter.nivel.value,
            "capitulo": chapter.nome,
            "objetivo": chapter.objetivo,
            "palavras_minimas": 1500,
        }
        
        prompt = self.prompt_gen.gerar(TipoPrompt.CAPITULO, contexto_prompt)
        UI.info("Prompt gerado para IA:")
        self.prompt_gen._exibir_prompt(prompt)
        
        # Salvar o prompt
        prompt_path = self.prompt_gen._salvar(prompt, TipoPrompt.CAPITULO)
        UI.sucesso(f"Prompt salvo: {prompt_path.name}")

        # 3. Atualizar MkDocs
        self.mkdocs_upd.atualizar(silencioso=True)
        UI.sucesso("mkdocs.yml atualizado automaticamente.")
        
        UI.secao("✅ FLUXO CONCLUÍDO")
        UI.muted(f"Tempo estimado da criação: rápido e eficiente!")

    def _mostrar_menu(self) -> None:
        """Exibe o menu principal."""
        console.print()
        UI.titulo_menu("MENU PRINCIPAL — CourseForge")
        UI.menu(_MENU_OPCOES)

    def _rotear(self, escolha: str) -> None:
        """Roteia escolha do usuário para o gerador/conversor correto."""
        if escolha == "0":
            UI.sucesso("Ate logo! Bons estudos!")
            sys.exit(0)

        elif escolha == "1":
            course = self.course_gen.criar_interativo()
            if course:
                self.mkdocs_upd.atualizar(silencioso=True)
                UI.muted("  mkdocs.yml atualizado automaticamente.")
            UI.aguardar_enter()

        elif escolha == "2":
            module = self.module_gen.criar_interativo()
            if module:
                self.mkdocs_upd.atualizar(silencioso=True)
                UI.muted("  mkdocs.yml atualizado automaticamente.")
            UI.aguardar_enter()

        elif escolha == "3":
            chapter = self.chapter_gen.criar_interativo()
            if chapter:
                self.mkdocs_upd.atualizar(silencioso=True)
                UI.muted("  mkdocs.yml atualizado automaticamente.")
            UI.aguardar_enter()

        elif escolha == "4":
            self.exercicio_gen.criar_interativo()
            UI.aguardar_enter()

        elif escolha == "5":
            self.projeto_gen.criar_interativo()
            UI.aguardar_enter()

        elif escolha == "6":
            self.prompt_gen.gerar_interativo()
            UI.aguardar_enter()

        elif escolha == "7":
            self.mkdocs_upd.atualizar(silencioso=False)
            UI.aguardar_enter()

        elif escolha == "8":
            self.html_conv.converter_interativo()
            UI.aguardar_enter()

        elif escolha == "9":
            self.splitter.dividir_interativo()
            UI.aguardar_enter()

        else:
            UI.aviso(f"Opcao invalida: '{escolha}'. Escolha entre 0 e 9.")


# ------------------------------------------------------------------ #
# Entry point                                                          #
# ------------------------------------------------------------------ #

if __name__ == "__main__":
    app = CourseForgeApp()
    
    if len(sys.argv) > 1:
        comando = sys.argv[1].lower()
        if comando == "publicar":
            app.fluxo_publicar()
        elif comando == "gerar-capitulo":
            app.fluxo_gerar_capitulo()
        else:
            UI.erro(f"Comando desconhecido: '{comando}'")
            print("Comandos disponíveis: publicar, gerar-capitulo")
            sys.exit(1)
    else:
        app.executar()
