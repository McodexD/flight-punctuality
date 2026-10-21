with airlines as (
    select
        coalesce(airline_icao, airline_iata, 'UNKNOWN') as airline_key,
        max(airline_iata) as iata_code,
        max(airline_icao) as icao_code,
        max(airline_name) as airline_name
    from {{ ref('stg_flights') }}
    group by 1
)

select
    airlines.airline_key,
    airlines.iata_code,
    airlines.icao_code,
    airlines.airline_name,
    wiki.country_region,
    wiki.telephony_designator
from airlines
left join {{ ref('stg_wikipedia_airlines') }} as wiki
    on airlines.icao_code = wiki.airline_icao
