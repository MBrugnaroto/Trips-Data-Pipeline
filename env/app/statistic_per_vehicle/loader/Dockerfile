FROM python:3.8

WORKDIR /usr/src/app

COPY source/app/etls/statistic_per_vehicle/loader.py \
     source/app/etls/statistic_per_vehicle/querys/generic_dml.py \
     env/app/statistic_per_vehicle/loader/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python3" ]