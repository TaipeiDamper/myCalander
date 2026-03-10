import urllib.request
import json
import time

def to_float(v, default=None):
    if v == '-' or v is None: return default
    try:
        return float(v)
    except:
        return default

stocks = ["tse_0050", "otc_00679B", "otc_00687B", "tse_2603", "tse_2609"]
query_parts = [f"{s}.tw" for s in stocks]
symbol_map = {s.split('_')[-1]: s for s in stocks}

ts = int(time.time() * 1000)
url = f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={'|'.join(query_parts)}&json=1&delay=0&_={ts}"

print(f"URL: {url}")
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})

try:
    with urllib.request.urlopen(req, timeout=5) as res:
        data = json.loads(res.read().decode('utf-8'))
        if 'msgArray' in data:
            print(f"Success! Found {len(data['msgArray'])} stocks.")
            for item in data['msgArray']:
                code = item.get('c')
                config_symbol = symbol_map.get(code)
                
                curr_str = item.get('z', '-')
                if curr_str == '-':
                    b_str = item.get('b', '-')
                    if b_str != '-': curr_str = b_str.split('_')[0]
                if curr_str == '-':
                    a_str = item.get('a', '-')
                    if a_str != '-': curr_str = a_str.split('_')[0]
                if curr_str == '-':
                    curr_str = item.get('y', '0')
                
                curr_val = to_float(curr_str, 0.0)
                prev_val = to_float(item.get('y'), curr_val)
                high_val = to_float(item.get('h'), curr_val)
                low_val = to_float(item.get('l'), curr_val)
                
                print(f"Code: {code} | Symbol: {config_symbol}")
                print(f"  Price: {curr_val} (from {curr_str})")
                print(f"  Prev: {prev_val}, High: {high_val}, Low: {low_val}")
        else:
            print("msgArray missing!")
            print(data)
except Exception as e:
    print(f"Fatal error: {e}")
