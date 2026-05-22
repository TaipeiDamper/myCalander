Created At: 2026-05-22T03:46:59Z
Completed At: 2026-05-22T03:46:59Z
File Path: `file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/stock_widget.py`
Total Lines: 683
Total Bytes: 32423
Showing lines 1 to 300
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
1: import tkinter as tk
2: from tkinter import messagebox
3: import os
4: from .data_manager import StockDataManager
5: 
6: CONFIG_FILE = "stock_config.json"
7: 
8: class StockStyle:
9:     """集中管理 UI 配色與樣式"""
10:     PRIMARY_GREY = "#c4c4c4"    # 調整至 0.4 位置，極致柔和
11:     HOVER_GREY = "#999999"      # 懸停時略微加深
12:     HOVER_BG = "#f8f8f8"
13:     BAR_TRACK = "#eeeeee"
14:     BAR_GUIDE = "#d0d0d0"
15:     TEXT_POPUP = "#444444"
16:     FONT_MAIN = ("Arial", 9)
17:     FONT_SMALL = ("Arial", 7)
18:     FONT_BOLD = ("Arial", 8, "bold")
19: 
20: class HiddenStockWidget(tk.Frame):
21:     def __init__(self, parent, on_notify_toggle=None, on_alert=None):
22:         super().__init__(parent, cursor="hand2")
23:         self.on_notify_toggle = on_notify_toggle
24:         self.on_alert = on_alert
25: 
26:         self.labels = {}
27:         self._update_job = None
28:         self.is_collapsed = False
29:         self.active_dialog = None  # 紀錄當前開啟的對話視窗
30:         self.active_trigger = None # 紀錄是誰觸發的 (代號或⚙️)
31:         self.expanded_bars = set() # 紀錄哪些 symbol 展開了詳細分析 bar
32: 
33: 
34:         
35:         # 初始化數據管理器
36:         self.data_manager = StockDataManager(self._get_config_path())
37:         self.update_interval_ms = self.data_manager.config_data.get("update_interval_seconds", 30) * 1000
38:         
39:         # 綁定全域滾輪事件 (僅綁定一次)
40:         self.bind_all("<MouseWheel>", self._on_m
<truncated 11397 bytes>
  if sym not in self.labels: continue
262:                 # 注意：data 格式為 (prev, curr, high, low, hint)
263:                 prev, curr, high, low, hint = data
264:                 lbl_prev, lbl_curr, canvas, lbl_diff = self.labels[sym]
265:                 if not lbl_curr.winfo_exists(): continue
266: 
267:                 # 更新文字
268:                 lbl_prev.config(text=f"{prev:.2f}")
269:                 lbl_curr.config(text=f"{curr:.{hint}f}")
270:                 diff_pct = (curr - prev) / prev * 100 if prev > 0 else 0
271:                 lbl_diff.config(text=f"{diff_pct:+.2f}%")
272: 
273:                 # 繪製圖形
274:                 self._draw_status_bar(canvas, prev, curr, high, low, sym)
275:             
276:             # 處理警報
277:             if self.on_alert is not None:
278:                 self.on_alert(alerts)
279: 
280:         # 循環更新排程 (確保永遠持續)
281:         if self._update_job:
282:             self.after_cancel(self._update_job)
283:         self._update_job = self.after(self.update_interval_ms, self.refresh_prices)
284: 
285:     def _draw_status_bar(self, canvas, prev, curr, high, low, symbol):
286:         canvas.delete("all")
287:         w, h = int(canvas.cget("width")), int(canvas.cget("height"))
288:         
289:         # 儲存最後繪製的價格值，以便在展開/收回時能直接從快取中重繪
290:         canvas.last_draw_values = (prev, curr, high, low)
291:         show_detail = (symbol in self.expanded_bars)
292:         
293:         # 水平中心線位置
294:         y1 = 12
295:         
296:         # 初始化坐標對照表，用於點擊 Canvas 互動
297:         canvas.stock_coords = []
298:         
299:         if not show_detail:
300:             # 1. 未展開模式：維持原本的今日波幅比例縮放軌道
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.
