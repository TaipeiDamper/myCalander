"""
Todo List 應用程式 - 月曆視圖
版本: v1.0.0
建立日期: 2024-01-XX
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
        
        # 星期標題
        weekdays_frame = ttk.Frame(self.frame)
        weekdays_frame.pack(pady=5)
        
        weekdays = ["一", "二", "三", "四", "五", "六", "日"]
        for day in weekdays:
            label = ttk.Label(weekdays_frame, text=day, width=10, anchor="center")
            label.pack(side=tk.LEFT, padx=2)
        
        # 月曆網格
        self.calendar_frame = ttk.Frame(self.frame)
        self.calendar_frame.pack(pady=10)
        
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
        
        # 計算月份的第一天是星期幾（一=0, 日=6）
        first_day = self.current_date.replace(day=1)
        weekday = (first_day.weekday() + 1) % 7  # 轉換為一=0, 日=6
        
        # 計算月份有多少天
        if self.current_date.month == 12:
            next_month = self.current_date.replace(year=self.current_date.year + 1, month=1, day=1)
        else:
            next_month = self.current_date.replace(month=self.current_date.month + 1, day=1)
        days_in_month = (next_month - timedelta(days=1)).day
        
        # 建立日期按鈕
        row = 0
        col = weekday
        
        # 填充前面的空白
        for _ in range(weekday):
            ttk.Label(self.calendar_frame, text="", width=10).grid(row=row, column=col, padx=2, pady=2)
            col += 1
        
        # 建立日期按鈕
        for day in range(1, days_in_month + 1):
            date_str = first_day.replace(day=day).strftime("%Y-%m-%d")
            
            # 檢查這一天是否有 todo
            day_todos = [t for t in self.todos if t.date == date_str and not t.completed]
            
            # 建立按鈕
            if day_todos:
                # 有 todo 的日期，顯示第一個 todo 的標題
                btn_text = f"{day}\n{day_todos[0].title[:8]}"
                if len(day_todos) > 1:
                    btn_text += f"\n(+{len(day_todos)-1})"
                btn = tk.Button(
                    self.calendar_frame,
                    text=btn_text,
                    width=10,
                    height=3,
                    command=lambda d=date_str: self.on_date_click(d),
                    bg="#e3f2fd",
                    relief=tk.RAISED
                )
            else:
                # 沒有 todo 的日期
                btn = tk.Button(
                    self.calendar_frame,
                    text=str(day),
                    width=10,
                    height=3,
                    command=lambda d=date_str: self.on_date_click(d),
                    relief=tk.RAISED
                )
            
            # 如果是今天，標記顏色
            today = datetime.now()
            if (self.current_date.year == today.year and 
                self.current_date.month == today.month and 
                day == today.day):
                btn.config(bg="#fff9c4")
            
            btn.grid(row=row, column=col, padx=2, pady=2)
            
            col += 1
            if col > 6:
                col = 0
                row += 1
    
    def update_todos(self, todos: List[Todo]):
        """更新 todo 列表並刷新月曆"""
        self.todos = todos
        self._update_calendar()
    
    def get_frame(self) -> ttk.Frame:
        """取得框架元件"""
        return self.frame

