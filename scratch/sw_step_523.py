Created At: 2026-05-22T04:43:33Z
Completed At: 2026-05-22T04:43:33Z
File Path: `file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/stock_widget.py`
Total Lines: 833
Total Bytes: 39218
Showing lines 545 to 585
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
545:             stocks = self.data_manager.config_data.get("stocks", [])
546:             s_cfg = next((s for s in stocks if s.get("symbol") == symbol), None)
547:             if s_cfg:
548:                 lbl_prev, lbl_curr, canvas, _ = self.labels.get(symbol, (None, None, None, None))
549:                 curr_val = s_cfg.get("reference", 0.0)
550:                 if canvas and hasattr(canvas, "last_draw_values"):
551:                     curr_val = canvas.last_draw_values[1]
552:                 asset_data = {
553:                     "symbol": symbol.split('_')[-1],
554:                     "type": s_cfg.get("type", "stock"),
555:                     "lastPrice": curr_val,
556:                     "ma20": s_cfg.get("ma20"),
557:                     "low20": s_cfg.get("low20"),
558:                     "nav": s_cfg.get("nav")
559:                 }
560:                 computed = self.data_manager.compute_asset(asset_data)
561:                 
562:         if not computed: return
563:         
564:         # 簡寫對照表
565:         SHORT_NAMES = [
566:             ("ma20", "MA"),
567:             ("low20", "L20"),
568:             ("nav", "NAV"),
569:             ("watchPrice", "Watch"),
570:             ("buyPrice", "Buy"),
571:             ("strongBuyPrice", "SBuy")
572:         ]
573:         
574:         self.detail_labels[symbol] = {}
575:         
576:         # 動態生成項目 Label，有值才顯示
577:         for key, short in SHORT_NAMES:
578:             val = computed.get(key)
579:             if val is not None:
580:                 # 檢查是否需要預設高亮
581:                 is_highlighted = (self.highlighted_keys.get(symbol) == key)
582:                 lbl_bg = "#e5e5e5" if is_highlighted else bg
583:                 lbl_fg = StockStyle.TEXT_POPUP if is_highlighted else StockStyle.PRIMARY_GREY
584:                 
585:                 lbl = tk.Label(detail_fm, text=f"{short}: {val:.2f}", font=StockStyle.FONT_SMALL, fg=lbl_fg, bg=lbl_bg, padx=4, pady=1, cursor="hand2")
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.
