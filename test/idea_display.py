import tkinter as tk

class PixelArtDisplay(tk.Frame):
    def __init__(self, parent, pixel_size=10, bg_color="#1e1e1e", *args, **kwargs):
        super().__init__(parent, bg=bg_color, *args, **kwargs)
        self.pixel_size = pixel_size
        self.canvas = tk.Canvas(self, bg=bg_color, highlightthickness=0)
        self.canvas.pack(padx=10, pady=10)

    def draw(self, matrix):
        self.canvas.delete("all")
        if not matrix or not matrix[0]: return
        
        rows = len(matrix)
        cols = max(len(row) for row in matrix)
        self.canvas.config(width=cols * self.pixel_size, height=rows * self.pixel_size)
        
        for r in range(rows):
            for c in range(cols):
                color = matrix[r][c] if c < len(matrix[r]) else ""
                if color:
                    x = c * self.pixel_size
                    y = r * self.pixel_size
                    self.canvas.create_rectangle(x, y, x + self.pixel_size, y + self.pixel_size, fill=color, outline=color)

# --- 顏色定義 ---
_ = ""           # 透明/背景
K = "#000000"    # 黑
W = "#FFFFFF"    # 白
G = "#A0A0A0"    # 灰
LG = "#D0D0D0"   # 淺灰
DG = "#505050"   # 暗灰


# --- 1. 沙漏 (Hourglass) 16x16 ---
hourglass = [
    [_, _, _, _, K, K, K, K, K, K, K, K, _, _, _, _],
    [_, _, _, _, K, W, W, W, W, W, W, K, _, _, _, _],
    [_, _, _, _, K, W, G, G, G, G, W, K, _, _, _, _],
    [_, _, _, _, K, W, G, G, G, G, W, K, _, _, _, _],
    [_, _, _, _, K, K, W, G, G, W, K, K, _, _, _, _],
    [_, _, _, _, _, K, K, W, W, K, K, _, _, _, _, _],
    [_, _, _, _, _, _, K, W, W, K, _, _, _, _, _, _],
    [_, _, _, _, _, _, K, G, G, K, _, _, _, _, _, _],
    [_, _, _, _, _, K, K, W, G, K, K, _, _, _, _, _],
    [_, _, _, _, K, K, W, _, G, W, K, K, _, _, _, _],
    [_, _, _, _, K, W, G, _, _, G, W, K, _, _, _, _],
    [_, _, _, _, K, W, G, G, G, G, W, K, _, _, _, _],
    [_, _, _, _, K, W, W, W, W, W, W, K, _, _, _, _],
    [_, _, _, _, K, K, K, K, K, K, K, K, _, _, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _]
]

# --- 2. 釣魚 (Fishing) 16x16 ---
fishing = [
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, K],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, K, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, K, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, K, _, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, K, _, _, _, _],
    [_, _, _, _, DG, DG, DG, _, _, _, K, _, _, _, _, _],
    [_, _, _, DG, DG, W, K, _, _, K, _, _, _, _, _, _],
    [_, _, _, DG, G, G, G, _, K, _, _, _, _, _, _, _],
    [_, _, _, _, G, G, G, K, _, _, _, _, _, _, _, _],
    [_, _, _, _, K, K, K, K, _, _, _, _, _, _, _, DG],
    [_, _, _, K, K, _, K, K, _, _, _, _, _, _, DG, _],
    [LG, LG, LG, LG, LG, LG, LG, LG, LG, LG, LG, LG, LG, DG, LG, LG],
    [DG, LG, DG, LG, DG, LG, DG, LG, DG, LG, DG, LG, DG, LG, DG, LG],
    [LG, DG, LG, DG, LG, DG, LG, DG, LG, DG, LG, DG, LG, DG, LG, DG],
    [DG, LG, DG, LG, DG, LG, DG, LG, DG, LG, DG, LG, DG, LG, DG, LG],
    [DG, DG, DG, DG, DG, DG, DG, DG, DG, DG, DG, DG, DG, DG, DG, DG]
]

# --- 3. 讀書 (Reading) 16x16 ---
reading = [
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, K, K, K, K, _, _, _, _, _, _, _],
    [_, _, _, _, K, W, W, W, K, _, _, _, _, _, _],
    [_, _, _, K, W, K, W, K, W, K, _, _, _, _, _],
    [_, _, _, K, W, W, W, W, W, K, _, _, _, _, _],
    [_, _, _, _, K, W, W, W, K, _, _, _, _, _, _],
    [_, _, _, _, _, K, G, G, K, _, _, _, _, _, _],
    [_, _, _, _, K, G, G, G, G, K, _, _, _, _, _],
    [_, _, _, K, W, K, G, G, K, W, K, _, _, _, _],
    [_, _, _, K, W, W, K, K, W, W, K, _, _, _, _],
    [_, _, _, _, K, W, W, W, W, K, _, _, _, _, _],
    [_, _, _, K, W, K, W, W, K, W, K, _, _, _, _],
    [_, _, _, K, W, W, K, K, W, W, K, _, _, _, _],
    [_, _, _, _, K, K, _, _, K, K, _, _, _, _, _],
    [_, _, _, _, K, DG, _, _, DG, K, _, _, _, _, _],
    [_, _, _, _, K, DG, _, _, DG, K, _, _, _, _, _]
]

# --- 4. 下雨 (Raining) 16x16 ---
raining = [
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, G, G, G, G, _, _, _, _, _, _, _],
    [_, _, _, G, G, G, W, G, G, G, _, _, _, _, _, _],
    [_, _, G, G, W, G, G, G, W, G, G, _, _, _, _, _],
    [_, G, G, G, G, G, W, G, G, W, G, G, _, _, _, _],
    [G, G, W, G, G, G, G, G, G, G, G, G, G, _, _, _],
    [G, G, G, G, G, W, G, G, W, G, G, G, G, _, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    [_, _, G, _, _, _, _, G, _, _, _, _, G, _, _, _],
    [_, G, _, _, _, G, _, _, _, _, G, _, _, _, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    [_, _, _, G, _, _, _, _, G, _, _, _, _, _, _, _],
    [_, G, _, _, _, _, G, _, _, _, _, G, _, _, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    [DG, LG, DG, LG, DG, LG, DG, LG, DG, LG, DG, LG, DG, LG, DG, LG],
    [DG, DG, DG, DG, DG, DG, DG, DG, DG, DG, DG, DG, DG, DG, DG, DG]
]

# --- 5. 管線漏水 (Pipe Leaking) 16x16 ---
pipe_leaking = [
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    [_, _, G, G, G, G, G, G, G, G, G, G, G, _, _, _],
    [_, _, G, G, G, G, G, G, G, G, G, G, G, _, _, _],
    [_, _, G, G, G, DG, DG, DG, G, G, G, G, G, _, _, _],
    [_, _, _, _, _, DG, DG, DG, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, DG, G, DG, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, DG, DG, DG, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, G, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, G, _, G, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, G, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, G, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, G, W, G, _, _, _, _, _, _, _, _],
    [_, _, _, _, G, G, G, G, G, _, _, _, _, _, _, _],
    [_, _, _, G, G, G, W, G, G, G, _, _, _, _, _, _],
    [_, _, G, G, W, G, G, G, G, G, G, _, _, _, _, _]
]

# --- 6. 寫程式 (Coding) 16x16 ---
coding = [
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, K, K, K, K, _, _, _, _, _, _, _],
    [_, _, _, _, K, W, W, W, K, _, _, _, _, _, _],
    [_, _, _, K, W, K, W, K, W, K, _, _, _, _, _],
    [_, _, _, K, W, W, W, W, W, K, _, _, _, _, _],
    [_, _, _, _, K, W, W, W, K, _, _, _, _, _, _],
    [_, _, _, _, _, K, G, G, K, _, _, _, _, _, _, _],
    [_, _, _, _, K, G, G, G, G, K, _, _, _, _, _, _],
    [_, _, K, K, K, K, K, K, K, K, K, K, _, _, _, _],
    [_, _, K, DG, DG, DG, DG, DG, DG, DG, DG, K, _, _, _, _],
    [_, _, K, G, K, K, G, K, K, G, DG, K, _, _, _, _],
    [_, _, K, DG, DG, G, DG, DG, G, DG, DG, K, _, _, _, _],
    [_, _, K, K, K, K, K, K, K, K, K, K, _, _, _, _],
    [_, _, _, _, _, _, K, K, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, K, G, G, K, _, _, _, _, _, _, _],
    [_, _, _, _, _, K, K, K, K, _, _, _, _, _, _, _]
]

# --- 7. 發呆 (Spacing out) ... (Zzz) 16x16 ---
spacing_out = [
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, _, _, _, K, K, _, _, _, _, _],
    [_, _, _, _, _, _, _, _, _, _, K, _, _, _, _, _],
    [_, _, _, _, _, _, _, _, _, K, K, _, _, _, _, _],
    [_, _, _, _, _, _, _, K, K, K, _, _, _, _, _, _],
    [_, _, _, _, _, _, _, _, K, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, _, K, K, K, _, _, _, _, _, _],
    [_, _, _, _, _, _, K, K, K, K, _, _, _, _, _, _],
    [_, _, _, _, _, K, W, W, W, K, _, _, _, _, _],
    [_, _, _, _, K, W, K, W, K, W, K, _, _, _, _],
    [_, _, _, _, K, W, W, K, W, W, K, _, _, _, _],
    [_, _, _, _, _, K, W, W, W, K, _, _, _, _, _],
    [_, _, _, _, K, G, G, G, G, K, _, _, _, _],
    [_, _, _, _, K, G, G, G, G, K, _, _, _, _],
    [_, _, _, _, K, G, G, G, G, K, _, _, _, _]
]

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Pixel Art Ideas展示")
    root.configure(bg="#1e1e1e")
    
    # Grid佈局展示
    tk.Label(root, text="Pixel Art 靜態展示 (Idea預覽)", fg="white", bg="#1e1e1e", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=4, pady=10)
    
    items = [
        ("沙漏 Hourglass", hourglass),
        ("釣魚 Fishing", fishing),
        ("讀書 Reading", reading),
        ("寫程式 Coding", coding),
        ("下雨 Raining", raining),
        ("漏水 Pip Leaking", pipe_leaking),
        ("發呆 Spacing Out", spacing_out),
    ]
    
    for i, (name, matrix) in enumerate(items):
        r = (i // 4) * 2 + 1
        c = i % 4
        
        frame = tk.Frame(root, bg="#1e1e1e")
        frame.grid(row=r+1, column=c, padx=15, pady=15)
        
        tk.Label(root, text=name, fg="#b0b0b0", bg="#1e1e1e", font=("Arial", 10)).grid(row=r, column=c)
        pad = PixelArtDisplay(frame, pixel_size=8)
        pad.pack()
        pad.draw(matrix)
        
    root.mainloop()

