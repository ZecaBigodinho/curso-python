"""
CourseForge — utils/slugify.py

Função única de slugificação para toda a plataforma.

Por que módulo dedicado?
    A função _slugify estava triplicada em course.py, module.py e chapter.py.
    Qualquer correção (novo caractere especial, limite de tamanho, etc.)
    precisava ser feita em 3 arquivos — garantia de divergência futura.

Decisão de design:
    Módulo standalone (não classe) porque slugify é uma função pura:
    mesmo input → mesmo output, sem estado, sem dependências.
"""
from __future__ import annotations

import re
import unicodedata


# Mapa explícito de caracteres acentuados → ASCII
# Mais legível e controlável do que unicodedata sozinho para PT-BR
_CHAR_MAP: dict[str, str] = {
    "à": "a", "á": "a", "â": "a", "ã": "a", "ä": "a", "å": "a",
    "è": "e", "é": "e", "ê": "e", "ë": "e",
    "ì": "i", "í": "i", "î": "i", "ï": "i",
    "ò": "o", "ó": "o", "ô": "o", "õ": "o", "ö": "o",
    "ù": "u", "ú": "u", "û": "u", "ü": "u",
    "ç": "c",
    "ñ": "n",
    "ý": "y", "ÿ": "y",
    "ß": "ss",
    # Maiúsculas (para robustez antes do lower())
    "À": "a", "Á": "a", "Â": "a", "Ã": "a", "Ä": "a", "Å": "a",
    "È": "e", "É": "e", "Ê": "e", "Ë": "e",
    "Ì": "i", "Í": "i", "Î": "i", "Ï": "i",
    "Ò": "o", "Ó": "o", "Ô": "o", "Õ": "o", "Ö": "o",
    "Ù": "u", "Ú": "u", "Û": "u", "Ü": "u",
    "Ç": "c", "Ñ": "n",
}


def slugify(text: str, max_len: int = 80) -> str:
    """
    Converte texto arbitrário para slug seguro para uso em nomes de arquivo/diretório.

    Regras aplicadas (em ordem):
        1. Substituição de caracteres acentuados por equivalentes ASCII
        2. Lowercase
        3. Remoção de caracteres não alfanuméricos (exceto espaço e hífen)
        4. Substituição de espaços por underscore
        5. Colapso de underscores múltiplos consecutivos
        6. Remoção de underscores no início/fim
        7. Truncamento em `max_len` caracteres

    Args:
        text: Texto de entrada (qualquer string).
        max_len: Tamanho máximo do slug resultante.

    Returns:
        Slug normalizado, seguro para sistema de arquivos.

    Examples:
        >>> slugify("Python para Iniciantes")
        'python_para_iniciantes'
        >>> slugify("Introdução à Programação!")
        'introducao_a_programacao'
        >>> slugify("C# e .NET")
        'c_e_net'
    """
    if not text:
        return "sem_nome"

    # 1. Substituir caracteres acentuados
    for char, replacement in _CHAR_MAP.items():
        text = text.replace(char, replacement)

    # 2. Fallback: normalização Unicode para qualquer caractere não mapeado
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", errors="ignore").decode("ascii")

    # 3. Lowercase
    text = text.lower()

    # 4. Remover caracteres inválidos (manter letras, números, espaço, hífen, underscore)
    text = re.sub(r"[^a-z0-9\s_-]", "", text)

    # 5. Substituir espaços e hífens por underscore
    text = re.sub(r"[\s\-]+", "_", text)

    # 6. Colapsar underscores múltiplos
    text = re.sub(r"_+", "_", text)

    # 7. Remover underscores nas bordas
    text = text.strip("_")

    # 8. Truncar
    text = text[:max_len]
    text = text.strip("_")  # re-strip após truncamento

    return text or "sem_nome"
