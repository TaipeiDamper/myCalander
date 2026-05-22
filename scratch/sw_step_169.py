Created At: 2026-05-22T03:22:02Z
Completed At: 2026-05-22T03:22:02Z
File Path: `file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/stock_widget.py`
Total Lines: 730
Total Bytes: 34948
Showing lines 470 to 500
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
470:                 pct_down = float(e_target_down_pct.get())
471:                 p_down = ref * (1 - pct_down / 100.0)
472:                 e_target_down_p.delete(0, tk.END); e_target_down_p.insert(0, f"{p_down:.2f}")
473:             except: pass
474: 
475:         e_target_up_p.bind("<KeyRelease>", sync_p_to_pct)
476:         e_target_down_p.bind("<KeyRelease>", sync_p_to_pct)
477:         e_target_up_pct.bind("<KeyRelease>", sync_pct_to_p)
478:         e_target_down_pct.bind("<KeyRelease>", sync_pct_to_p)
479: 
480:         def save():
481:             try:
482:                 ref_val = float(e_ref.get())
483:                 ma20_val = float(e_ma20.get()) if e_ma20.get().strip() else None
484:                 low20_val = float(e_low20.get()) if e_low20.get().strip() else None
485:                 
486:                 nav_val = None
487:                 if type_var.get() == "etf":
488:                     if e_nav.get().strip():
489:                         nav_val = float(e_nav.get())
490:                 
491:                 params = {
492:                     "type": type_var.get(),
493:                     "reference": ref_val,
494:                     "alert_short": float(e_short.get()) if e_short.get().strip() else 5.0,
495:                     "alert_long_up": float(e_target_up_pct.get()) if e_target_up_pct.get().strip() else 15.0,
496:                     "alert_long_down": float(e_target_down_pct.get()) if e_target_down_pct.get().strip() else 15.0,
497:                     "ma20": ma20_val,
498:                     "low20": low20_val,
499:                     "nav": nav_val
500:                 }
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.
