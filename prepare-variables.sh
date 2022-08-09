#!/bin/bash
PATH_AIRFLOW="$(pwd)/env/airflow/"
PATH_DW="$(pwd)/source/data/statistic_per_vehicle/" 

cd ${PATH_AIRFLOW}

sed -i "s@AIRFLOW_DOCKER_REPORTS=.*@AIRFLOW_DOCKER_REPORTS='${PATH_DW}'@" .env
sed -i "s@AIRFLOW_UID=.*@AIRFLOW_UID=$(id -u)@" .env
