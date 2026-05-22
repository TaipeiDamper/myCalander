Created At: 2026-05-22T03:56:06Z
Completed At: 2026-05-22T03:56:06Z
File Path: `file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/stock_widget.py`
Total Lines: 721
Total Bytes: 34417
Showing lines 381 to 460
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
381:             
382:             # 取得該標的之計算參數
383:             computed = self.data_manager.computed_assets.get(symbol)
384:             if not computed:
385:                 stocks = self.data_manager.config_data.get("stocks", [])
386:                 s_cfg = next((s for s in stocks if s.get("symbol") == symbol), None)
387:                 if s_cfg:
388:                     asset_data = {
389:                         "symbol": symbol.split('_')[-1],
390:                         "type": s_cfg.get("type", "stock"),
391:                         "lastPrice": curr,
392:                         "ma20": s_cfg.get("ma20", curr),
393:                         "low20": s_cfg.get("low20", curr * 0.95),
394:                         "nav": s_cfg.get("nav")
395:                     }
396:                     computed = self.data_manager.compute_asset(asset_data)
397:             
398:             # 收集所有有效的參考點價格，用以計算展示區間
399:             ref_data = {}
400:             if computed:
401:                 for key, name in [
402:                     ("ma20", "20日均線"),
403:                     ("low20", "20日最低"),
404:                     ("nav", "ETF淨值"),
405:                     ("strongBuyPrice", "強烈買進"),
406:                     ("buyPrice", "買進價位"),
407:                     ("watchPrice", "觀察價位")
408:                 ]:
409:                     val = computed.get(key)
410:                     if val is not None and val > 0:
411:                         pric
<truncated 1038 bytes>
  
434:             # 計算核心元素的 x 座標 (因為都在核心區間內，絕不會被 Clamping 擠到最邊緣)
435:             xl, xh, xp, xc = get_x_clamped(low), get_x_clamped(high), get_x_clamped(prev), get_x_clamped(curr)
436:             
437:             # 記錄核心點坐標以供點擊提示
438:             canvas.stock_coords.append({'x': xl, 'val': low, 'lbl': '今日最低'})
439:             canvas.stock_coords.append({'x': xh, 'val': high, 'lbl': '今日最高'})
440:             canvas.stock_coords.append({'x': xp, 'val': prev, 'lbl': '昨日收盤'})
441:             canvas.stock_coords.append({'x': xc, 'val': curr, 'lbl': '現在價格'})
442:             
443:             # A. 繪製橫向背景參考細線
444:             canvas.create_line(start_x, y1, start_x + uw, y1, fill="#e6e6e6", width=1)
445:             
446:             # B. 繪製今日高低範圍粗軌道 (疊加在背景細線上)
447:             canvas.create_line(xl, y1, xh, y1, fill=StockStyle.BAR_TRACK, width=4, capstyle=tk.ROUND)
448:             
449:             # C. 繪製昨收垂直引導虛線 (高度延伸，y=4 到 y=20)
450:             canvas.create_line(xp, y1-8, xp, y1+8, fill=StockStyle.BAR_GUIDE, width=1, dash=(2, 2))
451:             
452:             # D. 繪製參考點小凸起 (垂直刻度)
453:             if computed:
454:                 # 判斷是否為 ETF 買點退化狀態
455:                 is_degraded = (computed.get("status") == "watch" and computed.get("type") == "etf" and (computed.get("premiumDiscount") or 0) > 1.0)
456:                 
457:                 for key, (val, name) in ref_data.items():
458:                     xk = get_x_clamped(val)
459:                     
460:                     # 區分刻度高度：背景參考高度 6 (上下各 3)，決策警戒高度 8 (上下各 4)
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.
