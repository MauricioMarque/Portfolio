# 🎯 Looqbox Data Challenge

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![SQL](https://img.shields.io/badge/SQL-MySQL-orange.svg)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-green.svg)
![Plotly](https://img.shields.io/badge/Plotly-5.0+-red.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-yellow.svg)

**Análise de Dados de Vendas e Produtos com Python e SQL**

[Sobre](#-sobre-o-projeto) • [Desafios](#-desafios) • [Tecnologias](#-tecnologias) • [Instalação](#-instalação) • [Resultados](#-resultados) • [Contato](#-contato)

</div>

---

## 📋 Sobre o Projeto

Este projeto foi desenvolvido como parte de um desafio técnico de análise de dados, envolvendo **consultas SQL complexas**, **manipulação de dados com Pandas** e **visualizações interativas com Plotly**. O objetivo é demonstrar habilidades em engenharia de dados, análise exploratória e desenvolvimento de soluções escaláveis.

### 🎓 Contexto

Uma empresa de varejo necessita de soluções de dados para:
- Automatizar consultas repetitivas ao banco de dados
- Visualizar métricas de performance de lojas
- Extrair insights estratégicos de dados de entretenimento

---

## 🔄 Pipeline do Projeto

```
┌─────────────────────────────────────────────────────────────────────┐
│                         DATA PIPELINE                        
└─────────────────────────────────────────────────────────────────────┘

┌──────────────┐        ┌──────────────┐        ┌──────────────┐
│              │        │              │        │              │
│   MySQL DB   │───────▶│  SQLAlchemy  │───────▶│    Pandas    │
│              │        │  Connection  │        │  Processing  │
│ • Produtos   │        │              │        │              │
│ • Lojas      │        └──────────────┘        │ • Limpeza    │
│ • Vendas     │                                │ • Transform  │
│ • Filmes     │                                │ • Agregação  │
└──────────────┘                                └──────┬───────┘
                                                       │
                   ┌───────────────────────────────────┘
                   │
                   ▼
    ┌──────────────────────────────┐         ┌─────────────────┐
    │                              │         │                 │
    │   Análise & Visualização     │────────▶│    Insights     │
    │                              │         │   de Negócio    │
    │ • Plotly (Interativo)        │         │                 │
    │ • Métricas Calculadas        │         │ • Relatórios    │
    │ • Dashboards                 │         │ • Recomendações │
    │                              │         │                 │
    └──────────────────────────────┘         └─────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    OUTPUTS & ENTREGÁVEIS                             │
├─────────────────────────────────────────────────────────────────────┤
│  ✓ Função Python Reutilizável (retrieve_data)                       │
│  ✓ Queries SQL Otimizadas                                           │
│  ✓ Visualizações Interativas                                        │
│  ✓ Análise Estatística Completa                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Desafios

### **Challenge 1: Função Dinâmica de Consulta ao Banco**

**Problema**: A equipe de desenvolvimento estava cansada de criar queries similares apenas variando filtros.

**Solução**: Desenvolvimento de uma função Python genérica e reutilizável.

```python
def retrieve_data(product_code: int, store_code: int, dates: List[str]) -> pd.DataFrame
```

**Características**:
- ✅ Parametrização completa
- ✅ Validação de entrada
- ✅ Queries SQL parametrizadas (proteção contra SQL Injection)
- ✅ Documentação profissional (docstrings)
- ✅ Tratamento de erros robusto
- ✅ Type hints para clareza

**Exemplo de Uso**:
```python
data = retrieve_data(
    product_code=18,
    store_code=1,
    dates=['2019-01-01', '2019-01-02']
)
```

---

### **Challenge 2: Visualização de Ticket Médio**

**Problema**: Cliente solicitou visualização do ticket médio por loja e categoria no último trimestre de 2019.

**Restrições**:
- Usar queries fornecidas sem modificação
- Período: Out-Dez 2019
- Calcular TM = Valor Total / Quantidade

**Pipeline de Processamento**:

```
Query 1 (Lojas)  ─┐
                  ├─▶ MERGE ─▶ Filtro Temporal ─▶ Cálculo TM ─▶ Agregação
Query 2 (Vendas) ─┘
```

**Tecnologias Utilizadas**:
- Pandas para manipulação
- Merge de múltiplas fontes
- Agregação com groupby
- Cálculos de métricas financeiras

**Resultado**: DataFrame estruturado com TM por Loja e Categoria

---

### **Challenge 3: Análise Exploratória IMDB**

**Objetivo**: Criar visualização relevante usando dados de 1.000 filmes do IMDB.

**Escolha**: Gráfico de Dispersão - **Avaliação Crítica vs Sucesso Comercial**

#### Por que esta visualização?

1. **Insights Estratégicos**: Identifica padrões entre qualidade percebida (rating) e performance financeira (receita)
2. **Múltiplas Dimensões**: Visualiza simultaneamente 5+ variáveis
3. **Interatividade**: Exploração detalhada com hover
4. **Aplicabilidade**: Útil para estúdios, produtores e investidores

#### Dimensões Visualizadas:
- **Eixo X**: Rating médio (crítica)
- **Eixo Y**: Receita em milhões USD
- **Tamanho**: Quantidade de votos (popularidade)
- **Cor**: Gradiente de receita
- **Hover**: Título, gênero, diretor, ano

**Descobertas**:
- ✓ Filmes de franquia dominam receita independente do rating
- ✓ Correlação fraca entre crítica e sucesso comercial
- ✓ Identificação de filmes subestimados (alto rating, baixa receita)

---

## 🛠 Tecnologias

### Core Stack

| Tecnologia | Versão | Uso |
|-----------|---------|-----|
| **Python** | 3.9+ | Linguagem principal |
| **Pandas** | 2.0+ | Manipulação de dados |
| **SQLAlchemy** | 2.0+ | ORM e conexão DB |
| **PyMySQL** | 1.0+ | Driver MySQL |
| **Plotly** | 5.0+ | Visualizações interativas |
| **MySQL** | 8.0+ | Banco de dados |

### Bibliotecas Auxiliares

```python
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text
from typing import List, Optional
```

---

## 📥 Instalação

### Pré-requisitos

- Python 3.9+
- Acesso ao banco MySQL (credenciais fornecidas)
- Jupyter Notebook ou JupyterLab
```

---

## 📊 Estrutura do Projeto

```
data-challenge/
│
├── 📓 notebook.ipynb  # Notebook principal
├── 📄 banco_de_dados.sql       # Queries SQL
├── 📖 README.md                              # Documentação
└── 📁 pipeline                               # Visualizações exportadas
```

---

## 🎯 Resultados

### Métricas de Qualidade do Código

- ✅ **Documentação**: 100% das funções com docstrings
- ✅ **Type Hints**: Todas as funções tipadas
- ✅ **Modularidade**: Código organizado em funções reutilizáveis
- ✅ **Segurança**: Queries parametrizadas (SQL Injection-proof)
- ✅ **Performance**: Otimizado para grandes volumes de dados

### Entregas

| Item | Status | Descrição |
|------|--------|-----------|
| Função Python | ✅ | `retrieve_data()` completa e testada |
| SQL Queries | ✅ | 3 queries principais + 5 análises bônus |
| Visualizações | ✅ | Gráfico interativo com insights |
| Documentação | ✅ | README + comentários em código |

---

## 💡 Principais Aprendizados

### Técnicos
- Desenvolvimento de código production-ready
- Integração Python + SQL com SQLAlchemy
- Visualizações interativas com Plotly
- Boas práticas de documentação

### Analíticos
- Análise de métricas de varejo (Ticket Médio)
- Exploração de dados multidimensionais
- Identificação de insights de negócio

### Soft Skills
- Resolução de problemas complexos
- Comunicação técnica clara
- Pensamento orientado a produto

---

## 🔍 Análises SQL Disponíveis

### Queries Principais

1. **Top 10 Produtos Mais Caros**
   - Ordenação por valor unitário
   
2. **Seções por Departamento**
   - Agregação com GROUP_CONCAT
   - Foco em BEBIDAS e PADARIA

3. **Vendas por Área de Negócio (Q1 2019)**
   - JOIN entre vendas e cadastro
   - Agregação temporal

### Queries Bônus

4. **Análise Mensal de Vendas**
   - Tendências sazonais por categoria
   
5. **Ranking de Lojas**
   - Performance comparativa
   
6. **Crescimento Trimestral**
   - CTE para comparação Q1 vs Q4
   
7. **Validação de Integridade**
   - Identificação de inconsistências

---

## 📈 Exemplos de Visualização

### Gráfico de Dispersão - Filmes IMDB

**Características**:
- 🎨 Coloração por receita (escala Viridis)
- 📏 Tamanho dos pontos = quantidade de votos
- 🔍 Hover com 5+ informações
- 📊 Top 30 filmes por receita

**Insights Extraídos**:
```
✓ Filmes com avaliação ≥ 8.0: 5 filmes
✓ Filmes com receita ≥ $500M: 8 filmes
✓ Receita Média: $387.5M
✓ Avaliação Média: 7.4
```

---

## 🚀 Próximos Passos

- [ ] Implementar testes unitários (pytest)
- [ ] Criar API REST com FastAPI
- [ ] Dashboard interativo com Streamlit
- [ ] Pipeline de ETL automatizado (Airflow)
- [ ] Dockerização do ambiente

---

## 📄 Licença

Este projeto foi desenvolvido como parte de um desafio técnico e está disponível para fins educacionais.

---

<div align="center">

**⭐ Se este projeto foi útil, considere dar uma estrela!**

</div>