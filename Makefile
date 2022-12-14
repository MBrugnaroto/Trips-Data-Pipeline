DOCKER_COMPOSE := docker compose -f
DOCKER_BUILD := docker build . -t
DOCKER_PUSH := docker push --all-tags
USER := $(shell whoami)

all: system/env docker/source docker/airflow docker/datawarehouse docker/kibana docker/kafka system/createconnectors

system/env:
	mkdir -p source/data source/data/statistic_per_vehicle
	sh yourconfigs.sh

docker/source:
	${DOCKER_COMPOSE} ./env/datasource/docker-compose.yml up -d

docker/airflow: 
	${DOCKER_COMPOSE} ./env/airflow/docker-compose.yml up -d

docker/datawarehouse: 
	${DOCKER_COMPOSE} ./env/datawarehouse/docker-compose.yml up -d

docker/kafka:
	${DOCKER_COMPOSE} ./env/kafka/docker-compose.yml up -d

docker/kibana:
	${DOCKER_COMPOSE} ./env/kibana/docker-compose.yml up -d

system/createconnectors:
	sh env/kafka/create-source-sink-connectors.sh

docker/buildimages:
	${DOCKER_BUILD} ${USER}/extractor_vehicle_statistics:latest -t ${USER}/extractor_vehicle_statistics:v1.0 -f env/app/statistic_per_vehicle/extractor/Dockerfile
	${DOCKER_BUILD} ${USER}/loader_vehicle_statistics:latest -t ${USER}/loader_vehicle_statistics:v1.0 -f env/app/statistic_per_vehicle/loader/Dockerfile
	${DOCKER_BUILD} ${USER}/senderreport_vehicle_statistics:latest -t ${USER}/senderreport_vehicle_statistics:v1.0 -f env/app/statistic_per_vehicle/sender/Dockerfile

docker/pushimages:
	${DOCKER_PUSH} ${USER}/extractor_vehicle_statistics
	${DOCKER_PUSH} ${USER}/loader_vehicle_statistics
	${DOCKER_PUSH} ${USER}/senderreport_vehicle_statistics

docker/pruneimages:
	docker image prune -a -f

docker/prepareimages: docker/pruneimages docker/buildimages docker/pushimages

clean:
	${DOCKER_COMPOSE} ./env/kafka/docker-compose.yml down -v
	${DOCKER_COMPOSE} ./env/datasource/docker-compose.yml down -v 
	${DOCKER_COMPOSE} ./env/airflow/docker-compose.yml down -v 
	${DOCKER_COMPOSE} ./env/kibana/docker-compose.yml down -v
	${DOCKER_COMPOSE} ./env/datawarehouse/docker-compose.yml down -v
	make docker/pruneimages
