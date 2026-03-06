import tkinter as tk

class PixelArtWidget(tk.Frame):
    """
    用來顯示靜態與動態 Pixel Art 的測試元件。
    這是一個獨立的小工具，可以輕鬆嵌入原有的主應用程式 (如 Sidebar 或 Main Container 中)。
    完全獨立運行，不會影響原本的其他 widgets。
    """
    def __init__(self, parent, pixel_size=10, bg_color="#2c2c2c", *args, **kwargs):
        super().__init__(parent, bg=bg_color, *args, **kwargs)
        self.pixel_size = pixel_size
        self.bg_color = bg_color
        
        # 畫布用來繪製像素
        self.canvas = tk.Canvas(self, bg=self.bg_color, highlightthickness=0)
        self.canvas.pack(padx=5, pady=5)
        
        # 動畫相關屬性
        self.frames = []
        self.current_frame = 0
        self.animation_job = None
        self.frame_delay = 500  # 毫秒

    def set_static_image(self, pixel_matrix):
        """
        繪製靜態的 pixel art。
        pixel_matrix 是一個二維陣列（列表的列表），裡面包含顏色字串（如 "#FF0000" 或 "red"）。
        如果某個像素是透明的，可以使用 None 或者是空字串 ""。
        """
        self.stop_animation()
        self._draw_matrix(pixel_matrix)

    def set_animation(self, frames, delay=500):
        """
        播放動態 pixel art。
        frames 是包含多個 pixel_matrix 的列表。
        delay 是每張影格之間的毫秒延遲。
        """
        self.stop_animation()
        if not frames:
            return
            
        self.frames = frames
        self.frame_delay = delay
        self.current_frame = 0
        self._animate()

    def _draw_matrix(self, matrix):
        """內部方法：實際在畫布上繪製像素矩陣"""
        self.canvas.delete("all")
        if not matrix or not matrix[0]:
            return
            
        rows = len(matrix)
        cols = len(matrix[0])
        
        # 調整畫布大小以符合圖片
        canvas_width = cols * self.pixel_size
        canvas_height = rows * self.pixel_size
        self.canvas.config(width=canvas_width, height=canvas_height)
        
        for r in range(rows):
            for c in range(cols):
                color = matrix[r][c]
                if color:  # 只有在有顏色時才繪製 (如果是 None 或空字串則當透明背景)
                    x1 = c * self.pixel_size
                    y1 = r * self.pixel_size
                    x2 = x1 + self.pixel_size
                    y2 = y1 + self.pixel_size
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)

    def _animate(self):
        """內部方法：執行下一張影格，並排程下一次更新"""
        if not self.frames:
            return
            
        matrix = self.frames[self.current_frame]
        self._draw_matrix(matrix)
        
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.animation_job = self.after(self.frame_delay, self._animate)

    def stop_animation(self):
        """停止當前的動畫播放"""
        if self.animation_job is not None:
            self.after_cancel(self.animation_job)
            self.animation_job = None
            self.frames = []

if __name__ == "__main__":
    # 測試程式碼：這一段只有在單獨執行這個檔案時才會跑
    # 可以用來「確認可行性」，但這「不會干擾到原本的 main.py 與其他功能」
    
    root = tk.Tk()
    root.title("Pixel Art Widget 獨立測試")
    root.geometry("400x300")
    root.configure(bg="#1e1e1e")
    
    # 定義一些顏色
    W = "white"
    R = "red"
    B = "blue"
    Y = "yellow"
    _ = ""  # 透明 / 無色
    
    # 靜態圖：簡單的笑臉 (8x8)
    static_smiley = [
        [_, _, W, W, W, W, _, _],
        [_, W, _, _, _, _, W, _],
        [W, _, B, _, _, B, _, W],
        [W, _, _, _, _, _, _, W],
        [W, _, R, _, _, R, _, W],
        [W, _, _, R, R, _, _, W],
        [_, W, _, _, _, _, W, _],
        [_, _, W, W, W, W, _, _],
    ]
    
    # 動態圖：心跳效果
    heart_frame_1 = [
        [_, R, R, _, R, R, _],
        [R, R, R, R, R, R, R],
        [R, R, R, R, R, R, R],
        [_, R, R, R, R, R, _],
        [_, _, R, R, R, _, _],
        [_, _, _, R, _, _, _],
    ]
    
    heart_frame_2 = [
        [_, _, _, _, _, _, _],
        [_, _, R, _, R, _, _],
        [_, R, R, R, R, R, _],
        [_, _, R, R, R, _, _],
        [_, _, _, R, _, _, _],
        [_, _, _, _, _, _, _],
    ]

    # --- UI 佈列 ---
    title = tk.Label(root, text="像素藝術測試面板", fg="white", bg="#1e1e1e", font=("Arial", 14, "bold"))
    title.pack(pady=10)

    # 1. 靜態圖展示
    static_frame = tk.Frame(root, bg="#1e1e1e")
    static_frame.pack(side=tk.LEFT, padx=30)
    
    tk.Label(static_frame, text="靜態圖示 (Static)", fg="#b0b0b0", bg="#1e1e1e").pack()
    static_widget = PixelArtWidget(static_frame, pixel_size=12)
    static_widget.pack()
    static_widget.set_static_image(static_smiley)
    
    # 2. 動態圖展示
    anim_frame = tk.Frame(root, bg="#1e1e1e")
    anim_frame.pack(side=tk.RIGHT, padx=30)
    
    tk.Label(anim_frame, text="動態圖示 (Dynamic/Animation)", fg="#b0b0b0", bg="#1e1e1e").pack()
    anim_widget = PixelArtWidget(anim_frame, pixel_size=12)
    anim_widget.pack()
    anim_widget.set_animation([heart_frame_1, heart_frame_2], delay=400) # 每400ms切換一次
    
    root.mainloop()
