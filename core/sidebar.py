import tkinter as tk

class AppSidebar(tk.Toplevel):
    def __init__(self, parent, width=240):
        super().__init__(parent)
        self.parent = parent
        self.width = width
        
        # 1. 基礎設定
        self.withdraw() # 初始隱藏
        self.overrideredirect(True) # 移除邊框
        self.config(bg="#f8f9fa", bd=1, relief=tk.SOLID)
        
        # 2. 標題列 (含標題與關閉按鈕)
        header_frame = tk.Frame(self, bg="#ececec")
        header_frame.pack(fill=tk.X)
        
        tk.Label(
            header_frame, text="擴 展 側 邊 欄", font=("Microsoft JhengHei", 10, "bold"), 
            bg="#ececec", fg="#333333", pady=8
        ).pack(side=tk.LEFT, padx=10)
        
        close_btn = tk.Label(
            header_frame, text="×", font=("Arial", 14, "bold"), 
            bg="#ececec", fg="#666666", cursor="hand2", padx=10
        )
        close_btn.pack(side=tk.RIGHT)
        close_btn.bind("<Button-1>", lambda e: self.close_sidebar())
        
        # 3. 滾動容器
        self.canvas = tk.Canvas(self, bg="#f8f9fa", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f8f9fa")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=self.width-20)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True, padx=(5,0))
        self.scrollbar.pack(side="right", fill="y")

        # 4. 狀態管理
        self.widget_configs = {} 
        self.ordered_names = ["番茄鐘控制", "詳細天氣", "系統設定"]
        self.active_count = 0

        # === 同步邏輯 (關鍵修正) ===
        # 使用 update_idletasks 確保座標計算準確
        self.parent.bind("<Configure>", self._sync_position)
        
        # 處理層級：當主視窗被點擊時，確保側邊欄浮上來
        self.parent.bind("<FocusIn>", lambda e: self.lift() if self.active_count > 0 else None)
        
        # 監聽最小化與恢復
        self.parent.bind("<Unmap>", lambda e: self.withdraw())
        self.parent.bind("<Map>", self._on_parent_map)

    def _sync_position(self, event=None):
        """磁吸式同步：精準對齊主視窗右緣 (防閃爍增強版)"""
        # 如果事件是由側邊欄內部的元件觸發的，忽略它
        if event and event.widget != self.parent:
            return
            
        if self.active_count > 0:
            if self.parent.state() == "normal":
                # 使用 debounce 避免短時間內多次更新
                if hasattr(self, "_sync_after_id") and self._sync_after_id:
                    self.after_cancel(self._sync_after_id)
                self._sync_after_id = self.after(10, self._do_sync)
            else:
                if self.state() == "normal":
                    self.withdraw()

    def _do_sync(self):
        self._sync_after_id = None
        if self.parent.state() != "normal": return
        
        # 取得目標座標與尺寸
        try:
            px = self.parent.winfo_rootx()
            py = self.parent.winfo_rooty()
            pw = self.parent.winfo_width()
            ph = self.parent.winfo_height()
            
            new_geo = f"{self.width}x{ph}+{px + pw}+{py}"
            
            # 只有當幾何狀態真的改變時才更新
            if self.wm_geometry() != new_geo:
                self.geometry(new_geo)
            
            if self.state() != "normal":
                self.deiconify()
                self.lift()
        except tk.TclError:
            pass # 處理視窗銷毀時的異常

    def _on_parent_map(self, event=None):
        if self.active_count > 0:
            # 延遲一點點確保主視窗位置已回歸
            self.after(200, self._sync_position)

    def close_sidebar(self):
        """一鍵關閉：將所有小工具設為不啟用並隱藏"""
        for cfg in self.widget_configs.values():
            cfg['active'] = False
        self._refresh_layout()

    def register_widget(self, name, widget_class):
        container = tk.LabelFrame(
            self.scrollable_frame, text=f" {name} ", 
            font=("Microsoft JhengHei", 9, "bold"), bg="#ffffff", 
            fg="#555555", relief=tk.FLAT, bd=0
        )
        tk.Frame(container, bg="#eeeeee", height=1).pack(fill=tk.X, side=tk.BOTTOM)
        
        widget = widget_class(container)
        widget.pack(fill=tk.X, padx=10, pady=10)
        
        self.widget_configs[name] = {
            'container': container,
            'active': False
        }
        return widget

    def toggle_widget(self, name):
        if name in self.widget_configs:
            cfg = self.widget_configs[name]
            cfg['active'] = not cfg['active']
            if cfg['active']: self.active_count += 1
            else: self.active_count -= 1
            self._refresh_layout()

    def _refresh_layout(self):
        any_visible = False
        for cfg in self.widget_configs.values():
            cfg['container'].pack_forget()
            
        for name in self.ordered_names:
            if name in self.widget_configs:
                cfg = self.widget_configs[name]
                if cfg['active']:
                    cfg['container'].pack(fill=tk.X, padx=10, pady=(5,15))
                    any_visible = True
        
        self.active_count = sum(1 for c in self.widget_configs.values() if c['active'])
        
        if any_visible:
            self._sync_position()
        else:
            self.withdraw()

    def show_only(self, name):
        if name in self.widget_configs:
            if not self.widget_configs[name]['active']:
                self.widget_configs[name]['active'] = True
                self._refresh_layout()
