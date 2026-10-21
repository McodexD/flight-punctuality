import io

import dlt
import pandas as pd
import requests

HEADERS = {"User-Agent": "flight-punctuality-student-project/1.0"}
AIRLINES_URL = "https://en.wikipedia.org/wiki/List_of_airline_codes"
AIRPORTS_URL = "https://en.wikipedia.org/wiki/List_of_international_airports_by_country"


def load_tables(url):
    response = requests.get(url, headers=HEADERS, timeout=60)
    response.raise_for_status()
    return pd.read_html(io.StringIO(response.text))


def to_records(table):
    cleaned = table.astype(object).where(table.notna(), None)
    return cleaned.to_dict("records")


def airline_rows():
    for table in load_tables(AIRLINES_URL):
        columns = [str(column) for column in table.columns]
        if "IATA" in columns and "Airline" in columns:
            return to_records(table)
    return []


def airport_rows():
    wanted = ["Location", "Airport", "IATA Code"]
    for table_number, table in enumerate(load_tables(AIRPORTS_URL)):
        columns = [str(column) for column in table.columns]
        if all(column in columns for column in wanted):
            subset = table[wanted].dropna(subset=["IATA Code"])
            for record in to_records(subset):
                record["source_table_number"] = table_number
                yield record


@dlt.source(name="wikipedia")
def wikipedia_source():
    @dlt.resource(name="wikipedia_airlines", write_disposition="replace")
    def wikipedia_airlines():
        yield airline_rows()

    @dlt.resource(name="wikipedia_airports", write_disposition="replace")
    def wikipedia_airports():
        yield from airport_rows()

    return wikipedia_airlines, wikipedia_airports
