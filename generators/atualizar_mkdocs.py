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
            - Introdução ao Python:
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
        """Salva o mkdocs.yml usando FileManager (não yaml.dump direto)."""
        output_dir = self.fm.path(DIR_MKDOCS)
        self.fm.criar_diretorio(output_dir)
        output_path = output_dir / MKDOCS_FILENAME
        # Usa escrever_yaml do FileManager — única via de escrita YAML no projeto
        self.fm.escrever_yaml(output_path, cfg, sobrescrever=True)
        return output_path

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
