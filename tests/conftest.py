"""
Fixtures compartilhadas para todos os testes do CourseForge.

Design das fixtures:
    - Cada teste roda em diretório temporário independente (tmp_path)
    - Nenhum arquivo é escrito fora do diretório temporário
    - fm_temp e te_temp são as únicas instâncias de FileManager/TemplateEngine nos testes
    - O diretório real de templates (templates/) é compartilhado como read-only
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Garantir que a raiz do projeto está no sys.path
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

from utils.file_manager import FileManager
from utils.template_engine import TemplateEngine


@pytest.fixture
def project_root() -> Path:
    """Retorna a raiz real do projeto CourseForge."""
    return PROJECT_ROOT


@pytest.fixture
def templates_dir(project_root: Path) -> Path:
    """Retorna o diretório real de templates (read-only nos testes)."""
    return project_root / "templates"


@pytest.fixture
def prompts_dir(project_root: Path) -> Path:
    """Retorna o diretório real de prompts (read-only nos testes)."""
    return project_root / "prompts"


@pytest.fixture
def fm_temp(tmp_path: Path) -> FileManager:
    """
    FileManager apontando para diretório temporário.
    Cada teste recebe seu próprio tmp_path isolado.
    """
    return FileManager(tmp_path)


@pytest.fixture
def te_real(templates_dir: Path) -> TemplateEngine:
    """
    TemplateEngine usando os templates reais do projeto.
    Permite testar o conteúdo gerado pelos templates.
    """
    return TemplateEngine(templates_dir)


@pytest.fixture
def config_padrao() -> dict:
    """Configuração mínima para testes que precisam de config."""
    return {
        "plataforma": {"nome": "CourseForge", "versao": "1.0.0", "autor_padrao": "Professor"},
        "mkdocs": {
            "site_name": "Test Docs",
            "site_description": "Test",
            "site_author": "Test",
            "theme": {"name": "material", "language": "pt"},
            "markdown_extensions": ["admonition"],
        },
    }
