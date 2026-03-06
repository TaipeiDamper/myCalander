# Pixel Art 動態展示區 - 構想與實作草案

## 1. 預期效果清單 (Themes & Effects)
這些是未來想要實作的 Pixel Art 小動畫，可以用來對應用戶當前的狀態或環境：
- **沙漏 (Hourglass)**：適合在番茄鐘倒數或等待時顯示。
- **釣魚 (Fishing)**：適合休閒、悠哉或閒置狀態。
- **讀書 (Reading)**：適合在啟動專注模式 (番茄鐘) 時播放。
- **下雨 (Raining)**：可以與現在的天氣 API 結合，如果當地天氣為下雨，就切換成這個動畫。
- **管線漏水 (Pipe Leaking)**：趣味性的例外狀態，例如 API 發生小錯誤或需要提醒時。
- **維修管線 (Fixing Pipe)**：適合系統資料儲存中、網路重連中，或是正在進行設定時。
- **寫程式 (Coding)**：專心打字的動畫，同樣適合工作模式。
- **唱歌 (Singing)**：休閒或是播放某種成功的音效時。
- **發呆 (Spacing out)**：當滑鼠有段時間沒有移動、程式進入閒置時。
- **作夢 (Dreaming)**：待辦清單全數完成，或是進入晚間休息時段。

## 2. 佈局與尺寸評估 (Layout & Size)
根據提供的截圖以及程式碼 `core/sidebar.py` 的分析：
- **位置**：位於「擴展側邊欄 (Sidebar)」底部的空白處 (詳細天氣下方)。
- **寬度限制**：側邊欄的總寬度預設為 `240px`。扣掉左右 padding 與內部的滾動條寬度後，**可用寬度大約落在 `180px` ~ `200px`**。
- **高度預測**：參考紅色箭頭與方框的比例，該區塊大致為正方形，因此**可用高度大約也是 `180px` ~ `220px`** 之間。
- **像素尺寸建議**：
  若想呈現復古的 Pixel Art 感，建議網格解析度控制在 **`24x24` 到 `32x32`** 內。
  例如解析度為 `32x32` 時，每個模擬像素可設為 `6x6` 實際螢幕大小，總畫面就是 `192x192` 像素，完美落在預估的可用空間內！

## 3. 實作可行性與方法 (Implementation Approaches)
在「**決不干擾其他 Agent 所寫的功能**」與「**不破壞現有架構**」的大前提下，這項功能完全可行。我們可以將其包裝成一個獨立的 Widget 塞進 `sidebar`。

### 方法 A：`tk.Canvas` 純矩陣繪製法 (如先前的測試程式)
- **作法**：把每一個動畫的每一幀(Frame)寫成二維 List（把顏色存進 Python 陣列裡），再用 `Canvas.create_rectangle` 畫上去。
- **優點**：完全不需要管理外部圖片檔案，建置成 `.exe` 時也不用怕漏圖；不需額外安裝 `Pillow` 函式庫。
- **缺點**：動畫幀數如果太多，把整個圖轉換為陣列手寫（或透過腳本轉換）會比較繁瑣。

### 方法 B：GIF / Sprite 素材與 `tk.PhotoImage`
- **作法**：使用事先做好的 `.gif` 或一系列的 `.png`。
- **優點**：可以去網路上找現成的 Pixel Art 動圖，直接掛載，程式碼非常簡潔。
- **缺點**：未來打包執行檔 (`build_exe.py`) 時需要新增對這些圖檔的資源封裝處理 (`--add-data`)。

### 方法 C：獨立動畫控制中心 (The Controller)
未來我們可以寫一支獨立的 `PixelArtController` 來聽取其他元件的廣播或讀取狀態，但彼此不互相耦合：
```python
# 概念偽代碼 (Pseudocode)
class StatefulPixelArtWidget(tk.Frame):
    def check_status(self):
        if is_raining():
            self.play_animation("raining")
        elif is_pomodoro_running():
            self.play_animation("coding")
        elif idle_time > 5_minutes:
            self.play_animation("spacing_out")
```

## 總結
1. 這個想法**非常棒且可行**，尺寸大小也能完美消化。
2. 只要遵守把 Pixel Art 元件註冊進 `self.sidebar` (或新增一個專屬 Container)，它就能跟天氣、番茄鐘等模組和平共存。
3. 接下來隨時可以依據上述的方法，挑其中一種開始陸續建立動畫庫（Animation Library）來套用！
