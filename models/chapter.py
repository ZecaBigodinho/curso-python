"""
CourseForge — Modelo de Domínio: Chapter
Representa um capítulo dentro de um módulo.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from models.enums import NivelDificuldade
from utils.slugify import slugify


@dataclass
class Chapter:
    """
    Representa um capítulo de um módulo no CourseForge.

    Attributes:
        nome: Nome legível do capítulo (ex: 'Variáveis e Tipos de Dados')
        curso_slug: Slug do curso pai
        modulo_dir: Diretório do módulo pai (ex: 'modulo_01_introducao')
        numero: Número sequencial do capítulo dentro do módulo
        objetivo: Objetivo principal do capítulo (opcional)
        prerequisitos: Lista de pré-requisitos (opcional)
        nivel: Nível de dificuldade (NivelDificuldade Enum)
    """

    nome: str
    curso_slug: str
    modulo_dir: str
    numero: int
    objetivo: str = ""
    prerequisitos: List[str] = field(default_factory=list)
    nivel: NivelDificuldade = NivelDificuldade.INTERMEDIARIO

    def __post_init__(self) -> None:
        """Valida e normaliza campos ao construir o objeto."""
        if not self.nome or not self.nome.strip():
            raise ValueError("Chapter.nome não pode ser vazio.")
        if not self.curso_slug or not self.curso_slug.strip():
            raise ValueError("Chapter.curso_slug não pode ser vazio.")
        if not self.modulo_dir or not self.modulo_dir.strip():
            raise ValueError("Chapter.modulo_dir não pode ser vazio.")
        if self.numero < 1:
            raise ValueError(f"Chapter.numero deve ser >= 1. Recebido: {self.numero}")

        # Converter string para Enum se necessário (para compatibilidade com from_dict)
        if isinstance(self.nivel, str):
            self.nivel = NivelDificuldade.from_str(self.nivel)

    # ------------------------------------------------------------------ #
    # Propriedades derivadas                                               #
    # ------------------------------------------------------------------ #

    @property
    def slug(self) -> str:
        """Slug do nome do capítulo."""
        return slugify(self.nome)

    @property
    def filename(self) -> str:
        """Nome do arquivo Markdown: ex. 01_variaveis_e_tipos_de_dados.md"""
        return f"{self.numero:02d}_{self.slug}.md"

    # ------------------------------------------------------------------ #
    # Serialização                                                         #
    # ------------------------------------------------------------------ #

    def to_dict(self) -> dict:
        """Converte o capítulo para dicionário (para YAML e templates Jinja2)."""
        return {
            "nome": self.nome,
            "curso_slug": self.curso_slug,
            "modulo_dir": self.modulo_dir,
            "numero": self.numero,
            "objetivo": self.objetivo,
            "prerequisitos": self.prerequisitos,
            "nivel": self.nivel.value,  # valor legível do Enum para templates/YAML
            "slug": self.slug,
            "filename": self.filename,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Chapter":
        """Reconstrói um Chapter a partir de dicionário."""
        data = dict(data)
        data.pop("slug", None)
        data.pop("filename", None)
        return cls(**data)

    def __str__(self) -> str:
        return f"Chapter('{self.filename}', módulo='{self.modulo_dir}')"
