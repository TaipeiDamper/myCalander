"""
Todo List 應用程式 - 月曆視圖
版本: v1.0.5
建立日期: 2024-01-XX
更新: 
  - v1.0.1: 修正日期計算錯誤和版面對齊問題
  - v1.0.2: 週日移到最左側、日期加英文簡寫、顏色區分、今日任務顯示
  - v1.0.3: 移除日期格子中的英文縮寫，只保留標題；修正對齊問題
  - v1.0.4: 修正日期上下對齊問題；今日任務分為未完成和已完成兩部分
  - v1.0.5: 修正二月、三月等月份變窄的問題，確保所有月份寬度一致
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from typing import List, Callable, Optional
from core.models import Todo


class CalendarView:
    """互動月曆視圖"""
    
    def __init__(self, parent, todos: List[Todo], 
                 on_date_click: Callable[[str], None],
                 external_nav_frame: tk.Frame = None):
        """
        初始化月曆視圖
        
        Args:
            parent: 父容器
            todos: 所有 todo 列表
            on_date_click: 日期點擊回調函數，參數為日期字串 (YYYY-MM-DD)
            external_nav_frame: (可選) 外部提供的導航按鈕容器
        """
        self.parent = parent
        self.todos = todos
        self.on_date_click = on_date_click
        self.external_nav_frame = external_nav_frame
        self.current_date = datetime.now()
        
        # 建立主框架
        self.frame = ttk.Frame(parent)
        
        # 建立月曆元件
        self._create_calendar()
    
    def _create_calendar(self):
        """建立月曆介面"""
        # 標題和導航按鈕
        if self.external_nav_frame:
            header_frame = self.external_nav_frame
            # 清除可能殘留的舊內容
            for widget in header_frame.winfo_children():
                widget.destroy()
        else:
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
        
        # 建立 PanedWindow 讓使用者可以上下拖動調整「月曆」與「今日任務」的區塊大小
        self.paned_window = tk.PanedWindow(self.frame, orient=tk.VERTICAL, sashrelief=tk.RAISED, sashwidth=6, bg="#cccccc")
        self.paned_window.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        # 建立一個容器框架來包含星期標題和月曆網格，確保對齊
        self.calendar_container = ttk.Frame(self.paned_window)
        self.paned_window.add(self.calendar_container, minsize=200) # 加入 PanedWindow，並且設定最小高度
        
        # 星期標題（週日在最左側）- 使用 grid 以確保對齊
        weekdays_frame = ttk.Frame(self.calendar_container)
        weekdays_frame.grid(row=0, column=0, sticky="ew")
        
        # 週日移到最左側：["日", "一", "二", "三", "四", "五", "六"]
        weekdays = ["日", "一", "二", "三", "四", "五", "六"]
        weekday_abbr = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
        for i, day in enumerate(weekdays):
            label_text = f"{day}\n{weekday_abbr[i]}"
            label = ttk.Label(weekdays_frame, text=label_text, anchor="center", font=("Arial", 9))
            label.grid(row=0, column=i, padx=2, pady=2, sticky="nsew")
        
        # 設定星期標題欄位權重（與月曆網格一致，使用相同的 uniform 名稱）
        for i in range(7):
            weekdays_frame.columnconfigure(i, weight=1, uniform="calendar_col")
        
        # 月曆網格
        self.calendar_frame = ttk.Frame(self.calendar_container)
        self.calendar_frame.grid(row=1, column=0, sticky="ew", pady=(5, 0))
        
        # 設定容器框架的欄位權重，並確保有最小寬度
        self.calendar_container.columnconfigure(0, weight=1, minsize=700)
        
        # 今日任務區域
        self.today_tasks_frame = ttk.LabelFrame(self.paned_window, text="今日任務", padding=10)
        self.paned_window.add(self.today_tasks_frame, minsize=180) # 加大最小高度以防標題欄位被擠壓到看不到
        
        self.holidays_cache = {}
        self._fetch_holidays(self.current_date.year)
        
        self._update_calendar()
    
    def _fetch_holidays(self, year):
        """非同步抓取該年度的台灣國定假日資料"""
        if year in self.holidays_cache:
            return
            
        self.holidays_cache[year] = "loading"
        
        def fetch():
            import urllib.request
            import json
            try:
                url = f"https://cdn.jsdelivr.net/gh/ruyut/TaiwanCalendar/data/{year}.json"
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=5) as res:
                    data = json.loads(res.read())
                    year_data = {}
                    for item in data:
                        date_str = item.get('date', "")
                        if len(date_str) == 8:
                            formatted = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
                            year_data[formatted] = item
                            
                    self.holidays_cache[year] = year_data
                    
                    if hasattr(self, 'current_date') and self.current_date.year == year:
                        if hasattr(self, 'frame') and self.frame.winfo_exists():
                            self.frame.after(0, self._update_calendar)
            except Exception:
                self.holidays_cache.pop(year, None)
                
        import threading
        threading.Thread(target=fetch, daemon=True).start()
    
    def _get_month_year_str(self) -> str:
        """取得月份年份字串"""
        return self.current_date.strftime("%Y 年 %m 月")
    
    def _prev_month(self):
        """切換到上一個月"""
        old_year = self.current_date.year
        if self.current_date.month == 1:
            self.current_date = self.current_date.replace(year=self.current_date.year - 1, month=12)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month - 1)
        self.month_label.config(text=self._get_month_year_str())
        
        if old_year != self.current_date.year:
            self._fetch_holidays(self.current_date.year)
            
        self._update_calendar()
    
    def _next_month(self):
        """切換到下一個月"""
        old_year = self.current_date.year
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(year=self.current_date.year + 1, month=1)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month + 1)
        self.month_label.config(text=self._get_month_year_str())
        
        if old_year != self.current_date.year:
            self._fetch_holidays(self.current_date.year)
            
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
            
            # 檢查這一天是否有 todo (包含已完成的)
            day_todos = [t for t in self.todos if t.date == date_str]
            
            # 判斷是否為今天
            is_today = (self.current_date.year == today.year and 
                       self.current_date.month == today.month and 
                       day == today.day)
            
            # 是否為假日判斷
            is_weekend = (col == 0 or col == 6) # 週日為0，週六為6
            is_holiday = is_weekend
            holiday_desc = ""
            
            year = self.current_date.year
            if hasattr(self, 'holidays_cache') and year in self.holidays_cache and isinstance(self.holidays_cache[year], dict):
                day_info = self.holidays_cache[year].get(date_str)
                if day_info:
                    is_holiday = day_info.get("isHoliday", is_weekend)
                    holiday_desc = day_info.get("description", "")
            
            # 建立按鈕文字（只顯示日期數字，不顯示英文縮寫）
            if day_todos:
                # 排序，讓「未完成」的任務排在最前面顯示
                day_todos_sorted = sorted(day_todos, key=lambda x: x.completed)
                first_todo = day_todos_sorted[0]
                
                # 判斷是否「全數完成」
                all_completed = all(t.completed for t in day_todos_sorted)
                
                prefix = "✓ " if first_todo.completed else ""
                # 如果加上 ✓ 前綴，為了排版好看，標題擷取可稍微縮短
                btn_text = f"{day}\n{prefix}{first_todo.title[:5]}"
                
                if len(day_todos_sorted) > 1:
                    btn_text += f"\n(+{len(day_todos_sorted)-1})"
            else:
                all_completed = False
                btn_text = str(day)
                if holiday_desc:
                    btn_text += f"\n{holiday_desc[:5]}"
            
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
            text_color = "#d32f2f" if is_holiday else "#000000" # 假日為紅色
            
            if is_today:
                # 今天是特殊標註（邊框加粗 + 特殊顏色）
                btn.config(bg="#ffeb3b", fg=text_color, 
                          relief=tk.SOLID, borderwidth=3)
            elif day_todos:
                if all_completed:
                    # 所有任務皆已完成（使用淺綠色並將字體變灰，代表已結案）
                    btn.config(bg="#e8f5e9", fg="#757575")
                else:
                    # 還有未完成任務的日期（淺藍色）
                    btn.config(bg="#e3f2fd", fg=text_color)
            else:
                # 沒有任務的日期（白色/灰色）
                btn.config(bg="#f5f5f5", fg=text_color)
            
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            
            col += 1
            if col > 6:
                col = 0
                row += 1
        
        # 填充最後一行的空白格子，確保每行都有7個格子
        while col < 7:
            empty_label = ttk.Label(self.calendar_frame, text="")
            empty_label.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            col += 1
        
        # 設定欄位權重，讓按鈕均勻分佈（與星期標題使用相同的 uniform 名稱以確保對齊）
        # 確保所有行都使用相同的設定
        for i in range(7):
            self.calendar_frame.columnconfigure(i, weight=1, uniform="calendar_col")
        
        # 確保容器框架有最小寬度，避免月份天數少時變窄
        self.calendar_frame.update_idletasks()
        self.calendar_container.update_idletasks()
        
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
        
        # 取得今日的任務（分為未完成和已完成）
        today_todos_all = [t for t in self.todos if t.date == today_str]
        today_todos_incomplete = [t for t in today_todos_all if not t.completed]
        today_todos_completed = [t for t in today_todos_all if t.completed]
        
        # 排序任務（按時間）
        today_todos_incomplete = sorted(today_todos_incomplete)
        today_todos_completed = sorted(today_todos_completed)
        
        # 建立主容器（使用 grid 來分上下兩部分）
        main_container = ttk.Frame(self.today_tasks_frame)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # 上半部分：未完成任務
        incomplete_frame = ttk.LabelFrame(main_container, text="未完成任務", padding=5)
        incomplete_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        if not today_todos_incomplete:
            no_task_label = ttk.Label(
                incomplete_frame, 
                text="沒有待完成的任務",
                foreground="gray"
            )
            no_task_label.pack(pady=10)
        else:
            # 建立任務列表框架（含滾動條）
            list_frame = ttk.Frame(incomplete_frame)
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
            
            # 加入未完成任務到列表
            for todo in today_todos_incomplete:
                time_str = todo.time if todo.time else "全天"
                task_text = f"[{time_str}] {todo.title}"
                if todo.content:
                    task_text += f" - {todo.content[:30]}"
                task_listbox.insert(tk.END, task_text)
        
        # 下半部分：已完成任務
        completed_frame = ttk.LabelFrame(main_container, text="已完成任務", padding=5)
        completed_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        if not today_todos_completed:
            no_completed_label = ttk.Label(
                completed_frame, 
                text="沒有已完成的任務",
                foreground="gray"
            )
            no_completed_label.pack(pady=10)
        else:
            # 建立任務列表框架（含滾動條）
            list_frame2 = ttk.Frame(completed_frame)
            list_frame2.pack(fill=tk.BOTH, expand=True)
            
            # 滾動條
            scrollbar2 = ttk.Scrollbar(list_frame2)
            scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
            
            # 任務列表
            task_listbox2 = tk.Listbox(
                list_frame2,
                yscrollcommand=scrollbar2.set,
                font=("Arial", 10),
                selectmode=tk.SINGLE,
                foreground="gray"
            )
            task_listbox2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar2.config(command=task_listbox2.yview)
            
            # 加入已完成任務到列表
            for todo in today_todos_completed:
                time_str = todo.time if todo.time else "全天"
                task_text = f"[{time_str}] ✓ {todo.title}"
                if todo.content:
                    task_text += f" - {todo.content[:30]}"
                task_listbox2.insert(tk.END, task_text)
        
        # 設定主容器的行權重
        main_container.rowconfigure(0, weight=1, minsize=60)
        main_container.rowconfigure(1, weight=1, minsize=60)
        main_container.columnconfigure(0, weight=1)
    
    def update_todos(self, todos: List[Todo]):
        """更新 todo 列表並刷新月曆"""
        self.todos = todos
        self._update_calendar()
    
    def get_frame(self) -> ttk.Frame:
        """取得框架元件"""
        return self.frame


