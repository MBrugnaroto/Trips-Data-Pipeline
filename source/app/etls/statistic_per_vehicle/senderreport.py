import os
import argparse
from pathlib import Path
from os import path
from typing import List
from EmailDispacherService import EmailDispacher


SOURCE_FOLDER = str(Path(__file__).parents[0])
REPORT_PATH = path.join(
    SOURCE_FOLDER,
    "reports",
    "consumer-{report_date}.csv",
)


def getContent(month_ref: str) -> str:
    return \
    f'<p>Hello!</p> \
      <p>We are sending you the report for the month of {month_ref}.</p>\
      <p>Best regards.</p>'


def emailDispacher(report_date: str, month_ref: str) -> None:
    try:
        EmailDispacher(
            email_address=os.environ["EADDRESS"],
            email_password=os.environ["EPASSWORD"],
            destination_email=os.environ["EDESTIONATION"],
            subject="Your monthly report",
            content=getContent(month_ref),
            attachment=REPORT_PATH.format(report_date=report_date)
        ).execute()
    except Exception as e:
        raise Exception("Report dispacher: ", e)


def parse_args() -> List[str]:
    parser = argparse.ArgumentParser(description="Send Report")
    parser.add_argument("--month-ref", required=True)
    parser.add_argument("--report_date", required=False)
    args = parser.parse_args()
    return args.report_date, args.month_ref


if __name__ == "__main__":
    args = parse_args()
    emailDispacher(report_date=args[0], month_ref=args[1])
