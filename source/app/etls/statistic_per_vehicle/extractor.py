import os
import argparse
import dask.dataframe as daskdf
from pathlib import Path
from os import path
from typing import List


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


def valid_process(report: str) -> None:
    if os.path.exists(report):
        raise FileExistsError(f"The process has already been executed this month")


def extract_report(report: daskdf, report_path: str) -> None:
    report.compute().to_csv(
        report_path,
        header=["vehicle_id", "total_trips", "total_distance", "total_moving", "total_idle"],
        index=False,
    )


def report_df(month: str, year: str) -> daskdf:
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


def get_vehicle_statistics(report_df: daskdf) -> daskdf:
    return (
        report_df.groupby(["after.vehicle_id"])
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


def execute(month: str, year: str) -> None:
    report_path = REPORT_PATH.format(month=month, year=year)

    valid_process(report=report_path)
    consumer_report = get_vehicle_statistics(
        report_df=report_df(month=month, year=year)
    )
    extract_report(report=consumer_report, report_path=report_path)


def parse_args() -> List[str]:
    parser = argparse.ArgumentParser(description="Extract Reports")
    parser.add_argument("--month", required=True)
    parser.add_argument("--year", required=True)
    args = parser.parse_args()
    return args.month, args.year


if __name__ == "__main__":
    args = parse_args()
    execute(month=args[0], year=args[1])
