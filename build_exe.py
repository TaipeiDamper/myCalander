"""
打包腳本 - 使用 PyInstaller 將應用程式打包成 exe
版本: v1.0.0
"""

import PyInstaller.__main__
import os
import sys

def build_exe():
    """打包應用程式為 exe"""
    
    # PyInstaller 參數
    args = [
        'main.py',                    # 主程式檔案
        '--name=TodoListCalendar',    # 執行檔名稱
        '--onefile',                  # 打包成單一執行檔
        '--windowed',                 # 不顯示控制台視窗（GUI 應用）
        '--icon=NONE',                # 如果有圖示檔案可以指定路徑
        '--add-data=todos.json;.',    # 包含資料檔案（如果存在）
        '--hidden-import=tkinter',     # 確保 tkinter 被包含
        '--hidden-import=tkinter.ttk',
        '--clean',                     # 清理暫存檔案
    ]
    
    # 如果 todos.json 不存在，移除該參數
    if not os.path.exists('todos.json'):
        args = [arg for arg in args if not arg.startswith('--add-data=todos.json')]
    
    PyInstaller.__main__.run(args)
    
    print("\n打包完成！執行檔位於 dist/TodoListCalendar.exe")

if __name__ == "__main__":
    build_exe()

