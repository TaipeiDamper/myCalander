import json
import os
import urllib.request
import time
import threading

class StockDataManager:
    """處理股票數據的載入、儲存與網路請求"""
    
    def __init__(self, config_path):
        self.config_path = config_path
        self.config_data = self.load_config()

    def load_config(self):
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
        
        # 預設值
        return {
            "update_interval_seconds": 60,
            "stocks": [
                {"symbol": "tse_0050", "reference": 190.0},
                {"symbol": "tse_2330", "reference": 800.0}
            ]
        }

    def save_stock_params(self, symbol, params):
        """儲存特定股票的參數 (參考價, 警報門檻)"""
        changed = False
        for stock in self.config_data.get("stocks", []):
            if stock.get("symbol") == symbol:
                stock.update(params)
                changed = True
                break
        
        if changed:
            return self._save_to_disk()
        return False

    def update_global_config(self, params):
        """更新全局設定 (預設門檻, 顏色強度)"""
        self.config_data.update(params)
        return self._save_to_disk()

    def _save_to_disk(self):
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config_data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False

    def fetch_prices(self, callback):

        """非同步抓取價格資料"""
        def task():
            try:
                data = self._do_fetch()
                callback(data)
            except Exception as e:
                print(f"Fetch error: {e}")
                callback({})

        threading.Thread(target=task, daemon=True).start()

    def _do_fetch(self):
        stocks = self.config_data.get("stocks", [])
        if not stocks: return {}

        query_parts = []
        symbol_map = {} 
        for s in stocks:
            key = s.get("symbol", "")
            if not key: continue
            query_parts.append(f"{key}.tw")
            symbol_map[key.split('_')[-1]] = key

        ts = int(time.time() * 1000)
        url = f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={'|'.join(query_parts)}&json=1&delay=0&_={ts}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        updates = {}
        with urllib.request.urlopen(req, timeout=5) as res:
            raw = json.loads(res.read())
            if 'msgArray' not in raw: return {}
            
            for item in raw['msgArray']:
                code = item.get('c')
                config_symbol = symbol_map.get(code)
                if not config_symbol: continue
                
                # 數據解析邏輯
                parsed = self._parse_item(item)
                if parsed:
                    updates[config_symbol] = parsed
        
        # 檢查預警實例
        alerts = self._check_alerts(updates)
        return {"updates": updates, "alerts": alerts}

    def _check_alerts(self, updates):
        """檢查股票預警：短線看昨收差異，長線看基準價差異"""
        alerts = []
        global_short = self.config_data.get("alert_threshold_short", 5.0)
        global_long = self.config_data.get("alert_threshold_long", 15.0)
        
        stocks_config = {s['symbol']: s for s in self.config_data.get("stocks", [])}
        
        for symbol, data in updates.items():
            prev, curr, high, low, hint = data
            s_cfg = stocks_config.get(symbol, {})
            ref = s_cfg.get('reference', 0)
            if ref == 0: continue
            
            # 優先使用個股設定，若無則用全局預設
            short_th = s_cfg.get('alert_short', global_short)
            long_th = s_cfg.get('alert_long', global_long)
            
            # 短線預警：跟昨日收盤比 (prev)
            diff_short_pct = abs((curr - prev) / prev * 100) if prev > 0 else 0
            # 長線預警：跟參考價基準價比 (ref)
            diff_long_pct = abs((curr - ref) / ref * 100)
            
            if diff_long_pct >= long_th:
                alerts.append({
                    "symbol": symbol.split('_')[-1],
                    "type": "LONG",
                    "value": diff_long_pct,
                    "price": curr
                })
            elif diff_short_pct >= short_th:
                alerts.append({
                    "symbol": symbol.split('_')[-1],
                    "type": "SHORT",
                    "value": diff_short_pct,
                    "price": curr
                })
        return alerts



    def _parse_item(self, item):

        def parse_f(v, default=0.0):
            if v == '-' or v is None: return default
            try: return float(v)
            except: return default

        # 價格優先級：成交價(z) > 賣標(a) > 買標(b) > 昨收(y)
        z = item.get('z', '-')
        a = item.get('a', '-').split('_')[0] if item.get('a', '-') != '-' else '-'
        b = item.get('b', '-').split('_')[0] if item.get('b', '-') != '-' else '-'
        y = item.get('y', '0')

        curr_str = '-'
        if z != '-': curr_str = z
        elif a != '-': curr_str = a
        elif b != '-': curr_str = b
        else: curr_str = y

        curr_val = parse_f(curr_str)
        prev_val = parse_f(item.get('y'), curr_val)
        high_val = parse_f(item.get('h'), curr_val)
        low_val = parse_f(item.get('l'), curr_val)
        
        hint = 4 if "." in str(curr_str) and len(str(curr_str).split(".")[1]) > 2 else 2
        return (prev_val, curr_val, high_val, low_val, hint)
