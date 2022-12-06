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
baseurl = 'https://www.puntopack.es/api/parcelshop?country=FR&postcode='


#add excel file to interpreter into a list
wb = openpyxl.load_workbook('C:\WS\puntopack\ZIP.xlsx')
ws = wb['France']
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
                    'requestverificationtoken':'OaWoV7KOR5NjwUjJkuUdDiccpXbmri-azKGwO7dtoiTb6VcFdJ2cVfrbwolIIjlcakHT0KffK0WABLM-tCKN2yM9U001:UP-U-93g8WyBa3NAkHTdO4zOKnDZTkVdkyt4TM2tAliO67ECCVL4nCarXrTLlR-5HVgr_gfRixE0WfzRdyNPRHtF7R01',
                    'Cookie':'_gcl_au=1.1.410432584.1653472584; _ga=GA1.2.788662825.1653472584; OptanonAlertBoxClosed=2022-05-25T09:56:28.168Z; cf_clearance=2COlOtY8VvZnoGX9veCamHgnsF97kzoBLcTwI8ID3gE-1653639458-0-150; _clck=ayr8dn|1|f1x|0; OptanonConsent=geolocation=ES%3BMD&datestamp=Tue+May+31+2022+20%3A45%3A57+GMT%2B0100+(GMT%2B01%3A00)&version=6.5.0&isIABGlobal=false&consentId=0ce21e85-3de1-4632-a4f5-f598a7a556c1&interactionCount=1&landingPath=https%3A%2F%2Fwww.puntopack.es%2Fbuscar-el-punto-pack-mas-cercano%2F&groups=C0001%3A1%2CC0005%3A0%2CC0004%3A0%2CC0002%3A1&hosts=H64%3A1%2CH11%3A0%2CH21%3A0%2CH28%3A0%2CH35%3A0%2CH38%3A0%2CH50%3A0%2CH52%3A0%2CH54%3A0; ASP.NET_SessionId=dv2br22oqb4pqpnxmzamzus3; __RequestVerificationToken=ysnUhdO9-0pu6ITORuIYj7zSGSMcARuwg2a3tC9EnU86ily-rG13JQZPJS4nvdV7GV2cRC_QxPOFGPEvRlSWS2g49Q01; mr.returning.visitor=2'})
    pdb.set_trace()

    soup = BeautifulSoup(req.text,"html.parser")
    pdb.set_trace()
                #parse a json string
    data = json.loads(str(soup))
    pdb.set_trace()
    data_len = len(data)
            
                #Avoid data that is empty
    if data_len == 0:
        no_data = True
        continue 
                #building the dictionary
    else:
            if int(cont) % 400 == 0:
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

#Get json file
print('Filtering')

pp_dg = pd.DataFrame(pp_lista)
before =len(pp_dg)
print(pp_dg.duplicated(subset=['Longitude']).sum())
mask = pp_dg.duplicated(subset=['Latitude'])
df = pp_dg[~mask]
after = len(df)
pp_str = pd.DataFrame.to_json(df)


jsonFile = open("C:\WS\puntopack\puntopack_FR_data.json", "w")
jsonFile.write(pp_str)
jsonFile.close()

pp = pd.read_json("C:\WS\puntopack\puntopack_FR_data.json")
#Georef
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))

#Get geojson file
gdf.to_file("C:\WS\puntopack\puntopack_FR.geojson", driver="GeoJSON")
print('The program has finished,filtered:',after,'total:',before, 'percentaje filtered:',(after/before)*100)