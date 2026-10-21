import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

url = "https://api.swedavia.se/airportinfo/v2/airports"
headers = {
    "Accept": "application/json",
    "Ocp-Apim-Subscription-Key": os.getenv("SWEDAVIA_AIRPORT_KEY"),
}

response = requests.get(url, headers=headers, timeout=30)
print(response.status_code)

if not response.ok:
    print(response.text[:500])
    raise SystemExit

data = response.json()

os.makedirs("data", exist_ok=True)
with open("data/airports_sample.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)

print(type(data).__name__)

if isinstance(data, list):
    items = data
else:
    items = next((v for v in data.values() if isinstance(v, list)), [])

print(len(items))
if items:
    print(json.dumps(items[0], indent=2, ensure_ascii=False)[:1500])
