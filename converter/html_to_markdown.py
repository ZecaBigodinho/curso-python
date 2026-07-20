"""
CourseForge — HtmlToMarkdown
Conversor completo de HTML para Markdown compatível com MkDocs Material.

Converte:
  <h1>     → # Título
  <h2>     → ## Título
  <h3>     → ### Título
  <ul>     → lista com -
  <ol>     → lista numerada
  <table>  → tabela Markdown
  <pre>    → bloco ```python
  <code>   → `código inline`
  <div class="warning"> → !!! warning
  <div class="note">    → !!! note
  <div class="tip">     → !!! tip
  <strong> → **negrito**
  <em>     → *itálico*
  <a>      → [texto](url)
  <img>    → ![alt](src)

Estratégia:
  1. BeautifulSoup para parsing seguro do HTML
  2. Conversão por tipo de tag com tratamento de borda
  3. Limpeza pós-conversão (espaços extras, linhas em branco)
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

from bs4 import BeautifulSoup, Tag, NavigableString

from utils.file_manager import FileManager
from utils.cli_ui import UI
from utils.logger import get_logger

logger = get_logger(__name__)


# Mapeamento de classes de div para admonitions MkDocs
_DIV_CLASS_MAP = {
    "warning": "warning",
    "note": "note",
    "tip": "tip",
    "info": "info",
    "danger": "danger",
    "success": "success",
}


class HtmlToMarkdown:
    """
    Conversor de HTML para Markdown MkDocs Material.

    Uso:
        converter = HtmlToMarkdown(file_manager)
        md = converter.converter_arquivo("input.html")
        converter.salvar("output.md", md)
    """

    def __init__(self, fm: FileManager):
        self.fm = fm

    # ------------------------------------------------------------------ #
    # Interface pública                                                    #
    # ------------------------------------------------------------------ #

    def converter_interativo(self) -> Optional[Path]:
        """Interface CLI para conversão de arquivo HTML."""
        UI.secao("CONVERTER HTML → MARKDOWN")

        html_path = UI.perguntar("Caminho do arquivo HTML")
        if not Path(html_path).exists():
            UI.erro(f"Arquivo não encontrado: {html_path}")
            return None

        output_nome = UI.perguntar("Nome do arquivo de saída (ex: 06_json.md)")

        html = Path(html_path).read_text(encoding="utf-8", errors="replace")
        markdown = self.converter_string(html)

        # Salvar na pasta convertidos/
        output_dir = self.fm.path("convertidos")
        self.fm.criar_diretorio(output_dir)
        output_path = output_dir / output_nome

        self.fm.escrever(output_path, markdown, sobrescrever=True)
        UI.sucesso(f"Arquivo convertido: {output_path.relative_to(self.fm.root)}")
        UI.muted(f"  Tamanho: {len(markdown)} caracteres")
        return output_path

    def converter_arquivo(self, html_path: Path | str) -> str:
        """Converte arquivo HTML e retorna string Markdown."""
        html = Path(html_path).read_text(encoding="utf-8", errors="replace")
        return self.converter_string(html)

    def converter_string(self, html: str) -> str:
        """
        Converte string HTML para Markdown.

        Args:
            html: String HTML de entrada.

        Returns:
            String Markdown de saída.
        """
        soup = BeautifulSoup(html, "html.parser")

        # Remover scripts, styles e elementos indesejados
        for tag in soup(["script", "style", "head", "meta", "link"]):
            tag.decompose()

        # Processar body ou raiz
        body = soup.find("body") or soup
        linhas = self._processar_elemento(body)

        markdown = "\n".join(linhas)
        markdown = self._limpar(markdown)
        return markdown

    # ------------------------------------------------------------------ #
    # Processamento recursivo                                              #
    # ------------------------------------------------------------------ #

    def _processar_elemento(self, elemento, nivel_lista: int = 0) -> list[str]:
        """
        Processa recursivamente um elemento BeautifulSoup.

        Args:
            elemento: Tag ou NavigableString a processar.
            nivel_lista: Nível de aninhamento de listas.

        Returns:
            Lista de linhas Markdown.
        """
        linhas: list[str] = []

        for filho in elemento.children:
            if isinstance(filho, NavigableString):
                texto = filho.strip()
                if texto:
                    linhas.append(texto)
                continue

            if not isinstance(filho, Tag):
                continue

            tag = filho.name.lower() if filho.name else ""

            # Headings
            if tag == "h1":
                linhas.extend(["", f"# {self._texto(filho)}", ""])
            elif tag == "h2":
                linhas.extend(["", f"## {self._texto(filho)}", ""])
            elif tag == "h3":
                linhas.extend(["", f"### {self._texto(filho)}", ""])
            elif tag == "h4":
                linhas.extend(["", f"#### {self._texto(filho)}", ""])
            elif tag == "h5":
                linhas.extend(["", f"##### {self._texto(filho)}", ""])

            # Parágrafos e blocos
            elif tag == "p":
                texto = self._processar_inline(filho)
                if texto.strip():
                    linhas.extend(["", texto, ""])

            # Listas
            elif tag == "ul":
                linhas.extend(self._processar_lista(filho, ordenada=False, nivel=nivel_lista))
            elif tag == "ol":
                linhas.extend(self._processar_lista(filho, ordenada=True, nivel=nivel_lista))

            # Código
            elif tag == "pre":
                linhas.extend(self._processar_pre(filho))
            elif tag == "code" and filho.parent and filho.parent.name != "pre":
                linhas.append(f"`{self._texto(filho)}`")

            # Tabelas
            elif tag == "table":
                linhas.extend(self._processar_tabela(filho))

            # Divs com classes especiais (admonitions)
            elif tag == "div":
                classes = filho.get("class", [])
                admonition = None
                for cls in classes:
                    if cls in _DIV_CLASS_MAP:
                        admonition = _DIV_CLASS_MAP[cls]
                        break

                if admonition:
                    linhas.extend(self._processar_admonition(filho, admonition))
                else:
                    linhas.extend(self._processar_elemento(filho, nivel_lista))

            # Formatação inline em bloco
            elif tag == "blockquote":
                conteudo = self._processar_elemento(filho, nivel_lista)
                for linha in conteudo:
                    if linha.strip():
                        linhas.append(f"> {linha}")
                    else:
                        linhas.append(">")

            # Links e imagens
            elif tag == "a":
                href = filho.get("href", "#")
                texto = self._texto(filho)
                linhas.append(f"[{texto}]({href})")
            elif tag == "img":
                src = filho.get("src", "")
                alt = filho.get("alt", "imagem")
                linhas.append(f"![{alt}]({src})")

            # Separador
            elif tag == "hr":
                linhas.extend(["", "---", ""])

            # Quebra de linha
            elif tag == "br":
                linhas.append("")

            # Elementos a ignorar (processar filhos)
            elif tag in ("section", "article", "main", "header", "footer",
                         "nav", "aside", "figure", "figcaption", "span"):
                linhas.extend(self._processar_elemento(filho, nivel_lista))

            # Qualquer outro elemento — tentar extrair texto
            else:
                sub = self._processar_elemento(filho, nivel_lista)
                linhas.extend(sub)

        return linhas

    # ------------------------------------------------------------------ #
    # Processamento específico por tipo                                    #
    # ------------------------------------------------------------------ #

    def _processar_inline(self, elemento: Tag) -> str:
        """Processa formatação inline (strong, em, code, a) dentro de um parágrafo."""
        resultado = ""
        for filho in elemento.children:
            if isinstance(filho, NavigableString):
                resultado += str(filho)
            elif isinstance(filho, Tag):
                tag = filho.name.lower() if filho.name else ""
                if tag in ("strong", "b"):
                    resultado += f"**{self._texto(filho)}**"
                elif tag in ("em", "i"):
                    resultado += f"*{self._texto(filho)}*"
                elif tag == "code":
                    resultado += f"`{self._texto(filho)}`"
                elif tag == "a":
                    href = filho.get("href", "#")
                    resultado += f"[{self._texto(filho)}]({href})"
                elif tag == "br":
                    resultado += "  \n"
                else:
                    resultado += self._processar_inline(filho)
        return resultado.strip()

    def _processar_lista(self, elemento: Tag, ordenada: bool, nivel: int = 0) -> list[str]:
        """Converte ul/ol para lista Markdown com suporte a aninhamento."""
        linhas = [""]
        indent = "    " * nivel
        contador = 1

        for li in elemento.find_all("li", recursive=False):
            # Verificar se há sub-lista
            sublista_ul = li.find("ul", recursive=False)
            sublista_ol = li.find("ol", recursive=False)

            # Texto do item (sem a sub-lista)
            if sublista_ul or sublista_ol:
                sublista = sublista_ul or sublista_ol
                sublista.extract()

            texto_li = self._processar_inline(li).strip() or self._texto(li).strip()

            if ordenada:
                linhas.append(f"{indent}{contador}. {texto_li}")
                contador += 1
            else:
                linhas.append(f"{indent}- {texto_li}")

            # Sub-listas
            if sublista_ul:
                linhas.extend(self._processar_lista(sublista_ul, False, nivel + 1))
            if sublista_ol:
                linhas.extend(self._processar_lista(sublista_ol, True, nivel + 1))

        linhas.append("")
        return linhas

    def _processar_pre(self, elemento: Tag) -> list[str]:
        """Converte <pre> / <pre><code> para bloco de código Markdown."""
        code_tag = elemento.find("code")
        codigo = code_tag.get_text() if code_tag else elemento.get_text()

        # Detectar linguagem pela classe
        linguagem = "python"
        classes = []
        if code_tag:
            classes = code_tag.get("class", [])
        elif elemento:
            classes = elemento.get("class", [])

        for cls in (classes or []):
            if cls.startswith("language-") or cls.startswith("lang-"):
                linguagem = cls.split("-", 1)[1]
                break
            if cls in ("python", "bash", "sql", "json", "yaml", "html", "css", "js", "javascript"):
                linguagem = cls
                break

        return ["", f"```{linguagem}", codigo.rstrip(), "```", ""]

    def _processar_tabela(self, elemento: Tag) -> list[str]:
        """Converte <table> para tabela Markdown."""
        linhas = [""]
        cabecalho_feito = False

        for tr in elemento.find_all("tr"):
            celulas = tr.find_all(["th", "td"])
            if not celulas:
                continue

            linha = "| " + " | ".join(self._texto(c) for c in celulas) + " |"
            linhas.append(linha)

            if not cabecalho_feito:
                separador = "| " + " | ".join("---" for _ in celulas) + " |"
                linhas.append(separador)
                cabecalho_feito = True

        linhas.append("")
        return linhas

    def _processar_admonition(self, elemento: Tag, tipo: str) -> list[str]:
        """Converte <div class="warning"> em !!! warning MkDocs."""
        titulo = ""
        titulo_tag = elemento.find(["h1", "h2", "h3", "h4", "strong", "b"])
        if titulo_tag:
            titulo = f' "{self._texto(titulo_tag)}"'
            titulo_tag.decompose()

        linhas = ["", f"!!! {tipo}{titulo}"]

        # Indentar conteúdo com 4 espaços
        conteudo_linhas = self._processar_elemento(elemento)
        for linha in conteudo_linhas:
            if linha.strip():
                linhas.append(f"    {linha}")
            else:
                linhas.append("")

        linhas.append("")
        return linhas

    # ------------------------------------------------------------------ #
    # Helpers                                                              #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _texto(elemento: Tag) -> str:
        """Extrai texto limpo de um elemento."""
        return elemento.get_text(separator=" ").strip()

    @staticmethod
    def _limpar(markdown: str) -> str:
        """Limpa linhas em branco excessivas e espaços desnecessários."""
        # Máximo de 2 linhas em branco consecutivas
        markdown = re.sub(r"\n{3,}", "\n\n", markdown)
        # Remover espaços no fim das linhas
        linhas = [linha.rstrip() for linha in markdown.splitlines()]
        return "\n".join(linhas).strip() + "\n"
