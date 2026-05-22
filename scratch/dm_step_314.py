Created At: 2026-05-22T03:36:28Z
Completed At: 2026-05-22T03:36:28Z
File Path: `file:///C:/Users/ASAHI/.gemini/antigravity-ide/brain/4c70f361-ddc2-4366-bf46-5d2ced6e799e/task.md`
Total Lines: 14
Total Bytes: 1152
Showing lines 1 to 14
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
1: - [x] 重構 `stock_widget.py`
2:     - [x] 新增 `self._expand_bar` 與 `self._collapse_bar` 事件處理，並調整價格數字 `curr_lbl` 的事件綁定（`<Button-1>` 與 `<Leave>`）
3:     - [x] 重構 `_draw_status_bar`：
4:         - [x] 計算展開模式下的些微外擴橫軸範圍 `[v_axis_min, v_axis_max]` 與 clamping 限制坐標演算法
5:         - [x] 繪製水平背景參考細線與今日波動範圍粗線
6:         - [x] 依漲跌繪製空心三角形 `▷`（漲）、`◁`（跌）或圓圈 `○`（平盤）指針
7:         - [x] 繪製各參考價的垂直小短線（凸起），高度區分背景參考（高6）與決策警戒（高8），並實作 ETF 折溢價退化淡化樣式
8:     - [x] 重構 `_on_bar_click`：
9:         - [x] 將所有繪製點 the `(x, value, label)` 記錄在 `canvas.stock_coords` 中
10:         - [x] 點擊時比對最接近的刻度，並在 8 像素內時浮現中文名稱與價格提示，3秒後隱藏
11: - [x] 修復 `data_manager.py`（補回 git reset 丟失的分析計算邏輯與屬性）
12: - [x] 啟動本機日曆程式進行測試 (Task ID: task-263)
13: - [/] 手動驗證所有視覺與互動功能
14: 
The above content shows the entire, complete file contents of the requested file.
