Created At: 2026-05-22T02:56:09Z
Completed At: 2026-05-22T02:56:09Z
File Path: `file:///C:/Users/ASAHI/.gemini/antigravity-ide/brain/4c70f361-ddc2-4366-bf46-5d2ced6e799e/implementation_plan.md`
Total Lines: 49
Total Bytes: 3324
Showing lines 1 to 49
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
1: # 實作計畫：股票與 ETF 的三層價格監控與分析功能
2: 
3: 此計畫旨在實現點選現價（紅色區域的數字）時，彈出視窗展示個股的「自動產生參考價、觀察價、買進價、強烈買進價」分析報告，並根據股票或 ETF 的不同屬性，進行客製化折溢價與狀態判定。
4: 
5: ## User Review Required
6: 
7: > [!IMPORTANT]
8: > - 本次修改將在 `stock_config.json` 設定檔中擴展各檔標的的屬性欄位（如 `type`, `ma20`, `low20`, `nav`），並提供在 UI 設定介面調整這些屬性的功能。
9: > - 對於舊有的設定檔，系統將提供平滑的自動降級與預設值機制，確保舊資料不會導致程式異常。
10: 
11: ## Proposed Changes
12: 
13: ---
14: 
15: ### 1. 設定檔擴充
16: 
17: #### [MODIFY] [stock_config.json](file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/stock_config.json)
18: 為現有的 10 檔監控標的補齊需要的屬性：
19: - 3231 緯創設定為 `type: "stock"`，並補上 `ma20` 與 `low20`。
20: - 00403A、00981A、0050 等設定為 `type: "etf"`，並補上 `ma20`、`low20` 與 `nav`。
21: - 其他股票比照辦理。
22: 
23: ---
24: 
25: ### 2. 分析計算模組
26: 
27: #### [MODIFY] [data_manager.py](file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/data_manager.py)
28: - 實作可重用的 `compute_asset` 函數，精準實現使用者要求的 TypeScript 偽碼邏輯（包含四捨五入至小數點後二位，ETF 溢價大於 1% 的買點狀態退化等）。
29: - 在 `fetch_prices` 流程中，將抓取到的最新價格 `lastPrice` 與設定檔中的 `ma20`, `low20`, `nav` 結合，動態進行 `compute_asset` 計算，並將計算結果儲存在 `self.computed_assets` 字典中。
30: - 修改 `save_stock_params`，支援在編輯個股參數時寫入並保存 `type`, `ma20`, `low20`, `nav` 等新欄位。
31: 
32: ---
33: 
34: ### 3. UI 點擊事件與分析對話框
35: 
36: #### [MODIFY] [stock_widget.py](file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/stock_widget.py)
37: - **最新價格 Label 綁定**：在 `curr_lbl`（現價）上綁定點擊事件 `<Button-1>`，點擊時呼叫 `self._show_analysis_dialog(symbol)`。
38: - **分析報告 Dialog**：實作 `_show_analysis_dialog`，以簡潔、柔和的 HSL 色調風格彈出 Toplevel 視窗。視窗中呈現該標的的最新價格、20日均線、參考價、觀察價、買進價、強烈買進價、折溢價百分比（僅 ETF 顯示）以及當前狀態（status），並用合適的背景色標示狀態等級（如 "strong_buy" 顯示綠色，"watch" 顯示黃色等）。
39: - **參數設定介面擴充**：修改 `_show_edit_dialog`，新增 `型態 (Type)` 下拉選單/單選按鈕，以及 `ma20`、`low20`、`nav` 的輸入欄位，讓使用者可以直接在 UI 上編輯與儲存這些分析基準值。
40: 
41: ---
42: 
43: ## Verification Plan
44: 
45: ### Manual Verification
46: 1. 啟動應用程式（`python main.py`），點擊右下角股票清單的個股現價，驗證是否能順利彈出分析視窗。
47: 2. 檢查 3231（Stock）與 00403A/00981A（ETF）顯示的分析資料與狀態判定是否符合預期規則（例如：測試 ETF 溢價超過 1% 時是否強行退化為 watch）。
48: 3. 點擊個股代號，在編輯視窗中修改 `ma20` 或 `nav`，儲存後再次點擊現價，檢查分析值是否即時更新。
49: 
The above content shows the entire, complete file contents of the requested file.
