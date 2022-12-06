import pandas as pd
import json
import openpyxl
import requests

from bs4 import BeautifulSoup
import geopandas as gpd
import time 
import numpy as np
import pdb



#get baseurl in postman
baseurl = 'https://www.inpost.es/api/parcelshop?country=ES&postcode='


#add excel file to interpreter into a list
wb = openpyxl.load_workbook('C:\WS\puntopack\ZIP.xlsx')
ws = wb['Spain']
lista_zip = []
for row in ws.iter_rows():
    lista_zip.append(row[0].value)

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

    req = s.get(link, timeout=None ,headers={'Connection':'keep-alive','user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
                    'requestverificationtoken':'FSqLk4W9jzvD9Pf1iUUL_wET2FAZBRLO-G7LSMu9yu9c5s_v5H3NstXICeG9ghddrXDyoUpBjXu5TsA_NtruHPORg141:3dg-ygduNLBFFJ-4plgpaLNh69__wVzypaAoh2XigszerFsVDRT6gDm7ommwRyXJrkPpJVcJ1Bs8k88elVptR_7mujo1',
                    #'Cookie':'FSqLk4W9jzvD9Pf1iUUL_wET2FAZBRLO-G7LSMu9yu9c5s_v5H3NstXICeG9ghddrXDyoUpBjXu5TsA_NtruHPORg141:3dg-ygduNLBFFJ-4plgpaLNh69__wVzypaAoh2XigszerFsVDRT6gDm7ommwRyXJrkPpJVcJ1Bs8k88elVptR_7mujo'
                    })
    #reqpdb.set_trace()
    
    soup = BeautifulSoup(req.text,"html.parser")
                #parse a json string
    data = json.loads(str(soup))
    data_len = len(data)
            
                #Avoid data that is empty
    if data_len == 0:
        no_data = True
        continue 
                #building the dictionary
    else:
            if int(cont) % 80 == 0:
                for i in range(data_len):
                        try:
                            name = data[i]['Adresse']['Libelle']
                        except KeyError:
                            name = np.nan
                        try:
                            adress = data[i]['Adresse']['AdresseLigne1']
                        except KeyError:
                            adress = np.nan
                        try:
                            zipcode = data[i]['Adresse']['CodePostal']
                        except KeyError:
                            zipcode = np.nan
                        try:
                            city = data[i]['Adresse']['Ville']
                        except:
                            city = np.nan
                        try:
                            country = data[i]['Adresse']['Pays']['Code']
                        except KeyError:
                            country = np.nan
                        try:
                            latitude = data[i]['Adresse']['Latitude']
                        except KeyError: 
                            latitude = np.nan
                        try:
                            longitude = data[i]['Adresse']['Longitude']
                        except KeyError:
                            longitude = np.nan
                        try:
                            hours= data[i]['Horaires']
                        except KeyError: 
                            hours= np.nan

                        opening_hours =''
                        try:
                            for x in range (len(hours)):
                                if (hours[x]['HeureFermeturePM']) == None :
                                    opening_hours+= str(hours[x]['JourSemaine'])+ ' ' + str(hours[x]['HeureOuvertureAM']) +" - "+str(hours[x]['HeureFermetureAM'])
                                else:
                                    opening_hours+= str(hours[x]['JourSemaine'])+ ' ' + str(hours[x]['HeureOuvertureAM']) +" - "+str(hours[x]['HeureFermeturePM'])+ ' break ' +\
                                    str(hours[x]['HeureFermetureAM'])+" - "+str(hours[x]['HeureOuverturePM']) + ' '

                        except TypeError:
                            opening_hours+= None


                        feature = {
                                'Name': name,
                                'City':city,
                                'Country':country,
                                'Address': adress,
                                'ZipCode': zipcode,
                                'Latitude': latitude,
                                'Longitude': longitude,
                                'Opening_hours':opening_hours.replace('1 '," Mo ").replace('2 ',' Tu ').replace('3 ',' We ').replace('4 ', ' Th ').replace('5 ',' Fr ').replace('6 ',' Sa ').replace(' 0 ',' Do ')
                                }
            
                     #add dicc to the list
                        pp_lista.append(feature)
                        
                    
            
                print(cont,'from',cant_links)
                time.sleep(20)
            else:
                for i in range(data_len):
                        try:
                            name = data[i]['Adresse']['Libelle']
                        except KeyError:
                            name = np.nan
                        try:
                            adress = data[i]['Adresse']['AdresseLigne1']
                        except KeyError:
                            adress = np.nan
                        try:
                            zipcode = data[i]['Adresse']['CodePostal']
                        except KeyError:
                            zipcode = np.nan
                        try:
                            city = data[i]['Adresse']['Ville']
                        except:
                            city = np.nan
                        try:
                            country = data[i]['Adresse']['Pays']['Code']
                        except KeyError:
                            country = np.nan
                        try:
                            latitude = data[i]['Adresse']['Latitude']
                        except KeyError: 
                            latitude = np.nan
                        try:
                            longitude = data[i]['Adresse']['Longitude']
                        except KeyError:
                            longitude = np.nan
                        try:
                            hours= data[i]['Horaires']
                        except KeyError: 
                            hours= np.nan

                        opening_hours =''
                        try:
                            for x in range (len(hours)):
                                if (hours[x]['HeureFermeturePM']) == None :
                                    opening_hours+= str(hours[x]['JourSemaine'])+ ' ' + str(hours[x]['HeureOuvertureAM']) +" - "+str(hours[x]['HeureFermetureAM'])
                                else:
                                    opening_hours+= str(hours[x]['JourSemaine'])+ ' ' + str(hours[x]['HeureOuvertureAM']) +" - "+str(hours[x]['HeureFermeturePM'])+ ' break ' +\
                                    str(hours[x]['HeureFermetureAM'])+" - "+str(hours[x]['HeureOuverturePM']) + ' '

                        except TypeError:
                            opening_hours+= None


                        feature = {
                                    'Name': name,
                                    'City':city,
                                    'Country':country,
                                    'Address': adress,
                                    'ZipCode': zipcode,
                                    'Latitude': latitude,
                                    'Longitude': longitude,
                                    'Opening_hours':opening_hours.replace('1 '," Mo ").replace('2 ',' Tu ').replace('3 ',' We ').replace('4 ', ' Th ').replace('5 ',' Fr ').replace('6 ',' Sa ').replace(' 0 ',' Do ')
                                    }
                
                        #add dicc to the list
                        pp_lista.append(feature)
                            
                        
                
                print(cont,'from',cant_links)
                #time.sleep(1)

#Get json file
print('Filtering')

pp_dg = pd.DataFrame(pp_lista)
before =len(pp_dg)
print(pp_dg.duplicated(subset=['Longitude']).sum())
mask = pp_dg.duplicated(subset=['Latitude'])
df = pp_dg[~mask]
after = len(df)
pp_str = pd.DataFrame.to_json(df)

jsonFile = open("C:\WS\puntopack\puntopack_ES_data.json", "w")
jsonFile.write(pp_str)
jsonFile.close()

pp = pd.read_json("C:\WS\puntopack\puntopack_ES_data.json")
#Georef

gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))

#Get geojson file
gdf.to_file("C:\WS\puntopack\puntopack_ES.geojson", driver="GeoJSON")
print('The program has finished,filtered:',after,'total:',before, 'percentaje filtered:',(after/before)*100)