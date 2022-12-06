import requests 
from bs4 import BeautifulSoup


url = "https://celeritastransporte.com/buscador-punto-celeritas/"
html_doc = requests.get(url).text
soup = BeautifulSoup(html_doc,'html.parser')

stores = soup.find_all('div',{'class':'f-row clearfix'})

for item in stores:
    title = item.find('div',{'input':'name'})



