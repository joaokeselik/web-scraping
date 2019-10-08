#! python3 
# web-scraping.py - Collects data from Blocket.se

import requests
from bs4 import BeautifulSoup
import xlsxwriter
import re

workbook = xlsxwriter.Workbook('blocket_data.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': 1})
money_format = workbook.add_format({'num_format': '$#,##0'})
date_format = workbook.add_format({'num_format': 'mmmm d yyyy'})
worksheet.set_column(0, 0, 50)
worksheet.set_column(1, 1, 30)
worksheet.set_column(2, 2, 20)
worksheet.set_column(3, 3, 20)
worksheet.write_string(0, 0, "Title", bold)
worksheet.write_string(0, 1, "Price", bold)
worksheet.write_string(0, 2, "Category", bold)
worksheet.write_string(0, 3, "Region", bold)

row = 1
col = 0

url = 'https://www.blocket.se/hela_sverige'

#i=0

while not url.endswith('&last=1'):    
    
    #i=i+1
    #if i == 20:
     #   break

    print("-"*50 + " " + str(url) + " " + "-"*50)    
    
    result = requests.get(url)    
    try:    
        result.raise_for_status() 
    except Exception as exc:    
        print('There was a problem: %s' % (exc))

    c = result.content
    soup = BeautifulSoup(c, "html.parser")

    items = soup.find_all("a", "item_link")
    prices = soup.find_all("p", "list_price") 
    categories = soup.find_all('a', {'tabindex': '-1'})
    regions = soup.find_all('div', 'pull-left')

    for item_a, price_p, category_a, region_div in zip(items, prices, categories, regions[6:]):
         item = item_a.string.strip()   

         price = price_p.text
         if not price:
             price = "NULL"

         category = category_a.text
         if re.search(r"Lägenheter|Utland|Djur|Villor|Tjänster", category):
            continue
         
         if re.search(r"Jobb", region_div.text):
            continue

         region = region_div.text.split(',')[-1]         
             
         print("%s  PRICE:  %s  CATEGORY:  %s  REGION:  %s" %(item, price, category, region))         
         
         worksheet.write_string(row, col, item)
         worksheet.write_string(row, col + 1, price)
         worksheet.write_string(row, col + 2, category)
         worksheet.write_string(row, col + 3, region)
         row += 1     
         
    nextLink = soup.find_all('a', 'page_nav')[5]
    if not "Nästa sida »" in nextLink.decode_contents().strip():
        nextLink = soup.find_all('a', 'page_nav')[6]
        if not "Nästa sida »" in nextLink.decode_contents().strip():  
            nextLink = soup.find_all('a', 'page_nav')[7]               
    
    nextLinkSuffix = nextLink.get('href')     
    url = 'https://www.blocket.se/hela_sverige' + nextLinkSuffix     

workbook.close()
    
