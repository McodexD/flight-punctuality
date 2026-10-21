select * from {{ ref('stg_arrivals') }}
union all
select * from {{ ref('stg_departures') }}
