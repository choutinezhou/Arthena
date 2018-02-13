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
    artists.append({'artist':head,'works':works})

# transform the list to JSON arrays    
jarray=json.dumps(artists)

print (artists)

