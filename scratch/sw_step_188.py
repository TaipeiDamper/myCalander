Created At: 2026-05-22T03:23:15Z
Completed At: 2026-05-22T03:23:15Z
File Path: `file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/stock_widget.py`
Total Lines: 651
Total Bytes: 30555
Showing lines 1 to 651
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
31:         self.expanded_bars = set() # 記錄哪些 symbol 展開了詳細分析 bar
32: 
33:         
34:         # 初始化數據管理器
35:         self.data_manager = StockDataManager(self._get_config_path())
36:         self.update_interval_ms = self.data_manager.config_data.get("update_interval_seconds", 30) * 1000
37:         
38:         # 綁定全域滾輪事件 (僅綁定一次)
39:         self.bind_all("<MouseWheel>", self._on_mousew
<truncated 30167 bytes>
        e_l = tk.Entry(fm, width=8); e_l.insert(0, str(cfg.get('alert_threshold_long', 15.0))); e_l.grid(row=1, column=1)
617:         
618:         tk.Label(fm, text="顏色強度(0-2):").grid(row=2, column=0, sticky="e", pady=2)
619:         e_i = tk.Entry(fm, width=8); e_i.insert(0, str(cfg.get('color_intensity', 1.0))); e_i.grid(row=2, column=1)
620: 
621:         def save():
622:             try:
623:                 new_cfg = {
624:                     "alert_threshold_short": float(e_s.get()),
625:                     "alert_threshold_long": float(e_l.get()),
626:                     "color_intensity": float(e_i.get())
627:                 }
628:                 if self.data_manager.update_global_config(new_cfg):
629:                     self._build_ui(); self.refresh_prices(); dialog.destroy()
630:             except: messagebox.showerror("錯誤", "請輸入有效數字")
631: 
632:         btn_fm = tk.Frame(dialog); btn_fm.pack(pady=15)
633:         tk.Button(btn_fm, text="儲存", command=save, width=10).pack(side=tk.LEFT, padx=5)
634: 
635:         # --- 新增：程式位置展示區 ---
636:         tk.Label(dialog, text="---------------------------", fg="#ccc").pack()
637:         tk.Label(dialog, text="程式位置 (可找到設定檔):", font=("Arial", 8, "italic"), fg="#888888").pack()
638:         
639:         app_path = os.path.dirname(os.path.abspath(self.data_manager.config_path))
640:         path_lbl = tk.Label(dialog, text=app_path, font=("Arial", 7), fg="#999999", wraplength=220, justify="center")
641:         path_lbl.pack(padx=10)
642:         
643:         def open_folder():
644:             try:
645:                 os.startfile(app_path)
646:             except:
647:                 pass
648:                 
649:         tk.Button(dialog, text="📁 開啟程式資料夾", font=("Arial", 8), command=open_folder, 
650:                   relief=tk.FLAT, fg="#6666ff", cursor="hand2").pack(pady=5)
651: 
The above content shows the entire, complete file contents of the requested file.
