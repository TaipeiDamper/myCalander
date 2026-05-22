Created At: 2026-05-22T03:46:10Z
Completed At: 2026-05-22T03:46:11Z
File Path: `file:///C:/Users/ASAHI/.gemini/antigravity-ide/brain/4c70f361-ddc2-4366-bf46-5d2ced6e799e/walkthrough.md`
Total Lines: 46
Total Bytes: 3514
Showing lines 1 to 46
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
1: # 股票與 ETF 極致隱密「小凸起刻度」Canvas 監控軌道 實作紀錄
2: 
3: 我們已經將分析警戒軌道全面重構為**同一條水平價格軸上的垂直灰色小凸起刻度**，並新增了「滑鼠游標移開即自動收回」的流暢體驗。這項設計徹底避免了額外的視覺負擔，且提供了強大的交易相對位置參考。
4: 
5: ## 變更內容摘要
6: 
7: ### 1. 水平小凸起刻度設計
8: * **檔案**：[stock_widget.py](file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/stock_widget.py)
9: * **細節**：
10:   * **點選現價展開**：點擊現價數字（價格數字）時，會在 Canvas 水平軌道上浮現數個垂直的小凸起。
11:   * **滑鼠離開收回**：滑鼠游標一離開該價格數字，凸起刻度立即自動收回，恢復日常的最簡約軌道。
12:   * **單一水平價格軸 (y = 12)**：不再向下長出第二軌，全程維持在一條線。
13:     * **背景細線**：橫跨全寬，作為長期坐標軸。
14:     * **今日高低軌道**：粗實線（寬度 4）疊加於背景線上，標示今日的實際波動區間。
15:   * **指針方向動態調整**：現價指針根據漲跌動態調整箭頭方向：
16:     * 相較昨日收盤上漲：繪製向右空心三角形 `▷`。
17:     * 相較昨日收盤下跌：繪製向左空心三角形 `◁`。
18:     * 相較昨日收盤平盤：維持空心小圓圈 `○`。
19:   * **些微擴展與端點限制 (Clamping)**：
20:     * 展開時價格區間會以
<truncated 163 bytes>
比今日低很多），則**直接限制在最左或最右端點上**，避免拉扁主要行情。
22:   * **垂直凸起高度區分**：
23:     * 背景數據 (`ma20`、`low20`、`nav`)：高度 6 像素，細線。
24:     * 決策警戒 (`strongBuyPrice`、`buyPrice`、`watchPrice`)：高度 8 像素，較明顯。
25:   * **折溢價退化淡化**：
26:     * 若 ETF 溢價大於 1%，買點（`strongBuyPrice`、`buyPrice`）刻度自動淡化為 `#e0e0e0`。
27: 
28: ### 2. 懸停點擊互動
29: * 當展開小凸起後，點擊橫軸上任何刻度附近，程式會找到最接近的刻度，並在 Canvas 上方暫時浮現其對應的中文標籤與精確價格（例如：`20日均線:140.00`），於 3 秒後自動隱藏，方便您確認數字。
30: 
31: ---
32: 
33: ## 驗證與測試步驟
34: 
35: 請在您本機的日曆視窗中進行以下操作來驗證：
36: 
37: 1. **啟動確認**：日曆程式目前已在背景重新執行。請確認股票小工具顯示正常且無任何報錯。
38: 2. **點選展開**：點擊任意股票的**最新價格（價格數字）**：
39:    * 該列的 Canvas 水平線會浮現高矮不一的垂直小凸起刻度。
40:    * 觀察現價的空心三角形是否依據今日漲跌，正確指向右邊 `▷`（如 2603 長榮）或左邊 `◁`（如 2330 台積電）。
41: 3. **離開收回**：將滑鼠移開價格數字，檢查小凸起是否瞬間消失，恢復為極簡的外觀。
42: 4. **驗證端點限制**：再次將滑鼠移到價格數字上點擊並**保持滑鼠在數字上方**：
43:    * 檢查是否有部分參考點（例如 `low20` 或 `ma20`）因為距離今日波動太大，而靠在最左端（`start_x=8`）或最右端。
44: 5. **點擊刻度提示**：在展開狀態下，點擊 Canvas 上的某個刻度（如最左側靠邊的凸起）：
45:    * 檢查 Canvas 上方是否浮現 `強烈買進:xxx` 類似字樣，且 3 秒後自動消失。
46: 
The above content shows the entire, complete file contents of the requested file.
