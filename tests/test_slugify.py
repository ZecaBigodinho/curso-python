"""
Testes: utils/slugify.py

Verifica o comportamento da função slugify para todos os casos de uso
da plataforma CourseForge, incluindo caracteres especiais PT-BR.
"""
from __future__ import annotations

import pytest
from utils.slugify import slugify


class TestSlugify:
    """Testes para a função slugify."""

    def test_texto_simples(self):
        assert slugify("Python para Iniciantes") == "python_para_iniciantes"

    def test_acentos_portugues(self):
        assert slugify("Introdução à Programação") == "introducao_a_programacao"

    def test_cedilha(self):
        assert slugify("Lógica e Programação") == "logica_e_programacao"

    def test_til(self):
        assert slugify("Coleções e Iterações") == "colecoes_e_iteracoes"

    def test_caracteres_especiais_removidos(self):
        assert slugify("C# e .NET Framework!") == "c_e_net_framework"

    def test_multiplos_espacos(self):
        assert slugify("Python   para   Iniciantes") == "python_para_iniciantes"

    def test_string_vazia(self):
        assert slugify("") == "sem_nome"

    def test_apenas_espacos(self):
        assert slugify("   ") == "sem_nome"

    def test_underscores_existentes(self):
        result = slugify("python_basico")
        assert result == "python_basico"

    def test_truncamento(self):
        texto_longo = "a" * 100
        result = slugify(texto_longo, max_len=10)
        assert len(result) <= 10

    def test_numeros_preservados(self):
        assert slugify("Python 3.12 Avançado") == "python_312_avancado"

    def test_hifen_vira_underscore(self):
        assert slugify("django-rest-framework") == "django_rest_framework"

    def test_case_insensitive(self):
        assert slugify("PYTHON") == "python"

    def test_consistencia(self):
        """Mesma entrada sempre produz o mesmo output."""
        texto = "Variáveis e Tipos de Dados"
        assert slugify(texto) == slugify(texto)
