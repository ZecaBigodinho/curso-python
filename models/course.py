"""
CourseForge — Models de Domínio: Course
Representa um curso completo na plataforma.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import List

from utils.slugify import slugify


@dataclass
class Course:
    """
    Representa um curso completo na plataforma CourseForge.

    Attributes:
        nome: Nome legível do curso (ex: 'Python para Iniciantes')
        descricao: Descrição resumida do curso
        autor: Nome do autor/instrutor
        num_modulos: Quantidade planejada de módulos
        data_criacao: Data de criação (default: hoje)
        versao: Versão da apostila
        tags: Lista de tags/categorias
    """

    nome: str
    descricao: str
    autor: str
    num_modulos: int = 1
    data_criacao: date = field(default_factory=date.today)
    versao: str = "1.0.0"
    tags: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Valida campos obrigatórios ao construir o objeto."""
        if not self.nome or not self.nome.strip():
            raise ValueError("Course.nome não pode ser vazio.")
        if not self.autor or not self.autor.strip():
            raise ValueError("Course.autor não pode ser vazio.")
        if self.num_modulos < 1:
            raise ValueError(f"Course.num_modulos deve ser >= 1. Recebido: {self.num_modulos}")

    # ------------------------------------------------------------------ #
    # Propriedades derivadas                                               #
    # ------------------------------------------------------------------ #

    @property
    def slug(self) -> str:
        """Slug do curso — usado como nome de diretório em cursos/."""
        return slugify(self.nome)

    @property
    def diretorio(self) -> str:
        """Alias de slug para legibilidade nos geradores."""
        return self.slug

    # ------------------------------------------------------------------ #
    # Serialização                                                         #
    # ------------------------------------------------------------------ #

    def to_dict(self) -> dict:
        """Converte o curso para dicionário (para YAML e templates Jinja2)."""
        return {
            "nome": self.nome,
            "descricao": self.descricao,
            "autor": self.autor,
            "num_modulos": self.num_modulos,
            "data_criacao": self.data_criacao.isoformat(),
            "versao": self.versao,
            "tags": self.tags,
            "slug": self.slug,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Course":
        """Reconstrói um Course a partir de dicionário (ex: YAML de metadados)."""
        data = dict(data)
        if "data_criacao" in data and isinstance(data["data_criacao"], str):
            data["data_criacao"] = date.fromisoformat(data["data_criacao"])
        data.pop("slug", None)  # slug é derivado, nunca armazenado
        return cls(**data)

    def __str__(self) -> str:
        return f"Course(nome='{self.nome}', slug='{self.slug}', módulos={self.num_modulos})"
