import os
import argparse
import pandas as pd
import consumer_query
from pathlib import Path
from os import path
from sqlalchemy import create_engine   



SOURCE_FOLDER = str(Path(__file__).parents[0])
PATH_REPORTS = path.join(
    SOURCE_FOLDER,
    "reports",
    "{filename}.csv",
)


def get_engine():
    return create_engine(url=os.environ["PURL"])


def extract_report(report, consumer_id):
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
        consumer_report = pd.read_sql(consumer_query.CONSUMER_GET_STATISTICS, conn)

    extract_report(consumer_report, report_name)


def parse_args() -> str:
    parser = argparse.ArgumentParser(description="Extract Reports")
    parser.add_argument("--report", required=True)
    args = parser.parse_args()
    print(type(args.report))
    return args.report


if __name__ == "__main__":
    execute(report_name=parse_args())
    