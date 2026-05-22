# Changelog

## 2026-05-22
- **功能新增**: 在 `stock_widget.py` 中的 `_draw_status_bar` 加入指標線條樣式設定，使不同指標（WA、MA、NAV、StrongBuy）具有不同的粗細與虛線樣式，以提升右側 bar 的辨識度。
  - 新增 `style_map` 於指標繪製區塊，設定
    - `wa5`: 寬度 2、實線
    - `ma20`: 寬度 2、短虛線 `(4, 2)`
    - `nav`: 寬度 2、長虛線 `(2, 4)`
    - `strongBuyPrice`: 寬度 3、實線
  - 依據 `style_map` 使用 `canvas.create_line` 繪製有對應的 `width` 與 `dash` 參數。
- 此變更已提交到 `main` 分支，未出現其他分支可比較。
