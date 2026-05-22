Created At: 2026-05-22T04:45:29Z
Completed At: 2026-05-22T04:45:29Z
File Path: `file:///C:/Users/ASAHI/.gemini/antigravity-ide/brain/4c70f361-ddc2-4366-bf46-5d2ced6e799e/implementation_plan.md`
Total Lines: 58
Total Bytes: 4791
Showing lines 1 to 58
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
1: # 實作計畫：參數自動更新、移除當日價格 Fallback 與下方動態數值列
2: 
3: 根據您的最新意見，我們設計了以下精緻且低調的互動機制：
4: 1. **點擊 Canvas 刻度不顯示懸浮文字**：
5:    * 移除點擊 Canvas 刻度線時在 Canvas 上方浮現 `名稱: 數值` 的懸浮文字，保持畫面的極簡與低調。
6: 2. **下方動態新增數值列**：
7:    * 當點擊現價數字展開小工具時，會在該標的列下方**新增一行**（動態 Frame）。
8:    * 該行中會精簡地列出該標的有值的 `MA`、`NAV`（若為 ETF）、與 `SBuy`（強烈買進價）之簡寫與數值，剔除其餘重複或多餘指標。
9: 3. **點擊刻度高亮對應數值區塊**：
10:    * 當使用者在 Canvas 上點擊對應這三個指標的小刻度（bar）時，下方數值列中對應的項目背景會**稍微變深色**（`#e5e5e5`），字體顏色加深。
11:    * 下方的項目本身也綁定點擊事件，可以直接點擊項目來使其高亮。
12:    * 當滑鼠游標移開這檔股票整列範圍時，高亮會自動清除，回復原本極淡配色。
13: 
14: ---
15: 
16: ## 1. 檔案修改計畫
17: 
18: ### [MODIFY] [data_manager.py](file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/data_manager.py)
19: * **`fetch_history_yahoo`**：若歷史交易天數不足 20 天，使用實際天數計算 `ma20` 與 `low20`。
20: * **`compute_asset`**：完全移除對 `ma20`、`low20`、`nav` 填入當前現價做為預設的當
<truncated 1496 bytes>
 `pack` 與 `pack_forget` 來顯示/隱藏 `detail_fm`，並呼叫 `_render_detail_content`，避免重建整個 UI。
40: * **`_on_bar_click`**：
41:   * 點擊刻度時，不呼叫 `_show_temp_val`，改為呼叫 `_highlight_detail_label` 來高亮下方對應簡寫區塊；若點擊非刻度處則清除高亮。
42: * **`_highlight_detail_label` [NEW]** / **`_clear_highlights` [NEW]**：
43:   * 根據懸停狀態安全地設定或重置下方 Label 的高亮背景色。
44: * **高亮優化 [NEW]**：
45:   * **過濾無 key 刻度**：在 `_on_bar_click` 尋找最近刻度時，過濾掉沒有 `key` 的基礎價格點（如昨日收盤、現在價格等），確保指標刻度（bar）不會被基礎價格點阻擋而點不到。
46:   * **滑鼠離開整列才清除高亮**：修改 Canvas 的 `<Leave>` 事件不立即清除高亮。而是在整列的 `on_leave` 懸停處理中，透過 `winfo_containing` 判斷滑鼠是否確實離開了這一檔股票的容器 `item_fm`，離開時才還原背景並清除高亮。這能讓滑鼠移動到詳細列時，高亮保持顯示，移出整列才乾淨收合。
47:   * **刷新時保持高亮**：在 Widget 初始化時新增 `self.highlighted_keys` 字典。點選高亮時記錄該 key，而在背景刷新資料調用 `_render_detail_content` 重建 Label 時，若該 key 依然存在則直接套用高亮，避免定時刷新時高亮無故消失。
48: 
49: ---
50: 
51: ## 2. 驗證計畫
52: 
53: ### 手動驗證
54: 1. 啟動 `python main.py`，點選 `↻` 更新。
55: 2. 點選某股票（如 `2603`）的現價數字，確認下方立即長出新的一行，且內含 `MA`, `L20`, `Watch` 等簡寫與數值。
56: 3. 點選 Canvas 上的各垂直短刻度（bar），觀察下方對應的簡寫字樣背景是否會變灰深色，且 Canvas 上不再跳出任何字樣。
57: 4. 滑鼠移開 Canvas 時，確認下方的高亮背景是否自動收回，維持畫面乾淨。
58: 
The above content shows the entire, complete file contents of the requested file.
