.PHONY: install start@dev clean db@init db@migrate db@up db@rev db@down db@his db@curr docker@up
FLASK_APP := app.py
PACKAGE_NAME := api_bloxs
APP := $(PACKAGE_NAME)/$(FLASK_APP)
POETRY_RUN_FLASK = poetry run flask --app $(APP)


define run_flask_context
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

db@init:
	@echo "Initializing the database..."
	$(call run_flask_context,init)

db@migrate:
	@echo "Migrating the database..."
	$(call run_flask_context,migrate,-m $(m))

db@up:
	@echo "Downgrading the database..."
	$(call run_flask_context,downgrade)

db@rev:
	@echo "Revising the database..."
	$(call run_flask_context,revision,-c $(c))

db@down:
	@echo "Downgrading the database..."
	$(call run_flask_context,upgrade)

db@his:
	@echo "Showing the database history..."
	$(call run_flask_context,history)

db@curr:
	@echo "Showing the current database revision..."
	$(call run_flask_context,current)

docker@up:
	@echo "Starting the Docker containers..."
	docker compose --env-file .env -f docker-compose.yml up -d --force-recreate 