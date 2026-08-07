"""
CourseForge — generators/atualizar_mkdocs.py

Gerador automático do mkdocs.yml.
Nunca edite o mkdocs.yml manualmente — use esta classe.

Estratégia:
  - Percorre cursos/ → módulos/ → arquivos .md
  - Usa metadados .courseforge.yaml para nomes legíveis (em vez de converter slugs)
  - Monta estrutura nav: hierárquica
  - Escreve mkdocs.yml via FileManager (não diretamente)
"""
from __future__ import annotations

from pathlib import Path

from utils.file_manager import FileManager
from utils.cli_ui import UI
from utils.constants import (
    DIR_CURSOS, DIR_MKDOCS, MKDOCS_FILENAME, MODULE_DIR_PREFIX,
    CURSO_DOCS_SUBDIR,
)
from utils.logger import get_logger

logger = get_logger(__name__)


class MkDocsUpdater:
    """
    Gerador automático do mkdocs.yml.

    Responsabilidades:
    - Varrer estrutura de cursos/
    - Usar nomes legíveis dos metadados (não converter slugs)
    - Construir navegação hierárquica (curso → módulo → capítulo)
    - Gerar mkdocs.yml completo via FileManager
    """

    # Mapeamento de palavras-chave → ícone para módulos do sidebar.
    # Quando o nome do módulo contém uma dessas palavras, o ícone é prefixado.
    ICONES_MODULO: dict[str, str] = {
        "fundament": "🐍",
        "interface": "🖥️",
        "grafica": "🖥️",
        "banco": "🗄️",
        "dados": "🗄️",
        "web": "🌐",
        "api": "🔌",
        "teste": "🧪",
        "deploy": "🚀",
        "seguranca": "🔒",
        "avancad": "⚡",
        "projeto": "🏗️",
        "automacao": "🤖",
        "machine": "🧠",
        "ia": "🧠",
        "rede": "🌐",
        "git": "🔀",
    }

    def __init__(self, fm: FileManager, config_global: dict) -> None:
        """
        Args:
            fm: Gerenciador de arquivos da plataforma.
            config_global: Dicionário de configuração global (config.yaml).
        """
        self.fm = fm
        self.config = config_global

    # ------------------------------------------------------------------ #
    # Interface pública                                                    #
    # ------------------------------------------------------------------ #

    def atualizar(self, silencioso: bool = False) -> Path:
        """
        Gera ou atualiza o mkdocs.yml com base na estrutura atual de cursos/.

        Args:
            silencioso: Se True, suprime mensagens de status no terminal.
                        Use True quando chamado automaticamente após criar curso/módulo/capítulo.

        Returns:
            Path do mkdocs.yml gerado.
        """
        if not silencioso:
            UI.secao("ATUALIZAR MKDOCS.YML")

        nav = self._construir_nav()
        mkdocs_cfg = self._construir_config(nav)
        output_path = self._salvar(mkdocs_cfg)

        if not silencioso:
            cursos_count = len(nav) - 1  # descontar o Home
            UI.sucesso(f"mkdocs.yml atualizado: {output_path.relative_to(self.fm.root)}")
            UI.muted(f"  {cursos_count} curso(s) na navegação.")

        logger.info("mkdocs.yml gerado em: %s (%d cursos)", output_path, len(nav) - 1)
        return output_path

    # Mantido por compatibilidade retroativa — use atualizar(silencioso=True)
    def atualizar_silencioso(self) -> Path:
        """Alias para atualizar(silencioso=True). Mantido para retrocompatibilidade."""
        return self.atualizar(silencioso=True)

    # ------------------------------------------------------------------ #
    # Construção da navegação                                              #
    # ------------------------------------------------------------------ #

    def _construir_nav(self) -> list:
        """
        Constrói a estrutura nav: do MkDocs percorrendo cursos/.

        Usa metadados .courseforge.yaml para nomes legíveis.
        Formato resultante:
          - Home: index.md
          - Python para Iniciantes:
            - Índice: cursos/python_para_iniciantes/docs/index.md
            - 🐍 Introdução ao Python:
              - Visão Geral: .../index.md
              - Variáveis e Tipos: .../01_variaveis.md
        """
        nav: list = [{"Home": "index.md"}]

        cursos_dir = self.fm.path(DIR_CURSOS)
        for curso_dir in self.fm.listar_subdiretorios(cursos_dir):
            entrada_curso = self._construir_entrada_curso(curso_dir, cursos_dir)
            if entrada_curso:
                nav.append(entrada_curso)

        return nav

    def _construir_entrada_curso(self, curso_dir: Path, cursos_dir: Path) -> dict | None:
        """Constrói a entrada de navegação de um curso."""
        meta = self.fm.ler_metadados_curso(curso_dir)
        # Usa nome do metadata para exibição — não converte o slug
        curso_nome = meta.get("nome", curso_dir.name) if meta else curso_dir.name

        curso_entries: list = []

        # Índice do curso
        index_curso = curso_dir / CURSO_DOCS_SUBDIR / "index.md"
        if index_curso.exists():
            rel = index_curso.relative_to(cursos_dir).as_posix()
            curso_entries.append({"Índice": rel})

        # Módulos
        for modulo_dir in self.fm.listar_subdiretorios(curso_dir):
            if not modulo_dir.name.startswith(MODULE_DIR_PREFIX):
                continue
            entrada_modulo = self._construir_entrada_modulo(modulo_dir, cursos_dir)
            if entrada_modulo:
                curso_entries.append(entrada_modulo)

        if not curso_entries:
            return None

        return {curso_nome: curso_entries}

    def _construir_entrada_modulo(self, modulo_dir: Path, cursos_dir: Path) -> dict | None:
        """Constrói a entrada de navegação de um módulo."""
        # Nome legível: remove prefixo "modulo_01_" e humaniza
        nome_sem_numero = "_".join(modulo_dir.name.split("_")[2:])
        modulo_nome = nome_sem_numero.replace("_", " ").title() if nome_sem_numero else modulo_dir.name

        # Prefixar com ícone baseado em palavras-chave
        icone = self._resolver_icone_modulo(modulo_nome)
        if icone:
            modulo_nome = f"{icone} {modulo_nome}"

        modulo_entries: list = []

        # Índice do módulo
        index_mod = modulo_dir / "index.md"
        if index_mod.exists():
            rel = index_mod.relative_to(cursos_dir).as_posix()
            modulo_entries.append({"Visão Geral": rel})

        # Capítulos
        for cap in self.fm.listar_arquivos(modulo_dir, "md"):
            if cap.name == "index.md":
                continue
            cap_nome = self._nome_capitulo_legivel(cap.stem)
            rel = cap.relative_to(cursos_dir).as_posix()
            modulo_entries.append({cap_nome: rel})

        if not modulo_entries:
            return None

        return {modulo_nome: modulo_entries}

    # ------------------------------------------------------------------ #
    # Construção da configuração completa                                  #
    # ------------------------------------------------------------------ #

    def _construir_config(self, nav: list) -> dict:
        """Monta o dicionário completo do mkdocs.yml."""
        mkdocs_cfg = self.config.get("mkdocs", {}).copy()
        mkdocs_cfg["nav"] = nav
        mkdocs_cfg["docs_dir"] = "../cursos"
        return mkdocs_cfg

    # ------------------------------------------------------------------ #
    # Persistência via FileManager                                         #
    # ------------------------------------------------------------------ #

    def _salvar(self, cfg: dict) -> Path:
        """
        Salva o mkdocs.yml usando FileManager.

        Após a escrita YAML padrão, injeta a extensão pymdownx.emoji
        com tags !!python/name: que o yaml.dump não consegue serializar.
        """
        output_dir = self.fm.path(DIR_MKDOCS)
        self.fm.criar_diretorio(output_dir)
        output_path = output_dir / MKDOCS_FILENAME
        # Usa escrever_yaml do FileManager — única via de escrita YAML no projeto
        self.fm.escrever_yaml(output_path, cfg, sobrescrever=True)

        # Injetar pymdownx.emoji com tags !!python/name (incompatíveis com yaml.dump)
        self._injetar_emoji_extension(output_path)

        return output_path

    @staticmethod
    def _injetar_emoji_extension(path: Path) -> None:
        """
        Adiciona a extensão pymdownx.emoji ao mkdocs.yml após a serialização YAML.

        Os tags !!python/name: são necessários para o MkDocs Material mas não são
        suportados por yaml.safe_load/dump, então são injetados como texto raw.
        """
        emoji_block = (
            "- pymdownx.emoji:\n"
            "    emoji_index: !!python/name:material.extensions.emoji.twemoji\n"
            "    emoji_generator: !!python/name:material.extensions.emoji.to_svg\n"
        )

        content = path.read_text(encoding="utf-8")

        # Inserir antes da linha "- attr_list" nas markdown_extensions
        marker = "- attr_list"
        if marker in content and "pymdownx.emoji" not in content:
            # Detectar a indentação do marker
            for line in content.splitlines():
                if marker in line:
                    indent = line[: len(line) - len(line.lstrip())]
                    emoji_indented = "".join(
                        f"{indent}{ln}\n" if ln.strip() else "\n"
                        for ln in emoji_block.splitlines()
                    )
                    content = content.replace(
                        f"{indent}{marker}",
                        f"{emoji_indented}{indent}{marker}",
                    )
                    break

            path.write_text(content, encoding="utf-8")

    # ------------------------------------------------------------------ #
    # Helpers                                                              #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _nome_capitulo_legivel(stem: str) -> str:
        """
        Converte stem de capítulo para nome legível.
        Ex: '01_variaveis_e_tipos' → 'Variáveis e Tipos'
        Remove o número inicial e humaniza o slug.
        """
        partes = stem.split("_")
        # Pular o número inicial (ex: "01")
        if partes and partes[0].isdigit():
            partes = partes[1:]
        return " ".join(p.capitalize() for p in partes) if partes else stem

    @classmethod
    def _resolver_icone_modulo(cls, nome_modulo: str) -> str | None:
        """
        Resolve o ícone (emoji) para um módulo com base em palavras-chave.

        Busca match parcial (case-insensitive) no dicionário ICONES_MODULO.
        Retorna o primeiro ícone encontrado, ou None se nenhuma palavra-chave bater.

        Args:
            nome_modulo: Nome legível do módulo (ex: "Fundamentos").

        Returns:
            Emoji string ou None.
        """
        nome_lower = nome_modulo.lower()
        for palavra, icone in cls.ICONES_MODULO.items():
            if palavra in nome_lower:
                return icone
        return None
