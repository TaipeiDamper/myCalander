import urllib.request
import json

lat, lon =  25.0478, 121.5319
url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=weather_code,temperature_2m&hourly=weather_code,temperature_2m&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=auto&forecast_days=3"

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=5) as res:
        data = json.loads(res.read())
        print(json.dumps(data, indent=2))
except Exception as e:
    print('ERROR:', e)
