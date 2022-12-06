import requests
import json
from shapely.geometry import MultiPolygon, Polygon, box, MultiPoint, Point
from shapely.geometry import Polygon, mapping
from shapely import wkt
import matplotlib.pyplot as plt
import openpyxl
import pandas as pd
import geopandas as gpd
import pdb

wb = openpyxl.load_workbook('C:\WS\Coor_europe_XY.xlsx')
ws = wb['Spain']
lista_zip = []
for row in ws.iter_rows():

    lista_zip.append([row[0].value,row[1].value])


dpd_list = []
for x in range(0, len(lista_zip)):

    response = requests.request("POST", 
    url = "https://carte.pickup.fr/PudoMap/GetPudoListByLongLat",
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36', 
    'Accept-Encoding': 'gzip, deflate',
     'Accept': '*/*', 
     'Connection': 'keep-alive',
     'Accept-Language': 'es,en;q=0.9,es-ES;q=0.8',
     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': '_ga=GA1.2.1205219681.1654080585; Language=en; SERVERID=s2; _gid=GA1.2.264746661.1654505919; _gat_UA-159550324-1=1',
    'Origin': 'https://carte.pickup.fr', 'Referer': 'https://carte.pickup.fr/?pudo_keyword=&lang=en',
          'Sec-Fetch-Dest': 'empty',
           'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
             'X-Requested-With': 'XMLHttpRequest',
              'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
               'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"', 
    'Content-Length': '96'},
     
    data=f"longitude={lista_zip[x][0]}&latitude={lista_zip[x][1]}&destCountryCode=ES&language=fr&pudoCount=-1&pudoType=")
    pdb.set_trace()
    
    data_ = json.loads(response.text)['pudosInfos']
    #pdb.set_trace()
    if response.text != '{"success":false}':        
        for i in range(0, len(data_)):
            name = data_[i]['PudoName']
            street_name = data_[i]['PudoAdress'].strip()
            street_number = data_[i]['PudoStreetNumber']
            postal_code = data_[i]['PudoPostaleCode']
            city = data_[i]['PudoCity']
            country = data_[i]['PudoCountry']
            lat = float(data_[i]['Latitude'])
            lon = float(data_[i]['Longitude'])
            hours = data_[0]['OpeningHours']
            opening_hours = ''
            for j in range(0,len(hours)):
                opening = str(hours[j]['Day']) + " " + str(hours[j]['AM_Begin']) + "-" + str(hours[j]['AM_End']) + "," + str(hours[j]['PM_Begin']) + "-" + str(hours[j]['PM_End']) + " " 
                opening_hours+=opening
            dpd = {
                'name': name,
                'street_name': street_name,
                'street_number': street_number,
                'postal_code': postal_code,
                'city': city,
                'country': country,
                'lat': lat,
                'lon': lon,
                'opening_hours': opening_hours
            }
            dpd_list.append(dpd)
    else:
        pass
    
df = pd.DataFrame(dpd_list)
len(dpd_list)