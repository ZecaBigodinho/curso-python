# 02. Ambientes Virtuais (`venv`) e Terminal Integrado

> **Curso:** Python para Desktop  
> **Módulo:** 06 — Configuração do VS Code & Ambiente Python (Bônus)  
> **Nível:** Intermediário Didático  
> **Tempo estimado:** 20 min  

---

## 🎯 Objetivos de Aprendizagem

Ao final deste capítulo, você será capaz de:

- Entender a importância de usar **Ambientes Virtuais (`venv`)** em cada projeto.
- Criar e ativar um `venv` no terminal do VS Code.
- Resolver o erro comum de **Política de Execução de Scripts** no Windows PowerShell.
- Selecionar o **Interpretador Python** correto no VS Code.
- Instalar bibliotecas externas com `pip` de forma isolada e segura.

---

## 💡 O que é um Ambiente Virtual (`venv`)?

Imagine que o Projeto A precisa da biblioteca `CustomTkinter` versão 5.0, e o Projeto B precisa da versão 4.0. Se você instalar tudo no Python global do sistema, um projeto vai quebrar o outro!

!!! note "A Metáfora da Maleta Isolada"
    Um **Ambiente Virtual (`venv`)** é como uma maleta de ferramentas exclusiva para aquele projeto. Tudo o que você instala com `pip` dentro da maleta fica isolado e não afeta o resto do computador.

---

## 🛠️ Criando o Ambiente Virtual Passo a Passo

No terminal integrado do VS Code (`Ctrl + ~`), certifique-se de estar na pasta do seu projeto e execute:

```bash
# Criar a pasta 'venv' com o ambiente isolado
python -m venv venv
```

Após alguns segundos, uma pasta chamada `venv` aparecerá no seu explorador de arquivos!

---

## 🚀 Ativando o Ambiente Virtual no Terminal

=== "🪟 Windows (PowerShell)"
    ```powershell
    .\venv\Scripts\Activate.ps1
    ```

=== "🐧 Linux / 🍎 macOS (Bash/Zsh)"
    ```bash
    source venv/bin/activate
    ```

Quando ativado com sucesso, o terminal exibirá `(venv)` no início da linha de comando:
```text
(venv) PS E:\meu_projeto>
```

---

## ⚠️ Erro Clássico no Windows: "A execução de scripts foi desabilitada neste sistema"

Ao tentar ativar o `venv` no PowerShell do Windows pela primeira vez, você pode receber a seguinte mensagem vermelha:

```text
.\venv\Scripts\Activate.ps1 : O arquivo não pode ser carregado porque a execução de scripts foi desabilitada neste sistema.
```

### 🔧 Como Resolver em 1 Minuto:

1. Abra o PowerShell do Windows como **Administrador** (Clique com botão direito no menu Iniciar ➔ *PowerShell como Administrador*).
2. Digite o comando:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
3. Digite `S` (Sim) e feche o PowerShell.
4. Volte ao VS Code e tente ativar o `venv` novamente!

---

## 🎯 Selecionando o Interpretador Python no VS Code

Para que o VS Code saiba que deve usar a versão do Python que está dentro da pasta `venv`:

1. Pressione `Ctrl + Shift + P` para abrir a Paleta de Comandos.
2. Digite **Python: Select Interpreter**.
3. Selecione a opção que indica o caminho do seu ambiente virtual:
   `.\venv\Scripts\python.exe` (ou `./venv/bin/python`).

---

## 📦 Instalando Bibliotecas com `pip` no `venv`

Com o `(venv)` ativo no terminal, você pode instalar qualquer biblioteca com total segurança:

```bash
# Atualizar o gerenciador de pacotes pip
python -m pip install --upgrade pip

# Instalar bibliotecas do nosso curso
pip install customtkinter requests python-dotenv

# Congelar as dependências instaladas no arquivo requirements.txt
pip freeze > requirements.txt
```

---

## 🧪 Quiz Rápido de Fixação

1. **Como saber se o ambiente virtual está realmente ativo no terminal do VS Code?**
??? check "Ver Resposta Comentada"
    Você verá o prefixo **`(venv)`** destacado no início da linha de comando do terminal.

2. **Para que serve o arquivo `requirements.txt`?**
??? check "Ver Resposta Comentada"
    Para listar o nome e a versão exata de todas as bibliotecas usadas no projeto, permitindo que outro desenvolvedor reinstale tudo com `pip install -r requirements.txt`.
