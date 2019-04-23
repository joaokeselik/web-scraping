import sys
import requests
from bs4 import BeautifulSoup
import xlsxwriter

workbook = xlsxwriter.Workbook('blocket_data.xlsx')
worksheet = workbook.add_worksheet()

bold = workbook.add_format({'bold': 1})
money_format = workbook.add_format({'num_format': '$#,##0'})
date_format = workbook.add_format({'num_format': 'mmmm d yyyy'})
worksheet.set_column(0, 0, 50)
worksheet.set_column(1, 1, 30)
worksheet.set_column(2, 2, 20)
worksheet.write_string(0, 0, "Title", bold)
worksheet.write_string(0, 1, "Price", bold)
worksheet.write_string(0, 2, "Region", bold)

row = 1
col = 0

def list_product_price(page_number):
    url = 'https://www.blocket.se/stockholm?ca=11&o=' + str(page_number)
    result = requests.get(url)    
    try:    
        result.raise_for_status() 
    except Exception as exc:    
        print('There was a problem: %s' % (exc))

    c = result.content
    soup = BeautifulSoup(c, "html.parser")

    items = soup.find_all("a", "item_link")
    prices = soup.find_all("p", "list_price") 

    for item, price in zip(items, prices):
         title = item.string.strip()        
         print("%s  PRICE:  %s" %(title, price.text))
         
         global row
         global col
         worksheet.write_string(row, col, title)
         worksheet.write_string(row, col + 1, price.text)
         worksheet.write_string(row, col + 2, "Stockholm")
         row += 1             
   

for page_number in range(1, 5):
    print("|" + "-"*50 + " PAGE " + str(page_number) + " " + "-"*50 + "|")
    list_product_price(page_number)

workbook.close()
    
