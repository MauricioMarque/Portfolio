#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Instalando biblioteca para leitura de arquivo xlsb

# pip install pandas pyxlsb


# In[2]:


# Importando pandas
import pandas as pd

# Caminho para o seu arquivo .xlsb
caminho = r'C:\Users\mau_a\OneDrive\Área de Trabalho\Base Case.xlsb'

# Ler a planilha do arquivo .xlsb
df = pd.read_excel(caminho, engine='pyxlsb', sheet_name='BASE MOTORISTAS')

# Mostrar o DataFrame
print(df)


# In[3]:


from sklearn.preprocessing import MinMaxScaler


# Normalização das variáveis
scaler = MinMaxScaler()

# Normalizar as variáveis relevantes
variaveis = [
    'Horas Online (h)',
    'Taxa de Aceitação de Corridas (%)',
    'Corridas (#)',
    'Valor Total Produzido ($)',
    'Distância Percorrida (m)',
    'Taxa de Ocupação'
]

df_normalizado = df.copy()
df_normalizado[variaveis] = scaler.fit_transform(df[variaveis])

# Definir pesos para cada variável com base na importância
pesos = {
    'Horas Online (h)': 0.1,
    'Taxa de Aceitação de Corridas (%)': 0.2,
    'Corridas (#)': 0.2,
    'Valor Total Produzido ($)': 0.2,
    'Distância Percorrida (m)': 0.1,
    'Taxa de Ocupação': 0.2
}

# Calcular a nota para cada motorista
df_normalizado['Nota'] = (
    df_normalizado['Horas Online (h)'] * pesos['Horas Online (h)'] +
    df_normalizado['Taxa de Aceitação de Corridas (%)'] * pesos['Taxa de Aceitação de Corridas (%)'] +
    df_normalizado['Corridas (#)'] * pesos['Corridas (#)'] +
    df_normalizado['Valor Total Produzido ($)'] * pesos['Valor Total Produzido ($)'] +
    df_normalizado['Distância Percorrida (m)'] * pesos['Distância Percorrida (m)'] +
    df_normalizado['Taxa de Ocupação'] * pesos['Taxa de Ocupação']
)


# Convertendo nota de 0-1 para 0-10
df_normalizado['Nota'] = df_normalizado['Nota']*10

# Exibir o DataFrame com as notas
print(df_normalizado[['Código Motorista', 'Nota']])


# In[4]:


df_notas = df_normalizado[['Código Motorista', 'Nota']]


# In[7]:


df_notas.to_excel('df_notas.xlsx', index=False)


# In[ ]:




