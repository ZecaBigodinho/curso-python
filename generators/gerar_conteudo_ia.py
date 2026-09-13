"""
CourseForge — generators/gerar_conteudo_ia.py

Motor de geração automática de conteúdo via OpenCode + NVIDIA NIM.

Substitui as Fases 1 e 2 do AI_COURSEFORGE_PLAYBOOK.md:
  - Fase 1 (geração de prompt) → continua usando PromptGenerator
  - Fase 2 (colagem manual do DeepSeek) → agora automática via OpenCode

Fluxo:
  1. Cria placeholder do capítulo via ChapterGenerator
  2. Monta prompt via PromptGenerator
  3. Chama OpenCode em modo não-interativo (subprocess)
  4. Escreve resultado no arquivo .md
  5. Atualiza mkdocs.yml, build, e opcionalmente gh-deploy

Uso programático:
    from generators.gerar_conteudo_ia import gerar_e_publicar_capitulo
    resultado = gerar_e_publicar_capitulo("python_para_desktop", "modulo_01_fundamentos", "Decoradores")

Uso CLI:
    python main.py gerar-ia python_para_desktop modulo_01_fundamentos "Decoradores"
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

from models.chapter import Chapter
from models.enums import NivelDificuldade, TipoPrompt
from utils.file_manager import FileManager
from utils.template_engine import TemplateEngine
from utils.constants import DIR_CURSOS, DIR_MKDOCS
from utils.logger import get_logger

logger = get_logger(__name__)

# Raiz do projeto (mesmo padrão do main.py)
PROJECT_ROOT = Path(__file__).parent.parent.resolve()

# Configuração padrão do modelo (pode ser sobrescrita via .env ou argumento)
DEFAULT_MODEL = os.environ.get(
    "OPENCODE_MODEL", "nvidia/deepseek-ai/deepseek-v4-pro"
)

# Timeout para a chamada ao OpenCode (em segundos)
OPENCODE_TIMEOUT = int(os.environ.get("OPENCODE_TIMEOUT", "600"))

# URL base do site publicado (para montar links)
SITE_BASE_URL = os.environ.get(
    "SITE_BASE_URL", "https://zecabigodinho.github.io/curso-python/"
)


# ------------------------------------------------------------------ #
# Função pública principal                                             #
# ------------------------------------------------------------------ #

def gerar_e_publicar_capitulo(
    curso_slug: str,
    modulo_dir: str,
    tema: str,
    objetivo: str = "",
    nivel: str = "intermediário",
    auto_publish: bool = False,
    model: str | None = None,
    numero: int | None = None,
) -> dict:
    """
    Gera um capítulo completo via IA e opcionalmente publica no GitHub Pages.

    Substitui o fluxo manual de copiar/colar entre Gemini e DeepSeek.
    Reaproveita ChapterGenerator e PromptGenerator existentes.

    Args:
        curso_slug: Slug do curso (ex: "python_para_desktop").
        modulo_dir: Diretório do módulo (ex: "modulo_01_fundamentos").
        tema: Tema/nome do capítulo (ex: "Decoradores").
        objetivo: Objetivo do capítulo (opcional).
        nivel: Nível de dificuldade ("iniciante", "intermediário", "avançado").
        auto_publish: Se True, executa gh-deploy automaticamente.
        model: Modelo do OpenCode a usar (default: env OPENCODE_MODEL).
        numero: Número do capítulo (auto-detectado se None).

    Returns:
        dict com:
            - status: "success" | "error" | "pending_approval"
            - capitulo_path: str (caminho absoluto do arquivo)
            - capitulo_filename: str (nome do arquivo)
            - link: str | None (URL no GitHub Pages, se publicado)
            - erro: str | None (mensagem de erro, se houver)
    """
    model = model or DEFAULT_MODEL

    logger.info(
        "Iniciando geração automática: curso=%s, modulo=%s, tema='%s', modelo=%s",
        curso_slug, modulo_dir, tema, model,
    )

    resultado = {
        "status": "error",
        "capitulo_path": "",
        "capitulo_filename": "",
        "link": None,
        "erro": None,
    }

    try:
        # ── 1. Inicializar componentes ────────────────────────────────
        fm = FileManager(PROJECT_ROOT)
        te = TemplateEngine(PROJECT_ROOT / "templates")

        from generators.gerar_capitulo import ChapterGenerator
        from generators.gerar_prompt import PromptGenerator
        from generators.atualizar_mkdocs import MkDocsUpdater
        from utils.config_loader import ConfigLoader

        chap_gen = ChapterGenerator(fm, te)
        prompt_gen = PromptGenerator(fm, te)

        config_loader = ConfigLoader(PROJECT_ROOT / "config" / "config.yaml")
        mkdocs_upd = MkDocsUpdater(fm, config_loader.as_dict())

        # ── 2. Detectar próximo número de capítulo ────────────────────
        if numero is None:
            numero = chap_gen._detectar_proximo_numero(curso_slug, modulo_dir)
        logger.info("Número do capítulo: %02d", numero)

        # ── 3. Criar Chapter e placeholder ────────────────────────────
        nivel_enum = NivelDificuldade.from_str(nivel)
        meta_curso = fm.ler_metadados_curso(fm.path(DIR_CURSOS) / curso_slug)

        chapter = Chapter(
            nome=tema,
            curso_slug=curso_slug,
            modulo_dir=modulo_dir,
            numero=numero,
            objetivo=objetivo,
            nivel=nivel_enum,
        )

        cap_path = chap_gen.criar(chapter, meta_curso)
        resultado["capitulo_path"] = str(cap_path)
        resultado["capitulo_filename"] = chapter.filename
        logger.info("Placeholder criado: %s", cap_path)

        # ── 4. Gerar prompt ───────────────────────────────────────────
        contexto_prompt = {
            "curso": meta_curso.get("nome", curso_slug) if meta_curso else curso_slug,
            "tema": chapter.nome,
            "nivel": chapter.nivel.value,
            "capitulo": chapter.nome,
            "objetivo": chapter.objetivo or f"Compreender {chapter.nome}",
            "palavras_minimas": 1500,
        }
        prompt = prompt_gen.gerar(TipoPrompt.CAPITULO, contexto_prompt)
        logger.info("Prompt gerado (%d caracteres)", len(prompt))

        # ── 5. Chamar OpenCode via subprocess ─────────────────────────
        logger.info("Chamando OpenCode (modelo: %s)...", model)
        conteudo_ia = _chamar_opencode(prompt, model)

        if not conteudo_ia or len(conteudo_ia.strip()) < 100:
            raise RuntimeError(
                f"OpenCode retornou conteúdo insuficiente ({len(conteudo_ia)} chars). "
                "Verifique a chave NVIDIA_API_KEY e o modelo configurado."
            )
        logger.info("Conteúdo gerado com sucesso (%d caracteres)", len(conteudo_ia))

        # ── 6. Escrever conteúdo no arquivo .md ──────────────────────
        fm.escrever(cap_path, conteudo_ia, sobrescrever=True)
        logger.info("Arquivo sobrescrito: %s", cap_path)

        # ── 7. Atualizar mkdocs.yml ──────────────────────────────────
        mkdocs_upd.atualizar(silencioso=True)
        logger.info("mkdocs.yml atualizado")

        # ── 8. Build com validação ───────────────────────────────────
        _executar_build(fm)
        logger.info("Build MkDocs concluído com sucesso")

        # ── 9. Publicar (se auto_publish) ────────────────────────────
        link_capitulo = _montar_link(curso_slug, modulo_dir, chapter.filename)

        if auto_publish:
            _executar_deploy(fm)
            resultado["status"] = "success"
            resultado["link"] = link_capitulo
            logger.info("Deploy concluído! Link: %s", link_capitulo)
        else:
            resultado["status"] = "pending_approval"
            resultado["link"] = link_capitulo  # link potencial, ainda não publicado
            logger.info(
                "Capítulo gerado e validado (build OK). Aguardando aprovação para deploy."
            )

    except Exception as e:
        resultado["status"] = "error"
        resultado["erro"] = str(e)
        logger.exception("Erro na geração automática: %s", e)

    return resultado


# ------------------------------------------------------------------ #
# Funções auxiliares                                                   #
# ------------------------------------------------------------------ #

def _chamar_opencode(prompt: str, model: str) -> str:
    """
    Chama o OpenCode em modo não-interativo e retorna o conteúdo gerado.

    Estratégia:
      1. Tenta com --format json (parsing estruturado)
      2. Fallback para --format default (output raw)

    Args:
        prompt: Texto completo do prompt a enviar.
        model: Identificador do modelo (ex: "nvidia/deepseek-ai/deepseek-v4-pro").

    Returns:
        Conteúdo Markdown gerado pela IA.

    Raises:
        RuntimeError: Se o OpenCode falhar ou retornar vazio.
    """
    # Tentar primeiro com formato JSON para parsing estruturado
    try:
        return _chamar_opencode_json(prompt, model)
    except Exception as e:
        logger.warning("Fallback: JSON parsing falhou (%s). Tentando formato default...", e)

    # Fallback: formato default (texto puro)
    return _chamar_opencode_default(prompt, model)


def _chamar_opencode_json(prompt: str, model: str) -> str:
    """Chama OpenCode com --format json e parseia eventos JSONL."""
    result = subprocess.run(
        ["opencode", "run", prompt, "--model", model, "--format", "json"],
        capture_output=True,
        text=True,
        timeout=OPENCODE_TIMEOUT,
        cwd=str(PROJECT_ROOT),
        env={**os.environ, "NO_COLOR": "1"},
    )

    if result.returncode != 0:
        stderr = result.stderr.strip() if result.stderr else "(sem detalhes)"
        raise RuntimeError(f"OpenCode falhou (exit code {result.returncode}): {stderr}")

    # Parsear eventos JSONL — extrair texto das mensagens do assistente
    conteudo_parts = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            evento = json.loads(line)
            # Extrair conteúdo textual dos eventos
            if isinstance(evento, dict):
                # Formato varia por versão do OpenCode — tentar múltiplos campos
                text = (
                    evento.get("text", "")
                    or evento.get("content", "")
                    or evento.get("message", {}).get("content", "")
                )
                if text:
                    conteudo_parts.append(text)
        except json.JSONDecodeError:
            # Linha não é JSON válido — pode ser output de controle
            continue

    conteudo = "".join(conteudo_parts)
    if not conteudo.strip():
        raise RuntimeError("Nenhum conteúdo extraído dos eventos JSON do OpenCode")

    return _limpar_markdown(conteudo)


def _chamar_opencode_default(prompt: str, model: str) -> str:
    """Chama OpenCode com --format default e captura output raw."""
    result = subprocess.run(
        ["opencode", "run", prompt, "--model", model, "--format", "default"],
        capture_output=True,
        text=True,
        timeout=OPENCODE_TIMEOUT,
        cwd=str(PROJECT_ROOT),
        env={**os.environ, "NO_COLOR": "1"},
    )

    if result.returncode != 0:
        stderr = result.stderr.strip() if result.stderr else "(sem detalhes)"
        raise RuntimeError(f"OpenCode falhou (exit code {result.returncode}): {stderr}")

    conteudo = result.stdout.strip()
    if not conteudo:
        raise RuntimeError("OpenCode retornou output vazio (formato default)")

    return _limpar_markdown(conteudo)


def _limpar_markdown(conteudo: str) -> str:
    """
    Limpa o conteúdo Markdown retornado pela IA.

    Remove:
      - Fences ```markdown ... ``` envolvendo todo o conteúdo
      - Prefixos de sistema/controle do OpenCode
      - Linhas em branco excessivas
    """
    conteudo = conteudo.strip()

    # Remover fence de markdown se o modelo envolver tudo em ```markdown
    fence_pattern = r"^```(?:markdown|md)?\s*\n(.*?)\n```\s*$"
    match = re.match(fence_pattern, conteudo, re.DOTALL)
    if match:
        conteudo = match.group(1).strip()

    # Remover linhas de controle do OpenCode (ex: "Session: ...", "Model: ...")
    linhas = conteudo.splitlines()
    inicio_conteudo = 0
    for i, linha in enumerate(linhas):
        # O conteúdo real começa com # (título Markdown)
        if linha.strip().startswith("#"):
            inicio_conteudo = i
            break
    conteudo = "\n".join(linhas[inicio_conteudo:])

    # Normalizar quebras de linha excessivas (máximo 2 consecutivas)
    conteudo = re.sub(r"\n{3,}", "\n\n", conteudo)

    return conteudo.strip()


def _executar_build(fm: FileManager) -> None:
    """Executa mkdocs build --strict para validar o conteúdo."""
    resultado = subprocess.run(
        [sys.executable, "-m", "mkdocs", "build", "--strict", "-f", "mkdocs/mkdocs.yml"],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
    )

    if resultado.returncode != 0:
        stderr = resultado.stderr.strip() if resultado.stderr else "(sem detalhes)"
        raise RuntimeError(f"mkdocs build falhou: {stderr}")


def _executar_deploy(fm: FileManager) -> None:
    """Executa mkdocs gh-deploy --force."""
    resultado = subprocess.run(
        [sys.executable, "-m", "mkdocs", "gh-deploy", "-f", "mkdocs/mkdocs.yml", "--force"],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
    )

    if resultado.returncode != 0:
        stderr = resultado.stderr.strip() if resultado.stderr else "(sem detalhes)"
        raise RuntimeError(f"mkdocs gh-deploy falhou: {stderr}")


def _montar_link(curso_slug: str, modulo_dir: str, filename: str) -> str:
    """Monta o link público do capítulo no GitHub Pages."""
    # Remove a extensão .md para montar o path de URL
    page_slug = filename.replace(".md", "/")
    base = SITE_BASE_URL.rstrip("/")
    return f"{base}/{curso_slug}/{modulo_dir}/{page_slug}"
