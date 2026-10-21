select
    icao as airline_icao,
    iata as airline_iata,
    airline as wikipedia_airline_name,
    telephony_designator,
    country_region
from {{ source('raw', 'wikipedia_airlines') }}
where icao is not null and icao <> 'n/a'
qualify row_number() over (partition by icao order by (comments is null) desc, airline) = 1
