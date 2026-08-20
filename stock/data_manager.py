import json
import os
import urllib.request
import time
import threading
import datetime
import concurrent.futures

class StockDataManager:
    """處理股票數據的載入、儲存與網路請求"""
    
    def __init__(self, config_path):
        self.config_path = config_path
        self.config_data = self.load_config()
        self.computed_assets = {}

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
            if k in ["ma20", "low20", "wa5", "ma60", "ma120", "nav", "reference"]:
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
        """抓取 Yahoo Finance 歷史資料並計算 ma20、low20、wa5、ma60 與 ma120"""
        if symbol.startswith('^') or '_' not in symbol:
            yahoo_sym = symbol
        else:
            parts = symbol.split('_')
            if len(parts) < 2: return None
            market, code = parts[0], parts[1]
            suffix = "TW" if market == "tse" else "TWO"
            yahoo_sym = f"{code}.{suffix}"
        
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{yahoo_sym}?range=7mo&interval=1d"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req, timeout=10) as res:
                data = json.loads(res.read().decode('utf-8'))
                chart = data.get("chart", {})
                result = chart.get("result", [{}])[0]
                indicators = result.get("indicators", {})
                quote = indicators.get("quote", [{}])[0]
                close_prices = [p for p in quote.get("close", []) if p is not None]
                high_prices = [p for p in quote.get("high", []) if p is not None]
                low_prices = [p for p in quote.get("low", []) if p is not None]
                n_days = len(close_prices)
                if n_days > 0:
                    use_days = min(n_days, 20)
                    last_closes = close_prices[-use_days:]
                    last_highs = high_prices[-use_days:] if len(high_prices) >= use_days else last_closes
                    last_lows = low_prices[-use_days:] if len(low_prices) >= use_days else last_closes

                    ma20 = sum(last_closes) / use_days
                    low20 = min(last_lows)
                    high20 = max(last_highs)
                    
                    use_days_5 = min(n_days, 5)
                    last_prices_5 = close_prices[-use_days_5:]
                    wa5 = sum(last_prices_5) / use_days_5

                    use_days_60 = min(n_days, 60)
                    last_prices_60 = close_prices[-use_days_60:]
                    ma60 = sum(last_prices_60) / use_days_60

                    use_days_120 = min(n_days, 120)
                    last_prices_120 = close_prices[-use_days_120:]
                    ma120 = sum(last_prices_120) / use_days_120
                    
                    # 計算歷史連漲跌天數
                    consec_hist = 0
                    if n_days >= 2:
                        diffs = [close_prices[i] - close_prices[i-1] for i in range(1, n_days)]
                        if diffs:
                            last_diff = diffs[-1]
                            if last_diff > 0:
                                for d in reversed(diffs):
                                    if d > 0: consec_hist += 1
                                    else: break
                            elif last_diff < 0:
                                for d in reversed(diffs):
                                    if d < 0: consec_hist -= 1
                                    else: break

                    volumes = quote.get("volume", [])
                    volumes = [v for v in volumes if v is not None]
                    last_vol = 0
                    if len(volumes) >= 2:
                        last_vol = int(volumes[-2]) # 單位：張
                    elif len(volumes) == 1:
                        last_vol = int(volumes[-1])

                    return round(ma20, 2), round(low20, 2), round(wa5, 2), round(ma60, 2), round(ma120, 2), last_vol, consec_hist, round(high20, 2)
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
        ma60 = asset.get("ma60")
        ma120 = asset.get("ma120")
        high20 = asset.get("high20")
        nav = asset.get("nav")
        high = asset.get("high")
        low = asset.get("low")

        # 動態即時校正 20H 與 20L，確保 20H 包含當日最高與現價，20L 包含當日最低與現價
        if high20 is not None:
            high20 = max(high20, last_price, high if high else last_price)
        elif high or last_price:
            high20 = max(last_price, high if high else last_price)

        if low20 is not None:
            low20 = min(low20, last_price, low if (low and low > 0) else last_price)
        elif low or last_price:
            low20 = min(last_price, low if (low and low > 0) else last_price)

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

        inst = asset.get("institutional")
        if not isinstance(inst, dict):
            f_val = asset.get("foreign", 0) if asset.get("foreign") is not None else 0
            t_val = asset.get("trust", 0) if asset.get("trust") is not None else 0
            d_val = asset.get("dealer", 0) if asset.get("dealer") is not None else 0
            inst = {
                "foreign": {"1d": f_val, "5d": f_val, "consec": 0},
                "trust": {"1d": t_val, "5d": t_val, "consec": 0},
                "dealer": {"1d": d_val, "5d": d_val, "consec": 0}
            }

        curr_vol = asset.get("currVol", 0)
        last_vol = asset.get("lastVol", 0)

        # 計算交易時間進度比例 (09:00 - 13:30, 共 270 分鐘)
        import datetime
        now = datetime.datetime.now()
        start_time = now.replace(hour=9, minute=0, second=0, microsecond=0)
        end_time = now.replace(hour=13, minute=30, second=0, microsecond=0)
        if now < start_time:
            time_fraction = 0.05
        elif now > end_time:
            time_fraction = 1.0
        else:
            elapsed = (now - start_time).total_seconds() / 60.0
            time_fraction = max(0.05, min(1.0, elapsed / 270.0))

        est_yesterday_vol = last_vol * time_fraction
        vol_diff_pct = ((curr_vol - est_yesterday_vol) / est_yesterday_vol * 100.0) if est_yesterday_vol > 0 else 0.0

        consec_hist = asset.get("consecHist", 0)
        prev_price = asset.get("prevPrice", 0.0)
        today_diff = last_price - prev_price if prev_price > 0 else 0
        if today_diff > 0:
            consec_days = (consec_hist + 1) if consec_hist >= 0 else 1
        elif today_diff < 0:
            consec_days = (consec_hist - 1) if consec_hist <= 0 else -1
        else:
            consec_days = consec_hist

        if consec_days > 0:
            consec_str = f"+{consec_days}d"
        elif consec_days < 0:
            consec_str = f"-{abs(consec_days)}d"
        else:
            consec_str = "0d"

        return {
            "symbol": symbol,
            "type": asset_type,
            "lastPrice": last_price,
            "high": round2(high),
            "low": round2(low),
            "ma20": round2(ma20),
            "low20": round2(low20),
            "high20": round2(high20) if high20 is not None else round2(high),
            "wa5": round2(wa5),
            "ma60": round2(ma60),
            "ma120": round2(ma120),
            "nav": round2(nav),
            "currVol": curr_vol,
            "lastVol": last_vol,
            "estYesterdayVol": round(est_yesterday_vol, 0),
            "volDiffPct": round(vol_diff_pct, 1),
            "consecDays": consec_days,
            "consecStr": consec_str,
            "referencePrice": reference_price,
            "watchPrice": watch_price,
            "buyPrice": buy_price,
            "strongBuyPrice": strong_buy_price,
            "status": status,
            "premium_discount": premium_discount,
            "institutional": inst
        }

    def _fetch_single_index(self, sym):
        try:
            url_idx = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range=1d&interval=1m"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
            req_idx = urllib.request.Request(url_idx, headers=headers)
            with urllib.request.urlopen(req_idx, timeout=5) as res_idx:
                idx_data = json.loads(res_idx.read().decode('utf-8'))
                meta = idx_data.get("chart", {}).get("result", [{}])[0].get("meta", {})
                price = meta.get("regularMarketPrice")
                prev_close = meta.get("previousClose")
                high = meta.get("regularMarketDayHigh", price)
                low = meta.get("regularMarketDayLow", price)
                price_hint = meta.get("priceHint", 2)
                if price is not None and prev_close is not None:
                    return sym, (prev_close, price, high, low, price_hint)
        except Exception:
            pass
        return sym, None

    def _do_fetch(self):
        stocks = self.config_data.get("stocks", [])
        if not stocks: return {}

        # 1. 抓取即時價格 (加入重試與超時防護)
        query_parts = []
        symbol_map = {} 
        for s in stocks:
            key = s.get("symbol", "")
            if not key: continue
            query_parts.append(f"{key}.tw")
            symbol_map[key.split('_')[-1]] = key

        updates = {}
        if query_parts:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
            max_retries = 1
            for attempt in range(max_retries + 1):
                try:
                    ts = int(time.time() * 1000)
                    url = f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={'|'.join(query_parts)}&json=1&delay=0&_={ts}"
                    req = urllib.request.Request(url, headers=headers)
                    with urllib.request.urlopen(req, timeout=4) as res:
                        raw = json.loads(res.read())
                        if 'msgArray' in raw:
                            for item in raw['msgArray']:
                                code = item.get('c')
                                config_symbol = symbol_map.get(code)
                                if not config_symbol: continue
                                parsed = self._parse_item(item)
                                if parsed:
                                    updates[config_symbol] = parsed
                            break
                except Exception as e:
                    if attempt < max_retries:
                        time.sleep(0.3)
                    else:
                        pass

        # 若 TWSE 伺服器異常或逾時，自動啟動 Yahoo Finance 多執行緒並行備援抓取
        if not updates and stocks:
            def fetch_yahoo_live(s_item):
                sym = s_item.get("symbol", "")
                if not sym: return None, None
                code = sym.split('_')[-1]
                suffix = '.TWO' if sym.startswith('otc_') else '.TW'
                url = f"https://query1.finance.yahoo.com/v8/finance/chart/{code}{suffix}?range=1d&interval=1m"
                try:
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
                    req = urllib.request.Request(url, headers=headers)
                    with urllib.request.urlopen(req, timeout=4) as res:
                        data = json.loads(res.read().decode('utf-8'))
                        meta = data.get('chart', {}).get('result', [{}])[0].get('meta', {})
                        curr = meta.get('regularMarketPrice')
                        prev = meta.get('previousClose')
                        high = meta.get('regularMarketDayHigh', curr)
                        low = meta.get('regularMarketDayLow', curr)
                        hint = meta.get('priceHint', 2)
                        if curr is not None and prev is not None:
                            return sym, (prev, curr, high, low, hint, 0)
                except Exception:
                    pass
                return sym, None

            with ThreadPoolExecutor(max_workers=5) as executor:
                results = list(executor.map(fetch_yahoo_live, stocks))
                for sym, val in results:
                    if sym and val:
                        updates[sym] = val

        if updates:
            self.last_updates = updates
        else:
            updates = getattr(self, "last_updates", {})

        # 2. 盤中如果包含 ETF，一併獲取最新即時淨值
        has_etf = any(s.get("symbol", "").split('_')[-1].startswith('00') for s in stocks)
        etf_navs = {}
        if has_etf:
            try:
                url_etf = "https://mis.twse.com.tw/stock/data/all_etf.txt"
                req_etf = urllib.request.Request(url_etf, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
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

        # 3. 異步更新設定檔中的歷史數據與淨值，避免阻塞即時價格抓取
        threading.Thread(target=self._update_history_and_nav_async, args=(stocks, etf_navs), daemon=True).start()

        # 4. 計算三層價格與狀態分析
        self.computed_assets = {}
        for symbol, parsed in updates.items():
            prev, curr, high, low, hint, curr_vol = parsed
            s_cfg = next((x for x in stocks if x.get("symbol") == symbol), {})
            
            asset_data = {
                "symbol": symbol.split('_')[-1],
                "type": s_cfg.get("type", "stock"),
                "lastPrice": curr,
                "prevPrice": prev,
                "ma20": s_cfg.get("ma20"),
                "low20": s_cfg.get("low20"),
                "wa5": s_cfg.get("wa5"),
                "ma60": s_cfg.get("ma60"),
                "ma120": s_cfg.get("ma120"),
                "high20": s_cfg.get("high20"),
                "nav": s_cfg.get("nav"),
                "high": high,
                "low": low,
                "currVol": curr_vol,
                "lastVol": s_cfg.get("last_vol", 0),
                "consecHist": s_cfg.get("consec_hist", 0),
                "institutional": s_cfg.get("institutional"),
                "foreign": s_cfg.get("foreign"),
                "trust": s_cfg.get("trust"),
                "dealer": s_cfg.get("dealer")
            }
            computed = self.compute_asset(asset_data)
            self.computed_assets[symbol] = computed

        # 5. 檢查預警實例
        alerts = self._check_alerts(updates)

        # 6. 並行抓取全球參考指標
        indices = {}
        index_symbols = ["^TWII", "^N225", "^KS11", "^SOX", "CL=F", "USDTWD=X", "EURTWD=X", "GBPTWD=X", "JPYTWD=X"]
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(self._fetch_single_index, sym) for sym in index_symbols]
            for f in concurrent.futures.as_completed(futures):
                sym, data = f.result()
                if data:
                    indices[sym] = data

        if "^TWII" in indices:
            prev, curr, high, low, hint = indices["^TWII"]
            twii_cfg = self.config_data.get("twii_info", {})
            asset_data = {
                "symbol": "^TWII",
                "type": "index",
                "lastPrice": curr,
                "prevPrice": prev,
                "ma20": twii_cfg.get("ma20"),
                "low20": twii_cfg.get("low20"),
                "high20": twii_cfg.get("high20"),
                "wa5": twii_cfg.get("wa5"),
                "ma60": twii_cfg.get("ma60"),
                "ma120": twii_cfg.get("ma120"),
                "high": high,
                "low": low,
                "currVol": 0,
                "lastVol": twii_cfg.get("last_vol", 0),
                "consecHist": twii_cfg.get("consec_hist", 0)
            }
            computed = self.compute_asset(asset_data)
            self.computed_assets["^TWII"] = computed

        return {"updates": updates, "alerts": alerts, "indices": indices}

    def _update_history_and_nav_async(self, stocks, etf_navs):
        """在背景執行緒中非同步更新歷史均線數據與 ETF 淨值，避免阻塞即時價格抓取"""
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
            if not s.get("ma20") or not s.get("low20") or not s.get("high20") or not s.get("wa5") or not s.get("ma60") or not s.get("ma120") or not s.get("last_vol") or "consec_hist" not in s or last_up != today_str:
                res_hist = self.fetch_history_yahoo(symbol)
                if res_hist:
                    s["ma20"], s["low20"], s["wa5"], s["ma60"], s["ma120"], s["last_vol"], s["consec_hist"], s["high20"] = res_hist
                    s["history_updated_at"] = today_str
                    config_changed = True
                    
            if is_etf:
                code = symbol.split('_')[-1]
                nav_val = etf_navs.get(code)
                if nav_val is not None and nav_val != s.get("nav"):
                    s["nav"] = nav_val
                    config_changed = True
                    
        # 非同步更新大盤歷史數據
        twii_cfg = self.config_data.setdefault("twii_info", {})
        last_up_twii = twii_cfg.get("history_updated_at", "")
        if not twii_cfg.get("ma20") or not twii_cfg.get("high20") or last_up_twii != today_str:
            res_hist = self.fetch_history_yahoo("^TWII")
            if res_hist:
                twii_cfg["ma20"], twii_cfg["low20"], twii_cfg["wa5"], twii_cfg["ma60"], twii_cfg["ma120"], twii_cfg["last_vol"], twii_cfg["consec_hist"], twii_cfg["high20"] = res_hist
                twii_cfg["history_updated_at"] = today_str
                config_changed = True

        if config_changed:
            self._save_to_disk()

    def fetch_institutional_twse(self):
        """從 TWSE 與 TPEx 抓取最近個股三大法人買賣超資料 (T86)，計算 1日、5日加總(買賣抵銷)與連N買賣"""
        import datetime, time, ssl
        today = datetime.date.today()
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        daily_maps = []
        
        # 1. 優先嘗試 TWSE OpenAPI 抓取最新單日 (超高速且不限流)
        try:
            url_openapi = "https://openapi.twse.com.tw/v1/fund/T86"
            req = urllib.request.Request(url_openapi, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(req, context=ctx, timeout=5) as res:
                raw = res.read().decode('utf-8', errors='ignore')
                data = json.loads(raw)
                if isinstance(data, list) and len(data) > 0:
                    day_map = {}
                    for item in data:
                        code = str(item.get("Code", "")).strip()
                        if not code: continue
                        def p_num(v):
                            try: return int(str(v).replace(',', ''))
                            except: return 0
                        f_net = int(p_num(item.get("ForeignInvestorsDifference", 0)) / 1000.0)
                        t_net = int(p_num(item.get("InvestmentTrustDifference", 0)) / 1000.0)
                        d_net = int(p_num(item.get("DealerDifference", 0)) / 1000.0)
                        day_map[code] = (f_net, t_net, d_net)
                    if day_map:
                        daily_maps.append(day_map)
        except Exception:
            pass

        # 2. 若需要更多歷史日進行 5日與連買賣計算，以適當間隔(避免被 TWSE 擋 IP)請求近幾日 RWD API
        needed_days = 5 if daily_maps else 6
        for days_back in range(10):
            if len(daily_maps) >= needed_days: break
            d_obj = today - datetime.timedelta(days=days_back)
            target_date_twse = d_obj.strftime("%Y%m%d")
            url_twse = f"https://www.twse.com.tw/rwd/zh/fund/T86?date={target_date_twse}&response=json"
            
            day_map = {}
            try:
                time.sleep(0.2)
                req = urllib.request.Request(url_twse, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
                with urllib.request.urlopen(req, context=ctx, timeout=4) as res:
                    raw = res.read().decode('utf-8', errors='ignore')
                    data = json.loads(raw)
                    if data.get("stat") == "OK" and "data" in data:
                        for row in data.get("data", []):
                            if len(row) >= 12:
                                code = row[0].strip()
                                def parse_num(s):
                                    try: return int(s.replace(',', ''))
                                    except: return 0
                                f_net = int(parse_num(row[4]) / 1000.0)
                                t_net = int(parse_num(row[10]) / 1000.0)
                                d_net = int(parse_num(row[11]) / 1000.0)
                                day_map[code] = (f_net, t_net, d_net)
            except Exception:
                pass

            # 抓取 TPEx (上櫃)
            try:
                roc_year = d_obj.year - 1911
                target_date_tpex = f"{roc_year}/{d_obj.month:02d}/{d_obj.day:02d}"
                url_tpex = f"https://www.tpex.org.tw/web/stock/33broker/33broker_service.php?response=json&date={target_date_tpex}"
                req_tpex = urllib.request.Request(url_tpex, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
                with urllib.request.urlopen(req_tpex, context=ctx, timeout=4) as res_tpex:
                    raw_tpex = res_tpex.read().decode('utf-8', errors='ignore')
                    data_tpex = json.loads(raw_tpex)
                    aa_data = data_tpex.get("aaData", [])
                    for row in aa_data:
                        if len(row) >= 11:
                            code = row[0].strip()
                            def parse_num(s):
                                try: return int(s.replace(',', ''))
                                except: return 0
                            f_net = int(parse_num(row[4]) / 1000.0) if len(row) > 4 else 0
                            t_net = int(parse_num(row[7]) / 1000.0) if len(row) > 7 else 0
                            d_net = int(parse_num(row[10]) / 1000.0) if len(row) > 10 else 0
                            if code not in day_map:
                                day_map[code] = (f_net, t_net, d_net)
            except Exception:
                pass

            if day_map:
                daily_maps.append(day_map)

        if not daily_maps:
            return {}

        result_map = {}
        all_codes = set()
        for m in daily_maps:
            all_codes.update(m.keys())

        for code in all_codes:
            f_history = [m[code][0] for m in daily_maps if code in m]
            t_history = [m[code][1] for m in daily_maps if code in m]
            d_history = [m[code][2] for m in daily_maps if code in m]

            def calc_stats(hist):
                if not hist: return 0, 0, 0
                n1 = hist[0]
                n5 = sum(hist[:5]) # 5日直接加總 (買賣互相抵銷)
                
                consec = 0
                if n1 > 0:
                    for v in hist:
                        if v > 0: consec += 1
                        else: break
                elif n1 < 0:
                    for v in hist:
                        if v < 0: consec -= 1
                        else: break
                return n1, n5, consec

            f_1d, f_5d, f_c = calc_stats(f_history)
            t_1d, t_5d, t_c = calc_stats(t_history)
            d_1d, d_5d, d_c = calc_stats(d_history)

            result_map[code] = {
                "foreign": {"1d": f_1d, "5d": f_5d, "consec": f_c},
                "trust": {"1d": t_1d, "5d": t_5d, "consec": t_c},
                "dealer": {"1d": d_1d, "5d": d_5d, "consec": d_c}
            }

        return result_map

    def _check_alerts(self, updates):
        """檢查股票預警：短線看昨收差異，長線看基準價差異"""
        alerts = []
        global_short = self.config_data.get("alert_threshold_short", 5.0)
        global_long = self.config_data.get("alert_threshold_long", 15.0)
        
        stocks_config = {s['symbol']: s for s in self.config_data.get("stocks", [])}
        
        for symbol, data in updates.items():
            prev, curr, high, low, hint = data[:5]
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
        
        vol_val = parse_f(item.get('v'), 0.0)
        try:
            clean_str = str(float(curr_str))
            hint = len(clean_str.split(".")[1]) if "." in clean_str else 0
            hint = max(2, hint)
        except:
            hint = 2
        return (prev_val, curr_val, high_val, low_val, hint, vol_val)
