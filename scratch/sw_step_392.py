Created At: 2026-05-22T03:46:52Z
Completed At: 2026-05-22T03:46:52Z
File Path: `file:///C:/Users/ASAHI/.gemini/antigravity-ide/brain/4c70f361-ddc2-4366-bf46-5d2ced6e799e/implementation_plan.md`
Total Lines: 77
Total Bytes: 5253
Showing lines 1 to 77
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
1: # 實作計畫：水平價格軸「小凸起刻度」極隱蔽監控軌道 (最新修訂版)
2: 
3: 根據您的最新意見，我們修訂了實作計畫，主要調整為：
4: 1. **觸發與收回機制**：
5:    * **點選顯示**：點擊現價數字（價格數字 Label）時，展開該標的的小凸起刻度。
6:    * **離開收回**：當滑鼠游標離開該價格數字時，自動收回（隱藏）小凸起刻度，恢復為一般簡潔軌道。這免去了二次點擊的繁瑣，且極具隱密性。
7: 2. **現價指針方向**：依據今日漲跌動態調整箭頭方向（相較昨日上漲顯示向右箭頭 `▷`，下跌顯示向左箭頭 `◁`，平盤顯示對稱圓圈 `○`）。
8: 3. **橫軸外擴與端點限制 (Clamping)**：
9:    * 當展開時，橫軸價格區間以今日行情核心範圍 `[min(low, prev, curr), max(high, prev, curr)]` 為主，向左右兩側**各些微外擴該區間長度的 30%**（最小外擴為昨收的 1%）。
10:    * 若參考點價格在此擴大區間內，則以實際比例繪製。
11:    * 若超出此擴大區間太多，則**直接將其 x 座標限制在橫軸的最左端或最右端點上**，避免極端參考價將今日行情的繪製空間壓縮。
12: 
13: ## 1. 介面視覺設計
14: * **水平價格軸 (y = 12)**：
15:   * **背景參考線**：橫跨整個 Canvas 寬度（左右留 8 像素 padding，寬度為 `w - 16`），使用極淡灰色（`#e6e6e6`），作為刻度與價格的基準線。
16:   * **今日高低軌道**：在今日最低至今
<truncated 2033 bytes>

46:   * **`low20`** (20日最低價)：高度 6 像素，細線，顏色為 `StockStyle.PRIMARY_GREY`。
47:   * **`nav`** (ETF 淨值，若有)：高度 6 像素，細線，顏色為 `StockStyle.PRIMARY_GREY`。
48: * **決策警戒價**（買點/觀察點）：
49:   * **`strongBuyPrice`** (強烈買進)：高度 8 像素（上下各突出 4 像素），較明顯，顏色為 `StockStyle.PRIMARY_GREY`。
50:   * **`buyPrice`** (買進價位)：高度 8 像素，顏色為 `StockStyle.PRIMARY_GREY`。
51:   * **`watchPrice`** (觀察價位/參考價)：高度 8 像素，顏色為 `StockStyle.PRIMARY_GREY`。
52: * **折溢價退化處理**：
53:   * 當 ETF 溢價大於 1% 時，`strongBuyPrice` 與 `buyPrice` 的小凸起顏色淡化為 `#e0e0e0`。
54: 
55: ## 4. 點擊互動數值提示
56: * 點擊刻度附近，Canvas 上方會暫時顯示其對應的 `名稱: 數值`（3 秒後自動隱藏）。
57: 
58: ---
59: 
60: ## Proposed Changes
61: 
62: ### [MODIFY] [stock_widget.py](file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/stock_widget.py)
63: * 在價格數字 `curr_lbl` 上：
64:   * 點擊時（`<Button-1>`）觸發 `self._expand_bar(symbol)`。
65:   * 離開時（`<Leave>`）觸發 `self._collapse_bar(symbol)`。
66: * 重構 `_draw_status_bar` 中的坐標與現價指針繪製邏輯。
67: * 重構 `_on_bar_click` 中的最近刻度匹配邏輯，點選時顯示包含中文名稱的提示（例如：`20日均線: xxx`）。
68: 
69: ---
70: 
71: ## Verification Plan
72: 
73: ### Manual Verification
74: 1. 啟動 `python main.py`，點擊現價數字（價格數字）。
75: 2. 檢查同一條軌道上是否出現了幾個高矮不一的垂直小凸起，且現價變成了精緻的向右 `▷`（上漲）、向左 `◁`（下跌）或 `○`（持平）指針。
76: 3. 將滑鼠游標移開該價格數字，確認這些小凸起是否立刻消失，恢復為一般的簡潔軌道。
77: 
The above content shows the entire, complete file contents of the requested file.
