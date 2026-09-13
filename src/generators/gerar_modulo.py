"""
CourseForge — generators/gerar_modulo.py

Responsável por criar módulos dentro de um curso.

Fluxo:
  1. Usuário seleciona o curso (via selectors.py)
  2. Detectar próximo número disponível automaticamente
  3. Coletar nome, descrição e quantidade de capítulos
  4. Criar diretório numerado e index.md do módulo
  5. Criar arquivos placeholder para cada capítulo planejado
"""
from __future__ import annotations

from pathlib import Path

from models.module import Module
from utils.file_manager import FileManager
from utils.template_engine import TemplateEngine
from utils.cli_ui import UI
from utils.validators import validate_nome, validate_descricao, validate_numero
from utils.selectors import selecionar_curso
from utils.constants import (
    TEMPLATE_MODULO, MODULE_DIR_PREFIX, DIR_CURSOS,
    CAPITULOS_MIN, CAPITULOS_MAX,
)
from utils.logger import get_logger

logger = get_logger(__name__)

# Placeholder de capítulo como constante — evita string hardcoded no loop
_PLACEHOLDER_CAPITULO = (
    "# Capítulo {numero:02d}\n\n"
    "> *Use o menu **Criar Capítulo** (opção 3) para gerar o conteúdo completo deste capítulo.*\n"
)


class ModuleGenerator:
    """
    Gera módulos dentro de cursos existentes na plataforma.

    Responsabilidades:
    - Detectar cursos disponíveis (via selectors)
    - Numerar módulo automaticamente
    - Criar diretório modulo_NN_<slug>/
    - Criar index.md a partir do template
    - Criar arquivos placeholder para capítulos planejados
    """

    def __init__(self, fm: FileManager, template_engine: TemplateEngine) -> None:
        """
        Args:
            fm: Gerenciador de arquivos da plataforma.
            template_engine: Motor de renderização Jinja2.
        """
        self.fm = fm
        self.te = template_engine

    # ------------------------------------------------------------------ #
    # Interface pública                                                    #
    # ------------------------------------------------------------------ #

    def criar_interativo(self) -> Module | None:
        """Coleta dados via CLI e cria o módulo."""
        UI.secao("CRIAR NOVO MÓDULO")

        curso_slug = selecionar_curso(self.fm)
        if not curso_slug:
            return None

        numero = self._detectar_proximo_numero(curso_slug)
        UI.info(f"Próximo número de módulo disponível: {numero:02d}")

        nome = self._pedir_nome()
        descricao = self._pedir_descricao()
        num_capitulos = self._pedir_num_capitulos()

        meta_curso = self.fm.ler_metadados_curso(self.fm.path(DIR_CURSOS) / curso_slug)

        module = Module(
            nome=nome,
            curso_slug=curso_slug,
            numero=numero,
            descricao=descricao,
            num_capitulos=num_capitulos,
        )

        logger.info("Criando módulo: %s", module.diretorio)
        UI.info(f"Criando módulo: {module.diretorio}")
        self.criar(module, meta_curso)

        UI.sucesso(f"Módulo '{module.nome}' criado com sucesso!")
        self._exibir_resumo(module)
        return module

    def criar(self, module: Module, meta_curso: dict | None = None) -> Path:
        """
        Cria módulo a partir de objeto (uso programático).

        Args:
            module: Objeto Module construído e validado.
            meta_curso: Metadados do curso pai (para o template).

        Returns:
            Path do diretório do módulo criado.
        """
        return self._criar_estrutura(module, meta_curso or {})

    # ------------------------------------------------------------------ #
    # Coleta de dados                                                      #
    # ------------------------------------------------------------------ #

    def _detectar_proximo_numero(self, curso_slug: str) -> int:
        """Detecta o próximo número sequencial de módulo disponível no curso."""
        curso_dir = self.fm.path(DIR_CURSOS) / curso_slug
        modulos = [
            p for p in self.fm.listar_subdiretorios(curso_dir)
            if p.name.startswith(MODULE_DIR_PREFIX)
        ]
        return len(modulos) + 1

    def _pedir_nome(self) -> str:
        while True:
            try:
                return validate_nome(UI.perguntar("Nome do módulo"), "Nome do módulo")
            except ValueError as e:
                UI.erro(str(e))

    def _pedir_descricao(self) -> str:
        return validate_descricao(UI.perguntar("Descrição do módulo (opcional)", padrao=""))

    def _pedir_num_capitulos(self) -> int:
        while True:
            try:
                valor = UI.perguntar_numero(
                    "Quantidade de capítulos planejados",
                    padrao=1,
                    minimo=CAPITULOS_MIN,
                    maximo=CAPITULOS_MAX,
                )
                return validate_numero(valor, "Quantidade de capítulos", CAPITULOS_MIN, CAPITULOS_MAX)
            except ValueError as e:
                UI.erro(str(e))

    # ------------------------------------------------------------------ #
    # Criação de estrutura                                                 #
    # ------------------------------------------------------------------ #

    def _criar_estrutura(self, module: Module, meta_curso: dict) -> Path:
        """
        Cria o diretório do módulo e arquivos iniciais.

        Estrutura gerada:
          cursos/<curso_slug>/<modulo_dir>/
            index.md           ← visão geral do módulo
            01_capitulo.md     ← placeholder por capítulo planejado
        """
        curso_dir = self.fm.path(DIR_CURSOS) / module.curso_slug
        modulo_dir = curso_dir / module.diretorio

        if modulo_dir.exists():
            raise FileExistsError(
                f"Módulo '{module.diretorio}' já existe em '{modulo_dir}'."
            )

        self.fm.criar_diretorio(modulo_dir)

        # Renderizar index.md do módulo
        contexto = {
            **module.to_dict(),
            "curso_nome": meta_curso.get("nome", module.curso_slug) if meta_curso else module.curso_slug,
            "total_modulos": meta_curso.get("num_modulos", "?") if meta_curso else "?",
        }
        conteudo = self.te.renderizar(TEMPLATE_MODULO, contexto)
        index_path = modulo_dir / "index.md"
        self.fm.escrever(index_path, conteudo)
        UI.muted(f"  [+] {index_path.relative_to(self.fm.root)}")

        # Criar placeholders para cada capítulo planejado
        for i in range(1, module.num_capitulos + 1):
            cap_path = modulo_dir / f"{i:02d}_capitulo.md"
            placeholder = _PLACEHOLDER_CAPITULO.format(numero=i)
            self.fm.escrever(cap_path, placeholder)
            UI.muted(f"  [+] {cap_path.relative_to(self.fm.root)}")

        logger.info("Módulo criado em: %s", modulo_dir)
        return modulo_dir

    # ------------------------------------------------------------------ #
    # Exibição                                                             #
    # ------------------------------------------------------------------ #

    def _exibir_resumo(self, module: Module) -> None:
        """Exibe tabela resumida com os dados do módulo criado."""
        UI.tabela(
            titulo="Módulo Criado",
            colunas=["Campo", "Valor"],
            linhas=[
                ["Nome", module.nome],
                ["Diretório", module.diretorio],
                ["Curso", module.curso_slug],
                ["Número", str(module.numero)],
                ["Capítulos planejados", str(module.num_capitulos)],
            ],
        )
