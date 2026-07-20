"""
CourseForge — generators/gerar_capitulo.py

Responsável por criar capítulos completos dentro de módulos.

Fluxo:
  1. Usuário seleciona curso e módulo (via selectors.py)
  2. Detectar próximo número de capítulo automaticamente
  3. Coletar nome, objetivo e nível
  4. Renderizar template capitulo.md completo
  5. Salvar arquivo numerado no diretório do módulo
"""
from __future__ import annotations

from pathlib import Path

from models.chapter import Chapter
from models.enums import NivelDificuldade
from utils.file_manager import FileManager
from utils.template_engine import TemplateEngine
from utils.cli_ui import UI
from utils.validators import validate_nome, validate_descricao
from utils.selectors import selecionar_curso, selecionar_modulo
from utils.constants import TEMPLATE_CAPITULO, DIR_CURSOS, MODULE_DIR_PREFIX
from utils.logger import get_logger

logger = get_logger(__name__)


class ChapterGenerator:
    """
    Gera capítulos completos dentro de módulos existentes.

    Responsabilidades:
    - Selecionar curso e módulo (via selectors)
    - Numerar capítulo automaticamente
    - Renderizar template de capítulo completo (com admonitions, tabs, etc.)
    - Salvar arquivo .md no diretório correto
    """

    def __init__(self, fm: FileManager, template_engine: TemplateEngine) -> None:
        """
        Args:
            fm: Gerenciador de arquivos da plataforma.
            template_engine: Motor de renderização Jinja2.
        """
        self.fm = fm
        self.te = template_engine

    # ------------------------------------------------------------------ #
    # Interface pública                                                    #
    # ------------------------------------------------------------------ #

    def criar_interativo(self) -> Chapter | None:
        """Coleta dados via CLI e cria o capítulo."""
        UI.secao("CRIAR NOVO CAPÍTULO")

        curso_slug = selecionar_curso(self.fm)
        if not curso_slug:
            return None

        modulo_dir_nome = selecionar_modulo(self.fm, curso_slug)
        if not modulo_dir_nome:
            return None

        numero = self._detectar_proximo_numero(curso_slug, modulo_dir_nome)
        UI.info(f"Próximo número de capítulo disponível: {numero:02d}")

        nome = self._pedir_nome()
        objetivo = self._pedir_objetivo()
        nivel = self._pedir_nivel()

        meta_curso = self.fm.ler_metadados_curso(self.fm.path(DIR_CURSOS) / curso_slug)

        chapter = Chapter(
            nome=nome,
            curso_slug=curso_slug,
            modulo_dir=modulo_dir_nome,
            numero=numero,
            objetivo=objetivo,
            nivel=nivel,
        )

        logger.info("Criando capítulo: %s", chapter.filename)
        UI.info(f"Criando capítulo: {chapter.filename}")
        path = self.criar(chapter, meta_curso)

        UI.sucesso(f"Capítulo '{chapter.nome}' criado com sucesso!")
        self._exibir_resumo(chapter, path)
        return chapter

    def criar(self, chapter: Chapter, meta_curso: dict | None = None) -> Path:
        """
        Cria capítulo a partir de objeto (uso programático).

        Args:
            chapter: Objeto Chapter construído e validado.
            meta_curso: Metadados do curso pai (para o template).

        Returns:
            Path do arquivo de capítulo criado.
        """
        return self._criar_arquivo(chapter, meta_curso or {})

    # ------------------------------------------------------------------ #
    # Coleta de dados                                                      #
    # ------------------------------------------------------------------ #

    def _detectar_proximo_numero(self, curso_slug: str, modulo_dir_nome: str) -> int:
        """Detecta o próximo número de capítulo disponível no módulo."""
        modulo_dir = self.fm.path(DIR_CURSOS) / curso_slug / modulo_dir_nome
        arquivos = [
            f for f in self.fm.listar_arquivos(modulo_dir, "md")
            if f.name != "index.md"
        ]
        return len(arquivos) + 1

    def _pedir_nome(self) -> str:
        while True:
            try:
                return validate_nome(UI.perguntar("Nome do capítulo"), "Nome do capítulo")
            except ValueError as e:
                UI.erro(str(e))

    def _pedir_objetivo(self) -> str:
        return validate_descricao(
            UI.perguntar("Objetivo principal do capítulo (opcional)", padrao="")
        )

    def _pedir_nivel(self) -> NivelDificuldade:
        """Solicita nível de dificuldade e retorna como Enum."""
        escolha = UI.selecionar(
            "Nível de dificuldade",
            NivelDificuldade.opcoes(),
        )
        return NivelDificuldade.from_str(escolha)

    # ------------------------------------------------------------------ #
    # Criação do arquivo                                                   #
    # ------------------------------------------------------------------ #

    def _criar_arquivo(self, chapter: Chapter, meta_curso: dict) -> Path:
        """Renderiza o template completo e salva o capítulo."""
        modulo_dir = self.fm.path(DIR_CURSOS) / chapter.curso_slug / chapter.modulo_dir
        cap_path = modulo_dir / chapter.filename

        contexto = {
            **chapter.to_dict(),
            "curso_nome": meta_curso.get("nome", chapter.curso_slug) if meta_curso else chapter.curso_slug,
            "modulo_nome": chapter.modulo_dir.replace("_", " ").title(),
        }

        conteudo = self.te.renderizar(TEMPLATE_CAPITULO, contexto)
        self.fm.escrever(cap_path, conteudo, sobrescrever=False)
        UI.muted(f"  [+] {cap_path.relative_to(self.fm.root)}")
        logger.info("Capítulo criado: %s", cap_path)
        return cap_path

    # ------------------------------------------------------------------ #
    # Exibição                                                             #
    # ------------------------------------------------------------------ #

    def _exibir_resumo(self, chapter: Chapter, path: Path) -> None:
        """Exibe tabela resumida com os dados do capítulo criado."""
        UI.tabela(
            titulo="Capítulo Criado",
            colunas=["Campo", "Valor"],
            linhas=[
                ["Nome", chapter.nome],
                ["Arquivo", chapter.filename],
                ["Módulo", chapter.modulo_dir],
                ["Curso", chapter.curso_slug],
                ["Número", str(chapter.numero)],
                ["Nível", chapter.nivel.value],
                ["Path", str(path.relative_to(self.fm.root))],
            ],
        )
