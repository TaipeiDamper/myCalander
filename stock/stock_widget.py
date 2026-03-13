import tkinter as tk
from tkinter import messagebox
import os
from .data_manager import StockDataManager

CONFIG_FILE = "stock_config.json"

class StockStyle:
    """集中管理 UI 配色與樣式"""
    PRIMARY_GREY = "#d0d0d0"
    HOVER_GREY = "#888888"
    BAR_TRACK = "#e0e0e0"
    BAR_GUIDE = "#d0d0d0"
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
        self._update_job = None
        self.is_collapsed = False
        self.active_dialog = None  # 紀錄當前開啟的對話視窗
        self.active_trigger = None # 紀錄是誰觸發的 (代號或⚙️)

        
        # 初始化數據管理器
        self.data_manager = StockDataManager(self._get_config_path())
        self.update_interval_ms = self.data_manager.config_data.get("update_interval_seconds", 30) * 1000
        
        self._build_ui()
        self.refresh_prices()
        
    def _get_config_path(self):
        import sys
        base = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base, CONFIG_FILE)

    def toggle_collapse(self, event=None):
        self.is_collapsed = not self.is_collapsed
        self._build_ui()
        if not self.is_collapsed:
            self.refresh_prices()

    def _build_ui(self):
        for w in self.winfo_children(): w.destroy()
        self.labels.clear()
        
        bg_col = self.master.cget("bg")
        self.config(bg=bg_col)
        
        if self.is_collapsed:
            self._build_collapsed_ui(bg_col)
        else:
            self._build_expanded_ui(bg_col)
        
        self.bind("<Button-1>", self.manual_update)

    def _build_collapsed_ui(self, bg):
        lbl = tk.Label(self, text="·", font=("Arial", 10, "bold"), fg=StockStyle.PRIMARY_GREY, bg=bg, cursor="hand2")
        lbl.grid(row=0, column=0, padx=5, pady=2, sticky="e")
        lbl.bind("<Button-1>", self.toggle_collapse)

    def _build_expanded_ui(self, bg):
        stocks = self.data_manager.config_data.get("stocks", [])
        for i, stock in enumerate(stocks):
            symbol = stock.get("symbol", "")
            ref = stock.get("reference", "-")
            display_sym = symbol.split('_')[-1]
            
            # 標記
            sym_lbl = tk.Label(self, text=display_sym, font=StockStyle.FONT_MAIN, fg=StockStyle.PRIMARY_GREY, bg=bg, cursor="hand2")
            sym_lbl.grid(row=i, column=0, padx=2, pady=2, sticky="e")
            sym_lbl.bind("<Button-1>", lambda e, s=symbol, r=ref, cfg=stock: self._show_edit_dialog(e, s, r, cfg))
            self._add_hover(sym_lbl)
            
            ref_lbl = tk.Label(self, text=str(ref), font=StockStyle.FONT_MAIN, fg=StockStyle.PRIMARY_GREY, bg=bg)
            ref_lbl.grid(row=i, column=1, padx=4, sticky="e")


            
            prev_lbl = tk.Label(self, text="-", font=StockStyle.FONT_MAIN, fg=StockStyle.PRIMARY_GREY, bg=bg)
            prev_lbl.grid(row=i, column=2, padx=4, sticky="e")
            
            curr_lbl = tk.Label(self, text="-", font=StockStyle.FONT_MAIN, fg=StockStyle.PRIMARY_GREY, bg=bg)
            curr_lbl.grid(row=i, column=3, padx=4, sticky="e")
            
            canvas = tk.Canvas(self, width=80, height=24, bg=bg, highlightthickness=0, cursor="hand2")
            canvas.grid(row=i, column=4, padx=5, sticky="w")
            canvas.bind("<Button-1>", lambda e, c=canvas: self._on_bar_click(e, c))
            canvas.bind("<Leave>", lambda e, c=canvas: self._hide_temp_val(c))
            
            diff_lbl = tk.Label(self, text="", font=StockStyle.FONT_SMALL, fg=StockStyle.PRIMARY_GREY, bg=bg, justify="left")
            diff_lbl.grid(row=i, column=5, padx=2, sticky="w")
            
            self.labels[symbol] = (prev_lbl, curr_lbl, canvas, diff_lbl)

        # 底部控制鈕
        btn_row = len(stocks)
        self._build_control_btns(btn_row, bg)

    def _build_control_btns(self, row, bg):
        items = [
            ("⚙️", 1, "w", self._show_global_config_dialog),
            ("×", 4, "e", self.toggle_collapse),
            ("↻", 5, "w", self.manual_update)
        ]

        if self.on_notify_toggle:
            items.append(("🔔", 3, "e", lambda: self.on_notify_toggle()))

        for text, col, stick, cmd in items:
            btn = tk.Label(self, text=text, font=("Arial", 10), fg=StockStyle.PRIMARY_GREY, bg=bg, cursor="hand2")
            btn.grid(row=row, column=col, padx=5, pady=2, sticky=stick)
            btn.bind("<Button-1>", lambda e, c=cmd: c())
            self._add_hover(btn)

    def _add_hover(self, widget):
        widget.bind("<Enter>", lambda e: widget.config(fg=StockStyle.HOVER_GREY))
        widget.bind("<Leave>", lambda e: widget.config(fg=StockStyle.PRIMARY_GREY))

    def manual_update(self, event=None):
        # 檢查設定是否有變動
        old_config = self.data_manager.config_data.copy()
        self.data_manager.config_data = self.data_manager.load_config()
        if self.data_manager.config_data != old_config:
            self._build_ui()
            
        for _, curr, canvas, _ in self.labels.values():
            if curr.winfo_exists():
                curr.config(text="...")
                canvas.delete("all")
        self.refresh_prices()

    def refresh_prices(self):
        if self._update_job: self.after_cancel(self._update_job)
        # 每次刷新前重新讀取設定，確保手動修改 JSON 也能即時反應
        self.data_manager.config_data = self.data_manager.load_config()
        self.data_manager.fetch_prices(self._on_fetch_done)

    def _on_fetch_done(self, result):
        # 切換到主執行緒執行 UI 更新
        self.after(0, lambda: self._do_apply_updates(result))

    def _do_apply_updates(self, result):
        if self.is_collapsed or not result: return
        
        updates = result.get("updates", {})
        alerts = result.get("alerts", [])
        
        for sym, (prev, curr, high, low, hint) in updates.items():

            if sym not in self.labels: continue
            lbl_prev, lbl_curr, canvas, lbl_diff = self.labels[sym]
            if not lbl_curr.winfo_exists(): continue

            # 更新文字
            lbl_prev.config(text=f"{prev:.2f}")
            lbl_curr.config(text=f"{curr:.{hint}f}")
            diff_pct = (curr - prev) / prev * 100 if prev > 0 else 0
            lbl_diff.config(text=f"{diff_pct:+.2f}%")

            # 繪製圖形
            self._draw_status_bar(canvas, prev, curr, high, low)
            
        # 處理警報 (即使 alerts 為空也要傳送，用來清除 UI 警示圖示)
        if self.on_alert is not None:
            self.on_alert(alerts)

            
        # 循環更新

        self._update_job = self.after(self.update_interval_ms, self.refresh_prices)

    def _draw_status_bar(self, canvas, prev, curr, high, low):
        canvas.delete("all")
        w, h = int(canvas.cget("width")), int(canvas.cget("height"))
        
        # 置中計算
        v_low, v_high = min(low, prev), max(high, prev)
        v_range = v_high - v_low
        v_range_pct = (v_range / prev * 100.0) if prev > 0 else 0
        
        scale = min(1.0, (v_range_pct / 10.0) ** 0.7) if v_range_pct > 0 else 0.05
        uw = (w - 12) * scale
        if uw < 10: uw = 10
        start_x = (w - uw) / 2
        
        def get_x(v):
            return start_x + (v - v_low) / (v_high - v_low) * uw if v_high > v_low else w/2

        xl, xh, xp, xc = get_x(low), get_x(high), get_x(prev), get_x(curr)
        canvas.stock_coords = {'low': low, 'high': high, 'x_low': xl, 'x_high': xh}

        # 軌道
        canvas.create_line(xl, h/2, xh, h/2, fill=StockStyle.BAR_TRACK, width=4, capstyle=tk.ROUND)
        # 端點
        for x in (xl, xh): canvas.create_oval(x-2, h/2-2, x+2, h/2+2, fill="#eeeeee", outline="")
        # 昨收線：改為寬度 1 並使用虛線，減少視覺重量
        canvas.create_line(xp, 4, xp, h-4, fill=StockStyle.BAR_GUIDE, width=1, dash=(2, 2))
        
        # 指示器：縮小尺寸並加入淺色填充，改善重疊感
        if curr != prev:
            # 寬度從 9 改為 7, 高度從 10 改為 8
            points = [xc+4, h/2, xc-3, h/2-4, xc-3, h/2+4] if curr > prev else [xc-4, h/2, xc+3, h/2-4, xc+3, h/2+4]
            canvas.create_polygon(points, fill="#f0f0f0", outline=StockStyle.PRIMARY_GREY, width=1)
        else:
            canvas.create_oval(xc-3, h/2-3, xc+3, h/2+3, fill="#f0f0f0", outline=StockStyle.PRIMARY_GREY, width=1)

    def _on_bar_click(self, event, canvas):
        if hasattr(canvas, "stock_coords"):
            coords = canvas.stock_coords
            # 改為判斷距離點擊位置最近的座標 (L 或 H)
            dist_l = abs(event.x - coords['x_low'])
            dist_h = abs(event.x - coords['x_high'])
            
            if dist_l < dist_h:
                self._show_temp_val(canvas, f"L:{coords['low']:.2f}", coords['x_low'])
            else:
                self._show_temp_val(canvas, f"H:{coords['high']:.2f}", coords['x_high'])
            return

    def _show_temp_val(self, canvas, text, x):
        self._hide_temp_val(canvas) # 先清除舊的
        
        # 顯示數值，座標上移一點預留間距
        canvas.create_text(x, 6, text=text, fill=StockStyle.TEXT_POPUP, font=StockStyle.FONT_BOLD, tags="temp_val")
        
        # 設定自動消失計時器
        timer_id = self.after(3000, lambda: self._hide_temp_val(canvas))
        canvas.hide_timer = timer_id

    def _hide_temp_val(self, canvas):
        """隱藏暫時顯示的數值並取消計時器"""
        canvas.delete("temp_val")
        if hasattr(canvas, "hide_timer") and canvas.hide_timer:
            self.after_cancel(canvas.hide_timer)
            canvas.hide_timer = None

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
        w, h = 260, 220
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
        tk.Label(fm2, text="長線目標價/百分比(vs基準):", font=("Arial", 8, "italic")).grid(row=0, column=0, columnspan=2, pady=(0,5))
        
        tk.Label(fm2, text="目標價格:").grid(row=1, column=0, sticky="e")
        e_target_p = tk.Entry(fm2, width=12); e_target_p.grid(row=1, column=1)
        
        tk.Label(fm2, text="變動比例(%):").grid(row=2, column=0, sticky="e")
        e_target_pct = tk.Entry(fm2, width=12); e_target_pct.grid(row=2, column=1)
        
        # 初始填充長線數值
        curr_long_th = stock_cfg.get('alert_long', self.data_manager.config_data.get('alert_threshold_long', 15.0))
        e_target_pct.insert(0, str(curr_long_th))
        try:
            target_p = current_ref * (1 + curr_long_th/100.0)
            e_target_p.insert(0, f"{target_p:.2f}")
        except: pass

        def sync_p_to_pct(ev=None):
            try:
                ref = float(e_ref.get())
                p = float(e_target_p.get())
                pct = abs((p - ref) / ref * 100)
                e_target_pct.delete(0, tk.END); e_target_pct.insert(0, f"{pct:.2f}")
            except: pass

        def sync_pct_to_p(ev=None):
            try:
                ref = float(e_ref.get())
                pct = float(e_target_pct.get())
                p = ref * (1 + pct / 100.0) # 預設顯示正向目標價
                e_target_p.delete(0, tk.END); e_target_p.insert(0, f"{p:.2f}")
            except: pass

        e_target_p.bind("<KeyRelease>", sync_p_to_pct)
        e_target_pct.bind("<KeyRelease>", sync_pct_to_p)

        def save():
            try:
                params = {
                    "reference": float(e_ref.get()),
                    "alert_short": float(e_short.get()) if e_short.get() else 5.0,
                    "alert_long": float(e_target_pct.get()) if e_target_pct.get() else 15.0
                }
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

        # 置中於螢幕 - 調大高度以容納路徑資訊
        w, h = 260, 320
        sw = dialog.winfo_screenwidth()
        sh = dialog.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        dialog.geometry(f"{w}x{h}+{x}+{y}")
        dialog.attributes("-topmost", True)

        
        bg = self.cget("bg")
        tk.Label(dialog, text="全局預設參數", font=StockStyle.FONT_BOLD).pack(pady=10)
        
        fm = tk.Frame(dialog); fm.pack(padx=20)
        cfg = self.data_manager.config_data
        
        tk.Label(fm, text="預設短預警(%):").grid(row=0, column=0, sticky="e", pady=2)
        e_s = tk.Entry(fm, width=8); e_s.insert(0, str(cfg.get('alert_threshold_short', 5.0))); e_s.grid(row=0, column=1)
        
        tk.Label(fm, text="預設長預警(%):").grid(row=1, column=0, sticky="e", pady=2)
        e_l = tk.Entry(fm, width=8); e_l.insert(0, str(cfg.get('alert_threshold_long', 15.0))); e_l.grid(row=1, column=1)
        
        tk.Label(fm, text="顏色強度(0-2):").grid(row=2, column=0, sticky="e", pady=2)
        e_i = tk.Entry(fm, width=8); e_i.insert(0, str(cfg.get('color_intensity', 1.0))); e_i.grid(row=2, column=1)

        def save():
            try:
                new_cfg = {
                    "alert_threshold_short": float(e_s.get()),
                    "alert_threshold_long": float(e_l.get()),
                    "color_intensity": float(e_i.get())
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
