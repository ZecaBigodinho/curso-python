"""
CourseForge — courseforge_watcher.py

Serviço de background que roda no PC Windows e consome jobs
pendentes da fila do Hermes na VPS Oracle.

Fluxo:
    1. A cada POLL_INTERVAL segundos, consulta GET /jobs/pending na VPS
    2. Se houver job pendente, chama gerar_e_publicar_capitulo() localmente
    3. Reporta o resultado via POST /jobs/{id}/concluido na VPS
    4. O Hermes então notifica no Telegram

Execução:
    - Direto: python courseforge_watcher.py
    - Como tarefa agendada: ver install_watcher.ps1

Configuração via .env:
    HERMES_API_URL    — URL base da API Hermes (Tailscale)
    HERMES_API_TOKEN  — Token de autenticação (opcional)
    WATCHER_POLL_INTERVAL — Intervalo de polling em segundos (default: 60)
"""
from __future__ import annotations

import json
import os
import signal
import sys
import time
import traceback
from pathlib import Path

# Garantir que a raiz do projeto está no path
PROJECT_ROOT = Path(__file__).parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

# Carregar .env antes de qualquer import que use os.environ
try:
    from dotenv import load_dotenv
    load_dotenv(PROJECT_ROOT / ".env")
except ImportError:
    pass

from utils.logger import configurar_logging, get_logger

# Configurar logging antes de tudo
configurar_logging(PROJECT_ROOT)
logger = get_logger("watcher")

# Importar requests aqui para dar mensagem clara se faltar
try:
    import requests
except ImportError:
    logger.critical("Módulo 'requests' não encontrado. Instale: pip install requests")
    print("[ERRO] Módulo 'requests' não encontrado. Instale: pip install requests",
          file=sys.stderr)
    sys.exit(1)

# Configuração
HERMES_API_URL = os.environ.get("HERMES_API_URL", "").rstrip("/")
HERMES_API_TOKEN = os.environ.get("HERMES_API_TOKEN", "")
POLL_INTERVAL = int(os.environ.get("WATCHER_POLL_INTERVAL", "60"))
MAX_BACKOFF = 300  # Máximo de 5 minutos entre retries

# Flag de shutdown
_running = True


def signal_handler(signum, frame):
    """Graceful shutdown via Ctrl+C ou sinal do Windows."""
    global _running
    logger.info("Recebido sinal de shutdown (signal=%d)", signum)
    _running = False


def get_headers() -> dict:
    """Retorna headers HTTP com autenticação, se configurada."""
    headers = {"Content-Type": "application/json"}
    if HERMES_API_TOKEN:
        headers["Authorization"] = f"Bearer {HERMES_API_TOKEN}"
    return headers


def fetch_pending_job() -> dict | None:
    """
    Consulta a VPS por um job pendente.

    Returns:
        Dict do job se houver, None caso contrário.

    Raises:
        requests.RequestException: Se a VPS não responder.
    """
    url = f"{HERMES_API_URL}/jobs/pending"
    logger.debug("Consultando: %s", url)

    resp = requests.get(url, headers=get_headers(), timeout=10)

    if resp.status_code == 204:
        return None  # Sem jobs pendentes

    if resp.status_code == 200:
        data = resp.json()
        return data.get("job")

    logger.warning("Resposta inesperada da API: %d %s", resp.status_code, resp.text)
    return None


def report_result(job_id: int, resultado: dict, erro: str | None = None) -> bool:
    """
    Reporta o resultado de um job para a VPS.

    Args:
        job_id: ID do job.
        resultado: Dict de resultado do gerar_e_publicar_capitulo.
        erro: Mensagem de erro, se houver.

    Returns:
        True se o report foi aceito pela VPS.
    """
    url = f"{HERMES_API_URL}/jobs/{job_id}/concluido"

    payload = {
        "status": "error" if erro else "completed",
        "resultado": resultado,
        "erro": erro or "",
    }

    try:
        resp = requests.post(
            url,
            headers=get_headers(),
            json=payload,
            timeout=10,
        )
        if resp.status_code == 200:
            logger.info("Resultado reportado para job #%d", job_id)
            return True
        else:
            logger.warning("Falha ao reportar job #%d: %d %s",
                           job_id, resp.status_code, resp.text)
            return False
    except Exception as e:
        logger.error("Erro ao reportar resultado do job #%d: %s", job_id, e)
        return False


def process_job(job: dict) -> None:
    """
    Processa um job: executa gerar_e_publicar_capitulo e reporta resultado.

    Args:
        job: Dict do job retornado pela API.
    """
    job_id = job["id"]
    curso = job["curso"]
    modulo = job["modulo"]
    tema = job["tema"]
    objetivo = job.get("objetivo", "")
    nivel = job.get("nivel", "intermediário")

    logger.info(
        "Processando job #%d: curso=%s, modulo=%s, tema='%s'",
        job_id, curso, modulo, tema,
    )

    try:
        from generators.gerar_conteudo_ia import gerar_e_publicar_capitulo

        resultado = gerar_e_publicar_capitulo(
            curso_slug=curso,
            modulo_dir=modulo,
            tema=tema,
            objetivo=objetivo,
            nivel=nivel,
            auto_publish=False,  # Segurança: nunca auto-publish via watcher
        )

        if resultado["status"] == "error":
            logger.error("Job #%d falhou: %s", job_id, resultado["erro"])
            report_result(job_id, resultado, erro=resultado["erro"])
        else:
            logger.info("Job #%d concluído: status=%s", job_id, resultado["status"])
            report_result(job_id, resultado)

    except Exception as e:
        erro_msg = f"{type(e).__name__}: {e}\n{traceback.format_exc()}"
        logger.exception("Exceção não tratada no job #%d", job_id)
        report_result(job_id, {}, erro=erro_msg)


def main_loop() -> None:
    """Loop principal do watcher com backoff exponencial."""
    backoff = POLL_INTERVAL
    consecutive_errors = 0

    logger.info("=" * 60)
    logger.info("  CourseForge Watcher iniciado")
    logger.info("  API: %s", HERMES_API_URL)
    logger.info("  Intervalo: %ds", POLL_INTERVAL)
    logger.info("=" * 60)

    print(f"[WATCHER] Iniciado. Polling {HERMES_API_URL} a cada {POLL_INTERVAL}s",
          file=sys.stderr)

    while _running:
        try:
            job = fetch_pending_job()

            if job:
                consecutive_errors = 0
                backoff = POLL_INTERVAL
                process_job(job)
                # Não dormir — checar imediatamente se há mais jobs
                continue
            else:
                consecutive_errors = 0
                backoff = POLL_INTERVAL

        except requests.exceptions.ConnectionError:
            consecutive_errors += 1
            backoff = min(POLL_INTERVAL * (2 ** consecutive_errors), MAX_BACKOFF)
            logger.warning(
                "VPS inacessível (tentativa %d). Próximo retry em %ds.",
                consecutive_errors, backoff,
            )
        except requests.exceptions.Timeout:
            consecutive_errors += 1
            backoff = min(POLL_INTERVAL * (2 ** consecutive_errors), MAX_BACKOFF)
            logger.warning("Timeout ao contactar VPS. Retry em %ds.", backoff)
        except Exception as e:
            consecutive_errors += 1
            backoff = min(POLL_INTERVAL * (2 ** consecutive_errors), MAX_BACKOFF)
            logger.exception("Erro inesperado no watcher: %s", e)

        # Dormir em intervalos curtos para reagir rápido a shutdown
        elapsed = 0
        while _running and elapsed < backoff:
            time.sleep(min(1, backoff - elapsed))
            elapsed += 1

    logger.info("Watcher encerrado.")
    print("[WATCHER] Encerrado.", file=sys.stderr)


def main() -> None:
    """Entry point."""
    if not HERMES_API_URL:
        print(
            "[ERRO] HERMES_API_URL não configurado.\n"
            "Defina no arquivo .env ou como variável de ambiente.\n"
            "Exemplo: HERMES_API_URL=http://100.x.x.x:8765",
            file=sys.stderr,
        )
        sys.exit(1)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    main_loop()


if __name__ == "__main__":
    main()
