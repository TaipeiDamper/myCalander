import urllib.request
import json
from datetime import datetime

lat, lon = 25.0478, 121.5319
url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=time,weather_code,temperature_2m&hourly=time,weather_code,temperature_2m&timezone=auto&forecast_days=1"

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=5) as res:
        data = json.loads(res.read())
        print(f"Current time from API: {data.get('current', {}).get('time')}")
        print(f"First 5 hourly times: {data.get('hourly', {}).get('time')[:5]}")
except Exception as e:
    print('ERROR:', e)
