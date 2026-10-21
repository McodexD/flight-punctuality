with flights as (
    select * from {{ ref('stg_flights') }}
),

calculated as (
    select
        flight_key,
        cast(convert_timezone('UTC', scheduled_utc) as timestamp_ntz)::date as date_key,
        coalesce(airline_icao, airline_iata, 'UNKNOWN') as airline_key,
        airport_iata as airport_key,
        other_airport_iata,
        direction,
        flight_id,
        flight_status,
        scheduled_utc,
        estimated_utc,
        actual_utc,
        coalesce(flight_status in ('Cancelled', 'Deleted'), false) as is_cancelled,
        datediff('minute', scheduled_utc, coalesce(actual_utc, estimated_utc)) as raw_delay_minutes
    from flights
)

select
    flight_key,
    date_key,
    airline_key,
    airport_key,
    other_airport_iata,
    direction,
    flight_id,
    flight_status,
    scheduled_utc,
    estimated_utc,
    actual_utc,
    case when is_cancelled then null else raw_delay_minutes end as delay_minutes,
    case when is_cancelled or raw_delay_minutes is null then null else raw_delay_minutes > 15 end as is_delayed,
    is_cancelled
from calculated
