# %% [markdown]
# # **REDES NEURAIS ARTIFICIAIS: CLASSIFICAÇÃO**

# %% [markdown]
# Este projeto tem por objetivo desenvolver um algoritmo de Machine Learning para prever a tendência de uma pessoa desenvolver algum tipo de doença cardíaca com base em alguns fatores clínicos e laboratoriais. 

# %% [markdown]
# Os dados foram extraídos do site do Kaggle:
# 
# https://www.kaggle.com/fedesoriano/heart-failure-prediction/version/1

# %%
import numpy as np
import pandas as pd
import pickle
import streamlit as st

# %%
df = pd.read_csv(r'C:\Users\mau_a\OneDrive\Área de Trabalho\python\ml_udemy\6. classificacao_redes_neurais\heart_tratado.csv',
                    sep=';', encoding='iso-8859-1')

# %%
df2 = pd.DataFrame.copy(df)

# %%
df2['Sex'].replace({'M':0, 'F': 1}, inplace=True)
df2['ChestPainType'].replace({'TA':0, 'ATA': 1, 'NAP':2, 'ASY': 3}, inplace=True)
df2['RestingECG'].replace({'Normal':0, 'ST': 1, 'LVH':2}, inplace=True)
df2['ExerciseAngina'].replace({'N':0, 'Y': 1}, inplace=True)
df2['ST_Slope'].replace({'Up':0, 'Flat': 1, 'Down':2}, inplace=True)

# %% [markdown]
# ## **ATRIBUTOS PREVISORES E ALVO**

# %%
previsores = df2.iloc[:, 0:11].values  # quando usamos values temos array de 2 dimensões


# %%
alvo = df.iloc[:, 11].values

# %% [markdown]
# ## **RESUMO PRÉ-PROCESSAMENTO**

# %% [markdown]
# alvo = variável que se pretende atingir (tem ou não doença cardíaca).
# 
# previsores = conjunto de variáveis previsoras com as variáveis categóricas transformadas em numéricas manualmente, sem escalonar.
# 
# previsores_esc = conjunto de variáveis previsoras com as variáveis categóricas transformadas em numéricas, escalonada.
# 
# previsores2 = conjunto de variáveis previsoras com as variáveis categóricas transformadas em numéricas pelo labelencoder.
# 
# previsores3 = conjunto de variáveis previsoras transformadas pelo labelencoder e onehotencoder, sem escalonar.
# 
# previsores3_esc = conjunto de variáveis previsoras transformadas pelo labelencoder e onehotencoder escalonada.

# %% [markdown]
# ## **BASE DE TREINO E TESTE**

# %%
from sklearn.model_selection import train_test_split

# %%
x_treino, x_teste, y_treino, y_teste = train_test_split(previsores, alvo, test_size = 0.3, random_state = 0)

# %% [markdown]
# # **CRIAÇÃO DO ALGORITMO**

# %%
from sklearn.neural_network import MLPClassifier

# %%
redes = MLPClassifier(hidden_layer_sizes=(7), activation='relu', solver='adam', max_iter =800,
                              tol=0.0001, random_state = 3, verbose = True)
                               

# %%
redes.fit(x_treino, y_treino)

# %%
previsoes = redes.predict(x_teste)

# %%
# Criando o modelo
modelo = redes


# %%
# Salvando o modelo
with open('modelo.pkl', 'wb') as f:
    pickle.dump(modelo, f)

# %%
# Carregar o modelo
with open('modelo.pkl', 'rb') as file:
    modelo = pickle.load(file)

# Título do aplicativo
st.title("Classificação de Modelo")

# Inputs do usuário
st.header("Insira as informações dos preditores")

# Supondo que seu modelo tenha 3 preditores
age = st.number_input("Age", min_value=0)
sex = st.number_input("Sex", min_value=0)
chestpaintype = st.number_input("Chest pain type", min_value=0)
restingbp = st.number_input("Resting BP", min_value=0)
cholesterol = st.number_input("Cholesterol", min_value=0)
fastingbs = st.number_input("Fasting BS", min_value=0)
restingecg = st.number_input("Resting ECG", min_value=0)
maxhr = st.number_input("Max HR", min_value=0)
exerciseangina = st.number_input("Exercise Angina", min_value=0)
oldpeak = st.number_input("Oldpeak", min_value=0)
st_slope = st.number_input("ST Slope", min_value=0)

# Botão para fazer a previsão
if st.button("Prever"):
    # Preparar os dados para o modelo
    input_data = np.array([[age, sex, chestpaintype, restingbp, cholesterol, fastingbs, restingecg, maxhr, exerciseangina, oldpeak, st_slope]])
    
    # Fazer a previsão
    prediction = modelo.predict(input_data)

    # Exibir o resultado
    st.success(f"A previsão é: {prediction[0]}")



