Created At: 2026-05-22T03:30:27Z
Completed At: 2026-05-22T03:30:27Z
File Path: `file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/stock_widget.py`
Total Lines: 542
Total Bytes: 24894
Showing lines 280 to 335
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
280:             self.after_cancel(self._update_job)
281:         self._update_job = self.after(self.update_interval_ms, self.refresh_prices)
282: 
283:     def _draw_status_bar(self, canvas, prev, curr, high, low):
284:         canvas.delete("all")
285:         w, h = int(canvas.cget("width")), int(canvas.cget("height"))
286:         
287:         # 置中計算
288:         v_low, v_high = min(low, prev), max(high, prev)
289:         v_range = v_high - v_low
290:         v_range_pct = (v_range / prev * 100.0) if prev > 0 else 0
291:         
292:         scale = min(1.0, (v_range_pct / 10.0) ** 0.7) if v_range_pct > 0 else 0.05
293:         uw = (w - 12) * scale
294:         if uw < 10: uw = 10
295:         start_x = (w - uw) / 2
296:         
297:         def get_x(v):
298:             return start_x + (v - v_low) / (v_high - v_low) * uw if v_high > v_low else w/2
299: 
300:         xl, xh, xp, xc = get_x(low), get_x(high), get_x(prev), get_x(curr)
301:         canvas.stock_coords = {'low': low, 'high': high, 'x_low': xl, 'x_high': xh}
302: 
303:         # 軌道
304:         canvas.create_line(xl, h/2, xh, h/2, fill=StockStyle.BAR_TRACK, width=4, capstyle=tk.ROUND)
305:         # 端點
306:         for x in (xl, xh): canvas.create_oval(x-2, h/2-2, x+2, h/2+2, fill="#eeeeee", outline="")
307:         # 昨收線：改為寬度 1 並使用虛線，減少視覺重量
308:         canvas.create_line(xp, 4, xp, h-4, fill=StockStyle.BAR_GUIDE, width=1, dash=(2, 2))
309:         
310:         # 指示器：縮小尺寸並加入淺色填充，改善重疊感
311:         if curr != prev:
312:             # 寬度從 9 改為 7, 高度從 10 改為 8
313:             points = [xc+4, h/2, xc-3, h/2-4, xc-3, h/2+4] if curr > prev else [xc-4, h/2, xc+3, h/2-4, xc+3, h/2+4]
314:             canvas.create_polygon(points, fill="#f0f0f0", outline=StockStyle.PRIMARY_GREY, width=1)
315:         else:
316:             canvas.create_oval(xc-3, h/2-3, xc+3, h/2+3, fill="#f0f0f0", outline=StockStyle.PRIMARY_GREY, width=1)
317: 
318:     def _on_bar_click(self, event, canvas):
319:         if hasattr(canvas, "stock_coords"):
320:             coords = canvas.stock_coords
321:             # 改為判斷距離點擊位置最近的座標 (L 或 H)
322:             dist_l = abs(event.x - coords['x_low'])
323:             dist_h = abs(event.x - coords['x_high'])
324:             
325:             if dist_l < dist_h:
326:                 self._show_temp_val(canvas, f"L:{coords['low']:.2f}", coords['x_low'])
327:             else:
328:                 self._show_temp_val(canvas, f"H:{coords['high']:.2f}", coords['x_high'])
329:             return
330: 
331:     def _show_temp_val(self, canvas, text, x):
332:         self._hide_temp_val(canvas) # 先清除舊的
333:         
334:         # 顯示數值，座標上移一點預留間距
335:         canvas.create_text(x, 6, text=text, fill=StockStyle.TEXT_POPUP, font=StockStyle.FONT_BOLD, tags="temp_val")
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.
