from airflow import DAG
from airflow.models import Variable
from airflow.utils.task_group import TaskGroup
from airflow.operators.bash import BashOperator
from airflow.operators.docker_operator import DockerOperator

from datetime import datetime
from docker.types import Mount

ENV = {
    'DB': Variable.get("DB"),
    'HOST': Variable.get("HOST"),
    'PORT': Variable.get("PORT"),
    'USER': Variable.get("USER"),
    'PASSWORD': Variable.get("PASSWORD"),
    'PURL': Variable.get("PURL")
}

VOLUME = [
    Mount(target='/usr/src/app/reports', source=Variable.get("REPORTS"), type='bind')
]

ARGS = {
    "owner": "root",
    "depends_on_past": False,
    "start_date": datetime(2022, 8, 1),
    "schedule_interval": "0 0 1 * *"
}

TIMESTEMP_FORMAT = '%m-%Y'

with DAG(
    dag_id="statistic_per_vehicle", 
    default_args=ARGS,
    catchup=False
) as dag:

    start = BashOperator(task_id='start', bash_command="echo 'Starting the report generation process!!'")

    extract = DockerOperator(
        task_id='extract_vehicle_statistics',
        image='mbrugnar/extractor_vehicle_statistics:latest',
        container_name='extractor_vehicle_statistics',
        command="extractor.py --report consumer-{{"f"execution_date.strftime('{ TIMESTEMP_FORMAT }')""}}",
        environment=ENV,
        force_pull=True,
        auto_remove=True,
        network_mode='debezium-compose-network',
        mounts=VOLUME
    )
    
    with TaskGroup(group_id="process_report") as process_report:
        loader = DockerOperator(
            task_id='loader_vehicle_statistics',
            image='mbrugnar/loader_vehicle_statistics:latest',
            container_name='loader_vehicle_statistics',
            command="loader.py --report consumer-{{"f"execution_date.strftime('{ TIMESTEMP_FORMAT }')""}}",
            environment=ENV,
            force_pull=True,
            auto_remove=True,
            network_mode='analytics-network',
            mounts=VOLUME
        )

        senderreport = DockerOperator(
            task_id='senderreport_vehicle_statistics',
            image='mbrugnar/senderreport_vehicle_statistics:latest',
            container_name='senderreport_vehicle_statistics',
            command="senderreport.py --month-ref {{"f"execution_date.strftime('{ '%B/Y' }')""}} --report consumer-{{"f"execution_date.strftime('{ TIMESTEMP_FORMAT }')""}}",
            environment=ENV,
            force_pull=True,
            auto_remove=True,
            mounts=VOLUME
        )

    end = BashOperator(task_id='end', bash_command="echo 'Reporting process completed successfully!!'")

    start >> extract >> process_report >> end