# Prompt — Capítulo 11: Refatoração

> **Instruções de uso:**
> 1. Cole o conteúdo de `.ai/prompts/project-mode.md` no DeepSeek como primeira mensagem
> 2. Em seguida, cole este prompt

---

## Dados do Capítulo

| Campo | Valor |
|---|---|
| **Curso** | Python para Desktop |
| **Módulo** | 04 — Projeto Finalizador |
| **Capítulo** | 11 — Refatoração |
| **Arquivo de destino** | `11_refatoracao.md` |
| **Palavras mínimas** | 2000 |

## Objetivo

Reorganizar o código do sistema seguindo boas práticas profissionais, eliminar duplicações, adicionar documentação, docstrings e preparar o projeto para entrega.

## Contexto

- **Capítulo anterior:** 10 — Integração
- **O que foi feito:** Todos os fluxos testados e integrados. Atalhos de teclado, barra de status, exceções tratadas, feedback padronizado. Sistema funcional do início ao fim.
- **Estado do código:** Sistema 100% funcional mas possivelmente com código duplicado, funções longas demais, falta de documentação, e prints de debug esquecidos.

## Competências a Desenvolver

- Refatoração de código
- Princípio DRY (Don't Repeat Yourself)
- Docstrings em Python
- PEP 8 — estilo de código
- README.md para projetos
- requirements.txt
- Revisão de código (code review)
- Remoção de código morto

## Resultado Esperado

Ao final deste capítulo, o aluno terá:
- Código limpo sem duplicações
- Docstrings em todas as funções
- Nomes de variáveis e funções revisados
- `README.md` do projeto com descrição, como executar, tecnologias usadas
- `requirements.txt` com todas as dependências
- Sem prints de debug ou código comentado desnecessário
- Código formatado seguindo PEP 8

## Tópicos Obrigatórios

1. O que é refatoração e por que é importante
2. Como identificar código duplicado (mostrar exemplos do próprio projeto)
3. Extrair funções: código repetido → função reutilizável
4. Docstrings: o que são, formato, onde colocar
5. Revisar nomes: variáveis de uma letra → nomes descritivos
6. Criar `README.md` do projeto do aluno:
   - Nome do projeto
   - Descrição
   - Tecnologias utilizadas
   - Como instalar e executar
   - Funcionalidades
   - Autores (membros da equipe)
7. Criar `requirements.txt` com `pip freeze` ou manualmente
8. Verificar PEP 8: indentação, espaços, linhas em branco
9. Remover prints de debug e código morto
10. Verificação final: o sistema ainda funciona após refatoração?

## Regras Especiais deste Capítulo

- Mostrar exemplos de "antes e depois" da refatoração usando blocos de código comparativos
- Enfatizar: refatorar NÃO muda o comportamento — só melhora a organização
- Testar após cada refatoração (não acumular mudanças sem testar)
- A "Missão da Equipe" deve ser: refatorar o código do projeto da equipe, adicionar docstrings, criar README.md
- O "Desafio" deve ser: usar `pylint` ou `flake8` para verificar automaticamente o estilo do código
- Nos erros comuns, destacar: refatorar sem testar, renomear variáveis e esquecer de atualizar as referências

## Próximo Capítulo

**Capítulo 12 — Projeto Final:** O sistema está pronto, limpo e documentado. É hora de entregar, apresentar e celebrar!

---

**GERE O CAPÍTULO COMPLETO SEGUINDO TODAS AS REGRAS DO PROMPT MESTRE.**
