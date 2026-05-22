Created At: 2026-05-22T03:22:04Z
Completed At: 2026-05-22T03:22:04Z
File Path: `file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/stock_widget.py`
Total Lines: 730
Total Bytes: 34948
Showing lines 501 to 530
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
501:                 
502:                 if self.data_manager.save_stock_params(symbol, params):
503:                     self._build_ui(); self.refresh_prices(); dialog.destroy()
504:             except ValueError as ve:
505:                 messagebox.showerror("錯誤", f"請檢查欄位格式: {ve}")
506:             except Exception as e:
507:                 messagebox.showerror("錯誤", f"儲存失敗: {e}")
508: 
509:         btn_fm = tk.Frame(dialog); btn_fm.pack(pady=10)
510:         tk.Button(btn_fm, text="儲存", command=save, width=8).pack(side=tk.LEFT, padx=5)
511:         tk.Button(btn_fm, text="取消", command=dialog.destroy, width=8).pack(side=tk.LEFT, padx=5)
512: 
513:     def _show_analysis_dialog(self, event, symbol):
514:         # 實現 Toggle 邏輯：按第二次就收回
515:         trigger_id = f"ANALYSIS_{symbol}"
516:         if self.active_dialog and self.active_dialog.winfo_exists():
517:             is_same = (self.active_trigger == trigger_id)
518:             self.active_dialog.destroy()
519:             self.active_dialog = None
520:             self.active_trigger = None
521:             if is_same: return
522: 
523:         dialog = tk.Toplevel(self)
524:         self.active_dialog = dialog
525:         self.active_trigger = trigger_id
526:         
527:         display_sym = symbol.split('_')[-1]
528:         dialog.title(f"數據分析報告: {display_sym}")
529:         
530:         # 置中於螢幕
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.
