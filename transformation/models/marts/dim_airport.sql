with flight_airports as (
    select
        airport_iata,
        max(airport_icao) as airport_icao
    from {{ ref('stg_flights') }}
    group by 1
)

select
    airports.airport_iata as airport_key,
    flight_airports.airport_icao as icao_code,
    airports.airport_name,
    airports.display_name,
    wiki.city
from {{ ref('stg_airports') }} as airports
left join flight_airports
    on airports.airport_iata = flight_airports.airport_iata
left join {{ ref('stg_wikipedia_airports') }} as wiki
    on airports.airport_iata = wiki.airport_iata
