import tkinter as tk
from tkinter import messagebox
import time
from core.models import Todo
from core.data_manager import load_todos, save_todos
from todo.calendar_view import CalendarView
from todo.todo_list_view import TodoListView
from todo.todo_editor import TodoEditor
from stock.stock_widget import HiddenStockWidget
from weather.weather_widget import HiddenWeatherWidget
from core.clock_widget import ClockPomodoroWidget
from core.sidebar import AppSidebar

class TodoApp:
    """Todo List 應用程式主類別"""
    
class TodoApp:
    """Todo List 應用程式主類別"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Todo List 智能曆")
        self.root.geometry("900x700") # 固定主視窗尺寸，不變形
        
        # 載入資料
        self.todos = load_todos()
        
        # --- 佈局架構 ---
        # 1. 頂部導航
        self.header = tk.Frame(root)
        self.header.pack(fill=tk.X, padx=10, pady=5)
        
        # 2. 磁吸式側邊欄 (獨立懸浮擴展)
        self.sidebar = AppSidebar(root)
        
        # --- 主體導航列元件 ---
        # 天氣摘要 -> 點選切換側邊欄天氣
        self.weather_header = HiddenWeatherWidget(self.header, mode="header")
        self.weather_header.pack(side=tk.LEFT)
        self.weather_header.collapsed_lbl.bind("<Button-1>", lambda e: self.sidebar.toggle_widget("詳細天氣"))
        
        # 時鐘摘要 -> 點選切換側邊欄番茄鐘
        self.clock_lbl = tk.Label(self.header, text="00:00:00", font=("Courier", 14, "bold"), fg="#333333", cursor="hand2")
        self.clock_lbl.pack(side=tk.RIGHT)
        self.clock_lbl.bind("<Button-1>", lambda e: self.sidebar.toggle_widget("番茄鐘控制"))
        
        def update_header_clock():
            self.clock_lbl.config(text=time.strftime("%H:%M:%S"))
            self.root.after(1000, update_header_clock)
        update_header_clock()

        self.nav_frame = tk.Frame(self.header)
        self.nav_frame.pack(expand=True)
        
        # --- 中央主容器 ---
        self.main_container = tk.Frame(root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # 側邊欄功能註冊
        self.weather_sidebar = self.sidebar.register_widget("詳細天氣", lambda p: HiddenWeatherWidget(p, mode="sidebar"))
        self.pomo_widget = self.sidebar.register_widget("番茄鐘控制", lambda p: ClockPomodoroWidget(p, on_activate=lambda: self.sidebar.show_only("番茄鐘控制")))

        # 初始化視圖
        self.calendar_view = CalendarView(
            self.main_container,
            self.todos,
            on_date_click=self._on_date_click,
            external_nav_frame=self.nav_frame
        )
        self.calendar_view.get_frame().pack(fill=tk.BOTH, expand=True)
        
        self.current_view = "calendar"
        self.selected_date = None
        
        self.stock_widget = HiddenStockWidget(self.root)
        self.stock_widget.place(relx=0.99, rely=0.99, anchor="se")
        self.stock_widget.lift()
    
    def show_calendar_view(self):
        """顯示月曆視圖"""
        # 如果不是從列表切回月曆，一般是由此管理
        if self.current_view != "calendar":
            self._clear_view()
            self.calendar_view = CalendarView(
                self.main_container,
                self.todos,
                on_date_click=self._on_date_click,
                external_nav_frame=self.nav_frame
            )
            self.calendar_view.get_frame().pack(fill=tk.BOTH, expand=True)
            self.current_view = "calendar"
            self.selected_date = None
            
            # 回到月曆頁面時，顯示股票小工具
            self.stock_widget.place(relx=0.99, rely=0.99, anchor="se")
            self.stock_widget.lift()
    
    def show_todo_list_view(self, date: str = None):
        """顯示 Todo 列表視圖"""
        # 清除當前主視圖
        self._clear_view()
        
        # 清除頂部中央的月曆導航內容 (因為現在是列表模式)
        for widget in self.nav_frame.winfo_children():
            widget.destroy()
            
        # 進入任務選單時，隱藏右下角的股票小工具
        self.stock_widget.place_forget()
        
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


