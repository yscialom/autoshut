.PHONY: help build start stop

all: help

help:
	@echo "make help ........ display this message and exit"
	@echo "make build ....... build the service docker images"
	@echo "make start ....... start the service docker containers"
	@echo "make stop ........ gracefully stop the service"

codestyle:
	@python3 -m pycodestyle --max-line-length=120 monitor/app controller/app

build:
	@docker-compose build

start:
	@docker-compose up -d

stop:
	@docker-compose down
