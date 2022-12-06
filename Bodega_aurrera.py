import pandas as pd
import json
import openpyxl
import requests

from bs4 import BeautifulSoup
import geopandas as gpd
import time 
import numpy as np



#get baseurl in postman
baseurl = 'https://www.bodegaaurrera.com.mx/api/rest/model/atg/commerce/catalog/ProductCatalogActor/getStoreDetails?zipcode='


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
                    'Cookie':'Emaps-UserId=512bca3a-5ac7-4180-a6b9-c9fc401f48a1; ErMapsSession=CfDJ8Lq2Z91BaSJChMVYYzV0VY9Zc2Fljf8h6lM%2BI%2FeIjnUzboVnsgxB0UbH9Dz746zu5O%2Fd3swKclbsXx16qglTqLQgxD2SlCUSy8WLCrbL1C40tHLg%2FU2eGjMP4o1Hf66w6Br0CI9g7S5MrWh55ugfOwDH39wGkgg3RxIt5yMRKADa; TS0152d7f5=015b3bbaa3d8606636b883f3434815bb0d4011a78f81d14f5e836ed4ec611e42d7f87c892e3c5c5e03d8e6bf9aa453d0b1dfbd124f; _ga=GA1.2.1576151278.1656337339; _gid=GA1.2.319693535.1656337339; _gat=1; _gat_countryTracker=1'})
    soup = BeautifulSoup(req.text,"html.parser")
                #parse a json string
    try:
        data = json.loads(str(soup))
        data_len = len(data['storeDetails'])
            
          #Avoid data that is empty
    
                #building the dictionary
        if int(cont) % 100 == 0:
                for i in range(data_len):
                        try:
                            name = data['storeDetails'][i]['name']
                        except KeyError:
                            name = np.nan
                        try:
                            adress = data['storeDetails'][i]['address1'] + data['storeDetails'][i]['address2'] + data['storeDetails'][i]['address3']
                        except KeyError:
                            adress = np.nan
                        try:
                            zipcode = data['storeDetails'][i]['PostalCode']
                        except KeyError:
                            zipcode = np.nan
                        try:
                            city = data['storeDetails'][i]['city']
                        except:
                            city = np.nan
                        try:
                            country = data['storeDetails'][i]['Country']
                        except KeyError:
                            country = np.nan
                        #try:
                        #    latitude = data[i]['storeDetails']['Latitude']
                        #except KeyError: 
                        #    latitude = np.nan
                        #try:
                        #    longitude = data[i]['storeDetails']['Longitude']
                        #except KeyError:
                        #    longitude = np.nan
                        try:
                            hours= data['storeDetails'][i]['hours']
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
                                'Country':country,
                                'Address': adress,
                                'ZipCode': zipcode,
                                #'Latitude': latitude,
                                #'Longitude': longitude,
                                'Opening_hours':hours
                                }
            
                     #add dicc to the list
                        pp_lista.append(feature)
                        
                    
            
                print(cont,'from',cant_links)
                time.sleep(20)
        else:
                for i in range(data_len):
                        try:
                            name = data['storeDetails'][i]['name']
                        except KeyError:
                            name = np.nan
                        try:
                            adress = data['storeDetails'][i]['address1'] + ' ' + data['storeDetails'][i]['address2'] + ' ' + data['storeDetails'][i]['address3']
                        except KeyError:
                            adress = np.nan
                        try:
                            zipcode = data['storeDetails'][i]['postalCode']
                        except KeyError:
                            zipcode = np.nan
                        try:
                            phone = data['storeDetails'][i]['phoneNumber']
                        except:
                            phone = np.nan
                        try:
                            city = data['storeDetails'][i]['city']
                        except:
                            city = np.nan
                        try:
                            county = data['storeDetails'][i]['county']
                        except:
                            county = np.nan
                        try:
                            state = data['storeDetails'][i]['state']
                        except:
                            state = np.nan
                        try:
                            country = data['storeDetails'][i]['Country']
                        except KeyError:
                            country = np.nan
                        #try:
                        #    latitude = data[i]['storeDetails']['Latitude']
                        #except KeyError: 
                        #    latitude = np.nan
                        #try:
                        #    longitude = data[i]['storeDetails']['Longitude']
                        #except KeyError:
                        #    longitude = np.nan
                        try:
                            hours= 'Mo-Su 11:00-20:00'
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
                                'County':county,
                                'State':state,
                                'Country':country,
                                'Address': adress,
                                'ZipCode': zipcode,
                                'Phone': phone,
                                #'Latitude': latitude,
                                #'Longitude': longitude,
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
pp_str = pd.DataFrame.to_json(df)


jsonFile = open('bodegas.json', "w")
jsonFile.write(pp_str)
jsonFile.close()

#pp = pd.read_json('bodegas.json')
#Georef
#gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))

#Get geojson file
#gdf.to_file("C:\WS\bodegas.geojson", driver="GeoJSON")
print('The program has finished,filtered:',after,'total:',before, 'percentaje filtered:',(after/before)*100)