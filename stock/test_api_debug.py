import urllib.request
import json
import time

stocks = [
    {"symbol": "tse_0050"},
    {"symbol": "otc_00679B"},
    {"symbol": "otc_00687B"},
    {"symbol": "tse_2603"},
    {"symbol": "tse_2609"}
]

query_parts = [f"{s['symbol']}.tw" for s in stocks]
ts = int(time.time() * 1000)
url = f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={'|'.join(query_parts)}&json=1&delay=0&_={ts}"

print(f"Requesting URL: {url}")

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

try:
    with urllib.request.urlopen(req, timeout=10) as res:
        raw_content = res.read().decode('utf-8')
        print(f"Raw response: {raw_content[:500]}...")
        data = json.loads(raw_content)
        if 'msgArray' in data:
            print(f"Found {len(data['msgArray'])} stocks in msgArray")
            for item in data['msgArray']:
                print(f"Symbol: {item.get('c')}, Name: {item.get('n')}, Price: {item.get('z', item.get('b', item.get('y')))}")
        else:
            print("msgArray not found in response")
            print(f"Response keys: {data.keys()}")
except Exception as e:
    print(f"Error: {e}")
