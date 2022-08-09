import os
import argparse
import psycopg2
import psycopg2.extras as psyex
import pandas as pd
from pathlib import Path
from os.path import join
import consumer_query


SOURCE_FOLDER = str(Path(__file__).parents[0])
PATH_REPORTS = join(
    SOURCE_FOLDER,
    "reports",
    "{filename}.csv",
)
DW_CONNECT = {
    "host": os.environ["HOST"],
    "database": os.environ["DB"],
    "user": os.environ["USER"],
    "password": os.environ["PASSWORD"],
    "port": os.environ["PORT"],
}


def get_conn():
    try:
        return psycopg2.connect(**DW_CONNECT)
    except Exception as e:
        raise Exception("Get connection error: ", e)


def upload_data(report):
    conn = get_conn()

    consumer_df = pd.read_csv(report)
    statistics_tuple = [tuple(x) for x in consumer_df.to_numpy()]
    cols = ",".join(list(consumer_df.columns))

    query = consumer_query._CONSUMER_INSERT_STATISTICS.format(table='consumer_statistics', columns=cols)
    cursor = conn.cursor()

    try:
        psyex.execute_values(cursor, query, statistics_tuple)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise Exception('Load data error: ', e)

    cursor.close()


def execute(report):
    upload_data(PATH_REPORTS.format(filename=report))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load Reports")

    parser.add_argument("--report", required=True)
    args = parser.parse_args()

    execute(args.report)
