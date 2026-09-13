"""
CourseForge — hermes/api_server.py

Servidor HTTP interno para o watcher consultar jobs pendentes.

Endpoints (acessíveis apenas via rede Tailscale):
    GET  /health           → health check
    GET  /jobs/pending     → retorna próximo job pendente (marca como running)
    POST /jobs/{id}/concluido  → recebe resultado e marca como concluído

Roda como thread no processo do Hermes, ou standalone via __main__.

Segurança:
    - Escuta apenas no IP Tailscale (não 0.0.0.0)
    - Token de autenticação via header Authorization: Bearer <token>
"""
from __future__ import annotations

import json
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Optional
from urllib.parse import urlparse

from hermes.job_queue import JobQueue

# Configuração via ambiente
API_HOST = os.environ.get("HERMES_API_HOST", "0.0.0.0")
API_PORT = int(os.environ.get("HERMES_API_PORT", "8765"))
API_TOKEN = os.environ.get("HERMES_API_TOKEN", "")


class JobAPIHandler(BaseHTTPRequestHandler):
    """Handler HTTP para endpoints da fila de jobs."""

    # Referência ao JobQueue — definida na criação do servidor
    queue: JobQueue

    def do_GET(self) -> None:
        """Roteia requisições GET."""
        path = urlparse(self.path).path.rstrip("/")

        if not self._check_auth():
            return

        if path == "/health":
            self._respond_json({"status": "ok", "service": "courseforge-hermes"})

        elif path == "/jobs/pending":
            job = self.queue.get_pending()
            if job:
                self._respond_json({"job": job})
            else:
                self._respond_json({"job": None}, status=204)

        else:
            self._respond_json({"error": "Not found"}, status=404)

    def do_POST(self) -> None:
        """Roteia requisições POST."""
        path = urlparse(self.path).path.rstrip("/")

        if not self._check_auth():
            return

        # POST /jobs/create — Cria um novo job na fila
        if path == "/jobs/create":
            body = self._read_body()
            if body is None:
                return

            # Validar campos obrigatórios
            curso = body.get("curso", "")
            modulo = body.get("modulo", "")
            tema = body.get("tema", "")

            if not all([curso, modulo, tema]):
                self._respond_json(
                    {"error": "Campos obrigatórios: curso, modulo, tema"},
                    status=400,
                )
                return

            job_id = self.queue.create_job(
                curso=curso,
                modulo=modulo,
                tema=tema,
                objetivo=body.get("objetivo", ""),
                nivel=body.get("nivel", "intermediário"),
            )
            self._respond_json({"ok": True, "job_id": job_id}, status=201)
            return

        # POST /jobs/{id}/concluido
        parts = path.split("/")
        if len(parts) == 4 and parts[1] == "jobs" and parts[3] == "concluido":
            try:
                job_id = int(parts[2])
            except ValueError:
                self._respond_json({"error": "ID inválido"}, status=400)
                return

            body = self._read_body()
            if body is None:
                return

            status = body.get("status", "completed")
            resultado = body.get("resultado", {})
            erro = body.get("erro", "")

            if status == "error":
                self.queue.mark_error(job_id, erro)
            else:
                self.queue.mark_completed(job_id, resultado)

            # Disparar notificação Telegram (import lazy para evitar circular)
            try:
                from hermes.notifier import notificar_job_concluido
                job = self.queue.get_job(job_id)
                if job:
                    notificar_job_concluido(job, resultado, erro if status == "error" else None)
            except Exception as e:
                print(f"[WARN] Falha ao notificar Telegram: {e}", file=sys.stderr)

            self._respond_json({"ok": True, "job_id": job_id})

        else:
            self._respond_json({"error": "Not found"}, status=404)

    # ------------------------------------------------------------------ #
    # Helpers                                                              #
    # ------------------------------------------------------------------ #

    def _check_auth(self) -> bool:
        """Verifica token de autenticação, se configurado."""
        if not API_TOKEN:
            return True  # Sem token configurado = sem auth (uso em rede privada)

        auth_header = self.headers.get("Authorization", "")
        if auth_header == f"Bearer {API_TOKEN}":
            return True

        self._respond_json({"error": "Unauthorized"}, status=401)
        return False

    def _respond_json(self, data: dict, status: int = 200) -> None:
        """Envia resposta JSON."""
        body = json.dumps(data, ensure_ascii=False, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self) -> dict | None:
        """Lê e parseia o body JSON da requisição."""
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(content_length)
            return json.loads(raw.decode("utf-8"))
        except (json.JSONDecodeError, ValueError) as e:
            self._respond_json({"error": f"JSON inválido: {e}"}, status=400)
            return None

    def log_message(self, format: str, *args) -> None:
        """Redireciona logs do HTTPServer para stderr com timestamp."""
        print(f"[API] {self.address_string()} - {format % args}", file=sys.stderr)


def create_server(
    queue: JobQueue,
    host: str | None = None,
    port: int | None = None,
) -> HTTPServer:
    """
    Cria e retorna o servidor HTTP (não inicia).

    Args:
        queue: Instância do JobQueue.
        host: Endereço para escutar (default: env HERMES_API_HOST).
        port: Porta para escutar (default: env HERMES_API_PORT).

    Returns:
        HTTPServer configurado. Chamar .serve_forever() para iniciar.
    """
    host = host or API_HOST
    port = port or API_PORT

    # Injeta a referência do queue no handler
    handler_class = type("Handler", (JobAPIHandler,), {"queue": queue})

    server = HTTPServer((host, port), handler_class)
    print(f"[API] Servidor HTTP escutando em {host}:{port}", file=sys.stderr)
    return server


def run_server(queue: JobQueue | None = None) -> None:
    """Inicia o servidor HTTP (bloqueante)."""
    queue = queue or JobQueue()
    server = create_server(queue)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[API] Servidor encerrado.", file=sys.stderr)
        server.server_close()


if __name__ == "__main__":
    run_server()
