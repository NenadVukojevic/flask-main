from model import Dataset, Data, Graph
from dataclasses import asdict

def makeChartDataForSingleItem(list, purchases, id):
    snapshots = extractSnapshotDates(list)
    purchase = next((sub for sub in purchases if str(sub['id']) == id), None)
    print(purchase)
    buys = []
    sells = []
    p = []
    d = []
    for snapshot in snapshots:
        item = next((sub for sub in list if sub['item_id'] == purchase['item_id'] and sub['snapshot_id'] == snapshot[0]), None)


        buys.append(item['buy'])
        sells.append(item['sell'])
                    
        d.append(snapshot[1].strftime("%m.%d - %H"))
        p.append(purchase['paid'])

    datasets = []
    dataset = Dataset('buy', buys, 'rgb(255, 0, 0)', False)
    datasets.append(dataset)
    if(sum(sells) > 0):
        dataset = Dataset('sell', sells, 'rgb(0, 255, 0)', False)
        datasets.append(dataset)
    dataset = Dataset('paid', p, 'rgb(0, 0, 255)', False)
    datasets.append(dataset)
    data = Data(d, datasets)

    graph = Graph('line', data) 

    jsonstr = asdict(graph)
    return jsonstr

def makeChartData(list, purchases):
    snapshots = extractSnapshotDates(list)
    sum_of_paid = 0
    for purchase in purchases:
        sum_of_paid += purchase['paid']

    buys = []
    sells = []
    p = []
    d = []
    for snapshot in snapshots:
        sum_buys = 0
        sum_sells = 0
        for purchase in purchases:
            f = next((sub for sub in list if sub['item_id'] == purchase['item_id'] and sub['snapshot_id'] == snapshot[0]), None)
            if f != None:
                sum_buys += f['buy']
                if f['sell'] > 0:
                    sum_sells += f['sell']
                else:
                    sum_sells += f['buy']
        buys.append(sum_buys)
        sells.append(sum_sells)
        d.append(snapshot[1].strftime("%m.%d - %H"))
        p.append(sum_of_paid)

    datasets = []
    dataset = Dataset('buy', buys, 'rgb(255, 0, 0)', False)
    datasets.append(dataset)
    dataset = Dataset('sell', sells, 'rgb(0, 255, 0)', False)
    datasets.append(dataset)
    dataset = Dataset('paid', p, 'rgb(0, 0, 255)', False)
    datasets.append(dataset)
    data = Data(d, datasets)

    graph = Graph('line', data) 

    jsonstr = asdict(graph)
    return jsonstr

def makeChartData1(list):
    b = [x["buy"] for x in list]
    s = [x["sell"] for x in list]
    d = [x["datum"].strftime("%m.%d - %H") for x in list]
    datasets = []
    dataset = Dataset('buy', b, 'rgb(255, 0, 0)', False)
    datasets.append(dataset)
    dataset = Dataset('sell', s, 'rgb(0, 255, 0)', False)
    datasets.append(dataset)
    data = Data(d, datasets)

    graph = Graph('line', data) 

    jsonstr = asdict(graph)
    return jsonstr

def extractSnapshotDates(list):
    res = [y for y in set((x['snapshot_id'], x['snapshot_date']) for x in list)]
    return sorted(res)

def getSumOfPurchases(purchases):
    res = sum([x['paid'] for x in purchases])
    return res