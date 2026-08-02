# Prompt — Capítulo 10: Integração

> **Instruções de uso:**
> 1. Cole o conteúdo de `.ai/prompts/project-mode.md` no DeepSeek como primeira mensagem
> 2. Em seguida, cole este prompt

---

## Dados do Capítulo

| Campo | Valor |
|---|---|
| **Curso** | Python para Desktop |
| **Módulo** | 04 — Projeto Finalizador |
| **Capítulo** | 10 — Integração |
| **Arquivo de destino** | `10_integracao.md` |
| **Palavras mínimas** | 2000 |

## Objetivo

Conectar todas as telas e funcionalidades em um fluxo completo e coeso, testar todos os caminhos, adicionar polimento de UX e garantir que o sistema funciona sem erros do início ao fim.

## Contexto

- **Capítulo anterior:** 09 — Banco em Nuvem
- **O que foi feito:** Integração com banco em nuvem, sincronização, indicador online/offline, `.env` para credenciais
- **Estado do código:** Sistema completo mas com possíveis "pontas soltas". Login → Menu → Cadastro → CRUD → SQLite → Nuvem. Todas as funcionalidades existem individualmente. Falta: garantir que tudo funciona junto sem falhas.

## Competências a Desenvolver

- Testes de integração manuais
- Tratamento de exceções em pontos críticos
- UX: atalhos de teclado, barra de status, feedback consistente
- Fluxo completo: teste de ida e volta entre todas as telas
- Logging para debug
- Consistência visual entre telas

## Resultado Esperado

Ao final deste capítulo, o aluno terá:
- Todos os fluxos testados e funcionando sem erros
- Atalhos de teclado: Enter no login, Esc para sair, etc.
- Barra de status no rodapé com informações do sistema
- Mensagens de feedback padronizadas em todas as operações
- Try/except em todos os pontos críticos (banco, rede, entrada do usuário)
- Menu completo com todas as opções funcionais (nenhum botão "Em construção")

## Tópicos Obrigatórios

1. Roteiro de teste: listar todos os fluxos e testar cada um
2. Atalhos de teclado: `bind("<Return>")` no login, `bind("<Escape>")` para sair
3. Barra de status: Frame no rodapé com Label informativo
4. Padronizar messagebox: sucesso com ✅, erro com ❌, confirmação com ⚠️
5. Try/except em: conexão com banco, operações CRUD, sincronização com nuvem
6. Verificar transição entre todas as telas (ida e volta)
7. Verificar que dados persistem após fechar e reabrir
8. Adicionar ícone na janela principal (opcional)
9. Verificar que `.env` está no `.gitignore`

## Regras Especiais deste Capítulo

- Este capítulo é mais de "polimento" do que de "construção" — não adiciona funcionalidades novas, melhora as existentes
- Criar um roteiro de testes passo a passo para o aluno seguir
- A "Missão da Equipe" deve ser: seguir o roteiro de testes com o projeto da equipe, corrigir qualquer fluxo quebrado
- O "Desafio" deve ser: adicionar logging com o módulo `logging` do Python para registrar operações
- Nos erros comuns, destacar: esquecer de testar o fluxo completo, não tratar exceções de banco

## Próximo Capítulo

**Capítulo 11 — Refatoração:** O sistema funciona, mas o código pode estar desorganizado. Hora de limpar, documentar e preparar para entrega profissional.

---

**GERE O CAPÍTULO COMPLETO SEGUINDO TODAS AS REGRAS DO PROMPT MESTRE.**
