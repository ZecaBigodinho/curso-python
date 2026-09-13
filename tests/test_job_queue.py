"""
Testes unitários para hermes/job_queue.py

Testa operações CRUD da fila SQLite.
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from hermes.job_queue import JobQueue


@pytest.fixture
def queue(tmp_path):
    """Cria uma fila temporária para cada teste."""
    db_path = tmp_path / "test_jobs.db"
    return JobQueue(db_path)


class TestJobQueue:
    """Testes da fila de jobs SQLite."""

    def test_create_job(self, queue):
        """Testa criação de um job."""
        job_id = queue.create_job(
            curso="python_para_desktop",
            modulo="modulo_01_fundamentos",
            tema="Decoradores",
        )
        assert job_id is not None
        assert job_id >= 1

    def test_get_pending(self, queue):
        """Testa recuperação de job pendente."""
        queue.create_job("curso_a", "modulo_01", "Tema A")
        queue.create_job("curso_b", "modulo_02", "Tema B")

        job = queue.get_pending()
        assert job is not None
        assert job["curso"] == "curso_a"  # FIFO: primeiro criado
        assert job["tema"] == "Tema A"

    def test_get_pending_marks_running(self, queue):
        """Testa que get_pending marca o job como running."""
        queue.create_job("curso_a", "modulo_01", "Tema A")

        job = queue.get_pending()
        assert job is not None

        # O próximo get_pending não deve retornar o mesmo job
        next_job = queue.get_pending()
        assert next_job is None  # Não há mais pendentes

    def test_get_pending_empty(self, queue):
        """Testa retorno quando não há jobs pendentes."""
        job = queue.get_pending()
        assert job is None

    def test_mark_completed(self, queue):
        """Testa marcação de job como concluído."""
        job_id = queue.create_job("curso_a", "modulo_01", "Tema A")
        queue.mark_running(job_id)
        queue.mark_completed(job_id, {"status": "success", "link": "https://example.com"})

        job = queue.get_job(job_id)
        assert job["status"] == "completed"
        assert "success" in job["resultado"]

    def test_mark_error(self, queue):
        """Testa marcação de job como erro."""
        job_id = queue.create_job("curso_a", "modulo_01", "Tema A")
        queue.mark_running(job_id)
        queue.mark_error(job_id, "OpenCode falhou")

        job = queue.get_job(job_id)
        assert job["status"] == "error"
        assert "OpenCode falhou" in job["erro"]

    def test_list_jobs(self, queue):
        """Testa listagem de jobs."""
        queue.create_job("curso_a", "modulo_01", "Tema A")
        queue.create_job("curso_b", "modulo_02", "Tema B")
        queue.create_job("curso_c", "modulo_03", "Tema C")

        jobs = queue.list_jobs()
        assert len(jobs) == 3

    def test_list_jobs_filtered(self, queue):
        """Testa listagem filtrada por status."""
        queue.create_job("curso_a", "modulo_01", "Tema A")
        job_id_b = queue.create_job("curso_b", "modulo_02", "Tema B")
        queue.mark_running(job_id_b)

        pending = queue.list_jobs(status="pending")
        assert len(pending) == 1

        running = queue.list_jobs(status="running")
        assert len(running) == 1

    def test_count_pending(self, queue):
        """Testa contagem de jobs pendentes."""
        assert queue.count_pending() == 0

        queue.create_job("curso_a", "modulo_01", "Tema A")
        queue.create_job("curso_b", "modulo_02", "Tema B")
        assert queue.count_pending() == 2

        queue.get_pending()  # Remove um da fila
        assert queue.count_pending() == 1

    def test_get_job(self, queue):
        """Testa recuperação de job por ID."""
        job_id = queue.create_job(
            curso="python_para_desktop",
            modulo="modulo_01_fundamentos",
            tema="Decoradores",
            objetivo="Aprender decoradores",
            nivel="avançado",
        )

        job = queue.get_job(job_id)
        assert job is not None
        assert job["curso"] == "python_para_desktop"
        assert job["tema"] == "Decoradores"
        assert job["objetivo"] == "Aprender decoradores"
        assert job["nivel"] == "avançado"

    def test_get_job_not_found(self, queue):
        """Testa recuperação de job inexistente."""
        job = queue.get_job(9999)
        assert job is None

    def test_fifo_ordering(self, queue):
        """Testa que jobs são consumidos na ordem FIFO."""
        queue.create_job("curso", "mod", "Primeiro")
        queue.create_job("curso", "mod", "Segundo")
        queue.create_job("curso", "mod", "Terceiro")

        job1 = queue.get_pending()
        assert job1["tema"] == "Primeiro"

        job2 = queue.get_pending()
        assert job2["tema"] == "Segundo"

        job3 = queue.get_pending()
        assert job3["tema"] == "Terceiro"

        assert queue.get_pending() is None
