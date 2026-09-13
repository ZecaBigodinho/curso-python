"""
CourseForge — utils/cli_ui.py

Interface visual de terminal da plataforma CourseForge.
Centraliza todos os componentes visuais usando Rich.

Decisão de design:
    A configuração de encoding UTF-8 NÃO é feita aqui.
    Ela é feita em main.py antes de qualquer import, para não
    afetar módulos que não são de UI (testes, API futura).

Responsabilidades:
    - Banner e cabeçalhos
    - Menus interativos
    - Mensagens de status (sucesso, erro, aviso, info)
    - Formulários de entrada de dados
    - Tabelas formatadas
    - Barras de progresso (via Rich Progress)
"""
from __future__ import annotations

from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.rule import Rule
from rich.table import Table
from rich.theme import Theme


# ------------------------------------------------------------------ #
# Tema de cores da plataforma                                         #
# ------------------------------------------------------------------ #
_THEME = Theme(
    {
        "brand": "bold cyan",
        "success": "bold green",
        "error": "bold red",
        "warning": "bold yellow",
        "info": "bold blue",
        "muted": "dim white",
        "highlight": "bold magenta",
    }
)

# Console global — instância única compartilhada pelo projeto
console = Console(theme=_THEME, highlight=False)


class UI:
    """
    Interface visual de terminal para o CourseForge.

    Todos os métodos são estáticos — a classe é usada como namespace,
    não como objeto. Isso mantém o uso simples: UI.sucesso("mensagem").

    Componentes disponíveis:
    - Banner e seções: banner(), secao(), titulo_menu()
    - Mensagens: sucesso(), erro(), aviso(), info(), muted()
    - Menus: menu()
    - Inputs: perguntar(), perguntar_numero(), confirmar(), selecionar()
    - Tabelas: tabela()
    - Controle: aguardar_enter()
    """

    # ------------------------------------------------------------------ #
    # Banner / Cabeçalho                                                   #
    # ------------------------------------------------------------------ #

    @staticmethod
    def banner() -> None:
        """Exibe o banner principal da plataforma."""
        console.print()
        console.print(
            Panel(
                "[brand]"
                "  CourseForge\n"
                "  Plataforma de Cursos MkDocs Material"
                "[/brand]",
                border_style="cyan",
                padding=(1, 4),
                expand=False,
            )
        )
        console.print()

    @staticmethod
    def secao(titulo: str) -> None:
        """Exibe um separador de seção com título."""
        console.print()
        console.print(Rule(f"[brand]{titulo}[/brand]", style="cyan"))
        console.print()

    @staticmethod
    def titulo_menu(titulo: str) -> None:
        """Exibe o título de um menu com destaque."""
        console.print(
            Panel(
                f"[brand]{titulo}[/brand]",
                border_style="cyan",
                expand=False,
            )
        )

    # ------------------------------------------------------------------ #
    # Mensagens de Status                                                  #
    # ------------------------------------------------------------------ #

    @staticmethod
    def sucesso(mensagem: str) -> None:
        """Exibe mensagem de sucesso."""
        console.print(f"[success][OK] {mensagem}[/success]")

    @staticmethod
    def erro(mensagem: str) -> None:
        """Exibe mensagem de erro."""
        console.print(f"[error][ERRO] {mensagem}[/error]")

    @staticmethod
    def aviso(mensagem: str) -> None:
        """Exibe mensagem de aviso."""
        console.print(f"[warning][AVISO] {mensagem}[/warning]")

    @staticmethod
    def info(mensagem: str) -> None:
        """Exibe mensagem informativa."""
        console.print(f"[info][INFO] {mensagem}[/info]")

    @staticmethod
    def muted(mensagem: str) -> None:
        """Exibe mensagem discreta (para log de operações)."""
        console.print(f"[muted]{mensagem}[/muted]")

    # ------------------------------------------------------------------ #
    # Menus                                                                #
    # ------------------------------------------------------------------ #

    @staticmethod
    def menu(opcoes: list[tuple[str, str]]) -> None:
        """
        Exibe um menu numerado com descrições.

        Args:
            opcoes: Lista de tuplas (numero_como_string, descricao).
        """
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("num", style="brand", justify="right", width=4)
        table.add_column("desc", style="white")

        for num, desc in opcoes:
            table.add_row(f"[{num}]", desc)

        console.print(table)
        console.print()

    # ------------------------------------------------------------------ #
    # Formulários / Inputs                                                 #
    # ------------------------------------------------------------------ #

    @staticmethod
    def perguntar(pergunta: str, padrao: str = "") -> str:
        """
        Solicita entrada de texto ao usuário.

        Args:
            pergunta: Texto da pergunta.
            padrao: Valor padrão (usado se usuário pressionar Enter vazio).

        Returns:
            Texto digitado (ou padrão se vazio).
        """
        return Prompt.ask(f"[brand]?[/brand] {pergunta}", default=padrao or None)

    @staticmethod
    def perguntar_numero(
        pergunta: str,
        padrao: int = 1,
        minimo: int = 1,
        maximo: int = 100,
    ) -> int:
        """
        Solicita número inteiro com validação de range.

        Args:
            pergunta: Texto da pergunta.
            padrao: Valor padrão.
            minimo: Valor mínimo aceito (inclusivo).
            maximo: Valor máximo aceito (inclusivo).

        Returns:
            Inteiro validado.
        """
        while True:
            valor = IntPrompt.ask(f"[brand]?[/brand] {pergunta}", default=padrao)
            if minimo <= valor <= maximo:
                return valor
            UI.aviso(f"Informe um número entre {minimo} e {maximo}.")

    @staticmethod
    def confirmar(pergunta: str, padrao: bool = True) -> bool:
        """
        Solicita confirmação S/N.

        Args:
            pergunta: Texto da pergunta.
            padrao: Resposta padrão se Enter for pressionado.

        Returns:
            True para sim, False para não.
        """
        return Confirm.ask(f"[brand]?[/brand] {pergunta}", default=padrao)

    @staticmethod
    def selecionar(pergunta: str, opcoes: list[str]) -> str:
        """
        Exibe lista numerada e solicita seleção por índice.

        Args:
            pergunta: Texto da pergunta.
            opcoes: Lista de strings para exibição e seleção.

        Returns:
            A string da opção selecionada.
        """
        console.print(f"\n[brand]?[/brand] {pergunta}")
        for i, op in enumerate(opcoes, 1):
            console.print(f"  [brand][{i}][/brand] {op}")
        console.print()

        while True:
            idx = IntPrompt.ask("  Escolha o numero", default=1)
            if 1 <= idx <= len(opcoes):
                return opcoes[idx - 1]
            UI.aviso(f"Escolha entre 1 e {len(opcoes)}.")

    # ------------------------------------------------------------------ #
    # Tabelas                                                              #
    # ------------------------------------------------------------------ #

    @staticmethod
    def tabela(titulo: str, colunas: list[str], linhas: list[list[Any]]) -> None:
        """
        Exibe uma tabela formatada com Rich.

        Args:
            titulo: Título da tabela.
            colunas: Nomes das colunas.
            linhas: Dados das linhas (cada item é uma lista de valores).
        """
        table = Table(title=titulo, border_style="cyan")
        for col in colunas:
            table.add_column(col, style="white")
        for linha in linhas:
            table.add_row(*[str(v) for v in linha])
        console.print(table)

    # ------------------------------------------------------------------ #
    # Progresso                                                            #
    # ------------------------------------------------------------------ #

    @staticmethod
    def progresso_spinner(mensagem: str) -> Progress:
        """
        Retorna um contexto de progresso com spinner.

        Uso:
            with UI.progresso_spinner("Processando...") as p:
                tarefa = p.add_task("", total=None)
                # ... operação longa ...

        Args:
            mensagem: Texto exibido ao lado do spinner.

        Returns:
            Objeto Progress configurado para uso como context manager.
        """
        return Progress(
            SpinnerColumn(),
            TextColumn(f"[info]{mensagem}[/info]"),
            console=console,
        )

    # ------------------------------------------------------------------ #
    # Controle de fluxo                                                    #
    # ------------------------------------------------------------------ #

    @staticmethod
    def aguardar_enter(mensagem: str = "Pressione Enter para continuar...") -> None:
        """Pausa a execução até o usuário pressionar Enter."""
        console.print(f"\n[muted]{mensagem}[/muted]")
        input()
