"""
CourseForge — models/enums.py

Enumerações do domínio da plataforma.

Por que Enum e não strings literais?
    Strings como "iniciante", "intermediário", "avançado" espalhadas pelo código
    são frágeis: um typo silencioso ("inicante") passa pela validação de tipo
    do Python sem erro.

    Com Enum:
    - Autocompletar na IDE
    - Type checking em tempo de análise estática
    - Adição de novo nível em UM lugar → reflete em todo o sistema
    - Uso como str (herda de str) para compatibilidade com YAML/JSON

Decisão: herdar de (str, Enum) permite usar os valores diretamente
    como strings em templates Jinja2, YAML e comparações, sem `.value`.
"""
from __future__ import annotations

from enum import Enum


class NivelDificuldade(str, Enum):
    """Nível de dificuldade de um capítulo ou exercício."""

    INICIANTE = "iniciante"
    INTERMEDIARIO = "intermediário"
    AVANCADO = "avançado"

    @classmethod
    def opcoes(cls) -> list[str]:
        """Retorna lista de valores válidos (para exibição em menus)."""
        return [nivel.value for nivel in cls]

    @classmethod
    def from_str(cls, valor: str) -> "NivelDificuldade":
        """
        Converte string para NivelDificuldade.

        Args:
            valor: String do nível.

        Returns:
            NivelDificuldade correspondente.

        Raises:
            ValueError: Se o valor não for reconhecido.
        """
        valor_norm = valor.strip().lower()
        for nivel in cls:
            if nivel.value == valor_norm:
                return nivel
        opcoes = ", ".join(f"'{n.value}'" for n in cls)
        raise ValueError(
            f"Nível inválido: '{valor}'. Opções válidas: {opcoes}."
        )


class TipoPrompt(str, Enum):
    """Tipo de prompt para geração de conteúdo com IA."""

    CAPITULO = "capitulo"
    EXERCICIOS = "exercicios"
    PROJETO = "projeto"

    def template_filename(self) -> str:
        """Retorna o nome do arquivo de template correspondente."""
        return f"prompt_{self.value}.txt"

    def descricao(self) -> str:
        """Retorna descrição legível para exibição em menu."""
        descricoes = {
            TipoPrompt.CAPITULO: "Capítulo Completo",
            TipoPrompt.EXERCICIOS: "Lista de Exercícios",
            TipoPrompt.PROJETO: "Projeto Prático",
        }
        return descricoes[self]
