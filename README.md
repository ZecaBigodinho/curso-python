# CourseForge

Plataforma em Python para organizar e gerar conteúdo de cursos em Markdown com publicação via MkDocs.

## Requisitos

- Python 3.10+
- pip

## Instalação

```bash
python -m venv venv
# Windows
.\venv\Scripts\activate

pip install -r requirements.txt
pip install mkdocs-material
```

## Uso

### Menu interativo

```bash
python main.py
```

### Fluxo de publicação (build com validação strict)

```bash
python main.py publicar
```

### Pré-visualização local do site

```bash
python -m mkdocs serve -f mkdocs/mkdocs.yml
```

## Publicação no GitHub Pages

```bash
python -m mkdocs gh-deploy -f mkdocs/mkdocs.yml --force
```

URL padrão:

`https://<seu-usuario>.github.io/<seu-repositorio>/`

## Estrutura principal

- `main.py`: ponto de entrada da CLI
- `generators/`: geração de curso, módulo, capítulo e prompts
- `models/`: entidades de domínio
- `templates/`: templates Markdown
- `cursos/`: conteúdo dos cursos
- `mkdocs/mkdocs.yml`: configuração do site
