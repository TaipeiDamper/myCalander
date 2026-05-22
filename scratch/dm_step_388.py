Created At: 2026-05-22T03:46:46Z
Completed At: 2026-05-22T03:46:46Z
File Path: `file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/data_manager.py`
Total Lines: 398
Total Bytes: 15358
Showing lines 1 to 398
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
<truncated 13705 bytes>
ts.append({
350:                     "symbol": symbol.split('_')[-1],
351:                     "type": "LONG_DOWN",
352:                     "value": diff_long_down_pct,
353:                     "price": curr
354:                 })
355:             elif diff_short_pct >= short_th:
356:                 alerts.append({
357:                     "symbol": symbol.split('_')[-1],
358:                     "type": "SHORT",
359:                     "value": diff_short_pct,
360:                     "price": curr
361:                 })
362:         return alerts
363: 
364: 
365: 
366:     def _parse_item(self, item):
367: 
368:         def parse_f(v, default=0.0):
369:             if v == '-' or v is None: return default
370:             try: return float(v)
371:             except: return default
372: 
373:         # 價格優先級：成交價(z) > 賣標(a) > 買標(b) > 昨收(y)
374:         z = item.get('z', '-')
375:         a = item.get('a', '-').split('_')[0] if item.get('a', '-') != '-' else '-'
376:         b = item.get('b', '-').split('_')[0] if item.get('b', '-') != '-' else '-'
377:         y = item.get('y', '0')
378: 
379:         curr_str = '-'
380:         if z != '-': curr_str = z
381:         elif a != '-': curr_str = a
382:         elif b != '-': curr_str = b
383:         else: curr_str = y
384: 
385:         curr_val = parse_f(curr_str)
386:         prev_val = parse_f(item.get('y'), curr_val)
387:         high_val = parse_f(item.get('h'), curr_val)
388:         low_val = parse_f(item.get('l'), curr_val)
389:         
390:         try:
391:             # 先轉 float 去掉無效尾隨零，再轉 string 判斷小數位
392:             clean_str = str(float(curr_str))
393:             hint = len(clean_str.split(".")[1]) if "." in clean_str else 0
394:             hint = max(2, hint) # 最少顯示兩位
395:         except:
396:             hint = 2
397:         return (prev_val, curr_val, high_val, low_val, hint)
398: 
The above content shows the entire, complete file contents of the requested file.
