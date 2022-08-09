FROM python:3.8

WORKDIR /usr/src/app

COPY source/app/etls/statistic_per_vehicle/senderreport.py \ 
     source/app/services/email_sender/EmailDispacherService.py \
     env/app/statistic_per_vehicle/sender/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python3" ]