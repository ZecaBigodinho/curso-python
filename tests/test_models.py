"""
Testes: models/ (Course, Module, Chapter, Enums)

Verifica a integridade dos modelos de domínio:
- Propriedades derivadas (slug, diretorio, filename)
- Serialização (to_dict / from_dict)
- Validação via __post_init__
- Enums de domínio
"""
from __future__ import annotations

import pytest
from datetime import date

from models.course import Course
from models.module import Module
from models.chapter import Chapter
from models.enums import NivelDificuldade, TipoPrompt


class TestCourse:
    """Testes para o modelo Course."""

    def test_slug_gerado_corretamente(self):
        course = Course(nome="Python para Iniciantes", descricao="", autor="Prof")
        assert course.slug == "python_para_iniciantes"

    def test_slug_com_acentos(self):
        course = Course(nome="Introdução à Programação", descricao="", autor="Prof")
        assert course.slug == "introducao_a_programacao"

    def test_diretorio_igual_slug(self):
        course = Course(nome="Django REST", descricao="", autor="Prof")
        assert course.diretorio == course.slug

    def test_to_dict_contem_campos_obrigatorios(self):
        course = Course(nome="Python", descricao="Desc", autor="Prof", num_modulos=3)
        d = course.to_dict()
        assert d["nome"] == "Python"
        assert d["autor"] == "Prof"
        assert d["num_modulos"] == 3
        assert "slug" in d
        assert "data_criacao" in d

    def test_from_dict_roundtrip(self):
        course = Course(nome="Python", descricao="Desc", autor="Prof", num_modulos=2)
        restored = Course.from_dict(course.to_dict())
        assert restored.nome == course.nome
        assert restored.autor == course.autor
        assert restored.num_modulos == course.num_modulos

    def test_post_init_nome_vazio_levanta_erro(self):
        with pytest.raises(ValueError, match="nome"):
            Course(nome="", descricao="", autor="Prof")

    def test_post_init_autor_vazio_levanta_erro(self):
        with pytest.raises(ValueError, match="autor"):
            Course(nome="Python", descricao="", autor="")

    def test_post_init_num_modulos_invalido(self):
        with pytest.raises(ValueError, match="num_modulos"):
            Course(nome="Python", descricao="", autor="Prof", num_modulos=0)

    def test_str_representacao(self):
        course = Course(nome="Python", descricao="", autor="Prof")
        assert "Python" in str(course)
        assert "python" in str(course)


class TestModule:
    """Testes para o modelo Module."""

    def test_diretorio_formato_correto(self):
        module = Module(nome="Introdução ao Python", curso_slug="python", numero=1)
        assert module.diretorio == "modulo_01_introducao_ao_python"

    def test_diretorio_numero_dois_digitos(self):
        module = Module(nome="Avançado", curso_slug="python", numero=9)
        assert module.diretorio.startswith("modulo_09_")

    def test_slug_derivado_do_nome(self):
        module = Module(nome="Variáveis e Tipos", curso_slug="python", numero=1)
        assert module.slug == "variaveis_e_tipos"

    def test_to_dict_contem_diretorio(self):
        module = Module(nome="Intro", curso_slug="python", numero=1)
        d = module.to_dict()
        assert "diretorio" in d
        assert "slug" in d

    def test_from_dict_roundtrip(self):
        module = Module(nome="Intro", curso_slug="python", numero=2, num_capitulos=3)
        restored = Module.from_dict(module.to_dict())
        assert restored.nome == module.nome
        assert restored.numero == module.numero

    def test_post_init_numero_zero_levanta_erro(self):
        with pytest.raises(ValueError, match="numero"):
            Module(nome="Intro", curso_slug="python", numero=0)

    def test_post_init_curso_slug_vazio_levanta_erro(self):
        with pytest.raises(ValueError, match="curso_slug"):
            Module(nome="Intro", curso_slug="", numero=1)


class TestChapter:
    """Testes para o modelo Chapter."""

    def test_filename_formato_correto(self):
        chapter = Chapter(
            nome="Variáveis e Tipos",
            curso_slug="python",
            modulo_dir="modulo_01_intro",
            numero=1,
        )
        assert chapter.filename == "01_variaveis_e_tipos.md"

    def test_filename_numero_dois_digitos(self):
        chapter = Chapter(
            nome="Funções",
            curso_slug="python",
            modulo_dir="modulo_01_intro",
            numero=5,
        )
        assert chapter.filename.startswith("05_")

    def test_nivel_padrao_intermediario(self):
        chapter = Chapter(
            nome="Funções",
            curso_slug="python",
            modulo_dir="modulo_01_intro",
            numero=1,
        )
        assert chapter.nivel == NivelDificuldade.INTERMEDIARIO

    def test_nivel_aceita_string(self):
        chapter = Chapter(
            nome="Funções",
            curso_slug="python",
            modulo_dir="modulo_01_intro",
            numero=1,
            nivel="iniciante",
        )
        assert chapter.nivel == NivelDificuldade.INICIANTE

    def test_nivel_invalido_levanta_erro(self):
        with pytest.raises(ValueError):
            Chapter(
                nome="Funções",
                curso_slug="python",
                modulo_dir="modulo_01_intro",
                numero=1,
                nivel="super_avancado",
            )

    def test_to_dict_nivel_como_string(self):
        chapter = Chapter(
            nome="Funções",
            curso_slug="python",
            modulo_dir="modulo_01_intro",
            numero=1,
            nivel=NivelDificuldade.AVANCADO,
        )
        d = chapter.to_dict()
        assert d["nivel"] == "avançado"
        assert isinstance(d["nivel"], str)

    def test_from_dict_roundtrip(self):
        chapter = Chapter(
            nome="Funções",
            curso_slug="python",
            modulo_dir="modulo_01_intro",
            numero=2,
            objetivo="Aprender funções",
        )
        restored = Chapter.from_dict(chapter.to_dict())
        assert restored.nome == chapter.nome
        assert restored.numero == chapter.numero
        assert restored.nivel == chapter.nivel


class TestNivelDificuldade:
    """Testes para o Enum NivelDificuldade."""

    def test_valores_disponiveis(self):
        opcoes = NivelDificuldade.opcoes()
        assert "iniciante" in opcoes
        assert "intermediário" in opcoes
        assert "avançado" in opcoes

    def test_from_str_valido(self):
        assert NivelDificuldade.from_str("iniciante") == NivelDificuldade.INICIANTE
        assert NivelDificuldade.from_str("intermediário") == NivelDificuldade.INTERMEDIARIO

    def test_from_str_case_insensitive(self):
        assert NivelDificuldade.from_str("INICIANTE") == NivelDificuldade.INICIANTE

    def test_from_str_invalido_levanta_erro(self):
        with pytest.raises(ValueError, match="Nível inválido"):
            NivelDificuldade.from_str("expert")

    def test_enum_e_string(self):
        """NivelDificuldade.value deve retornar string limpa."""
        nivel = NivelDificuldade.INICIANTE
        assert nivel.value == "iniciante"
        assert f"Nível: {nivel.value}" == "Nível: iniciante"


class TestTipoPrompt:
    """Testes para o Enum TipoPrompt."""

    def test_template_filename(self):
        assert TipoPrompt.CAPITULO.template_filename() == "prompt_capitulo.txt"
        assert TipoPrompt.EXERCICIOS.template_filename() == "prompt_exercicios.txt"
        assert TipoPrompt.PROJETO.template_filename() == "prompt_projeto.txt"

    def test_descricao_nao_vazia(self):
        for tipo in TipoPrompt:
            assert len(tipo.descricao()) > 0
