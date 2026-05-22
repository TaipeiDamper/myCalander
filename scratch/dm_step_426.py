Created At: 2026-05-22T03:55:03Z
Completed At: 2026-05-22T03:55:04Z
File Path: `file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/data_manager.py`
Total Lines: 406
Total Bytes: 15683
Showing lines 280 to 320
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
280:                     for item in raw['msgArray']:
281:                         code = item.get('c')
282:                         config_symbol = symbol_map.get(code)
283:                         if not config_symbol: continue
284:                         parsed = self._parse_item(item)
285:                         if parsed:
286:                             updates[config_symbol] = parsed
287:         except Exception as e:
288:             print(f"Error fetching real-time prices: {e}")
289: 
290:         # 4. 計算三層預警價位與狀態分析
291:         self.computed_assets = {}
292:         stocks_dict = {s['symbol']: s for s in stocks}
293:         for symbol, parsed in updates.items():
294:             s_cfg = stocks_dict.get(symbol, {})
295:             curr_val = parsed[1]
296:             code = symbol.split('_')[-1]
297: 
298:             # 若為 ETF，優先使用盤中即時淨值，否則使用設定檔中之 nav，或現價作為 fallback
299:             nav_val = None
300:             if s_cfg.get("type") == "etf":
301:                 nav_val = etf_navs.get(code)
302:                 if nav_val is None:
303:                     nav_val = s_cfg.get("nav")
304:                 else:
305:                     # 同步更新記憶體與設定檔中的 nav，便於介面使用與存檔
306:                     s_cfg["nav"] = nav_val
307: 
308:             asset_data = {
309:                 "symbol": code,
310:                 "type": s_cfg.get("type", "stock"),
311:                 "lastPrice": curr_val,
312:                 "ma20": s_cfg.get("ma20", curr_val),
313:                 "low20": s_cfg.get("low20", curr_val * 0.95),
314:                 "nav": nav_val
315:             }
316:             computed = self.compute_asset(asset_data)
317:             self.computed_assets[symbol] = computed
318: 
319:         # 檢查預警實例
320:         alerts = self._check_alerts(updates)
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.
