#!/usr/bin/env python
# coding: utf-8

# #### Carregando as bases

# In[1]:


import pandas as pd


caminho_dados = r'C:\Users\mau_a\OneDrive\Área de Trabalho\Python 2024\teste_principia-main\dados.xlsx'
caminho_sistema = r'C:\Users\mau_a\OneDrive\Área de Trabalho\Python 2024\teste_principia-main\sistema.xlsx'


dados = pd.read_excel(caminho_dados)
sistema = pd.read_excel(caminho_sistema)


#  não conseguimos ler o arquivo json em função do comprimento distinto dos arrays
# dados_json = pd.read_json('dados.json')


# abriremos o arquivo dados.json do seguinte modo:

import json

with open('dados.json', 'r') as f:
    cliente = json.load(f)


# #### 1) O CPF do cliente é válido?

# In[2]:


# Script para validação do CPF

def validar_cpf(cpf):
    # Remove caracteres não numéricos
    cpf = ''.join(filter(str.isdigit, cpf))
    
    # Verifica o comprimento
    if len(cpf) != 11:
        return False

    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return False

    # Função para calcular o dígito verificador
    def calcular_digito(cpf, pesos):
        soma = sum(int(cpf[i]) * pesos[i] for i in range(len(pesos)))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    # Calcula os dois dígitos verificadores
    pesos_1 = list(range(10, 1, -1))
    digito1 = calcular_digito(cpf[:9], pesos_1)
    
    pesos_2 = list(range(11, 1, -1))
    digito2 = calcular_digito(cpf[:10], pesos_2)

    # Verifica se os dígitos verificadores estão corretos
    return cpf[-2:] == f"{digito1}{digito2}"


if validar_cpf(cliente['cpf']) == False:
    print('O cpf do cliente é inválido')
else:
    print('O cpf do cliente é válido')


# #### 2) O cliente possui nome completo ?

# In[3]:


cliente['nome']


# RESPOSTA: Sim, seu nome completo é "Lucas da Silva"

# #### 3) A data de nascimento é válida? É uma idade possível? (Maiores de 17 anos)

# In[4]:


# Script para cálculo de idade

from datetime import datetime

def calcular_idade(data_nascimento_str):
    # Obtém a data de hoje
    hoje = datetime.now()

    # Converte a string da data de nascimento para um objeto datetime
    data_nascimento = datetime.strptime(data_nascimento_str, "%Y-%m-%d")
    
    # Calcula a idade inicial com base na diferença de anos
    idade = hoje.year - data_nascimento.year

    # Ajusta a idade se o aniversário ainda não ocorreu neste ano
    if (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day):
        idade -= 1

    return idade


# Calcula a idade usando a data de nascimento do dicionário
idade = calcular_idade(cliente['dataNascimento'])

# Exibe a idade calculada
print("Idade:", idade)


# #### 4) O email é válido?

# In[5]:


cliente['emails']


# In[6]:


sistema.head()


# Considerando que os emails presentes em "sistema.xlsx" verificamos que os emails tem sempre o nome de uma empresa ou instituição após o @, desta forma o email do "Lucas Silva" parece um email pessoal e não corporativo

# #### 5) O Telefone informado esta no formato certo?

# In[7]:


cliente['telefones']


# In[8]:


# Script para verificar se o telefone é válido

import re

def validar_numero_telefone(telefone):
    # Define o padrão para validação de telefone celular no Brasil
    padrao = re.compile(r'^\d{2}\d{9}$')

    # Verifica se o telefone corresponde ao padrão
    if padrao.match(telefone):
        return True
    else:
        return False

def verificar_dados_telefone(dados):
    for item in dados:
        tipo = item.get('tipo')
        ddd = item.get('ddd')
        telefone = item.get('telefone')

        if tipo != 'CELULAR':
            print("Tipo de telefone não é CELULAR.")
            continue
        
        # Verifica se o DDD tem exatamente 2 dígitos e o telefone tem exatamente 9 dígitos
        if len(ddd) != 2 or not ddd.isdigit():
            print(f"DDD inválido: {ddd}")
            continue
        
        if len(telefone) != 9 or not telefone.isdigit():
            print(f"Número de telefone inválido: {telefone}")
            continue
        
        # Verifica se o número completo é válido
        numero_completo = ddd + telefone
        if validar_numero_telefone(numero_completo):
            print(f"Número de telefone {ddd}-{telefone} é válido.")
        else:
            print(f"Número de telefone {ddd}-{telefone} é inválido.")


# Verifica os dados dos números de telefone
verificar_dados_telefone(cliente['telefones'])


# #### 6) Valide o CEP e Endereço informados, utlizando-se da API: https://viacep.com.br/

# In[24]:


import requests

def consultar_cep(cep):
    # URL base da API do ViaCEP
    url = f'https://viacep.com.br/ws/{cep}/json/'
    
    try:
        # Faz a requisição GET para a API
        resposta = requests.get(url)
        
        # Verifica se a resposta foi bem-sucedida
        resposta.raise_for_status()
        
        # Converte a resposta em JSON
        resposta_json = resposta.json()
        
        # Retorna os dados
        return resposta_json

    except requests.RequestException as e:
        print(f"Erro ao fazer a requisição: {e}")
        return None

def main():
    # Obtém o CEP do usuário
    cep = input("Digite o CEP (somente números): ")
    
    # Valida se o CEP tem exatamente 8 dígitos
    if len(cep) != 8 or not cep.isdigit():
        print("CEP inválido. O CEP deve ter exatamente 8 dígitos numéricos.")
        return

    # Consulta o CEP
    resposta_json = consultar_cep(cep)

    if resposta_json:
        # Exibe os dados retornados pela API
        print(f"Logradouro: {resposta_json.get('logradouro', 'Não disponível')}")
        print(f"Bairro: {resposta_json.get('bairro', 'Não disponível')}")
        print(f"Cidade: {resposta_json.get('localidade', 'Não disponível')}")
        print(f"Estado: {resposta_json.get('uf', 'Não disponível')}")
        print(f"CEP: {resposta_json.get('cep', 'Não disponível')}")
    else:
        print("Não foi possível obter os dados para o CEP fornecido.")

if __name__ == "__main__":
    main()


# #### 7) Após essas verificações lhe foi dado um modelo da base que se encontra em um determinado sistema ("sistema.xlsx"), os clientes que você recebeu são novos clientes? Quem já está na base? É necessário atualizar os dados? 

# In[10]:


# Renomeia-se a coluna 'CPF' para 'cpf' deixando as colunas de cpf em sistemas e dados com o mesmo nome

dados.rename(columns={'CPF': 'cpf'}, inplace=True)


# In[11]:


# Realizaremos um inner join para verificar se existem valores repetidos de CPF

def repetidos(sistema, dados):
    pd.merge(sistema, dados, how='inner', on='cpf')
    return repetidos


# Encontramos o "César Roberto Castro", já cadastrado em nosso sistema, logo os demais clientes precisam ser inseridos no sistema ainda

# #### Salvando em JSON os clientes que precisam ser inseridos na base

# In[25]:


# Identifica clientes no arquivo dados que não são comuns ao arquivo sistema
clientes_nao_comuns_sistema = dados[~dados['cpf'].isin(sistema['cpf'])]

# Salva o resultado em um arquivo JSON
clientes_nao_comuns_sistema.to_json('clientes_nao_comuns_sistema.json', orient='records', lines=True)

print("Arquivo JSON criado com sucesso!")


# #### Salvando em XLSX os clientes que não precisam ser inseridos na base

# In[34]:


# Identifica clientes no arquivo dados que  são comuns ao arquivo sistema
clientes_comuns_sistema = dados[dados['cpf'].isin(sistema['cpf'])]

# Salva o resultado em um arquivo Excel
clientes_comuns_sistema.to_excel('clientes_comuns_sistema.xlsx', index=False)

