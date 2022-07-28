#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 10:24:53 2021

@author: dcrone
"""

# Import modules
import requests
from bs4 import BeautifulSoup
import pandas
import json
import time

pause_duration = 5

url_base = 'https://www.philamuseum.org/collection/object/'
hdrs = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0'}

df = pandas.read_csv('object_urls.csv')
collection = []

for index, row in df.iterrows():
    
    object_data = {}
    object_data['object'] = row['object']
    
    origin_filename = row['image']
    object_url = url_base + str(row['object'])
    
    response = requests.get(object_url, headers=hdrs)
    page_soup = BeautifulSoup(response.content, 'html.parser')
    
    label_div = page_soup.find_all('div', attrs={'class': 'object-label'})
    
    if len(label_div) > 0:
        label_str = label_div[0].find_all(text=True)[0]
        object_data['Label'] = label_str
        
    
    metadata_table = page_soup.find_all('table', attrs={'class': 'object-description'})
    
    # Loop through rows
    metadata_table_rows = metadata_table[0].find_all('tr')
    
    for table_row in metadata_table_rows:
        
        row_data = []
        
        col_num = 0
        
        for table_element in table_row.find_all('td'):
            
            element_data = table_element.find_all(text=True)[0]
            row_data.append(element_data)
        
        object_data[row_data[0]] = row_data[1]
    
    # Save individual object metadata as json file
    output_filename = 'meta/' + str(row['object']) + '.json'
    with open(output_filename, 'w') as f:
        json.dump(object_data, f)
    
    # Append object info to list
    collection.append(object_data)
    
    print(object_data)
    time.sleep(pause_duration)
    
# Save all data in one file
output_filename = 'all_metadata.json'
with open(output_filename, 'w') as f:
    json.dump(collection, f)
