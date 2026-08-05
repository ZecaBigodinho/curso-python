# 09 — Banco em Nuvem

## 🎯 Objetivo

Neste capítulo você vai conectar o Sistema Escolar a um banco de dados em nuvem, permitindo que os dados sincronizem entre diferentes dispositivos e funcionem como backup remoto — sem abandonar o SQLite local.

Ao final, você terá:

- Um projeto configurado no Firebase (banco em nuvem gratuito)
- O arquivo `.env` protegendo credenciais com python-dotenv
- Um novo módulo `database/nuvem.py` com funções de sincronização
- Um botão Sincronizar na interface que envia e recebe dados da nuvem
- Um indicador visual de status (🟢 online / 🔴 offline)
- O sistema funcionando offline com SQLite e sincronizando quando houver internet

## 📍 Contextualização

No Capítulo 08, você concluiu o CRUD completo. O sistema cadastra, lista, edita, exclui e busca alunos — tudo persistido no SQLite local. É funcional, mas sofre de uma limitação: os dados só existem na máquina onde foram cadastrados.

E se a escola tiver dois computadores na secretaria? E se o diretor quiser acessar os dados de casa? E se o HD queimar?

A solução profissional é um banco em nuvem — um servidor remoto que armazena os dados e permite acesso de qualquer lugar. Neste capítulo, você aprenderá a usar o Firebase Realtime Database, um serviço gratuito do Google que armazena dados em formato JSON e sincroniza em tempo real.

Seguiremos a filosofia offline-first: o SQLite continua sendo o banco principal (operações são instantâneas e funcionam sem internet). A nuvem atua como backup e sincronização.

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
🔨 Banco em Nuvem ← VOCÊ ESTÁ AQUI
⬜ Integração e Testes
⬜ Refatoração e Entrega
```

## ✅ Resultado Esperado

A tela de cadastro ganhará um botão "Sincronizar ☁️" e um indicador de status. Ao clicar:

- Se houver internet: os dados locais são enviados para a nuvem e os dados remotos são baixados para o SQLite (mesclando sem duplicar).
- Se não houver internet: uma mensagem informa que a sincronização falhou e o sistema continua funcionando offline.

Visualmente:

```text
┌──────────────────────────────────────────────────────┐
│  Cadastro de Alunos                              _ □ X│
│                                                      │
│  ┌─ Dados do Aluno ────────────────────────────────┐ │
│  │  ...                                            │ │
│  └─────────────────────────────────────────────────┘ │
│                                                      │
│  Status: 🟢 Online    [☁️ Sincronizar]              │
│                                                      │
│  ┌─ Alunos Cadastrados ────────────────────────────┐ │
│  │  ...                                            │ │
│  └─────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────┘
```

Arquivos criados ou modificados:

| Arquivo | Ação |
|---|---|
| `.env` | Novo — credenciais do Firebase (NÃO versionado) |
| `.gitignore` | Modificado — adicionar `.env` e `escola.db` |
| `database/nuvem.py` | Novo — funções de sincronização com Firebase |
| `views/cadastro.py` | Modificado — botão Sincronizar e indicador de status |
| `requirements.txt` ou instruções de instalação | Novo — dependências |

## 💻 Implementação Guiada

### Passo 1 — Entendendo a arquitetura offline-first

Antes de programar, entenda o modelo que adotaremos:

```text
┌─────────────────────┐         ┌─────────────────────┐
│   Computador Local  │         │     Nuvem (Firebase) │
│                     │         │                     │
│  ┌───────────────┐  │  envia  │  ┌───────────────┐  │
│  │   SQLite      │──┼────────▶│  │  Realtime     │  │
│  │  (escola.db)  │  │         │  │  Database     │  │
│  └───────────────┘  │  baixa  │  └───────────────┘  │
│                     │◀────────│                     │
└─────────────────────┘         └─────────────────────┘

Fluxo normal (offline):
  Usuário → Interface → Controller → SQLite

Fluxo de sincronização (online):
  SQLite ←→ Nuvem (via botão "Sincronizar" ou automático)
```

O SQLite é o dono da verdade local. A nuvem é uma cópia. A sincronização mescla os dados — se um aluno existe nos dois lugares, prevalece a versão mais recente (ou a local, para simplificar).

!!! note "Conceito Importante"
    Offline-first é um padrão de arquitetura onde o sistema funciona plenamente sem internet. A conexão é um bônus, não um requisito. Aplicativos como Google Docs, Notion e WhatsApp usam esse modelo.

### Passo 2 — Configurando o Firebase

Você precisará de uma conta Google. Vamos criar o projeto no Firebase passo a passo.

1. Acesse `console.firebase.google.com`
2. Clique em **Adicionar projeto** → dê o nome "Sistema Escolar" → siga o assistente (analytics opcional)
3. No menu à esquerda, vá em **Criação > Realtime Database**
4. Clique em **Criar banco de dados** → escolha o local (recomendo us-central1 ou southamerica-east1)
5. Em Regras de segurança, para teste, escolha **Modo de teste** (permite leitura/escrita por 30 dias). ⚠️ Para produção, configure regras de autenticação.
6. Copie a URL do banco (algo como `https://sistema-escolar-xxxxx-default-rtdb.firebaseio.com/`)
7. No menu **Visão geral do projeto > Configurações do projeto > Contas de serviço**, clique em **Gerar nova chave privada** (isso baixa um JSON com as credenciais). Guarde esse arquivo — nós o usaremos para autenticar o Python.

!!! tip "Dica Profissional"
    Para um sistema real, você configuraria autenticação por e-mail/senha e regras de segurança granulares. Mas para este capítulo, a chave de serviço é suficiente. O Firebase Realtime Database é gratuito até 1 GB armazenado e 10 GB de download por mês — mais que suficiente para nosso sistema escolar.

### Passo 3 — Instalando dependências e configurando o .env

Instale as bibliotecas necessárias:

```bash
pip install firebase-admin python-dotenv
```

- `firebase-admin`: SDK oficial do Firebase para Python (usado em servidores)
- `python-dotenv`: Carrega variáveis de ambiente do arquivo `.env`

Crie o arquivo `.env` na raiz do projeto (`sistema_escolar/.env`):

```text
# ===== CREDENCIAIS DO FIREBASE =====
# ATENÇÃO: Este arquivo NÃO deve ser versionado!
FIREBASE_DATABASE_URL=https://seu-projeto-default-rtdb.firebaseio.com/
FIREBASE_CREDENTIALS=caminho/para/o/arquivo/baixado.json
```

Preencha com a URL do seu banco e o caminho do arquivo JSON de credenciais que você baixou. Coloque esse JSON dentro da pasta `database/` (ex: `database/credenciais-firebase.json`) e referencie o caminho relativo:

```text
FIREBASE_CREDENTIALS=database/credenciais-firebase.json
```

Agora, adicione ao `.gitignore` (crie o arquivo se não existir):

```text
# .gitignore
.env
database/credenciais-firebase.json
escola.db
__pycache__/
*.pyc
```

!!! danger "Erro Crítico"
    NUNCA faça commit do arquivo `.env` ou das credenciais do Firebase. Se essas chaves vazarem no GitHub, qualquer pessoa poderá acessar seu banco de dados. Em 2023, mais de 10 milhões de chaves de API vazaram em repositórios públicos. Proteja-se.

### Passo 4 — Criando o módulo de sincronização

Crie o arquivo `database/nuvem.py`:

```python
# ======================================================================
# nuvem.py — Sincronização com Firebase
# ======================================================================
# Eu sou responsável por enviar e receber dados da nuvem.
# Trabalho em conjunto com o SQLite local.
# ======================================================================

import os
from pathlib import Path
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, db

from database.conexao import conectar

# ---------- CARREGAMENTO DAS VARIÁVEIS DE AMBIENTE ----------
# Eu carrego o arquivo .env para acessar as credenciais.
# O path é relativo à raiz do projeto.
load_dotenv(Path(__file__).parent.parent / ".env")

# ---------- INICIALIZAÇÃO DO FIREBASE (acontece uma única vez) ----------
_firebase_inicializado = False


def _inicializar_firebase():
    """
    Eu configuro a conexão com o Firebase.
    Só executo na primeira vez que for chamado.
    """
    global _firebase_inicializado
    if _firebase_inicializado:
        return

    # Eu busco as credenciais nas variáveis de ambiente.
    caminho_credenciais = os.getenv("FIREBASE_CREDENTIALS")
    database_url = os.getenv("FIREBASE_DATABASE_URL")

    if not caminho_credenciais or not database_url:
        raise ValueError(
            "Variáveis FIREBASE_CREDENTIALS e FIREBASE_DATABASE_URL "
            "devem estar definidas no arquivo .env"
        )

    # Eu inicio o app Firebase com as credenciais do arquivo JSON.
    cred = credentials.Certificate(caminho_credenciais)
    firebase_admin.initialize_app(cred, {
        "databaseURL": database_url
    })
    _firebase_inicializado = True


# ---------- FUNÇÕES DE SINCRONIZAÇÃO ----------

def enviar_alunos_para_nuvem():
    """
    Eu envio todos os alunos do SQLite para o Firebase.
    Substituo completamente o nó 'alunos' na nuvem.
    """
    _inicializar_firebase()

    # Busco os alunos locais.
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, idade, turma FROM alunos")
        alunos_locais = [dict(aluno) for aluno in cursor.fetchall()]

    # Eu apago o nó 'alunos' na nuvem e recrio com os dados locais.
    ref_alunos = db.reference("alunos")
    ref_alunos.delete()  # Limpa a nuvem

    for aluno in alunos_locais:
        # Uso o id do SQLite como chave do nó no Firebase.
        ref_alunos.child(str(aluno["id"])).set({
            "nome": aluno["nome"],
            "idade": aluno["idade"],
            "turma": aluno["turma"]
        })

    return len(alunos_locais)


def baixar_alunos_da_nuvem():
    """
    Eu busco os alunos do Firebase e os insiro/atualizo no SQLite.
    Se um aluno com o mesmo id já existir, atualizo; senão, insiro.
    """
    _inicializar_firebase()

    # Busco os dados do nó 'alunos' no Firebase.
    ref_alunos = db.reference("alunos")
    dados_nuvem = ref_alunos.get()

    if not dados_nuvem:
        return 0  # Nenhum dado na nuvem

    with conectar() as conn:
        cursor = conn.cursor()
        contador = 0

        for id_str, dados in dados_nuvem.items():
            aluno_id = int(id_str)
            # Verifico se o aluno já existe no SQLite.
            cursor.execute(
                "SELECT id FROM alunos WHERE id = ?", (aluno_id,)
            )
            if cursor.fetchone():
                # Atualizo os dados existentes.
                cursor.execute("""
                    UPDATE alunos
                    SET nome = ?, idade = ?, turma = ?
                    WHERE id = ?
                """, (dados["nome"], dados["idade"], dados["turma"], aluno_id))
            else:
                # Insiro um novo aluno vindo da nuvem.
                cursor.execute("""
                    INSERT INTO alunos (id, nome, idade, turma)
                    VALUES (?, ?, ?, ?)
                """, (aluno_id, dados["nome"], dados["idade"], dados["turma"]))
            contador += 1

        conn.commit()

    return contador


def verificar_conexao():
    """
    Eu testo se o Firebase está acessível.
    Retorno True se conseguir conectar, False caso contrário.
    """
    try:
        _inicializar_firebase()
        ref = db.reference(".info/connected")
        return ref.get() is True
    except Exception:
        return False
```

!!! note "Estrutura dos dados no Firebase"
    O Realtime Database armazena dados como JSON. Nossa estrutura será:
    
    ```json
    {
      "alunos": {
        "1": { "nome": "João", "idade": 15, "turma": "9A" },
        "2": { "nome": "Maria", "idade": 14, "turma": "9B" }
      }
    }
    ```
    
    Cada aluno é um nó filho de `alunos`, identificado pelo `id` do SQLite. Isso permite mapeamento direto entre local e nuvem.

### Passo 5 — Integrando a sincronização na interface

Abra `views/cadastro.py` e adicione o botão Sincronizar e o indicador de status.

No topo do arquivo, adicione os imports:

```python
# ===== ADICIONE ESTES IMPORTS no topo de views/cadastro.py =====
from database.nuvem import (
    enviar_alunos_para_nuvem,
    baixar_alunos_da_nuvem,
    verificar_conexao,
)
import threading
```

Após o `frame_busca` e antes do `frame_lista`, adicione o frame de status:

```python
    # ---------- FRAME DE STATUS E SINCRONIZAÇÃO ----------
    # (adicione este bloco após o frame_busca.pack() e antes do frame_lista)

    frame_status = tk.Frame(janela, bg="#f5f6fa")
    frame_status.pack(fill=tk.X, padx=20, pady=(5, 0))

    # Eu crio um label que mostrará o status da conexão.
    lbl_status = tk.Label(
        frame_status,
        text="🔴 Verificando...",
        font=("Arial", 10, "bold"),
        bg="#f5f6fa",
        fg="#555555"
    )
    lbl_status.pack(side=tk.LEFT)

    # Eu crio o botão de sincronização.
    btn_sincronizar = tk.Button(
        frame_status,
        text="☁️ Sincronizar",
        font=("Arial", 10, "bold"),
        bg="#3498db",
        fg="white",
        activebackground="#2980b9",
        activeforeground="white",
        width=14,
        height=1,
        bd=0,
        cursor="hand2",
        command=lambda: ao_clicar_sincronizar()
    )
    btn_sincronizar.pack(side=tk.RIGHT)
```

Adicione as funções de sincronização e verificação de status, dentro de `abrir_janela_cadastro` (antes do `atualizar_tabela()` final):

```python
    # ===== FUNÇÕES DE SINCRONIZAÇÃO (dentro de abrir_janela_cadastro) =====

    def verificar_status():
        """
        Eu verifico a conexão com a nuvem em uma thread separada
        e atualizo o label de status.
        """
        try:
            online = verificar_conexao()
            if online:
                lbl_status.config(text="🟢 Online", fg="#27ae60")
            else:
                lbl_status.config(text="🔴 Offline", fg="#e74c3c")
        except Exception:
            lbl_status.config(text="🔴 Offline", fg="#e74c3c")

    def ao_clicar_sincronizar():
        """
        Eu sincronizo os dados locais com a nuvem.
        Primeiro envio, depois baixo (para mesclar).
        """
        btn_sincronizar.config(state=tk.DISABLED, text="⏳ Sincronizando...")
        lbl_status.config(text="⏳ Sincronizando...", fg="#f39c12")

        try:
            # Envio dados locais para a nuvem.
            enviados = enviar_alunos_para_nuvem()
            # Baixo dados da nuvem para o local.
            baixados = baixar_alunos_da_nuvem()

            messagebox.showinfo(
                "Sincronização Concluída",
                f"Enviados: {enviados} aluno(s)\nBaixados: {baixados} aluno(s)"
            )
            lbl_status.config(text="🟢 Online", fg="#27ae60")
            # Atualizo a tabela com os dados recém-baixados.
            atualizar_tabela()
        except Exception as erro:
            messagebox.showerror(
                "Erro de Sincronização",
                f"Não foi possível sincronizar.\n\nErro: {erro}"
            )
            lbl_status.config(text="🔴 Offline", fg="#e74c3c")
        finally:
            btn_sincronizar.config(state=tk.NORMAL, text="☁️ Sincronizar")

    # Verifico o status assim que a janela abre.
    # threading.Thread(target=verificar_status).start()  # Ideal, mas para simplicidade didática vamos chamar direto se preferir
    verificar_status()
```

!!! tip "Dica Profissional"
    A verificação de conexão (`verificar_conexao`) pode travar a interface por alguns segundos se não houver resposta do servidor. Para evitar congelamento, envolva a chamada em uma thread separada usando `threading.Thread(target=verificar_status).start()`. No código acima, mantivemos simples para foco didático — mas fica o desafio implícito.

### Passo 6 — Testando a sincronização

1. Execute o sistema: `python main.py`
2. Abra o Cadastro de Alunos.
3. Observe o indicador de status: 🟢 Online ou 🔴 Offline.
4. Cadastre alguns alunos localmente.
5. Clique em ☁️ Sincronizar.
6. Se tudo funcionar, mensagem: "Enviados: 3 aluno(s) | Baixados: 0 aluno(s)".
7. Abra o console do Firebase → Realtime Database. Os alunos devem aparecer lá!
8. Para testar o download, adicione um aluno manualmente no console do Firebase e clique em Sincronizar novamente — ele será baixado para o SQLite e aparecerá na tabela.

## 📝 Exercício

**Tempo estimado:** 15-20 minutos

**Tarefa:** Adicione um botão "Forçar Download" que limpa o SQLite local e baixa todos os dados da nuvem novamente (útil se o banco local corromper).

Dica: Antes de baixar, execute `DELETE FROM alunos` no SQLite. Depois, chame `baixar_alunos_da_nuvem()` e atualize a tabela. Peça confirmação antes de executar, pois é uma ação destrutiva.

??? hint "Dica"
    Crie um botão "⬇️ Forçar Download" ao lado do Sincronizar. No comando, use `messagebox.askyesno` para confirmar. Se sim, execute:
    
    ```python
    with conectar() as conn:
        conn.execute("DELETE FROM alunos")
        conn.commit()
    baixar_alunos_da_nuvem()
    atualizar_tabela()
    ```

??? success "Solução resumida"
    Adicione o botão no `frame_status`:
    
    ```python
    btn_forcar_download = tk.Button(
        frame_status, text="⬇️ Forçar Download", font=("Arial", 10, "bold"),
        bg="#e67e22", fg="white", activebackground="#d35400",
        width=16, height=1, bd=0, cursor="hand2",
        command=ao_clicar_forcar_download
    )
    btn_forcar_download.pack(side=tk.RIGHT, padx=(5, 0))
    ```
    
    Função:
    
    ```python
    def ao_clicar_forcar_download():
        if not messagebox.askyesno("Confirmar", "Isso apagará TODOS os dados locais e baixará da nuvem. Continuar?"):
            return
        with conectar() as conn:
            conn.execute("DELETE FROM alunos")
            conn.commit()
        baixados = baixar_alunos_da_nuvem()
        atualizar_tabela()
        messagebox.showinfo("Download", f"{baixados} aluno(s) baixados da nuvem.")
    ```
    
    (Lembre-se de importar `conectar` do módulo `database.conexao`.)

## 🏆 Missão da Equipe

**Tempo estimado:** 30-45 minutos

**Tarefa:** Configurem o Firebase para o projeto da equipe e implementem a sincronização básica.

**Entregável:** O sistema da equipe com:

- Projeto Firebase criado e configurado
- `.env` com credenciais (não versionado)
- `.gitignore` atualizado
- `database/nuvem.py` adaptado para a entidade do projeto
- Botão Sincronizar na interface
- Indicador de status online/offline

**Checklist da Missão:**

- [ ] Projeto Firebase criado com Realtime Database
- [ ] Credenciais baixadas e armazenadas em `database/`
- [ ] `.env` configurado com FIREBASE_DATABASE_URL e FIREBASE_CREDENTIALS
- [ ] `.gitignore` inclui `.env`, credenciais e arquivo `.db`
- [ ] `database/nuvem.py` adaptado com funções de enviar/baixar para a entidade do projeto
- [ ] Botão Sincronizar funcional na tela de cadastro
- [ ] Indicador de status mostra 🟢 Online ou 🔴 Offline
- [ ] Sincronização testada: dados aparecem no console Firebase
- [ ] O professor verificou a sincronização funcionando

!!! important "Nota para o Professor"
    Verifique: Cada equipe deve demonstrar a sincronização completa. Peça que cadastrem um registro, cliquem em Sincronizar e mostrem o dado no console Firebase. Depois, peça que adicionem um registro manualmente no console e sincronizem novamente — o registro deve aparecer no sistema local.

## ⚡ Desafio

**Vá além:** Implemente sincronização automática — toda vez que um aluno for salvo, editado ou excluído, o sistema sincroniza automaticamente com a nuvem (se estiver online).

Dica: Modifique as funções `ao_clicar_salvar`, `ao_clicar_editar` e `ao_clicar_excluir` em `views/cadastro.py` para, após a operação local, verificar o status e, se online, chamar `enviar_alunos_para_nuvem()` silenciosamente (sem messagebox, a menos que haja erro).

```python
# Exemplo de adaptação em ao_clicar_salvar:
salvar_aluno(nome, idade, turma)
atualizar_tabela()

# Sincronização automática silenciosa
if verificar_conexao():
    try:
        enviar_alunos_para_nuvem()
    except Exception:
        pass  # Falha silenciosa — o dado já está salvo localmente
```

Isso torna o sistema praticamente em tempo real — como o Google Docs.

## ⚠️ Erros Comuns

!!! danger "Credenciais expostas no código"
    **Sintoma:** O código contém a chave da API ou a URL do Firebase hardcoded.
    
    **Causa:** Copiar e colar a chave diretamente no arquivo `.py` em vez de usar variáveis de ambiente.
    
    **Solução:** Use SEMPRE `.env` e `os.getenv()`. Adicione `.env` ao `.gitignore`. Se já fez commit com a chave, o Firebase pode invalidá-la automaticamente — você precisará gerar uma nova.

!!! warning "Firebase não inicializado corretamente"
    **Sintoma:** `ValueError: The default Firebase app does not exist.`
    
    **Causa:** `_inicializar_firebase()` não foi chamado antes de usar o banco, ou o arquivo de credenciais está em um caminho errado.
    
    **Solução:** Verifique se o caminho em FIREBASE_CREDENTIALS está correto (use caminho absoluto ou relativo à raiz do projeto). Chame `_inicializar_firebase()` no início de cada função pública.

!!! danger "Falha de rede sem tratamento"
    **Sintoma:** O sistema trava ou mostra um traceback gigante quando não há internet.
    
    **Causa:** Falta de try/except ao redor das chamadas de rede.
    
    **Solução:** Envolva todas as chamadas ao Firebase em blocos `try/except Exception as e`. Exiba um `messagebox.showerror` amigável e mantenha o sistema funcional offline.

!!! warning "Duplicação de dados na sincronização"
    **Sintoma:** Após várias sincronizações, o mesmo aluno aparece duplicado na tabela.
    
    **Causa:** A função `baixar_alunos_da_nuvem` insere registros sem verificar se o id já existe. Se o INSERT falhar por conflito de chave, o aluno da nuvem não é mesclado.
    
    **Solução:** Nossa implementação já trata isso com INSERT OR... na verdade, usamos SELECT + UPDATE/INSERT. Verifique se a lógica condicional está correta. Outra abordagem é usar `INSERT OR REPLACE`.

## 💡 Boas Práticas

**1. Offline-first como filosofia**

O sistema não depende da nuvem para funcionar. Se o Firebase estiver fora do ar ou o usuário estiver sem internet, o sistema continua operando normalmente com o SQLite. A nuvem é um recurso adicional, não um ponto único de falha.

**2. Variáveis de ambiente para credenciais**

Nunca coloque chaves, senhas ou URLs confidenciais no código-fonte. Use `.env` + python-dotenv. Em produção, essas variáveis são injetadas pelo servidor, não por um arquivo.

**3. .gitignore desde o início**

Adicionar `.env` e credenciais ao `.gitignore` evita que dados sensíveis sejam versionados acidentalmente. Se você perceber que fez commit de uma chave, gire-a imediatamente (gere uma nova) e faça um `git rm --cached` do arquivo comprometido.

**4. Sincronização manual vs automática**

Para um sistema escolar, a sincronização manual (botão) é adequada — o usuário decide quando enviar/receber dados. Para sistemas que exigem tempo real (chat, colaboração), a sincronização automática é necessária. O desafio deste capítulo mostra como evoluir para esse modelo.

**5. Estrutura de dados plana no Firebase**

Usamos `alunos/{id}/...` em vez de arrays. O Firebase recomenda estruturas planas com chaves únicas para evitar conflitos de concorrência e facilitar consultas.

## ☑️ Checklist

Antes de prosseguir para o próximo capítulo, confirme:

- [ ] Projeto Firebase criado e Realtime Database ativado
- [ ] Credenciais baixadas e armazenadas em `database/`
- [ ] Arquivo `.env` criado com FIREBASE_DATABASE_URL e FIREBASE_CREDENTIALS
- [ ] `.gitignore` inclui `.env`, credenciais e `escola.db`
- [ ] Bibliotecas `firebase-admin` e `python-dotenv` instaladas
- [ ] Módulo `database/nuvem.py` criado com funções de enviar, baixar e verificar conexão
- [ ] Botão "☁️ Sincronizar" adicionado à tela de cadastro
- [ ] Indicador de status mostra 🟢 Online ou 🔴 Offline
- [ ] Sincronização testada com sucesso (dados aparecem no console Firebase)
- [ ] Sistema funciona offline (simular desconectando a internet)
- [ ] Minha equipe concluiu a Missão da Equipe

## ➡️ Próximo Capítulo

No **Capítulo 10 — Integração**, você fará a revisão completa do sistema. Todas as peças estão construídas: login, menu, navegação, cadastro, CRUD, SQLite e nuvem. Agora é hora de:

- Revisar o fluxo completo (Login → Menu → Cadastro → Sincronização)
- Corrigir arestas (comportamento do botão X, mensagens de erro, centralização)
- Testar o sistema como um todo
- Preparar o projeto final para apresentação

O sistema está quase pronto. A reta final chegou! 🏁
