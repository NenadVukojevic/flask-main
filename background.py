import requests
from bs4 import BeautifulSoup
import json
from database import OracleDB


prices = []
def get_item_id(title, items):
    id = 0
    id = next((i['id'] for i in items if i['name'] == title), 0)
    return id

def get_snapshot_id():
    return 0

proxies = {
#   'http': 'http://172.17.5.30:8080',
#   'https': 'http://172.17.5.30:8080',
}

prices = []

def getFirstValue(list):
    result = ''
    if len(list)>0:
        result = list[0].decode_contents()
    return result

def parsePriceValue(list):
    result = 0
    if len(list)>0:
        if list[0].has_attr('data-pricelist'):
            prices = list[0]['data-pricelist']
            jsonData=json.loads(prices)
            # get price for the sale option quantity from 1 to 4 
            sell_1 = [item for item in jsonData['sell'] if item['quantityFrom'] == 1]
            if len(sell_1) > 0:
                result = sell_1[0]['price']
    return result
        
def getPrice(title):
    result = 0
    found = [item for item in prices
          if item[0] == title]
    if len(found) > 0:
        result = int(found[0][1])
    return result

def logPrice():
    url = 'https://tavex.rs/zlato/'
    page = requests.get(url, proxies=proxies)
    soup = BeautifulSoup(page.content, 'html.parser')
    rows = soup.find_all('div', class_='grid__col--xs-6')
    
    ora = OracleDB()
    ora.connect()
    items = ora.getItemList()
    print(items)
    
    snapshot_id = get_snapshot_id()
    
    for row in rows:
        title = getFirstValue(row.select('.product__title-inner'))
        buy = getFirstValue(row.select('.price-amount-whole')).replace(" ", "")
        sell = parsePriceValue(row.select('.product__price-value'))
        #print (temp)
        item_id = get_item_id(title, items)
        print(title, item_id)
        if item_id > 0: #title in mine and 
            prices.append({'item_id':item_id, 'snapshot_id': snapshot_id, 'buy':buy, 'sell':sell})
            print(title, ',', buy, ', ', sell)
    print (prices)
    ora.connection_close()        

