import bs4
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import geopandas as gpd
import numpy as np

url = 'https://inpost.it/sites/default/files/points.json' 

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
'cookie':'_ga=GA1.2.1358420730.1655201715; cookiemsg=true; _gid=GA1.2.1806931279.1655718370; _gat_UA-43049027-3=1'}


def extractdata(url):
    result = requests.get(url, headers)
    doc = BeautifulSoup(result.content, "html.parser").text
   
    data = json.loads(doc)
    
    lista = data['items']

    for i in range(0, len(lista)):
        try:
          name = lista[i]['d']
        except KeyError:
          name = np.nan
        
        try:
          city = lista[i]['g']
        except KeyError:
          city = np.nan   
          
        address = lista[i]['e'] + lista[i]['b']
        
        try:
          zipcode = lista[i]['o']
        except KeyError:
          zipcode = np.nan
        try:
          open_hours = lista[i]['h']
        except:
          open_hours = np.nan

        try: 
          latitude = lista[i]['l']['a']
        except:
          latitude = np.nan
        try:
          longitude = lista[i]['l']['o']
        except:
          longitude = np.nan

        feature = {'Hotel Name': name,
                   'Address': address,
                   'ZipCode': zipcode,
                   'Open_hours': open_hours,
                   'Latitude': latitude,
                   'Longitude': longitude}
        yield feature

agencies_list = list(extractdata(url))

jsonStr = json.dumps(agencies_list)
jsonFile = open("puntopack_IT_data.json", "w")
jsonFile.write(jsonStr)
jsonFile.close()  

nacex = pd.read_json("puntopack_IT_data.json")

nacex_gdf = gpd.GeoDataFrame(
    {
        "geometry": gpd.points_from_xy(
            nacex["Longitude"], nacex["Latitude"]
        )
    }, crs="EPSG:4326"
).join(nacex)


nacex_gdf.to_file("puntopack_IT2.geojson", driver="GeoJSON")