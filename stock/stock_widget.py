import tkinter as tk
from tkinter import messagebox
import os
from .data_manager import StockDataManager

CONFIG_FILE = "stock_config.json"

class StockStyle:
    """集中管理 UI 配色與樣式"""
    PRIMARY_GREY = "#b0b0b0"    # 極致柔和灰白，不喧賓奪主
    HOVER_GREY = "#777777"      # 懸停時柔和加深
    HOVER_BG = "#f8f8f8"
    BAR_TRACK = "#d4d4d4"       # 統一柔和的灰白軌道，不顯眼
    BAR_GUIDE = "#c4c4c4"
    TEXT_POPUP = "#444444"
    FONT_MAIN = ("Arial", 9)
    FONT_SMALL = ("Arial", 7)
    FONT_BOLD = ("Arial", 8, "bold")
    TEXT_POPUP = "#444444"
    FONT_MAIN = ("Arial", 9)
    FONT_SMALL = ("Arial", 7)
    FONT_BOLD = ("Arial", 8, "bold")

class HiddenStockWidget(tk.Frame):
    def __init__(self, parent, on_notify_toggle=None, on_alert=None):
        super().__init__(parent, cursor="hand2")
        self.on_notify_toggle = on_notify_toggle
        self.on_alert = on_alert

        self.labels = {}
        self.detail_frames = {}
        self.detail_labels = {}
        self.highlighted_keys = {}
        self.expanded_symbols = set()
        self._update_job = None
        self.is_collapsed = False
        self.active_dialog = None  # 紀錄當前開啟的對話視窗
        self.active_trigger = None # 紀錄是誰觸發的 (代號或⚙️)

        
        # 初始化數據管理器
        self.data_manager = StockDataManager(self._get_config_path())
        self.update_interval_ms = self.data_manager.config_data.get("update_interval_seconds", 30) * 1000
        
        # 綁定全域滾輪事件 (僅綁定一次)
        self.bind_all("<MouseWheel>", self._on_mousewheel)
        
        self._build_ui()
        # 強制刷新 UI 佈局後再啟動數據更新，確保第一次加載就能正常秀位
        self.update()
        self.after(500, self.refresh_prices)
        
    def _get_config_path(self):
        import sys
        base = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base, CONFIG_FILE)

    def toggle_collapse(self, event=None):
        self.is_collapsed = not self.is_collapsed
        self._build_ui()
        if not self.is_collapsed:
            self.refresh_prices()

    def _get_category_key(self, symbol, asset_type):
        """依據標的代號與類型取得分群的 key"""
        code = symbol.split('_')[-1]
        
        # 1513, 1773, 6613 自己一區
        if code in ["1513", "1773", "6613"]:
            return "special"
            
        # 海運一區 (2603, 2609, 2615)
        if code in ["2603", "2609", "2615"]:
            return "shipping"
            
        # 黃金一區 (00635U)
        if code == "00635U":
            return "gold"
            
        # 646 移到其他股票區
        if code == "00646":
            return "others"
            
        # 0403 (00403A) 與 0981A 放到 ETF
        if code in ["00403A", "00981A"]:
            return "etf"
            
        # 美債一區 (以 B 結尾的債券 ETF，如 00679B, 00687B, 00719B)
        if code.endswith("B") or code in ["00679B", "00687B"]:
            return "bond"
            
        # ETF一區
        if asset_type == "etf" or code.startswith("00"):
            return "etf"
            
        # 剩下的股票一區
        return "others"

    def _get_dynamic_color(self, target_hex):
        cfg = self.data_manager.config_data
        intensity = cfg.get('color_intensity', 1.0)
        
        # 獲取實際背景的 RGB 值
        bg_color = self.master.cget("bg")
        try:
            bg_rgb = self.winfo_rgb(bg_color)
            bg_r, bg_g, bg_b = bg_rgb[0] // 256, bg_rgb[1] // 256, bg_rgb[2] // 256
        except:
            bg_r, bg_g, bg_b = 240, 240, 240 # 預設回退

        try:
            target_rgb = self.winfo_rgb(target_hex)
            tgt_r, tgt_g, tgt_b = target_rgb[0] // 256, target_rgb[1] // 256, target_rgb[2] // 256
        except:
            tgt_r, tgt_g, tgt_b = 168, 168, 168

        # 根據強度的兩個區間進行線性內插
        if intensity <= 1.0:
            r = int(bg_r + (tgt_r - bg_r) * intensity)
            g = int(bg_g + (tgt_g - bg_g) * intensity)
            b = int(bg_b + (tgt_b - bg_b) * intensity)
        else:
            # 2.0 代表完全的純黑 (0, 0, 0)
            black_r, black_g, black_b = 0, 0, 0
            factor = intensity - 1.0
            r = int(tgt_r + (black_r - tgt_r) * factor)
            g = int(tgt_g + (black_g - tgt_g) * factor)
            b = int(tgt_b + (black_b - tgt_b) * factor)

        r = min(255, max(0, r))
        g = min(255, max(0, g))
        b = min(255, max(0, b))
        return f"#{r:02x}{g:02x}{b:02x}"

    def _update_colors(self):
        # 根據儲存的強度重新計算全局色彩
        StockStyle.PRIMARY_GREY = self._get_dynamic_color("#a8a8a8")
        StockStyle.BAR_TRACK = self._get_dynamic_color("#e0e0e0")
        StockStyle.BAR_GUIDE = self._get_dynamic_color("#dcdcdc")

    def _build_ui(self):
        self._update_colors()
        for w in self.winfo_children(): w.destroy()
        self.labels.clear()
        self.detail_frames.clear()
        self.detail_labels.clear()
        
        bg_col = self.master.cget("bg")
        self.config(bg=bg_col)
        
        if self.is_collapsed:
            self._build_collapsed_ui(bg_col)
        else:
            self._build_expanded_ui(bg_col)
        
        # 使用 lambda 與 return "break" 確保事件不會冒泡到父層
        self.bind("<Button-1>", lambda e: self.manual_update(e))

    def _build_collapsed_ui(self, bg):
        lbl = tk.Label(self, text="·", font=("Arial", 10, "bold"), fg=StockStyle.PRIMARY_GREY, bg=bg, cursor="hand2")
        lbl.grid(row=0, column=0, padx=5, pady=2, sticky="e")
        lbl.bind("<Button-1>", self.toggle_collapse)

    def _build_expanded_ui(self, bg):
        stocks = self.data_manager.config_data.get("stocks", [])
        max_visible = 4 # 回復為 4 檔以節省空間，搭配捲軸查看更多項目
        item_height = 28 # 每列概估高度
        
        # 建立外層容器以區分布局：清單區 (捲動) 與 控制區 (固定)
        self.columnconfigure(0, weight=1)
        
        # 1. 捲動清單區
        list_container = tk.Frame(self, bg=bg)
        list_container.grid(row=0, column=0, sticky="nsew")
        
        # 表頭 (代號 基準 昨收 現價 走勢K線 漲跌)
        header_fm = tk.Frame(list_container, bg=bg)
        header_fm.pack(fill=tk.X, side=tk.TOP, padx=(7, 2))
        
        tk.Label(header_fm, text="代號", font=StockStyle.FONT_MAIN, fg=StockStyle.PRIMARY_GREY, bg=bg, width=6, anchor="e").grid(row=0, column=0, padx=2)
        tk.Label(header_fm, text="基準", font=StockStyle.FONT_MAIN, fg=StockStyle.PRIMARY_GREY, bg=bg, width=8, anchor="e").grid(row=0, column=1, padx=4)
        tk.Label(header_fm, text="昨收", font=StockStyle.FONT_MAIN, fg=StockStyle.PRIMARY_GREY, bg=bg, width=8, anchor="e").grid(row=0, column=2, padx=4)
        tk.Label(header_fm, text="現價", font=StockStyle.FONT_MAIN, fg=StockStyle.PRIMARY_GREY, bg=bg, width=8, anchor="e").grid(row=0, column=3, padx=4)
        
        c4_fm = tk.Frame(header_fm, width=80, height=20, bg=bg)
        c4_fm.grid(row=0, column=4, padx=5)
        c4_fm.grid_propagate(False)
        tk.Label(c4_fm, text="走勢 K 線", font=StockStyle.FONT_MAIN, fg=StockStyle.PRIMARY_GREY, bg=bg, anchor="center").pack(fill=tk.BOTH, expand=True)
        
        tk.Label(header_fm, text="漲跌", font=StockStyle.FONT_MAIN, fg=StockStyle.PRIMARY_GREY, bg=bg, width=7, anchor="w").grid(row=0, column=5, padx=2)
        
        # 計算畫布高度
        display_count = min(len(stocks), max_visible)
        canvas_h = display_count * item_height
        
        self.canvas = tk.Canvas(list_container, height=canvas_h, bg=bg, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 建立捲軸 (當股票數量超過顯示上限時)
        if len(stocks) > max_visible:
            sb = tk.Scrollbar(list_container, orient="vertical", command=self.canvas.yview, width=8)
            sb.pack(side=tk.RIGHT, fill=tk.Y)
            self.canvas.configure(yscrollcommand=sb.set)
        
        # 內部框架放置股票資料
        self.scroll_frame = tk.Frame(self.canvas, bg=bg)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        
        # 綁定捲動事件
        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        def set_item_bg(item_fm, row_fm, detail_fm, symbol, color):
            item_fm.config(bg=color)
            row_fm.config(bg=color)
            for child in row_fm.winfo_children():
                if isinstance(child, (tk.Label, tk.Canvas)):
                    child.config(bg=color)
            detail_fm.config(bg=color)
            for child in detail_fm.winfo_children():
                if isinstance(child, tk.Label):
                    lbl_key = getattr(child, "indicator_key", None)
                    is_hl = (self.highlighted_keys.get(symbol) == lbl_key) if lbl_key else False
                    if is_hl:
                        child.config(bg="#e5e5e5", fg="#000000")
                    else:
                        child.config(bg=color, fg=StockStyle.PRIMARY_GREY)

        active_border = self._get_dynamic_color("#ebebeb")
        # 定義分區資訊 (採用動態計算、貼合背景的極淺灰)
        categories = [
            ("etf", "ETF", active_border),
            ("bond", "美債", active_border),
            ("gold", "黃金", active_border),
            ("shipping", "海運", active_border),
            ("special", "1513 / 1773 / 6613", active_border),
            ("others", "其他股票", active_border)
        ]
        
        grouped_stocks = {cat_key: [] for cat_key, _, _ in categories}
        for stock in stocks:
            sym = stock.get("symbol", "")
            asset_type = stock.get("type", "stock")
            cat_key = self._get_category_key(sym, asset_type)
            if cat_key in grouped_stocks:
                grouped_stocks[cat_key].append(stock)
            else:
                grouped_stocks["others"].append(stock)

        # 遍歷各分區並渲染
        for cat_key, cat_title, border_color in categories:
            cat_stocks = grouped_stocks[cat_key]
            if not cat_stocks:
                continue
                
            # 建立該分類的框線容器 (使用 highlightthickness=1 產生實線邊框)
            group_fm = tk.Frame(self.scroll_frame, bg=bg, highlightthickness=1, highlightbackground=border_color)
            group_fm.pack(fill=tk.X, padx=4, pady=4)
            
            # 分區標題
            title_lbl = tk.Label(group_fm, text=cat_title, font=StockStyle.FONT_BOLD, fg=StockStyle.PRIMARY_GREY, bg=bg, anchor="w")
            title_lbl.pack(fill=tk.X, padx=6, pady=(4, 2))
            
            for stock in cat_stocks:
                symbol = stock.get("symbol", "")
                ref = stock.get("reference", "-")
                display_sym = symbol.split('_')[-1]
                
                # 建立單列容器 (置於 group_fm 內)
                item_fm = tk.Frame(group_fm, bg=bg)
                item_fm.pack(fill=tk.X, pady=1, padx=2)
                
                row_fm = tk.Frame(item_fm, bg=bg)
                row_fm.pack(fill=tk.X, expand=True)
                
                detail_fm = tk.Frame(item_fm, bg=bg)
                self.detail_frames[symbol] = detail_fm
                
                def make_hover_handlers(i_fm=item_fm, r_fm=row_fm, d_fm=detail_fm, sym=symbol):
                    def on_enter(e):
                        set_item_bg(i_fm, r_fm, d_fm, sym, StockStyle.HOVER_BG)
                    
                    def on_leave(e):
                        x, y = self.winfo_pointerxy()
                        containing = self.winfo_containing(x, y)
                        if containing:
                            p = containing
                            is_inside = False
                            while p:
                                if p == i_fm:
                                    is_inside = True
                                    break
                                p = p.master
                            if is_inside:
                                return
                        set_item_bg(i_fm, r_fm, d_fm, sym, bg)
                        self._clear_highlights(sym)
                    return on_enter, on_leave

                on_enter, on_leave = make_hover_handlers()
                
                item_fm.bind("<Enter>", on_enter)
                item_fm.bind("<Leave>", on_leave)
                row_fm.bind("<Enter>", on_enter)
                row_fm.bind("<Leave>", on_leave)
                detail_fm.bind("<Enter>", on_enter)
                detail_fm.bind("<Leave>", on_leave)

                # 標記 (使用 grid 以維持對齊)
                row_fm.columnconfigure(4, weight=1) # 讓圖表區有伸縮性
                
                sym_lbl = tk.Label(row_fm, text=display_sym, font=StockStyle.FONT_MAIN, fg=StockStyle.PRIMARY_GREY, bg=bg, cursor="hand2", width=6, anchor="e")
                sym_lbl.grid(row=0, column=0, padx=2)
                sym_lbl.bind("<Button-1>", lambda e, s=symbol, r=ref, cfg=stock: self._show_edit_dialog(e, s, r, cfg))
                
                ref_lbl = tk.Label(row_fm, text=str(ref), font=StockStyle.FONT_MAIN, fg=StockStyle.PRIMARY_GREY, bg=bg, width=8, anchor="e")
                ref_lbl.grid(row=0, column=1, padx=4)

                prev_lbl = tk.Label(row_fm, text="-", font=StockStyle.FONT_MAIN, fg=StockStyle.PRIMARY_GREY, bg=bg, width=8, anchor="e")
                prev_lbl.grid(row=0, column=2, padx=4)
                
                curr_lbl = tk.Label(row_fm, text="-", font=StockStyle.FONT_MAIN, fg=StockStyle.PRIMARY_GREY, bg=bg, width=8, anchor="e", cursor="hand2")
                curr_lbl.grid(row=0, column=3, padx=4)
                curr_lbl.bind("<Button-1>", lambda e, s=symbol: self._toggle_detail_bar(s))
                
                canvas_bar = tk.Canvas(row_fm, width=80, height=24, bg=bg, highlightthickness=0, cursor="hand2")
                canvas_bar.grid(row=0, column=4, padx=5)
                canvas_bar.bind("<Button-1>", lambda e, c=canvas_bar: self._on_bar_click(e, c))
                canvas_bar.bind("<Leave>", lambda e, c=canvas_bar: self._hide_temp_val(c))
                
                diff_lbl = tk.Label(row_fm, text="", font=StockStyle.FONT_SMALL, fg=StockStyle.PRIMARY_GREY, bg=bg, width=7, anchor="w")
                diff_lbl.grid(row=0, column=5, padx=2)
                
                # 綁定子元件 hover 事件
                for child in row_fm.winfo_children():
                    if child == sym_lbl:
                        child.bind("<Enter>", lambda e, w=sym_lbl: (on_enter(e), w.config(fg=StockStyle.HOVER_GREY)))
                        child.bind("<Leave>", lambda e, w=sym_lbl: (on_leave(e), w.config(fg=StockStyle.PRIMARY_GREY)))
                    else:
                        child.bind("<Enter>", on_enter)
                        child.bind("<Leave>", on_leave)
                
                self.labels[symbol] = (prev_lbl, curr_lbl, canvas_bar, diff_lbl)
                
                # 如果原本是展開的，維持展開
                if symbol in self.expanded_symbols:
                    detail_fm.pack(fill=tk.X)
                    self._render_detail_content(symbol)

        # 2. 參考指標區 (放在捲動區最底部，跟股票一併捲動，統一使用極淺灰框)
        indices_container = tk.Frame(self.scroll_frame, bg=bg, highlightthickness=1, highlightbackground=active_border)
        indices_container.pack(fill=tk.X, padx=4, pady=4)
        
        # 分區標題
        title_lbl = tk.Label(indices_container, text="參考指標", font=StockStyle.FONT_BOLD, fg=StockStyle.PRIMARY_GREY, bg=bg, anchor="w")
        title_lbl.pack(fill=tk.X, padx=6, pady=(4, 2))
        
        index_symbols = [
            ("^N225", "日經"),
            ("^KS11", "韓股"),
            ("^SOX", "費半"),
            ("CL=F", "油價")
        ]
        
        self.index_labels = {}
        for sym, name in index_symbols:
            item_fm = tk.Frame(indices_container, bg=bg)
            item_fm.pack(fill=tk.X, pady=1, padx=2)
            
            row_fm = tk.Frame(item_fm, bg=bg)
            row_fm.pack(fill=tk.X, expand=True)
            
            row_fm.columnconfigure(4, weight=1) # 讓圖表區有伸縮性
            
            sym_lbl = tk.Label(row_fm, text=name, font=StockStyle.FONT_MAIN, fg=StockStyle.PRIMARY_GREY, bg=bg, width=6, anchor="e")
            sym_lbl.grid(row=0, column=0, padx=2)
            
            ref_lbl = tk.Label(row_fm, text="-", font=StockStyle.FONT_MAIN, fg=StockStyle.PRIMARY_GREY, bg=bg, width=8, anchor="e")
            ref_lbl.grid(row=0, column=1, padx=4)
            
            prev_lbl = tk.Label(row_fm, text="-", font=StockStyle.FONT_MAIN, fg=StockStyle.PRIMARY_GREY, bg=bg, width=8, anchor="e")
            prev_lbl.grid(row=0, column=2, padx=4)
            
            curr_lbl = tk.Label(row_fm, text="-", font=StockStyle.FONT_MAIN, fg=StockStyle.PRIMARY_GREY, bg=bg, width=8, anchor="e")
            curr_lbl.grid(row=0, column=3, padx=4)
            
            canvas_bar = tk.Canvas(row_fm, width=80, height=24, bg=bg, highlightthickness=0)
            canvas_bar.grid(row=0, column=4, padx=5)
            
            diff_lbl = tk.Label(row_fm, text="", font=StockStyle.FONT_SMALL, fg=StockStyle.PRIMARY_GREY, bg=bg, width=7, anchor="w")
            diff_lbl.grid(row=0, column=5, padx=2)
            
            self.index_labels[sym] = (prev_lbl, curr_lbl, canvas_bar, diff_lbl)

        # 3. 固定控制區 (放在 Grid 的下一列)
        ctrl_container = tk.Frame(self, bg=bg)
        ctrl_container.grid(row=1, column=0, sticky="ew")
        self._build_control_btns(ctrl_container, bg)

    def _on_mousewheel(self, event):
        """處理滑鼠捲動，僅當滑鼠在小工具上方時觸發"""
        # 檢查滑鼠是否在小工具範圍內
        x, y = self.winfo_pointerxy()
        widget = self.winfo_containing(x, y)
        
        # 如果當前 widget 是本體或其子元件，且 Canvas 存在
        if widget and (str(widget).startswith(str(self))) and hasattr(self, "canvas") and self.canvas.winfo_exists():
            try:
                self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except:
                pass

    def _build_control_btns(self, container, bg):
        items = [
            ("⚙️", 0, "w", self._show_global_config_dialog),
            ("×", 3, "e", self.toggle_collapse),
            ("↻", 4, "w", self.manual_update)
        ]

        if self.on_notify_toggle:
            items.append(("🔔", 2, "e", lambda: self.on_notify_toggle()))

        container.columnconfigure(1, weight=1) # 中間留白
        
        for text, col, stick, cmd in items:
            btn = tk.Label(container, text=text, font=("Arial", 10), fg=StockStyle.PRIMARY_GREY, bg=bg, cursor="hand2")
            btn.grid(row=0, column=col, padx=8, pady=2, sticky=stick)
            btn.bind("<Button-1>", lambda e, c=cmd: (c(), "break")[1])
            self._add_hover(btn)

    def _add_hover(self, widget):
        widget.bind("<Enter>", lambda e: widget.config(fg=StockStyle.HOVER_GREY))
        widget.bind("<Leave>", lambda e: widget.config(fg=StockStyle.PRIMARY_GREY))

    def manual_update(self, event=None):
        """強助手動刷新：重新載入設定、重建 UI、並立即抓取數據"""
        # 1. 重新讀取設定與週期
        self.data_manager.config_data = self.data_manager.load_config()
        self.update_interval_ms = self.data_manager.config_data.get("update_interval_seconds", 30) * 1000
        
        # 2. 重建 UI
        self._build_ui()
        self.update_idletasks() # 強制同步 UI 尺寸以便後續計算
            
        # 3. 初始狀態回饋
        for sym in self.labels:
            _, lbl_curr, canvas, _ = self.labels[sym]
            if lbl_curr.winfo_exists():
                lbl_curr.config(text="..." )
                canvas.delete("all")
        
        # 4. 執行數據更新
        self.refresh_prices()
        return "break"

    def refresh_prices(self):
        if not self.winfo_exists(): return
        if self._update_job: 
            self.after_cancel(self._update_job)
            self._update_job = None
        
        # 更新畫布內的 window 寬度 (增加 winfo_width > 1 判斷)
        if hasattr(self, "canvas") and self.canvas.winfo_exists() and hasattr(self, "scroll_frame") and self.scroll_frame.winfo_exists():
            w = self.canvas.winfo_width()
            if w > 1:
                self.canvas.itemconfig(self.canvas_window, width=w)
            
        self.data_manager.fetch_prices(self._on_fetch_done)

    def _on_fetch_done(self, result):
        # 切換到主執行緒執行 UI 更新
        self.after(0, lambda: self._do_apply_updates(result))

    def _do_apply_updates(self, result):
        if not self.winfo_exists(): return
        
        # 二次嘗試校正寬度，確保數據填入時布局是正確的
        if hasattr(self, "canvas") and self.canvas.winfo_exists():
            w = self.canvas.winfo_width()
            if w > 1:
                self.canvas.itemconfig(self.canvas_window, width=w)

        # 哪怕 fetch 失敗或是處於縮小狀態，也要排程下一次更新，否則功能會「失去」
        if result and not self.is_collapsed:
            updates = result.get("updates", {})
            alerts = result.get("alerts", [])
            
            for sym, data in updates.items():
                if sym not in self.labels: continue
                # 注意：data 格式為 (prev, curr, high, low, hint)
                prev, curr, high, low, hint = data
                lbl_prev, lbl_curr, canvas, lbl_diff = self.labels[sym]
                if not lbl_curr.winfo_exists(): continue

                # 更新文字
                lbl_prev.config(text=f"{prev:.2f}")
                lbl_curr.config(text=f"{curr:.{hint}f}")
                diff_pct = (curr - prev) / prev * 100 if prev > 0 else 0
                lbl_diff.config(text=f"{diff_pct:+.2f}%")

                # 繪製圖形
                self._draw_status_bar(canvas, prev, curr, high, low, sym)
                
                # 若處於展開狀態，一併刷新詳細數值列
                if sym in self.expanded_symbols:
                    self._render_detail_content(sym)

            # 更新全球參考指標
            indices = result.get("indices", {})
            self.last_indices = indices
            for sym, data in indices.items():
                if sym not in getattr(self, "index_labels", {}): continue
                prev, curr, high, low, hint = data
                lbl_prev, lbl_curr, canvas, lbl_diff = self.index_labels[sym]
                if not lbl_curr.winfo_exists(): continue

                lbl_prev.config(text=f"{prev:.2f}")
                lbl_curr.config(text=f"{curr:.{hint}f}")
                diff_pct = (curr - prev) / prev * 100 if prev > 0 else 0
                lbl_diff.config(text=f"{diff_pct:+.2f}%")

                self._draw_status_bar(canvas, prev, curr, high, low, sym)

            # 觸發預警通知
            if self.on_alert:
                self.on_alert(alerts)

        # 排程下一次自動更新
        self._update_job = self.after(self.update_interval_ms, self.refresh_prices)

    def _draw_status_bar(self, canvas, prev, curr, high, low, symbol):
        canvas.delete("all")
        w = canvas.winfo_width()
        if w <= 1:
            w = int(canvas.cget("width"))
        h = canvas.winfo_height()
        if h <= 1:
            h = int(canvas.cget("height"))
        
        # 獲取 computed 數據
        computed = self.data_manager.computed_assets.get(symbol)
        ma20 = computed.get("ma20") if computed else None
        wa5 = computed.get("wa5") if computed else None
        ma60 = computed.get("ma60") if computed else None
        ma120 = computed.get("ma120") if computed else None
        nav = computed.get("nav") if (computed and computed.get("type") == "etf") else None
        strong_buy = computed.get("strongBuyPrice") if computed else None
        
        # 判斷 strong_buy 是否在原本的橫線上 (low <= strong_buy <= high)
        show_strong_buy = False
        if strong_buy is not None:
            if low <= strong_buy <= high:
                show_strong_buy = True
        
        # 計算當日波動主體範圍，以進行月線與周線的繪圖限幅
        base_low = min(prev, curr, low)
        base_high = max(prev, curr, high)
        limit_val = prev * 0.10 if prev > 0 else 0
        
        ma20_drawn = max(base_low - limit_val, min(base_high + limit_val, ma20)) if ma20 is not None else None
        wa5_drawn = max(base_low - limit_val, min(base_high + limit_val, wa5)) if wa5 is not None else None
        
        # 收集所有有值的價格 (月線與周線使用限幅後的繪圖值，避免拉扁主橫線。季線與半年線不納入決定 X 軸比例的計算)
        all_vals = [prev, curr, high, low]
        if ma20_drawn is not None: all_vals.append(ma20_drawn)
        if wa5_drawn is not None: all_vals.append(wa5_drawn)
        
        v_low, v_high = min(all_vals), max(all_vals)
        v_range = v_high - v_low
        v_range_pct = (v_range / prev * 100.0) if prev > 0 else 0
        
        scale = min(1.0, (v_range_pct / 10.0) ** 0.7) if v_range_pct > 0 else 0.05
        # 將安全邊距由 12 擴大至 24，防止當現價在最高/最低點時指標被 Canvas 邊界截斷
        uw = (w - 24) * scale
        if uw < 10: uw = 10
        start_x = (w - uw) / 2
        
        def get_x(v):
            return start_x + (v - v_low) / (v_high - v_low) * uw if v_high > v_low else w/2

        xl, xh, xp, xc = get_x(low), get_x(high), get_x(prev), get_x(curr)
        
        # 確保最低至最高軌道長度不低於 8px，防止單點情況下橫線完全「消失」
        if xh - xl < 8:
            diff = (8 - (xh - xl)) / 2
            xl -= diff
            xh += diff

        canvas.stock_coords = [
            {"key": "low", "val": low, "x": xl},
            {"key": "high", "val": high, "x": xh}
        ]
        canvas.stock_symbol = symbol

        # 軌道與端點繪製：去除異化色彩，統一為柔和的灰白軌道 (BAR_TRACK)
        track_w = 2.5  # 軌道寬度定為 2.5px，極簡自然
        
        canvas.create_line(xl, h/2, xh, h/2, fill=StockStyle.BAR_TRACK, width=track_w, capstyle=tk.ROUND)
        color_l = StockStyle.BAR_TRACK
        color_r = StockStyle.BAR_TRACK
            
        # 端點
        canvas.create_oval(xl-2, h/2-2, xl+2, h/2+2, fill=color_l, outline="")
        canvas.create_oval(xh-2, h/2-2, xh+2, h/2+2, fill=color_r, outline="")

        # 昨日收盤價格 (隨全局顏色強度動態調整)
        canvas.create_line(xp, 4, xp, h-4, fill=StockStyle.PRIMARY_GREY, width=1)
        
        # 現在價格 (指示器：點或三角形，隨全局顏色強度動態調整)
        if curr > prev:
            points = [xc+5, h/2, xc-3, h/2-4, xc-3, h/2+4]
            canvas.create_polygon(points, fill=StockStyle.PRIMARY_GREY, outline=StockStyle.PRIMARY_GREY)
        elif curr < prev:
            points = [xc-5, h/2, xc+3, h/2-4, xc+3, h/2+4]
            canvas.create_polygon(points, fill=StockStyle.PRIMARY_GREY, outline=StockStyle.PRIMARY_GREY)
        else:
            canvas.create_oval(xc-3, h/2-3, xc+3, h/2+3, fill=StockStyle.PRIMARY_GREY, outline=StockStyle.PRIMARY_GREY)
            
        # 繪製有值的指標垂直短線刻度，並記錄在 stock_coords 中
        indicator_draws = []
        if wa5 is not None:
            indicator_draws.append(("wa5", wa5, wa5_drawn))
        if ma20 is not None:
            indicator_draws.append(("ma20", ma20, ma20_drawn))
        if ma60 is not None and v_low <= ma60 <= v_high:
            indicator_draws.append(("ma60", ma60, ma60))
        if ma120 is not None and v_low <= ma120 <= v_high:
            indicator_draws.append(("ma120", ma120, ma120))
            
        # 設定不同指標的線條樣式（統一使用極柔和灰白色彩 #cccccc）
        style_map = {
            "wa5": {"width": 1.5, "color": "#cccccc", "dash": None},            # 週線：極淡灰白實線
            "ma20": {"width": 1.5, "color": "#cccccc", "dash": (2, 2)},         # 月線：極淡灰白密虛線
            "ma60": {"width": 1.5, "color": "#cccccc", "dash": (4, 4)},         # 季線：極淡灰白疏虛線
            "ma120": {"width": 1.5, "color": "#cccccc", "dash": (1, 3)}         # 半年線：極淡灰白點線
        }

        for key, val, val_drawn in indicator_draws:
            if val is not None:
                x = get_x(val_drawn)
                style = style_map.get(key, {"width": 2, "color": StockStyle.PRIMARY_GREY, "dash": None})
                
                # 週線畫在上半部，中長均線均畫在下半部，以達到明確的空間區隔
                if key == "wa5":
                    y1, y2 = h/2 - 7, h/2
                elif key in ["ma20", "ma60", "ma120"]:
                    y1, y2 = h/2, h/2 + 7
                else:
                    y1, y2 = h/2 - 6, h/2 + 6

                if style["dash"]:
                    canvas.create_line(x, y1, x, y2,
                                       fill=style["color"],
                                       width=style["width"], dash=style["dash"])
                else:
                    canvas.create_line(x, y1, x, y2,
                                       fill=style["color"],
                                       width=style["width"])
                canvas.stock_coords.append({
                    "key": key,
                    "val": val,
                    "x": x
                })

    def _on_bar_click(self, event, canvas):
        if hasattr(canvas, "stock_coords") and canvas.stock_coords:
            valid_coords = [c for c in canvas.stock_coords if c.get('key')]
            if not valid_coords: return
            
            closest = min(valid_coords, key=lambda c: abs(event.x - c['x']))
            symbol = getattr(canvas, "stock_symbol", None)
            if symbol:
                if symbol not in self.expanded_symbols:
                    self._toggle_detail_bar(symbol)
                self._highlight_detail_label(symbol, closest['key'])

    def _hide_temp_val(self, canvas):
        pass

    def _highlight_detail_label(self, symbol, key):
        self._clear_highlights(symbol)
        
        self.highlighted_keys[symbol] = key
        
        labels_map = self.detail_labels.get(symbol, {})
        lbl = labels_map.get(key)
        if lbl and lbl.winfo_exists():
            lbl.config(bg="#e5e5e5", fg="#000000")

    def _clear_highlights(self, symbol):
        if symbol in self.highlighted_keys:
            del self.highlighted_keys[symbol]
        
        labels_map = self.detail_labels.get(symbol, {})
        detail_fm = self.detail_frames.get(symbol)
        bg_color = detail_fm.cget("bg") if (detail_fm and detail_fm.winfo_exists()) else self.master.cget("bg")
        
        for key, lbl in labels_map.items():
            if lbl and lbl.winfo_exists():
                lbl.config(bg=bg_color, fg=StockStyle.PRIMARY_GREY)

    def _toggle_detail_bar(self, symbol):
        detail_fm = self.detail_frames.get(symbol)
        if not detail_fm: return
        
        if symbol in self.expanded_symbols:
            self.expanded_symbols.remove(symbol)
            detail_fm.pack_forget()
        else:
            # 限制同時只能開啟一個：關閉其他所有目前展開的股票
            for other_sym in list(self.expanded_symbols):
                other_fm = self.detail_frames.get(other_sym)
                if other_fm:
                    other_fm.pack_forget()
                self.expanded_symbols.discard(other_sym)
                
            self.expanded_symbols.add(symbol)
            detail_fm.pack(fill=tk.X)
            self._render_detail_content(symbol)

    def _render_detail_content(self, symbol):
        detail_fm = self.detail_frames.get(symbol)
        if not detail_fm or not detail_fm.winfo_exists(): return
        
        for w in detail_fm.winfo_children():
            w.destroy()
            
        if symbol not in self.detail_labels:
            self.detail_labels[symbol] = {}
        else:
            self.detail_labels[symbol].clear()
            
        computed = self.data_manager.computed_assets.get(symbol)
        if not computed: return
        
        indicator_configs = [
            ("最高", "high", computed.get("high")),
            ("最低", "low", computed.get("low")),
            ("WA", "wa5", computed.get("wa5")),
            ("MA", "ma20", computed.get("ma20")),
            ("季線", "ma60", computed.get("ma60")),
            ("半年", "ma120", computed.get("ma120"))
        ]
        
        valid_indicators = [(label, key, val) for label, key, val in indicator_configs if val is not None]
        if not valid_indicators:
            return
            
        bg_col = detail_fm.cget("bg")
        
        pad_lbl = tk.Label(detail_fm, text="   詳細指標:", font=StockStyle.FONT_SMALL, fg=StockStyle.PRIMARY_GREY, bg=bg_col)
        pad_lbl.pack(side=tk.LEFT, padx=2)
        
        for label_text, key, val in valid_indicators:
            display_text = f" {label_text}: {val:.2f} "
            lbl = tk.Label(detail_fm, text=display_text, font=StockStyle.FONT_BOLD, fg=StockStyle.PRIMARY_GREY, bg=bg_col, cursor="hand2")
            lbl.pack(side=tk.LEFT, padx=8, pady=2)
            
            lbl.indicator_key = key
            self.detail_labels[symbol][key] = lbl
            
            lbl.bind("<Button-1>", lambda e, s=symbol, k=key: self._highlight_detail_label(s, k))
            
            if self.highlighted_keys.get(symbol) == key:
                lbl.config(bg="#e5e5e5", fg="#000000")

    def _show_edit_dialog(self, event, symbol, current_ref, stock_cfg):
        # 實現 Toggle 邏輯：按第二次就收回
        if self.active_dialog and self.active_dialog.winfo_exists():
            is_same = (self.active_trigger == symbol)
            self.active_dialog.destroy()
            self.active_dialog = None
            self.active_trigger = None
            if is_same: return

        dialog = tk.Toplevel(self)
        self.active_dialog = dialog
        self.active_trigger = symbol
        
        dialog.title(f"標的設定: {symbol.split('_')[-1]}")
        
        # 置中於螢幕
        w, h = 300, 240
        sw = dialog.winfo_screenwidth()
        sh = dialog.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        dialog.geometry(f"{w}x{h}+{x}+{y}")
        dialog.resizable(0, 0)

        dialog.attributes("-topmost", True)
        
        # 標題與基準價
        tk.Label(dialog, text=f"【{symbol.split('_')[-1]}】 參數調校", font=StockStyle.FONT_BOLD).pack(pady=5)
        
        fm = tk.Frame(dialog); fm.pack(padx=10, fill=tk.X)
        
        # 基準價 (影響長線)
        tk.Label(fm, text="基準(參考價):").grid(row=0, column=0, sticky="e", pady=2)
        e_ref = tk.Entry(fm, width=12); e_ref.insert(0, str(current_ref)); e_ref.grid(row=0, column=1)
        
        # 短線預警 (vs 昨收)
        tk.Label(fm, text="短線預警(vs昨收%):").grid(row=1, column=0, sticky="e", pady=2)
        e_short = tk.Entry(fm, width=12); e_short.insert(0, str(stock_cfg.get('alert_short', ''))); e_short.grid(row=1, column=1)
        
        tk.Label(dialog, text="---------------------------", fg="#ccc").pack()
        
        # 長線預警 (vs 基準) - 雙向綁定
        fm2 = tk.Frame(dialog); fm2.pack(padx=10, fill=tk.X)
        tk.Label(fm2, text="長線目標價上下限/百分比(vs基準):", font=("Arial", 8, "italic")).grid(row=0, column=0, columnspan=4, pady=(0,5))
        
        tk.Label(fm2, text="目標上限:").grid(row=1, column=0, sticky="e")
        e_target_up_p = tk.Entry(fm2, width=8); e_target_up_p.grid(row=1, column=1)
        tk.Label(fm2, text="%:").grid(row=1, column=2, sticky="e")
        e_target_up_pct = tk.Entry(fm2, width=6); e_target_up_pct.grid(row=1, column=3)
        
        tk.Label(fm2, text="目標下限:").grid(row=2, column=0, sticky="e")
        e_target_down_p = tk.Entry(fm2, width=8); e_target_down_p.grid(row=2, column=1)
        tk.Label(fm2, text="%:").grid(row=2, column=2, sticky="e")
        e_target_down_pct = tk.Entry(fm2, width=6); e_target_down_pct.grid(row=2, column=3)
        
        # 初始填充長線數值
        def_long = self.data_manager.config_data.get('alert_threshold_long', 15.0)
        curr_up_th = stock_cfg.get('alert_long_up', stock_cfg.get('alert_long', def_long))
        curr_down_th = stock_cfg.get('alert_long_down', stock_cfg.get('alert_long', def_long))
        
        e_target_up_pct.insert(0, str(curr_up_th))
        e_target_down_pct.insert(0, str(curr_down_th))
        try:
            target_up_p = current_ref * (1 + curr_up_th/100.0)
            e_target_up_p.insert(0, f"{target_up_p:.2f}")
            target_down_p = current_ref * (1 - curr_down_th/100.0)
            e_target_down_p.insert(0, f"{target_down_p:.2f}")
        except: pass

        def sync_p_to_pct(ev=None):
            try:
                ref = float(e_ref.get())
                p_up = float(e_target_up_p.get())
                pct_up = (p_up - ref) / ref * 100 if ref > 0 else 0
                e_target_up_pct.delete(0, tk.END); e_target_up_pct.insert(0, f"{pct_up:.2f}")
            except: pass
            try:
                ref = float(e_ref.get())
                p_down = float(e_target_down_p.get())
                pct_down = (ref - p_down) / ref * 100 if ref > 0 else 0
                e_target_down_pct.delete(0, tk.END); e_target_down_pct.insert(0, f"{pct_down:.2f}")
            except: pass

        def sync_pct_to_p(ev=None):
            try:
                ref = float(e_ref.get())
                pct_up = float(e_target_up_pct.get())
                p_up = ref * (1 + pct_up / 100.0)
                e_target_up_p.delete(0, tk.END); e_target_up_p.insert(0, f"{p_up:.2f}")
            except: pass
            try:
                ref = float(e_ref.get())
                pct_down = float(e_target_down_pct.get())
                p_down = ref * (1 - pct_down / 100.0)
                e_target_down_p.delete(0, tk.END); e_target_down_p.insert(0, f"{p_down:.2f}")
            except: pass

        e_target_up_p.bind("<KeyRelease>", sync_p_to_pct)
        e_target_down_p.bind("<KeyRelease>", sync_p_to_pct)
        e_target_up_pct.bind("<KeyRelease>", sync_pct_to_p)
        e_target_down_pct.bind("<KeyRelease>", sync_pct_to_p)

        def save():
            try:
                params = {
                    "reference": float(e_ref.get()),
                    "alert_short": float(e_short.get()) if e_short.get() else 5.0,
                    "alert_long_up": float(e_target_up_pct.get()) if e_target_up_pct.get() else 15.0,
                    "alert_long_down": float(e_target_down_pct.get()) if e_target_down_pct.get() else 15.0
                }
                
                # 若舊參數存在則移除，避免干擾，但因為 save_stock_params 是 update 所以可能會保留
                # 我們可以藉由回傳 params 更新 data，但沒法輕鬆刪除 key。
                if self.data_manager.save_stock_params(symbol, params):
                    self._build_ui(); self.refresh_prices(); dialog.destroy()
            except Exception as e:
                messagebox.showerror("錯誤", f"請檢查欄位格式: {e}")

        btn_fm = tk.Frame(dialog); btn_fm.pack(pady=10)
        tk.Button(btn_fm, text="儲存", command=save, width=8).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_fm, text="取消", command=dialog.destroy, width=8).pack(side=tk.LEFT, padx=5)


    def _show_global_config_dialog(self):
        # 實現 Toggle 邏輯
        trigger_id = "GLOBAL_CONFIG"
        if self.active_dialog and self.active_dialog.winfo_exists():
            is_same = (self.active_trigger == trigger_id)
            self.active_dialog.destroy()
            self.active_dialog = None
            self.active_trigger = None
            if is_same: return

        dialog = tk.Toplevel(self)
        self.active_dialog = dialog
        self.active_trigger = trigger_id
        
        dialog.title("全局股票設定")
        dialog.transient(self.winfo_toplevel())  # 設為基礎介面的子視窗，保持高一層
        dialog.grab_set()  # 鎖定焦點於此對話框

        # 置中於螢幕 - 增加寬度與高度以容納滑桿 (Scale)
        w, h = 280, 360
        sw = dialog.winfo_screenwidth()
        sh = dialog.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        dialog.geometry(f"{w}x{h}+{x}+{y}")
        
        bg = self.cget("bg")
        tk.Label(dialog, text="全局預設參數", font=StockStyle.FONT_BOLD).pack(pady=10)
        
        fm_cfg = tk.Frame(dialog); fm_cfg.pack(padx=20)
        cfg = self.data_manager.config_data
        
        tk.Label(fm_cfg, text="預設短預警(%):").grid(row=0, column=0, sticky="e", pady=2)
        e_s = tk.Entry(fm_cfg, width=8); e_s.insert(0, str(cfg.get('alert_threshold_short', 5.0))); e_s.grid(row=0, column=1)
        
        tk.Label(fm_cfg, text="預設長預警(%):").grid(row=1, column=0, sticky="e", pady=2)
        e_l = tk.Entry(fm_cfg, width=8); e_l.insert(0, str(cfg.get('alert_threshold_long', 15.0))); e_l.grid(row=1, column=1)
        
        tk.Label(fm_cfg, text="顏色強度滑桿:").grid(row=2, column=0, sticky="e", pady=2)
        val_i = cfg.get('color_intensity', 1.0)
        s_i = tk.Scale(fm_cfg, from_=0.0, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, length=80, showvalue=True)
        s_i.set(val_i)
        s_i.grid(row=2, column=1, sticky="w", pady=2)

        def save():
            try:
                new_cfg = {
                    "alert_threshold_short": float(e_s.get()),
                    "alert_threshold_long": float(e_l.get()),
                    "color_intensity": float(s_i.get())
                }
                if self.data_manager.update_global_config(new_cfg):
                    self._build_ui(); self.refresh_prices(); dialog.destroy()
            except: messagebox.showerror("錯誤", "請輸入有效數字")

        btn_fm = tk.Frame(dialog); btn_fm.pack(pady=15)
        tk.Button(btn_fm, text="儲存", command=save, width=10).pack(side=tk.LEFT, padx=5)

        # --- 新增：程式位置展示區 ---
        tk.Label(dialog, text="---------------------------", fg="#ccc").pack()
        tk.Label(dialog, text="程式位置 (可找到設定檔):", font=("Arial", 8, "italic"), fg="#888888").pack()
        
        app_path = os.path.dirname(os.path.abspath(self.data_manager.config_path))
        path_lbl = tk.Label(dialog, text=app_path, font=("Arial", 7), fg="#999999", wraplength=220, justify="center")
        path_lbl.pack(padx=10)
        
        def open_folder():
            try:
                os.startfile(app_path)
            except:
                pass
                
        tk.Button(dialog, text="📁 開啟程式資料夾", font=("Arial", 8), command=open_folder, 
                  relief=tk.FLAT, fg="#6666ff", cursor="hand2").pack(pady=5)
