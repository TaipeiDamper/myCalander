import tkinter as tk
from tkinter import ttk
from stock.analyzer.kline_viewer import KLineViewer

class StockNotificationSidebar(tk.Frame):
    def __init__(self, parent):
        # 繼承父容器樣式
        bg_color = parent.cget("bg")
        super().__init__(parent, bg=bg_color)
        
        self.is_visible = False
        self._build_ui()
        
    def _build_ui(self):
        # 標題
        title_lbl = tk.Label(
            self, text="投資資訊通知", font=("Arial", 10, "bold"),
            bg=self.cget("bg"), fg="#333333"
        )
        title_lbl.pack(fill=tk.X, pady=(0, 5))
        
        # 滾動區域容器
        self.container = tk.Frame(self, bg="white", highlightthickness=1, highlightbackground="#dddddd")
        self.container.pack(fill=tk.BOTH, expand=True)
        
        # 插入剛創立的「分析組件」
        self.kline_viewer = KLineViewer(self.container)
        self.kline_viewer.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 這裡之後會填入內容
        self.placeholder = tk.Label(
            self.container, text="[其他投資資訊通知區]",
            font=("Arial", 9), bg="white", fg="gray", pady=10
        )
        self.placeholder.pack(fill=tk.BOTH, expand=True)
        
        # 底部狀態 (可選)
        self.status_lbl = tk.Label(
            self, text="連線正常", font=("Arial", 8),
            bg=self.cget("bg"), fg="gray"
        )
        self.status_lbl.pack(fill=tk.X, pady=(5, 0))

    def update_info(self, alerts):
        """顯示預警項目"""
        # 清除舊內容 (保留 KLineViewer)
        for widget in self.container.winfo_children():
            if widget != self.kline_viewer:
                widget.destroy()
        
        if not alerts:
            tk.Label(self.container, text="[目前無預警項目]", font=("Arial", 9), bg="white", fg="gray", pady=10).pack(fill=tk.X)
            self.status_lbl.config(text="連線正常", fg="gray")
            return

        # 顯示警報項目
        for alert in alerts:
            icon = "🚨" if alert['type'] == "LONG" else "⚠️"
            text = f"{icon} {alert['symbol']}: 變動 {alert['value']:.1f}% ({alert['price']:.2f})"
            
            lbl = tk.Label(self.container, text=text, font=("微软雅黑", 9), bg="white", fg="#666666", anchor="w", padx=10, pady=5)
            lbl.pack(fill=tk.X)
        
        self.status_lbl.config(text=f"偵測到 {len(alerts)} 項異動", fg="#666666")


