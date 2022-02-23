# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 21:50:15 2021

@author: 97jak
"""


import re
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import csv



number = re.compile('^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$')
zip_code = re.compile('([0-9]{5})$')
address = re.compile(',')
principle = re.compile(':')
website = re.compile('htt')
labels = ['school', 'district', 'address', 'city', 'zip', 'number', 'website']

    
def get_ids():
    
    """Here I open a Chrome session. The experimental options allow me to keep the browser
    open """
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome("C:/Users/97jak/Downloads/chromedriver_win32/chromedriver.exe",options=chrome_options)
    
    driver.get('https://newmexicoschools.com/schools')
    time.sleep(20)
    
    next_button = True
    
    with open('school_ids.txt', 'w') as file:
        while next_button:
            next_button = False
        
            rows = driver.find_elements_by_tag_name('tr')
            
            for r in rows:
                file.write(r.get_attribute('id') + '\n')
                
                
            
            buttons = driver.find_elements_by_tag_name('button')
            for b in buttons:
                if b.text == 'Next':
                    next_button = True
                    b.click()
                    time.sleep(5)
                    continue
            
            if next_button == False:
                break

    
def pta():
    my_url = 'https://newmexicoschools.com/schools/'
    
    with open('school_ids.txt', 'r') as file:
            ids = file.readlines()
    
    with open('school_info.csv', mode='w',newline='',encoding='utf-8') as employee_file:
            
        for i, my_id in enumerate(ids):
            
            chrome_options = Options()
            chrome_options.add_experimental_option("detach", False)
            driver = webdriver.Chrome("C:/Users/97jak/Downloads/chromedriver_win32/chromedriver.exe",options=chrome_options)
            driver.get(my_url + my_id)
            #time.sleep(10)
            
            titles = driver.find_element_by_class_name('p-profile-header__name')
            stuff = driver.find_element_by_id('entity_detail')
            more_stuff = stuff.find_elements_by_tag_name('li')
            
            
            
            info = {}
            pre_stuff = []
            for m in more_stuff[:-1]:
                pre_stuff.append(m.text)
            
            info['school'] = titles.text
            
            for t in pre_stuff:
                if bool(zip_code.search(t)):
                    info['zip'] = zip_code.findall(t)[0]
                    
                if bool(address.search(t)):
                    stuff = t.split(',')
                    info['address'] = stuff[0]
                    info['city'] = stuff[1]
                
                if bool(address.search(t)) == False and bool(principle.search(t)) == False and bool(number.search(t)) == False:
                    info['district'] = t
                
                if bool(number.search(t)):
                    info['number'] = t
            
            lnks = more_stuff[-1].find_elements_by_tag_name("a")
            
            if lnks:
                info['website'] = lnks[0].get_attribute('href')
            else:
                info['website'] = ""
            

            titles = list(info.keys())
            row = []
            for i in labels:
                if i not in titles:
                    row.append("")
                else:
                    row.append(info[i])
    
    
            employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
            employee_writer.writerow(row)
        
            driver.quit()
            
def pta_specific_school(id_):
    my_url = 'https://newmexicoschools.com/schools/'
    
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", False)
    driver = webdriver.Chrome("C:/Users/97jak/Downloads/chromedriver_win32/chromedriver.exe",options=chrome_options)
    driver.get(my_url + id_)
    #time.sleep(10)
    
    info = []
    
    titles = driver.find_element_by_class_name('p-profile-header__name')
    
    stuff = driver.find_element_by_id('entity_detail')
    
    more_stuff = stuff.find_elements_by_tag_name('li')

        
    info.append(titles.text)
    print(titles.text)
    
    for m in more_stuff[:-1]:
        info.append(m.text)
    
    lnks = more_stuff[-1].find_elements_by_tag_name("a")
    
    if lnks:
        print(lnks[0].get_attribute('href'))
    else:
        print("No website")

    driver.quit()
    
with open('school_ids.txt', 'r') as file:
    id_ = file.readlines()[0]

pta()


    