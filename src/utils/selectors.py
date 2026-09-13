"""
CourseForge — utils/selectors.py

Funções de seleção interativa de entidades da plataforma.

Por que módulo dedicado?
    A lógica de "listar cursos disponíveis e pedir que o usuário selecione um"
    estava copiada em gerar_modulo.py, gerar_capitulo.py e main.py (2x).

    Qualquer melhoria (ex: mostrar nome legível do curso em vez do slug,
    adicionar opção de criar novo curso inline) precisaria ser feita em
    4 lugares diferentes.

    Este módulo é o único responsável por essas interações de seleção.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from utils.file_manager import FileManager
from utils.cli_ui import UI
from utils.constants import MODULE_DIR_PREFIX
from utils.logger import get_logger

logger = get_logger(__name__)


def selecionar_curso(fm: FileManager) -> Optional[str]:
    """
    Lista cursos disponíveis e solicita seleção ao usuário.

    Args:
        fm: Gerenciador de arquivos para localizar os cursos.

    Returns:
        Slug do curso selecionado, ou None se não houver cursos.
    """
    cursos_dir = fm.path("cursos")
    pastas = fm.listar_subdiretorios(cursos_dir)

    if not pastas:
        UI.aviso("Nenhum curso encontrado. Crie um curso primeiro (opção 1).")
        logger.warning("Tentativa de seleção de curso com cursos/ vazio.")
        return None

    # Montar opções mostrando nome legível (do metadata) + slug
    opcoes_display = []
    slugs = []
    for pasta in pastas:
        meta = fm.ler_metadados_curso(pasta)
        nome_display = meta.get("nome", pasta.name) if meta else pasta.name
        opcoes_display.append(f"{nome_display}  [{pasta.name}]")
        slugs.append(pasta.name)

    escolha_display = UI.selecionar("Selecione o curso", opcoes_display)
    idx = opcoes_display.index(escolha_display)
    curso_slug = slugs[idx]

    logger.info("Curso selecionado: %s", curso_slug)
    return curso_slug


def selecionar_modulo(fm: FileManager, curso_slug: str) -> Optional[str]:
    """
    Lista módulos de um curso e solicita seleção ao usuário.

    Args:
        fm: Gerenciador de arquivos.
        curso_slug: Slug do curso pai.

    Returns:
        Nome do diretório do módulo selecionado, ou None se não houver módulos.
    """
    curso_dir = fm.path("cursos") / curso_slug
    modulos = [
        p.name
        for p in fm.listar_subdiretorios(curso_dir)
        if p.name.startswith(MODULE_DIR_PREFIX)
    ]

    if not modulos:
        UI.aviso("Nenhum módulo encontrado neste curso. Crie um módulo primeiro (opção 2).")
        logger.warning("Tentativa de seleção de módulo em curso '%s' sem módulos.", curso_slug)
        return None

    modulo_dir = UI.selecionar("Selecione o módulo", modulos)
    logger.info("Módulo selecionado: %s", modulo_dir)
    return modulo_dir


def listar_cursos_info(fm: FileManager) -> list[dict]:
    """
    Retorna lista de informações resumidas de todos os cursos.

    Args:
        fm: Gerenciador de arquivos.

    Returns:
        Lista de dicts com 'slug', 'nome', 'autor', 'num_modulos', 'versao'.
    """
    cursos_dir = fm.path("cursos")
    resultado = []

    for pasta in fm.listar_subdiretorios(cursos_dir):
        meta = fm.ler_metadados_curso(pasta)
        if meta:
            resultado.append({
                "slug": meta.get("slug", pasta.name),
                "nome": meta.get("nome", pasta.name),
                "autor": meta.get("autor", "?"),
                "num_modulos": meta.get("num_modulos", "?"),
                "versao": meta.get("versao", "1.0.0"),
            })
        else:
            resultado.append({
                "slug": pasta.name,
                "nome": pasta.name,
                "autor": "?",
                "num_modulos": "?",
                "versao": "?",
            })

    return resultado
