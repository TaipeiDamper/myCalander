Created At: 2026-05-22T03:35:04Z
Completed At: 2026-05-22T03:35:04Z
File Path: `file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/stock_widget.py`
Total Lines: 683
Total Bytes: 32381
Showing lines 1 to 683
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
<truncated 32153 bytes>
        e_l = tk.Entry(fm, width=8); e_l.insert(0, str(cfg.get('alert_threshold_long', 15.0))); e_l.grid(row=1, column=1)
649:         
650:         tk.Label(fm, text="顏色強度(0-2):").grid(row=2, column=0, sticky="e", pady=2)
651:         e_i = tk.Entry(fm, width=8); e_i.insert(0, str(cfg.get('color_intensity', 1.0))); e_i.grid(row=2, column=1)
652: 
653:         def save():
654:             try:
655:                 new_cfg = {
656:                     "alert_threshold_short": float(e_s.get()),
657:                     "alert_threshold_long": float(e_l.get()),
658:                     "color_intensity": float(e_i.get())
659:                 }
660:                 if self.data_manager.update_global_config(new_cfg):
661:                     self._build_ui(); self.refresh_prices(); dialog.destroy()
662:             except: messagebox.showerror("錯誤", "請輸入有效數字")
663: 
664:         btn_fm = tk.Frame(dialog); btn_fm.pack(pady=15)
665:         tk.Button(btn_fm, text="儲存", command=save, width=10).pack(side=tk.LEFT, padx=5)
666: 
667:         # --- 新增：程式位置展示區 ---
668:         tk.Label(dialog, text="---------------------------", fg="#ccc").pack()
669:         tk.Label(dialog, text="程式位置 (可找到設定檔):", font=("Arial", 8, "italic"), fg="#888888").pack()
670:         
671:         app_path = os.path.dirname(os.path.abspath(self.data_manager.config_path))
672:         path_lbl = tk.Label(dialog, text=app_path, font=("Arial", 7), fg="#999999", wraplength=220, justify="center")
673:         path_lbl.pack(padx=10)
674:         
675:         def open_folder():
676:             try:
677:                 os.startfile(app_path)
678:             except:
679:                 pass
680:                 
681:         tk.Button(dialog, text="📁 開啟程式資料夾", font=("Arial", 8), command=open_folder, 
682:                   relief=tk.FLAT, fg="#6666ff", cursor="hand2").pack(pady=5)
683: 
The above content shows the entire, complete file contents of the requested file.
