#! python3 
# web-scraping.py - Gets data from Blocket.se

import requests
from bs4 import BeautifulSoup
import xlsxwriter

#maybe should remove main() and use a while instead getting the next page links

def list_product_price(page_number):
    url = 'https://www.blocket.se/hela_sverige?&o=' + str(page_number)
    print('Downloading page %s...' % url) 
    result = requests.get(url)    
    try:    
        result.raise_for_status() 
    except Exception as exc:    
        print('There was a problem: %s' % (exc))

    c = result.content
    soup = BeautifulSoup(c, "html.parser")

    items = soup.find_all("a", "item_link")
    prices = soup.find_all("p", "list_price") 
    categories=soup.find_all('a', {'tabindex': '-1'})
    regions=soup.find_all('div', 'pull-left')

    #still some problems parsing the region with BMWselection which comes straight after the region in the same div
    for item_a, price_p, category_a, region_div in zip(items, prices, categories, regions[6:]):
         item = item_a.string.strip()   

         price = price_p.text
         if not price:
             price = "NULL"

         category = category_a.text

         region = region_div.text.split(',')[-1]
         if "Butik" in region:
             region="NULL"    
             
         print("%s  PRICE:  %s  CATEGORY:  %s  REGION:  %s" %(item, price, category, region))
         
         global row
         global col
         worksheet.write_string(row, col, item)
         worksheet.write_string(row, col + 1, price)
         worksheet.write_string(row, col + 2, category)
         worksheet.write_string(row, col + 3, region)
         row += 1           
 
def main():
    #while not url.endswith('&last=1'):
    for page_number in range(1, 5):
        print("|" + "-"*50 + " PAGE " + str(page_number) + " " + "-"*50 + "|")
        list_product_price(page_number)
    #url = list_product_price

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

main()

workbook.close()
    
