import urllib.request
import json
import time

query = "tse_0050.tw|otc_00679B.tw"
ts = int(time.time() * 1000)
url = f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={query}&json=1&delay=0&_={ts}"

print(f"URL: {url}")
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=10) as res:
        data = json.loads(res.read())
        if 'msgArray' in data and len(data['msgArray']) > 0:
            item = data['msgArray'][0]
            print("\nKeys in first item:")
            for k in sorted(item.keys()):
                print(f"  {k}: {item[k]}")
        else:
            print("No msgArray or empty")
            print(data)
except Exception as e:
    print(f"Error: {e}")
