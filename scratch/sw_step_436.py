Created At: 2026-05-22T03:55:28Z
Completed At: 2026-05-22T03:55:28Z
File Path: `file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/stock_widget.py`
Total Lines: 717
Total Bytes: 34216
Showing lines 250 to 285
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
250:             
251:         # 3. 初始狀態回饋
252:         for sym in self.labels:
253:             _, lbl_curr, canvas, _ = self.labels[sym]
254:             if lbl_curr.winfo_exists():
255:                 lbl_curr.config(text="..." )
256:                 canvas.delete("all")
257:         
258:         # 4. 執行數據更新
259:         self.refresh_prices()
260:         return "break"
261: 
262:     def refresh_prices(self):
263:         if not self.winfo_exists(): return
264:         if self._update_job: 
265:             self.after_cancel(self._update_job)
266:             self._update_job = None
267:         
268:         # 更新畫布內的 window 寬度 (增加 winfo_width > 1 判斷)
269:         if hasattr(self, "canvas") and self.canvas.winfo_exists() and hasattr(self, "scroll_frame") and self.scroll_frame.winfo_exists():
270:             w = self.canvas.winfo_width()
271:             if w > 1:
272:                 self.canvas.itemconfig(self.canvas_window, width=w)
273:             
274:         self.data_manager.fetch_prices(self._on_fetch_done)
275: 
276:     def _on_fetch_done(self, result):
277:         # 切換到主執行緒執行 UI 更新
278:         self.after(0, lambda: self._do_apply_updates(result))
279: 
280:     def _do_apply_updates(self, result):
281:         if not self.winfo_exists(): return
282:         
283:         # 二次嘗試校正寬度，確保數據填入時布局是正確的
284:         if hasattr(self, "canvas") and self.canvas.winfo_exists():
285:             w = self.canvas.winfo_width()
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.
