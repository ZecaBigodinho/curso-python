"""
CourseForge — generators/gerar_exercicio.py

Gerador de arquivos de exercícios para capítulos.

Por que este gerador foi criado?
    A lógica de criação de exercícios estava em main.py (_criar_exercicios),
    violando o SRP: main.py deveria conter APENAS roteamento de menu.

    Ao mover para um gerador dedicado:
    - A lógica pode ser testada isoladamente
    - Pode ser reutilizada por interfaces futuras (GUI, API)
    - Segue o mesmo padrão dos outros geradores
"""
from __future__ import annotations

from pathlib import Path

from utils.file_manager import FileManager
from utils.template_engine import TemplateEngine
from utils.cli_ui import UI
from utils.selectors import selecionar_curso, selecionar_modulo
from utils.slugify import slugify
from utils.constants import TEMPLATE_EXERCICIOS
from utils.logger import get_logger

logger = get_logger(__name__)


class ExercicioGenerator:
    """
    Gera arquivos de exercícios para capítulos existentes.

    Responsabilidades:
    - Selecionar curso e módulo
    - Coletar nome do capítulo de referência
    - Renderizar template de exercícios
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
        """Coleta dados via CLI e cria o arquivo de exercícios."""
        UI.secao("CRIAR EXERCÍCIOS")

        curso_slug = selecionar_curso(self.fm)
        if not curso_slug:
            return None

        modulo_dir_nome = selecionar_modulo(self.fm, curso_slug)
        if not modulo_dir_nome:
            return None

        capitulo_nome = UI.perguntar("Nome do capítulo de referência")
        if not capitulo_nome.strip():
            UI.erro("Nome do capítulo não pode ser vazio.")
            return None

        return self.criar(
            curso_slug=curso_slug,
            modulo_dir_nome=modulo_dir_nome,
            capitulo_nome=capitulo_nome.strip(),
        )

    def criar(
        self,
        curso_slug: str,
        modulo_dir_nome: str,
        capitulo_nome: str,
    ) -> Path:
        """
        Cria arquivo de exercícios (uso programático e interativo).

        Args:
            curso_slug: Slug do curso.
            modulo_dir_nome: Nome do diretório do módulo.
            capitulo_nome: Nome do capítulo de referência.

        Returns:
            Path do arquivo de exercícios criado.

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
            "capitulo_nome": capitulo_nome,
        }

        conteudo = self.te.renderizar(TEMPLATE_EXERCICIOS, contexto)
        filename = f"exercicios_{slugify(capitulo_nome)}.md"
        output_path = modulo_dir / filename

        self.fm.escrever(output_path, conteudo)
        logger.info("Exercícios criados: %s", output_path)
        UI.sucesso(f"Exercícios criados: {output_path.relative_to(self.fm.root)}")
        return output_path
