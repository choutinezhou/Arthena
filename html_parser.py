# -*- coding: utf-8 -*-

# import libraries
from bs4 import BeautifulSoup
import os
import glob
import json

path='data/2015-03-18/'
artists = []
for htmlfile in glob.glob(os.path.join(path, "*.html")):
    with open(htmlfile,"r") as f:
        page = f.read()
    soup = BeautifulSoup(page,"lxml")
    head = soup.h2.string
    artists.append(head)

jarray=json.dumps(artists)

print (artists)

