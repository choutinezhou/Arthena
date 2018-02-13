# -*- coding: utf-8 -*-

# import libraries
from bs4 import BeautifulSoup
import os
import glob
import json

# identify the directory path
# parse the 2015-03-18 folder

path='data/2015-03-18/'

# create a list of artists
artists = []

# open all html files in this folder
for htmlfile in glob.glob(os.path.join(path, "*.html")):
    with open(htmlfile,"r") as f:
        page = f.read()
    soup = BeautifulSoup(page,"lxml")
    # parse the artist names
    head = soup.h2.string
    # parse the art work titles
    works=soup.h3.string
    # parse the price
    # split the price into currency and ammount
    price=soup.find_all('div')[1].string.split()
    price[1] = round(int(price[1].replace(',','')),2)
    # if the currency is GBP, convert it into USD with 1.34 exchange rate
    if(price[0]=='GBP'):
        price[1] = price[1]*1.34
    price[1] = round(price[1],2)
    
    # create an object to include each artist's data
    obj = {'artist':head,'totalValue':0,'works':[]}
    # append artists data
    
    obj['works'].append({'title':works,'currency':'USD','totalLifetimeValue':price[1]})
    obj['totalValue'] = price[1]
    artists.append(obj)
    

# transform the list to JSON arrays    
jarray=json.dumps(artists)


# identify the directory of folder 2017-12-20
path2= 'data/2017-12-20/'

for htmlfile in glob.glob(os.path.join(path2, "*.html")):
    with open(htmlfile,"r") as f:
        page = f.read()
    soup = BeautifulSoup(page,"lxml")
    head = soup.h3.string
    obj={'artist':head,'totalValue':0,'works':[]}
    index = -1
    
    # aggregate the data of a same artist
    for i,data in enumerate(artists):
        if data["artist"] == head:
            obj = data
            index = i
            break
    works = soup.find_all('h3')[1].string
    pricePath = soup.find_all('div')[1]
    amount = soup.find_all('span')
    currency = amount[0].string
    # extract the price from the span
    price2 = round(int(amount[1].string.replace(',','')),2)
    if currency == 'GBP':
        price2 = price2*1.34
    obj['works'].append({'title':works,'currency':'USD','totalLifetimeValue':price2})
    obj['totalValue'] = obj['totalValue'] + price2
    if index != -1:
        artists.pop(index)
    artists.append(obj)

# transform the list to JSON arrays 
jarray = json.dumps(artists)

print (artists)
