"""
CourseForge — hermes/__main__.py

Ponto de entrada do Hermes Agent.

Inicia três componentes em paralelo:
    1. Bot Telegram (polling de comandos)
    2. Servidor HTTP (API para o watcher)
    3. Fila de jobs (SQLite compartilhada)

Uso:
    python -m hermes

Requer:
    - TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID no .env
    - Rede Tailscale configurada (para o API server)
"""
from __future__ import annotations

import os
import sys
import signal
import threading
import time

# Carregar .env se disponível
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from hermes.job_queue import JobQueue
from hermes.api_server import create_server
from hermes.courseforge_handler import processar_novaaula


TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

# Flag de shutdown
_shutdown = threading.Event()


def _signal_handler(signum, frame):
    print("\n[HERMES] Recebido sinal de shutdown...", file=sys.stderr)
    _shutdown.set()


def run_telegram_polling(queue: JobQueue) -> None:
    """
    Loop simples de polling do Telegram para receber comandos.

    Usa a API getUpdates do Telegram diretamente (sem frameworks).
    """
    try:
        import requests
    except ImportError:
        print("[ERRO] Módulo 'requests' necessário. Instale: pip install requests",
              file=sys.stderr)
        return

    if not TELEGRAM_BOT_TOKEN:
        print("[WARN] TELEGRAM_BOT_TOKEN não configurado. Bot Telegram desativado.",
              file=sys.stderr)
        return

    base_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
    offset = 0
    print("[TELEGRAM] Bot iniciado. Aguardando comandos...", file=sys.stderr)

    while not _shutdown.is_set():
        try:
            resp = requests.get(
                f"{base_url}/getUpdates",
                params={"offset": offset, "timeout": 30},
                timeout=35,
            )
            if resp.status_code != 200:
                print(f"[TELEGRAM] Erro na API: {resp.status_code}", file=sys.stderr)
                time.sleep(5)
                continue

            data = resp.json()
            if not data.get("ok"):
                time.sleep(5)
                continue

            for update in data.get("result", []):
                offset = update["update_id"] + 1
                message = update.get("message", {})
                text = message.get("text", "")
                chat_id = str(message.get("chat", {}).get("id", ""))

                # Filtrar: só responder ao chat autorizado
                if TELEGRAM_CHAT_ID and chat_id != TELEGRAM_CHAT_ID:
                    continue

                if text.startswith("/novaaula"):
                    resposta = processar_novaaula(text, queue)
                    # Enviar resposta
                    try:
                        requests.post(
                            f"{base_url}/sendMessage",
                            json={
                                "chat_id": chat_id,
                                "text": resposta,
                                "parse_mode": "HTML",
                            },
                            timeout=10,
                        )
                    except Exception as e:
                        print(f"[TELEGRAM] Erro ao responder: {e}", file=sys.stderr)

                elif text.startswith("/status"):
                    # Comando de status: mostra jobs pendentes
                    pending = queue.count_pending()
                    jobs = queue.list_jobs(limit=5)
                    status_lines = [f"📊 <b>Status CourseForge</b>\n\nJobs pendentes: {pending}\n"]
                    for j in jobs[:5]:
                        emoji = {"pending": "🟡", "running": "🔵", "completed": "✅", "error": "❌"}.get(j["status"], "⚪")
                        status_lines.append(f"{emoji} #{j['id']} {j['tema']} ({j['status']})")
                    try:
                        requests.post(
                            f"{base_url}/sendMessage",
                            json={
                                "chat_id": chat_id,
                                "text": "\n".join(status_lines),
                                "parse_mode": "HTML",
                            },
                            timeout=10,
                        )
                    except Exception as e:
                        print(f"[TELEGRAM] Erro ao responder /status: {e}", file=sys.stderr)

                elif text.startswith("/help"):
                    help_text = (
                        "🤖 <b>CourseForge Hermes</b>\n\n"
                        "Comandos disponíveis:\n"
                        "/novaaula <curso> <modulo> <tema> — Registra nova aula\n"
                        "/status — Mostra jobs recentes\n"
                        "/help — Mostra esta ajuda"
                    )
                    try:
                        requests.post(
                            f"{base_url}/sendMessage",
                            json={
                                "chat_id": chat_id,
                                "text": help_text,
                                "parse_mode": "HTML",
                            },
                            timeout=10,
                        )
                    except Exception:
                        pass

        except requests.exceptions.Timeout:
            continue  # Long polling timeout normal
        except Exception as e:
            print(f"[TELEGRAM] Erro no polling: {e}", file=sys.stderr)
            time.sleep(5)


def main() -> None:
    """Ponto de entrada principal do Hermes."""
    print("=" * 60, file=sys.stderr)
    print("  CourseForge Hermes Agent", file=sys.stderr)
    print("=" * 60, file=sys.stderr)

    # Registrar signal handlers
    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)

    # Criar fila compartilhada
    queue = JobQueue()
    pending = queue.count_pending()
    print(f"[HERMES] Fila inicializada. Jobs pendentes: {pending}", file=sys.stderr)

    # Iniciar API server em thread separada
    api_server = create_server(queue)
    api_thread = threading.Thread(target=api_server.serve_forever, daemon=True)
    api_thread.start()
    print("[HERMES] API server iniciado.", file=sys.stderr)

    # Iniciar Telegram polling em thread separada
    telegram_thread = threading.Thread(target=run_telegram_polling, args=(queue,), daemon=True)
    telegram_thread.start()
    print("[HERMES] Telegram bot iniciado.", file=sys.stderr)

    # Aguardar shutdown
    print("[HERMES] Tudo rodando. Ctrl+C para encerrar.", file=sys.stderr)
    _shutdown.wait()

    # Cleanup
    api_server.shutdown()
    print("[HERMES] Encerrado.", file=sys.stderr)


if __name__ == "__main__":
    main()
