"""
CourseForge — utils/validators.py

Funções de validação de entradas do usuário.

Por que separar dos geradores?
    Validação é uma responsabilidade independente de geração.
    Ao separar, é possível testar validações sem instanciar geradores,
    e os geradores podem usar a mesma validação independentemente.

Convenção de nomes:
    validate_<campo>(valor, ...) -> valor_normalizado
    Todas as funções retornam o valor normalizado (com strip aplicado)
    e levantam ValueError se inválido.
"""
from __future__ import annotations

import re

from utils.constants import (
    NOME_MIN_LEN, NOME_MAX_LEN,
    AUTOR_MIN_LEN, AUTOR_MAX_LEN,
)


# ------------------------------------------------------------------ #
# Constante exportada para retrocompatibilidade                       #
# ------------------------------------------------------------------ #
# Os módulos que usavam validators.NIVEIS_VALIDOS devem migrar para
# models.enums.NivelDificuldade.opcoes(), mas mantemos aqui para
# não quebrar código legado até a próxima sprint.
NIVEIS_VALIDOS = ("iniciante", "intermediário", "avançado")


# ------------------------------------------------------------------ #
# Validadores de texto                                                #
# ------------------------------------------------------------------ #

def validate_nome(valor: str, campo: str = "Nome") -> str:
    """
    Valida e normaliza um nome de curso/módulo/capítulo.

    Regras:
        - Mínimo de 2 caracteres (após strip)
        - Máximo de 100 caracteres
        - Sem caracteres de controle

    Args:
        valor: Texto inserido pelo usuário.
        campo: Nome do campo para mensagens de erro.

    Returns:
        Valor normalizado (strip aplicado).

    Raises:
        ValueError: Se a validação falhar.
    """
    valor = valor.strip() if valor else ""
    if len(valor) < NOME_MIN_LEN:
        raise ValueError(f"{campo} deve ter pelo menos {NOME_MIN_LEN} caracteres.")
    if len(valor) > NOME_MAX_LEN:
        raise ValueError(f"{campo} deve ter no máximo {NOME_MAX_LEN} caracteres.")
    if re.search(r"[\x00-\x1f]", valor):
        raise ValueError(f"{campo} contém caracteres de controle inválidos.")
    return valor


def validate_descricao(valor: str) -> str:
    """
    Normaliza uma descrição (campo opcional).

    Args:
        valor: Texto da descrição.

    Returns:
        Descrição com strip aplicado (pode ser string vazia).
    """
    return valor.strip() if valor else ""


def validate_autor(valor: str) -> str:
    """
    Valida o nome do autor/instrutor.

    Regras:
        - Mínimo de 2 caracteres (após strip)
        - Máximo de 80 caracteres

    Args:
        valor: Nome do autor.

    Returns:
        Nome normalizado.

    Raises:
        ValueError: Se a validação falhar.
    """
    valor = valor.strip() if valor else ""
    if len(valor) < AUTOR_MIN_LEN:
        raise ValueError(f"Autor deve ter pelo menos {AUTOR_MIN_LEN} caracteres.")
    if len(valor) > AUTOR_MAX_LEN:
        raise ValueError(f"Autor deve ter no máximo {AUTOR_MAX_LEN} caracteres.")
    return valor


# ------------------------------------------------------------------ #
# Validadores numéricos                                               #
# ------------------------------------------------------------------ #

def validate_numero(
    valor: int,
    campo: str = "Número",
    minimo: int = 1,
    maximo: int = 200,
) -> int:
    """
    Valida um número inteiro dentro de um range.

    Args:
        valor: Número a validar.
        campo: Nome do campo para mensagens de erro.
        minimo: Valor mínimo aceito (inclusivo).
        maximo: Valor máximo aceito (inclusivo).

    Returns:
        O número validado (sem alteração).

    Raises:
        ValueError: Se estiver fora do range.
    """
    if not (minimo <= valor <= maximo):
        raise ValueError(
            f"{campo} deve estar entre {minimo} e {maximo}. Recebido: {valor}."
        )
    return valor


# ------------------------------------------------------------------ #
# Validadores de seleção                                              #
# ------------------------------------------------------------------ #

def validate_nivel(valor: str) -> str:
    """
    Valida o nível de dificuldade.

    Args:
        valor: Nível informado pelo usuário.

    Returns:
        Nível normalizado (lowercase, strip).

    Raises:
        ValueError: Se o nível não for reconhecido.

    Note:
        Prefira usar NivelDificuldade.from_str() para novas implementações.
    """
    valor = valor.strip().lower() if valor else ""
    if valor not in NIVEIS_VALIDOS:
        raise ValueError(
            f"Nível inválido: '{valor}'. Opções: {', '.join(NIVEIS_VALIDOS)}."
        )
    return valor


def validate_slug_unico(slug: str, existentes: list[str], entidade: str = "Item") -> None:
    """
    Verifica que um slug não conflita com slugs existentes.

    Args:
        slug: Slug a verificar.
        existentes: Lista de slugs já cadastrados.
        entidade: Nome da entidade para mensagem de erro.

    Raises:
        ValueError: Se o slug já existir na lista.
    """
    if slug in existentes:
        raise ValueError(f"{entidade} '{slug}' já existe na plataforma.")
