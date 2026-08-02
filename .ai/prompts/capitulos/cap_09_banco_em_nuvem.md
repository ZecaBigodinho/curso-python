# Prompt — Capítulo 09: Banco em Nuvem

> **Instruções de uso:**
> 1. Cole o conteúdo de `.ai/prompts/project-mode.md` no DeepSeek como primeira mensagem
> 2. Em seguida, cole este prompt

---

## Dados do Capítulo

| Campo | Valor |
|---|---|
| **Curso** | Python para Desktop |
| **Módulo** | 04 — Projeto Finalizador |
| **Capítulo** | 09 — Banco em Nuvem |
| **Arquivo de destino** | `09_banco_em_nuvem.md` |
| **Palavras mínimas** | 2500 |

## Objetivo

Integrar o sistema a um banco de dados em nuvem para permitir sincronização dos dados e acesso remoto, mantendo o SQLite como fallback local.

## Contexto

- **Capítulo anterior:** 08 — CRUD
- **O que foi feito:** CRUD completo implementado — inserir, consultar, atualizar, excluir alunos no SQLite. Busca por nome, seleção no Treeview, confirmação de exclusão.
- **Estado do código:** Todos os arquivos anteriores. `database/operacoes.py` com funções CRUD. Sistema 100% funcional localmente. Falta: acesso remoto e sincronização.

## Competências a Desenvolver

- Conceito de banco local vs banco em nuvem
- Configuração de serviço de banco em nuvem
- Variáveis de ambiente com `python-dotenv`
- Arquivo `.env` para credenciais
- Funções de sincronização (local → nuvem)
- Tratamento de erros de rede
- Fallback para modo offline

## Resultado Esperado

Ao final deste capítulo, o aluno terá:
- Integração com um serviço de banco em nuvem configurado
- Arquivo `.env` com credenciais (nunca hardcoded)
- Funções de sincronização: enviar dados para nuvem, baixar dados da nuvem
- Botão "Sincronizar" na interface
- Indicador de status: online/offline
- Sistema funciona offline com SQLite e sincroniza quando tem internet
- `.gitignore` atualizado para não versionar `.env`

## Tópicos Obrigatórios

1. Diferença entre banco local (SQLite) e banco em nuvem
2. Quando usar cada um e por que usar os dois
3. Configuração do serviço de nuvem (passo a passo com screenshots textuais)
4. Instalação da biblioteca necessária
5. Arquivo `.env` para credenciais — nunca hardcodar
6. `python-dotenv` para carregar variáveis de ambiente
7. Funções de sincronização em `database/conexao.py` ou novo módulo `database/nuvem.py`
8. Botão "Sincronizar" na tela de cadastro ou no menu
9. Indicador visual de conexão (Label com cor verde/vermelha)
10. Try/except para erros de rede
11. `.gitignore` — adicionar `.env` e `escola.db`

## Regras Especiais deste Capítulo

- O SQLite continua sendo o banco principal (operações são feitas localmente)
- A nuvem é usada para backup e sincronização
- O sistema deve funcionar 100% offline — a nuvem é um bônus
- Explicar conceito de "offline first"
- Usar `.env` para todas as credenciais
- A "Missão da Equipe" deve ser: configurar o banco em nuvem para o projeto da equipe e implementar sincronização básica
- O "Desafio" deve ser: implementar sincronização automática (ao salvar/editar/excluir, sincroniza automaticamente se online)
- Nos erros comuns, destacar: credenciais expostas no código, falha de conexão sem try/except

## Próximo Capítulo

**Capítulo 10 — Integração:** Todas as peças existem. Agora vamos conectar tudo em um fluxo perfeito, sem falhas.

---

**GERE O CAPÍTULO COMPLETO SEGUINDO TODAS AS REGRAS DO PROMPT MESTRE.**
