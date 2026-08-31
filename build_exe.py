import os
import subprocess
import sys

def build():
    # 檢查是否安裝了 pyinstaller
    try:
        import PyInstaller
    except ImportError:
        print("未偵測到 PyInstaller，正在進行安裝...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    print("開始打包 智能曆 應用程式...")
    
    # 打包指令
    # --noconsole: 不顯示黑視窗
    # --onefile: 打包成單一 exe (雖然啟動稍慢，但方便攜帶)
    # --name: 輸出的檔名
    # --clean: 清除暫存目錄
    cmd = [
        "pyinstaller",
        "--noconsole",
        "--onefile",
        "--name", "SmartCalendar",
        "--paths", ".",
        "--collect-submodules", "core",
        "--collect-submodules", "todo",
        "--collect-submodules", "stock",
        "--collect-submodules", "weather",
        "--clean",
        "main.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        
        # 自動複製設定檔到 dist 資料夾
        import shutil
        configs = [
            "todos.json", 
            os.path.join("stock", "stock_config.json"), 
            os.path.join("weather", "weather_config.json")
        ]
        for cfg in configs:
            if os.path.exists(cfg):
                dest_name = os.path.basename(cfg)
                dest_path = os.path.join("dist", dest_name)
                # 邏輯調整：todos.json 保留使用者資料，其餘設定檔則強制覆蓋更新
                is_config = "config" in dest_name
                
                # 特殊判定：若 todos.json 在 dist 中為空或大小極小，而來源比較大，則仍允許覆蓋複製
                force_copy = False
                if dest_name == "todos.json" and os.path.exists(dest_path):
                    dest_size = os.path.getsize(dest_path)
                    src_size = os.path.getsize(cfg)
                    if dest_size <= 20 and src_size > dest_size:
                        force_copy = True

                if not os.path.exists(dest_path) or is_config or force_copy:
                    shutil.copy(cfg, dest_path)
                    action = "覆蓋更新" if os.path.exists(dest_path) and (is_config or force_copy) else "已複製"
                    print(f"{action}: {cfg} -> dist/{dest_name}")
                else:
                    print(f"保留現有使用者資料 (不覆蓋): dist/{dest_name}")

        print("\n" + "="*50)
        print("打包完成！")
        print("您的執行檔 (.exe) 位在: dist/SmartCalendar.exe")
        print("="*50)
    except subprocess.CalledProcessError as e:
        print(f"打包失敗: {e}")

if __name__ == "__main__":
    build()
