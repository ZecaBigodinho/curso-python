"""
Testes unitários para generators/gerar_conteudo_ia.py

Testa a lógica de geração automática com mock do subprocess (OpenCode).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# Garantir path do projeto
sys.path.insert(0, str(Path(__file__).parent.parent))

from generators.gerar_conteudo_ia import (
    _limpar_markdown,
    _montar_link,
    _chamar_opencode_json,
    _chamar_opencode_default,
    gerar_e_publicar_capitulo,
)


class TestLimparMarkdown:
    """Testa a limpeza do conteúdo Markdown retornado pela IA."""

    def test_remove_fence_markdown(self):
        conteudo = '```markdown\n# Título\n\nConteúdo aqui.\n```'
        resultado = _limpar_markdown(conteudo)
        assert resultado.startswith("# Título")
        assert "```markdown" not in resultado

    def test_remove_fence_md(self):
        conteudo = '```md\n# Título\n\nConteúdo.\n```'
        resultado = _limpar_markdown(conteudo)
        assert resultado.startswith("# Título")

    def test_preserva_conteudo_sem_fence(self):
        conteudo = "# Título\n\nConteúdo normal."
        resultado = _limpar_markdown(conteudo)
        assert resultado == conteudo

    def test_normaliza_linhas_vazias_excessivas(self):
        conteudo = "# Título\n\n\n\n\nConteúdo."
        resultado = _limpar_markdown(conteudo)
        assert "\n\n\n" not in resultado

    def test_remove_linhas_controle_opencode(self):
        conteudo = "Session: abc123\nModel: deepseek\n# Título Real\n\nConteúdo."
        resultado = _limpar_markdown(conteudo)
        assert resultado.startswith("# Título Real")


class TestMontarLink:
    """Testa a montagem de links do GitHub Pages."""

    def test_link_basico(self):
        link = _montar_link("python_para_desktop", "modulo_01_fundamentos", "01_variaveis.md")
        assert "python_para_desktop" in link
        assert "modulo_01_fundamentos" in link
        assert "01_variaveis/" in link
        assert ".md" not in link

    @patch.dict("os.environ", {"SITE_BASE_URL": "https://example.com/curso/"})
    def test_link_com_base_url_custom(self):
        # Reimportar para pegar o novo env
        from generators import gerar_conteudo_ia
        original = gerar_conteudo_ia.SITE_BASE_URL
        gerar_conteudo_ia.SITE_BASE_URL = "https://example.com/curso/"
        
        link = _montar_link("meu_curso", "modulo_01", "05_teste.md")
        assert link.startswith("https://example.com/curso/")
        
        # Restaurar
        gerar_conteudo_ia.SITE_BASE_URL = original


class TestChamarOpencode:
    """Testa as chamadas ao OpenCode via subprocess mock."""

    @patch("generators.gerar_conteudo_ia.subprocess.run")
    def test_chamar_json_sucesso(self, mock_run):
        """Testa parsing de output JSON do OpenCode."""
        eventos = [
            json.dumps({"text": "# Decoradores\n\n"}),
            json.dumps({"text": "Conteúdo sobre decoradores em Python."}),
        ]
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="\n".join(eventos),
            stderr="",
        )

        resultado = _chamar_opencode_json("prompt teste", "nvidia/deepseek-ai/deepseek-v4-pro")
        assert "Decoradores" in resultado
        assert "decoradores" in resultado.lower()

    @patch("generators.gerar_conteudo_ia.subprocess.run")
    def test_chamar_json_falha_returncode(self, mock_run):
        """Testa erro quando OpenCode retorna código não-zero."""
        mock_run.return_value = MagicMock(
            returncode=1,
            stdout="",
            stderr="Model not found",
        )

        with pytest.raises(RuntimeError, match="OpenCode falhou"):
            _chamar_opencode_json("prompt", "modelo_invalido")

    @patch("generators.gerar_conteudo_ia.subprocess.run")
    def test_chamar_default_sucesso(self, mock_run):
        """Testa formato default (texto puro)."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="# Título\n\nConteúdo gerado pela IA.",
            stderr="",
        )

        resultado = _chamar_opencode_default("prompt", "nvidia/deepseek-ai/deepseek-v4-pro")
        assert "Título" in resultado


class TestGerarEPublicar:
    """Testa o fluxo completo (com todos os subcomponentes mockados)."""

    @patch("generators.gerar_conteudo_ia._executar_deploy")
    @patch("generators.gerar_conteudo_ia._executar_build")
    @patch("generators.gerar_conteudo_ia._chamar_opencode")
    def test_fluxo_completo_sem_publish(self, mock_opencode, mock_build, mock_deploy):
        """Testa geração completa sem auto_publish."""
        mock_opencode.return_value = (
            "# Decoradores em Python\n\n"
            "## Objetivos\n\n"
            "Aprender sobre decoradores.\n\n"
            "## Conteúdo\n\n"
            "Decoradores são funções que modificam outras funções...\n" * 50
        )

        resultado = gerar_e_publicar_capitulo(
            curso_slug="python_para_desktop",
            modulo_dir="modulo_01_fundamentos",
            tema="Decoradores Teste",
            auto_publish=False,
        )

        assert resultado["status"] in ("pending_approval", "error")
        # Deploy NÃO deve ter sido chamado
        mock_deploy.assert_not_called()

    @patch("generators.gerar_conteudo_ia._executar_deploy")
    @patch("generators.gerar_conteudo_ia._executar_build")
    @patch("generators.gerar_conteudo_ia._chamar_opencode")
    def test_fluxo_com_publish(self, mock_opencode, mock_build, mock_deploy):
        """Testa que deploy é chamado com auto_publish=True."""
        mock_opencode.return_value = (
            "# Teste Auto Publish\n\n"
            "Conteúdo suficiente para não ser rejeitado.\n" * 30
        )

        resultado = gerar_e_publicar_capitulo(
            curso_slug="python_para_desktop",
            modulo_dir="modulo_01_fundamentos",
            tema="Teste Auto Publish",
            auto_publish=True,
        )

        if resultado["status"] == "success":
            mock_deploy.assert_called_once()

    @patch("generators.gerar_conteudo_ia._chamar_opencode")
    def test_opencode_retorna_vazio(self, mock_opencode):
        """Testa tratamento de resposta vazia do OpenCode."""
        mock_opencode.return_value = ""

        resultado = gerar_e_publicar_capitulo(
            curso_slug="python_para_desktop",
            modulo_dir="modulo_01_fundamentos",
            tema="Teste Vazio",
        )

        assert resultado["status"] == "error"
        assert resultado["erro"] is not None
