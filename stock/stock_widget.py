import tkinter as tk
import urllib.request
import json
import threading
import os

CONFIG_FILE = "stock_config.json"

class HiddenStockWidget(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, cursor="hand2")
        self.parent = parent
        
        self.labels = {}
        self._update_job = None
        self.is_collapsed = False
        
        self.config_data = self._load_config()
        # 更新間隔改為「秒」，預設為 30 秒
        self.update_interval_ms = self.config_data.get("update_interval_seconds", 30) * 1000
        
        self._build_ui()
        self.update_prices()
        
    def _load_config(self):
        import sys
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
            
        try:
            config_path = os.path.join(base_path, CONFIG_FILE)
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {
                "update_interval_seconds": 60,
                "stocks": [
                    {"symbol": "tse_0050", "reference": 190.0},
                    {"symbol": "tse_2330", "reference": 800.0}
                ]
            }

    def toggle_collapse(self, event=None):
        self.is_collapsed = not self.is_collapsed
        self._build_ui()
        if not self.is_collapsed:
            self.update_prices()

    def _build_ui(self):
        for widget in self.winfo_children():
            widget.destroy()
            
        self.labels.clear()
        
        bg_col = self.master.cget("bg")
        self.config(bg=bg_col)
        
        if self.is_collapsed:
            expand_lbl = tk.Label(self, text="·", font=("Arial", 10, "bold"), fg="#b0b0b0", bg=bg_col, cursor="hand2")
            expand_lbl.grid(row=0, column=0, padx=5, pady=2, sticky="e")
            expand_lbl.bind("<Button-1>", self.toggle_collapse)
            return

        stocks = self.config_data.get("stocks", [])
        
        for i, stock in enumerate(stocks):
            row_idx = i
            symbol = stock.get("symbol", "")
            reference = stock.get("reference", "-")
            # 顯示時只保留數字代號 (e.g., tse_0050 -> 0050)
            display_sym = symbol.split('_')[-1]
            
            sym_lbl = tk.Label(self, text=display_sym, font=("Arial", 9), fg="#b0b0b0", bg=bg_col)
            sym_lbl.grid(row=row_idx, column=0, padx=2, pady=2, sticky="e")
            
            ref_lbl = tk.Label(self, text=str(reference), font=("Arial", 9), fg="#b0b0b0", bg=bg_col)
            ref_lbl.grid(row=row_idx, column=1, padx=4, sticky="e")
            
            prev_lbl = tk.Label(self, text="-", font=("Arial", 9), fg="#b0b0b0", bg=bg_col)
            prev_lbl.grid(row=row_idx, column=2, padx=4, sticky="e")
            
            curr_lbl = tk.Label(self, text="-", font=("Arial", 9), fg="#b0b0b0", bg=bg_col)
            curr_lbl.grid(row=row_idx, column=3, padx=4, sticky="e")
            
            bar_canvas = tk.Canvas(self, width=60, height=20, bg=bg_col, highlightthickness=0)
            bar_canvas.grid(row=row_idx, column=4, padx=5, sticky="w")
            
            hl_text_lbl = tk.Label(self, text="", font=("Arial", 7), fg="#b0b0b0", bg=bg_col, justify="left")
            hl_text_lbl.grid(row=row_idx, column=5, padx=2, sticky="w")
            
            self.labels[symbol] = (prev_lbl, curr_lbl, bar_canvas, hl_text_lbl)
            
            for w in (sym_lbl, ref_lbl, prev_lbl, curr_lbl, bar_canvas, hl_text_lbl):
                w.bind("<Button-1>", self.manual_update)

        btn_row = len(stocks)
        
        collapse_lbl = tk.Label(self, text="×", font=("Arial", 9), fg="#b0b0b0", bg=bg_col, cursor="hand2")
        collapse_lbl.grid(row=btn_row, column=4, padx=5, pady=2, sticky="e")
        collapse_lbl.bind("<Button-1>", self.toggle_collapse)
        
        refresh_lbl = tk.Label(self, text="↻", font=("Arial", 9), fg="#b0b0b0", bg=bg_col, cursor="hand2")
        refresh_lbl.grid(row=btn_row, column=5, padx=5, pady=2, sticky="w")
        refresh_lbl.bind("<Button-1>", self.manual_update)
        
        self.bind("<Button-1>", self.manual_update)

    def manual_update(self, event=None):
        new_config = self._load_config()
        if new_config != self.config_data:
            self.config_data = new_config
            self.update_interval_ms = self.config_data.get("update_interval_seconds", 30) * 1000
            self._build_ui()
            
        for prev_lbl, curr_lbl, bar_canvas, hl_text_lbl in self.labels.values():
            if curr_lbl.winfo_exists():
                curr_lbl.config(text="...")
                bar_canvas.delete("all")
            
        self.update_prices()
        
    def update_prices(self):
        if self._update_job is not None:
            self.after_cancel(self._update_job)
            self._update_job = None
            
        threading.Thread(target=self._fetch_data, daemon=True).start()
        
    def _fetch_data(self):
        updates = {}
        stocks = self.config_data.get("stocks", [])
        if not stocks: return
        import time

        # 直接使用 config 裡的代碼 (tse_0050 等)
        query_parts = []
        symbol_map = {} 
        for stock in stocks:
            s_key = stock.get("symbol", "")
            if not s_key: continue
            
            # 向 TWSE API 請求時需加上 .tw (tse_0050.tw)
            twse_code = f"{s_key}.tw"
            query_parts.append(twse_code)
            
            # 建立代碼與 key 的映射 (0050 -> tse_0050)
            code_only = s_key.split('_')[-1]
            symbol_map[code_only] = s_key

        if not query_parts: return

        try:
            ts = int(time.time() * 1000)
            url = f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={'|'.join(query_parts)}&json=1&delay=0&_={ts}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            
            with urllib.request.urlopen(req, timeout=5) as res:
                data = json.loads(res.read())
                if 'msgArray' in data:
                    for item in data['msgArray']:
                        code = item.get('c')
                        config_symbol = symbol_map.get(code)
                        if not config_symbol: continue
                        
                        curr_str = item.get('z', '-')
                        if curr_str == '-': curr_str = item.get('b', '-').split('_')[0]
                        if curr_str == '-': curr_str = item.get('y', '0')
                        
                        try:
                            curr_price = float(curr_str)
                            prev_close = float(item.get('y', curr_price))
                            day_high = float(item.get('h', curr_price))
                            day_low = float(item.get('l', curr_price))
                            
                            hint = 2
                            if "." in curr_str and len(curr_str.split(".")[1]) > 2:
                                hint = 4
                                
                            updates[config_symbol] = (prev_close, curr_price, day_high, day_low, hint)
                        except:
                            continue
        except Exception:
            pass
                
        self.after(0, lambda: self._apply_updates(updates))
        
    def _apply_updates(self, updates):
        if self.is_collapsed or not self.labels:
            pass
        elif updates:
            bg_col = self.master.cget("bg")
            for symbol, (prev_val, curr_val, high_val, low_val, hint) in updates.items():
                if symbol in self.labels:
                    prev_lbl, curr_lbl, bar_canvas, hl_text_lbl = self.labels[symbol]
                    if not curr_lbl.winfo_exists(): continue
                    
                    if prev_val == "ERR":
                        prev_lbl.config(text="N/A")
                        curr_lbl.config(text="N/A")
                        hl_text_lbl.config(text="")
                        bar_canvas.delete("all")
                    else:
                        fmt = "{:.2f}"
                        prev_lbl.config(text=fmt.format(prev_val))
                        
                        # 恢復極簡的灰色顏色設定
                        color = "#b0b0b0"
                        bg_line_color = "#e0e0e0"
                        cur_line_color = "#c0c0c0"
                        
                        curr_lbl.config(text=fmt.format(curr_val), fg=color)
                        
                        # 計算漲跌幅 %
                        diff_pct = 0.0
                        if prev_val > 0:
                            diff_pct = (curr_val - prev_val) / prev_val * 100.0
                            
                        # 顯示漲跌幅
                        hl_text_lbl.config(text=f"{diff_pct:+.2f}%", fg=color)
                        
                        if high_val and low_val:
                            bar_canvas.delete("all")
                            w = int(bar_canvas.cget("width"))
                            h = int(bar_canvas.cget("height"))
                            
                            # 計算今日震幅比例
                            range_val = high_val - low_val
                            range_pct = (range_val / prev_val * 100.0) if prev_val > 0 else 0
                            
                            # 非線性縮放：5% 以上為 100% 寬度，以下依 0.7 次方縮減
                            scale_factor = min(1.0, (range_pct / 5.0) ** 0.7) if range_pct > 0 else 0.05
                            
                            # 計算動態繪圖區域 (置中)
                            usable_w = (w - 10) * scale_factor
                            if usable_w < 4: usable_w = 4
                            start_x = (w - usable_w) / 2
                            
                            def get_x(v):
                                # 若數值在當前高低範圍內，映射到 start_x ~ start_x + usable_w
                                # 若昨收(v)在範圍外，它會被正確推向兩邊
                                if high_val > low_val:
                                    return start_x + (v - low_val) / (high_val - low_val) * usable_w
                                else:
                                    return w // 2
                                
                            x_low = get_x(low_val)
                            x_high = get_x(high_val)
                            x_prev = get_x(prev_val)
                            x_curr = get_x(curr_val)
                            
                            # 繪製灰色背景軌道線 (今日震幅區間)
                            bar_canvas.create_line(x_low, h//2, x_high, h//2, fill=bg_line_color, width=4, capstyle=tk.ROUND)
                            
                            # 繪製昨日收盤價的刻度線 (直線)
                            bar_canvas.create_line(x_prev, 3, x_prev, h-3, fill=cur_line_color, width=2)
                            
                            # 繪製代表現在價位的圖示
                            if curr_val > prev_val:
                                # 價格上漲 (大於昨日收盤)，三角形頭部指向遠離昨日價格 (向右)
                                bar_canvas.create_polygon(
                                    x_curr + 5, h//2, 
                                    x_curr - 4, h//2 - 5, 
                                    x_curr - 4, h//2 + 5, 
                                    fill="", outline=color, width=2
                                )
                            elif curr_val < prev_val:
                                # 價格下跌 (小於昨日收盤)，三角形頭部指向遠離昨日價格 (向左)
                                bar_canvas.create_polygon(
                                    x_curr - 5, h//2, 
                                    x_curr + 4, h//2 - 5, 
                                    x_curr + 4, h//2 + 5, 
                                    fill="", outline=color, width=2
                                )
                            else:
                                # 價格持平，空心圓球
                                bar_canvas.create_oval(x_curr-4, h//2-4, x_curr+4, h//2+4, fill="", outline=color, width=2)
                            
                        else:
                            bar_canvas.delete("all")
                    
        if self.update_interval_ms > 0:
            self._update_job = self.after(self.update_interval_ms, self.update_prices)
