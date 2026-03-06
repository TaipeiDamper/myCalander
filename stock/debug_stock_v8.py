import urllib.request
import json
import time

symbols = ["0050.TW", "2603.TW", "00679B.TWO"]
for symbol in symbols:
    try:
        ts = int(time.time())
        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1m&range=1d&_={ts}'
        print(f"Testing URL: {url}")
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as res:
            content = res.read().decode('utf-8')
            print(f"Response code: {res.getcode()}")
            data = json.loads(content)
            if 'chart' in data and data['chart']['result']:
                meta = data['chart']['result'][0]['meta']
                print(f"Success: {symbol} price is {meta.get('regularMarketPrice')}")
            else:
                print(f"Failed: No result in response for {symbol}")
    except Exception as e:
        print(f"Error for {symbol}: {e}")
