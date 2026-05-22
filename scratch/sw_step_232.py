Created At: 2026-05-22T03:30:32Z
Completed At: 2026-05-22T03:30:32Z
File Path: `file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/stock_widget.py`
Total Lines: 542
Total Bytes: 24894
Showing lines 250 to 279
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
250:             if w > 1:
251:                 self.canvas.itemconfig(self.canvas_window, width=w)
252: 
253:         # 哪怕 fetch 失敗或是處於縮小狀態，也要排程下一次更新，否則功能會「失去」
254:         if result and not self.is_collapsed:
255:             updates = result.get("updates", {})
256:             alerts = result.get("alerts", [])
257:             
258:             for sym, data in updates.items():
259:                 if sym not in self.labels: continue
260:                 # 注意：data 格式為 (prev, curr, high, low, hint)
261:                 prev, curr, high, low, hint = data
262:                 lbl_prev, lbl_curr, canvas, lbl_diff = self.labels[sym]
263:                 if not lbl_curr.winfo_exists(): continue
264: 
265:                 # 更新文字
266:                 lbl_prev.config(text=f"{prev:.2f}")
267:                 lbl_curr.config(text=f"{curr:.{hint}f}")
268:                 diff_pct = (curr - prev) / prev * 100 if prev > 0 else 0
269:                 lbl_diff.config(text=f"{diff_pct:+.2f}%")
270: 
271:                 # 繪製圖形
272:                 self._draw_status_bar(canvas, prev, curr, high, low)
273:             
274:             # 處理警報
275:             if self.on_alert is not None:
276:                 self.on_alert(alerts)
277: 
278:         # 循環更新排程 (確保永遠持續)
279:         if self._update_job:
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.
