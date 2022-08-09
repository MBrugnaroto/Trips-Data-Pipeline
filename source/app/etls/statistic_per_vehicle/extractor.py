import os
import argparse
import pandas as pd
from pathlib import Path
from os.path import join
from sqlalchemy import create_engine   
import consumer_query


SOURCE_FOLDER = str(Path(__file__).parents[0])
PATH_REPORTS = join(
    SOURCE_FOLDER,
    "reports",
    "{filename}.csv",
)


def get_engine():
    return create_engine(url=os.environ["PURL"])


def get_report(report, consumer_id):
    report.to_csv(
        PATH_REPORTS.format(filename=consumer_id),
        index=False
    )


def valid_process(report_name):
    file = PATH_REPORTS.format(filename=report_name)

    if os.path.exists(file):
        raise FileExistsError(f"the process has already been executed this month")


def execute(report_name):
    engine = get_engine()

    with engine.connect() as conn:
        valid_process(report_name)
        consumer_report = pd.read_sql(consumer_query._CONSUMER_GET_STATISTICS, conn)

    get_report(consumer_report, report_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract Reports")

    parser.add_argument("--report", required=True)
    args = parser.parse_args()

    execute(args.report)
