"""
Todo List 應用程式 - Todo 編輯器
版本: v1.0.1
建立日期: 2024-01-XX
更新: 新增 default_date 參數，支援預設日期設定
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from core.models import Todo


class TodoEditor:
    """Todo 編輯對話框"""
    
    def __init__(self, parent, todo: Todo = None, default_date: str = None):
        """
        初始化編輯器
        
        Args:
            parent: 父視窗
            todo: 要編輯的 Todo 物件（如果為 None 則為新增模式）
            default_date: 新增模式時的預設日期（格式: YYYY-MM-DD），如果為 None 則使用今天
        """
        self.parent = parent
        self.todo = todo
        self.default_date = default_date
        self.result = None
        
        # 建立對話框
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("編輯任務" if todo else "新增任務")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # 設定對話框大小和位置
        self.dialog.geometry("400x520")
        self.dialog.resizable(False, False)
        
        # 居中顯示
        self._center_window()
        
        # 建立表單
        self._create_form()
        
        # 如果是編輯模式，填入現有資料
        if todo:
            self._load_todo_data()
    
    def _center_window(self):
        """將對話框置中顯示"""
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'{width}x{height}+{x}+{y}')
    
    def _create_form(self):
        """建立表單元件"""
        # 標題
        ttk.Label(self.dialog, text="標題（顯示在月曆上）:").grid(
            row=0, column=0, padx=10, pady=10, sticky="w"
        )
        self.title_entry = ttk.Entry(self.dialog, width=40)
        self.title_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # 內容
        ttk.Label(self.dialog, text="內容:").grid(
            row=1, column=0, padx=10, pady=10, sticky="nw"
        )
        self.content_text = tk.Text(self.dialog, width=40, height=8)
        self.content_text.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        # 日期
        ttk.Label(self.dialog, text="日期 (YYYY-MM-DD):").grid(
            row=2, column=0, padx=10, pady=10, sticky="w"
        )
        self.date_entry = ttk.Entry(self.dialog, width=40)
        self.date_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        # 預設日期：如果有 default_date 就用它，否則用今天
        if not self.todo:
            if self.default_date:
                self.date_entry.insert(0, self.default_date)
            else:
                self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # 時間
        ttk.Label(self.dialog, text="時間 (HH:MM):").grid(
            row=3, column=0, padx=10, pady=10, sticky="w"
        )
        self.time_entry = ttk.Entry(self.dialog, width=40)
        self.time_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
        # 預設為當前時間
        if not self.todo:
            self.time_entry.insert(0, datetime.now().strftime("%H:%M"))
        
        # 重要性
        ttk.Label(self.dialog, text="重要性 (1-10):").grid(
            row=4, column=0, padx=10, pady=10, sticky="w"
        )
        self.importance_scale = tk.Scale(self.dialog, from_=1, to=10, orient=tk.HORIZONTAL)
        self.importance_scale.set(5)
        self.importance_scale.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        # 時間相關性
        ttk.Label(self.dialog, text="時間相關性 (0-10):").grid(
            row=5, column=0, padx=10, pady=10, sticky="w"
        )
        self.time_sensitivity_scale = tk.Scale(self.dialog, from_=0, to=10, orient=tk.HORIZONTAL)
        self.time_sensitivity_scale.set(5)
        self.time_sensitivity_scale.grid(row=5, column=1, padx=10, pady=5, sticky="ew")
        
        # 完成狀態
        self.completed_var = tk.BooleanVar()
        self.completed_check = ttk.Checkbutton(self.dialog, text="已完成", variable=self.completed_var)
        self.completed_check.grid(row=6, column=1, padx=10, pady=10, sticky="w")

        # 按鈕框架
        button_frame = ttk.Frame(self.dialog)
        button_frame.grid(row=7, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="確定", command=self._on_ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消", command=self._on_cancel).pack(side=tk.LEFT, padx=5)
        
        # 設定欄位權重
        self.dialog.columnconfigure(1, weight=1)
        self.dialog.rowconfigure(1, weight=1)
    
    def _load_todo_data(self):
        """載入現有 todo 資料到表單"""
        if self.todo:
            self.title_entry.insert(0, self.todo.title)
            self.content_text.insert("1.0", self.todo.content)
            self.date_entry.insert(0, self.todo.date)
            self.time_entry.insert(0, self.todo.time)
            if hasattr(self.todo, 'importance'):
                self.importance_scale.set(self.todo.importance)
            if hasattr(self.todo, 'time_sensitivity'):
                self.time_sensitivity_scale.set(self.todo.time_sensitivity)
            self.completed_var.set(self.todo.completed)
    
    def _validate_input(self) -> bool:
        """驗證輸入"""
        title = self.title_entry.get().strip()
        date = self.date_entry.get().strip()
        time = self.time_entry.get().strip()
        
        if not title:
            messagebox.showerror("錯誤", "標題不能為空！")
            return False
        
        if date:
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("錯誤", "日期格式不正確！請使用 YYYY-MM-DD 格式。")
                return False
        
        if time:
            try:
                datetime.strptime(time, "%H:%M")
            except ValueError:
                messagebox.showerror("錯誤", "時間格式不正確！請使用 HH:MM 格式。")
                return False
        
        return True
    
    def _on_ok(self):
        """確定按鈕處理"""
        if not self._validate_input():
            return
        
        title = self.title_entry.get().strip()
        content = self.content_text.get("1.0", tk.END).strip()
        date = self.date_entry.get().strip()
        time = self.time_entry.get().strip()
        importance_val = int(self.importance_scale.get())
        time_sens_val = int(self.time_sensitivity_scale.get())
        completed_val = self.completed_var.get()
        
        if self.todo:
            # 編輯模式：更新現有 todo
            self.todo.title = title
            self.todo.content = content
            self.todo.date = date
            self.todo.time = time
            self.todo.importance = importance_val
            self.todo.time_sensitivity = time_sens_val
            self.todo.completed = completed_val
            self.result = self.todo
        else:
            # 新增模式：建立新 todo
            self.result = Todo(
                title=title,
                content=content,
                date=date,
                time=time,
                importance=importance_val,
                time_sensitivity=time_sens_val,
                completed=completed_val
            )
        
        self.dialog.destroy()
    
    def _on_cancel(self):
        """取消按鈕處理"""
        self.result = None
        self.dialog.destroy()
    
    def show(self) -> Todo:
        """
        顯示對話框並等待結果
        
        Returns:
            編輯後的 Todo 物件，如果取消則返回 None
        """
        self.dialog.wait_window()
        return self.result


