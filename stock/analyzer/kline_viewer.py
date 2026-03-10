import tkinter as tk
from tkinter import ttk

class KLineViewer(tk.Frame):
    """
    K線與技術指標視覺化組件
    這是一個「兩棲組件」：
    1. 可以獨立運行作為數據研究工具
    2. 可以被插入到主程式的側邊欄中
    """
    def __init__(self, parent, **kwargs):
        # 繼承父容器樣式，若獨立運行則由 __main__ 提供 root
        super().__init__(parent, **kwargs)
        self.config(bg="white")
        
        self.data_source = None
        self._build_ui()

    def _build_ui(self):
        # --- UI 架構佈置 ---
        # 標題區
        header = tk.Frame(self, bg="#f5f5f5", height=30)
        header.pack(fill=tk.X)
        tk.Label(header, text="K線與指標分析區", font=("Arial", 9, "bold"), bg="#f5f5f5").pack(side=tk.LEFT, padx=5)
        
        # 繪圖/顯示主區
        self.canvas = tk.Canvas(self, bg="white", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # 暫時的說明文字 (之後換成繪圖邏輯)
        self.canvas.create_text(
            150, 100, 
            text="[K線圖開發預留區域]\n之後於此實作 K 線繪製或數值分析",
            font=("Arial", 9), fill="gray", justify="center"
        )
        
        # 底部控制/數值區
        footer = tk.Frame(self, bg="#eeeeee", height=25)
        footer.pack(fill=tk.X)
        self.info_lbl = tk.Label(footer, text="等待數據輸入...", font=("Arial", 8), bg="#eeeeee")
        self.info_lbl.pack(side=tk.LEFT, padx=5)

    def load_stock_data(self, stock_id, history_data):
        """
        對外接口：讓外部程式餵入數據
        stock_id: 個股代碼
        history_data: 歷史價格列表或 DataFrame
        """
        self.info_lbl.config(text=f"當前解析: {stock_id}")
        # 在這裡實作數據解析與繪圖
        pass

# --- 獨立工具入口 ---
if __name__ == "__main__":
    # 當獨立執行此檔案時，會啟動這個測試視窗
    root = tk.Tk()
    root.title("新工具獨立研發模式")
    root.geometry("400x500")
    
    # 模擬主程式的掛載動作
    test_viewer = KLineViewer(root)
    test_viewer.pack(fill=tk.BOTH, expand=True)
    
    # 模擬數據載入
    test_viewer.after(1000, lambda: test_viewer.load_stock_data("2330", []))
    
    root.mainloop()
