import os
import argparse
import psycopg2
import psycopg2.extras as psyex
import pandas as pd
from pathlib import Path
from os.path import join
from generic_dml import INSERT


SOURCE_FOLDER = str(Path(__file__).parents[0])
PATH_REPORTS = join(
    SOURCE_FOLDER,
    "reports",
    "consumer-{report_date}.csv",
)
DW_CONNECT = {
    "host": os.environ["HOST"],
    "database": os.environ["DB"],
    "user": os.environ["USER"],
    "password": os.environ["PASSWORD"],
    "port": os.environ["PORT"],
}


def get_conn() -> psycopg2:
    try:
        return psycopg2.connect(**DW_CONNECT)
    except Exception as e:
        raise Exception("Get connection error: ", e)


def upload_data(report: str) -> None:
    conn = get_conn()

    consumer_df = pd.read_csv(report)
    statistics_tuple = [tuple(x) for x in consumer_df.to_numpy()]
    cols = ",".join(list(consumer_df.columns))

    query = INSERT.format(table='consumer_statistics', columns=cols)
    
    with conn.cursor() as c:
        try:
            psyex.execute_values(c, query, statistics_tuple)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise Exception('Load data error: ', e)


def execute(report_date: str) -> None:
    upload_data(report=PATH_REPORTS.format(report_date=report_date))


def parse_args() -> str:
    parser = argparse.ArgumentParser(description="Load Reports")
    parser.add_argument("--report_date", required=True)
    args = parser.parse_args()
    return args.report_date


if __name__ == "__main__":
    execute(report_date=parse_args())
