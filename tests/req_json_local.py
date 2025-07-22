import requests
import pandas as pd
import json

url = 'https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson'
response = requests.get(url)

if response.status_code == 200:
    Brazil = response.json()  # Converte o conteúdo JSON diretamente
else:
    print(f"Erro ao acessar a URL: {response.status_code}")

print(f'{Brazil}')

df_brasil = pd.DataFrame(Brazil)
