select
    iata_code as airport_iata,
    location as city,
    airport as wikipedia_airport_name
from {{ source('raw', 'wikipedia_airports') }}
where iata_code is not null
qualify row_number() over (partition by iata_code order by airport) = 1
