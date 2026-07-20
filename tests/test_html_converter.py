"""
Testes: converter/html_to_markdown.py

Verifica a conversão de HTML para Markdown compatível com MkDocs Material.
"""
from __future__ import annotations

import pytest

from converter.html_to_markdown import HtmlToMarkdown


class TestHtmlToMarkdown:
    """Testes para HtmlToMarkdown.converter_string()."""

    @pytest.fixture
    def conv(self, fm_temp) -> HtmlToMarkdown:
        """Conversor com FileManager apontando para tmp_path."""
        return HtmlToMarkdown(fm_temp)

    def test_h1_convertido(self, conv):
        html = "<h1>Título Principal</h1>"
        md = conv.converter_string(html)
        assert "# Título Principal" in md

    def test_h2_convertido(self, conv):
        html = "<h2>Subtítulo</h2>"
        md = conv.converter_string(html)
        assert "## Subtítulo" in md

    def test_h3_convertido(self, conv):
        html = "<h3>Seção</h3>"
        md = conv.converter_string(html)
        assert "### Seção" in md

    def test_paragrafo_convertido(self, conv):
        html = "<p>Texto de parágrafo aqui.</p>"
        md = conv.converter_string(html)
        assert "Texto de parágrafo aqui." in md

    def test_lista_nao_ordenada(self, conv):
        html = "<ul><li>Item 1</li><li>Item 2</li></ul>"
        md = conv.converter_string(html)
        assert "- Item 1" in md
        assert "- Item 2" in md

    def test_lista_ordenada(self, conv):
        html = "<ol><li>Primeiro</li><li>Segundo</li></ol>"
        md = conv.converter_string(html)
        assert "1. Primeiro" in md
        assert "2. Segundo" in md

    def test_negrito(self, conv):
        html = "<p><strong>Negrito</strong></p>"
        md = conv.converter_string(html)
        assert "**Negrito**" in md

    def test_italico(self, conv):
        html = "<p><em>Itálico</em></p>"
        md = conv.converter_string(html)
        assert "*Itálico*" in md

    def test_codigo_inline(self, conv):
        html = "<p>Use <code>print()</code> para exibir.</p>"
        md = conv.converter_string(html)
        assert "`print()`" in md

    def test_bloco_codigo(self, conv):
        html = "<pre><code>x = 1\nprint(x)</code></pre>"
        md = conv.converter_string(html)
        assert "```" in md
        assert "x = 1" in md

    def test_link(self, conv):
        html = '<p><a href="https://python.org">Python</a></p>'
        md = conv.converter_string(html)
        assert "[Python](https://python.org)" in md

    def test_imagem(self, conv):
        html = '<img src="foto.png" alt="Descrição">'
        md = conv.converter_string(html)
        assert "![Descrição](foto.png)" in md

    def test_tabela(self, conv):
        html = """
        <table>
            <tr><th>Col1</th><th>Col2</th></tr>
            <tr><td>A</td><td>B</td></tr>
        </table>
        """
        md = conv.converter_string(html)
        assert "| Col1 |" in md
        assert "| --- |" in md
        assert "| A |" in md

    def test_admonition_warning(self, conv):
        html = '<div class="warning"><p>Cuidado!</p></div>'
        md = conv.converter_string(html)
        assert "!!! warning" in md

    def test_admonition_note(self, conv):
        html = '<div class="note"><p>Importante.</p></div>'
        md = conv.converter_string(html)
        assert "!!! note" in md

    def test_script_removido(self, conv):
        html = "<script>alert('xss')</script><p>Texto</p>"
        md = conv.converter_string(html)
        assert "alert" not in md
        assert "Texto" in md

    def test_style_removido(self, conv):
        html = "<style>body { color: red; }</style><p>Visível</p>"
        md = conv.converter_string(html)
        assert "color: red" not in md
        assert "Visível" in md

    def test_output_sem_linhas_em_branco_excessivas(self, conv):
        html = "<p>A</p><p>B</p><p>C</p>"
        md = conv.converter_string(html)
        # Máximo de 2 linhas em branco consecutivas
        assert "\n\n\n" not in md

    def test_string_vazia(self, conv):
        md = conv.converter_string("")
        assert isinstance(md, str)

    def test_html_complexo_retorna_string(self, conv):
        html = """
        <html><body>
            <h1>Título</h1>
            <p>Parágrafo com <strong>negrito</strong> e <em>itálico</em>.</p>
            <ul><li>Item A</li><li>Item B</li></ul>
        </body></html>
        """
        md = conv.converter_string(html)
        assert isinstance(md, str)
        assert "# Título" in md
        assert "**negrito**" in md
