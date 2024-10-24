

# importando biblioteca pandas

import pandas as pd



# Configurar o máximo de colunas a ser exibido

pd.set_option('display.max_columns', 200)



br_category_id = pd.read_json(r'C:\Users\mau_a\OneDrive\Área de Trabalho\Teste AtivGreen\Desafio\BR_category_id.json')
ca_category_id = pd.read_json(r'C:\Users\mau_a\OneDrive\Área de Trabalho\Teste AtivGreen\Desafio\CA_category_id.json')
gb_category_id = pd.read_json(r'C:\Users\mau_a\OneDrive\Área de Trabalho\Teste AtivGreen\Desafio\GB_category_id.json')
us_category_id = pd.read_json(r'C:\Users\mau_a\OneDrive\Área de Trabalho\Teste AtivGreen\Desafio\US_category_id.json')
br_youtube = pd.read_excel(r'C:\Users\mau_a\OneDrive\Área de Trabalho\Teste AtivGreen\Desafio\BR_youtube_trending_data.xlsx')
ca_youtube = pd.read_excel(r'C:\Users\mau_a\OneDrive\Área de Trabalho\Teste AtivGreen\Desafio\CA_youtube_trending_data.xlsx')
gb_youtube = pd.read_excel(r'C:\Users\mau_a\OneDrive\Área de Trabalho\Teste AtivGreen\Desafio\GB_youtube_trending_data.xlsx')
us_youtube = pd.read_excel(r'C:\Users\mau_a\OneDrive\Área de Trabalho\Teste AtivGreen\Desafio\US_youtube_trending_data.xlsx')



# Criando coluna de país

br_youtube['country'] = 'BR'
ca_youtube['country'] = 'CA'
gb_youtube['country'] = 'GB'
us_youtube['country'] = 'US'



# Unindo as tabelas e ignorando o index

youtube = pd.concat([br_youtube, ca_youtube, gb_youtube, us_youtube], ignore_index=True)



# Substituindo valores vazios por "sem informação"
youtube.fillna('sem informação')



# Salvando arquivo em csv para uso no Power BI
youtube.to_csv('youtube.csv', sep=',', index=False)

