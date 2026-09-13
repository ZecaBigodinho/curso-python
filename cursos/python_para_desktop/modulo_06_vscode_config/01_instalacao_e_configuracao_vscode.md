# 01. Instalando e Configurando o VS Code do Zero

> **Curso:** Python para Desktop  
> **Módulo:** 06 — Configuração do VS Code & Ambiente Python (Bônus)  
> **Nível:** Iniciante / Passo a Passo  
> **Tempo estimado:** 25 min  

---

## 🎯 Objetivos de Aprendizagem

Ao final deste capítulo, você será capaz de:

- Baixar e instalar o **Python 3.10+** e o **VS Code** no seu computador.
- Marcar a opção essencial `Add python.exe to PATH` na instalação.
- Instalar as **extensões profissionais** recomendadas para Python no VS Code.
- Dominar os **atalhos de teclado indispensáveis** do dia a dia.
- Configurar o VS Code para formatar e salvar seu código automaticamente.

---

## 📥 Passo 1: Instalando o Python no Computador

Antes do VS Code, seu computador precisa aprender a entender a linguagem Python.

=== "🪟 Windows"
    1. Acesse o site oficial: [python.org/downloads](https://www.python.org/downloads/)
    2. Clique no botão **Download Python 3.x.x**.
    3. Execute o instalador baixado.
    4. ⚠️ **MUITO IMPORTANTE:** Na primeira tela do instalador, marque a caixa:
       - `[X] Add python.exe to PATH` (no rodapé da janela).
    5. Clique em **Install Now** e aguarde a conclusão.

=== "🐧 Linux (Ubuntu/Debian)"
    Abra o terminal e execute:
    ```bash
    sudo apt update
    sudo apt install python3 python3-pip python3-venv -y
    ```

=== "🍎 macOS"
    Baixe o instalador no site oficial ou via Homebrew:
    ```bash
    brew install python
    ```

!!! danger "Atenção: Esqueceu de marcar 'Add to PATH'?"
    Se você não marcar a caixa `Add python.exe to PATH` no Windows, o VS Code e o terminal não conseguirão encontrar o comando `python`! Caso tenha esquecido, execute o instalador novamente, escolha `Modify` e marque a opção.

---

## 💻 Passo 2: Instalando o VS Code

1. Acesse [code.visualstudio.com](https://code.visualstudio.com/) e baixe o instalador para seu sistema operacional.
2. Durante a instalação no Windows, recomendamos marcar as opções:
   - `[X] Criar um atalho na Área de Trabalho`
   - `[X] Adicionar "Abrir com Código" ao menu de contexto de arquivos`
   - `[X] Adicionar "Abrir com Código" ao menu de contexto de diretórios`

---

## 🧩 Passo 3: Extensões Indispensáveis para Python

Abra o VS Code, clique no ícone de **Extensões** na barra lateral esquerda (ou pressione `Ctrl + Shift + X`) e pesquise pelas seguintes extensões:

<div class="grid cards" markdown>

-   :material-language-python: **1. Python (Microsoft)**
    ---
    **Id:** `ms-python.python`  
    Suporte oficial para execução, depuração (debug), autocompletar e linting.

-   :material-lightning-bolt: **2. Pylance (Microsoft)**
    ---
    **Id:** `ms-python.vscode-pylance`  
    Fornece autocompletar ultra-rápido, verificação de tipos e sugestões inteligentes de código.

-   :material-format-paint: **3. Material Icon Theme**
    ---
    **Id:** `PKief.material-icon-theme`  
    Adiciona ícones visuais bonitos e coloridos para cada tipo de arquivo e pasta no seu explorador.

-   :material-circle-slice-8: **4. Error Lens**
    ---
    **Id:** `usernamehw.errorlens`  
    Destaca erros e avisos de sintaxe diretamente na linha do código sem precisar passar o mouse por cima.

-   :material-format-align-left: **5. Python Indent**
    ---
    **Id:** `KevinRose.vsc-python-indent`  
    Ajusta a indentação automática de blocos `if`, `for`, `def` exatamente como o Python exige.

</div>

---

## ⚙️ Passo 4: Configuração Automática do VS Code (`settings.json`)

Para que seu VS Code formate o código automaticamente ao salvar, pressione `Ctrl + Shift + P`, digite **Preferences: Open User Settings (JSON)** e adicione estas configurações:

```json
{
    "workbench.iconTheme": "material-icon-theme",
    "editor.fontSize": 15,
    "editor.fontFamily": "'JetBrains Mono', 'Fira Code', Consolas, monospace",
    "editor.fontLigatures": true,
    "editor.formatOnSave": true,
    "editor.tabSize": 4,
    "editor.insertSpaces": true,
    "python.analysis.typeCheckingMode": "basic",
    "files.autoSave": "afterDelay"
}
```

---

## ⌨️ Atalhos de Teclado Mágicos do VS Code

| Atalho (Windows/Linux) | Função |
|------------------------|--------|
| `Ctrl + Shift + P` | **Paleta de Comandos** (Busca qualquer comando do VS Code) |
| `Ctrl + ~` (ou `Ctrl + '`) | **Abrir / Fechar Terminal Integrado** |
| `Ctrl + F5` | Executar o arquivo Python atual sem depurador |
| `F5` | Iniciar Depuração (Debug) com pontos de interrupção (breakpoints) |
| `Alt + Shift + F` | Formatar o código atual |
| `Ctrl + B` | Ocultar / Mostrar a barra lateral esquerda |
| `Ctrl + /` | Comentar / Descomentar a linha selecionada |
| `Alt + Seta Cima/Baixo` | Mover a linha atual para cima ou para baixo |

---

## 🧪 Teste Prático: Seu Primeiro Script no VS Code

1. No VS Code, clique em **File ➔ Open Folder** e selecione uma pasta vazia.
2. Crie um arquivo chamado `teste.py`.
3. Digite o seguinte código:

```python
import sys

print("🎉 Parabéns! Seu ambiente Python está funcionando no VS Code!")
print(f"Versão do Python: {sys.version}")
```

4. Pressione `Ctrl + F5` (ou clique no botão de **Play** no canto superior direito).
5. O resultado aparecerá no **Terminal Integrado** na parte inferior!
