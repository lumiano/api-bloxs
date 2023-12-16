.PHONY: install start@dev clean

FLASK_APP := app.py
PACKAGE_NAME := api_bloxs
APP := $(PACKAGE_NAME)/$(FLASK_APP)
POETRY_RUN_FLASK = poetry run flask --app $(APP)


define run_database_command
	$(POETRY_RUN_FLASK) db $(1) $(2)
endef


install:
	@echo "Installing dependencies with Poetry..."
	poetry install

start@dev:
	@echo "Running the Python script..."
	poetry run flask --app $(APP) run --reload

clean:
	@echo "Cleaning up..."
	poetry env remove $(shell poetry env info --path)
	rm -rf __pycache__
	rm -f *.pyc


db@init:
	@echo "Initializing the database..."
	$(call run_database_command,init)

db@migrate:
	@echo "Migrating the database..."
	$(call run_database_command,migrate,-m $(m))

db@upgrade:
	@echo "Upgrading the database..."
	$(call run_database_command,upgrade)

db@downgrade:
	@echo "Downgrading the database..."
	$(call run_database_command,downgrade)


db@current:
	@echo "Showing the current database revision..."
	$(call run_database_command,current)

docker@up:
	@echo "Starting the Docker containers..."
	docker compose --env-file .env -f docker-compose.yml up -d --force-recreate 