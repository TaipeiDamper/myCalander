Created At: 2026-05-22T03:31:46Z
Completed At: 2026-05-22T03:31:46Z
File Path: `file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/data_manager.py`
Total Lines: 191
Total Bytes: 6886
Showing lines 1 to 191
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
1: import json
2: import os
3: import urllib.request
4: import time
5: import threading
6: 
7: class StockDataManager:
8:     """處理股票數據的載入、儲存與網路請求"""
9:     
10:     def __init__(self, config_path):
11:         self.config_path = config_path
12:         self.config_data = self.load_config()
13: 
14:     def load_config(self):
15:         try:
16:             if os.path.exists(self.config_path):
17:                 with open(self.config_path, "r", encoding="utf-8") as f:
18:                     return json.load(f)
19:         except Exception as e:
20:             print(f"Error loading config: {e}")
21:         
22:         # 預設值
23:         return {
24:             "update_interval_seconds": 60,
25:             "stocks": [
26:                 {"symbol": "tse_0050", "reference": 190.0},
27:                 {"symbol": "tse_2330", "reference": 800.0}
28:             ]
29:         }
30: 
31:     def save_stock_params(self, symbol, params):
32:         """儲存特定股票的參數 (參考價, 警報門檻)"""
33:         changed = False
34:         for stock in self.config_data.get("stocks", []):
35:             if stock.get("symbol") == symbol:
36:                 stock.update(params)
37:                 if "alert_long" in stock and "alert_long_up" in params:
38:                     del stock["alert_long"]
39:                 changed = True
40:                 break
41:         
42:         if changed:
43:             return self._save_to_disk()
44:         return False
45: 
46:     def update_global_config(
<truncated 4197 bytes>
ts.append({
143:                     "symbol": symbol.split('_')[-1],
144:                     "type": "LONG_DOWN",
145:                     "value": diff_long_down_pct,
146:                     "price": curr
147:                 })
148:             elif diff_short_pct >= short_th:
149:                 alerts.append({
150:                     "symbol": symbol.split('_')[-1],
151:                     "type": "SHORT",
152:                     "value": diff_short_pct,
153:                     "price": curr
154:                 })
155:         return alerts
156: 
157: 
158: 
159:     def _parse_item(self, item):
160: 
161:         def parse_f(v, default=0.0):
162:             if v == '-' or v is None: return default
163:             try: return float(v)
164:             except: return default
165: 
166:         # 價格優先級：成交價(z) > 賣標(a) > 買標(b) > 昨收(y)
167:         z = item.get('z', '-')
168:         a = item.get('a', '-').split('_')[0] if item.get('a', '-') != '-' else '-'
169:         b = item.get('b', '-').split('_')[0] if item.get('b', '-') != '-' else '-'
170:         y = item.get('y', '0')
171: 
172:         curr_str = '-'
173:         if z != '-': curr_str = z
174:         elif a != '-': curr_str = a
175:         elif b != '-': curr_str = b
176:         else: curr_str = y
177: 
178:         curr_val = parse_f(curr_str)
179:         prev_val = parse_f(item.get('y'), curr_val)
180:         high_val = parse_f(item.get('h'), curr_val)
181:         low_val = parse_f(item.get('l'), curr_val)
182:         
183:         try:
184:             # 先轉 float 去掉無效尾隨零，再轉 string 判斷小數位
185:             clean_str = str(float(curr_str))
186:             hint = len(clean_str.split(".")[1]) if "." in clean_str else 0
187:             hint = max(2, hint) # 最少顯示兩位
188:         except:
189:             hint = 2
190:         return (prev_val, curr_val, high_val, low_val, hint)
191: 
The above content shows the entire, complete file contents of the requested file.
