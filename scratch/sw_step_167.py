Created At: 2026-05-22T03:21:59Z
Completed At: 2026-05-22T03:22:00Z
File Path: `file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/stock_widget.py`
Total Lines: 730
Total Bytes: 34948
Showing lines 450 to 470
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
450:                 p_up = float(e_target_up_p.get())
451:                 pct_up = (p_up - ref) / ref * 100 if ref > 0 else 0
452:                 e_target_up_pct.delete(0, tk.END); e_target_up_pct.insert(0, f"{pct_up:.2f}")
453:             except: pass
454:             try:
455:                 ref = float(e_ref.get())
456:                 p_down = float(e_target_down_p.get())
457:                 pct_down = (ref - p_down) / ref * 100 if ref > 0 else 0
458:                 e_target_down_pct.delete(0, tk.END); e_target_down_pct.insert(0, f"{pct_down:.2f}")
459:             except: pass
460: 
461:         def sync_pct_to_p(ev=None):
462:             try:
463:                 ref = float(e_ref.get())
464:                 pct_up = float(e_target_up_pct.get())
465:                 p_up = ref * (1 + pct_up / 100.0)
466:                 e_target_up_p.delete(0, tk.END); e_target_up_p.insert(0, f"{p_up:.2f}")
467:             except: pass
468:             try:
469:                 ref = float(e_ref.get())
470:                 pct_down = float(e_target_down_pct.get())
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.
