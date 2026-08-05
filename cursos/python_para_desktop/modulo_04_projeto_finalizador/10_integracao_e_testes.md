# 10 — Integração

## 🎯 Objetivo

Neste capítulo você vai polir e integrar todas as peças do Sistema Escolar, garantindo que o fluxo completo funcione sem falhas e oferecendo uma experiência de usuário profissional.

Ao final, você terá:

- Todos os fluxos testados (Login → Menu → Cadastro → CRUD → Sincronização)
- Atalhos de teclado: Enter para login, Esc para sair de janelas
- Uma barra de status informativa no rodapé da janela principal
- Mensagens de feedback padronizadas (✅ sucesso, ❌ erro, ⚠️ confirmação)
- Tratamento de exceções em todos os pontos críticos
- Um roteiro de testes completo para validar o sistema

## 📍 Contextualização

No Capítulo 09, você conectou o sistema ao Firebase, implementou sincronização e protegeu credenciais com `.env`. O sistema agora tem todas as funcionalidades previstas: Login, Menu, Cadastro, CRUD, SQLite e Nuvem.

Mas um sistema funcional não é necessariamente um sistema robusto. Pequenas arestas podem comprometer a experiência: um botão que não responde ao Enter, uma mensagem de erro genérica, uma janela que não fecha com Esc, a ausência de um indicador do que está acontecendo.

Este capítulo é sobre acabamento. Você não construirá novas funcionalidades — você tornará as existentes mais profissionais. É a diferença entre um protótipo e um produto.

**Progresso do Sistema:**

```text
✅ Capítulo 01 — Introdução e Planejamento
✅ Capítulo 02 — Arquitetura do Sistema
✅ Capítulo 03 — Tela de Login
✅ Capítulo 04 — Menu Principal
✅ Capítulo 05 — Múltiplas Janelas
✅ Capítulo 06 — Cadastro de Alunos
✅ Capítulo 07 — SQLite
✅ Capítulo 08 — CRUD Completo
✅ Capítulo 09 — Banco em Nuvem
🔨 Integração ← VOCÊ ESTÁ AQUI
⬜ Refatoração e Entrega
```

## ✅ Resultado Esperado

Após este capítulo, o sistema se comportará como um software comercial:

- Ao pressionar Enter no campo de senha, o login é acionado
- Ao pressionar Esc em qualquer janela secundária, ela se fecha
- No rodapé da tela de cadastro, uma barra de status mostra a quantidade de registros e o status da conexão
- Todas as mensagens seguem um padrão visual consistente
- Erros inesperados (banco corrompido, falha de rede) são capturados e exibem mensagens amigáveis
- O fluxo completo foi testado e nenhum caminho quebra o sistema

Arquivos modificados:

| Arquivo | Modificação |
|---|---|
| `main.py` | Atalho Escape na janela principal |
| `views/login.py` | Atalho Enter no campo de senha (já existe), padronização de mensagens |
| `views/menu.py` | Atalho Escape para sair, ícones nos botões |
| `views/cadastro.py` | Barra de status, atalho Escape, try/except em todas as operações, padronização de mensagens |
| `controllers/auth.py` | Try/except na validação de login |
| `controllers/aluno.py` | Try/except em todas as operações de banco |

## 💻 Implementação Guiada

### Passo 1 — Roteiro de Testes

Antes de modificar qualquer código, execute o roteiro abaixo e anote qualquer comportamento inesperado. Este roteiro cobre todos os fluxos do sistema.

```text
ROTEIRO DE TESTES — SISTEMA ESCOLAR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔐 LOGIN
[  ] Tela de login abre centralizada
[  ] Campo "Usuário" recebe foco automaticamente
[  ] Pressionar Enter no campo de senha aciona login
[  ] Login com admin/admin mostra Menu Principal
[  ] Login com credenciais erradas mostra mensagem de erro
[  ] Campos vazios mostram mensagem de aviso
[  ] Campo de senha exibe asteriscos

📋 MENU PRINCIPAL
[  ] Menu exibe três botões: Cadastrar Alunos, Consultar Alunos, Sair
[  ] Botão "Cadastrar Alunos" abre janela de cadastro
[  ] Botão "Consultar Alunos" abre janela de consulta
[  ] Botão "Sair" pergunta confirmação e fecha o sistema
[  ] Pressionar Esc na janela principal pergunta se deseja sair

📝 CADASTRO (CRUD)
[  ] Janela abre centralizada
[  ] Campos: Nome, Idade, Turma (Combobox)
[  ] Salvar com campos vazios → aviso
[  ] Salvar com idade não numérica → erro
[  ] Salvar com idade negativa → erro
[  ] Salvar com dados válidos → sucesso, tabela atualiza
[  ] Selecionar uma linha → formulário preenche
[  ] Modo edição: Salvar desabilitado, Editar/Excluir habilitados
[  ] Editar um registro → sucesso, tabela atualiza
[  ] Excluir um registro → confirmação → sucesso, tabela atualiza
[  ] Limpar formulário → volta ao modo inserção
[  ] Busca por nome → filtra tabela
[  ] Busca vazia → mostra todos
[  ] Indicador de status mostra Online/Offline
[  ] Botão Sincronizar funciona quando online
[  ] Botão Sincronizar mostra erro amigável quando offline
[  ] Pressionar Esc fecha a janela

🔄 PERSISTÊNCIA
[  ] Cadastrar alunos, fechar sistema, reabrir → dados mantidos
[  ] Sincronizar com nuvem → dados aparecem no Firebase Console
[  ] Baixar da nuvem → dados aparecem no sistema local
```

Execute este roteiro antes de continuar. Os problemas que você encontrar guiarão as correções deste capítulo.

### Passo 2 — Atalhos de teclado

Usuários experientes preferem o teclado ao mouse. Adicionar atalhos torna o sistema mais ágil.

#### 2.1 — Atalho Escape para fechar janelas

Em `views/cadastro.py`, dentro de `abrir_janela_cadastro`, adicione após a criação da janela:

```python
# ===== ADICIONE APÓS janela.protocol("WM_DELETE_WINDOW", janela.destroy) =====
# Eu permito que o usuário feche a janela pressionando a tecla Esc.
janela.bind("<Escape>", lambda event: janela.destroy())
```

Faça o mesmo em qualquer outra janela Toplevel que você tenha (ex: janela de consulta, se implementada).

#### 2.2 — Atalho Escape na janela principal para sair do sistema

Em `main.py`, adicione após a criação da janela:

```python
# ===== ADICIONE APÓS janela.resizable(False, False) =====
# Eu pergunto se o usuário deseja sair ao pressionar Esc.
from tkinter import messagebox

def ao_pressionar_esc(event):
    if messagebox.askyesno("Sair", "Deseja realmente sair do sistema?"):
        janela.destroy()

janela.bind("<Escape>", ao_pressionar_esc)
```

#### 2.3 — Atalho Enter no login

O atalho Enter no campo de senha já foi implementado no Capítulo 03 com `entry_senha.bind("<Return>", ...)`. Verifique se continua funcionando. Se não, adicione-o novamente em `views/login.py`.

### Passo 3 — Barra de status

Uma barra de status no rodapé fornece informações contextuais ao usuário sem atrapalhar o fluxo.

#### 3.1 — Barra de status na tela de cadastro

Em `views/cadastro.py`, substitua o `frame_status` simples que criamos no Capítulo 09 por uma barra de status mais completa. Localize o frame de status e modifique:

```python
# ===== SUBSTITUA O frame_status EXISTENTE POR ESTE =====
# ---------- BARRA DE STATUS (RODAPÉ) ----------
frame_status = tk.Frame(janela, bg="#ecf0f1", bd=1, relief=tk.SUNKEN)
frame_status.pack(side=tk.BOTTOM, fill=tk.X)

# Label de contagem de registros
lbl_contagem = tk.Label(
    frame_status,
    text="",
    font=("Arial", 9),
    bg="#ecf0f1",
    fg="#2c3e50",
    anchor="w"
)
lbl_contagem.pack(side=tk.LEFT, padx=10)

# Label de status da nuvem
lbl_status_nuvem = tk.Label(
    frame_status,
    text="🔴 Offline",
    font=("Arial", 9, "bold"),
    bg="#ecf0f1",
    fg="#e74c3c",
    anchor="e"
)
lbl_status_nuvem.pack(side=tk.RIGHT, padx=10)

# Botão de sincronizar na barra de status (opcional)
btn_sincronizar = tk.Button(
    frame_status,
    text="☁️ Sincronizar",
    font=("Arial", 8),
    bg="#bdc3c7",
    fg="#2c3e50",
    activebackground="#95a5a6",
    activeforeground="white",
    width=12,
    height=1,
    bd=0,
    cursor="hand2",
    command=lambda: ao_clicar_sincronizar()
)
btn_sincronizar.pack(side=tk.RIGHT, padx=5)
```

Agora, atualize a função `atualizar_tabela` para também atualizar o contador na barra de status:

```python
# Dentro de atualizar_tabela, após o loop, adicione:
total = contar_alunos(filtro_nome)
frame_lista.config(text=f" Alunos Cadastrados ({total}) ")
lbl_contagem.config(text=f"📋 {total} aluno(s) cadastrado(s)")
```

E atualize a função `verificar_status` para usar o novo label:

```python
def verificar_status():
    try:
        online = verificar_conexao()
        if online:
            lbl_status_nuvem.config(text="🟢 Online", fg="#27ae60")
        else:
            lbl_status_nuvem.config(text="🔴 Offline", fg="#e74c3c")
    except Exception:
        lbl_status_nuvem.config(text="🔴 Offline", fg="#e74c3c")
```

Remova o `frame_status` antigo (com `pack(side=tk.LEFT)` etc.) e o `lbl_status` que estava nele, para evitar duplicação.

### Passo 4 — Padronização de mensagens

Mensagens inconsistentes confundem o usuário. Defina um padrão:

- **Sucesso:** `messagebox.showinfo("✅ Sucesso", "Mensagem...")`
- **Erro:** `messagebox.showerror("❌ Erro", "Mensagem...")`
- **Aviso:** `messagebox.showwarning("⚠️ Atenção", "Mensagem...")`
- **Confirmação:** `messagebox.askyesno("❓ Confirmar", "Mensagem...")`

Revise todas as chamadas de messagebox no seu código e padronize os títulos. Exemplo em `views/cadastro.py`:

```python
# ===== PADRONIZAÇÃO DE MENSAGENS =====

# Em ao_clicar_salvar:
messagebox.showinfo("✅ Sucesso", f"Aluno '{nome}' cadastrado com sucesso!")

# Em ao_clicar_editar:
messagebox.showinfo("✅ Sucesso", f"Aluno '{nome}' atualizado com sucesso!")

# Em ao_clicar_excluir:
resposta = messagebox.askyesno(
    "❓ Confirmar Exclusão",
    f"Tem certeza que deseja excluir o aluno '{nome}'?\n\n"
    "⚠️ Esta ação não pode ser desfeita."
)
if resposta:
    remover_aluno(id_selecionado)
    messagebox.showinfo("✅ Sucesso", f"Aluno '{nome}' removido do sistema.")

# Em validar_campos (campos vazios):
messagebox.showwarning("⚠️ Atenção", "Por favor, preencha todos os campos antes de salvar.")

# Em validar_campos (idade inválida):
messagebox.showerror("❌ Erro", "O campo 'Idade' deve ser um número inteiro.\nExemplo: 15")

# Em ao_clicar_sincronizar (erro):
messagebox.showerror("❌ Erro de Sincronização", f"Não foi possível sincronizar.\n\n{erro}")
```

!!! tip "Dica Profissional"
    Considere criar um módulo `utils/mensagens.py` com funções como `msg_sucesso(texto)`, `msg_erro(texto)`, etc., para garantir padronização em todo o sistema.

### Passo 5 — Tratamento de exceções em pontos críticos

O sistema lida com banco de dados, rede e entrada do usuário — três fontes comuns de falhas. Adicione try/except nos seguintes locais:

#### 5.1 — No controller aluno.py

```python
# ===== MODIFIQUE AS FUNÇÕES DO CONTROLLER =====

from database.conexao import conectar
import sqlite3

def salvar_aluno(nome, idade, turma):
    try:
        id_gerado = inserir_aluno(nome, idade, turma)
        return {"id": id_gerado, "nome": nome, "idade": idade, "turma": turma}
    except sqlite3.Error as e:
        raise Exception(f"Erro ao salvar aluno no banco de dados: {e}")

def listar_alunos(filtro_nome=None):
    try:
        return listar_alunos_db(filtro_nome)
    except sqlite3.Error as e:
        raise Exception(f"Erro ao consultar alunos: {e}")

def editar_aluno(id_aluno, nome, idade, turma):
    try:
        atualizar_aluno_db(id_aluno, nome, idade, turma)
    except sqlite3.Error as e:
        raise Exception(f"Erro ao atualizar aluno: {e}")

def remover_aluno(id_aluno):
    try:
        excluir_aluno_db(id_aluno)
    except sqlite3.Error as e:
        raise Exception(f"Erro ao excluir aluno: {e}")
```

#### 5.2 — Na view cadastro.py

Envolva as chamadas ao controller em try/except:

```python
# Em ao_clicar_salvar:
try:
    salvar_aluno(nome, idade, turma)
    messagebox.showinfo("✅ Sucesso", f"Aluno '{nome}' cadastrado com sucesso!")
    limpar_campos()
    atualizar_tabela()
except Exception as erro:
    messagebox.showerror("❌ Erro", f"Falha ao salvar:\n{erro}")
```

Repita o padrão para `ao_clicar_editar`, `ao_clicar_excluir` e `ao_clicar_sincronizar`.

#### 5.3 — No carregamento inicial da tabela

```python
# Substitua a chamada final atualizar_tabela() por:
try:
    atualizar_tabela()
except Exception as erro:
    messagebox.showerror("❌ Erro", f"Falha ao carregar dados:\n{erro}")
```

### Passo 6 — Verificação do .gitignore

Abra o arquivo `.gitignore` na raiz do projeto e confirme que contém:

```text
.env
database/credenciais-firebase.json
escola.db
__pycache__/
*.pyc
```

Se algum item estiver faltando, adicione-o agora. Execute `git status` (se estiver usando Git) para verificar se arquivos sensíveis não estão sendo rastreados.

## 📝 Exercício

**Tempo estimado:** 20-25 minutos

**Tarefa:** Siga o Roteiro de Testes completo (apresentado no Passo 1). Para cada item que falhar, corrija o problema e documente a solução em um arquivo `CORRECOES.md` na raiz do projeto.

Exemplo de entrada no `CORRECOES.md`:

```markdown
# Correções — Integração

## 1. Atalho Enter no login não funcionava
**Causa:** O bind havia sido removido acidentalmente na refatoração.
**Solução:** Readicionado `entry_senha.bind("<Return>", lambda event: ao_clicar_entrar())` em `views/login.py`.

## 2. ...
```

??? hint "Dica"
    Não tente corrigir tudo de uma vez. Execute o roteiro item por item. Se algo falhar, anote, corrija e teste novamente aquele item antes de prosseguir.

??? success "Checklist de verificação rápida"
    - [ ] Todos os binds de teclado funcionam
    - [ ] Nenhum botão "Em construção" permanece
    - [ ] As mensagens de erro são informativas (não mostram traceback)
    - [ ] O sistema não trava ao ficar offline
    - [ ] Os dados sobrevivem ao fechar e reabrir

## 🏆 Missão da Equipe

**Tempo estimado:** 30-45 minutos

**Tarefa:** Executem o roteiro de testes no projeto da equipe e realizem as melhorias de integração.

**Entregável:** O sistema da equipe com:

- Roteiro de testes executado e aprovado
- Atalhos de teclado funcionais (Enter, Escape)
- Barra de status na tela principal de cadastro
- Mensagens padronizadas
- Tratamento de exceções em todas as operações
- `.gitignore` verificado

**Checklist da Missão:**

- [ ] Roteiro de testes executado — todos os itens passam
- [ ] Atalho Enter no login funciona
- [ ] Atalho Escape fecha janelas secundárias
- [ ] Atalho Escape na janela principal pergunta se deseja sair
- [ ] Barra de status mostra contagem de registros e status da nuvem
- [ ] Mensagens de sucesso/erro/aviso seguem padrão consistente
- [ ] Erros de banco e rede são capturados com mensagens amigáveis
- [ ] `.gitignore` inclui `.env`, credenciais e `.db`
- [ ] O professor validou o fluxo completo sem erros

!!! important "Nota para o Professor"
    Verifique: Peça que cada equipe demonstre o sistema do início ao fim: login, cadastro de um item, edição do item, exclusão com confirmação, sincronização com nuvem (se configurada) e fechamento. Observe se os atalhos de teclado funcionam e se as mensagens de erro são amigáveis. Teste também o comportamento offline (desconecte a internet e veja se o sistema continua operando).

## ⚡ Desafio

**Vá além:** Implemente logging com o módulo `logging` do Python para registrar operações importantes.

Crie um arquivo `utils/logger.py`:

```python
import logging
from pathlib import Path

# Configuração do logger
LOG_FILE = Path(__file__).parent.parent / "sistema.log"

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)

logger = logging.getLogger("sistema_escolar")

def log_operacao(operacao, detalhes=""):
    """Registra uma operação no arquivo de log."""
    logger.info(f"{operacao} — {detalhes}")

def log_erro(operacao, erro):
    """Registra um erro no arquivo de log."""
    logger.error(f"{operacao} — {erro}")
```

Integre o logger nas operações do controller e nas sincronizações:

```python
from utils.logger import log_operacao, log_erro

# Exemplo em ao_clicar_salvar:
try:
    salvar_aluno(nome, idade, turma)
    log_operacao("INSERT", f"Aluno '{nome}' cadastrado")
    # ...
except Exception as erro:
    log_erro("INSERT", str(erro))
    # ...
```

Adicione `sistema.log` ao `.gitignore`. Isso criará um arquivo de auditoria que registra tudo o que acontece no sistema.

## ⚠️ Erros Comuns

!!! danger "Esquecer de testar o fluxo completo"
    **Sintoma:** O sistema funciona nos testes isolados, mas falha quando o usuário executa uma sequência real (ex: cadastrar, editar o mesmo registro, excluir e cadastrar outro).
    
    **Causa:** Falta de testes de integração. Testes unitários (uma função por vez) não detectam problemas de estado (ex: id_selecionado não resetado).
    
    **Solução:** Execute o roteiro de testes completo na ordem apresentada. Simule o uso real: faça login, cadastre 3 alunos, edite o segundo, exclua o primeiro, busque pelo terceiro, sincronize, saia e reabra.

!!! warning "Mensagens de erro genéricas"
    **Sintoma:** Ao ocorrer um erro, aparece uma janela com o traceback do Python ou uma mensagem vaga como "Erro".
    
    **Causa:** `try/except` ausente ou capturando a exceção mas não exibindo uma mensagem útil.
    
    **Solução:** Todo `try/except` deve incluir um `messagebox.showerror` com uma descrição clara do que aconteceu e, se possível, uma sugestão de ação.

!!! warning "Barra de status sobreposta ou oculta"
    **Sintoma:** A barra de status aparece em cima dos outros widgets ou some quando a janela é redimensionada.
    
    **Causa:** Uso incorreto de `pack(side=tk.BOTTOM)` combinado com `expand=True` em outros frames.
    
    **Solução:** A barra de status deve ser empacotada com `side=tk.BOTTOM` e `fill=tk.X` antes dos frames que usam `expand=True`. No nosso código, o `frame_lista` usa `expand=True` e a barra de status é empacotada antes — isso garante que ela fique no rodapé.

## 💡 Boas Práticas

**1. Testes de integração manuais**

Antes de automatizar testes, execute o fluxo completo manualmente. Anote cada passo e o resultado esperado. Um roteiro de testes como o que criamos é um artefato valioso que pode ser reutilizado em futuras versões do sistema.

**2. Atalhos de teclado como diferencial de UX**

Enter para confirmar e Escape para cancelar/fechar são esperados em qualquer software profissional. Implementá-los demonstra atenção aos detalhes e respeito pelo tempo do usuário.

**3. Barra de status informativa**

Uma barra de status discreta no rodapé evita o uso excessivo de pop-ups para informações triviais. O usuário sabe quantos registros existem e se está online sem precisar clicar em nada.

**4. Padronização de mensagens**

Usar emojis consistentes (✅, ❌, ⚠️) nos títulos das mensagens cria uma linguagem visual que o usuário aprende rapidamente. Em sistemas corporativos, essa padronização geralmente é definida em um guia de estilo.

**5. Logging para diagnóstico**

O módulo `logging` do Python é uma ferramenta poderosa. Em produção, os logs são essenciais para diagnosticar problemas que os usuários reportam mas não sabem descrever tecnicamente. Registre operações de escrita (INSERT, UPDATE, DELETE) e erros sempre.

## ☑️ Checklist

Antes de prosseguir para o próximo capítulo, confirme:

- [ ] Roteiro de testes executado — todos os itens passam
- [ ] Atalho Enter no login funciona
- [ ] Atalho Escape fecha janelas secundárias
- [ ] Atalho Escape na janela principal pergunta confirmação para sair
- [ ] Barra de status exibe contagem de registros e status online/offline
- [ ] Mensagens padronizadas com ✅, ❌, ⚠️ e ❓
- [ ] Todas as operações de banco estão envoltas em try/except
- [ ] Sincronização com nuvem tem tratamento de erro de rede
- [ ] `.gitignore` verificado e completo
- [ ] O sistema funciona offline (sem internet) sem travar
- [ ] Minha equipe concluiu a Missão da Equipe

## ➡️ Próximo Capítulo

No **Capítulo 11 — Refatoração**, você fará a limpeza final do código: remover comentários desnecessários, extrair funções duplicadas, garantir que os nomes seguem um padrão consistente e preparar o projeto para a apresentação final.

Pense na refatoração como a faxina antes da visita: o sistema já funciona, mas queremos que ele esteja impecável para a entrega de 20 de agosto. 🧹
