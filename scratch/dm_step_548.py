Created At: 2026-05-22T04:45:22Z
Completed At: 2026-05-22T04:45:22Z
File Path: `file:///C:/Users/ASAHI/.gemini/antigravity-ide/brain/4c70f361-ddc2-4366-bf46-5d2ced6e799e/walkthrough.md`
Total Lines: 46
Total Bytes: 5162
Showing lines 1 to 46
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
1: # 修改成果彙整與驗證說明 (Walkthrough)
2: 
3: 此修改完成了股票與 ETF 指標的實體自動更新機制，並依據您的最新要求重新設計了展開詳細數值列的互動 UI。
4: 
5: ## 1. 變更項目
6: 
7: ### [data_manager.py](file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/data_manager.py)
8: * **適應新上市標的歷史天數**：
9:   * 修改 `fetch_history_yahoo` 方法。若標的上市日數不足 20 天（如 `00403A`），則以其實際拥有的全部歷史交易日數計算其 `ma20` 與 `low20` 均線和最低值，不再回傳 `None`。
10: * **完全移除當日現價 Fallback**：
11:   * 重構 `compute_asset` 方法。移除使用當日價格模擬替代歷史參數（`ma20`、`low20` 與 `nav`）的邏輯。若欄位缺失，三層價格與狀態將直接保留為 `None`/`normal`。
12: * **持久化自動更新**：
13:   * 修正 `_do_fetch` 中 ETF 即時淨值 `nav` 產生變動時的存檔標記。
14:   * 移除 `_do_fetch` 的 `asset_data` 當日價格 fallback 預設值，並改在 `_do_fetch` 的函式結尾處統一呼叫 `_save_to_disk`。如此一來，每當背景執行緒抓取到最新的 `ma20`、`low20` 與盤中 `nav` 淨值時，均會自動將這些實體欄位更新回 `stock_config.json` 設定檔中。
15: 
16: ### [stock_widget.py](file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/stock_widget.py)
17: * **主列與詳細列之雙層布局 (item_fm)**：
18:   * 重構了 `_build_expanded_ui` 的股
<truncated 1811 bytes>
疊的影響。
30:   * **跨元件移動高亮保持 (Hover Boundary Refinement)**：將高亮清除邏輯由原本的「滑鼠移開 Canvas 立刻清除」優化為「滑鼠完全移開整檔股票容器（`item_fm`）時才清除」。在 `on_leave` 事件中，透過 `winfo_containing` 精準判斷，使滑鼠在主列與下方數值列之間移動時高亮依然完美保持，移出後自動收回。
31:   * **背景刷新高亮持久化 (Highlight State Persistence)**：於初始化中引入 `self.highlighted_keys`，使使用者正選取高亮的指標在背景定時重新抓取數據、重建 Label 時能被完美保留，不會因數據自動刷新而突然消失。
32: * **指標列精簡 [NEW]**：
33:   * 只保留 `MA`、`NAV`（若為 ETF）與 `SBuy`（強烈買進價）三個關鍵指標，其餘如 `L20`、`Watch`、`Buy` 等多餘或常有重合的指標已被徹底剔除。
34:   * Canvas 上的垂直參考刻度（小凸起 bar）與下方詳細列的簡寫 Labels 已同步精簡為此三項，點擊與視覺對應上皆更加清爽一緻。
35: 
36: ---
37: 
38: ## 2. 驗證說明
39: 
40: 1. **語法編譯檢查**：
41:    * 透過 Python py_compile 模組編譯了 [data_manager.py](file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/data_manager.py) 與 [stock_widget.py](file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/stock_widget.py)，皆編譯成功，無語法錯誤。
42: 2. **手動測試導引**：
43:    * 啟動日曆主程式。點擊某股票（如 2603 或新上市的 00403A）之價格數字，該股票下方應會動態長出一行，顯示其歷史參數如 `MA`、`L20` 等。
44:    * 點選該 Canvas 上的小凸起（垂直短線），下方相對應的項目（如 `MA` 或 `Watch`）背景會變深灰色高亮。
45:    * 滑鼠移開 Canvas 時高亮立刻消失，且點擊時 Canvas 本身不會跑出任何文字干擾。
46: 
The above content shows the entire, complete file contents of the requested file.
