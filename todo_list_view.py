"""
Todo List 應用程式 - Todo 列表視圖
版本: v1.0.3
建立日期: 2024-01-XX
更新: 
  - v1.0.1: 移除拖曳功能，新增完成/未完成切換功能
  - v1.0.2: 完全移除拖曳相關程式碼和標示
  - v1.0.3: 新增任務時傳遞選中的日期作為預設值
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime
from typing import List, Callable, Optional
from models import Todo


class TodoListView:
    """Todo 列表視圖"""
    
    def __init__(self, parent, todos: List[Todo], 
                 on_add: Callable[[Optional[str]], None],
                 on_edit: Callable[[Todo], None],
                 on_delete: Callable[[Todo], None],
                 on_toggle_complete: Callable[[Todo], None],
                 on_back: Callable[[], None],
                 selected_date: Optional[str] = None):
        """
        初始化 Todo 列表視圖
        
        Args:
            parent: 父容器
            todos: 所有 todo 列表
            on_add: 新增 todo 回調，接受可選的日期參數
            on_edit: 編輯 todo 回調
            on_delete: 刪除 todo 回調
            on_back: 返回月曆回調
            selected_date: 選中的日期（如果為 None 則顯示所有未完成的 todo）
        """
        self.parent = parent
        self.todos = todos
        self.on_add = on_add
        self.on_edit = on_edit
        self.on_delete = on_delete
        self.on_toggle_complete = on_toggle_complete
        self.on_back = on_back
        self.selected_date = selected_date
        
        # 建立主框架
        self.frame = ttk.Frame(parent)
        
        # 建立介面
        self._create_ui()
    
    def _create_ui(self):
        """建立使用者介面"""
        # 標題和返回按鈕
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill=tk.X, pady=10, padx=10)
        
        back_btn = ttk.Button(header_frame, text="← 返回月曆", command=self.on_back)
        back_btn.pack(side=tk.LEFT)
        
        if self.selected_date:
            date_obj = datetime.strptime(self.selected_date, "%Y-%m-%d")
            title_text = f"{date_obj.strftime('%Y 年 %m 月 %d 日')} 的任務"
        else:
            title_text = "所有待完成任務"
        
        title_label = ttk.Label(header_frame, text=title_text, font=("Arial", 12, "bold"))
        title_label.pack(side=tk.LEFT, padx=20)
        
        # 新增按鈕（傳遞選中的日期）
        add_btn = ttk.Button(
            header_frame, 
            text="+ 新增任務", 
            command=lambda: self.on_add(self.selected_date) if self.selected_date else self.on_add()
        )
        add_btn.pack(side=tk.RIGHT)
        
        # 建立列表框架（包含滾動條）
        list_frame = ttk.Frame(self.frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 滾動條
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 列表框（使用 Canvas 實現滾動功能）
        self.canvas = tk.Canvas(list_frame, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.canvas.yview)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 內部框架（用於放置 todo 項目）
        self.inner_frame = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.inner_frame, anchor="nw"
        )
        
        # 綁定滾動事件
        self.inner_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
        # 更新列表
        self._update_list()
    
    def _on_frame_configure(self, event):
        """當內部框架大小改變時更新滾動區域"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def _on_canvas_configure(self, event):
        """當畫布大小改變時調整內部框架寬度"""
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)
    
    def _update_list(self):
        """更新 todo 列表顯示"""
        # 清除舊的項目
        for widget in self.inner_frame.winfo_children():
            widget.destroy()
        
        # 取得要顯示的 todos
        if self.selected_date:
            # 顯示選中日期的 todos（包含已完成和未完成）
            display_todos = [t for t in self.todos if t.date == self.selected_date]
        else:
            # 顯示所有未完成的 todos
            display_todos = [t for t in self.todos if not t.completed]
        
        # 排序：未完成的按時間排序（越接近完成時刻越前面），已完成的放在最後
        incomplete = [t for t in display_todos if not t.completed]
        completed = [t for t in display_todos if t.completed]
        incomplete = sorted(incomplete)
        completed = sorted(completed)
        display_todos = incomplete + completed
        
        # 建立 todo 項目
        for idx, todo in enumerate(display_todos):
            self._create_todo_item(todo, idx)
    
    def _create_todo_item(self, todo: Todo, index: int):
        """建立單個 todo 項目"""
        item_frame = ttk.Frame(self.inner_frame, relief=tk.RAISED, borderwidth=1)
        item_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 左側：完成狀態核取方塊
        complete_var = tk.BooleanVar(value=todo.completed)
        complete_checkbox = ttk.Checkbutton(
            item_frame,
            variable=complete_var,
            command=lambda t=todo, v=complete_var: self._on_toggle_complete(t, v)
        )
        complete_checkbox.pack(side=tk.LEFT, padx=5)
        
        # 中間：todo 資訊
        info_frame = ttk.Frame(item_frame)
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 標題（如果已完成，加上刪除線效果）
        title_text = todo.title
        if todo.completed:
            title_text = f"✓ {title_text}"
            title_label = ttk.Label(
                info_frame, 
                text=title_text, 
                font=("Arial", 10, "bold", "overstrike"),
                anchor="w",
                foreground="gray"
            )
        else:
            title_label = ttk.Label(
                info_frame, 
                text=title_text, 
                font=("Arial", 10, "bold"),
                anchor="w"
            )
        title_label.pack(fill=tk.X)
        
        # 內容（如果有）
        if todo.content:
            content_text = todo.content[:50] + ("..." if len(todo.content) > 50 else "")
            if todo.completed:
                content_label = ttk.Label(
                    info_frame, 
                    text=content_text,
                    anchor="w",
                    foreground="lightgray"
                )
            else:
                content_label = ttk.Label(
                    info_frame, 
                    text=content_text,
                    anchor="w",
                    foreground="gray"
                )
            content_label.pack(fill=tk.X)
        
        # 日期時間
        datetime_str = ""
        if todo.date:
            date_obj = datetime.strptime(todo.date, "%Y-%m-%d")
            datetime_str = date_obj.strftime("%Y-%m-%d")
            if todo.time:
                datetime_str += f" {todo.time}"
        
        if datetime_str:
            if todo.completed:
                datetime_label = ttk.Label(
                    info_frame, 
                    text=datetime_str,
                    anchor="w",
                    foreground="lightblue"
                )
            else:
                datetime_label = ttk.Label(
                    info_frame, 
                    text=datetime_str,
                    anchor="w",
                    foreground="blue"
                )
            datetime_label.pack(fill=tk.X)
        
        # 右側：操作按鈕
        button_frame = ttk.Frame(item_frame)
        button_frame.pack(side=tk.RIGHT, padx=5)
        
        edit_btn = ttk.Button(
            button_frame, 
            text="編輯", 
            width=8,
            command=lambda t=todo: self.on_edit(t)
        )
        edit_btn.pack(side=tk.LEFT, padx=2)
        
        delete_btn = ttk.Button(
            button_frame, 
            text="刪除", 
            width=8,
            command=lambda t=todo: self.on_delete(t)
        )
        delete_btn.pack(side=tk.LEFT, padx=2)
        
        # 雙擊編輯
        item_frame.bind("<Double-Button-1>", lambda e, t=todo: self.on_edit(t))
        for widget in [item_frame, info_frame, title_label]:
            widget.bind("<Double-Button-1>", lambda e, t=todo: self.on_edit(t))
    
    def _on_toggle_complete(self, todo: Todo, var: tk.BooleanVar):
        """切換完成狀態"""
        todo.completed = var.get()
        self.on_toggle_complete(todo)
    
    def update_todos(self, todos: List[Todo], selected_date: Optional[str] = None):
        """更新 todo 列表"""
        self.todos = todos
        if selected_date is not None:
            self.selected_date = selected_date
        self._update_list()
    
    def get_frame(self) -> ttk.Frame:
        """取得框架元件"""
        return self.frame


