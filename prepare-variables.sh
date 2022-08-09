#!/bin/bash
PATH_AIRFLOW="$(pwd)/env/airflow/"

cd ${PATH_AIRFLOW}

sed -i "s@AIRFLOW_DOCKER_REPORTS=.*@AIRFLOW_DOCKER_REPORTS='${PATH_AIRFLOW}'@" .env
sed -i "s@AIRFLOW_UID=.*@AIRFLOW_UID=$(id -u)@" .env
