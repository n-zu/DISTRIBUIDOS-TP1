SHELL := /bin/bash
PWD := $(shell pwd)


default: build


docker-image:
	docker build -f ./client/Dockerfile -t "client:latest" .
	docker build -f ./worker/Dockerfile -t "worker:latest" .
	docker build -f ./sink/Dockerfile -t "sink:latest" .
	# Execute this command from time to time to clean up intermediate stages generated 
	# during client build (your hard drive will like this :) ). Don't left uncommented if you 
	# want to avoid rebuilding client image every time the docker-compose-up command 
	# is executed, even when client code has not changed
	# docker rmi `docker images --filter label=intermediateStageToBeDeleted=true -q`
.PHONY: docker-image

up: docker-image
	docker compose -f docker-compose.yml up -d --build
.PHONY: up

down:
	docker compose -f docker-compose.yml stop -t 1
	docker compose -f docker-compose.yml down
.PHONY: down

logs:
	docker compose -f docker-compose.yml logs -f
.PHONY: logs

du:
	$(MAKE) down
	$(MAKE) up
.PHONY: du
