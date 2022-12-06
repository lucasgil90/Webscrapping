import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.nacex.es/irCalcAgencias.do?LATITUD=40.416776&LONGITUD=-3.703495"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
}

#Print features:
response = requests.get(url, headers=headers)

#Parse data:
stores = response.json()['agencias']

for item in stores:
  try:
    print('name:',item['nombre'])
    print('adress:',item['direccion'])
    print('city:',item['poblacion'])
    print('province:',item['provincia'])
    print('zip:',item['codigo_postal'])
    print('phone:',item['telefono'])
    print('email:',item['mail_operativa'])
    print('xCoordinates:',item['longitud'])
    print('yCoordinates:',item['latitud'])
    print('\n')

  except:
    print('name:',item['nombre'])
    print('adress:',item['direccion'])
    print('-')
    print('-')
    print('-')
    print('-')
    print('email:',item['mail_operativa'])
    print('xCoordinates:',item['longitud'])
    print('yCoordinates:',item['latitud'])
    print('\n')

#Save data to csv or json:
df = pd.DataFrame(stores) 
df.to_csv('nacex.csv')

df.head()