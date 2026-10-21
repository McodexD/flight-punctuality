import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

url = "https://api.swedavia.se/flightinfo/v2/ARN/arrivals/2026-10-21"
headers = {
    "Accept": "application/json",
    "Ocp-Apim-Subscription-Key": os.getenv("SWEDAVIA_API_KEY"),
}

response = requests.get(url, headers=headers, timeout=30)
print(response.status_code)

if response.ok:
    data = response.json()
    print(data.get("numberOfFlights"))
    flights = data.get("flights", [])
    if flights:
        print(json.dumps(flights[0], indent=2, ensure_ascii=False))
else:
    print(response.text[:500])
