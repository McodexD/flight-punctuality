import os

import dlt
from dotenv import load_dotenv

from swedavia_source import swedavia_source

load_dotenv()


def build_destination():
    return dlt.destinations.snowflake(
        credentials={
            "database": os.environ["SNOWFLAKE_DATABASE"],
            "username": os.environ["DLT_USER"],
            "password": os.environ["DLT_PASSWORD"],
            "host": os.environ["SNOWFLAKE_ACCOUNT"],
            "warehouse": os.environ["SNOWFLAKE_WAREHOUSE"],
            "role": os.environ["DLT_ROLE"],
        }
    )


def run():
    pipeline = dlt.pipeline(
        pipeline_name="swedavia_flights",
        destination=build_destination(),
        dataset_name="raw",
    )
    source = swedavia_source(
        os.environ["SWEDAVIA_API_KEY"],
        os.environ["SWEDAVIA_AIRPORT_KEY"],
    )
    print(pipeline.run(source))


if __name__ == "__main__":
    run()
