"""
Testes: generators/gerar_curso.py, gerar_modulo.py, gerar_capitulo.py

Testa a geração programática (sem UI) de cursos, módulos e capítulos.
Todos os arquivos são escritos em tmp_path — nenhum arquivo permanente é criado.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from models.course import Course
from models.module import Module
from models.chapter import Chapter
from models.enums import NivelDificuldade
from generators.gerar_curso import CourseGenerator
from generators.gerar_modulo import ModuleGenerator
from generators.gerar_capitulo import ChapterGenerator
from utils.constants import METADATA_FILENAME


class TestCourseGenerator:
    """Testes para CourseGenerator.criar()."""

    def test_criar_gera_estrutura_completa(self, fm_temp, te_real):
        gen = CourseGenerator(fm_temp, te_real)
        course = Course(nome="Python Básico", descricao="Curso intro", autor="Prof")
        curso_dir = gen.criar(course)

        # Diretório do curso deve existir
        assert curso_dir.exists()
        assert curso_dir.is_dir()

        # docs/index.md deve existir
        index_md = curso_dir / "docs" / "index.md"
        assert index_md.exists()

        # .courseforge.yaml deve existir
        meta_yaml = curso_dir / METADATA_FILENAME
        assert meta_yaml.exists()

    def test_criar_index_md_contem_nome_curso(self, fm_temp, te_real):
        gen = CourseGenerator(fm_temp, te_real)
        course = Course(nome="Django Avançado", descricao="REST APIs", autor="Prof")
        curso_dir = gen.criar(course)

        conteudo = (curso_dir / "docs" / "index.md").read_text(encoding="utf-8")
        assert "Django Avançado" in conteudo

    def test_criar_metadados_contem_slug(self, fm_temp, te_real):
        gen = CourseGenerator(fm_temp, te_real)
        course = Course(nome="Python Básico", descricao="", autor="Prof")
        curso_dir = gen.criar(course)

        meta = fm_temp.ler_metadados_curso(curso_dir)
        assert meta.get("slug") == "python_basico"
        assert meta.get("nome") == "Python Básico"

    def test_criar_slug_como_nome_diretorio(self, fm_temp, te_real):
        gen = CourseGenerator(fm_temp, te_real)
        course = Course(nome="Introdução ao Python", descricao="", autor="Prof")
        curso_dir = gen.criar(course)

        assert curso_dir.name == "introducao_ao_python"

    def test_criar_curso_duplicado_levanta_erro(self, fm_temp, te_real):
        gen = CourseGenerator(fm_temp, te_real)
        course = Course(nome="Python Básico", descricao="", autor="Prof")
        gen.criar(course)  # Primeira criação OK

        with pytest.raises(FileExistsError):
            gen.criar(course)  # Segunda criação deve falhar


class TestModuleGenerator:
    """Testes para ModuleGenerator.criar()."""

    @pytest.fixture
    def curso_dir(self, fm_temp, te_real) -> Path:
        """Cria um curso de teste e retorna seu diretório."""
        gen = CourseGenerator(fm_temp, te_real)
        course = Course(nome="Python Básico", descricao="", autor="Prof")
        return gen.criar(course)

    def test_criar_gera_diretorio_numerado(self, fm_temp, te_real, curso_dir):
        gen = ModuleGenerator(fm_temp, te_real)
        module = Module(nome="Introdução", curso_slug="python_basico", numero=1)
        modulo_dir = gen.criar(module)

        assert modulo_dir.exists()
        assert modulo_dir.name == "modulo_01_introducao"

    def test_criar_gera_index_md(self, fm_temp, te_real, curso_dir):
        gen = ModuleGenerator(fm_temp, te_real)
        module = Module(nome="Introdução", curso_slug="python_basico", numero=1)
        modulo_dir = gen.criar(module)

        assert (modulo_dir / "index.md").exists()

    def test_criar_gera_placeholders(self, fm_temp, te_real, curso_dir):
        gen = ModuleGenerator(fm_temp, te_real)
        module = Module(nome="Funções", curso_slug="python_basico", numero=1, num_capitulos=3)
        modulo_dir = gen.criar(module)

        # Deve ter index.md + 3 placeholders
        arquivos_md = list(modulo_dir.glob("*.md"))
        assert len(arquivos_md) == 4  # index + 3 placeholders

    def test_criar_modulo_duplicado_levanta_erro(self, fm_temp, te_real, curso_dir):
        gen = ModuleGenerator(fm_temp, te_real)
        module = Module(nome="Introdução", curso_slug="python_basico", numero=1)
        gen.criar(module)

        with pytest.raises(FileExistsError):
            gen.criar(module)


class TestChapterGenerator:
    """Testes para ChapterGenerator.criar()."""

    @pytest.fixture
    def modulo_dir(self, fm_temp, te_real) -> Path:
        """Cria curso + módulo de teste e retorna o diretório do módulo."""
        cg = CourseGenerator(fm_temp, te_real)
        course = Course(nome="Python", descricao="", autor="Prof")
        cg.criar(course)

        mg = ModuleGenerator(fm_temp, te_real)
        module = Module(nome="Introducao", curso_slug="python", numero=1)
        return mg.criar(module)

    def test_criar_gera_arquivo_numerado(self, fm_temp, te_real, modulo_dir):
        gen = ChapterGenerator(fm_temp, te_real)
        chapter = Chapter(
            nome="Variáveis e Tipos",
            curso_slug="python",
            modulo_dir="modulo_01_introducao",
            numero=1,
        )
        cap_path = gen.criar(chapter)

        assert cap_path.exists()
        assert cap_path.name == "01_variaveis_e_tipos.md"

    def test_criar_conteudo_template_completo(self, fm_temp, te_real, modulo_dir):
        gen = ChapterGenerator(fm_temp, te_real)
        chapter = Chapter(
            nome="Funcoes",
            curso_slug="python",
            modulo_dir="modulo_01_introducao",
            numero=2,
            objetivo="Aprender funções",
        )
        cap_path = gen.criar(chapter)
        conteudo = cap_path.read_text(encoding="utf-8")

        # Template deve gerar seções obrigatórias
        assert "## " in conteudo  # Pelo menos uma seção H2
        assert "Funcoes" in conteudo  # Nome do capítulo

    def test_criar_capitulo_com_nivel_enum(self, fm_temp, te_real, modulo_dir):
        gen = ChapterGenerator(fm_temp, te_real)
        chapter = Chapter(
            nome="Decorators",
            curso_slug="python",
            modulo_dir="modulo_01_introducao",
            numero=3,
            nivel=NivelDificuldade.AVANCADO,
        )
        cap_path = gen.criar(chapter)
        assert cap_path.exists()

    def test_criar_capitulo_duplicado_levanta_erro(self, fm_temp, te_real, modulo_dir):
        gen = ChapterGenerator(fm_temp, te_real)
        chapter = Chapter(
            nome="Variaveis",
            curso_slug="python",
            modulo_dir="modulo_01_introducao",
            numero=1,
        )
        gen.criar(chapter)

        with pytest.raises(FileExistsError):
            gen.criar(chapter)
