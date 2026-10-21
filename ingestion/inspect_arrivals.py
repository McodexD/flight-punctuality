import os
import json
import collections
import requests
from dotenv import load_dotenv

load_dotenv()

url = "https://api.swedavia.se/flightinfo/v2/ARN/arrivals/2026-10-21"
headers = {
    "Accept": "application/json",
    "Ocp-Apim-Subscription-Key": os.getenv("SWEDAVIA_API_KEY"),
}

response = requests.get(url, headers=headers, timeout=30)
response.raise_for_status()
data = response.json()

os.makedirs("data", exist_ok=True)
with open("data/arn_arrivals_sample.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)

flights = data["flights"]

time_keys = collections.Counter()
for flight in flights:
    time_keys.update(flight.get("arrivalTime", {}).keys())

statuses = collections.Counter(
    flight.get("locationAndStatus", {}).get("flightLegStatusEnglish")
    for flight in flights
)

print("arrivalTime fields:", dict(time_keys))
print("statuses:", dict(statuses))

for flight in flights:
    if "actualUtc" in flight.get("arrivalTime", {}):
        print(json.dumps(flight["arrivalTime"], indent=2))
        print(flight["locationAndStatus"]["flightLegStatusEnglish"])
        break
