FROM python:3.8

WORKDIR /usr/src/app

COPY source/app/etls/statistic_per_vehicle/extractor.py \
     env/app/statistic_per_vehicle/extractor/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python3" ]