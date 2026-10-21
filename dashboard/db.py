import os
from pathlib import Path

import pandas as pd
import snowflake.connector
import streamlit as st
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

FLIGHTS_SQL = """
select
    f.flight_key,
    f.date_key,
    d.weekday_name,
    f.direction,
    f.airport_key,
    a.display_name as airport_name,
    f.airline_key,
    coalesce(l.airline_name, f.airline_key) as airline_name,
    f.flight_status,
    f.delay_minutes,
    f.is_delayed,
    f.is_cancelled
from flights_db.marts.fact_flights as f
join flights_db.marts.dim_airport as a on f.airport_key = a.airport_key
join flights_db.marts.dim_airline as l on f.airline_key = l.airline_key
join flights_db.marts.dim_date as d on f.date_key = d.date_key
"""


@st.cache_resource
def get_connection():
    return snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["STREAMLIT_USER"],
        password=os.environ["STREAMLIT_PASSWORD"],
        role=os.environ["STREAMLIT_ROLE"],
        warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
        database=os.environ["SNOWFLAKE_DATABASE"],
    )


@st.cache_data(ttl=600)
def load_flights():
    cursor = get_connection().cursor()
    try:
        cursor.execute(FLIGHTS_SQL)
        columns = [column[0].lower() for column in cursor.description]
        return pd.DataFrame(cursor.fetchall(), columns=columns)
    finally:
        cursor.close()
