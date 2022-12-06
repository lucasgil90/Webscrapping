from re import X
import bs4
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import geopandas as gpd
import numpy as np
import openpyxl
import time


#add excel file to interpreter into a list
#wb = openpyxl.load_workbook('C:\WS\puntopack\impost_uk.xlsx')
#ws = wb['LAT']
#ws2 = wb['LONG']
lista_LAT = list(np.arange(49.6099999999959,59.40999999999,0.1))
lista_LONG = list(np.arange(-10.65999999999,1.94000000001,0.1))

#add zipcodes to baseurl and put them into a list
links=[]
cont=0

url = 'https://api-uk-points.easypack24.net/v1/points?relative_point='
n_url =''

for i in lista_LAT:
    n_url = str(url) + str(i) + str('%2C') 
    for x in lista_LONG:
        n_url2 = n_url + str(x) + str('&max_distance=999999999&limit=500') 
        links.append(n_url2)
cant_links = len(links)

pp_lista =[]

    cont=cont+1
    no_data = False
        
    requests.adapters.DEFAULT_RETRIES = 99 # increase retries number
    s = requests.session()
    s.keep_alive = False # disable keep alive

    req = s.get(link, timeout=None ,headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'})
    soup = BeautifulSoup(req.text,"html.parser")
                #parse a json string
    data = json.loads(str(soup))
    prueba = data['items']
    data_len = len(prueba)        
                #Avoid data that is empty
    if data_len == 0:
        no_data = True
        continue 
                #building the dictionary
    else:
        
        if int(cont) % 500 == 0:
            for i in range(data_len):
                        try:
                            name = data['items'][i]['name']
                        except:
                            name = np.nan
                        try:
                            adress = data['items'][i]['address_details']['street']
                        except KeyError:
                            adress = np.nan
                        try:
                            zipcode = data['items'][i]['address_details']['post_code']
                        except KeyError:
                            zipcode = np.nan
                        try:
                            city = data['items'][i]['address_details']['city']
                        except:
                            city = np.nan
                        try:
                            country = data['items'][i]['address_details']['province']
                        except KeyError:
                            country = np.nan
                        try:
                            latitude = data['items'][i]['location']['latitude']
                        except KeyError: 
                            latitude = np.nan
                        try:
                            longitude = data['items'][i]['location']['longitude']
                        except KeyError:
                            longitude = np.nan
                        try:
                            hours= data['items'][i]['opening_hours']
                        except KeyError: 
                            hours= np.nan

                        feature = {
                                'Name':name,
                                'City':city,
                                'Country':country,
                                'Address': adress,
                                'ZipCode': zipcode,
                                'Latitude': latitude,
                                'Longitude': longitude,
                                'Opening_hours': hours
                                }
            
                     #add dicc to the list
                        pp_lista.append(feature)
                        
                    
            
            print(cont,'from',cant_links)
            time.sleep(20)
        
        else:
            for i in range(data_len):
                        try:
                            name = data['items'][i]['name']
                        except:
                            name = np.nan
                        try:
                            adress = data['items'][i]['address_details']['street']
                        except KeyError:
                            adress = np.nan
                        try:
                            zipcode = data['items'][i]['address_details']['post_code']
                        except KeyError:
                            zipcode = np.nan
                        try:
                            city = data['items'][i]['address_details']['city']
                        except:
                            city = np.nan
                        try:
                            country = data['items'][i]['address_details']['province']
                        except KeyError:
                            country = np.nan
                        try:
                            latitude = data['items'][i]['location']['latitude']
                        except KeyError: 
                            latitude = np.nan
                        try:
                            longitude = data['items'][i]['location']['longitude']
                        except KeyError:
                            longitude = np.nan
                        try:
                            hours= data['items'][i]['opening_hours']
                        except KeyError: 
                            hours= np.nan

                        feature = {
                                'Name':name,
                                'City':city,
                                'Country':country,
                                'Address': adress,
                                'ZipCode': zipcode,
                                'Latitude': latitude,
                                'Longitude': longitude,
                                'Opening_hours': hours
                                }
            
                     #add dicc to the list
                        pp_lista.append(feature)
                        
                    
            print(cont,'from',cant_links)

            

#Get json file
print('Filtering')

pp_dg = pd.DataFrame(pp_lista)
before =len(pp_dg)
print(pp_dg.duplicated(subset=['Longitude']).sum())
mask = pp_dg.duplicated(subset=['Name'])
df = pp_dg[~mask]
after = len(df)
pp_str = pd.DataFrame.to_json(df)

jsonFile = open("C:\WS\puntopack\puntopack_UK_data.json", "w")
jsonFile.write(pp_str)
jsonFile.close()

pp = pd.read_json("C:\WS\puntopack\puntopack_UK_data.json")

#Georef
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))

gdf.to_file("C:\WS\puntopack\puntopack_UK.geojson", driver="GeoJSON")
print('The program has finished,filtered:',after,'total:',before, 'percentaje filtered:',(after/before)*100)