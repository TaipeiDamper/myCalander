import tkinter as tk
from tkinter import ttk, messagebox
import time

class ClockPomodoroWidget(tk.Frame):
    def __init__(self, parent, on_activate=None):
        # 繼承父容器背景
        super().__init__(parent, bg=parent.cget("bg"))
        self.on_activate = on_activate
        
        # 狀態變數
        self.is_running = False
        self.work_mins = 25
        self.break_mins = 5
        self.time_left = self.work_mins * 60
        self.mode = "work" # "work" 或 "break"
        
        self._build_ui()
        
    def _build_ui(self):
        for w in self.winfo_children(): w.destroy()
        
        # 直接進入番茄鐘控制區 (移除重複時鐘)
        pomo_frame = tk.Frame(self, bg="#ffffff", padx=5, pady=5)
        pomo_frame.pack(fill=tk.X)
        
        self.pomo_status_lbl = tk.Label(
            pomo_frame, text=f"模式: {self.mode.upper()}", font=("Arial", 9, "bold"),
            fg="#d32f2f" if self.mode == "work" else "#388e3c", bg="#ffffff"
        )
        self.pomo_status_lbl.pack()
        
        self.pomo_timer_lbl = tk.Label(
            pomo_frame, text=self._get_timer_str(), font=("Courier", 24, "bold"),
            fg="#333333", bg="#ffffff"
        )
        self.pomo_timer_lbl.pack(pady=5)
        
        btn_frame = tk.Frame(pomo_frame, bg="#ffffff")
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="▶/⏸", command=self.toggle_timer, width=5).pack(side="left", padx=2)
        tk.Button(btn_frame, text="↺", command=self.reset_timer, width=3).pack(side="left", padx=2)
        tk.Button(btn_frame, text="⚙️", command=self._show_settings, width=3).pack(side="left", padx=2)
        
        mode_frame = tk.Frame(pomo_frame, bg="#ffffff")
        mode_frame.pack()
        tk.Button(mode_frame, text="工作", command=lambda: self.set_mode("work"), font=("Arial", 8)).pack(side="left", padx=2)
        tk.Button(mode_frame, text="休息", command=lambda: self.set_mode("break"), font=("Arial", 8)).pack(side="left", padx=2)

    def _get_timer_str(self):
        mins, secs = divmod(self.time_left, 60)
        return f"{mins:02d}:{secs:02d}"


    def toggle_timer(self):
        if self.on_activate: self.on_activate()
        if not self.is_running:
            self.is_running = True
            self._run_timer_logic()
        else:
            self.is_running = False

    def _run_timer_logic(self):
        if self.is_running and self.time_left > 0:
            self.time_left -= 1
            if self.pomo_timer_lbl.winfo_exists():
                self.pomo_timer_lbl.config(text=self._get_timer_str())
            self.after(1000, self._run_timer_logic)
        elif self.time_left <= 0:
            self.is_running = False
            messagebox.showinfo("Pomodoro", "時間到！")

    def set_mode(self, mode):
        self.mode = mode
        self.time_left = (self.work_mins if mode == "work" else self.break_mins) * 60
        self.is_running = False
        self._build_ui()

    def reset_timer(self):
        self.is_running = False
        self.set_mode(self.mode)

    def _show_settings(self):
        win = tk.Toplevel(self)
        win.title("Settings")
        win.geometry("200x120")
        win.attributes("-topmost", True)
        tk.Label(win, text="Work/Break Mins:").pack(pady=5)
        f = tk.Frame(win); f.pack()
        w_s = tk.Entry(f, width=5); w_s.insert(0, str(self.work_mins)); w_s.pack(side="left", padx=5)
        b_s = tk.Entry(f, width=5); b_s.insert(0, str(self.break_mins)); b_s.pack(side="left", padx=5)
        def save():
            try:
                self.work_mins, self.break_mins = int(w_s.get()), int(b_s.get())
                self.reset_timer(); win.destroy()
            except: pass
        tk.Button(win, text="Save", command=save, pady=5).pack(pady=10)
