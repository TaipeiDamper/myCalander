Created At: 2026-05-22T03:31:06Z
Completed At: 2026-05-22T03:31:07Z
File Path: `file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/stock_widget.py`
Total Lines: 688
Total Bytes: 32709
Showing lines 20 to 50
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
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
31: 
32:         
33:         # 初始化數據管理器
34:         self.data_manager = StockDataManager(self._get_config_path())
35:         self.update_interval_ms = self.data_manager.config_data.get("update_interval_seconds", 30) * 1000
36:         
37:         # 綁定全域滾輪事件 (僅綁定一次)
38:         self.bind_all("<MouseWheel>", self._on_mousewheel)
39:         
40:         self._build_ui()
41:         # 強制刷新 UI 佈局後再啟動數據更新，確保第一次加載就能正常秀位
42:         self.update()
43:         self.after(500, self.refresh_prices)
44:         
45:     def _get_config_path(self):
46:         import sys
47:         base = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
48:         return os.path.join(base, CONFIG_FILE)
49: 
50:     def toggle_collapse(self, event=None):
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.
