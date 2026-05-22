Created At: 2026-05-22T03:55:32Z
Completed At: 2026-05-22T03:55:32Z
File Path: `file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/stock_widget.py`
Total Lines: 717
Total Bytes: 34216
Showing lines 286 to 320
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
286:             if w > 1:
287:                 self.canvas.itemconfig(self.canvas_window, width=w)
288: 
289:         # 哪怕 fetch 失敗或是處於縮小狀態，也要排程下一次更新，否則功能會「失去」
290:         if result and not self.is_collapsed:
291:             updates = result.get("updates", {})
292:             alerts = result.get("alerts", [])
293:             
294:             for sym, data in updates.items():
295:                 if sym not in self.labels: continue
296:                 # 注意：data 格式為 (prev, curr, high, low, hint)
297:                 prev, curr, high, low, hint = data
298:                 lbl_prev, lbl_curr, canvas, lbl_diff = self.labels[sym]
299:                 if not lbl_curr.winfo_exists(): continue
300: 
301:                 # 更新文字
302:                 lbl_prev.config(text=f"{prev:.2f}")
303:                 lbl_curr.config(text=f"{curr:.{hint}f}")
304:                 diff_pct = (curr - prev) / prev * 100 if prev > 0 else 0
305:                 lbl_diff.config(text=f"{diff_pct:+.2f}%")
306: 
307:                 # 繪製圖形
308:                 self._draw_status_bar(canvas, prev, curr, high, low, sym)
309:             
310:             # 處理警報
311:             if self.on_alert is not None:
312:                 self.on_alert(alerts)
313: 
314:         # 循環更新排程 (確保永遠持續)
315:         if self._update_job:
316:             self.after_cancel(self._update_job)
317:         self._update_job = self.after(self.update_interval_ms, self.refresh_prices)
318: 
319:     def _draw_status_bar(self, canvas, prev, curr, high, low, symbol):
320:         canvas.delete("all")
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.
