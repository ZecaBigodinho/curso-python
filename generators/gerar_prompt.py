"""
CourseForge — generators/gerar_prompt.py

Gerador de prompts profissionais para IAs (DeepSeek, ChatGPT, Claude, Gemini).

Tipos de prompt:
  - Capítulo completo
  - Lista de exercícios
  - Projeto prático

Todos os prompts são renderizados via templates Jinja2.
NUNCA monta prompts por concatenação de strings.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

from models.enums import NivelDificuldade, TipoPrompt
from utils.file_manager import FileManager
from utils.template_engine import TemplateEngine
from utils.cli_ui import UI, console
from utils.constants import DIR_PROMPTS, DIR_PROMPTS_GERADOS
from utils.logger import get_logger

from rich.panel import Panel

logger = get_logger(__name__)


class PromptGenerator:
    """
    Gera prompts profissionais para IA a partir de templates Jinja2.

    Os prompts são renderizados com o contexto coletado via CLI.
    Nunca usa concatenação de strings para montar prompts.

    Responsabilidades:
    - Selecionar tipo de prompt
    - Coletar variáveis específicas do tipo
    - Renderizar template Jinja2
    - Exibir prompt no terminal
    - Salvar em arquivo (opcional)
    """

    def __init__(self, fm: FileManager, template_engine: TemplateEngine) -> None:
        """
        Args:
            fm: Gerenciador de arquivos da plataforma.
            template_engine: Motor Jinja2 apontado para templates/ principal.
                             Este gerador usa um engine dedicado para prompts/,
                             mas recebe o engine principal por conformidade com
                             a interface dos outros geradores.
        """
        self.fm = fm
        # Engine dedicado ao diretório de prompts — diferente do engine de templates .md
        self._te_prompts = TemplateEngine(fm.path(DIR_PROMPTS))

    # ------------------------------------------------------------------ #
    # Interface pública                                                    #
    # ------------------------------------------------------------------ #

    def gerar_interativo(self) -> str | None:
        """Coleta dados via CLI e gera o prompt."""
        UI.secao("GERADOR DE PROMPTS PARA IA")

        tipo = self._selecionar_tipo()
        UI.info(f"Gerando prompt: {tipo.descricao()}")

        contexto = self._coletar_contexto(tipo)
        prompt = self._renderizar(tipo, contexto)

        self._exibir_prompt(prompt)

        if UI.confirmar("Salvar prompt em arquivo?", padrao=True):
            path = self._salvar(prompt, tipo)
            UI.sucesso(f"Prompt salvo em: {path.relative_to(self.fm.root)}")

        return prompt

    def gerar(self, tipo: TipoPrompt, contexto: dict) -> str:
        """
        Gera prompt programaticamente (útil para testes).

        Args:
            tipo: Tipo de prompt (TipoPrompt Enum).
            contexto: Dicionário com variáveis para o template.

        Returns:
            String com o prompt renderizado.
        """
        return self._renderizar(tipo, contexto)

    # ------------------------------------------------------------------ #
    # Seleção e coleta                                                     #
    # ------------------------------------------------------------------ #

    def _selecionar_tipo(self) -> TipoPrompt:
        """Exibe menu de tipos e retorna o Enum selecionado."""
        opcoes_menu = [(str(i + 1), t.descricao()) for i, t in enumerate(TipoPrompt)]
        UI.menu(opcoes_menu)

        while True:
            escolha = UI.perguntar("Tipo de prompt", padrao="1")
            try:
                idx = int(escolha) - 1
                tipos = list(TipoPrompt)
                if 0 <= idx < len(tipos):
                    return tipos[idx]
            except ValueError:
                pass
            UI.erro(f"Escolha entre 1 e {len(TipoPrompt)}.")

    def _coletar_contexto(self, tipo: TipoPrompt) -> dict:
        """Coleta variáveis necessárias para o tipo de prompt selecionado."""
        # Variáveis comuns a todos os tipos
        contexto: dict = {
            "curso": UI.perguntar("Nome do curso"),
            "tema": UI.perguntar("Tema específico"),
            "nivel": UI.selecionar("Nível", NivelDificuldade.opcoes()),
        }

        if tipo is TipoPrompt.CAPITULO:
            contexto["capitulo"] = UI.perguntar("Título do capítulo")
            contexto["objetivo"] = UI.perguntar("Objetivo do capítulo")
            contexto["palavras_minimas"] = UI.perguntar_numero(
                "Mínimo de palavras", padrao=1500, minimo=500, maximo=10000
            )

        elif tipo is TipoPrompt.EXERCICIOS:
            contexto["capitulo"] = UI.perguntar("Capítulo de referência")
            contexto["quantidade"] = UI.perguntar_numero(
                "Quantidade de exercícios", padrao=10, minimo=3, maximo=50
            )

        elif tipo is TipoPrompt.PROJETO:
            contexto["modulo"] = UI.perguntar("Nome do módulo")
            contexto["projeto"] = UI.perguntar("Nome do projeto")
            contexto["objetivo"] = UI.perguntar("Objetivo do projeto")
            contexto["tecnologias"] = UI.perguntar("Tecnologias (ex: Python, SQLite, Tkinter)")

        return contexto

    # ------------------------------------------------------------------ #
    # Renderização e output                                                #
    # ------------------------------------------------------------------ #

    def _renderizar(self, tipo: TipoPrompt, contexto: dict) -> str:
        """Renderiza o template de prompt com Jinja2."""
        return self._te_prompts.renderizar(tipo.template_filename(), contexto)

    def _exibir_prompt(self, prompt: str) -> None:
        """Exibe o prompt gerado em painel formatado no terminal."""
        console.print()
        console.print(Panel(
            prompt,
            title="[brand]Prompt Gerado[/brand]",
            border_style="cyan",
            padding=(1, 2),
        ))
        console.print()

    def _salvar(self, prompt: str, tipo: TipoPrompt) -> Path:
        """
        Salva o prompt em arquivo .txt em prompts_gerados/.

        Naming: YYYYMMDD_HHMMSS_<tipo>.txt
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = self.fm.path(DIR_PROMPTS_GERADOS)
        self.fm.criar_diretorio(output_dir)
        filename = f"{timestamp}_{tipo.value}.txt"
        path = output_dir / filename
        self.fm.escrever(path, prompt)
        logger.info("Prompt salvo: %s", path)
        return path
