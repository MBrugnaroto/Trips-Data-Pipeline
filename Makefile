DOCKER_COMPOSE := docker compose -f

all: system/env docker/source docker/airflow docker/datawarehouse 

system/env:
	mkdir -p source/data source/data/statistic_per_vehicle

docker/source:
	${DOCKER_COMPOSE} ./env/datasource/docker-compose.yml up -d

docker/airflow: 
	${DOCKER_COMPOSE} ./env/airflow/docker-compose.yml up -d

docker/datawarehouse: 
	${DOCKER_COMPOSE} ./env/datawarehouse/docker-compose.yml up -d

clean:
	${DOCKER_COMPOSE} ./env/datasource/docker-compose.yml down -v 
	${DOCKER_COMPOSE} ./env/airflow/docker-compose.yml down -v 
	${DOCKER_COMPOSE} ./env/datawarehouse/docker-compose.yml down -v
	docker image prune -a -f
