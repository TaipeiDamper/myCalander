import urllib.request
import json

lat, lon = 25.0478, 121.5319
# 移除 current= 裡面的 time，因為 time 會自動回傳，放在裡面會導致 400 Bad Request
url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=weather_code,temperature_2m&hourly=weather_code,temperature_2m&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=auto&forecast_days=3"

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=5) as res:
        data = json.loads(res.read())
        print("SUCCESS")
        print(f"Current Keys: {data.get('current', {}).keys()}")
        print(f"Current Time: {data.get('current', {}).get('time')}")
except Exception as e:
    print('ERROR:', e)
