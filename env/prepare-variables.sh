#!/bin/bash
PATH_AIRFLOW="$(pwd)/env/airflow/"
PATH_DW="$(pwd)/source/data/statistic_per_vehicle/" 
PATH_KAFKA="$(pwd)/env/kafka"
PATH_DAGS="$(pwd)/source/app/dags"

EMAIL=$1
AWS_ACCESS_KEY_ID=$2
AWS_SECRET_ACCESS_KEY=$3

cd ${PATH_AIRFLOW}

sed -i "s@AIRFLOW_DOCKER_REPORTS=.*@AIRFLOW_DOCKER_REPORTS='${PATH_DW}'@" .env
sed -i "s@AIRFLOW_UID=.*@AIRFLOW_UID=$(id -u)@" .env
sed -i "s@AIRFLOW_DOCKER_S3KEY=.*@AIRFLOW_DOCKER_S3KEY='${AWS_ACCESS_KEY_ID}'@" .env
sed -i "s@AIRFLOW_DOCKER_S3SECRET=.*@AIRFLOW_DOCKER_S3SECRET='${AWS_SECRET_ACCESS_KEY}'@" .env

cd ${PATH_KAFKA}

sed -i "s@AWS_ACCESS_KEY_ID:.*@AWS_ACCESS_KEY_ID: '${AWS_ACCESS_KEY_ID}'@" docker-compose.yml
sed -i "s@AWS_SECRET_ACCESS_KEY:.*@AWS_SECRET_ACCESS_KEY: '${AWS_SECRET_ACCESS_KEY}'@" docker-compose.yml

cd ${PATH_DAGS}

sed -i "s#'EDESTIONATION':.*#'EDESTIONATION':' ${EMAIL}',#" statistic_per_vehicle.py