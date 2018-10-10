.PHONY: all build deploy swarm stop config export import

all: ensure-directories-exist build swarm deploy config deploy-splash load-assets

ensure-directories-exist:
	mkdir -p data/arangodb
	mkdir -p data/airflow/logs
	mkdir -p data/airflow/postgres-data

clean:
	rm -fr data/arangodb
	rm -fr data/airflow/logs
	rm -fr data/airflow/postgres-data

build:
	cd custom-envs/engine-env-3  && docker build -t localrepo/fastscore-engine:env-3 .
	cd custom-envs/airflow  && docker build -t localrepo/airflow .
	cd custom-envs/engine-env-2  && docker build -t localrepo/fastscore-engine:env-2 .
	cd custom-envs/model-deploy-env-1 && docker build -t localrepo/fastscore-model-deploy:env-1 .
	#cd custom-envs/grafana-env  && docker build -t localrepo/grafana .	
	cd custom-envs/model-deploy-env-2 && docker build -t localrepo/fastscore-model-deploy:env-2 .
	cd custom-envs/kafkaesq && docker build -t localrepo/kafkaesq .
	cd custom-envs/engine-env-1  && docker build -t localrepo/engine:tensorflow .
	cd custom-envs/influxdb && docker build -t localrepo/influxdb .
	cd custom-envs/nginx-proxy && docker build -t localrepo/nginx-proxy .

deploy:
	docker stack rm fastscore && ([ $$? -eq 0 ] && echo "success!") || echo "failure!"
	docker stack deploy -c docker-compose.yaml --resolve-image changed fastscore 

config:
	bash -x utils/config_demo.sh
	#bash ./utils/get_urls.sh

deploy-splash:
	cd splash-screen && ./run.sh

load-assets:
	# this sets up arango
	:q


swarm: stop
	docker swarm init

stop:
	docker stack rm fastscore && ([ $$? -eq 0 ] && echo "success!") || echo "failure!"
	docker swarm leave --force && ([ $$? -eq 0 ] && echo "success!") || echo "failure!"

export: stop
	bash ./utils/export_mm.sh

import: stop
	bash ./utils/import_mm.sh

test:
	cd notebooks/hello-world && bash -x run_demo.sh
