.PHONY: help build start stop

all: help

help:
	@echo "make help ........ display this message and exit"
	@echo "make codestyle ... Check code against PEP8"
	@echo "make build ....... build the service docker images"
	@echo "make start ....... start the service docker containers"
	@echo "make restart ..... restart the service docker containers"
	@echo "make stop ........ gracefully stop the service"
	@echo "make clean ....... remove mount point"

codestyle:
	@python3 -m pycodestyle --max-line-length=120 monitor/app controller/app

build:
	@docker-compose build

start:
	@mkdir -p config
	@docker-compose up -d

restart:
	@docker-compose restart

stop:
	@docker-compose down

clean:
	@rm -r config
