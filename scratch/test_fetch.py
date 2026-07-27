import sys
import os

# 加入上層目錄以便匯入 stock
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stock.data_manager import StockDataManager

config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "stock", "stock_config.json")
print("Config path:", config_path)

dm = StockDataManager(config_path)
print("Initial stocks:")
for s in dm.config_data.get("stocks", [])[:3]:
    print(s.get("symbol"), "ma20:", s.get("ma20"), "ma60:", s.get("ma60"), "ma120:", s.get("ma120"))

print("\nRunning fetch...")
res = dm._do_fetch()

print("\nAfter fetch stocks:")
for s in dm.config_data.get("stocks", [])[:3]:
    print(s.get("symbol"), "ma20:", s.get("ma20"), "ma60:", s.get("ma60"), "ma120:", s.get("ma120"))
