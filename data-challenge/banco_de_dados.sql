-- ============================================================================
-- TESTE TÉCNICO SQL
-- ============================================================================
-- Autor: Maurício Marques
-- Descrição: Queries de análise de dados de produtos, lojas e vendas
-- ============================================================================


-- ============================================================================
-- QUESTÃO 1: Top 10 Produtos Mais Caros
-- ============================================================================
-- Objetivo: Identificar os 10 produtos com maior valor unitário na empresa
-- Tabela: data_product
-- Ordenação: Valor decrescente
-- ============================================================================

SELECT 
    PRODUCT_NAME AS produto,
    PRODUCT_VAL AS valor_unitario
FROM data_product 
ORDER BY PRODUCT_VAL DESC 
LIMIT 10;


-- ============================================================================
-- QUESTÃO 2: Seções por Departamento
-- ============================================================================
-- Objetivo: Listar todas as seções distintas dos departamentos BEBIDAS e PADARIA
-- Tabela: data_product
-- Agrupamento: Por departamento
-- Nota: GROUP_CONCAT agrupa múltiplas seções em uma única string
-- ============================================================================

SELECT 
    DEP_NAME AS departamento,
    GROUP_CONCAT(DISTINCT SECTION_NAME ORDER BY SECTION_NAME SEPARATOR ', ') AS secoes
FROM data_product
WHERE DEP_NAME IN ('BEBIDAS', 'PADARIA')
GROUP BY DEP_NAME
ORDER BY DEP_NAME;


-- ============================================================================
-- QUESTÃO 3: Vendas por Área de Negócio no Q1 2019
-- ============================================================================
-- Objetivo: Calcular o total de vendas em valor ($) por área de negócio
-- Período: Primeiro trimestre de 2019 (Jan-Mar)
-- Tabelas: data_store_sales (vendas) + data_store_cad (cadastro de lojas)
-- Join: Relacionamento por STORE_CODE
-- ============================================================================

SELECT 
    c.BUSINESS_NAME AS area_negocio,
    CONCAT('$', FORMAT(SUM(s.SALES_VALUE), 2)) AS total_vendas,
    FORMAT(SUM(s.SALES_VALUE), 2) AS total_vendas_numerico
FROM data_store_sales AS s
INNER JOIN data_store_cad AS c 
    ON s.STORE_CODE = c.STORE_CODE
WHERE 
    -- Filtro de período: Q1 2019 (Janeiro a Março)
    s.DATE >= '2019-01-01' 
    AND s.DATE < '2019-04-01'
GROUP BY c.BUSINESS_NAME
ORDER BY SUM(s.SALES_VALUE) DESC;


-- ============================================================================
-- QUERY ALTERNATIVA - Q3: Com Métricas Adicionais
-- ============================================================================
-- Versão expandida incluindo quantidade vendida e ticket médio
-- ============================================================================

SELECT 
    c.BUSINESS_NAME AS area_negocio,
    COUNT(DISTINCT s.STORE_CODE) AS quantidade_lojas,
    CONCAT('$', FORMAT(SUM(s.SALES_VALUE), 2)) AS total_vendas,
    FORMAT(SUM(s.SALES_QTY), 0) AS quantidade_total_vendida,
    CONCAT('$', FORMAT(SUM(s.SALES_VALUE) / SUM(s.SALES_QTY), 2)) AS ticket_medio
FROM data_store_sales AS s
INNER JOIN data_store_cad AS c 
    ON s.STORE_CODE = c.STORE_CODE
WHERE 
    s.DATE BETWEEN '2019-01-01' AND '2019-03-31'
GROUP BY c.BUSINESS_NAME
ORDER BY SUM(s.SALES_VALUE) DESC;


-- ============================================================================
-- QUERIES ADICIONAIS DE ANÁLISE
-- ============================================================================


-- ----------------------------------------------------------------------------
-- A1: Análise Mensal de Vendas por Área de Negócio (2019)
-- ----------------------------------------------------------------------------
-- Permite visualizar tendências sazonais ao longo do ano

SELECT 
    c.BUSINESS_NAME AS area_negocio,
    DATE_FORMAT(s.DATE, '%Y-%m') AS mes_ano,
    CONCAT('$', FORMAT(SUM(s.SALES_VALUE), 2)) AS vendas_mes,
    FORMAT(SUM(s.SALES_QTY), 0) AS quantidade_vendida
FROM data_store_sales AS s
INNER JOIN data_store_cad AS c 
    ON s.STORE_CODE = c.STORE_CODE
WHERE 
    YEAR(s.DATE) = 2019
GROUP BY 
    c.BUSINESS_NAME,
    DATE_FORMAT(s.DATE, '%Y-%m')
ORDER BY 
    c.BUSINESS_NAME,
    mes_ano;


-- ----------------------------------------------------------------------------
-- A2: Ranking de Lojas por Performance (Q1 2019)
-- ----------------------------------------------------------------------------
-- Identifica as lojas com melhor desempenho no primeiro trimestre

SELECT 
    c.STORE_NAME AS loja,
    c.BUSINESS_NAME AS categoria,
    CONCAT('$', FORMAT(SUM(s.SALES_VALUE), 2)) AS total_vendas,
    FORMAT(SUM(s.SALES_QTY), 0) AS quantidade_vendida,
    CONCAT('$', FORMAT(SUM(s.SALES_VALUE) / SUM(s.SALES_QTY), 2)) AS ticket_medio,
    COUNT(DISTINCT DATE(s.DATE)) AS dias_operacao
FROM data_store_sales AS s
INNER JOIN data_store_cad AS c 
    ON s.STORE_CODE = c.STORE_CODE
WHERE 
    s.DATE BETWEEN '2019-01-01' AND '2019-03-31'
GROUP BY 
    c.STORE_CODE,
    c.STORE_NAME,
    c.BUSINESS_NAME
ORDER BY 
    SUM(s.SALES_VALUE) DESC
LIMIT 20;


-- ----------------------------------------------------------------------------
-- A3: Comparação de Crescimento Q1 vs Q4 2019
-- ----------------------------------------------------------------------------
-- Analisa variação percentual entre primeiro e último trimestre

WITH vendas_q1 AS (
    SELECT 
        c.BUSINESS_NAME,
        SUM(s.SALES_VALUE) AS vendas_q1
    FROM data_store_sales AS s
    INNER JOIN data_store_cad AS c ON s.STORE_CODE = c.STORE_CODE
    WHERE s.DATE BETWEEN '2019-01-01' AND '2019-03-31'
    GROUP BY c.BUSINESS_NAME
),
vendas_q4 AS (
    SELECT 
        c.BUSINESS_NAME,
        SUM(s.SALES_VALUE) AS vendas_q4
    FROM data_store_sales AS s
    INNER JOIN data_store_cad AS c ON s.STORE_CODE = c.STORE_CODE
    WHERE s.DATE BETWEEN '2019-10-01' AND '2019-12-31'
    GROUP BY c.BUSINESS_NAME
)
SELECT 
    q1.BUSINESS_NAME AS area_negocio,
    CONCAT('$', FORMAT(q1.vendas_q1, 2)) AS vendas_q1,
    CONCAT('$', FORMAT(q4.vendas_q4, 2)) AS vendas_q4,
    CONCAT(
        FORMAT(((q4.vendas_q4 - q1.vendas_q1) / q1.vendas_q1) * 100, 2),
        '%'
    ) AS variacao_percentual
FROM vendas_q1 q1
INNER JOIN vendas_q4 q4 
    ON q1.BUSINESS_NAME = q4.BUSINESS_NAME
ORDER BY ((q4.vendas_q4 - q1.vendas_q1) / q1.vendas_q1) DESC;


-- ============================================================================
-- QUERIES DE VALIDAÇÃO E QUALIDADE DE DADOS
-- ============================================================================


-- ----------------------------------------------------------------------------
-- V1: Verificação de Integridade - Lojas sem Vendas
-- ----------------------------------------------------------------------------

SELECT 
    c.STORE_CODE,
    c.STORE_NAME,
    c.BUSINESS_NAME,
    'Sem vendas registradas' AS status
FROM data_store_cad c
LEFT JOIN data_store_sales s 
    ON c.STORE_CODE = s.STORE_CODE
WHERE s.STORE_CODE IS NULL
ORDER BY c.STORE_NAME;


-- ----------------------------------------------------------------------------
-- V2: Verificação de Dados Ausentes ou Inconsistentes
-- ----------------------------------------------------------------------------

SELECT 
    'Vendas com valores nulos' AS verificacao,
    COUNT(*) AS registros_afetados
FROM data_store_sales
WHERE SALES_VALUE IS NULL OR SALES_QTY IS NULL

UNION ALL

SELECT 
    'Vendas com valores negativos' AS verificacao,
    COUNT(*) AS registros_afetados
FROM data_store_sales
WHERE SALES_VALUE < 0 OR SALES_QTY < 0

UNION ALL

SELECT 
    'Produtos sem nome' AS verificacao,
    COUNT(*) AS registros_afetados
FROM data_product
WHERE PRODUCT_NAME IS NULL OR PRODUCT_NAME = '';


-- ============================================================================
-- NOTAS DE IMPLEMENTAÇÃO
-- ============================================================================
/*
1. Todas as queries foram otimizadas com:
   - Aliases claros e descritivos
   - Formatação consistente
   - Comentários explicativos
   - Ordenação relevante dos resultados

2. Considerações de Performance:
   - Filtros em colunas indexadas (DATE, STORE_CODE)
   - JOINs eficientes usando chaves primárias
   - GROUP BY apenas em colunas necessárias

3. Boas Práticas Aplicadas:
   - Nomes de colunas em português para clareza
   - Formatação de valores monetários
   - Ordenação lógica dos resultados
   - Validação de integridade dos dados

4. Extensibilidade:
   - Queries base podem ser facilmente adaptadas para outros períodos
   - CTEs facilitam análises mais complexas
   - Estrutura modular permite composição de queries
*/