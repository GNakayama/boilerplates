SHELL := /bin/bash

build:
	docker-compose build

run: migrate
	docker-compose up

test:
	docker-compose run web pytest -v -n 16 --cov=.

migrate:
	docker-compose run web python manage.py migrate

makemigrations:
	docker-compose run web python manage.py makemigrations

psql:
	docker-compose run db psql -h db -U postgres

shell:
	docker-compose run web python manage.py shell

create_database:
	docker-compose up -d
	docker-compose run db psql -h db -U postgres -c "CREATE DATABASE {{ cookiecutter.project_slug }}"

drop_database:
	docker-compose up -d
	docker-compose run db psql -h db -U postgres -c "DROP DATABASE IF EXISTS {{ cookiecutter.project_slug }}"

create_superuser:
	docker-compose run web python manage.py createsuperuser

setup: build
	$(MAKE) drop_database
	$(MAKE) create_database
	$(MAKE) migrate
	$(MAKE) create_superuser

generate_documentation:
	docker-compose run web python manage.py generateschema --format openapi > schema.yml

lint:
	pycln . -a -x -s
	isort . --profile=black
	black .

env:
	python3 -m venv venv

install:
	pip install -r requirements-dev.txt
