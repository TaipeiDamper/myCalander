Created At: 2026-05-22T03:56:35Z
Completed At: 2026-05-22T03:56:35Z
File Path: `file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/stock_widget.py`
Total Lines: 815
Total Bytes: 38469
Showing lines 580 to 630
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
580:         
581:         if symbol in self.detail_labels:
582:             # 先將該檔股票所有 detail label 恢復原色背景
583:             for k, lbl in self.detail_labels[symbol].items():
584:                 if lbl.winfo_exists():
585:                     lbl.config(bg=current_bg, fg=StockStyle.PRIMARY_GREY)
586:                     
587:             # 再亮起被選取的 key 對應項目
588:             if key in self.detail_labels[symbol]:
589:                 lbl = self.detail_labels[symbol][key]
590:                 if lbl.winfo_exists():
591:                     # 變深灰色背景，高亮選中狀態
592:                     lbl.config(bg="#e5e5e5", fg=StockStyle.TEXT_POPUP)
593: 
594:     def _clear_highlights(self, symbol):
595:         detail_fm = self.detail_frames.get(symbol)
596:         current_bg = detail_fm.cget("bg") if detail_fm else self.cget("bg")
597:         if symbol in self.detail_labels:
598:             for k, lbl in self.detail_labels[symbol].items():
599:                 if lbl.winfo_exists():
600:                     lbl.config(bg=current_bg, fg=StockStyle.PRIMARY_GREY)
601:                 prev, curr, high, low = canvas.last_draw_values
602:                 self._draw_status_bar(canvas, prev, curr, high, low, symbol)
603: 
604:     def _show_temp_val(self, canvas, text, x):
605:         self._hide_temp_val(canvas) # 先清除舊的
606:         
607:         # 顯示數值，座標上移一點預留間距
608:         canvas.create_text(x, 6, text=text, fill=StockStyle.TEXT_POPUP, font=StockStyle.FONT_BOLD, tags="temp_val")
609:         
610:         # 設定自動消失計時器
611:         timer_id = self.after(3000, lambda: self._hide_temp_val(canvas))
612:         canvas.hide_timer = timer_id
613: 
614:     def _hide_temp_val(self, canvas):
615:         """隱藏暫時顯示的數值並取消計時器"""
616:         canvas.delete("temp_val")
617:         if hasattr(canvas, "hide_timer") and canvas.hide_timer:
618:             self.after_cancel(canvas.hide_timer)
619:             canvas.hide_timer = None
620: 
621:     def _show_edit_dialog(self, event, symbol, current_ref, stock_cfg):
622:         # 實現 Toggle 邏輯：按第二次就收回
623:         if self.active_dialog and self.active_dialog.winfo_exists():
624:             is_same = (self.active_trigger == symbol)
625:             self.active_dialog.destroy()
626:             self.active_dialog = None
627:             self.active_trigger = None
628:             if is_same: return
629: 
630:         dialog = tk.Toplevel(self)
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.
