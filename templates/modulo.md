# Módulo {{ "%02d"|format(numero) }} — {{ nome }}

> **Curso:** {{ curso_nome }}  
> **Módulo:** {{ numero }} de {{ total_modulos }}  
> **Descrição:** {{ descricao }}

---

## 📋 Visão Geral do Módulo

{{ descricao if descricao else "Este módulo apresenta conceitos fundamentais para o desenvolvimento da disciplina." }}

---

## 📚 Capítulos

{% for i in range(1, num_capitulos + 1) %}
- [ ] Capítulo {{ "%02d"|format(i) }} — *A ser definido*
{% endfor %}

---

## 🎯 Objetivos do Módulo

Ao final deste módulo, você será capaz de:

- [ ] Objetivo 1
- [ ] Objetivo 2
- [ ] Objetivo 3

---

!!! note "Organização"
    Os capítulos deste módulo foram organizados progressivamente.
    Recomendamos seguir a ordem indicada.
