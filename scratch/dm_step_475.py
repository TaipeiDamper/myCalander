Created At: 2026-05-22T04:27:12Z
Completed At: 2026-05-22T04:27:12Z
File Path: `file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/data_manager.py`
Total Lines: 409
Total Bytes: 15695
Showing lines 1 to 409
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
1: import json
2: import os
3: import urllib.request
4: import time
5: import threading
6: import datetime
7: 
8: class StockDataManager:
9:     """處理股票數據的載入、儲存與網路請求"""
10:     
11:     def __init__(self, config_path):
12:         self.config_path = config_path
13:         self.config_data = self.load_config()
14:         self.computed_assets = {}
15: 
16:     def load_config(self):
17:         try:
18:             if os.path.exists(self.config_path):
19:                 with open(self.config_path, "r", encoding="utf-8") as f:
20:                     return json.load(f)
21:         except Exception as e:
22:             print(f"Error loading config: {e}")
23:         
24:         # 預設值
25:         return {
26:             "update_interval_seconds": 60,
27:             "stocks": [
28:                 {"symbol": "tse_0050", "reference": 190.0},
29:                 {"symbol": "tse_2330", "reference": 800.0}
30:             ]
31:         }
32: 
33:     def save_stock_params(self, symbol, params):
34:         """儲存特定股票的參數 (參考價, 警報門檻)"""
35:         changed = False
36:         
37:         # 格式化數值型態參數，避免寫入 string 格式
38:         formatted_params = {}
39:         for k, v in params.items():
40:             if k in ["ma20", "low20", "nav", "reference"]:
41:                 try:
42:                     formatted_params[k] = float(v) if v not in [None, '', '-'] else None
43:                 except:
44:                     formatted_params[k] = None
45: 
<truncated 14097 bytes>
ts.append({
361:                     "symbol": symbol.split('_')[-1],
362:                     "type": "LONG_DOWN",
363:                     "value": diff_long_down_pct,
364:                     "price": curr
365:                 })
366:             elif diff_short_pct >= short_th:
367:                 alerts.append({
368:                     "symbol": symbol.split('_')[-1],
369:                     "type": "SHORT",
370:                     "value": diff_short_pct,
371:                     "price": curr
372:                 })
373:         return alerts
374: 
375: 
376: 
377:     def _parse_item(self, item):
378: 
379:         def parse_f(v, default=0.0):
380:             if v == '-' or v is None: return default
381:             try: return float(v)
382:             except: return default
383: 
384:         # 價格優先級：成交價(z) > 賣標(a) > 買標(b) > 昨收(y)
385:         z = item.get('z', '-')
386:         a = item.get('a', '-').split('_')[0] if item.get('a', '-') != '-' else '-'
387:         b = item.get('b', '-').split('_')[0] if item.get('b', '-') != '-' else '-'
388:         y = item.get('y', '0')
389: 
390:         curr_str = '-'
391:         if z != '-': curr_str = z
392:         elif a != '-': curr_str = a
393:         elif b != '-': curr_str = b
394:         else: curr_str = y
395: 
396:         curr_val = parse_f(curr_str)
397:         prev_val = parse_f(item.get('y'), curr_val)
398:         high_val = parse_f(item.get('h'), curr_val)
399:         low_val = parse_f(item.get('l'), curr_val)
400:         
401:         try:
402:             # 先轉 float 去掉無效尾隨零，再轉 string 判斷小數位
403:             clean_str = str(float(curr_str))
404:             hint = len(clean_str.split(".")[1]) if "." in clean_str else 0
405:             hint = max(2, hint) # 最少顯示兩位
406:         except:
407:             hint = 2
408:         return (prev_val, curr_val, high_val, low_val, hint)
409: 
The above content shows the entire, complete file contents of the requested file.
