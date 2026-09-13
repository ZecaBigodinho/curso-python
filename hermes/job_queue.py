"""
CourseForge — hermes/job_queue.py

Fila de tarefas SQLite para geração de capítulos.

A tabela `jobs` é a fonte de verdade do sistema de automação.
O Hermes grava jobs nela, e o watcher do PC consome.

Schema:
    jobs(id, curso, modulo, tema, objetivo, nivel, status,
         criado_em, iniciado_em, concluido_em, resultado, erro)

Status possíveis:
    pending   → gravado, aguardando execução
    running   → watcher está executando
    completed → finalizado com sucesso
    error     → finalizado com erro
"""
from __future__ import annotations

import json
import sqlite3
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


# Caminho padrão do banco (relativo ao diretório do hermes)
DEFAULT_DB_PATH = Path(__file__).parent / "courseforge_jobs.db"


class JobQueue:
    """
    Gerenciador da fila de tarefas SQLite.

    Thread-safe via lock interno. Usa um único banco por instância.
    """

    def __init__(self, db_path: Path | str | None = None) -> None:
        self.db_path = str(db_path or DEFAULT_DB_PATH)
        self._lock = threading.Lock()
        self._init_db()

    # ------------------------------------------------------------------ #
    # Inicialização                                                        #
    # ------------------------------------------------------------------ #

    def _init_db(self) -> None:
        """Cria a tabela se não existir."""
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS jobs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    curso TEXT NOT NULL,
                    modulo TEXT NOT NULL,
                    tema TEXT NOT NULL,
                    objetivo TEXT DEFAULT '',
                    nivel TEXT DEFAULT 'intermediário',
                    status TEXT DEFAULT 'pending',
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    iniciado_em TIMESTAMP,
                    concluido_em TIMESTAMP,
                    resultado TEXT,
                    erro TEXT
                )
            """)

    def _connect(self) -> sqlite3.Connection:
        """Abre conexão com row_factory para dicts."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        return conn

    # ------------------------------------------------------------------ #
    # Operações públicas                                                   #
    # ------------------------------------------------------------------ #

    def create_job(
        self,
        curso: str,
        modulo: str,
        tema: str,
        objetivo: str = "",
        nivel: str = "intermediário",
    ) -> int:
        """
        Cria um novo job na fila com status 'pending'.

        Returns:
            ID do job criado.
        """
        with self._lock:
            with self._connect() as conn:
                cursor = conn.execute(
                    """
                    INSERT INTO jobs (curso, modulo, tema, objetivo, nivel, status)
                    VALUES (?, ?, ?, ?, ?, 'pending')
                    """,
                    (curso, modulo, tema, objetivo, nivel),
                )
                return cursor.lastrowid

    def get_pending(self) -> dict | None:
        """
        Retorna o próximo job pendente (FIFO) e marca como 'running'.

        Returns:
            Dict com os dados do job, ou None se não houver pendentes.
        """
        with self._lock:
            with self._connect() as conn:
                row = conn.execute(
                    """
                    SELECT * FROM jobs
                    WHERE status = 'pending'
                    ORDER BY criado_em ASC
                    LIMIT 1
                    """,
                ).fetchone()

                if not row:
                    return None

                # Marcar como running atomicamente
                conn.execute(
                    """
                    UPDATE jobs
                    SET status = 'running', iniciado_em = ?
                    WHERE id = ?
                    """,
                    (datetime.now(timezone.utc).isoformat(), row["id"]),
                )

                return dict(row)

    def mark_completed(self, job_id: int, resultado: dict) -> None:
        """Marca um job como concluído com sucesso."""
        with self._lock:
            with self._connect() as conn:
                conn.execute(
                    """
                    UPDATE jobs
                    SET status = 'completed',
                        concluido_em = ?,
                        resultado = ?
                    WHERE id = ?
                    """,
                    (
                        datetime.now(timezone.utc).isoformat(),
                        json.dumps(resultado, ensure_ascii=False),
                        job_id,
                    ),
                )

    def mark_error(self, job_id: int, erro: str) -> None:
        """Marca um job como falho."""
        with self._lock:
            with self._connect() as conn:
                conn.execute(
                    """
                    UPDATE jobs
                    SET status = 'error',
                        concluido_em = ?,
                        erro = ?
                    WHERE id = ?
                    """,
                    (datetime.now(timezone.utc).isoformat(), erro, job_id),
                )

    def mark_running(self, job_id: int) -> None:
        """Marca um job como em execução."""
        with self._lock:
            with self._connect() as conn:
                conn.execute(
                    """
                    UPDATE jobs
                    SET status = 'running', iniciado_em = ?
                    WHERE id = ?
                    """,
                    (datetime.now(timezone.utc).isoformat(), job_id),
                )

    def get_job(self, job_id: int) -> dict | None:
        """Retorna um job pelo ID."""
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM jobs WHERE id = ?", (job_id,)
            ).fetchone()
            return dict(row) if row else None

    def list_jobs(self, status: str | None = None, limit: int = 50) -> list[dict]:
        """Lista jobs, opcionalmente filtrados por status."""
        with self._connect() as conn:
            if status:
                rows = conn.execute(
                    "SELECT * FROM jobs WHERE status = ? ORDER BY criado_em DESC LIMIT ?",
                    (status, limit),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM jobs ORDER BY criado_em DESC LIMIT ?",
                    (limit,),
                ).fetchall()
            return [dict(r) for r in rows]

    def count_pending(self) -> int:
        """Retorna a quantidade de jobs pendentes."""
        with self._connect() as conn:
            row = conn.execute(
                "SELECT COUNT(*) as cnt FROM jobs WHERE status = 'pending'"
            ).fetchone()
            return row["cnt"] if row else 0
