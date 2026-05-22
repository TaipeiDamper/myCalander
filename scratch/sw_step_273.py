Created At: 2026-05-22T03:34:34Z
Completed At: 2026-05-22T03:34:34Z
File Path: `file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/stock_widget.py`
Total Lines: 690
Total Bytes: 32767
Showing lines 450 to 485
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
450:     def _on_bar_click(self, event, canvas):
451:         if hasattr(canvas, "stock_coords") and canvas.stock_coords:
452:             # 尋找距離滑鼠點擊 x 坐標最近的刻度項
453:             best_item = min(canvas.stock_coords, key=lambda item: abs(event.x - item['x']))
454:             
455:             # 點擊位置在最近刻度的 8 像素內才進行提示，避免誤觸
456:             if abs(event.x - best_item['x']) <= 8:
457:                 text = f"{best_item['lbl']}:{best_item['val']:.2f}"
458:                 self._show_temp_val(canvas, text, best_item['x'])
459: 
460:     def _expand_bar(self, symbol):
461:         self.expanded_bars.add(symbol)
462:         # 重新繪製該 symbol 的 Canvas
463:         if symbol in self.labels:
464:             _, _, canvas, _ = self.labels[symbol]
465:             if hasattr(canvas, "last_draw_values") and canvas.last_draw_values:
466:                 prev, curr, high, low = canvas.last_draw_values
467:                 self._draw_status_bar(canvas, prev, curr, high, low, symbol)
468: 
469:     def _collapse_bar(self, symbol):
470:         if symbol in self.expanded_bars:
471:             self.expanded_bars.remove(symbol)
472:             # 重新繪製該 symbol 的 Canvas
473:             if symbol in self.labels:
474:                 _, _, canvas, _ = self.labels[symbol]
475:                 if hasattr(canvas, "last_draw_values") and canvas.last_draw_values:
476:                     prev, curr, high, low = canvas.last_draw_values
477:                     self._draw_status_bar(canvas, prev, curr, high, low, symbol)
478: 
479:     def _show_temp_val(self, canvas, text, x):
480:         self._hide_temp_val(canvas) # 先清除舊的
481:         
482:         # 顯示數值，座標上移一點預留間距
483:         canvas.create_text(x, 6, text=text, fill=StockStyle.TEXT_POPUP, font=StockStyle.FONT_BOLD, tags="temp_val")
484:         
485:         # 設定自動消失計時器
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.
