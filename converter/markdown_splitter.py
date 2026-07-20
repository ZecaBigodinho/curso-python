"""
CourseForge — MarkdownSplitter
Divide um HTML grande em múltiplos arquivos Markdown.

Estratégia:
  1. Parsear HTML com BeautifulSoup
  2. Detectar pontos de divisão por H1 / H2
  3. Dividir o conteúdo em seções
  4. Converter cada seção com HtmlToMarkdown
  5. Salvar cada seção como arquivo numerado

Exemplo:
  python_avancado.html
    → 01_introducao.md
    → 02_funcoes.md
    → 03_classes.md
    → 04_arquivos.md
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

from bs4 import BeautifulSoup, Tag

from converter.html_to_markdown import HtmlToMarkdown
from utils.file_manager import FileManager
from utils.cli_ui import UI


def _slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[àáâãäå]", "a", text)
    text = re.sub(r"[èéêë]", "e", text)
    text = re.sub(r"[ìíîï]", "i", text)
    text = re.sub(r"[òóôõö]", "o", text)
    text = re.sub(r"[ùúûü]", "u", text)
    text = re.sub(r"[ç]", "c", text)
    text = re.sub(r"[^a-z0-9\s_-]", "", text)
    text = re.sub(r"[\s]+", "_", text)
    return text[:50]  # Limitar tamanho


class MarkdownSplitter:
    """
    Divide um arquivo HTML grande em múltiplos arquivos Markdown.

    Usa as tags H1 e H2 como pontos de divisão naturais.
    Cada seção se torna um capítulo separado.
    """

    def __init__(self, fm: FileManager):
        self.fm = fm
        self.conversor = HtmlToMarkdown(fm)

    # ------------------------------------------------------------------ #
    # Interface pública                                                    #
    # ------------------------------------------------------------------ #

    def dividir_interativo(self) -> list[Path]:
        """Interface CLI para divisão de arquivo HTML."""
        UI.secao("DIVIDIR HTML EM CAPÍTULOS MARKDOWN")

        html_path = UI.perguntar("Caminho do arquivo HTML")
        if not Path(html_path).exists():
            UI.erro(f"Arquivo não encontrado: {html_path}")
            return []

        tag_divisao = UI.selecionar(
            "Dividir por qual tag?",
            ["h1 (divisões maiores)", "h2 (divisões menores)", "h1 e h2 (todos)"]
        )

        tags = []
        if "h1" in tag_divisao:
            tags.append("h1")
        if "h2" in tag_divisao:
            tags.append("h2")

        prefixo = UI.perguntar("Prefixo dos arquivos (ex: 06)", padrao="01")
        output_dir_nome = UI.perguntar("Diretório de saída (relativo à raiz)", padrao="convertidos")

        html = Path(html_path).read_text(encoding="utf-8", errors="replace")
        secoes = self.dividir(html, tags=tags)

        output_dir = self.fm.path(output_dir_nome)
        self.fm.criar_diretorio(output_dir)

        paths_gerados = []
        for i, (titulo, conteudo_html) in enumerate(secoes):
            numero = int(prefixo) + i
            slug = _slugify(titulo)
            filename = f"{numero:02d}_{slug}.md"
            output_path = output_dir / filename

            markdown = self.conversor.converter_string(conteudo_html)
            self.fm.escrever(output_path, markdown, sobrescrever=True)
            paths_gerados.append(output_path)
            UI.muted(f"  ✔ {filename}  ← {titulo[:60]}")

        UI.sucesso(f"{len(paths_gerados)} arquivo(s) gerado(s) em '{output_dir_nome}/'")
        return paths_gerados

    def dividir(self, html: str, tags: list[str] = None) -> list[tuple[str, str]]:
        """
        Divide HTML em seções com base nas tags de título.

        Args:
            html: String HTML de entrada.
            tags: Lista de tags para usar como divisores (ex: ['h1', 'h2']).

        Returns:
            Lista de tuplas (titulo, html_da_secao).
        """
        if tags is None:
            tags = ["h1", "h2"]

        soup = BeautifulSoup(html, "html.parser")
        body = soup.find("body") or soup

        secoes: list[tuple[str, str]] = []
        titulo_atual = "Introdução"
        elementos_atuais: list[Tag] = []

        for elemento in body.children:
            if not isinstance(elemento, Tag):
                continue

            if elemento.name and elemento.name.lower() in tags:
                # Salvar seção anterior
                if elementos_atuais:
                    html_secao = self._elementos_para_html(elementos_atuais)
                    secoes.append((titulo_atual, html_secao))
                    elementos_atuais = []

                titulo_atual = elemento.get_text(strip=True) or "Sem Título"
                elementos_atuais.append(elemento)
            else:
                elementos_atuais.append(elemento)

        # Salvar última seção
        if elementos_atuais:
            html_secao = self._elementos_para_html(elementos_atuais)
            secoes.append((titulo_atual, html_secao))

        # Filtrar seções vazias
        secoes = [(t, h) for t, h in secoes if h.strip()]

        return secoes

    # ------------------------------------------------------------------ #
    # Helpers                                                              #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _elementos_para_html(elementos: list[Tag]) -> str:
        """Converte lista de elementos BeautifulSoup de volta para HTML."""
        return "".join(str(e) for e in elementos)
