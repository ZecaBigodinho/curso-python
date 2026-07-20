# 🧪 Laboratório Prático: {{ nome_laboratorio | default('Nome do Lab') }}

> **Tipo:** Step-by-Step Guidado  
> **Tempo estimado:** 30–45 min

Neste laboratório, vamos construir juntos uma solução. Siga cada passo atentamente, executando e compreendendo o código antes de prosseguir.

---

## 🛠️ Passo 1: Preparação do Ambiente

Antes de escrever a lógica principal, precisamos configurar o arquivo inicial.

1. Crie um arquivo chamado `app.py`.
2. Adicione as importações necessárias:

```python
import os
import json
```

!!! warning "Verificação"
    Execute o arquivo apenas para garantir que não há erros de importação (ex: biblioteca faltando).

---

## 🚧 Passo 2: Implementando a Base

Agora vamos criar a função principal que fará a primeira parte do trabalho.

```python
def carregar_dados(caminho):
    # Insira o código base aqui
    pass
```

**O que isso faz:**
Explique de forma detalhada o que a função acima é responsável por fazer.

---

## 🧩 Passo 3: Adicionando a Regra de Negócio

Vamos evoluir nosso código inserindo a lógica principal:

```python
def carregar_dados(caminho):
    if not os.path.exists(caminho):
        return []
    
    with open(caminho, 'r', encoding='utf-8') as f:
        return json.load(f)
```

!!! tip "Dica de Boas Práticas"
    O uso do bloco `with` garante que o arquivo seja fechado corretamente mesmo que ocorra um erro durante a leitura.

---

## ✅ Passo 4: Testando o Resultado

Para finalizar nosso laboratório, vamos chamar a função e verificar o resultado no terminal.

```python
if __name__ == "__main__":
    dados = carregar_dados("dados.json")
    print(f"Total de registros carregados: {len(dados)}")
```

**Resultado esperado no terminal:**
```text
Total de registros carregados: 0
```

---

## 🏆 Conclusão do Laboratório

Parabéns! Você construiu a estrutura base com sucesso.

**Explore mais:**
O que aconteceria se o arquivo não fosse um JSON válido? Tente modificar o código para adicionar um bloco `try/except` capturando o `json.JSONDecodeError`.
