"""
Testes: generators/gerar_prompt.py

Verifica a geração programática de prompts via templates Jinja2.
Não testa a interface interativa (que depende de input do usuário).
"""
from __future__ import annotations

import pytest

from models.enums import TipoPrompt, NivelDificuldade
from generators.gerar_prompt import PromptGenerator


class TestPromptGenerator:
    """Testes para PromptGenerator.gerar()."""

    @pytest.fixture
    def gen(self, fm_temp, te_real, prompts_dir) -> PromptGenerator:
        """
        PromptGenerator com engine de prompts apontando para prompts/ real.
        fm_temp garante que qualquer arquivo salvo vai para tmp_path.
        """
        return PromptGenerator(fm_temp, te_real)

    def test_gerar_prompt_capitulo(self, gen):
        contexto = {
            "curso": "Python Básico",
            "tema": "Variáveis",
            "nivel": NivelDificuldade.INICIANTE,
            "capitulo": "Variáveis e Tipos",
            "objetivo": "Entender variáveis",
            "palavras_minimas": 1500,
        }
        prompt = gen.gerar(TipoPrompt.CAPITULO, contexto)
        assert isinstance(prompt, str)
        assert len(prompt) > 100
        assert "Python Básico" in prompt or "python" in prompt.lower()

    def test_gerar_prompt_exercicios(self, gen):
        contexto = {
            "curso": "Django REST",
            "tema": "APIs",
            "nivel": NivelDificuldade.INTERMEDIARIO,
            "capitulo": "Views e Serializers",
            "quantidade": 10,
        }
        prompt = gen.gerar(TipoPrompt.EXERCICIOS, contexto)
        assert isinstance(prompt, str)
        assert len(prompt) > 50

    def test_gerar_prompt_projeto(self, gen):
        contexto = {
            "curso": "Python Básico",
            "tema": "POO",
            "nivel": NivelDificuldade.INTERMEDIARIO,
            "modulo": "Módulo 3",
            "projeto": "Sistema de Biblioteca",
            "objetivo": "Aplicar POO",
            "tecnologias": "Python, SQLite",
        }
        prompt = gen.gerar(TipoPrompt.PROJETO, contexto)
        assert isinstance(prompt, str)
        assert len(prompt) > 50

    def test_salvar_cria_arquivo_txt(self, gen):
        contexto = {
            "curso": "Python",
            "tema": "Variáveis",
            "nivel": NivelDificuldade.INICIANTE,
            "capitulo": "Vars",
            "objetivo": "Aprender",
            "palavras_minimas": 500,
        }
        prompt = gen.gerar(TipoPrompt.CAPITULO, contexto)
        path = gen._salvar(prompt, TipoPrompt.CAPITULO)
        assert path.exists()
        assert path.suffix == ".txt"
        assert path.read_text(encoding="utf-8") == prompt
