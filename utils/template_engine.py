"""
CourseForge — TemplateEngine
Motor de renderização de templates usando Jinja2.
Carrega templates do diretório `templates/` e processa variáveis.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, StrictUndefined, TemplateNotFound


class TemplateEngine:
    """
    Motor de templates baseado em Jinja2.

    Responsável por carregar e renderizar todos os templates
    da plataforma CourseForge (Markdown, YAML, TXT).

    Por que Jinja2?
    - Suporta variáveis, loops e condicionais nos templates
    - Permite criar templates ricos sem lógica Python embutida
    - Fácil de escalar para novos tipos de conteúdo
    """

    def __init__(self, templates_dir: Path):
        """
        Args:
            templates_dir: Caminho para o diretório de templates.
        """
        self.templates_dir = templates_dir.resolve()
        self._env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            undefined=StrictUndefined,   # Levanta erro em variáveis não definidas
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
        )

    def renderizar(self, template_nome: str, contexto: dict[str, Any]) -> str:
        """
        Renderiza um template com o contexto fornecido.

        Args:
            template_nome: Nome do arquivo de template (ex: 'capitulo.md')
            contexto: Dicionário de variáveis para o template.

        Returns:
            String renderizada.

        Raises:
            TemplateNotFound: Se o template não existir.
            UndefinedError: Se uma variável do template não estiver no contexto.
        """
        try:
            template = self._env.get_template(template_nome)
            return template.render(**contexto)
        except TemplateNotFound:
            raise FileNotFoundError(
                f"Template '{template_nome}' não encontrado em '{self.templates_dir}'"
            )

    def listar_templates(self) -> list[str]:
        """Lista todos os templates disponíveis."""
        return sorted(self._env.list_templates())

    def template_existe(self, nome: str) -> bool:
        """Verifica se um template existe."""
        return (self.templates_dir / nome).exists()

    def renderizar_string(self, texto: str, contexto: dict[str, Any]) -> str:
        """
        Renderiza uma string de template diretamente (sem arquivo).
        Útil para prompts e textos dinâmicos curtos.
        """
        template = self._env.from_string(texto)
        return template.render(**contexto)
