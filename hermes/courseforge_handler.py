"""
CourseForge — hermes/courseforge_handler.py

Handler do comando /novaaula para integração com Telegram.

Uso no Telegram:
    /novaaula <curso_slug> <modulo_dir> <tema>

Exemplo:
    /novaaula python_para_desktop modulo_01_fundamentos "Decoradores"

Responsabilidades:
    1. Parsear argumentos do comando
    2. Gravar job na fila SQLite
    3. Checar se o PC está online via Tailscale (ping)
    4. Se online: disparar execução via SSH
    5. Notificar o resultado no Telegram
"""
from __future__ import annotations

import os
import platform
import shlex
import subprocess
import sys
from typing import Optional

from hermes.job_queue import JobQueue
from hermes.notifier import notificar_job_registrado


# Configuração via ambiente
PC_TAILSCALE_IP = os.environ.get("PC_TAILSCALE_IP", "")
SSH_USER = os.environ.get("SSH_USER", "")
SSH_KEY_PATH = os.environ.get("SSH_KEY_PATH", "")
COURSEFORGE_PATH = os.environ.get("COURSEFORGE_PATH", r"E:\chave\curso\CourseForge")


def parsear_comando_novaaula(texto: str) -> dict | None:
    """
    Parseia o texto do comando /novaaula.

    Formatos aceitos:
        /novaaula <curso> <modulo> <tema>
        /novaaula <curso> <modulo> "<tema com espaços>"
        /novaaula <curso> <modulo> <tema> --objetivo "..." --nivel "..."

    Returns:
        Dict com curso, modulo, tema, objetivo, nivel ou None se inválido.
    """
    # Remover o /novaaula do início
    texto = texto.strip()
    if texto.startswith("/novaaula"):
        texto = texto[len("/novaaula"):].strip()

    if not texto:
        return None

    try:
        partes = shlex.split(texto)
    except ValueError:
        # Fallback para split simples se shlex falhar
        partes = texto.split()

    if len(partes) < 3:
        return None

    resultado = {
        "curso": partes[0],
        "modulo": partes[1],
        "tema": partes[2],
        "objetivo": "",
        "nivel": "intermediário",
    }

    # Parsear flags opcionais
    i = 3
    while i < len(partes):
        if partes[i] == "--objetivo" and i + 1 < len(partes):
            resultado["objetivo"] = partes[i + 1]
            i += 2
        elif partes[i] == "--nivel" and i + 1 < len(partes):
            resultado["nivel"] = partes[i + 1]
            i += 2
        else:
            # Parte extra do tema (sem aspas)
            resultado["tema"] += " " + partes[i]
            i += 1

    return resultado


def checar_pc_online(ip: str | None = None, timeout: int = 3) -> bool:
    """
    Verifica se o PC está acessível via ping na rede Tailscale.

    Args:
        ip: IP Tailscale do PC (default: env PC_TAILSCALE_IP).
        timeout: Timeout do ping em segundos.

    Returns:
        True se o PC respondeu ao ping.
    """
    ip = ip or PC_TAILSCALE_IP
    if not ip:
        return False

    # Adaptar o comando ping para o OS
    if platform.system().lower() == "windows":
        cmd = ["ping", "-n", "1", "-w", str(timeout * 1000), ip]
    else:
        cmd = ["ping", "-c", "1", "-W", str(timeout), ip]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=timeout + 2,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def disparar_ssh(
    curso: str,
    modulo: str,
    tema: str,
    objetivo: str = "",
    nivel: str = "intermediário",
) -> bool:
    """
    Dispara a geração via SSH no PC remoto.

    Executa:
        ssh -i <key> <user>@<ip> "cd <path> && python main.py gerar-ia <args>"

    Returns:
        True se o SSH foi disparado com sucesso (assíncrono — não espera resultado).
    """
    if not all([PC_TAILSCALE_IP, SSH_USER, SSH_KEY_PATH]):
        print("[INFO] SSH não configurado. Job ficará na fila para o watcher.", file=sys.stderr)
        return False

    # Montar o comando remoto
    cmd_remoto = (
        f"cd {COURSEFORGE_PATH} && "
        f"python main.py gerar-ia "
        f"{shlex.quote(curso)} {shlex.quote(modulo)} {shlex.quote(tema)}"
    )
    if objetivo:
        cmd_remoto += f" --objetivo {shlex.quote(objetivo)}"
    if nivel:
        cmd_remoto += f" --nivel {shlex.quote(nivel)}"

    cmd_ssh = [
        "ssh",
        "-i", SSH_KEY_PATH,
        "-o", "StrictHostKeyChecking=no",
        "-o", "ConnectTimeout=5",
        f"{SSH_USER}@{PC_TAILSCALE_IP}",
        cmd_remoto,
    ]

    try:
        # Disparar assíncrono (não bloqueia o Hermes)
        subprocess.Popen(
            cmd_ssh,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print(f"[INFO] SSH disparado para {SSH_USER}@{PC_TAILSCALE_IP}", file=sys.stderr)
        return True
    except Exception as e:
        print(f"[WARN] Falha ao disparar SSH: {e}", file=sys.stderr)
        return False


def processar_novaaula(texto_comando: str, queue: JobQueue | None = None) -> str:
    """
    Processa o comando /novaaula de ponta a ponta.

    Args:
        texto_comando: Texto completo do comando (incluindo /novaaula).
        queue: Instância do JobQueue (cria default se None).

    Returns:
        Mensagem de resposta para o Telegram.
    """
    queue = queue or JobQueue()

    # 1. Parsear comando
    args = parsear_comando_novaaula(texto_comando)
    if not args:
        return (
            "❌ Formato inválido.\n\n"
            "Uso: /novaaula <curso> <modulo> <tema>\n"
            "Exemplo: /novaaula python_para_desktop modulo_01_fundamentos \"Decoradores\""
        )

    # 2. Criar job na fila
    job_id = queue.create_job(
        curso=args["curso"],
        modulo=args["modulo"],
        tema=args["tema"],
        objetivo=args["objetivo"],
        nivel=args["nivel"],
    )

    # 3. Checar disponibilidade do PC
    pc_online = checar_pc_online()

    # 4. Notificar no Telegram
    notificar_job_registrado(
        job_id=job_id,
        curso=args["curso"],
        modulo=args["modulo"],
        tema=args["tema"],
        pc_online=pc_online,
    )

    # 5. Se PC online, tentar disparar via SSH
    if pc_online:
        ssh_ok = disparar_ssh(
            curso=args["curso"],
            modulo=args["modulo"],
            tema=args["tema"],
            objetivo=args["objetivo"],
            nivel=args["nivel"],
        )
        if ssh_ok:
            return (
                f"✅ Job #{job_id} criado e execução disparada!\n"
                f"📖 {args['tema']} em {args['curso']}/{args['modulo']}\n"
                f"🟢 PC online — processando agora..."
            )

    # PC offline ou SSH falhou — job fica pendente na fila
    return (
        f"📋 Job #{job_id} registrado na fila!\n"
        f"📖 {args['tema']} em {args['curso']}/{args['modulo']}\n"
        f"🟡 Será executado quando o PC ligar."
    )
