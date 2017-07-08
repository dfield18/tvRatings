import requests
from bs4 import BeautifulSoup
import re
from geopy.geocoders import Nominatim
import time

page = "http://tvbythenumbers.zap2it.com/category/daily-ratings/page/"

# Loop through the 149 pages of news posts to get links to ratings pages
# Each of 149 news posts lists headlines and links to ratings tables
# Links stored in the list cable Daily
cableDaily = []
for i in range(1, 149):
    url = page + str(i)
    print(url)
    r  = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data)
    for link in soup.find_all('a', href=True):
        l = (link['href'])
        if 'cable' in str(link):
            if l not in cableDaily:
                l = (link['href'])
                cableDaily.append(link['href'])    
    time.sleep(1)

# Loop through each ratings table (stored in cableDaily list)
cnn = []
foxNews = []
msnbc = []
for i in cableDaily:
    r  = requests.get(i)
    data = r.text
    soup = BeautifulSoup(data)
    
    program = ""
    network = ""
    hour = ""
    viewers = ""
    people1849 = ""
    
    soup.find_all('p','b','strong')
    
    date = str(soup.find_all('strong')[0])
    dateReform = re.findall(r'for(.*)<', str(date))
    dateReform = str(dateReform)

# Within each table find each row of ratings (each row starts with tr)   
    for tr in soup.find_all('tr'):
        count = 0

# For each row, find the relevant information for program, channel, time and viewership  
        for td in tr.find_all('td'):
            
            td = str(td)
            td = td.replace("<td>", "").replace("</td>", "")
            
            if count == 0:
                program = td
                program = program.replace(",", "")
            if count == 1:
                channel = td
                channel = channel.replace(",", "")
            if count == 2:
                hour = td
                hour = hour.replace(",", "")
            if count == 3:
                viewers = td
                viewers = viewers.replace(",", "")
            if count == 4:
                people1849 = td
                people1849 = people1849.replace(",", "")
                           
            count = count + 1
            
# If row includes Fox News (also listed as 'FNC'), append row to foxNews list           
        if "Fox News" or "FNC" in channel:
            row = str(program + "," + channel + "," + hour + "," + viewers  + "," + people1849 +  "," + dateReform + "," + i)
            #print(row)
            foxNews.append(row)
      
# Convert list of ratings to csv file       
f = open('msnbc.csv','w')   
for i in msnbc:
       f.write(i)
       f.write('\n')            
            
            
            
            
            