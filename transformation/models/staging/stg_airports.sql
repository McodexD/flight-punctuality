select
    iata as airport_iata,
    name as airport_name,
    display_name,
    local_display_name
from {{ source('raw', 'airports') }}
qualify row_number() over (partition by iata order by to_double(_dlt_load_id) desc) = 1
