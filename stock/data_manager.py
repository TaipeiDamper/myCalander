import json
import os
import urllib.request
import time
import threading
import datetime

class StockDataManager:
    """處理股票數據的載入、儲存與網路請求"""
    
    def __init__(self, config_path):
        self.config_path = config_path
        self.config_data = self.load_config()
        self.computed_assets = {}
        self.indices_history = {}

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
        
        # 格式化數值型態參數，避免寫入 string 格式
        formatted_params = {}
        for k, v in params.items():
            if k in ["ma20", "low20", "wa5", "nav", "reference"]:
                try:
                    formatted_params[k] = float(v) if v not in [None, '', '-'] else None
                except:
                    formatted_params[k] = None
            else:
                formatted_params[k] = v

        for stock in self.config_data.get("stocks", []):
            if stock.get("symbol") == symbol:
                stock.update(formatted_params)
                if "alert_long" in stock and "alert_long_up" in formatted_params:
                    del stock["alert_long"]
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

    def fetch_history_yahoo(self, symbol):
        """抓取 Yahoo Finance 歷史資料並計算 ma20、low20 與 wa5"""
        if '_' in symbol:
            parts = symbol.split('_')
            market, code = parts[0], parts[1]
            suffix = "TW" if market == "tse" else "TWO"
            yahoo_sym = f"{code}.{suffix}"
        else:
            yahoo_sym = symbol
        
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{yahoo_sym}?range=2mo&interval=1d"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req, timeout=10) as res:
                data = json.loads(res.read().decode('utf-8'))
                chart = data.get("chart", {})
                result = chart.get("result", [{}])[0]
                indicators = result.get("indicators", {})
                quote = indicators.get("quote", [{}])[0]
                close_prices = quote.get("close", [])
                close_prices = [p for p in close_prices if p is not None]
                n_days = len(close_prices)
                if n_days > 0:
                    use_days = min(n_days, 20)
                    last_prices = close_prices[-use_days:]
                    ma20 = sum(last_prices) / use_days
                    low20 = min(last_prices)
                    
                    use_days_5 = min(n_days, 5)
                    last_prices_5 = close_prices[-use_days_5:]
                    wa5 = sum(last_prices_5) / use_days_5
                    
                    return round(ma20, 2), round(low20, 2), round(wa5, 2)
        except Exception as e:
            print(f"Error fetching history for {symbol} via Yahoo: {e}")
        return None

    def compute_asset(self, asset):
        """依據股票或 ETF 屬性，自動產生參考價、觀察價、買進價、強烈買進價與折溢價分析狀態"""
        def round2(n):
            if n is None: return None
            return round(float(n), 2)

        symbol = asset.get("symbol", "")
        asset_type = asset.get("type", "stock")
        last_price = asset.get("lastPrice", 0.0)
        ma20 = asset.get("ma20")
        low20 = asset.get("low20")
        wa5 = asset.get("wa5")
        nav = asset.get("nav")
        high = asset.get("high")
        low = asset.get("low")

        premium_discount = None
        reference_price = None
        reference_type = ""

        if asset_type == "stock":
            if ma20 is not None and low20 is not None:
                reference_price = min(ma20, low20 * 1.02)
                reference_type = "hybrid_stock"
            else:
                reference_price = None
                reference_type = "missing_parameters"
        else: # etf
             if ma20 is not None:
                 if nav is not None and nav > 0:
                     premium_discount = (last_price - nav) / nav
                     reference_price = min(ma20, nav * 0.995)
                     reference_type = "hybrid_etf"
                 else:
                     reference_price = ma20
                     reference_type = "etf_ma20_only"
             else:
                 reference_price = None
                 reference_type = "missing_parameters"

        watch_price = None
        buy_price = None
        strong_buy_price = None
        status = "normal"

        if reference_price is not None:
            reference_price = round2(reference_price)
            watch_price = round2(reference_price)
            buy_price = round2(reference_price * 0.97)
            strong_buy_price = round2(reference_price * 0.94)

            if last_price <= strong_buy_price:
                status = "strong_buy"
            elif last_price <= buy_price:
                status = "buy"
            elif last_price <= watch_price:
                status = "watch"

        if asset_type == "etf" and premium_discount is not None:
            
            if premium_discount > 0.01 and status != "normal":
                status = "normal"
            elif premium_discount < -0.01 and status == "normal":
                status = "watch"

        return {
            "symbol": symbol,
            "type": asset_type,
            "lastPrice": last_price,
            "high": round2(high),
            "low": round2(low),
            "ma20": round2(ma20),
            "low20": round2(low20),
            "wa5": round2(wa5),
            "nav": round2(nav),
            "referencePrice": reference_price,
            "watchPrice": watch_price,
            "buyPrice": buy_price,
            "strongBuyPrice": strong_buy_price,
            "status": status,
            "premium_discount": premium_discount
        }

    def _do_fetch(self):
        stocks = self.config_data.get("stocks", [])
        if not stocks: return {}

        # 1. 抓取即時價格
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
                
                parsed = self._parse_item(item)
                if parsed:
                    updates[config_symbol] = parsed
        
        # 2. 盤中如果包含 ETF，一併獲取最新即時淨值
        has_etf = any(s.get("symbol", "").split('_')[-1].startswith('00') for s in stocks)
        etf_navs = {}
        if has_etf:
            try:
                url_etf = "https://mis.twse.com.tw/stock/data/all_etf.txt"
                req_etf = urllib.request.Request(url_etf, headers={'User-Agent': 'Mozilla/5.0'})
                import ssl
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                with urllib.request.urlopen(req_etf, context=ctx, timeout=10) as res_etf:
                    etf_data = json.loads(res_etf.read().decode('utf-8'))
                    a1 = etf_data.get("a1", [])
                    for company in a1:
                        msg_array = company.get("msgArray", [])
                        for item in msg_array:
                            code = item.get("a")
                            if code:
                                nav_str = item.get("f")
                                try:
                                    if nav_str and nav_str != "-":
                                        etf_navs[code] = float(nav_str)
                                except:
                                    pass
            except Exception as e:
                print(f"Error fetching ETF NAVs: {e}")

        # 3. 更新設定檔中的歷史數據與淨值
        today_str = datetime.date.today().strftime("%Y-%m-%d")
        config_changed = False
        
        for s in stocks:
            symbol = s.get("symbol", "")
            if not symbol: continue
            
            is_etf = symbol.split('_')[-1].startswith('00') or s.get("type") == "etf"
            if is_etf and s.get("type") != "etf":
                s["type"] = "etf"
                config_changed = True
            elif not is_etf and s.get("type") != "stock":
                s["type"] = "stock"
                config_changed = True
                
            last_up = s.get("history_updated_at", "")
            if not s.get("ma20") or not s.get("low20") or not s.get("wa5") or last_up != today_str:
                res_hist = self.fetch_history_yahoo(symbol)
                if res_hist:
                    s["ma20"], s["low20"], s["wa5"] = res_hist
                    s["history_updated_at"] = today_str
                    config_changed = True
                    
            if is_etf:
                code = symbol.split('_')[-1]
                nav_val = etf_navs.get(code)
                if nav_val is not None and nav_val != s.get("nav"):
                    s["nav"] = nav_val
                    config_changed = True
                    
        if config_changed:
            self._save_to_disk()

        # 4. 計算三層價格與狀態分析
        self.computed_assets = {}
        for symbol, parsed in updates.items():
            prev, curr, high, low, hint = parsed
            s_cfg = next((x for x in stocks if x.get("symbol") == symbol), {})
            
            asset_data = {
                "symbol": symbol.split('_')[-1],
                "type": s_cfg.get("type", "stock"),
                "lastPrice": curr,
                "ma20": s_cfg.get("ma20"),
                "low20": s_cfg.get("low20"),
                "wa5": s_cfg.get("wa5"),
                "nav": s_cfg.get("nav"),
                "high": high,
                "low": low
            }
            computed = self.compute_asset(asset_data)
            self.computed_assets[symbol] = computed

        # 5. 檢查預警實例
        alerts = self._check_alerts(updates)

        # 6. 抓取全球參考指標
        indices = {}
        index_symbols = {
            "^N225": "日經",
            "^KS11": "韓股",
            "^SOX": "費半",
            "CL=F": "油價"
        }
        today_str = datetime.date.today().strftime("%Y-%m-%d")
        for sym, name in index_symbols.items():
            try:
                # 取得歷史均線 (MA20 與 WA5)
                hist = self.indices_history.get(sym)
                if not hist or hist.get("updated_at") != today_str:
                    res_hist = self.fetch_history_yahoo(sym)
                    if res_hist:
                        ma20, low20, wa5 = res_hist
                        self.indices_history[sym] = {
                            "ma20": ma20,
                            "low20": low20,
                            "wa5": wa5,
                            "updated_at": today_str
                        }
                
                url_idx = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range=1d&interval=1m"
                req_idx = urllib.request.Request(url_idx, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req_idx, timeout=3) as res_idx:
                    idx_data = json.loads(res_idx.read().decode('utf-8'))
                    meta = idx_data.get("chart", {}).get("result", [{}])[0].get("meta", {})
                    price = meta.get("regularMarketPrice")
                    prev_close = meta.get("previousClose")
                    high = meta.get("regularMarketDayHigh", price)
                    low = meta.get("regularMarketDayLow", price)
                    price_hint = meta.get("priceHint", 2)
                    if price is not None and prev_close is not None:
                        cached = self.indices_history.get(sym, {})
                        ma20 = cached.get("ma20")
                        wa5 = cached.get("wa5")
                        # 回傳格式統一為 (prev, curr, high, low, hint, ma20, wa5)
                        indices[sym] = (prev_close, price, high, low, price_hint, ma20, wa5)
            except Exception as e:
                print(f"Error fetching index {sym}: {e}")

        return {"updates": updates, "alerts": alerts, "indices": indices}

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
            
            short_th = s_cfg.get('alert_short', global_short)
            long_up_th = s_cfg.get('alert_long_up', s_cfg.get('alert_long', global_long))
            long_down_th = s_cfg.get('alert_long_down', s_cfg.get('alert_long', global_long))
            
            diff_short_pct = abs((curr - prev) / prev * 100) if prev > 0 else 0
            diff_long_up_pct = (curr - ref) / ref * 100 if ref > 0 else 0
            diff_long_down_pct = (ref - curr) / ref * 100 if ref > 0 else 0
            
            if diff_long_up_pct >= long_up_th:
                alerts.append({
                    "symbol": symbol.split('_')[-1],
                    "type": "LONG_UP",
                    "value": diff_long_up_pct,
                    "price": curr
                })
            elif diff_long_down_pct >= long_down_th:
                alerts.append({
                    "symbol": symbol.split('_')[-1],
                    "type": "LONG_DOWN",
                    "value": diff_long_down_pct,
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
        
        try:
            clean_str = str(float(curr_str))
            hint = len(clean_str.split(".")[1]) if "." in clean_str else 0
            hint = max(2, hint)
        except:
            hint = 2
        return (prev_val, curr_val, high_val, low_val, hint)
