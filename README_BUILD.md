# 打包說明

## 使用 uv 管理專案

### 安裝 PyInstaller（如果尚未安裝）
```bash
uv pip install pyinstaller
```

## 打包成 exe

### 方法 1: 使用提供的腳本
```bash
python build_exe.py
```

### 方法 2: 直接使用 PyInstaller
```bash
pyinstaller --name=TodoListCalendar --onefile --windowed main.py
```

### 方法 3: 使用 uv 執行（如果已安裝在虛擬環境中）
```bash
uv run pyinstaller --name=TodoListCalendar --onefile --windowed main.py
```

### 打包後的檔案位置
執行檔會位於 `dist/TodoListCalendar.exe`

## 注意事項

1. **首次打包**：PyInstaller 會自動分析依賴並打包所有必要的檔案
2. **檔案大小**：打包後的 exe 檔案可能會比較大（約 10-20MB），因為包含了 Python 執行環境
3. **防毒軟體**：某些防毒軟體可能會誤報，這是正常現象
4. **資料檔案**：`todos.json` 會在首次執行時自動建立

## 執行打包後的程式

直接雙擊 `dist/TodoListCalendar.exe` 即可執行，無需安裝 Python。

