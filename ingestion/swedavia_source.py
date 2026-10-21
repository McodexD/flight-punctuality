from datetime import datetime, timedelta, timezone

import dlt
import requests

FLIGHT_BASE_URL = "https://api.swedavia.se/flightinfo/v2"
AIRPORT_URL = "https://api.swedavia.se/airportinfo/v2/airports"
DAYS_BACK = 3


def build_headers(api_key):
    return {"Accept": "application/json", "Ocp-Apim-Subscription-Key": api_key}


def get_airports(airport_key):
    response = requests.get(AIRPORT_URL, headers=build_headers(airport_key), timeout=30)
    response.raise_for_status()
    return response.json()


def get_dates():
    today = datetime.now(timezone.utc).date()
    return [(today - timedelta(days=offset)).isoformat() for offset in range(DAYS_BACK)]


def build_flight_key(airport, direction, flight):
    leg = flight.get("flightLegIdentifier", {})
    parts = [
        airport,
        direction,
        flight.get("flightId"),
        leg.get("flightDepartureDateUtc"),
        leg.get("departureAirportIata"),
        leg.get("arrivalAirportIata"),
    ]
    return "|".join(str(part) for part in parts)


def fetch_flights(flight_key, airport_codes, direction):
    headers = build_headers(flight_key)
    for airport in airport_codes:
        for flight_date in get_dates():
            url = f"{FLIGHT_BASE_URL}/{airport}/{direction}/{flight_date}"
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code == 404:
                continue
            response.raise_for_status()
            for flight in response.json().get("flights", []):
                flight["flight_key"] = build_flight_key(airport, direction, flight)
                flight["queried_airport_iata"] = airport
                flight["queried_date"] = flight_date
                flight["direction"] = direction
                yield flight


@dlt.source(name="swedavia")
def swedavia_source(flight_key: str, airport_key: str):
    airports = get_airports(airport_key)
    airport_codes = [airport["iata"] for airport in airports]

    @dlt.resource(name="airports", write_disposition="replace", primary_key="iata")
    def airports_resource():
        yield airports

    @dlt.resource(name="arrivals", write_disposition="append")
    def arrivals():
        yield from fetch_flights(flight_key, airport_codes, "arrivals")

    @dlt.resource(name="departures", write_disposition="append")
    def departures():
        yield from fetch_flights(flight_key, airport_codes, "departures")

    return airports_resource, arrivals, departures
