import tkinter as tk
from tkinter import ttk
from datetime import datetime
import hashlib
from core.models import Todo
from typing import List

class MatrixView:
    def __init__(self, parent, todos: List[Todo], on_edit=None, on_toggle_complete=None):
        self.parent = parent
        self.todos = todos
        self.on_edit = on_edit
        self.on_toggle_complete = on_toggle_complete
        
        self.frame = ttk.Frame(parent)
        self.selected_todo_id = None
        self.max_days = 14
        self.sort_mode = "date" # "date" or "importance"
        self.drag_data = {"x": 0, "y": 0, "item": None, "id": None}
        self.offsets = {} # 暫時的拖曳位移量 {todo_id: (dx, dy)}
        
        self._build_ui()
        self.update_todos(self.todos)
        
    def get_frame(self):
        return self.frame
        
    def _build_ui(self):
        # 建立 PanedWindow 分割上下
        self.paned = tk.PanedWindow(self.frame, orient=tk.VERTICAL, sashrelief=tk.RAISED, sashwidth=6)
        self.paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # --- 上半部：四個清單 ---
        self.top_frame = ttk.Frame(self.paned)
        self.paned.add(self.top_frame, minsize=150)
        
        for i in range(4):
            self.top_frame.columnconfigure(i, weight=1, uniform="list_col")
        self.top_frame.rowconfigure(0, weight=1)
        
        self.listboxes = {}
        lists_info = [
            ("today", "今天到期"),
            ("week", "這周到期"),
            ("all_incomplete", "所有未完成"),
            ("today_completed", "今日完成 (更動)")
        ]
        
        for idx, (key, title) in enumerate(lists_info):
            frame = ttk.LabelFrame(self.top_frame, text=title)
            frame.grid(row=0, column=idx, sticky="nsew", padx=4, pady=2)
            
            scrollbar = ttk.Scrollbar(frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # exportselection=False 確保點擊一個 Listbox 時不會取消另一個的選取狀態
            lb = tk.Listbox(frame, yscrollcommand=scrollbar.set, font=("Arial", 10), exportselection=False)
            lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.config(command=lb.yview)
            
            lb.bind("<<ListboxSelect>>", lambda e, k=key: self._on_listbox_select(k))
            lb.bind("<Double-1>", lambda e, k=key: self._on_listbox_double_click(k))
            self.listboxes[key] = lb
            
        # --- 下半部：艾森豪矩陣 ---
        self.bottom_frame = ttk.Frame(self.paned)
        self.paned.add(self.bottom_frame, minsize=300)
        
        ctrl_frame = ttk.Frame(self.bottom_frame)
        ctrl_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(ctrl_frame, text="最遠顯示天數:").pack(side=tk.LEFT, padx=5)
        self.days_spinbox = ttk.Spinbox(ctrl_frame, from_=3, to=90, width=5, command=self._on_days_changed)
        self.days_spinbox.set(self.max_days)
        self.days_spinbox.pack(side=tk.LEFT)
        self.days_spinbox.bind("<Return>", lambda e: self._on_days_changed())
        
        ttk.Label(ctrl_frame, text="*水平軸為距離到期時間，垂直軸為即時重要性", foreground="gray").pack(side=tk.RIGHT, padx=5)
        
        # 排序與重整按鈕
        self.sort_var = tk.StringVar(value="date")
        ttk.Radiobutton(ctrl_frame, text="按日期", variable=self.sort_var, value="date", command=self._refresh_lists).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(ctrl_frame, text="按重要性", variable=self.sort_var, value="importance", command=self._refresh_lists).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(ctrl_frame, text="重新整理 (回到原位)", command=self._reset_positions).pack(side=tk.LEFT, padx=10)
        
        self.canvas = tk.Canvas(self.bottom_frame, bg="#ffffff", highlightthickness=1, highlightbackground="#cccccc")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.canvas.bind("<Configure>", lambda e: self._draw_matrix())
        
        self.canvas_items = {}
        
    def _on_days_changed(self):
        try:
            val = int(self.days_spinbox.get())
            if val > 0:
                self.max_days = val
                self._draw_matrix()
        except ValueError:
            pass
            
    def _reset_positions(self):
        self.offsets = {}
        self._draw_matrix()

    def update_todos(self, todos):
        self.all_todos = todos # 保留所有任務以篩選已完成
        self.todos = [t for t in todos if not t.completed]
        self._refresh_lists()
        self._draw_matrix()
        
    def _refresh_lists(self):
        for lb in self.listboxes.values():
            lb.delete(0, tk.END)
            
        self.list_data = {"today": [], "week": [], "all_incomplete": [], "today_completed": []}
        
        now = datetime.now()
        now_date = now.date()
        
        # 排序未完成
        sort_by = self.sort_var.get()
        if sort_by == "importance":
            # 依照重要性排序，重要性相同則按日期
            sorted_incomplete = sorted(self.todos, key=lambda x: (-(getattr(x, 'importance', 5)), x.date if x.date else "9999-12-31"))
        else:
            # 依照日期排序，日期相同則按重要性
            sorted_incomplete = sorted(self.todos, key=lambda x: (x.date if x.date else "9999-12-31", -(getattr(x, 'importance', 5))))

        for t in sorted_incomplete:
            self.list_data["all_incomplete"].append(t)
            if not t.date: continue
            try:
                t_date = datetime.strptime(t.date, "%Y-%m-%d").date()
                days_diff = (t_date - now_date).days
                if days_diff == 0: self.list_data["today"].append(t)
                if 0 <= days_diff <= 7: self.list_data["week"].append(t)
            except ValueError: pass

        # 今日完成 (今日完成時間有更動的)
        today_str = now.strftime("%Y-%m-%d")
        done_list = []
        for t in self.all_todos:
            if t.completed and t.completion_time and t.completion_time.startswith(today_str):
                done_list.append(t)
        # 依照完成時間排序：最晚完成的在上面 (reverse=True)
        done_list.sort(key=lambda x: x.completion_time if x.completion_time else "", reverse=True)
        self.list_data["today_completed"] = done_list
                
        # 填入 UI
        for key in self.list_data:
            for t in self.list_data[key]:
                display_text = f"[{t.date}] {t.title}"
                if key == "today_completed":
                    # 顯示完成時間
                    t_time = t.completion_time.split(" ")[1] if t.completion_time else "??:??"
                    display_text = f"✓ {t.title} ({t_time})"
                self.listboxes[key].insert(tk.END, display_text)
                
        self._update_selection()
                
    def _on_listbox_select(self, source_key):
        lb = self.listboxes[source_key]
        selection = lb.curselection()
        if selection:
            idx = selection[0]
            selected_t = self.list_data[source_key][idx]
            self.selected_todo_id = selected_t.id
            self._update_selection(redraw_canvas=True)
            
    def _on_listbox_double_click(self, source_key):
        lb = self.listboxes[source_key]
        selection = lb.curselection()
        if selection and self.on_edit:
            idx = selection[0]
            selected_t = self.list_data[source_key][idx]
            self.on_edit(selected_t)
            
    def _on_canvas_click(self, todo_id, event=None):
        # 初始化拖曳數據
        if event:
            self.drag_data["id"] = todo_id
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

        # 如果點擊的是已經選中的，我們嘗試找尋重疊的下一個
        if todo_id == self.selected_todo_id and event:
            # 尋找鼠標位置附近的所有項目
            overlapping = self.canvas.find_overlapping(event.x-2, event.y-2, event.x+2, event.y+2)
            # 過濾出屬於 todo 點的項目 (我們可以用 tag 來標記)
            todo_items = []
            for item in overlapping:
                tags = self.canvas.gettags(item)
                for tag in tags:
                    if tag.startswith("todo_"):
                        tid = tag.replace("todo_", "")
                        if tid not in todo_items:
                            todo_items.append(tid)
            
            if len(todo_items) > 1:
                # 循環切換
                try:
                    current_idx = todo_items.index(str(self.selected_todo_id))
                    next_idx = (current_idx + 1) % len(todo_items)
                    self.selected_todo_id = int(todo_items[next_idx])
                except (ValueError, IndexError):
                    self.selected_todo_id = int(todo_items[0])
            else:
                self.selected_todo_id = todo_id
        else:
            self.selected_todo_id = todo_id
            
        self._update_selection(redraw_canvas=True)
        
    def _on_canvas_double_click(self, todo_id):
        if self.on_edit:
            t = next((t for t in self.todos if t.id == todo_id), None)
            if t:
                self.on_edit(t)
            
    def _update_selection(self, redraw_canvas=True):
        # 更新 listbox 高亮
        for key in self.listboxes:
            lb = self.listboxes[key]
            lb.selection_clear(0, tk.END)
            for idx, t in enumerate(self.list_data[key]):
                if t.id == self.selected_todo_id:
                    lb.selection_set(idx)
                    lb.see(idx)
                    
        # 更新 canvas 高亮
        if redraw_canvas:
            self._draw_matrix()
        
    def _draw_matrix(self):
        self.canvas.delete("all")
        self.canvas_items.clear()
        
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        
        if w <= 1 or h <= 1: return
        
        # 邊界 (加大一點邊界，避免被吃掉字)
        pad_x, pad_y = 50, 50
        plot_w = w - pad_x * 2
        plot_h = h - pad_y * 2
        
        # 繪製座標軸
        # X軸 (時間距離) - 原點在右邊(最遠), 左邊表示現在(0) 甚至過去(<0)
        # 所以 X = w - pad_x 才是未來 (最遠)，而 pad_x 是今天
        
        # 畫十字線 (重要性5 為中心；X軸也畫一條時間的一半作為中心)
        mid_y = h - pad_y - (5 - 1) / 9.0 * plot_h
        mid_x = pad_x + plot_w / 2.0
        
        # 畫四象限的區分虛線 (顏色加深)
        self.canvas.create_line(pad_x, mid_y, w - pad_x, mid_y, fill="#666666", dash=(4, 4))
        self.canvas.create_line(mid_x, pad_y, mid_x, h - pad_y, fill="#666666", dash=(4, 4))
        
        # 軸線 (X=時間 Y=重要性)
        self.canvas.create_line(pad_x, h - pad_y, w - pad_x, h - pad_y, fill="#999999", width=2, arrow=tk.LAST)
        self.canvas.create_line(pad_x, h - pad_y, pad_x, pad_y, fill="#999999", width=2, arrow=tk.LAST)
        
        self.canvas.create_text(w - pad_x + 10, h - pad_y + 15, text="距離到期 (遠)", anchor="n", font=("Arial", 9))
        self.canvas.create_text(pad_x - 15, pad_y - 15, text="重要性", anchor="w", font=("Arial", 9))
        
        # 標籤
        self.canvas.create_text(pad_x, h - pad_y + 15, text="今天/已錯過", anchor="n", font=("Arial", 8))
        self.canvas.create_text(pad_x - 15, h - pad_y, text="1", anchor="e", font=("Arial", 8))
        self.canvas.create_text(pad_x - 15, pad_y, text="10", anchor="e", font=("Arial", 8))
        
        now = datetime.now()
        
        for t in self.todos:
            if not t.date: continue
            try:
                t_date = datetime.strptime(t.date, "%Y-%m-%d").date()
                days_diff = (t_date - now.date()).days
                
                # 越接近極限天數，X越靠右。超過max_days則頂在右邊。已錯過則在X=0
                plot_days = max(0, min(days_diff, self.max_days))
                
                # 將線性時間比例轉換為非線性（使用開根號，讓靠近現在的時間佔據較多空間）
                linear_x_ratio = plot_days / float(self.max_days)
                x_ratio = linear_x_ratio ** 0.5  # 非線性：0的依然是0，1的依然是1，但中間的值會放大 (例如 0.25 -> 0.5)
                
                x = pad_x + x_ratio * plot_w
                
                # 計算實際繪圖位置
                base_imp = getattr(t, 'importance', 5)
                time_sens = getattr(t, 'time_sensitivity', 5)
                
                # 越接近今天，重要性提升越多。假設最大提升 = time_sens / 2
                if days_diff <= 0:
                    bonus = time_sens / 2.0
                else:
                    ratio = max(0, 1.0 - (days_diff / self.max_days))
                    bonus = (time_sens / 2.0) * ratio
                    
                eff_imp = min(10.0, base_imp + bonus)
                
                
                y = h - pad_y - ((eff_imp - 1) / 9.0) * plot_h
                
                # 繪製移動軌跡 (示意從無時間加成的原本位置 到 現在位置的軌跡)
                # 從時間最遠的地方開始 (x最右, y原高度)
                orig_y = h - pad_y - ((base_imp - 1) / 9.0) * plot_h
                start_x = pad_x + plot_w  # 最遠的地方
                
                # 繪製移動軌跡 (示意從無時間加成的原本位置 到 現在位置的軌跡)
                self.canvas.create_line(start_x, orig_y, x, y, fill="#e0e0e0", dash=(2, 4))
                
                # 決定顏色
                # 最左上 (x=0, y=0) 最鮮豔 (#FF0000)
                imp_score = (eff_imp - 1) / 9.0
                urg_score = 1.0 - x_ratio
                
                # 色彩分布更極端一點：左上強紅
                color_factor = (imp_score * urg_score) ** 0.3 
                
                # 從淡灰 (180, 180, 180) 到 純紅 (255, 0, 0)
                r_val = int(180 + (255 - 180) * color_factor)
                g_val = int(180 + (0 - 180) * color_factor)
                b_val = int(180 + (0 - 180) * color_factor)
                color = f"#{r_val:02x}{g_val:02x}{b_val:02x}"
                
                is_selected = (t.id == self.selected_todo_id)
                
                # 重要性影響點點的大小
                base_r = 4 + (imp_score) * 10 
                r = base_r + 4 if is_selected else base_r
                outline = "#000000" if is_selected else color
                width = 2 if is_selected else 1
                
                # 取得拖曳偏移量
                off_x, off_y = self.offsets.get(t.id, (0, 0))
                draw_x = x + off_x
                draw_y = y + off_y
                
                # 使用 tag 標記 todo ID，方便重疊點選與拖曳
                obj_tag = f"todo_{t.id}"
                dash_tag = f"dash_{t.id}"
                
                # 繪製拖曳軌跡 (與原點連線)
                if off_x != 0 or off_y != 0:
                    dash_color = f"#{int(r_val*0.7):02x}{int(g_val*0.7):02x}{int(b_val*0.7):02x}"
                    self.canvas.create_line(x, y, draw_x, draw_y, fill=dash_color, dash=(2, 2), tags=(dash_tag,))
                
                item_id = self.canvas.create_oval(draw_x-r, draw_y-r, draw_x+r, draw_y+r, fill=color, outline=outline, width=width, tags=(obj_tag,))
                text_id = self.canvas.create_text(draw_x, draw_y-r-8, text=t.title[:5], font=("Arial", 8, "bold" if is_selected else "normal"), tags=(obj_tag,))
                
                if is_selected:
                    self.canvas.tag_raise(obj_tag)
                
                # 綁定事件
                for i_id in (item_id, text_id):
                    self.canvas.tag_bind(i_id, "<Button-1>", lambda e, tid=t.id: self._on_canvas_click(tid, e))
                    self.canvas.tag_bind(i_id, "<B1-Motion>", lambda e, tid=t.id: self._on_drag(e, tid))
                    self.canvas.tag_bind(i_id, "<ButtonRelease-1>", lambda e: self._on_drag_release(e))
                    self.canvas.tag_bind(i_id, "<Double-1>", lambda e, tid=t.id: self._on_canvas_double_click(tid))
                    self.canvas.tag_bind(i_id, "<Enter>", lambda e, i=item_id: self.canvas.config(cursor="hand2"))
                    self.canvas.tag_bind(i_id, "<Leave>", lambda e, i=item_id: self.canvas.config(cursor=""))

                    
            except Exception as e:
                pass

    def _on_drag(self, event, tid):
        if self.drag_data["id"] is None:
            self.drag_data["id"] = tid
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y
            return

        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]
        
        if dx == 0 and dy == 0:
            return
            
        old_off = self.offsets.get(tid, (0, 0))
        new_off = (old_off[0] + dx, old_off[1] + dy)
        self.offsets[tid] = new_off
        
        # 實時移動畫布上的元件
        obj_tag = f"todo_{tid}"
        self.canvas.move(obj_tag, dx, dy)
        
        # 同步移動虛線 (如果有)
        dash_tag = f"dash_{tid}"
        self.canvas.move(dash_tag, dx, dy)
        
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def _on_drag_release(self, event):
        if self.drag_data["id"]:
            # 釋放後才重新繪製，以正確顯示軌跡虛線等
            self._draw_matrix()
        self.drag_data["id"] = None
