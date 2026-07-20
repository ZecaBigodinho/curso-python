"""
CourseForge — utils/logger.py

Configuração centralizada do sistema de logging.

Por que logging e não só UI.erro()?
    UI.erro() é para o USUÁRIO — exibe mensagem amigável no terminal.
    logging é para o DESENVOLVEDOR — registra detalhes técnicos para diagnóstico.

    Exemplos de uso adequado:
        UI.erro("Arquivo já existe.")          → usuário vê no terminal
        logger.warning("FileExistsError: %s", path)  → desenvolvedor vê no log

    Princípio: nunca suprima informação técnica para agradar a UI.

Configuração:
    - Nível padrão: INFO em produção, DEBUG via variável de ambiente COURSEFORGE_DEBUG=1
    - Output: arquivo courseforge.log na raiz + console (apenas WARNING+)
    - Formato: timestamp + módulo + nível + mensagem
"""
from __future__ import annotations

import logging
import os
from pathlib import Path


# Nome do arquivo de log
LOG_FILENAME = "courseforge.log"

# Formato das mensagens
LOG_FORMAT = "%(asctime)s | %(name)-30s | %(levelname)-8s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def configurar_logging(root: Path, debug: bool | None = None) -> None:
    """
    Configura o sistema de logging da plataforma.

    Deve ser chamado UMA VEZ no início da aplicação (em main.py).

    Args:
        root: Diretório raiz do projeto (onde o log será salvo).
        debug: Se True, ativa nível DEBUG. Se None, detecta via
               variável de ambiente COURSEFORGE_DEBUG.
    """
    if debug is None:
        debug = os.environ.get("COURSEFORGE_DEBUG", "").lower() in ("1", "true", "yes")

    nivel = logging.DEBUG if debug else logging.INFO

    # Logger raiz da plataforma — todos os subloggers herdam dele
    logger_raiz = logging.getLogger("courseforge")
    logger_raiz.setLevel(nivel)

    # Evitar handlers duplicados se chamado mais de uma vez
    if logger_raiz.handlers:
        return

    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    # Handler 1: arquivo com rotação simples
    log_path = root / LOG_FILENAME
    try:
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setLevel(nivel)
        file_handler.setFormatter(formatter)
        logger_raiz.addHandler(file_handler)
    except (OSError, PermissionError) as e:
        # Se não conseguir escrever o log, avisar mas não travar a aplicação
        print(f"[AVISO] Não foi possível criar arquivo de log: {e}")

    # Handler 2: console apenas para WARNING+ (não poluir output do usuário)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)
    logger_raiz.addHandler(console_handler)


def get_logger(nome: str) -> logging.Logger:
    """
    Retorna logger filho com o nome do módulo solicitante.

    Uso em cada módulo:
        from utils.logger import get_logger
        logger = get_logger(__name__)

    Args:
        nome: Nome do módulo (__name__ recomendado).

    Returns:
        Logger configurado sob a hierarquia 'courseforge.*'.
    """
    # Garante que o logger fique sob a hierarquia courseforge
    if not nome.startswith("courseforge"):
        nome = f"courseforge.{nome}"
    return logging.getLogger(nome)
