Created At: 2026-05-22T03:21:57Z
Completed At: 2026-05-22T03:21:57Z
File Path: `file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/stock_widget.py`
Total Lines: 730
Total Bytes: 34948
Showing lines 630 to 730
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
630:         prices_fm.columnconfigure(3, weight=1)
631:         
632:         # 標題
633:         tk.Label(prices_fm, text="參考基準", font=StockStyle.FONT_SMALL, fg="#777").grid(row=0, column=0, pady=2)
634:         tk.Label(prices_fm, text="觀察價", font=StockStyle.FONT_SMALL, fg="#777").grid(row=0, column=1, pady=2)
635:         tk.Label(prices_fm, text="買進價", font=StockStyle.FONT_SMALL, fg="#777").grid(row=0, column=2, pady=2)
636:         tk.Label(prices_fm, text="強烈買進", font=StockStyle.FONT_SMALL, fg="#777").grid(row=0, column=3, pady=2)
637:         
638:         # 數值
639:         tk.Label(prices_fm, text=f"{computed['referencePrice']:.2f}", font=StockStyle.FONT_BOLD).grid(row=1, column=0, pady=2)
640:         tk.Label(prices_fm, text=f"{computed['watchPrice']:.2f}", font=StockStyle.FONT_BOLD, fg="#856404").grid(row=1, column=1, pady=2)
641:         tk.Label(prices_fm, text=f"{computed['buyPrice']:.2f}", font=StockStyle.FONT_BOLD, fg="#2e7d32").grid(row=1, column=2, pady=2)
642:         tk.Label(prices_fm, text=f"{computed['strongBuyPrice']:.2f}", font=StockStyle.FONT_BOLD, fg="#155724").grid(row=1, column=3, pady=2)
643:         
644:         # 計算類型說明
645:         ref_type_map = {
646:             "hybrid_stock": "計算公式: min(MA20, Low20 * 1.02)",
647:             "hybrid_etf": "計算公式: min(MA20, NAV * 0.995)",
648:             "fallback_etf_ma20": "備用公式: 直接使用 MA20 (無 NAV 淨值)"
649:         }
650:         ref_desc = ref_type_map.get(computed["referenceType"], "")
<truncated 2016 bytes>
(row=1, column=1)
696:         
697:         tk.Label(fm, text="顏色強度(0-2):").grid(row=2, column=0, sticky="e", pady=2)
698:         e_i = tk.Entry(fm, width=8); e_i.insert(0, str(cfg.get('color_intensity', 1.0))); e_i.grid(row=2, column=1)
699: 
700:         def save():
701:             try:
702:                 new_cfg = {
703:                     "alert_threshold_short": float(e_s.get()),
704:                     "alert_threshold_long": float(e_l.get()),
705:                     "color_intensity": float(e_i.get())
706:                 }
707:                 if self.data_manager.update_global_config(new_cfg):
708:                     self._build_ui(); self.refresh_prices(); dialog.destroy()
709:             except: messagebox.showerror("錯誤", "請輸入有效數字")
710: 
711:         btn_fm = tk.Frame(dialog); btn_fm.pack(pady=15)
712:         tk.Button(btn_fm, text="儲存", command=save, width=10).pack(side=tk.LEFT, padx=5)
713: 
714:         # --- 新增：程式位置展示區 ---
715:         tk.Label(dialog, text="---------------------------", fg="#ccc").pack()
716:         tk.Label(dialog, text="程式位置 (可找到設定檔):", font=("Arial", 8, "italic"), fg="#888888").pack()
717:         
718:         app_path = os.path.dirname(os.path.abspath(self.data_manager.config_path))
719:         path_lbl = tk.Label(dialog, text=app_path, font=("Arial", 7), fg="#999999", wraplength=220, justify="center")
720:         path_lbl.pack(padx=10)
721:         
722:         def open_folder():
723:             try:
724:                 os.startfile(app_path)
725:             except:
726:                 pass
727:                 
728:         tk.Button(dialog, text="📁 開啟程式資料夾", font=("Arial", 8), command=open_folder, 
729:                   relief=tk.FLAT, fg="#6666ff", cursor="hand2").pack(pady=5)
730: 
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.
