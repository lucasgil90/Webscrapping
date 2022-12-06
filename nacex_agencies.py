# -*- coding: latin-1 -*-#
import bs4
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import geopandas as gpd
import numpy as np

url = 'https://www.nacex.es/irCalcAgencias.do?LATITUD=40.416776&LONGITUD=-3.703495' 
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'

def extractdata(url):
    result = requests.get(url, verify=False)
    doc = BeautifulSoup(result.content, "html.parser").text
   
    #parse a json string
    data = json.loads(doc)
    
   #put json string into a list
    lista = data['agencias']

    for i in range(0, len(lista)):
        name = lista[i]['nombre']
        try:
          city = lista[i]['poblacion']
        except KeyError:
          city = np.nan
        try:
          province = lista[i]['provincia']
        except:
          province = np.nan
        address = lista[i]['direccion']
        try:
          zipcode = lista[i]['codigo_postal']
        except KeyError:
          zipcode = np.nan
        email = lista[i]['mail_operativa']
        try:
          phone = lista[i]['telefono']
        except KeyError:
          phone = np.nan
        latitude = lista[i]['latitud']
        longitude = lista[i]['longitud']
        feature = {'Hotel Name': name,
                   'city':city,
                   'province':province,
                   'Address': address,
                   'ZipCode': zipcode,
                   'E-mail': email,
                   'Phone': phone,
                   'Latitude': latitude,
                   'Longitude': longitude}
        yield feature

hotels_list = list(extractdata(url))

jsonStr = json.dumps(hotels_list)
jsonFile = open("nacex_agencies_data.json", "w")
jsonFile.write(jsonStr)
jsonFile.close()

paradores = pd.read_json("nacex_agencies_data.json")

paradores_gdf = gpd.GeoDataFrame(
    {
        "geometry": gpd.points_from_xy(
            paradores["Longitude"], paradores["Latitude"]
        )
    }, crs="EPSG:4326"
).join(paradores)


paradores_gdf.to_file("nacex_agencies.geojson", driver="GeoJSON")