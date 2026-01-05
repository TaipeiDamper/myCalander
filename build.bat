@echo off
echo 正在打包 Todo List 月曆應用程式...
pyinstaller --name=TodoListCalendar --onefile --windowed --clean main.py
echo.
echo 打包完成！執行檔位於 dist\TodoListCalendar.exe
pause

