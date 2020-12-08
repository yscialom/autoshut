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

prepare:
	@mkdir -p config signals
	@echo -n > signals/controller_shutdown_signal

start: prepare
	@controller/host_control.sh & echo "host_control.sh started (pid $$!)"
	@docker-compose up -d

restart:
	@docker-compose restart
	@pkill host_control.sh
stop:
	@docker-compose down
	@pkill -e host_control.sh

clean:
	@rm -r config
