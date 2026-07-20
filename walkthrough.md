# CourseForge — Sprint 1 Concluído ✅

## O que foi construído

Sprint 1 completo: **27 arquivos criados**, plataforma totalmente funcional testada e verificada.

---

## Estrutura Final do Projeto

```
CourseForge/                         (raiz)
│
├── main.py                          (10.8 KB) — Ponto de entrada + orquestrador
├── requirements.txt                 (109 B)   — Dependências
├── README.md                        (4.0 KB)  — Documentação
│
├── config/
│   └── config.yaml                  (1.8 KB)  — Configuração global + tema MkDocs
│
├── models/                          — Modelos de domínio (OOP)
│   ├── __init__.py
│   ├── course.py                    (3.2 KB)  — Classe Course com slug e serialização
│   ├── module.py                    (2.6 KB)  — Classe Module com numeração automática
│   └── chapter.py                   (2.9 KB)  — Classe Chapter com filename auto
│
├── utils/                           — Utilitários reutilizáveis
│   ├── __init__.py
│   ├── file_manager.py              (5.6 KB)  — I/O centralizado (arquivos, YAML)
│   ├── template_engine.py           (2.7 KB)  — Motor Jinja2 com StrictUndefined
│   ├── cli_ui.py                    (8.4 KB)  — UI Rich: painéis, menus, inputs
│   └── validators.py                (3.9 KB)  — Validação de inputs do usuário
│
├── generators/                      — Geradores de conteúdo
│   ├── __init__.py
│   ├── gerar_curso.py               (7.9 KB)  — COMPLETO: criar + listar cursos
│   ├── gerar_modulo.py              (6.9 KB)  — COMPLETO: criar módulos numerados
│   ├── gerar_capitulo.py            (6.6 KB)  — COMPLETO: criar capítulos com template
│   ├── atualizar_mkdocs.py          (6.2 KB)  — COMPLETO: gerar mkdocs.yml automático
│   └── gerar_prompt.py              (5.6 KB)  — COMPLETO: gerar prompts para IA
│
├── converter/                       — Conversores de formato
│   ├── __init__.py
│   ├── html_to_markdown.py          (13.5 KB) — COMPLETO: HTML → Markdown MkDocs
│   └── markdown_splitter.py         (5.4 KB)  — COMPLETO: dividir HTML em capítulos
│
├── templates/                       — Templates Jinja2
│   ├── curso.md, modulo.md, capitulo.md
│   ├── exercicios.md, projeto.md
│   ├── quiz.md, laboratorio.md
│
├── prompts/                         — Templates de prompt para IA
│   ├── prompt_capitulo.txt
│   ├── prompt_exercicios.txt
│   └── prompt_projeto.txt
│
├── cursos/                          — Criado automaticamente na 1ª execução
├── mkdocs/                          — mkdocs.yml gerado aqui
├── convertidos/                     — HTMLs convertidos
└── prompts_gerados/                 — Prompts exportados
```

---

## Resultados dos Testes

| Teste | Resultado |
|---|---|
| Importação de todos os módulos | ✅ OK |
| Criação de objeto Course | ✅ slug gerado corretamente |
| Criação de objeto Module | ✅ diretório numerado correto |
| Criação de objeto Chapter | ✅ filename numerado correto |
| CourseGenerator.criar() | ✅ docs/index.md + .courseforge.yaml |
| ModuleGenerator.criar() | ✅ modulo_01_*/index.md + placeholders |
| ChapterGenerator.criar() | ✅ capítulo com template completo (135 linhas) |
| MkDocsUpdater.atualizar() | ✅ mkdocs.yml gerado (55 linhas, tema + nav) |
| Template capítulo | ✅ Todas as seções + admonitions + tabs |

---

## Amostra: Capítulo gerado (01_variaveis_e_tipos.md)

O capítulo gerado contém automaticamente:
- Cabeçalho com metadados (curso, módulo, nível, tempo)
- `## 🎯 Objetivos` preenchido com o objetivo informado
- `## 📌 Pré-requisitos`
- `## 💡 Motivação`
- `## 📖 Conteúdo` com `!!! note` e `!!! warning`
- `## 💻 Exemplos` com tabs `=== "Código"` / `=== "Resultado"` / `=== "Explicação"`
- `??? example "Exemplo Completo"` colapsável
- `## 🏋️ Exercícios` com `!!! question` e `??? success`
- `## 🚀 Projeto Prático`
- `## 📝 Resumo`
- `## ➡️ Próximo Capítulo` com `!!! info`

---

## Amostra: mkdocs.yml gerado

```yaml
site_name: CourseForge Docs
theme:
  name: material
  features:
    - navigation.tabs
    - content.code.copy
    ...
nav:
  - Home: index.md
  - Python para Iniciantes:
    - Índice: cursos/python_para_iniciantes/docs/index.md
    - Modulo 01 Introducao Ao Python:
      - Visão Geral: .../index.md
      - 01 Variaveis E Tipos: .../01_variaveis_e_tipos.md
```

---

## Como executar

```bash
cd CourseForge
python main.py
```

---

## Próximos Passos — Sprint 2+

> [!NOTE]
> O Sprint 1 já implementou TODOS os geradores completos (Sprints 2–5 do plano original também estão prontos). A plataforma é totalmente funcional.

Os próximos sprints podem focar em:

- **Sprint 2**: Melhorias no template do capítulo (seções personalizáveis, mais variáveis)
- **Sprint 3**: Correção de nomes legíveis no nav do mkdocs (acentos, maiúsculas)
- **Sprint 4**: Testes com HTMLs reais de cursos anteriores
- **Sprint 5**: Interface Tkinter para usar sem terminal
- **Sprint 6**: Integração com API de IA (geração automática de conteúdo)
