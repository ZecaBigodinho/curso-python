"""
CourseForge — utils/config_loader.py

Carregamento e validação do arquivo config.yaml.

Por que não usar yaml.safe_load diretamente em main.py?
    Sem validação, qualquer campo faltando no config.yaml gera um KeyError
    em um lugar aleatório da aplicação, muito depois do carregamento.
    Aqui detectamos problemas NA FONTE e fornecemos mensagens claras.

Estratégia:
    1. Carregar o YAML
    2. Aplicar defaults para campos opcionais
    3. Validar campos obrigatórios
    4. Retornar configuração normalizada e segura
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from utils.logger import get_logger

logger = get_logger(__name__)


# ------------------------------------------------------------------ #
# Valores padrão da configuração                                      #
# ------------------------------------------------------------------ #

_DEFAULTS: dict[str, Any] = {
    "plataforma": {
        "nome": "CourseForge",
        "versao": "1.0.0",
        "autor_padrao": "Professor",
        "idioma": "pt-BR",
    },
    "diretorios": {
        "cursos": "cursos",
        "mkdocs_output": "mkdocs",
        "templates": "templates",
        "prompts": "prompts",
    },
    "mkdocs": {
        "site_name": "CourseForge Docs",
        "site_description": "Plataforma de Cursos",
        "site_author": "Professor",
        "theme": {
            "name": "material",
            "language": "pt",
        },
    },
    "numeracao": {
        "modulos": True,
        "capitulos": True,
        "formato_modulo": "modulo_{:02d}",
        "formato_capitulo": "{:02d}_{slug}",
    },
    "prompt": {
        "ia_padrao": "DeepSeek",
        "idioma_saida": "pt-BR",
        "nivel_padrao": "intermediário",
        "palavras_minimas": 1500,
    },
}


class ConfigLoader:
    """
    Responsável por carregar, validar e fornecer configurações da plataforma.

    Garante que campos obrigatórios existam e aplica defaults
    para campos opcionais ausentes.
    """

    def __init__(self, config_path: Path):
        """
        Args:
            config_path: Caminho absoluto para o config.yaml.

        Raises:
            FileNotFoundError: Se o arquivo não existir.
            ValueError: Se o arquivo estiver malformado ou inválido.
        """
        self._path = config_path
        self._config: dict[str, Any] = {}
        self._carregar()

    # ------------------------------------------------------------------ #
    # Carregamento                                                         #
    # ------------------------------------------------------------------ #

    def _carregar(self) -> None:
        """Carrega o YAML e aplica defaults."""
        if not self._path.exists():
            logger.error("config.yaml não encontrado: %s", self._path)
            raise FileNotFoundError(
                f"Arquivo de configuração não encontrado: {self._path}\n"
                "Certifique-se de que o arquivo config/config.yaml existe."
            )

        try:
            with self._path.open("r", encoding="utf-8") as f:
                carregado = yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            logger.error("Erro ao parsear config.yaml: %s", e)
            raise ValueError(f"Arquivo config.yaml inválido: {e}") from e

        # Mesclar com defaults (deep merge)
        self._config = self._merge(dict(_DEFAULTS), carregado)
        logger.info("Configuração carregada de: %s", self._path)

    # ------------------------------------------------------------------ #
    # Acesso                                                              #
    # ------------------------------------------------------------------ #

    def get(self, *chaves: str, default: Any = None) -> Any:
        """
        Acessa um valor aninhado no config via sequência de chaves.

        Args:
            *chaves: Sequência de chaves para navegação aninhada.
            default: Valor retornado se o caminho não existir.

        Returns:
            Valor encontrado ou default.

        Example:
            >>> loader.get("plataforma", "versao")
            '1.0.0'
        """
        atual = self._config
        for chave in chaves:
            if not isinstance(atual, dict):
                return default
            atual = atual.get(chave, default)
            if atual is default:
                return default
        return atual

    @property
    def plataforma(self) -> dict:
        """Seção 'plataforma' do config."""
        return self._config.get("plataforma", {})

    @property
    def mkdocs(self) -> dict:
        """Seção 'mkdocs' do config."""
        return self._config.get("mkdocs", {})

    @property
    def diretorios(self) -> dict:
        """Seção 'diretorios' do config."""
        return self._config.get("diretorios", {})

    @property
    def prompt(self) -> dict:
        """Seção 'prompt' do config."""
        return self._config.get("prompt", {})

    def as_dict(self) -> dict:
        """Retorna a configuração completa como dicionário."""
        return dict(self._config)

    # ------------------------------------------------------------------ #
    # Utilitários                                                          #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _merge(base: dict, override: dict) -> dict:
        """
        Deep merge de dois dicionários.
        Valores de `override` sobrescrevem `base` recursivamente.
        """
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                ConfigLoader._merge(base[key], value)
            else:
                base[key] = value
        return base
