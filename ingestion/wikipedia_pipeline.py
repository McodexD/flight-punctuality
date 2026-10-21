import dlt
from dotenv import load_dotenv

from pipeline import build_destination
from wikipedia_source import wikipedia_source

load_dotenv()


def run():
    pipeline = dlt.pipeline(
        pipeline_name="wikipedia_reference",
        destination=build_destination(),
        dataset_name="raw",
    )
    print(pipeline.run(wikipedia_source()))


if __name__ == "__main__":
    run()
