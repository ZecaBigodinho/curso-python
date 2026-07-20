"""
CourseForge — Modelo de Domínio: Module
Representa um módulo dentro de um curso.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from utils.slugify import slugify


@dataclass
class Module:
    """
    Representa um módulo de um curso no CourseForge.

    Attributes:
        nome: Nome legível do módulo (ex: 'Introdução ao Python')
        curso_slug: Slug do curso ao qual pertence
        numero: Número sequencial do módulo (1-based)
        descricao: Descrição resumida do módulo
        num_capitulos: Quantidade planejada de capítulos
    """

    nome: str
    curso_slug: str
    numero: int
    descricao: str = ""
    num_capitulos: int = 1

    def __post_init__(self) -> None:
        """Valida campos obrigatórios ao construir o objeto."""
        if not self.nome or not self.nome.strip():
            raise ValueError("Module.nome não pode ser vazio.")
        if not self.curso_slug or not self.curso_slug.strip():
            raise ValueError("Module.curso_slug não pode ser vazio.")
        if self.numero < 1:
            raise ValueError(f"Module.numero deve ser >= 1. Recebido: {self.numero}")
        if self.num_capitulos < 1:
            raise ValueError(f"Module.num_capitulos deve ser >= 1. Recebido: {self.num_capitulos}")

    # ------------------------------------------------------------------ #
    # Propriedades derivadas                                               #
    # ------------------------------------------------------------------ #

    @property
    def slug(self) -> str:
        """Slug do nome do módulo."""
        return slugify(self.nome)

    @property
    def diretorio(self) -> str:
        """Nome do diretório do módulo: ex. modulo_01_introducao_ao_python"""
        return f"modulo_{self.numero:02d}_{self.slug}"

    # ------------------------------------------------------------------ #
    # Serialização                                                         #
    # ------------------------------------------------------------------ #

    def to_dict(self) -> dict:
        """Converte o módulo para dicionário (para YAML e templates)."""
        return {
            "nome": self.nome,
            "curso_slug": self.curso_slug,
            "numero": self.numero,
            "descricao": self.descricao,
            "num_capitulos": self.num_capitulos,
            "slug": self.slug,
            "diretorio": self.diretorio,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Module":
        """Reconstrói um Module a partir de dicionário."""
        data = dict(data)
        data.pop("slug", None)
        data.pop("diretorio", None)
        return cls(**data)

    def __str__(self) -> str:
        return f"Module('{self.diretorio}', curso='{self.curso_slug}')"
