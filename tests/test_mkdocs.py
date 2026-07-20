"""
Testes: generators/atualizar_mkdocs.py

Verifica a geração do mkdocs.yml com estruturas de curso simples e complexas.
"""
from __future__ import annotations

import yaml
from pathlib import Path

import pytest

from models.course import Course
from models.module import Module
from models.chapter import Chapter
from generators.gerar_curso import CourseGenerator
from generators.gerar_modulo import ModuleGenerator
from generators.gerar_capitulo import ChapterGenerator
from generators.atualizar_mkdocs import MkDocsUpdater
from utils.constants import MKDOCS_FILENAME


class TestMkDocsUpdater:
    """Testes para MkDocsUpdater."""

    @pytest.fixture
    def updater(self, fm_temp, config_padrao) -> MkDocsUpdater:
        """Retorna um MkDocsUpdater apontando para tmp_path."""
        return MkDocsUpdater(fm_temp, config_padrao)

    @pytest.fixture
    def estrutura_completa(self, fm_temp, te_real) -> Path:
        """
        Cria estrutura curso → módulo → capítulo em tmp_path.
        Retorna o diretório tmp_path.
        """
        cg = CourseGenerator(fm_temp, te_real)
        course = Course(nome="Python Básico", descricao="Desc", autor="Prof")
        cg.criar(course)

        mg = ModuleGenerator(fm_temp, te_real)
        module = Module(nome="Introducao", curso_slug="python_basico", numero=1)
        mg.criar(module)

        chg = ChapterGenerator(fm_temp, te_real)
        chapter = Chapter(
            nome="Variaveis",
            curso_slug="python_basico",
            modulo_dir="modulo_01_introducao",
            numero=1,
        )
        chg.criar(chapter)

        return fm_temp.root

    def test_gerar_cria_mkdocs_yml(self, updater, estrutura_completa):
        output = updater.atualizar(silencioso=True)
        assert output.exists()
        assert output.name == MKDOCS_FILENAME

    def test_mkdocs_yml_e_yaml_valido(self, updater, estrutura_completa):
        output = updater.atualizar(silencioso=True)
        conteudo = output.read_text(encoding="utf-8")
        parsed = yaml.safe_load(conteudo)
        assert isinstance(parsed, dict)

    def test_mkdocs_yml_contem_site_name(self, updater, estrutura_completa):
        output = updater.atualizar(silencioso=True)
        parsed = yaml.safe_load(output.read_text(encoding="utf-8"))
        assert "site_name" in parsed

    def test_mkdocs_yml_contem_nav(self, updater, estrutura_completa):
        output = updater.atualizar(silencioso=True)
        parsed = yaml.safe_load(output.read_text(encoding="utf-8"))
        assert "nav" in parsed
        assert isinstance(parsed["nav"], list)

    def test_nav_contem_home(self, updater, estrutura_completa):
        output = updater.atualizar(silencioso=True)
        parsed = yaml.safe_load(output.read_text(encoding="utf-8"))
        nav = parsed["nav"]
        # Primeiro item deve ser Home
        assert nav[0] == {"Home": "index.md"}

    def test_nav_contem_curso(self, updater, estrutura_completa):
        output = updater.atualizar(silencioso=True)
        parsed = yaml.safe_load(output.read_text(encoding="utf-8"))
        nav = parsed["nav"]
        # Deve ter pelo menos o Home + 1 curso
        assert len(nav) >= 2

    def test_nav_usa_nome_legivel_do_curso(self, updater, estrutura_completa):
        """O nav deve usar o nome do metadata, não o slug."""
        output = updater.atualizar(silencioso=True)
        parsed = yaml.safe_load(output.read_text(encoding="utf-8"))
        nav = parsed["nav"]
        # O nome do curso no nav deve ser "Python Básico", não "python_basico"
        nav_keys = [list(item.keys())[0] for item in nav if isinstance(item, dict)]
        assert "Python Básico" in nav_keys

    def test_atualizar_silencioso_alias(self, updater, estrutura_completa):
        """atualizar_silencioso deve ser equivalente a atualizar(silencioso=True)."""
        output = updater.atualizar_silencioso()
        assert output.exists()

    def test_sem_cursos_nav_apenas_home(self, updater, fm_temp):
        """Sem cursos, nav deve ter apenas Home."""
        fm_temp.criar_diretorio(fm_temp.path("cursos"))
        output = updater.atualizar(silencioso=True)
        parsed = yaml.safe_load(output.read_text(encoding="utf-8"))
        assert parsed["nav"] == [{"Home": "index.md"}]
