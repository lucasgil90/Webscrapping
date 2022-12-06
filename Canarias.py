import re 
import bs4
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import geopandas as gpd
import numpy as np
import time

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'

url = "https://www.holaislascanarias.com/alojamientos/?limit=48&resource_type=a_alojamiento&page="

lista_pag = list(np.arange(12,20))

links=[]
for i in lista_pag:
    n_url = str(url) + str(i)
    links.append(n_url)

for link in links:
    try:
            result = requests.get(url, headers={'user-agent': user_agent})
            doc = BeautifulSoup(result.text, "html.parser")
            hotels = doc.find_all('div',{'class':'field_others'})
            
            for item in hotels:
                lat=''
                lon=''
                try:
                    title = item.find('div',{'class':'address'}).get_text().replace(' ','').replace('\r','').replace('\n','')
                except KeyError:
                    title = np.nan
                try:
                    loc = item.find('div',{'class':'localidad'}).get_text().replace(' ','').replace('\r','').replace('\n','')
                except KeyError:
                    loc = np.nan
                try:
                    phone = item.find('div',{'class':'phone-number'}).text.replace(' ','').replace('\r','').replace('\n','')
                except AttributeError:
                    phone = np.nan
                try:
                    mail = item.find('div',{'class':'email'}).text.replace(' ','').replace('\r','').replace('\n','')
                except AttributeError:
                    mail = np.nan
                try:

                    coords = re.findall(r'-?\d+\.\d+', str(item.find('div',{'class':'field_links'},{'href'})))
                    coords = [float(coord) for coord in coords]
                    lat,lon = coords
                    

                        

                except KeyError:
                    coords = np.nan
                except ValueError:
                    coords = np.nan

                
                    
                hotel = {'address': title,
                        'location':loc,
                        'phone':phone,
                        'email':mail,
                        'lat': lat,
                        'lon':lon }

                print(hotel)
    except UnicodeDecodeError:
        print('No se puede scrapear')
time.sleep(5)
