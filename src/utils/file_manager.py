"""
CourseForge — utils/file_manager.py

Responsável por TODAS as operações de I/O da plataforma.
Nenhum outro módulo deve abrir arquivos diretamente.

Responsabilidades:
    - Criar e listar diretórios
    - Ler e escrever arquivos de texto (Markdown)
    - Ler e escrever arquivos YAML
    - Gerenciar metadados de cursos (.courseforge.yaml)

Por que centralizar aqui?
    Se no futuro quisermos salvar em S3, banco de dados, ou cache,
    mudamos APENAS este arquivo. O resto do código não sabe onde
    os dados estão armazenados.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import yaml

from utils.constants import METADATA_FILENAME
from utils.logger import get_logger

logger = get_logger(__name__)


class FileManager:
    """
    Gerenciador central de I/O da plataforma CourseForge.

    Todas as operações de leitura e escrita passam por esta classe.
    """

    def __init__(self, root: Path) -> None:
        """
        Args:
            root: Diretório raiz do projeto CourseForge.
        """
        self.root = root.resolve()

    # ------------------------------------------------------------------ #
    # Diretórios                                                           #
    # ------------------------------------------------------------------ #

    def criar_diretorio(self, caminho: Path | str) -> Path:
        """
        Cria um diretório (e todos os pais necessários) se não existir.

        Args:
            caminho: Caminho do diretório a criar.

        Returns:
            Path absoluto do diretório criado/existente.
        """
        path = self._resolve(caminho)
        path.mkdir(parents=True, exist_ok=True)
        logger.debug("Diretório garantido: %s", path)
        return path

    def listar_subdiretorios(self, caminho: Path | str) -> list[Path]:
        """
        Lista subdiretórios imediatos de um caminho, ordenados por nome.

        Args:
            caminho: Diretório pai.

        Returns:
            Lista ordenada de Paths de subdiretórios. Vazia se não existir.
        """
        path = self._resolve(caminho)
        if not path.exists():
            return []
        return sorted([p for p in path.iterdir() if p.is_dir()])

    def listar_arquivos(self, caminho: Path | str, extensao: str = "*") -> list[Path]:
        """
        Lista arquivos em um diretório com extensão opcional.

        Args:
            caminho: Diretório a listar.
            extensao: Extensão sem ponto (ex: 'md', 'txt'). '*' lista todos.

        Returns:
            Lista ordenada de Paths de arquivos.
        """
        path = self._resolve(caminho)
        if not path.exists():
            return []
        return sorted(path.glob(f"*.{extensao.lstrip('.')}"))

    # ------------------------------------------------------------------ #
    # Arquivos de texto                                                    #
    # ------------------------------------------------------------------ #

    def escrever(
        self,
        caminho: Path | str,
        conteudo: str,
        sobrescrever: bool = False,
    ) -> Path:
        """
        Escreve conteúdo em arquivo de texto (UTF-8).

        Args:
            caminho: Caminho do arquivo.
            conteudo: Conteúdo a escrever.
            sobrescrever: Se False, levanta FileExistsError se já existir.

        Returns:
            Path absoluto do arquivo escrito.

        Raises:
            FileExistsError: Se arquivo existir e sobrescrever=False.
        """
        path = self._resolve(caminho)
        path.parent.mkdir(parents=True, exist_ok=True)

        if path.exists() and not sobrescrever:
            raise FileExistsError(f"Arquivo já existe: {path}")

        path.write_text(conteudo, encoding="utf-8")
        logger.debug("Arquivo escrito: %s (%d chars)", path, len(conteudo))
        return path

    def ler(self, caminho: Path | str) -> str:
        """
        Lê e retorna o conteúdo de um arquivo de texto.

        Args:
            caminho: Caminho do arquivo.

        Returns:
            Conteúdo como string.

        Raises:
            FileNotFoundError: Se o arquivo não existir.
        """
        path = self._resolve(caminho)
        if not path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {path}")
        return path.read_text(encoding="utf-8")

    def existe(self, caminho: Path | str) -> bool:
        """Verifica se um arquivo ou diretório existe."""
        return self._resolve(caminho).exists()

    # ------------------------------------------------------------------ #
    # YAML                                                                 #
    # ------------------------------------------------------------------ #

    def ler_yaml(self, caminho: Path | str) -> dict:
        """
        Lê e retorna o conteúdo de um arquivo YAML como dicionário.

        Args:
            caminho: Caminho do arquivo YAML.

        Returns:
            Dicionário com o conteúdo. Vazio se o arquivo for vazio.

        Raises:
            FileNotFoundError: Se o arquivo não existir.
            ValueError: Se o YAML for inválido.
        """
        path = self._resolve(caminho)
        if not path.exists():
            raise FileNotFoundError(f"Arquivo YAML não encontrado: {path}")
        try:
            with path.open("r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            raise ValueError(f"YAML inválido em {path}: {e}") from e

    def escrever_yaml(
        self,
        caminho: Path | str,
        dados: dict,
        sobrescrever: bool = True,
    ) -> Path:
        """
        Serializa um dicionário para arquivo YAML.

        Args:
            caminho: Caminho do arquivo.
            dados: Dicionário a serializar.
            sobrescrever: Se False, levanta FileExistsError se já existir.

        Returns:
            Path do arquivo escrito.
        """
        path = self._resolve(caminho)
        path.parent.mkdir(parents=True, exist_ok=True)

        if path.exists() and not sobrescrever:
            raise FileExistsError(f"Arquivo já existe: {path}")

        with path.open("w", encoding="utf-8") as f:
            yaml.dump(dados, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

        logger.debug("YAML escrito: %s", path)
        return path

    # ------------------------------------------------------------------ #
    # Metadados de curso                                                   #
    # ------------------------------------------------------------------ #

    def salvar_metadados_curso(self, curso_dir: Path, dados: dict) -> Path:
        """
        Salva os metadados de um curso em .courseforge.yaml.

        Args:
            curso_dir: Diretório raiz do curso.
            dados: Dicionário de metadados (geralmente Course.to_dict()).

        Returns:
            Path do arquivo de metadados.
        """
        return self.escrever_yaml(
            curso_dir / METADATA_FILENAME,
            dados,
            sobrescrever=True,
        )

    def ler_metadados_curso(self, curso_dir: Path) -> dict:
        """
        Lê metadados de um curso.

        Args:
            curso_dir: Diretório raiz do curso.

        Returns:
            Dicionário com metadados, ou {} se não existir.
        """
        meta_path = curso_dir / METADATA_FILENAME
        if not meta_path.exists():
            logger.debug("Metadados não encontrados em: %s", curso_dir)
            return {}
        return self.ler_yaml(meta_path)

    # ------------------------------------------------------------------ #
    # Helpers                                                              #
    # ------------------------------------------------------------------ #

    def _resolve(self, caminho: Path | str) -> Path:
        """
        Resolve caminho: se absoluto, usa direto; se relativo, une com root.

        Args:
            caminho: Path ou string absoluta ou relativa.

        Returns:
            Path absoluto.
        """
        p = Path(caminho)
        return p if p.is_absolute() else self.root / p

    def path(self, *partes: str) -> Path:
        """
        Constrói um path dentro da root do projeto.

        Args:
            *partes: Partes do caminho relativo.

        Returns:
            Path absoluto dentro da root.
        """
        return self.root.joinpath(*partes)
