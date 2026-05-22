Created At: 2026-05-22T03:30:19Z
Completed At: 2026-05-22T03:30:19Z
File Path: `file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/stock_widget.py`
Total Lines: 539
Total Bytes: 24542
Showing lines 140 to 165
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
140:             sym_lbl.bind("<Enter>", lambda e, w=sym_lbl: (on_enter(e), w.config(fg=StockStyle.HOVER_GREY)))
141:             sym_lbl.bind("<Leave>", lambda e, w=sym_lbl: (on_leave(e), w.config(fg=StockStyle.PRIMARY_GREY)))
142:             
143:             ref_lbl = tk.Label(row_fm, text=str(ref), font=StockStyle.FONT_MAIN, fg=StockStyle.PRIMARY_GREY, bg=bg, width=6, anchor="e")
144:             ref_lbl.grid(row=0, column=1, padx=4)
145: 
146:             prev_lbl = tk.Label(row_fm, text="-", font=StockStyle.FONT_MAIN, fg=StockStyle.PRIMARY_GREY, bg=bg, width=6, anchor="e")
147:             prev_lbl.grid(row=0, column=2, padx=4)
148:             
149:             curr_lbl = tk.Label(row_fm, text="-", font=StockStyle.FONT_MAIN, fg=StockStyle.PRIMARY_GREY, bg=bg, width=6, anchor="e")
150:             curr_lbl.grid(row=0, column=3, padx=4)
151:             
152:             canvas_bar = tk.Canvas(row_fm, width=80, height=24, bg=bg, highlightthickness=0, cursor="hand2")
153:             canvas_bar.grid(row=0, column=4, padx=5)
154:             canvas_bar.bind("<Button-1>", lambda e, c=canvas_bar: self._on_bar_click(e, c))
155:             canvas_bar.bind("<Leave>", lambda e, c=canvas_bar: self._hide_temp_val(c))
156:             
157:             diff_lbl = tk.Label(row_fm, text="", font=StockStyle.FONT_SMALL, fg=StockStyle.PRIMARY_GREY, bg=bg, width=7, anchor="w")
158:             diff_lbl.grid(row=0, column=5, padx=2)
159:             
160:             self.labels[symbol] = (prev_lbl, curr_lbl, canvas_bar, diff_lbl)
161: 
162:         # 2. 固定控制區 (放在 Grid 的下一列)
163:         ctrl_container = tk.Frame(self, bg=bg)
164:         ctrl_container.grid(row=1, column=0, sticky="ew")
165:         self._build_control_btns(ctrl_container, bg)
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.
