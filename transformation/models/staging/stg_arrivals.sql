select
    flight_key,
    flight_id,
    queried_airport_iata as airport_iata,
    flight_leg_identifier__arrival_airport_icao as airport_icao,
    'arrival' as direction,
    flight_leg_identifier__departure_airport_iata as other_airport_iata,
    airline_operator__iata as airline_iata,
    airline_operator__icao as airline_icao,
    airline_operator__name as airline_name,
    location_and_status__flight_leg_status_english as flight_status,
    arrival_time__scheduled_utc as scheduled_utc,
    arrival_time__estimated_utc as estimated_utc,
    arrival_time__actual_utc as actual_utc
from {{ source('raw', 'arrivals') }}
qualify row_number() over (partition by flight_key order by to_double(_dlt_load_id) desc) = 1
