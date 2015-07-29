#!/usr/bin/python
from __future__ import print_function
'''
wiki_scrape.py : Scrapes the tables 
off of wikipedia corresponding 
to current ufc fighters on the roster

'''

from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import urllib2
import re

import os
# move to the working directory on the 
# external hardrive
os.chdir('/Volumes/HAL/kyle/betty/')




wiki_roster = "https://en.wikipedia.org/wiki/List_of_current_UFC_fighters"
header = {'User-Agent': 'Mozilla/5.0'} #Needed to prevent 403 error on Wikipedia
req = urllib2.Request(wiki_roster,headers=header)
page = urllib2.urlopen(req)
soup = BeautifulSoup(page)
 
 

tables = soup.findAll("table", { "class" : "wikitable sortable" })

name=""
wiki_link=""
results = pd.DataFrame({"name" : name, "wiki_link" : [wiki_link]})

results.sort(['name'], ascending=1)

for table in tables:
    for row in table.findAll("tr"):
        cells = row.findAll("td")
        if len(cells) == 4:
            origin=cells[0].find(text=True)
            name=cells[1].find(text=True)
            for link in cells[1].findAll('a'):
                wiki_link = link.get("href")
            nick_name = cells[2].find(text=True)
            record = cells[3].find(text=True)
        
        res = {"name": [name], "wiki_link" : [wiki_link]}
        res = pd.DataFrame(res)
        print(res)
        results = results.append(res)

'''
results from the subset of data that corresponds to 
those that have attainable ufc records, etc, ... off of facebook
'''

res_sub = results[results['wiki_link'].str.contains("/wiki/")]



wiki_base = "https://en.wikipedia.org"

fighters = []
for index, row in res_sub.iterrows():
    wiki = wiki_base + row['wiki_link']
    print(wiki)
    header = {'User-Agent': 'Mozilla/5.0'} #Needed to prevent 403 error on Wikipedia
    req = urllib2.Request(wiki,headers=header)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page)

    ## scrape the fighter data table
    data_table = soup.find("table", { "class" : "infobox vcard" })
    
    if (data_table is None):
        continue
    
    import re
    attr = {}
    parse = {"label": [], "attr": []}
    
    ''' 
    this is kind of complicated,
    essentially in order to parse the ages off of the tables,
    I needed to find the ForceAgeToShow span class, then pull the 
    age off of the table
    '''
    age = data_table.find("span", {"class" : "noprint ForceAgeToShow"})
    if (age is None):
        age = 'NaN'
    else:
        age = age.find(text=True)
        age = re.findall(u'\d+', age)
     
    '''
    get the name, if the name is not parse_able from the wikipedia page
    then get the name in the form of Last, First
    '''       
    name = data_table.find("span", {"class" : "fn"})    
    if (name is None):
        name = row['name']
    else:
        name = name.find(text=True)
    
    
    
    for row in data_table.findAll("tr"):
        cells = row.findAll("td")
        labels = row.findAll("th")
        if len(cells) > 0 and len(labels) > 0:
            
            thing = cells[0].find(text=True).encode('utf-8').strip()
            label = labels[0].find(text=True).encode('utf-8').strip()
            
            parse['label'].append(label)
            parse['attr'].append(thing)
            
    parse['label'].append('age')
    parse['attr'].append(age[0])
        
    parse['label'].append('name')
    parse['attr'].append(name)
    
    from fighter import fighter, attr 
    
    
    
    
    '''
    What follows is probably an unneccesarily long
    list of if-statements that cover the 
    vast majority of the cases that the parser is going to cover.
    '''
    
    attrb={}
    for label in parse['label']:
        if label == 'name': ##1
            h = parse['label'].index(str(label))
            attrb['name'] = parse['attr'][h]
            
        if label == 'Height': 
            h = parse['label'].index(str(label))
            height = parse['attr'][h]
            height = re.findall(u'\d+', height)
            attrb['height'] = height
            
        if label == 'Weight': 
            h = parse['label'].index(str(label))
            weight = parse['attr'][h]
            weight = re.findall(u'\d+', weight)
            attrb['weight'] = weight
            
        if label == 'Division': 
            h = parse['label'].index(str(label))
            attrb['division'] = parse['attr'][h]
            
        if label == 'Years active': 
            h = parse['label'].index(str(label))
            tenure = parse['attr'][h]
            tenure = re.findall(u'\d+', tenure)
            attrb['tenure'] = tenure
            
        if label == 'Team': 
            h = parse['label'].index(str(label))
            attrb['team'] = parse['attr'][h]
            
        if label == 'Nationality': 
            h = parse['label'].index(str(label))
            attrb['nation'] = parse['attr'][h]
            
        if label == 'Style': 
            h = parse['label'].index(str(label))
            attrb['style'] = parse['attr'][h]    
                    
        if label == 'age': 
            h = parse['label'].index(str(label))
            attrb['age'] = parse['attr'][h]    
    
    
    
    '''
    now all we have left to throw in is the 
    record table
    
    '''
    result=''
    record=''
    opponent=''
    method=''
    event=''
    date=''
    round_end=''
    time=''
    location=''
    notes=''
    
    res = {'result': [result], 'record' : [record],
    'opponent' : [opponent], 'method' : [method], 'event' : [event],
    'date' : [date], 'round_end' : [round_end], 'time' : [time],
    'location' : [location], 'notes' : [notes]}
    
    fighter_record = pd.DataFrame(res)
    
    
    record_table =  soup.find("table", { "class" : "wikitable sortable"})
    
    if (record_table is None):
       continue 
    
    for row in record_table.findAll("tr"):
            cells = row.findAll("td")
            if len(cells) == 10:
                result=cells[0].find(text=True)
                res['result'] = [result]
                
                record=cells[1].find(text=True)
                res['record'] = [record]
                
                opponent = cells[2].find(text=True)
                res['opponent'] = [opponent]
                
                method = cells[3].find(text=True)
                res['method'] = [method]
                
                event = cells[4].find(text=True)
                res['event'] = [event]
                
                date= cells[5].find(text=True)
                res['date'] = [date]
                
                round_end = cells[6].find(text=True)
                res['round_end'] = [round_end]
                
                time = cells[7].find(text=True)
                res['time']= [time]
                
                location = cells[8].find(text=True)
                res['location'] = [location]
                
                notes = cells[9].find(text=True)
                res['notes'] = [notes]
                
            fighter_record = fighter_record.append(pd.DataFrame(res))
    
    fighter_record = fighter_record[fighter_record.date != '']
    
    
    attrb['record'] = fighter_record
    
    fighter=fighter(attrb)

    fighters.append(fighter)
    
    
    

    