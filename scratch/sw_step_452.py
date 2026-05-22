Created At: 2026-05-22T03:56:24Z
Completed At: 2026-05-22T03:56:24Z
File Path: `file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/stock_widget.py`
Total Lines: 721
Total Bytes: 34410
Showing lines 480 to 510
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
480:             elif curr < prev:
481:                 # 向左空心三角形
482:                 points = [xc-4, y1, xc+3, y1-4, xc+3, y1+4]
483:                 canvas.create_polygon(points, fill="#f0f0f0", outline=StockStyle.PRIMARY_GREY, width=1)
484:             else:
485:                 # 平盤圓圈
486:                 canvas.create_oval(xc-3, y1-3, xc+3, y1+3, fill="#f0f0f0", outline=StockStyle.PRIMARY_GREY, width=1)
487: 
488:     def _on_bar_click(self, event, canvas):
489:         if hasattr(canvas, "stock_coords") and canvas.stock_coords:
490:             # 尋找距離滑鼠點擊 x 坐標最近的刻度項
491:             best_item = min(canvas.stock_coords, key=lambda item: abs(event.x - item['x']))
492:             
493:             # 點擊位置在最近刻度的 8 像素內才進行提示，避免誤觸
494:             if abs(event.x - best_item['x']) <= 8:
495:                 text = f"{best_item['lbl']}:{best_item['val']:.2f}"
496:                 self._show_temp_val(canvas, text, best_item['x'])
497: 
498:     def _toggle_detail_bar(self, symbol):
499:         if symbol in self.expanded_bars:
500:             self.expanded_bars.remove(symbol)
501:         else:
502:             self.expanded_bars.add(symbol)
503:         # 重新繪製該 symbol 的 Canvas
504:         if symbol in self.labels:
505:             _, _, canvas, _ = self.labels[symbol]
506:             if hasattr(canvas, "last_draw_values") and canvas.last_draw_values:
507:                 prev, curr, high, low = canvas.last_draw_values
508:                 self._draw_status_bar(canvas, prev, curr, high, low, symbol)
509: 
510:     def _show_temp_val(self, canvas, text, x):
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.
