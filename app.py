# app.py
from flask import Flask
from flask import render_template
from database import OracleDB
from service import makeChartData, makeChartDataForSingleItem, getSumOfPurchases

app = Flask(__name__)

@app.route('/')
def index():
  return '<h1>Tavex monitor</h1>'

@app.route('/prices/<name>')
def showPrices(name=None):
    return render_template('prices.html', name=name)

@app.route('/snapshots/', methods=['GET', 'POST'])
def snapshotList():    
    ora = OracleDB()
    ora.connect()
    l_res = ora.getSnapshotList()
    ora.connection_close()
    return render_template('snapshots.html', snapshots=l_res)
    
@app.route('/items/')
def itemList():
   ora = OracleDB()
   ora.connect()
   list = ora.getItemList()
   ora.connection_close()
   return render_template('items.html', items=list)

@app.route("/graphs/<itemId>")
def drawGraph(itemId=1):
  ora = OracleDB()
  ora.connect()
  list = ora.getTracking(itemId, 5)
  items = ora.getItemList()
  ora.connection_close()
  #print(items)
  b = [x["buy"] for x in list]
  s = [x["sell"] for x in list]
  d = [x["datum"].strftime("%m.%d - %H") for x in list]



  return render_template('price.comparison.html', values=s, valueb=b, valued=d, items=items, itemId=int(itemId))

@app.route("/overview/<id>")
def nenad(id=None):
  ora = OracleDB()
  ora.connect()
  list = ora.getTrackingForAllItems(7)
  purchases = ora.getPurchases()
  total = getSumOfPurchases(purchases=purchases)
  ora.connection_close() 
  if id == 'all':
    jsonstr = makeChartData(list, purchases)
  else:
    jsonstr = makeChartDataForSingleItem(list, purchases, id)

  return render_template('overview.html', jsonstr=jsonstr, purchases=purchases, total=total, itemId=id) 

if __name__ == '__main__':
  app.run()