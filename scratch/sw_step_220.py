Created At: 2026-05-22T03:30:12Z
Completed At: 2026-05-22T03:30:12Z
File Path: `file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/stock_widget.py`
Total Lines: 539
Total Bytes: 24542
Showing lines 280 to 410
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
280:     def _draw_status_bar(self, canvas, prev, curr, high, low):
281:         canvas.delete("all")
282:         w, h = int(canvas.cget("width")), int(canvas.cget("height"))
283:         
284:         # 置中計算
285:         v_low, v_high = min(low, prev), max(high, prev)
286:         v_range = v_high - v_low
287:         v_range_pct = (v_range / prev * 100.0) if prev > 0 else 0
288:         
289:         scale = min(1.0, (v_range_pct / 10.0) ** 0.7) if v_range_pct > 0 else 0.05
290:         uw = (w - 12) * scale
291:         if uw < 10: uw = 10
292:         start_x = (w - uw) / 2
293:         
294:         def get_x(v):
295:             return start_x + (v - v_low) / (v_high - v_low) * uw if v_high > v_low else w/2
296: 
297:         xl, xh, xp, xc = get_x(low), get_x(high), get_x(prev), get_x(curr)
298:         canvas.stock_coords = {'low': low, 'high': high, 'x_low': xl, 'x_high': xh}
299: 
300:         # 軌道
301:         canvas.create_line(xl, h/2, xh, h/2, fill=StockStyle.BAR_TRACK, width=4, capstyle=tk.ROUND)
302:         # 端點
303:         for x in (xl, xh): canvas.create_oval(x-2, h/2-2, x+2, h/2+2, fill="#eeeeee", outline="")
304:         # 昨收線：改為寬度 1 並使用虛線，減少視覺重量
305:         canvas.create_line(xp, 4, xp, h-4, fill=StockStyle.BAR_GUIDE, width=1, dash=(2, 2))
306:         
307:         # 指示器：縮小尺寸並加入淺色填充，改善重疊感
308:         if curr != prev:
309:             # 寬度從 9 改為 7, 高度從 10 改為 8
310:             points = [xc+4, h/2, xc-
<truncated 3507 bytes>
, str(stock_cfg.get('alert_short', ''))); e_short.grid(row=1, column=1)
383:         
384:         tk.Label(dialog, text="---------------------------", fg="#ccc").pack()
385:         
386:         # 長線預警 (vs 基準) - 雙向綁定
387:         fm2 = tk.Frame(dialog); fm2.pack(padx=10, fill=tk.X)
388:         tk.Label(fm2, text="長線目標價上下限/百分比(vs基準):", font=("Arial", 8, "italic")).grid(row=0, column=0, columnspan=4, pady=(0,5))
389:         
390:         tk.Label(fm2, text="目標上限:").grid(row=1, column=0, sticky="e")
391:         e_target_up_p = tk.Entry(fm2, width=8); e_target_up_p.grid(row=1, column=1)
392:         tk.Label(fm2, text="%:").grid(row=1, column=2, sticky="e")
393:         e_target_up_pct = tk.Entry(fm2, width=6); e_target_up_pct.grid(row=1, column=3)
394:         
395:         tk.Label(fm2, text="目標下限:").grid(row=2, column=0, sticky="e")
396:         e_target_down_p = tk.Entry(fm2, width=8); e_target_down_p.grid(row=2, column=1)
397:         tk.Label(fm2, text="%:").grid(row=2, column=2, sticky="e")
398:         e_target_down_pct = tk.Entry(fm2, width=6); e_target_down_pct.grid(row=2, column=3)
399:         
400:         # 初始填充長線數值
401:         def_long = self.data_manager.config_data.get('alert_threshold_long', 15.0)
402:         curr_up_th = stock_cfg.get('alert_long_up', stock_cfg.get('alert_long', def_long))
403:         curr_down_th = stock_cfg.get('alert_long_down', stock_cfg.get('alert_long', def_long))
404:         
405:         e_target_up_pct.insert(0, str(curr_up_th))
406:         e_target_down_pct.insert(0, str(curr_down_th))
407:         try:
408:             target_up_p = current_ref * (1 + curr_up_th/100.0)
409:             e_target_up_p.insert(0, f"{target_up_p:.2f}")
410:             target_down_p = current_ref * (1 - curr_down_th/100.0)
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.
