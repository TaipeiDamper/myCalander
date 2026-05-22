Created At: 2026-05-22T03:34:25Z
Completed At: 2026-05-22T03:34:25Z
File Path: `file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/stock_widget.py`
Total Lines: 690
Total Bytes: 32793
Showing lines 145 to 158
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
145:             ref_lbl = tk.Label(row_fm, text=str(ref), font=StockStyle.FONT_MAIN, fg=StockStyle.PRIMARY_GREY, bg=bg, width=6, anchor="e")
146:             ref_lbl.grid(row=0, column=1, padx=4)
147: 
148:             prev_lbl = tk.Label(row_fm, text="-", font=StockStyle.FONT_MAIN, fg=StockStyle.PRIMARY_GREY, bg=bg, width=6, anchor="e")
149:             prev_lbl.grid(row=0, column=2, padx=4)
150:             
151:             curr_lbl = tk.Label(row_fm, text="-", font=StockStyle.FONT_MAIN, fg=StockStyle.PRIMARY_GREY, bg=bg, width=6, anchor="e", cursor="hand2")
152:             curr_lbl.grid(row=0, column=3, padx=4)
153:             curr_lbl.bind("<Button-1>", lambda e, s=symbol: self._expand_bar(s))
154:             curr_lbl.bind("<Enter>", lambda e, w=curr_lbl: (on_enter(e), w.config(fg=StockStyle.HOVER_GREY)))
155:             curr_lbl.bind("<Leave>", lambda e, w=curr_lbl, s=symbol: (on_leave(e), w.config(fg=StockStyle.PRIMARY_GREY), self._collapse_bar(s)))
156:             
157:             canvas_bar = tk.Canvas(row_fm, width=80, height=24, bg=bg, highlightthickness=0, cursor="hand2")
158:             canvas_bar.grid(row=0, column=4, padx=5)
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.
