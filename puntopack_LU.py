import pandas as pd
import json
import openpyxl
import requests

from bs4 import BeautifulSoup
import geopandas as gpd
import time 
import numpy as np
from pandas import json_normalize



#get baseurl in postman
baseurl = 'https://www.puntopack.es/api/parcelshop?country=LU&postcode='


#add excel file to interpreter into a list
wb = openpyxl.load_workbook('C:\WS\puntopack\ZIP.xlsx')
ws = wb['Luxembourg']
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

    req = s.get(link, timeout=None ,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36)',
    'requestverificationtoken':'DRT2zyVi0bcusS5Kms7tuia8CFQ9EkZ68JPqgf-DGCJCzTZw5a6ep0YjsatFUGJUVxTOAZwux8IxgCdqp9G3hbnaCtI1:JLzUKoWQpjUaZSzikniCXvPrbZCe1c73dDq2jw61-Zp4nme3uViB2X0hyYO0-j76FmQtvPpGdSja8PhWTH4BoA8rE6M1',
    'Cookie':'_gcl_au=1.1.410432584.1653472584; _ga=GA1.2.788662825.1653472584; OptanonAlertBoxClosed=2022-05-25T09:56:28.168Z; cf_clearance=2COlOtY8VvZnoGX9veCamHgnsF97kzoBLcTwI8ID3gE-1653639458-0-150; _clck=ayr8dn|1|f1x|0; OptanonConsent=geolocation=ES%3BMD&datestamp=Tue+May+31+2022+20%3A45%3A57+GMT%2B0100+(GMT%2B01%3A00)&version=6.5.0&isIABGlobal=false&consentId=0ce21e85-3de1-4632-a4f5-f598a7a556c1&interactionCount=1&landingPath=https%3A%2F%2Fwww.puntopack.es%2Fbuscar-el-punto-pack-mas-cercano%2F&groups=C0001%3A1%2CC0005%3A0%2CC0004%3A0%2CC0002%3A1&hosts=H64%3A1%2CH11%3A0%2CH21%3A0%2CH28%3A0%2CH35%3A0%2CH38%3A0%2CH50%3A0%2CH52%3A0%2CH54%3A0; ASP.NET_SessionId=iw3ch2avma5g01i0nwqyex0h; __RequestVerificationToken=T3iRJDHDkoHy2txcWJrtuSb2YSFmpYNouUh51lkXVp9z1k25fy6_DOFGGisxhyJSyMneGD-Z-ZOf4MkVypqlp9Sf5j81; JSESSSIONID=2691056812.1.612195776.3011222528; mr.returning.visitor=3'})
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
                                    'Latitude': float(latitude),
                                    'Longitude': float(longitude),
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


jsonFile = open("C:\WS\puntopack\puntopack_LU_data.json", "w")
jsonFile.write(pp_str)
jsonFile.close()


pp = pd.read_json("C:\WS\puntopack\puntopack_LU_data.json")
#Georef
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))
#Get geojson file
gdf.to_file("C:\WS\puntopack\puntopack_LU.geojson", driver="GeoJSON")

print('the program has finished','total:' ,before,'filtered: ',after)