import tkinter as tk
import urllib.request
import json
import threading
import os
import time

CONFIG_FILE = "weather_config.json"

# 天氣狀態碼對應的中文描述 (基於 Open-Meteo API WMO 規範)
WEATHER_CODES = {
    0: "晴天",
    1: "晴時多雲", 2: "多雲", 3: "陰天",
    45: "起霧", 48: "有霧",
    51: "毛毛雨", 53: "微雨", 55: "小雨", 56: "凍雨", 57: "凍雨",
    61: "小雨", 63: "中雨", 65: "大雨", 66: "冰雨", 67: "冰雨",
    71: "小雪", 73: "中雪", 75: "大雪", 77: "雪",
    80: "陣雨", 81: "強陣雨", 82: "狂陣雨",
    85: "陣雪", 86: "大陣雪",
    95: "雷雨", 96: "強雷雨", 99: "強雷雨"
}

class HiddenWeatherWidget(tk.Frame):
    def __init__(self, parent, mode="header"):
        super().__init__(parent)
        self.parent = parent
        self.mode = mode # "header" or "sidebar"
        
        self.labels = []
        self._update_job = None
        self.is_collapsed = (mode == "header")
        
        self.config_data = self._load_config()
        self.update_interval_ms = self.config_data.get("update_interval_minutes", 60) * 60000
        
        if self.mode == "sidebar":
            self._build_sidebar_ui()
        else:
            self._build_collapsed_ui()
            
        self.update_weather()
        
    def _load_config(self):
        import sys
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
            
        try:
            config_path = os.path.join(base_path, CONFIG_FILE)
            if not os.path.exists(config_path):
                # 如果同層沒有，嘗試建立預設值
                default_loc = {"update_interval_minutes": 60, "location": {"name": "Taipei", "latitude": 25.0478, "longitude": 121.5319}}
                with open(config_path, "w", encoding="utf-8") as f:
                    json.dump(default_loc, f, indent=4)
                return default_loc
                
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {
                "update_interval_minutes": 60,
                "location": {"name": "Taipei", "latitude": 25.0478, "longitude": 121.5319}
            }
            
    def _build_sidebar_ui(self):
        for widget in self.winfo_children(): widget.destroy()
        self.config(bg="#ffffff")
        self.labels.clear()
        
        # 數據顯示區
        self.content_frame = tk.Frame(self, bg="#ffffff")
        self.content_frame.pack(padx=5, pady=5)
        
        for i in range(3):
            row = tk.Frame(self.content_frame, bg="#ffffff")
            row.pack(fill=tk.X, pady=2)
            day_lbl = tk.Label(row, text="-", font=("Arial", 8, "bold"), bg="#ffffff", width=3)
            day_lbl.pack(side="left")
            icon_lbl = tk.Label(row, text="-", font=("Arial", 9), bg="#ffffff", width=4)
            icon_lbl.pack(side="left")
            temp_lbl = tk.Label(row, text="-", font=("Arial", 8), fg="#D84315", bg="#ffffff")
            temp_lbl.pack(side="left", padx=5)
            rain_lbl = tk.Label(row, text="-", font=("Arial", 8), fg="#1565C0", bg="#ffffff")
            rain_lbl.pack(side="left")
            self.labels.append((day_lbl, icon_lbl, temp_lbl, rain_lbl))
            
        # 設定按鈕
        self.settings_btn = tk.Button(self, text="⚙️ 設定位置", command=self._toggle_settings, font=("Arial", 8), bg="#f8f9fa")
        self.settings_btn.pack(pady=5)
        
        # 隱藏的設定區域
        self.settings_frame = tk.Frame(self, bg="#f0f0f0", padx=5, pady=5)
        
        tk.Label(self.settings_frame, text="地名:", font=("Arial", 8), bg="#f0f0f0").grid(row=0, column=0, sticky="e")
        self.name_ent = tk.Entry(self.settings_frame, width=12, font=("Arial", 8))
        self.name_ent.grid(row=0, column=1, pady=2)
        
        tk.Label(self.settings_frame, text="緯度:", font=("Arial", 8), bg="#f0f0f0").grid(row=1, column=0, sticky="e")
        self.lat_ent = tk.Entry(self.settings_frame, width=12, font=("Arial", 8))
        self.lat_ent.grid(row=1, column=1, pady=2)
        
        tk.Label(self.settings_frame, text="經度:", font=("Arial", 8), bg="#f0f0f0").grid(row=2, column=0, sticky="e")
        self.lon_ent = tk.Entry(self.settings_frame, width=12, font=("Arial", 8))
        self.lon_ent.grid(row=2, column=1, pady=2)
        
        save_btn = tk.Button(self.settings_frame, text="儲存並更新", command=self._save_settings, font=("Arial", 8, "bold"), bg="#4caf50", fg="white")
        save_btn.grid(row=3, column=0, columnspan=2, pady=5)
        
        # 預設填入值
        loc = self.config_data.get("location", {})
        self.name_ent.insert(0, loc.get("name", "Taipei"))
        self.lat_ent.insert(0, str(loc.get("latitude", 25.0478)))
        self.lon_ent.insert(0, str(loc.get("longitude", 121.5319)))

    def _toggle_settings(self):
        if self.settings_frame.winfo_viewable():
            self.settings_frame.pack_forget()
            self.content_frame.pack(padx=5, pady=5, before=self.settings_btn)
        else:
            self.content_frame.pack_forget()
            self.settings_frame.pack(fill=tk.X, padx=10, pady=5, before=self.settings_btn)

    def _save_settings(self):
        try:
            new_name = self.name_ent.get()
            new_lat = float(self.lat_ent.get())
            new_lon = float(self.lon_ent.get())
            
            self.config_data["location"] = {
                "name": new_name,
                "latitude": new_lat,
                "longitude": new_lon
            }
            
            # 存入檔案
            config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), CONFIG_FILE)
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(self.config_data, f, indent=4, ensure_ascii=False)
            
            # 收回設定面板並更新
            self._toggle_settings()
            self.manual_update()
        except ValueError:
            tk.messagebox.showerror("錯誤", "經緯度必須是數字")

    def _build_collapsed_ui(self):
        for widget in self.winfo_children(): widget.destroy()
        bg_col = self.master.cget("bg")
        self.config(bg=bg_col)
        self.collapsed_lbl = tk.Label(self, text="今日天氣: 載入中...", font=("Arial", 9, "bold"), fg="#1565C0", bg=bg_col, cursor="hand2")
        self.collapsed_lbl.pack()
        # 點擊天氣連動側邊欄
        self.collapsed_lbl.bind("<Button-1>", self._trigger_sidebar)

    def _trigger_sidebar(self, event=None):
        # 尋找 TodoApp 實例中的 sidebar 並切換
        p = self.master
        while p and not hasattr(p, "sidebar"):
            if hasattr(p, "master"): p = p.master
            else: break
        if p and hasattr(p, "sidebar"):
            p.sidebar.toggle()

    def manual_update(self, event=None):
        self.update_weather()

    def update_weather(self):
        if self._update_job:
            self.after_cancel(self._update_job)
        threading.Thread(target=self._fetch_data, daemon=True).start()

    def _fetch_data(self):
        loc = self.config_data.get("location", {})
        lat, lon = loc.get("latitude", 25.0478), loc.get("longitude", 121.5319)
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=auto&forecast_days=3"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as res:
                data = json.loads(res.read())
                self.after(0, lambda: self._apply_updates(data.get("daily", {})))
        except Exception as e:
            print('FETCH ERROR:', e)
            import traceback
            traceback.print_exc()
            self.after(0, lambda: self._apply_updates(None))

    def _apply_updates(self, daily):
        if daily:
            times = daily.get("time", [])
            codes = daily.get("weather_code", [])
            t_max = daily.get("temperature_2m_max", [])
            t_min = daily.get("temperature_2m_min", [])
            p_prob = daily.get("precipitation_probability_max", [])
            days = ["今", "明", "後"]
            
            if hasattr(self, 'collapsed_lbl') and self.collapsed_lbl.winfo_exists():
                icon = WEATHER_CODES.get(codes[0], "未知") if codes else "未知"
                self.collapsed_lbl.config(text=f"☁️ {icon} {int(round(t_min[0]))}~{int(round(t_max[0]))}°C")

            for i in range(min(3, len(times))):
                if i < len(self.labels):
                    day_lbl, icon_lbl, temp_lbl, rain_lbl = self.labels[i]
                    if day_lbl.winfo_exists():
                        day_lbl.config(text=f"{days[i]}")
                        icon_lbl.config(text=WEATHER_CODES.get(codes[i], "-"))
                        temp_lbl.config(text=f"{int(round(t_min[i]))}~{int(round(t_max[i]))}°C")
                        rain_lbl.config(text=f"☔{p_prob[i]}%")
        
        self._update_job = self.after(self.update_interval_ms, self.update_weather)
