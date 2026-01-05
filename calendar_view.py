"""
Todo List 應用程式 - 月曆視圖
版本: v1.0.3
建立日期: 2024-01-XX
更新: 
  - v1.0.1: 修正日期計算錯誤和版面對齊問題
  - v1.0.2: 週日移到最左側、日期加英文簡寫、顏色區分、今日任務顯示
  - v1.0.3: 移除日期格子中的英文縮寫，只保留標題；修正對齊問題
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from typing import List, Callable, Optional
from models import Todo


class CalendarView:
    """互動月曆視圖"""
    
    def __init__(self, parent, todos: List[Todo], on_date_click: Callable[[str], None]):
        """
        初始化月曆視圖
        
        Args:
            parent: 父容器
            todos: 所有 todo 列表
            on_date_click: 日期點擊回調函數，參數為日期字串 (YYYY-MM-DD)
        """
        self.parent = parent
        self.todos = todos
        self.on_date_click = on_date_click
        self.current_date = datetime.now()
        
        # 建立主框架
        self.frame = ttk.Frame(parent)
        
        # 建立月曆元件
        self._create_calendar()
    
    def _create_calendar(self):
        """建立月曆介面"""
        # 標題和導航按鈕
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(pady=10)
        
        prev_btn = ttk.Button(header_frame, text="◀", width=3, command=self._prev_month)
        prev_btn.pack(side=tk.LEFT, padx=5)
        
        self.month_label = ttk.Label(
            header_frame, 
            text=self._get_month_year_str(),
            font=("Arial", 14, "bold")
        )
        self.month_label.pack(side=tk.LEFT, padx=20)
        
        next_btn = ttk.Button(header_frame, text="▶", width=3, command=self._next_month)
        next_btn.pack(side=tk.LEFT, padx=5)
        
        # 星期標題（週日在最左側）- 使用 grid 以確保對齊
        weekdays_frame = ttk.Frame(self.frame)
        weekdays_frame.pack(pady=5)
        
        # 週日移到最左側：["日", "一", "二", "三", "四", "五", "六"]
        weekdays = ["日", "一", "二", "三", "四", "五", "六"]
        weekday_abbr = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
        for i, day in enumerate(weekdays):
            label_text = f"{day}\n{weekday_abbr[i]}"
            label = ttk.Label(weekdays_frame, text=label_text, anchor="center", font=("Arial", 9))
            label.grid(row=0, column=i, padx=2, sticky="nsew")
        
        # 設定星期標題欄位權重（與月曆網格一致，使用相同的 uniform 名稱）
        for i in range(7):
            weekdays_frame.columnconfigure(i, weight=1, uniform="calendar_col")
        
        # 月曆網格
        self.calendar_frame = ttk.Frame(self.frame)
        self.calendar_frame.pack(pady=10)
        
        # 今日任務區域
        self.today_tasks_frame = ttk.LabelFrame(self.frame, text="今日任務", padding=10)
        self.today_tasks_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self._update_calendar()
    
    def _get_month_year_str(self) -> str:
        """取得月份年份字串"""
        return self.current_date.strftime("%Y 年 %m 月")
    
    def _prev_month(self):
        """切換到上一個月"""
        if self.current_date.month == 1:
            self.current_date = self.current_date.replace(year=self.current_date.year - 1, month=12)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month - 1)
        self.month_label.config(text=self._get_month_year_str())
        self._update_calendar()
    
    def _next_month(self):
        """切換到下一個月"""
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(year=self.current_date.year + 1, month=1)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month + 1)
        self.month_label.config(text=self._get_month_year_str())
        self._update_calendar()
    
    def _update_calendar(self):
        """更新月曆顯示"""
        # 清除舊的按鈕
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()
        
        # 計算月份的第一天是星期幾
        # Python weekday(): Monday=0, Tuesday=1, ..., Sunday=6
        # 現在週日在最左側，所以：Sunday=6 -> 0, Monday=0 -> 1, ..., Saturday=5 -> 6
        first_day = self.current_date.replace(day=1)
        weekday_python = first_day.weekday()  # Monday=0, Sunday=6
        # 轉換為週日=0的格式：Sunday(6) -> 0, Monday(0) -> 1, ..., Saturday(5) -> 6
        weekday = (weekday_python + 1) % 7
        
        # 計算月份有多少天
        if self.current_date.month == 12:
            next_month = self.current_date.replace(year=self.current_date.year + 1, month=1, day=1)
        else:
            next_month = self.current_date.replace(month=self.current_date.month + 1, day=1)
        days_in_month = (next_month - timedelta(days=1)).day
        
        # 取得今天的日期
        today = datetime.now()
        today_str = today.strftime("%Y-%m-%d")
        
        # 建立日期按鈕
        row = 0
        col = 0
        
        # 填充前面的空白（從第一列開始）
        for _ in range(weekday):
            empty_label = ttk.Label(self.calendar_frame, text="", width=12)
            empty_label.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            col += 1
        
        # 建立日期按鈕
        for day in range(1, days_in_month + 1):
            date_obj = first_day.replace(day=day)
            date_str = date_obj.strftime("%Y-%m-%d")
            
            # 檢查這一天是否有 todo
            day_todos = [t for t in self.todos if t.date == date_str and not t.completed]
            
            # 判斷是否為今天
            is_today = (self.current_date.year == today.year and 
                       self.current_date.month == today.month and 
                       day == today.day)
            
            # 建立按鈕文字（只顯示日期數字，不顯示英文縮寫）
            if day_todos:
                # 有 todo 的日期
                btn_text = f"{day}\n{day_todos[0].title[:6]}"
                if len(day_todos) > 1:
                    btn_text += f"\n(+{len(day_todos)-1})"
            else:
                # 沒有 todo 的日期
                btn_text = str(day)
            
            # 建立按鈕
            btn = tk.Button(
                self.calendar_frame,
                text=btn_text,
                height=4,
                command=lambda d=date_str: self.on_date_click(d),
                relief=tk.RAISED,
                anchor="center",
                font=("Arial", 10)
            )
            
            # 設定顏色
            if is_today:
                # 今天是特殊標註（邊框加粗 + 特殊顏色）
                btn.config(bg="#ffeb3b", fg="#000000", 
                          relief=tk.SOLID, borderwidth=3)
            elif day_todos:
                # 有任務的日期（淺藍色）
                btn.config(bg="#e3f2fd", fg="#000000")
            else:
                # 沒有任務的日期（白色/灰色）
                btn.config(bg="#f5f5f5", fg="#000000")
            
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            
            col += 1
            if col > 6:
                col = 0
                row += 1
        
        # 設定欄位權重，讓按鈕均勻分佈（與星期標題使用相同的 uniform 名稱以確保對齊）
        for i in range(7):
            self.calendar_frame.columnconfigure(i, weight=1, uniform="calendar_col")
        
        # 更新今日任務顯示
        self._update_today_tasks()
    
    def _update_today_tasks(self):
        """更新今日任務顯示"""
        # 清除舊的任務顯示
        for widget in self.today_tasks_frame.winfo_children():
            widget.destroy()
        
        # 取得今天的日期
        today = datetime.now()
        today_str = today.strftime("%Y-%m-%d")
        
        # 取得今日的任務
        today_todos = [t for t in self.todos if t.date == today_str and not t.completed]
        
        if not today_todos:
            # 沒有任務
            no_task_label = ttk.Label(
                self.today_tasks_frame, 
                text="今天沒有待完成的任務",
                foreground="gray"
            )
            no_task_label.pack(pady=10)
        else:
            # 排序任務（按時間）
            today_todos = sorted(today_todos)
            
            # 建立任務列表框架（含滾動條）
            list_frame = ttk.Frame(self.today_tasks_frame)
            list_frame.pack(fill=tk.BOTH, expand=True)
            
            # 滾動條
            scrollbar = ttk.Scrollbar(list_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # 任務列表
            task_listbox = tk.Listbox(
                list_frame,
                yscrollcommand=scrollbar.set,
                font=("Arial", 10),
                selectmode=tk.SINGLE
            )
            task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.config(command=task_listbox.yview)
            
            # 加入任務到列表
            for todo in today_todos:
                time_str = todo.time if todo.time else "全天"
                task_text = f"[{time_str}] {todo.title}"
                if todo.content:
                    task_text += f" - {todo.content[:30]}"
                task_listbox.insert(tk.END, task_text)
    
    def update_todos(self, todos: List[Todo]):
        """更新 todo 列表並刷新月曆"""
        self.todos = todos
        self._update_calendar()
    
    def get_frame(self) -> ttk.Frame:
        """取得框架元件"""
        return self.frame


