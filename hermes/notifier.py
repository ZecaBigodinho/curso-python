"""
CourseForge — hermes/notifier.py

Envia notificações para o Telegram quando jobs são concluídos.

Usa a API do Telegram Bot diretamente (requests) — sem dependência
de frameworks como python-telegram-bot.

Configuração via variáveis de ambiente:
    TELEGRAM_BOT_TOKEN: Token do bot Telegram
    TELEGRAM_CHAT_ID: ID do chat para enviar notificações
"""
from __future__ import annotations

import os
import sys
from typing import Optional

try:
    import requests
except ImportError:
    requests = None  # type: ignore


TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

TELEGRAM_API_URL = "https://api.telegram.org/bot{token}/sendMessage"


def enviar_telegram(mensagem: str, parse_mode: str = "HTML") -> bool:
    """
    Envia uma mensagem via Telegram Bot API.

    Args:
        mensagem: Texto da mensagem (suporta HTML).
        parse_mode: Modo de parsing ("HTML" ou "Markdown").

    Returns:
        True se a mensagem foi enviada com sucesso.
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[WARN] Telegram não configurado (TELEGRAM_BOT_TOKEN ou TELEGRAM_CHAT_ID vazio).",
              file=sys.stderr)
        return False

    if requests is None:
        print("[WARN] Módulo 'requests' não instalado. Instale com: pip install requests",
              file=sys.stderr)
        return False

    url = TELEGRAM_API_URL.format(token=TELEGRAM_BOT_TOKEN)
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensagem,
        "parse_mode": parse_mode,
    }

    try:
        resp = requests.post(url, json=payload, timeout=10)
        if resp.status_code == 200:
            return True
        else:
            print(f"[WARN] Telegram API retornou {resp.status_code}: {resp.text}",
                  file=sys.stderr)
            return False
    except Exception as e:
        print(f"[WARN] Erro ao enviar Telegram: {e}", file=sys.stderr)
        return False


def notificar_job_concluido(
    job: dict,
    resultado: dict | None = None,
    erro: str | None = None,
) -> bool:
    """
    Envia notificação formatada ao Telegram quando um job finaliza.

    Args:
        job: Dict do job (da tabela SQLite).
        resultado: Dict de resultado do gerar_e_publicar_capitulo.
        erro: Mensagem de erro, se houver.

    Returns:
        True se a notificação foi enviada.
    """
    if erro:
        mensagem = (
            f"❌ <b>Falha na geração de aula</b>\n\n"
            f"📚 Curso: <code>{job.get('curso', '?')}</code>\n"
            f"📂 Módulo: <code>{job.get('modulo', '?')}</code>\n"
            f"📖 Tema: <b>{job.get('tema', '?')}</b>\n"
            f"🆔 Job: #{job.get('id', '?')}\n\n"
            f"⚠️ Erro:\n<pre>{erro[:500]}</pre>"
        )
    else:
        link = ""
        if resultado and resultado.get("link"):
            link = f"\n🔗 <a href=\"{resultado['link']}\">Ver capítulo</a>"

        status_text = ""
        if resultado and resultado.get("status") == "pending_approval":
            status_text = "\n⏳ <i>Aguardando aprovação para deploy</i>"
        elif resultado and resultado.get("status") == "success":
            status_text = "\n✅ <i>Deploy concluído</i>"

        filename = ""
        if resultado and resultado.get("capitulo_filename"):
            filename = f"\n📄 Arquivo: <code>{resultado['capitulo_filename']}</code>"

        mensagem = (
            f"✅ <b>Aula gerada com sucesso!</b>\n\n"
            f"📚 Curso: <code>{job.get('curso', '?')}</code>\n"
            f"📂 Módulo: <code>{job.get('modulo', '?')}</code>\n"
            f"📖 Tema: <b>{job.get('tema', '?')}</b>\n"
            f"🆔 Job: #{job.get('id', '?')}"
            f"{filename}{link}{status_text}"
        )

    return enviar_telegram(mensagem)


def notificar_job_registrado(job_id: int, curso: str, modulo: str, tema: str, pc_online: bool) -> bool:
    """
    Notifica que um novo job foi registrado na fila.

    Args:
        job_id: ID do job criado.
        curso: Slug do curso.
        modulo: Diretório do módulo.
        tema: Tema do capítulo.
        pc_online: Se o PC está acessível via Tailscale.
    """
    if pc_online:
        status = "🟢 PC online — executando agora..."
    else:
        status = "🟡 PC offline — será executado quando ligar"

    mensagem = (
        f"📋 <b>Nova aula registrada</b>\n\n"
        f"📚 Curso: <code>{curso}</code>\n"
        f"📂 Módulo: <code>{modulo}</code>\n"
        f"📖 Tema: <b>{tema}</b>\n"
        f"🆔 Job: #{job_id}\n\n"
        f"{status}"
    )

    return enviar_telegram(mensagem)
