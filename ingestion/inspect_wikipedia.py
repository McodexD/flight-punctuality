import io

import pandas as pd
import requests

HEADERS = {"User-Agent": "flight-punctuality-student-project/1.0"}
AIRLINES_URL = "https://en.wikipedia.org/wiki/List_of_airline_codes"
AIRPORTS_URL = "https://en.wikipedia.org/wiki/List_of_international_airports_by_country"


def load_tables(url):
    response = requests.get(url, headers=HEADERS, timeout=60)
    response.raise_for_status()
    return pd.read_html(io.StringIO(response.text))


airline_tables = load_tables(AIRLINES_URL)
print("airline tables:", len(airline_tables))
for table in airline_tables:
    columns = [str(column) for column in table.columns]
    if "IATA" in columns and "Airline" in columns:
        print(table.shape, columns)
        print(table[table["IATA"].isin(["FR", "SK", "DY", "D8", "LH", "AY"])].to_string())
        break

airport_tables = load_tables(AIRPORTS_URL)
print("airport tables:", len(airport_tables))
for table in airport_tables:
    columns = [str(column) for column in table.columns]
    if "IATA Code" in columns and table["IATA Code"].isin(["ARN", "GOT", "BMA"]).any():
        print(columns)
        print(table.to_string())
        break
