import urllib.request
import json
import time

symbols = ["0050.TW", "2603.TW", "00679B.TWO"]
for symbol in symbols:
    try:
        ts = int(time.time())
        url = f'https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}&_={ts}'
        print(f"Testing URL: {url}")
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
        with urllib.request.urlopen(req, timeout=5) as res:
            content = res.read().decode('utf-8')
            print(f"Response for {symbol}: {content[:200]}...")
            data = json.loads(content)
            if 'quoteResponse' in data and data['quoteResponse']['result']:
                result = data['quoteResponse']['result'][0]
                print(f"Success: {symbol} price is {result.get('regularMarketPrice')}")
            else:
                print(f"Failed: No result in response for {symbol}")
    except Exception as e:
        print(f"Error for {symbol}: {e}")
