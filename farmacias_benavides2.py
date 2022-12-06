import pandas as pd
import json
import requests

from bs4 import BeautifulSoup
import geopandas as gpd
import time 
import numpy as np
import re


#get baseurl in postman
baseurl = 'https://farmacias-benavides-prod.ent.eastus2.azure.elastic-cloud.com/api/as/v1/engines/benavides-locations/search.json?query='


#add excel file to interpreter into a list
#wb = openpyxl.load_workbook('C:\WS\puntopack\ZIP_MEX.xlsx')
#ws = wb['Prueba']
#lista_zip = []
#for row in ws.iter_rows():
#    lista_zip.append(row[0].value)
lista_zip = list(np.arange(20000,83000,2))
#add zipcodes to baseurl and put them into a list
links=[]
cont=0
for zip in lista_zip:
    url = baseurl + str(zip)
    links.append(url)
cant_links = len(links)
#for every link get data
pp_lista = []

for link in links:
    cont=cont+1
    no_data = False
        
    requests.adapters.DEFAULT_RETRIES = 99 # increase retries number
    s = requests.session()
    s.keep_alive = False # disable keep alive

    req = s.get(link, timeout=None ,headers={'Connection':'keep-alive','user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
                    'authorization':'Bearer search-14h9b6oj7d5zdh5qy8k7a8yb'})
    soup = BeautifulSoup(req.text,"html.parser")
                #parse a json string
    try:
        data = json.loads(str(soup))
        data_len = len(data['results'])
            
          #Avoid data that is empty
    
                #building the dictionary
        if int(cont) % 200 == 0:
                for i in range(data_len):
                        try:
                            name = data['results'][i]['branch_name']['raw']
                        except KeyError:
                            name = np.nan
                        try:
                            adress = data['results'][i]['branch_street']['raw']
                        except KeyError:
                            adress = np.nan
                        try:
                            zipcode = data['results'][i]['branch_zip']['raw']
                        except KeyError:
                            zipcode = np.nan
                        try:
                            city = data['results'][i]['branch_city']['raw']
                        except:
                            city = np.nan
                        try:
                            phone = data['results'][i]['branch_phone']['raw']
                        except KeyError:
                            phone = np.nan
                        try:
                            latitude =str(data['results'][i]['branch_latitud']['raw']).strip('.')
                            latitude_list = list(latitude)
                            for item in latitude_list:
                                if item=='.':
                                    latitude_list.remove('.')
                                
                            if  latitude_list[1]=='z':
                                latitude_list.insert(3,('.'))
                                latitude = ''.join(latitude_list)
                                float(latitude2)

                            else:
                                latitude_list.insert(2,('.'))
                                latitude2 = ''.join(latitude_list)
                                float(latitude2)
                        except:
                            latitude = np.nan

                        try:
                            longitude =str(data['results'][i]['branch_longitude']['raw'])
                            longitude_list = list(longitude)

                            for item in longitude_list:
                                if item=='.':
                                    longitude_list.remove('.')

                            if  longitude_list[1]=='9':
                                longitude_list.insert(3,('.'))
                                longitude2 = ''.join(longitude_list)
                                float(longitude2)

                            else:
                                longitude_list.insert(4,('.'))
                                longitude2 = ''.join(longitude_list)
                                float(longitude2)
                                
                        except KeyError:
                            longitude = np.nan
                        try:
                            hours= 'Mon Fri:' + data['results'][i]['lu_vi_open']['raw'] + '-' + data['results'][i]['lu_vi_close']['raw'] + ' Sa:' + data['results'][i]['sa_open']['raw'] + '-' + data['results'][i]['sa_close']['raw']
                        except KeyError: 
                            hours= np.nan

                       #opening_hours =''
                       # try:
                       #     for x in range (len(hours)):
                       #         if (hours[x]['HeureFermeturePM']) == None :
                       #             opening_hours+= str(hours[x]['JourSemaine'])+ ' ' + str(hours[x]['HeureOuvertureAM']) +" - "+str(hours[x]['HeureFermetureAM'])
                       #         else:
                       #             opening_hours+= str(hours[x]['JourSemaine'])+ ' ' + str(hours[x]['HeureOuvertureAM']) +" - "+str(hours[x]['HeureFermeturePM'])+ ' break ' +\
                       #             str(hours[x]['HeureFermetureAM'])+" - "+str(hours[x]['HeureOuverturePM']) + ' '
 
                       # except TypeError:
                       #     opening_hours+= None


                        feature = {
                                'Name': name,
                                'City':city,
                                'Phone':phone,
                                'Address': adress,
                                'ZipCode': zipcode,
                                'Latitude': latitude,
                                'Longitude': longitude,
                                'Opening_hours':hours
                                }
            
                     #add dicc to the list
                        pp_lista.append(feature)
                        
                    
            
                print(cont,'from',cant_links)
                time.sleep(20)
        else:
                for i in range(data_len):
                        try:
                            name = data['results'][i]['branch_name']['raw']
                        except KeyError:
                            name = np.nan
                        try:
                            adress = data['results'][i]['branch_street']['raw']
                        except KeyError:
                            adress = np.nan
                        try:
                            zipcode = data['results'][i]['branch_zip']['raw']
                        except KeyError:
                            zipcode = np.nan
                        try:
                            city = data['results'][i]['branch_city']['raw']
                        except:
                            city = np.nan
                        try:
                            phone = data['results'][i]['branch_phone']['raw']
                        except KeyError:
                            phone = np.nan
                        try:
                            latitude =str(data['results'][i]['branch_latitud']['raw']).strip('.')
                            latitude_list = list(latitude)
                            for item in latitude_list:
                                if item=='.':
                                    latitude_list.remove('.')
                                
                            if  latitude_list[1]=='z':
                                latitude_list.insert(3,('.'))
                                latitude = ''.join(latitude_list)
                                float(latitude2)

                            else:
                                latitude_list.insert(2,('.'))
                                latitude2 = ''.join(latitude_list)
                                float(latitude2)
                           
                        except KeyError: 
                            latitude = np.nan
                        try:
                            longitude =str(data['results'][i]['branch_longitude']['raw'])
                            longitude_list = list(longitude)

                            for item in longitude_list:
                                if item=='.':
                                    longitude_list.remove('.')

                            if  longitude_list[1]=='9':
                                longitude_list.insert(3,('.'))
                                longitude2 = ''.join(longitude_list)
                                float(longitude2)

                            else:
                                longitude_list.insert(4,('.'))
                                longitude2 = ''.join(longitude_list)
                                float(longitude2)
                                
                           


                        except KeyError:
                            longitude = np.nan
                        try:
                            hours= 'Mon Fri:' + data['results'][i]['lu_vi_open']['raw'] + '-' + data['results'][i]['lu_vi_close']['raw'] + ' Sa:' + data['results'][i]['sa_open']['raw'] + '-' + data['results'][i]['sa_close']['raw']
                        except KeyError: 
                            hours= np.nan

                       #opening_hours =''
                       # try:
                       #     for x in range (len(hours)):
                       #         if (hours[x]['HeureFermeturePM']) == None :
                       #             opening_hours+= str(hours[x]['JourSemaine'])+ ' ' + str(hours[x]['HeureOuvertureAM']) +" - "+str(hours[x]['HeureFermetureAM'])
                       #         else:
                       #             opening_hours+= str(hours[x]['JourSemaine'])+ ' ' + str(hours[x]['HeureOuvertureAM']) +" - "+str(hours[x]['HeureFermeturePM'])+ ' break ' +\
                       #             str(hours[x]['HeureFermetureAM'])+" - "+str(hours[x]['HeureOuverturePM']) + ' '
 
                       # except TypeError:
                       #     opening_hours+= None


                        feature = {
                                'Name': name,
                                'City':city,
                                'Phone':phone,
                                'Address': adress,
                                'ZipCode': zipcode,
                                'Latitude': latitude2,
                                'Longitude': longitude2,
                                'Opening_hours':hours
                                }
            
                     #add dicc to the list
                        pp_lista.append(feature)
                        
                    
            
                        
                    
            
                print(cont,'from',cant_links)
    except KeyError:
        continue

#Get json file
print('Filtering')

pp_dg = pd.DataFrame(pp_lista)
before =len(pp_dg)
print(pp_dg.duplicated(subset=['Name']).sum())
mask = pp_dg.duplicated(subset=['Name'])
df = pp_dg[~mask]
after = len(df)
print(after)
pp_str = pd.DataFrame.to_json(df)


jsonFile = open('farmacias_benavides_data.json', "w")  
jsonFile.write(pp_str)
jsonFile.close()

pp = pd.read_json('farmacias_benavides_data.json')
#Georef
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))

#Get geojson file
gdf.to_file("farmacias_benavides.geojson", driver="GeoJSON")
print('The program has finished,filtered:',after,'total:',before, 'percentaje filtered:',(after/before)*100)