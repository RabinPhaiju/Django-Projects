SHELL := /bin/bash


_ALLOWED_ENVS := dev prod
APP_ENV := $(or $(APP_ENV),dev)

ifeq ($(filter $(APP_ENV),$(_ALLOWED_ENVS)),)
$(error APP_ENV is not set correctly. You must set APP_ENV to one of: "$(_ALLOWED_ENVS)". For example: APP_ENV=live make arg=value command)
endif

ifeq ($(APP_ENV),prod)
	compose-cmd := APP_ENV=live docker compose -f docker-compose.yaml -f [file_name].yaml
	compose-cmd-server := $(compose-cmd) up -d --build

else
	compose-cmd := docker compose -f docker-compose.yaml
	compose-cmd-server := $(compose-cmd) up
endif

run-web := $(compose-cmd) run --rm web

echo-env: 
			@echo $(APP_ENV)
build:
			$(compose-cmd) build	

server: 
			$(compose-cmd-server)
dev-down:
			$(compose-cmd) down

collectstatic:
			$(compose-cmd) exec web python manage.py collectstatic --no-input --clear

migrate: 
			$(run-web) python manage.py migrate 

migrations:
			$(run-web) python manage.py makemigrations

superuser:
			$(run-web) python manage.py createsuperuser

dev:
			$(compose-cmd) up --build --attach web

app:
			$(run-web) python manage.py startapp $(app)

import-records:
	$(compose-cmd) run --rm -T web manage import_records $(apps)

test:
			$(run-web) python manage.py test ${test}