"""
Todo List 應用程式 - 主程式
版本: v1.0.3
建立日期: 2024-01-XX
更新: 
  - v1.0.1: 調整視窗大小以容納今日任務顯示
  - v1.0.2: 新增完成/未完成切換功能
  - v1.0.3: 新增任務時使用選中的日期作為預設值
"""

import tkinter as tk
from tkinter import messagebox
from models import Todo
from data_manager import load_todos, save_todos
from calendar_view import CalendarView
from todo_list_view import TodoListView
from todo_editor import TodoEditor


class TodoApp:
    """Todo List 應用程式主類別"""
    
    def __init__(self, root):
        """
        初始化應用程式
        
        Args:
            root: Tkinter 根視窗
        """
        self.root = root
        self.root.title("Todo List 月曆應用程式")
        self.root.geometry("900x700")
        
        # 載入資料
        self.todos = load_todos()
        
        # 當前視圖狀態
        self.current_view = "calendar"  # "calendar" 或 "todo_list"
        self.selected_date = None
        
        # 建立主容器
        self.main_container = tk.Frame(root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # 初始化視圖
        self.calendar_view = None
        self.todo_list_view = None
        
        # 顯示月曆視圖
        self.show_calendar_view()
    
    def show_calendar_view(self):
        """顯示月曆視圖"""
        # 清除當前視圖
        self._clear_view()
        
        # 建立月曆視圖
        self.calendar_view = CalendarView(
            self.main_container,
            self.todos,
            on_date_click=self._on_date_click
        )
        self.calendar_view.get_frame().pack(fill=tk.BOTH, expand=True)
        
        self.current_view = "calendar"
        self.selected_date = None
    
    def show_todo_list_view(self, date: str = None):
        """顯示 Todo 列表視圖"""
        # 清除當前視圖
        self._clear_view()
        
        # 建立 Todo 列表視圖
        self.todo_list_view = TodoListView(
            self.main_container,
            self.todos,
            on_add=self._on_add_todo,
            on_edit=self._on_edit_todo,
            on_delete=self._on_delete_todo,
            on_toggle_complete=self._on_toggle_complete,
            on_back=self.show_calendar_view,
            selected_date=date
        )
        self.todo_list_view.get_frame().pack(fill=tk.BOTH, expand=True)
        
        self.current_view = "todo_list"
        self.selected_date = date
    
    def _clear_view(self):
        """清除當前視圖"""
        for widget in self.main_container.winfo_children():
            widget.destroy()
        self.calendar_view = None
        self.todo_list_view = None
    
    def _on_date_click(self, date: str):
        """處理日期點擊事件"""
        self.show_todo_list_view(date)
    
    def _on_add_todo(self, default_date: str = None):
        """處理新增 todo 事件"""
        editor = TodoEditor(self.root, default_date=default_date)
        new_todo = editor.show()
        
        if new_todo:
            self.todos.append(new_todo)
            self._save_and_refresh()
    
    def _on_edit_todo(self, todo: Todo):
        """處理編輯 todo 事件"""
        editor = TodoEditor(self.root, todo)
        edited_todo = editor.show()
        
        if edited_todo:
            # todo 物件已經被編輯器直接修改，只需要刷新
            self._save_and_refresh()
    
    def _on_delete_todo(self, todo: Todo):
        """處理刪除 todo 事件"""
        result = messagebox.askyesno(
            "確認刪除",
            f"確定要刪除任務「{todo.title}」嗎？",
            parent=self.root
        )
        
        if result:
            self.todos.remove(todo)
            self._save_and_refresh()
    
    def _on_toggle_complete(self, todo: Todo):
        """處理切換完成狀態事件"""
        self._save_and_refresh()
    
    def _save_and_refresh(self):
        """儲存資料並刷新視圖"""
        # 儲存到檔案
        save_todos(self.todos)
        
        # 刷新當前視圖
        if self.current_view == "calendar":
            if self.calendar_view:
                self.calendar_view.update_todos(self.todos)
        elif self.current_view == "todo_list":
            if self.todo_list_view:
                self.todo_list_view.update_todos(self.todos, self.selected_date)
    
    def on_closing(self):
        """處理視窗關閉事件"""
        # 儲存資料
        save_todos(self.todos)
        self.root.destroy()


def main():
    """主函數"""
    root = tk.Tk()
    app = TodoApp(root)
    
    # 設定關閉事件處理
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # 啟動主迴圈
    root.mainloop()


if __name__ == "__main__":
    main()


