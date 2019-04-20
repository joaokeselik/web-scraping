import requests
from bs4 import BeautifulSoup

def list_product_price(page_number):
    url = 'https://www.blocket.se/stockholm?ca=11&o=' + str(page_number)
    result = requests.get(url)
    #print(result.status_code)

    c = result.content
    soup = BeautifulSoup(c, "html.parser")

    items = soup.find_all("a", "item_link")
    prices = soup.find_all("p", "list_price")
    
    for item, price in zip(items, prices):
        title = item.string.strip()        
        print("%s  PRICE:  %s" %(title, price.text))
       
for page_number in range(1, 21):
    print("|" + "-"*50 + " PAGE " + str(page_number) + " " + "-"*50 + "|")
    list_product_price(page_number)
