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
                shutil.copy(cfg, os.path.join("dist", dest_name))
                print(f"已複製: {cfg} -> dist/{dest_name}")

        print("\n" + "="*50)
        print("打包完成！")
        print("您的執行檔 (.exe) 位在: dist/SmartCalendar.exe")
        print("="*50)
    except subprocess.CalledProcessError as e:
        print(f"打包失敗: {e}")

if __name__ == "__main__":
    build()
