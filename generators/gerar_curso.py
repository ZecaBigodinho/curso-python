"""
CourseForge — generators/gerar_curso.py

Responsável por criar a estrutura completa de um novo curso.

Fluxo:
  1. Coletar dados via CLI (ou receber objeto Course diretamente)
  2. Validar entradas
  3. Criar estrutura de diretórios em cursos/<slug>/
  4. Renderizar template curso.md e salvar docs/index.md
  5. Salvar metadados .courseforge.yaml
"""
from __future__ import annotations

from pathlib import Path

from models.course import Course
from utils.file_manager import FileManager
from utils.template_engine import TemplateEngine
from utils.cli_ui import UI
from utils.validators import validate_nome, validate_descricao, validate_autor, validate_numero
from utils.constants import (
    TEMPLATE_CURSO, CURSO_DOCS_SUBDIR, DIR_CURSOS,
    NOME_MIN_LEN, NOME_MAX_LEN, AUTOR_MIN_LEN, AUTOR_MAX_LEN,
    MODULOS_MIN, MODULOS_MAX,
)
from utils.logger import get_logger

logger = get_logger(__name__)


class CourseGenerator:
    """
    Gera a estrutura completa de um novo curso na plataforma.

    Responsabilidades:
    - Criar diretório do curso em cursos/<slug>/
    - Criar cursos/<slug>/docs/index.md a partir do template
    - Salvar metadados em cursos/<slug>/.courseforge.yaml
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

    def criar_interativo(self) -> Course | None:
        """
        Coleta dados do usuário via CLI e cria o curso.

        Returns:
            O objeto Course criado, ou None se cancelado.
        """
        UI.secao("CRIAR NOVO CURSO")

        nome = self._pedir_nome()
        descricao = self._pedir_descricao()
        autor = self._pedir_autor()
        num_modulos = self._pedir_num_modulos()

        course = Course(
            nome=nome,
            descricao=descricao,
            autor=autor,
            num_modulos=num_modulos,
        )

        logger.info("Criando curso: %s (%s)", course.nome, course.slug)
        UI.info(f"Criando curso: {course.nome} ({course.slug})")
        self.criar(course)

        UI.sucesso(f"Curso '{course.nome}' criado com sucesso!")
        self._exibir_resumo(course)
        return course

    def criar(self, course: Course) -> Path:
        """
        Cria a estrutura do curso a partir de um objeto Course.
        Adequado para chamadas programáticas (testes, API futura).

        Args:
            course: Objeto Course previamente construído e validado.

        Returns:
            Path do diretório raiz do curso.

        Raises:
            FileExistsError: Se um curso com o mesmo slug já existir.
        """
        return self._criar_estrutura(course)

    # ------------------------------------------------------------------ #
    # Coleta de dados                                                      #
    # ------------------------------------------------------------------ #

    def _pedir_nome(self) -> str:
        while True:
            try:
                valor = UI.perguntar("Nome do curso")
                return validate_nome(valor, "Nome do curso")
            except ValueError as e:
                UI.erro(str(e))

    def _pedir_descricao(self) -> str:
        valor = UI.perguntar("Descrição do curso (opcional)", padrao="")
        return validate_descricao(valor)

    def _pedir_autor(self) -> str:
        while True:
            try:
                valor = UI.perguntar("Autor / Instrutor", padrao="Professor")
                return validate_autor(valor)
            except ValueError as e:
                UI.erro(str(e))

    def _pedir_num_modulos(self) -> int:
        while True:
            try:
                valor = UI.perguntar_numero(
                    "Quantidade de módulos planejados",
                    padrao=1,
                    minimo=MODULOS_MIN,
                    maximo=MODULOS_MAX,
                )
                return validate_numero(valor, "Quantidade de módulos", MODULOS_MIN, MODULOS_MAX)
            except ValueError as e:
                UI.erro(str(e))

    # ------------------------------------------------------------------ #
    # Criação de estrutura                                                 #
    # ------------------------------------------------------------------ #

    def _criar_estrutura(self, course: Course) -> Path:
        """
        Cria toda a estrutura de diretórios e arquivos do curso.

        Estrutura gerada:
          cursos/
            <slug>/
              docs/
                index.md        ← página principal renderizada do template
              .courseforge.yaml ← metadados da plataforma
        """
        cursos_dir = self.fm.path(DIR_CURSOS)
        curso_dir = cursos_dir / course.slug

        if curso_dir.exists():
            raise FileExistsError(
                f"Curso '{course.slug}' já existe em '{curso_dir}'.\n"
                "Use outro nome ou remova o diretório existente."
            )

        # Criar estrutura de diretórios
        docs_dir = curso_dir / CURSO_DOCS_SUBDIR
        self.fm.criar_diretorio(docs_dir)

        # Renderizar e salvar index.md
        conteudo = self.te.renderizar(TEMPLATE_CURSO, course.to_dict())
        index_path = docs_dir / "index.md"
        self.fm.escrever(index_path, conteudo)
        UI.muted(f"  [+] {index_path.relative_to(self.fm.root)}")

        # Salvar metadados
        meta_path = self.fm.salvar_metadados_curso(curso_dir, course.to_dict())
        UI.muted(f"  [+] {meta_path.relative_to(self.fm.root)}")

        logger.info("Estrutura do curso criada em: %s", curso_dir)
        return curso_dir

    # ------------------------------------------------------------------ #
    # Exibição                                                             #
    # ------------------------------------------------------------------ #

    def _exibir_resumo(self, course: Course) -> None:
        """Exibe tabela resumida com os dados do curso criado."""
        UI.tabela(
            titulo="Curso Criado",
            colunas=["Campo", "Valor"],
            linhas=[
                ["Nome", course.nome],
                ["Slug", course.slug],
                ["Autor", course.autor],
                ["Módulos planejados", str(course.num_modulos)],
                ["Versão", course.versao],
                ["Criado em", course.data_criacao.isoformat()],
                ["Diretório", f"cursos/{course.slug}/"],
            ],
        )

    # ------------------------------------------------------------------ #
    # Consultas                                                            #
    # ------------------------------------------------------------------ #

    def listar_cursos(self) -> list[dict]:
        """
        Lista todos os cursos existentes na plataforma.

        Returns:
            Lista de dicionários com metadados de cada curso.
        """
        from utils.selectors import listar_cursos_info
        return listar_cursos_info(self.fm)

    def exibir_cursos(self) -> None:
        """Exibe lista de cursos em formato de tabela."""
        cursos = self.listar_cursos()
        if not cursos:
            UI.aviso("Nenhum curso encontrado. Crie seu primeiro curso!")
            return

        UI.tabela(
            titulo="Cursos Disponíveis",
            colunas=["Nome", "Autor", "Módulos", "Versão"],
            linhas=[
                [c["nome"], c["autor"], str(c["num_modulos"]), c["versao"]]
                for c in cursos
            ],
        )
