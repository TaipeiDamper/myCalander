Created At: 2026-05-22T04:28:02Z
Completed At: 2026-05-22T04:28:02Z
File Path: `file:///C:/Users/ASAHI/.gemini/antigravity-ide/brain/4c70f361-ddc2-4366-bf46-5d2ced6e799e/implementation_plan.md`
Total Lines: 54
Total Bytes: 3895
Showing lines 1 to 54
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
1: # 實作計畫：參數自動更新、移除當日價格 Fallback 與下方動態數值列
2: 
3: 根據您的最新意見，我們設計了以下精緻且低調的互動機制：
4: 1. **點擊 Canvas 刻度不顯示懸浮文字**：
5:    * 移除點擊 Canvas 刻度線時在 Canvas 上方浮現 `名稱: 數值` 的懸浮文字，保持畫面的極簡與低調。
6: 2. **下方動態新增數值列**：
7:    * 當點擊現價數字展開小工具時，會在該標的列下方**新增一行**（動態 Frame）。
8:    * 該行中會列出該標的目前所有有值的指標簡寫與數值（例如：`MA: xxx`、`L20: xxx`、`NAV: xxx`、`Watch: xxx`、`Buy: xxx`、`SBuy: xxx`）。
9: 3. **點擊刻度高亮對應數值區塊**：
10:    * 當使用者在 Canvas 上點擊某個垂直小刻度（bar）時，下方數值列中對應的項目背景會**稍微變深色**（例如 `#e5e5e5`），字體顏色加深，以利精準識別。
11:    * 下方的項目本身也綁定點擊事件，可以直接點擊項目來使其高亮。
12:    * 當滑鼠游標離開該標的的 Canvas 區塊時，高亮會自動清除，回復原本極淡配色，不留痕跡。
13: 
14: ---
15: 
16: ## 1. 檔案修改計畫
17: 
18: ### [MODIFY] [data_manager.py](file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/data_manager.py)
19: * **`fetch_history_yahoo`**：若歷史交易天數不足 20 天，使用實際天數計算 `ma20` 與 `low20`。
20: * **`compute_asset`**：完全移除對 `ma20`、`low20`、`nav` 填入
<truncated 581 bytes>
em_fm` 作為容器，內含主列 `row_fm` 與隱藏的詳細資料列 `detail_fm`。
29:   * 設定 `detail_frames` 字典以記錄各標的的詳細列 Frame。
30:   * 實作懸停整列變色處理，且不覆蓋已被選中高亮的 Label 背景色。
31:   * 在 Canvas 的 `<Leave>` 事件中，除隱藏臨時值外，一併呼叫 `_clear_highlights`。
32: * **`_draw_status_bar`**：
33:   * 在展開模式獲取 `computed` 參數時，將 fallback 預設值移除。
34:   * 在繪製垂直小刻度時，將刻度對應的 `key`（如 `'ma20'`, `'strongBuyPrice'`）寫入 `canvas.stock_coords` 對照表中。
35: * **`_render_detail_content` [NEW]**：
36:   * 動態清空並在 `detail_fm` 中渲染所有有值指標的簡寫與數值，並將建立的 Label 參照存入 `self.detail_labels`。
37:   * 綁定點擊 Label 時同樣高亮該項目。
38: * **`_toggle_detail_bar`**：
39:   * 重構展開收合行為：使用 `pack` 與 `pack_forget` 來顯示/隱藏 `detail_fm`，並呼叫 `_render_detail_content`，避免重建整個 UI。
40: * **`_on_bar_click`**：
41:   * 點擊刻度時，不呼叫 `_show_temp_val`，改為呼叫 `_highlight_detail_label` 來高亮下方對應簡寫區塊；若點擊非刻度處則清除高亮。
42: * **`_highlight_detail_label` [NEW]** / **`_clear_highlights` [NEW]**：
43:   * 根據懸停狀態安全地設定或重置下方 Label 的高亮背景色。
44: 
45: ---
46: 
47: ## 2. 驗證計畫
48: 
49: ### 手動驗證
50: 1. 啟動 `python main.py`，點選 `↻` 更新。
51: 2. 點選某股票（如 `2603`）的現價數字，確認下方立即長出新的一行，且內含 `MA`, `L20`, `Watch` 等簡寫與數值。
52: 3. 點選 Canvas 上的各垂直短刻度（bar），觀察下方對應的簡寫字樣背景是否會變灰深色，且 Canvas 上不再跳出任何字樣。
53: 4. 滑鼠移開 Canvas 時，確認下方的高亮背景是否自動收回，維持畫面乾淨。
54: 
The above content shows the entire, complete file contents of the requested file.
