# .PHONY: server
SHELL := /bin/bash

_ALLOWED_ENVS := local live
APP_ENV := $(or $(APP_ENV),local)

ifeq ($(filter $(APP_ENV),$(_ALLOWED_ENVS)),)
$(error APP_ENV is not set correctly. You must set APP_ENV to one of: "$(_ALLOWED_ENVS)". For example: APP_ENV=local make arg=value command")
endif

ifeq ($(APP_ENV),live)
	compose-cmd := APP_ENV=live docker-compose \
		-f docker-compose.prod.yml
	compose-cmd-server := $(compose-cmd) up -d --build
else
	compose-cmd := APP_ENV=$(APP_ENV) docker-compose \
		-f docker-compose.yml
	compose-cmd-server := $(compose-cmd) up
endif


dev:
	$(compose-cmd-server)

dev-down:
	$(compose-cmd) down

server:
	$(compose-cmd-server)

server-down:
	$(compose-cmd) down

build:
	@$(compose-cmd) build

build-nocache:
	@$(compose-cmd) build --no-cache

migrate:
	@$(compose-cmd) run --rm web python manage.py migrate

shell:
	@$(compose-cmd) run --rm web python manage.py shell

# problem- we dont need client and dont need 'web' to backup, directly go to db_container and backup/restore
db-r-backup:
	docker exec -it djangodock_db_dev pg_dump -U djangodock djangodock_dev > dump1.sql

db-r-restore:
	docker exec -i djangodock_db_dev psql -U djangodock djangodock_dev < dump1.sql

db-r-drop:
	docker exec -i djangodock_db_dev dropdb -U djangodock djangodock_dev

db-backup:
	@$(compose-cmd) run --rm -v $$PWD:/tmp web /bin/bash -c  "PGPASSWORD=\$$SQL_PASSWORD pg_dump -h \$$SQL_HOST  -p \$$SQL_PORT -U \$$SQL_USER --format p \$$SQL_DATABASE > /tmp/dump.sql"

db-restore:
	@$(compose-cmd) run --rm -v $$PWD/dump.sql:/tmp/dump.sql web /bin/bash -c  "PGPASSWORD=\$$SQL_PASSWORD psql -h \$$SQL_HOST  -p \$$SQL_PORT -U \$$SQL_USER \$$SQL_DATABASE < dump.sql"

db-drop:
	@$(compose-cmd) run --rm  web /bin/bash -c "PGPASSWORD=\$$SQL_PASSWORD dropdb -U \$$SQL_USER -h \$$SQL_HOST -p \$$SQL_PORT \$$SQL_DATABASE"
