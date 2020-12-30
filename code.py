#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 20:05:52 2020

@author: erwanrh
"""
# WebScrapping on the Pokemon database 
#%% Libraries
import urllib
import bs4
from urllib.request import urlopen, Request, urlretrieve
import pandas as pd

#%% URL, database
url_pokemonlist = "https://pokemondb.net/pokedex/national"
req = Request(url_pokemonlist, headers={'User-Agent': 'Mozilla/5.0'})
opener = urllib.request.URLopener()
opener.addheader('User-Agent', 'Mozilla/5.0')

webpage = urlopen(req).read()
page1 = bs4.BeautifulSoup(webpage, "lxml")

# Get the list of all pokemons from the HTML code
pokemon_list= []
for item in page1.findAll('a', {'class':'ent-name'}):
    pokemon_list.append((item.getText(),item.get('href')))

# Get the data from the table and save the picture
poke_data = pd.DataFrame()
for name, url in pokemon_list:
    print(name)
    pokepage = 'https://pokemondb.net'+url
    req2 = Request(pokepage, headers={'User-Agent': 'Mozilla/5.0'})
    page2 = bs4.BeautifulSoup(urlopen(req2).read(), "lxml")
    #First Table
    table1_html = page2.find('table', {'class':'vitals-table'})
    table1_html
    pokedex_data = {}
    for row in table1_html.findAll('tr'):
        pokedex_data[row.find('th').getText()] = row.find('td').getText().replace('\n',' ')
    pokedex_data['name'] = name
    poke_data=poke_data.append(pokedex_data, ignore_index=True)
    #Saving the picture
    pic = page2.find('div',{'class':'grid-col span-md-6 span-lg-4 text-center'})
    filename, headers = opener.retrieve(pic.find('a').get('href'), 'pokemons/'+name+'.jpg')
    
#%% 
print(poke_data)
    
