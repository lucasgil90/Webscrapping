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
    lista = data['nxshop_agencias']

    for i in range(0, len(lista)):
        name = lista[i]['shop_nombre']
        try:
          city = lista[i]['pueb_codigo_nombre']
        except KeyError:
          city = np.nan 
        province = lista[i]['prov_codigo_nombre']
        address = lista[i]['shop_direccion']
        try:
          zipcode = lista[i]['pueb_codigo_postal']
        except KeyError:
          zipcode = np.nan
        try:
          email = lista[i]['shop_email']
        except KeyError:
          email = np.nan
        try:
          phone = lista[i]['shop_telefono']
        except KeyError:
          phone = np.nan
        latitude = lista[i]['shop_mapa_latitud']
        longitude = lista[i]['shop_mapa_longitud']
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

agencies_list = list(extractdata(url))

jsonStr = json.dumps(agencies_list)
jsonFile = open("nacex_nxshop_agencies_data.json", "w")
jsonFile.write(jsonStr)
jsonFile.close()  

nacex = pd.read_json("nacex_nxshop_agencies_data.json")

nacex_gdf = gpd.GeoDataFrame(
    {
        "geometry": gpd.points_from_xy(
            nacex["Longitude"], nacex["Latitude"]
        )
    }, crs="EPSG:4326"
).join(nacex)


nacex_gdf.to_file("nacex_nxshops_agencies.geojson", driver="GeoJSON")