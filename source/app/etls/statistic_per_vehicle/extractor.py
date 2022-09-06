import argparse
import os
from collections.abc import Iterable
from os import path
from pathlib import Path

import dask.dataframe as daskdf
import pandas as pd
from pandas import DataFrame

SOURCE_FOLDER = str(Path(__file__).parents[0])
REPORT_PATH = path.join(
    SOURCE_FOLDER,
    "reports",
    "consumer-{month}-{year}.csv",
)
S3_TRIP_TOPIC_URI = path.join(
    "s3://trip-statistics/topics/kconnectpsql.public.trip",
    "year={year}",
    "month={month}/",
)


def extract_report(report: pd.DataFrame, report_path: str) -> None:
    report.to_csv(
        report_path,
        columns=[
            "after.vehicle_id",
            "after.id",
            "after.total_distance",
            "total_moving_h",
            "total_idle_h",
        ],
        header=[
            "vehicle_id",
            "total_trips",
            "total_distance",
            "total_moving",
            "total_idle",
        ],
        index=False,
    )


def prepare_report(report: DataFrame) -> pd.DataFrame:
    report = report.compute()
    report[["total_moving_h", "total_idle_h"]] = pd.DataFrame(
        report.converted_time_measure.tolist(), index=report.index
    )
    return report


def seconds_to_hours(*argv) -> Iterable[float]:
    for arg in argv:
        yield arg / 3600


def convert_time_measure(report: DataFrame) -> DataFrame:
    return report.apply(
        lambda x: list(seconds_to_hours(
            x['after.total_moving'], x['after.total_idle'])),
        meta=report['after.total_moving'],
        axis=1,
    )


def convert_measures(report: DataFrame) -> pd.DataFrame:
    report["converted_time_measure"] = convert_time_measure(report=report)
    return report


def read_statistics(month: str, year: str) -> DataFrame:
    return daskdf.read_parquet(
        S3_TRIP_TOPIC_URI.format(year=year, month=month),
        engine="fastparquet",
        columns=[
            "after.id",
            "after.vehicle_id",
            "after.total_distance",
            "after.total_moving",
            "after.total_idle",
        ],
        ignore_metadata_file=True,
    )


def get_vehicle_statistics(statistics: DataFrame) -> DataFrame:
    return (
        statistics.groupby(["after.vehicle_id"])
        .agg(
            {
                "after.id": "count",
                "after.total_distance": "sum",
                "after.total_moving": "sum",
                "after.total_idle": "sum",
            }
        )
        .reset_index()
    )


def valid_process(report: str) -> None:
    if os.path.exists(report):
        raise FileExistsError(
            f'{"The process has already been executed this month"}')


def execute(month: str, year: str) -> None:
    report_path = REPORT_PATH.format(month=month, year=year)

    valid_process(report=report_path)
    consumer_report = get_vehicle_statistics(
        statistics=read_statistics(month=month, year=year)
    )
    consumer_report = convert_measures(consumer_report)
    consumer_report = prepare_report(consumer_report)
    extract_report(report=consumer_report, report_path=report_path)


def parse_args() -> tuple:
    parser = argparse.ArgumentParser(description="Extract Reports")
    parser.add_argument("--month", required=True)
    parser.add_argument("--year", required=True)
    args = parser.parse_args()
    return args.month, args.year


if __name__ == "__main__":
    args = parse_args()
    execute(month=args[0], year=args[1])
