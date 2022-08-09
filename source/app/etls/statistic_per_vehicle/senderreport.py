import os
import argparse
from pathlib import Path
from os import path
from shutil import ExecError
from EmailDispacherService import EmailDispacher


def getAttachment(report):
    if report:
        return path.join(
            str(Path(__file__).parents[0]),
            f"reports/{report}.csv"
            )
    return None


def getContent(month_ref):
    return \
    f'<p>Hello!</p> \
      <p>We are sending you the report for the month of {month_ref}.</p>\
      <p>Best regards.</p>'


def emailDispacher(report, month_ref):
    try:
        EmailDispacher(
            email_address=os.environ["EADDRESS"],
            email_password=os.environ["PASSWORD"],
            destination_email=os.environ["EDESTIONATION"],
            subject="Your report",
            content=getContent(month_ref),
            attachment=getAttachment(report)
        ).execute()
    except Exception as e:
        raise ExecError("Error sending report: ", e)


def parse_args() -> str:
    parser = argparse.ArgumentParser(description="Send Report")
    parser.add_argument("--month-ref", required=True)
    parser.add_argument("--report", required=False)
    args = parser.parse_args()
    return args.report, args.month_ref


if __name__ == "__main__":
    emailDispacher(reports=parse_args()[0], month_ref=parse_args()[1])
