Created At: 2026-05-22T03:47:01Z
Completed At: 2026-05-22T03:47:01Z
File Path: `file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/stock_widget.py`
Total Lines: 683
Total Bytes: 32423
Showing lines 301 to 683
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
301:             v_low, v_high = min(low, prev), max(high, prev)
302:             v_range = v_high - v_low
303:             v_range_pct = (v_range / prev * 100.0) if prev > 0 else 0
304:             
305:             # 使用 scale 設計讓無波動時軌道縮短，有波動時拉長
306:             scale = min(1.0, (v_range_pct / 10.0) ** 0.7) if v_range_pct > 0 else 0.05
307:             uw = (w - 12) * scale
308:             if uw < 10: uw = 10
309:             start_x = (w - uw) / 2
310:             
311:             def get_x(v):
312:                 return start_x + (v - v_low) / (v_high - v_low) * uw if v_high > v_low else w / 2
313:                 
314:             xl, xh, xp, xc = get_x(low), get_x(high), get_x(prev), get_x(curr)
315:             
316:             # 記錄坐標以供點擊提示 (未展開時只有高、低、昨收、現價)
317:             canvas.stock_coords.append({'x': xl, 'val': low, 'lbl': '今日最低'})
318:             canvas.stock_coords.append({'x': xh, 'val': high, 'lbl': '今日最高'})
319:             canvas.stock_coords.append({'x': xp, 'val': prev, 'lbl': '昨日收盤'})
320:             canvas.stock_coords.append({'x': xc, 'val': curr, 'lbl': '現在價格'})
321:             
322:             # 繪製行情軌道 (BAR_TRACK)
323:             canvas.create_line(xl, y1, xh, y1, fill=StockStyle.BAR_TRACK, width=4, capstyle=tk.ROUND)
324:             for x in (xl, xh): 
325:                 canvas.create_oval(x-2, y1-2, x+2, y1+2, fill="#eeeeee", outline="")
326:             
327:            
<truncated 17472 bytes>
(row=1, column=1)
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
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.
