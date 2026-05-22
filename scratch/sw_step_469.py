Created At: 2026-05-22T04:27:00Z
Completed At: 2026-05-22T04:27:00Z
File Path: `file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/stock_widget.py`
Total Lines: 813
Total Bytes: 38328
Showing lines 1 to 800
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
32:         self.detail_frames = {}    # 紀錄各股票的詳細資料 Frame
33:         self.detail_labels = {}    # 紀錄各股票下方詳細指標的 Label 參照
34: 
35: 
36:         
37:         # 初始化數據管理器
38:         self.data_manager = StockDataManager(self._get_config_path())
39:         self.update_interval_ms = self.data_manager.config_
<truncated 38229 bytes>
設參數", font=StockStyle.FONT_BOLD).pack(pady=10)
770:         
771:         fm = tk.Frame(dialog); fm.pack(padx=20)
772:         cfg = self.data_manager.config_data
773:         
774:         tk.Label(fm, text="預設短預警(%):").grid(row=0, column=0, sticky="e", pady=2)
775:         e_s = tk.Entry(fm, width=8); e_s.insert(0, str(cfg.get('alert_threshold_short', 5.0))); e_s.grid(row=0, column=1)
776:         
777:         tk.Label(fm, text="預設長預警(%):").grid(row=1, column=0, sticky="e", pady=2)
778:         e_l = tk.Entry(fm, width=8); e_l.insert(0, str(cfg.get('alert_threshold_long', 15.0))); e_l.grid(row=1, column=1)
779:         
780:         tk.Label(fm, text="顏色強度(0-2):").grid(row=2, column=0, sticky="e", pady=2)
781:         e_i = tk.Entry(fm, width=8); e_i.insert(0, str(cfg.get('color_intensity', 1.0))); e_i.grid(row=2, column=1)
782: 
783:         def save():
784:             try:
785:                 new_cfg = {
786:                     "alert_threshold_short": float(e_s.get()),
787:                     "alert_threshold_long": float(e_l.get()),
788:                     "color_intensity": float(e_i.get())
789:                 }
790:                 if self.data_manager.update_global_config(new_cfg):
791:                     self._build_ui(); self.refresh_prices(); dialog.destroy()
792:             except: messagebox.showerror("錯誤", "請輸入有效數字")
793: 
794:         btn_fm = tk.Frame(dialog); btn_fm.pack(pady=15)
795:         tk.Button(btn_fm, text="儲存", command=save, width=10).pack(side=tk.LEFT, padx=5)
796: 
797:         # --- 新增：程式位置展示區 ---
798:         tk.Label(dialog, text="---------------------------", fg="#ccc").pack()
799:         tk.Label(dialog, text="程式位置 (可找到設定檔):", font=("Arial", 8, "italic"), fg="#888888").pack()
800:         
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.
