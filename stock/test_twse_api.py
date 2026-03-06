import urllib.request
import json
import time

# 測試台灣證交所官方實時 API
# 格式: ex_ch=tse_0050.tw|otc_00679B.tw
# tse = 上市, otc = 上櫃
symbols = "tse_0050.tw|tse_2603.tw|tse_2609.tw|otc_00679B.tw|otc_00687B.tw"
url = f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={symbols}&json=1&delay=0&_={int(time.time()*1000)}"

try:
    print(f"Requesting: {url}")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=5) as res:
        content = res.read().decode('utf-8')
        data = json.loads(content)
        if 'msgArray' in data:
            for item in data['msgArray']:
                name = item.get('n')
                code = item.get('c')
                # z=現價, y=昨收, h=最高, l=最低
                price = item.get('z', 'N/A')
                y_price = item.get('y', 'N/A')
                print(f"Stock: {name} ({code}), Price: {price}, Prev Close: {y_price}")
        else:
            print("Failed to get msgArray")
            print(f"Full response: {content}")
except Exception as e:
    print(f"Error: {e}")
