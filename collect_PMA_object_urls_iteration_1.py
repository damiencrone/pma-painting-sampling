#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 12:16:07 2021

@author: dcrone
"""


# Import modules
import requests
from bs4 import BeautifulSoup
import csv

url_base = 'https://www.philamuseum.org/collections/results.html'
url_parameters = '?results=54&searchTxt=&searchNameID=&searchClassID=3&provenance=0&audio=0&onView=0&searchOrigin=&searchDeptID=&action=post'

hdrs = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0'}


page_links = []
page_num = 1
objects_found = True

while objects_found:
    
    print('Processing page ' + str(page_num))
    url = url_base + url_parameters + '&page=' + str(page_num)
    response = requests.get(url, headers=hdrs)
    page_soup = BeautifulSoup(response.content, 'html.parser')
    
    objects_in_page = 0

    for link_element in page_soup.find_all('a', href=True):
        
        object_link = link_element['href']
        
        if '/collection/object/' in object_link:
            
            link_str = str(link_element)
            image_link = link_str.split('/images/cad/mediaDecks/')[1]
            image_link = image_link.split('\');')[0]
            
            page_links.append({'object_URL':object_link, 'image_URL':image_link})
            objects_in_page += 1
            
    
    print(str(objects_in_page) + ' objects found')
    
    if objects_in_page == 0:
        objects_found = False
        
    page_num += 1


# Save results
keys = page_links[0].keys()
with open('object_urls.csv', 'w', newline='')  as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(page_links)