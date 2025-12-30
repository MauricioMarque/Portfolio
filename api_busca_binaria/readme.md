# 📚 Buscador de Livros: Google Books API & Busca Binária

Este projeto é uma ferramenta de linha de comando (CLI) desenvolvida em Python que permite buscar obras literárias de autores específicos utilizando a **Google Books API**. O projeto foca na demonstração de habilidades de consumo de APIs, tratamento de dados JSON e implementação de algoritmos fundamentais.

## 🎯 Objetivos do Projeto
- **Consumo de API REST**: Realizar requisições HTTP seguras e eficientes.
- **Tratamento de Dados**: Filtrar e organizar informações extraídas de estruturas JSON complexas.
- **Algoritmos Clássicos**: 
    - **Ordenação**: Organizar os resultados alfabeticamente.
    - **Busca Binária**: Implementar um algoritmo de busca com complexidade logarítmica $O(\log n)$ para encontrar títulos específicos dentro da lista.

## 🛠️ Tecnologias Utilizadas
- **Linguagem**: Python 3.x
- **Bibliotecas**: 
  - `requests`: Para comunicação com o servidor do Google.
- **Fonte de Dados**: [Google Books API](https://developers.google.com/books)

## 🧠 Lógica de Funcionamento

1. **Coleta**: O usuário insere o nome de um autor e o script consulta a API usando o parâmetro `inauthor`.
2. **Normalização**: O script percorre os itens retornados, tratando casos onde o preço ou a moeda não estão disponíveis (exibindo "Não à venda").
3. **Ordenação**: Antes de exibir os resultados, a lista é ordenada pelo título. Isso é um pré-requisito essencial para o funcionamento da **Busca Binária**.
4. **Eficiência**: Com a lista ordenada, o sistema está pronto para realizar buscas rápidas de títulos específicos sem precisar percorrer todos os itens sequencialmente.

## 🚀 Como Executar

1. **Clone este repositório:**
   ```bash
   git clone