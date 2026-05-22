Created At: 2026-05-22T03:32:03Z
Completed At: 2026-05-22T03:32:03Z
File Path: `file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/data_manager.py`
Total Lines: 272
Total Bytes: 10000
Showing lines 150 to 195
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
150:                 callback({})
151: 
152:         threading.Thread(target=task, daemon=True).start()
153: 
154:     def _do_fetch(self):
155:         stocks = self.config_data.get("stocks", [])
156:         if not stocks: return {}
157: 
158:         query_parts = []
159:         symbol_map = {} 
160:         for s in stocks:
161:             key = s.get("symbol", "")
162:             if not key: continue
163:             query_parts.append(f"{key}.tw")
164:             symbol_map[key.split('_')[-1]] = key
165: 
166:         ts = int(time.time() * 1000)
167:         url = f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={'|'.join(query_parts)}&json=1&delay=0&_={ts}"
168:         req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
169:         
170:         updates = {}
171:         with urllib.request.urlopen(req, timeout=5) as res:
172:             raw = json.loads(res.read())
173:             if 'msgArray' not in raw: return {}
174:             
175:             for item in raw['msgArray']:
176:                 code = item.get('c')
177:                 config_symbol = symbol_map.get(code)
178:                 if not config_symbol: continue
179:                 
180:                 # 數據解析邏輯
181:                 parsed = self._parse_item(item)
182:                 if parsed:
183:                     updates[config_symbol] = parsed
184:         
185:         # 檢查預警實例
186:         alerts = self._check_alerts(updates)
187:         return {"updates": updates, "alerts": alerts}
188: 
189:     def _check_alerts(self, updates):
190:         """檢查股票預警：短線看昨收差異，長線看基準價差異"""
191:         alerts = []
192:         global_short = self.config_data.get("alert_threshold_short", 5.0)
193:         global_long = self.config_data.get("alert_threshold_long", 15.0)
194:         
195:         stocks_config = {s['symbol']: s for s in self.config_data.get("stocks", [])}
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.
