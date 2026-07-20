"""
CourseForge — generators/gerar_projeto.py

Gerador de arquivos de projeto prático para módulos.

Por que este gerador foi criado?
    A lógica de criação de projetos estava em main.py (_criar_projeto),
    violando o SRP. Mesmo motivo e solução de gerar_exercicio.py.
"""
from __future__ import annotations

from pathlib import Path

from utils.file_manager import FileManager
from utils.template_engine import TemplateEngine
from utils.cli_ui import UI
from utils.selectors import selecionar_curso, selecionar_modulo
from utils.slugify import slugify
from utils.constants import TEMPLATE_PROJETO
from utils.logger import get_logger

logger = get_logger(__name__)


class ProjetoGenerator:
    """
    Gera arquivos de projeto prático dentro de módulos.

    Responsabilidades:
    - Selecionar curso e módulo
    - Coletar nome e dados do projeto
    - Renderizar template de projeto
    - Salvar arquivo no diretório do módulo
    """

    def __init__(self, fm: FileManager, template_engine: TemplateEngine) -> None:
        """
        Args:
            fm: Gerenciador de arquivos.
            template_engine: Motor de templates Jinja2.
        """
        self.fm = fm
        self.te = template_engine

    def criar_interativo(self) -> Path | None:
        """Coleta dados via CLI e cria o arquivo de projeto."""
        UI.secao("CRIAR PROJETO PRÁTICO")

        curso_slug = selecionar_curso(self.fm)
        if not curso_slug:
            return None

        modulo_dir_nome = selecionar_modulo(self.fm, curso_slug)
        if not modulo_dir_nome:
            return None

        projeto_nome = UI.perguntar("Nome do projeto")
        if not projeto_nome.strip():
            UI.erro("Nome do projeto não pode ser vazio.")
            return None

        return self.criar(
            curso_slug=curso_slug,
            modulo_dir_nome=modulo_dir_nome,
            projeto_nome=projeto_nome.strip(),
        )

    def criar(
        self,
        curso_slug: str,
        modulo_dir_nome: str,
        projeto_nome: str,
    ) -> Path:
        """
        Cria arquivo de projeto prático (uso programático e interativo).

        Args:
            curso_slug: Slug do curso.
            modulo_dir_nome: Nome do diretório do módulo.
            projeto_nome: Nome do projeto prático.

        Returns:
            Path do arquivo de projeto criado.

        Raises:
            FileNotFoundError: Se o diretório do módulo não existir.
        """
        curso_dir = self.fm.path("cursos") / curso_slug
        modulo_dir = curso_dir / modulo_dir_nome

        if not modulo_dir.exists():
            raise FileNotFoundError(f"Módulo não encontrado: {modulo_dir}")

        meta = self.fm.ler_metadados_curso(curso_dir)
        contexto = {
            "curso_nome": meta.get("nome", curso_slug) if meta else curso_slug,
            "modulo_nome": modulo_dir_nome.replace("_", " ").title(),
            "projeto_nome": projeto_nome,
        }

        conteudo = self.te.renderizar(TEMPLATE_PROJETO, contexto)
        filename = f"projeto_{slugify(projeto_nome)}.md"
        output_path = modulo_dir / filename

        self.fm.escrever(output_path, conteudo)
        logger.info("Projeto criado: %s", output_path)
        UI.sucesso(f"Projeto criado: {output_path.relative_to(self.fm.root)}")
        return output_path
