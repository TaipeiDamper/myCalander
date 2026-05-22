Created At: 2026-05-22T03:21:48Z
Completed At: 2026-05-22T03:21:48Z
File Path: `file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/stock_widget.py`
Total Lines: 730
Total Bytes: 34948
Showing lines 316 to 335
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
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
