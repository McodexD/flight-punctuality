import os
from dotenv import load_dotenv
import snowflake.connector

load_dotenv()

conn = snowflake.connector.connect(
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    user=os.getenv("DLT_USER"),
    password=os.getenv("DLT_PASSWORD"),
    role=os.getenv("DLT_ROLE"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
)
cur = conn.cursor()
cur.execute("select current_user(), current_role(), current_warehouse(), current_database()")
print(cur.fetchone())
cur.close()
conn.close()
