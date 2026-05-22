Created At: 2026-05-22T03:23:12Z
Completed At: 2026-05-22T03:23:12Z
File Path: `file:///C:/Users/ASAHI/.gemini/antigravity-ide/brain/4c70f361-ddc2-4366-bf46-5d2ced6e799e/implementation_plan.md`
Total Lines: 38
Total Bytes: 2531
Showing lines 1 to 38
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
1: # 實作計畫：無色系極隱蔽點線疏密 Canvas 分析 bar
2: 
3: 為實現絕對隱密性，我們將**完全不使用任何鮮豔色彩**。第二條動態長出的分析 bar 將全部採用低調的灰色系（與月曆小工具原本的灰色邊框/字體一致），純粹透過**線條的疏密程度與點線樣式 (Dash patterns)** 來代表不同的價格警戒區間：
4: 
5: ## 1. 線條疏密設計規範
6: 所有區間均使用統一的灰色（`StockStyle.PRIMARY_GREY`），寬度均為 1 到 2 像素：
7: * **`[90%, 94%]` 強烈買進區間**：**粗實線 (Solid Line)** -> 最密實，代表極佳買點（`width=2`）。
8: * **`[94%, 97%]` 買進區間**：**細實線 (Thin Solid Line)** -> 密實，代表可買進（`width=1`）。
9: * **`[97%, 100%]` 觀察區間**：**疏虛線 (Dashed Line)** -> 較稀疏，代表觀察（`dash=(2, 3)`）。
10: * **`[100%, 102%]` 正常區間**：**點狀線 (Dotted Line)** -> 最稀疏，代表無預警（`dash=(1, 5)`）。
11: 
12: ## 2. 折溢價退化視覺邏輯
13: 當 ETF 溢價大於 1% 導致買點退化為 `watch` 時：
14: * 彩色 bar 上的強烈買進（粗實線）與買進（細實線）區段，將自動**退化變稀疏**，繪製成與觀察區間相同的**疏虛線 (Dashed Line)**。
15: * 視覺上，原本實線的部分會變為虛線，一眼即知買點退化失效，但對外人而言只是單純的灰色點線排列。
16: 
17: ## 3. 現價指針設計
18: * 在分析軌道上，現價指針將使用一個低調的**灰色空心小圓圈**（而非紅點），輕巧地套在虛實線上，極具設計感且絲毫不顯眼。
19: 
20: ---
21: 
22: ## Proposed Changes
23: 
24: ### [MODIFY] [stock_widget.py](file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/stock_widget.py)
25: * **事件綁定**：點選現價時切換 `self.expanded_bars` 狀態，並立刻重繪。
26: * **點線重繪邏輯**：在 `_draw_status_bar` 中實作無色系的點線區間繪製，並加入退化後的線條稀疏化邏輯。
27: * **關閉舊彈窗**：刪除原先點擊現價會呼叫 `_show_analysis_dialog` 的實作（或將其改為切換 bar，不再彈出 Toplevel 視窗）。
28: 
29: ---
30: 
31: ## Verification Plan
32: 
33: ### Manual Verification
34: 1. 啟動 `python main.py`，點擊現價數字。
35: 2. 檢查 Canvas 下方是否長出第二條由灰色「實線 - 細實線 - 虛線 - 點線」組成的灰度軌道。
36: 3. 再次點擊現價數字，驗證其是否平滑收回。
37: 4. 修改 ETF 淨值使其產生大於 1% 的溢價，展開軌道驗證原本實線區段是否成功退化變稀疏。
38: 
The above content shows the entire, complete file contents of the requested file.
