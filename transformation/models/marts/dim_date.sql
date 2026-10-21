with flight_dates as (
    select distinct
        cast(convert_timezone('UTC', scheduled_utc) as timestamp_ntz)::date as date_key
    from {{ ref('stg_flights') }}
    where scheduled_utc is not null
)

select
    date_key,
    year(date_key) as year,
    month(date_key) as month,
    day(date_key) as day,
    dayname(date_key) as weekday_name
from flight_dates
