Created At: 2026-05-22T04:28:09Z
Completed At: 2026-05-22T04:28:09Z
File Path: `file:///C:/Users/ASAHI/.gemini/antigravity-ide/brain/4c70f361-ddc2-4366-bf46-5d2ced6e799e/task.md`
Total Lines: 17
Total Bytes: 1660
Showing lines 1 to 17
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
1: - [x] 修正 `data_manager.py`：
2:     - [x] 修改 `fetch_history_yahoo`：若歷史 close prices 天數大於 0 且小於 20 天，使用實際天數計算 `ma20` 與 `low20`。
3:     - [x] 修改 `compute_asset`：完全移除對 `ma20`, `low20`, `nav` 以當前現價為預設替代的當日 fallback 模擬邏輯。
4:     - [x] 修改 `_do_fetch`：若 `nav` 更新則將 `config_changed` 設為 `True`，並移除建構 `asset_data` 時的當日價格預設。
5:     - [x] 移動 `_do_fetch` 的 `save_to_disk` 機制至函式最底端統一存檔。
6: - [x] 修正 `stock_widget.py`：
7:     - [x] 修改 `_build_expanded_ui`：重構股票列為包含主列與詳細列的 item 容器，綁定自適應的 hover 事件與 Canvas 的 symbol 屬性。
8:     - [x] 修改 `_draw_status_bar`：在展開模式獲取 `computed` 參數時移除當日價格 fallback 預設，並將 key 欄位存入 `canvas.stock_coords`。
9:     - [x] 新增 `_render_detail_content` 函式，動態生成與更新下方數值列的 Labels。
10:     - [x] 重構 `_toggle_detail_bar`，改為僅對 `detail_fm` 進行顯示/隱藏與重新渲染，避開整頁 rebuild。
11:     - [x] 修改 `_on_bar_click`，移除 `_show_temp_val`，改為對 `_highlight_detail_label` 的呼叫。
12:     - [x] 新增 `_highlight_detail_label` 與 `_clear_highlights` 高亮控制機制，處理 hover 色覆蓋。
13: - [x] 驗證與測試：
14:     - [x] 測試 `00403A` 在沒有歷史資料時，背景是否能自動補齊正確的新上市實體數據並寫入檔案中。
15:     - [x] 測試點擊現價展開時下方長出新一行。
16:     - [x] 測試點擊 Canvas 刻度高亮下方對應簡寫 Label 區塊。
17: 
The above content shows the entire, complete file contents of the requested file.
