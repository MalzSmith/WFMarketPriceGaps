import requests, json, time

API_BASE = "https://api.warframe.market/v1"
ITEM = "/items"

print('Getting item list...')
r = requests.get(url = API_BASE + ITEM, timeout = 5)

data = r.json()

sets = [x for x in data['payload']['items'] if x['item_name'].endswith(' Set')]
setCount = len(sets)

print(f'Found {setCount} sets.')

def getPrice(url):
    r = requests.get(url = API_BASE + ITEM + '/' + url + '/orders')
    orders = r.json()
    prices = [x['platinum'] for x in orders['payload']['orders'] if x['platform'] == 'pc' and x['order_type'] == 'sell' and x['user']['status'] == 'ingame']
    if (len(prices) == 0):
        return -1
    return min(prices)

deals = []

i = 1
for set in sets:
    print(f'Checking prices for {set["item_name"]} ({i}/{setCount})')
    # Get components for set
    r = requests.get(url = API_BASE + ITEM + '/' + set['url_name'])
    setInfo = r.json()
    parts = [x['url_name'] for x in setInfo['payload']['item']['items_in_set'] if not x['set_root']]

    # Get full set price
    setPrice = getPrice(set['url_name'])
    if (setPrice) == -1:
        print('Skipping...')
        continue

    time.sleep(1) #I'm allowed 3 requests/s, not trying to DDOS wf market....
    # Calculate price for buying parts
    partPrices = 0
    for part in parts:
        partPrice = getPrice(part)
        if (partPrice) == -1:
            print('Skipping...')
            partPrices = -1
            continue
        partPrices += partPrice
    if (partPrices) == -1:
        continue
    grofit = setPrice - partPrices
    print(f'Set price: {setPrice}, Part prices: {partPrices}, possible profit: {grofit}')
    time.sleep(1) #I'm allowed 3 requests/s
    deals.append( {"profit": grofit, "name": set["item_name"]} )
    i += 1

deals = sorted(deals, key = lambda a: a['profit'])

print('List of deals:')
for deal in deals:
    print(f'Set name: {deal["name"]}, possible grofit: {deal["profit"]}')