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
    price=soup.find_all('div')[1].string
    # create an object to include each artist's data
    obj={'artist':head,'works':[]}
    # append artists data
    # split the price into currency and ammount
    obj['works'].append({'title':works,'currency':price.split()[0],'amount':price.split()[1]})
    artists.append(obj)
    

# transform the list to JSON arrays    
jarray=json.dumps(artists)

print (artists)

