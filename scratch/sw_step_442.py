Created At: 2026-05-22T03:56:03Z
Completed At: 2026-05-22T03:56:03Z
File Path: `file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/stock_widget.py`
Total Lines: 721
Total Bytes: 34417
Showing lines 340 to 380
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
340:             v_range = v_high - v_low
341:             v_range_pct = (v_range / prev * 100.0) if prev > 0 else 0
342:             
343:             # 使用 scale 設計讓無波動時軌道縮短，有波動時拉長
344:             scale = min(1.0, (v_range_pct / 10.0) ** 0.7) if v_range_pct > 0 else 0.05
345:             uw = (w - 12) * scale
346:             if uw < 10: uw = 10
347:             start_x = (w - uw) / 2
348:             
349:             def get_x(v):
350:                 return start_x + (v - v_low) / (v_high - v_low) * uw if v_high > v_low else w / 2
351:                 
352:             xl, xh, xp, xc = get_x(low), get_x(high), get_x(prev), get_x(curr)
353:             
354:             # 記錄坐標以供點擊提示 (未展開時只有高、低、昨收、現價)
355:             canvas.stock_coords.append({'x': xl, 'val': low, 'lbl': '今日最低'})
356:             canvas.stock_coords.append({'x': xh, 'val': high, 'lbl': '今日最高'})
357:             canvas.stock_coords.append({'x': xp, 'val': prev, 'lbl': '昨日收盤'})
358:             canvas.stock_coords.append({'x': xc, 'val': curr, 'lbl': '現在價格'})
359:             
360:             # 繪製行情軌道 (BAR_TRACK)
361:             canvas.create_line(xl, y1, xh, y1, fill=StockStyle.BAR_TRACK, width=4, capstyle=tk.ROUND)
362:             for x in (xl, xh): 
363:                 canvas.create_oval(x-2, y1-2, x+2, y1+2, fill="#eeeeee", outline="")
364:             
365:             # 昨收引導線 (BAR_GUIDE) - 未展開時高度較短
366:             canvas.create_line(xp, y1-4, xp, y1+4, fill=StockStyle.BAR_GUIDE, width=1, dash=(2, 2))
367:             
368:             # 現價指針 (依漲跌決定三角形方向，或平盤為圓圈)
369:             if curr > prev:
370:                 points = [xc+4, y1, xc-3, y1-4, xc-3, y1+4]
371:                 canvas.create_polygon(points, fill="#f0f0f0", outline=StockStyle.PRIMARY_GREY, width=1)
372:             elif curr < prev:
373:                 points = [xc-4, y1, xc+3, y1-4, xc+3, y1+4]
374:                 canvas.create_polygon(points, fill="#f0f0f0", outline=StockStyle.PRIMARY_GREY, width=1)
375:             else:
376:                 canvas.create_oval(xc-3, y1-3, xc+3, y1+3, fill="#f0f0f0", outline=StockStyle.PRIMARY_GREY, width=1)
377:                 
378:         else:
379:             # 2. 展開模式：顯示小凸起刻度，並擴大坐標區間以容納參考價，且限制超出太多者在端點上
380:             price_points = [low, high, prev, curr]
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.
