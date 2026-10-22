import sys
from pathlib import Path

from dagster import (
    AssetSelection,
    Definitions,
    ScheduleDefinition,
    asset,
    define_asset_job,
)
from dbt.cli.main import dbtRunner
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
DBT_DIR = ROOT / "transformation"

sys.path.insert(0, str(ROOT / "ingestion"))
load_dotenv(ROOT / ".env")

import pipeline as swedavia_pipeline
import wikipedia_pipeline


def run_dbt(command):
    arguments = [command, "--project-dir", str(DBT_DIR), "--profiles-dir", str(DBT_DIR)]
    result = dbtRunner().invoke(arguments)
    if not result.success:
        raise RuntimeError(f"dbt {command} failed: {result.exception}")


@asset(group_name="ingestion")
def swedavia_raw():
    swedavia_pipeline.run()


@asset(group_name="ingestion")
def wikipedia_raw():
    wikipedia_pipeline.run()


@asset(deps=[swedavia_raw, wikipedia_raw], group_name="transformation")
def dbt_models():
    run_dbt("run")


@asset(deps=[dbt_models], group_name="transformation")
def dbt_tests():
    run_dbt("test")


flight_pipeline_job = define_asset_job(
    "flight_pipeline", selection=AssetSelection.all()
)

daily_schedule = ScheduleDefinition(
    job=flight_pipeline_job,
    cron_schedule="0 6 * * *",
    execution_timezone="Europe/Stockholm",
)

defs = Definitions(
    assets=[swedavia_raw, wikipedia_raw, dbt_models, dbt_tests],
    jobs=[flight_pipeline_job],
    schedules=[daily_schedule],
)
