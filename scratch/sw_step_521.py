Created At: 2026-05-22T04:43:28Z
Completed At: 2026-05-22T04:43:28Z
File Path: `file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/stock_widget.py`
Total Lines: 833
Total Bytes: 39218
Showing lines 380 to 430
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
380:                 canvas.create_polygon(points, fill="#f0f0f0", outline=StockStyle.PRIMARY_GREY, width=1)
381:             else:
382:                 canvas.create_oval(xc-3, y1-3, xc+3, y1+3, fill="#f0f0f0", outline=StockStyle.PRIMARY_GREY, width=1)
383:                 
384:         else:
385:             # 2. 展開模式：顯示小凸起刻度，並擴大坐標區間以容納參考價，且限制超出太多者在端點上
386:             price_points = [low, high, prev, curr]
387:             
388:             # 取得該標的之計算參數
389:             computed = self.data_manager.computed_assets.get(symbol)
390:             if not computed:
391:                 stocks = self.data_manager.config_data.get("stocks", [])
392:                 s_cfg = next((s for s in stocks if s.get("symbol") == symbol), None)
393:                 if s_cfg:
394:                     asset_data = {
395:                         "symbol": symbol.split('_')[-1],
396:                         "type": s_cfg.get("type", "stock"),
397:                         "lastPrice": curr,
398:                         "ma20": s_cfg.get("ma20"),
399:                         "low20": s_cfg.get("low20"),
400:                         "nav": s_cfg.get("nav")
401:                     }
402:                     computed = self.data_manager.compute_asset(asset_data)
403:             
404:             # 收集所有有效的參考點價格，用以計算展示區間
405:             ref_data = {}
406:             if computed:
407:                 for key, name in [
408:                     ("ma20", "20日均線"),
409:                     ("low20", "20日最低"),
410:                     ("nav", "ETF淨值"),
411:                     ("strongBuyPrice", "強烈買進"),
412:                     ("buyPrice", "買進價位"),
413:                     ("watchPrice", "觀察價位")
414:                 ]:
415:                     val = computed.get(key)
416:                     if val is not None and val > 0:
417:                         price_points.append(val)
418:                         ref_data[key] = (val, name)
419:             
420:             # 計算核心波動區間與外擴 30% 區間
421:             v_core_min = min(low, prev, curr)
422:             v_core_max = max(high, prev, curr)
423:             v_core_range = v_core_max - v_core_min
424:             margin = max(v_core_range * 0.3, prev * 0.01 if prev > 0 else 1.0)
425:             
426:             v_axis_min = v_core_min - margin
427:             v_axis_max = v_core_max + margin
428:             
429:             start_x = 8
430:             uw = w - 16
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.
