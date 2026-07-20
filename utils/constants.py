"""
CourseForge — utils/constants.py

Constantes globais da plataforma.

Por que centralizar aqui?
    Magic strings espalhadas pelo código (ex: ".courseforge.yaml", "modulo_",
    "cursos") são fontes de bugs silenciosos: uma digitação errada ou
    uma renomeação parcial pode fazer o sistema falhar em locais inesperados.

    Aqui definimos ONE SOURCE OF TRUTH para todos os valores fixos do sistema.

Regra de uso:
    Nunca use strings literais para nomes de arquivo, prefixos de diretório
    ou configurações de sistema diretamente no código.
    Sempre importe desta constante.
"""
from __future__ import annotations

# ------------------------------------------------------------------ #
# Nomes de arquivo e diretório                                        #
# ------------------------------------------------------------------ #

#: Nome do arquivo de metadados dentro de cada diretório de curso
METADATA_FILENAME: str = ".courseforge.yaml"

#: Prefixo usado em diretórios de módulo
MODULE_DIR_PREFIX: str = "modulo_"

#: Nome do arquivo índice raiz de cada entidade
INDEX_FILENAME: str = "index.md"

#: Nome do arquivo de configuração MkDocs gerado
MKDOCS_FILENAME: str = "mkdocs.yml"

# ------------------------------------------------------------------ #
# Nomes de diretórios da plataforma (relativos à raiz)               #
# ------------------------------------------------------------------ #

#: Diretório raiz de todos os cursos gerados
DIR_CURSOS: str = "cursos"

#: Diretório de output do mkdocs.yml
DIR_MKDOCS: str = "mkdocs"

#: Diretório de arquivos HTML convertidos
DIR_CONVERTIDOS: str = "convertidos"

#: Diretório de prompts exportados
DIR_PROMPTS_GERADOS: str = "prompts_gerados"

#: Diretório de templates Jinja2
DIR_TEMPLATES: str = "templates"

#: Diretório de templates de prompt para IA
DIR_PROMPTS: str = "prompts"

#: Subdiretório de docs dentro de cada curso
CURSO_DOCS_SUBDIR: str = "docs"

# ------------------------------------------------------------------ #
# Nomes de templates                                                  #
# ------------------------------------------------------------------ #

TEMPLATE_CURSO: str = "curso.md"
TEMPLATE_MODULO: str = "modulo.md"
TEMPLATE_CAPITULO: str = "capitulo.md"
TEMPLATE_EXERCICIOS: str = "exercicios.md"
TEMPLATE_PROJETO: str = "projeto.md"
TEMPLATE_QUIZ: str = "quiz.md"
TEMPLATE_LABORATORIO: str = "laboratorio.md"
TEMPLATE_PLACEHOLDER_CAPITULO: str = "placeholder_capitulo.md"

# ------------------------------------------------------------------ #
# Nomes de templates de prompt                                        #
# ------------------------------------------------------------------ #

PROMPT_CAPITULO: str = "prompt_capitulo.txt"
PROMPT_EXERCICIOS: str = "prompt_exercicios.txt"
PROMPT_PROJETO: str = "prompt_projeto.txt"

# ------------------------------------------------------------------ #
# Limites de validação                                                #
# ------------------------------------------------------------------ #

NOME_MIN_LEN: int = 2
NOME_MAX_LEN: int = 100
AUTOR_MIN_LEN: int = 2
AUTOR_MAX_LEN: int = 80
MODULOS_MIN: int = 1
MODULOS_MAX: int = 50
CAPITULOS_MIN: int = 1
CAPITULOS_MAX: int = 50
PALAVRAS_MIN: int = 500
PALAVRAS_MAX: int = 10_000
PALAVRAS_DEFAULT: int = 1_500

# ------------------------------------------------------------------ #
# Versão da plataforma                                                #
# ------------------------------------------------------------------ #

PLATFORM_VERSION: str = "1.0.0"
PLATFORM_NAME: str = "CourseForge"
