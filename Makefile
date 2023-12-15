.PHONY: setup dev clean

FLASK_APP := app.py
PACKAGE_NAME := api_bloxs

setup:
	@echo "Installing dependencies with Poetry..."
	poetry install

dev:
	@echo "Running the Python script..."
	poetry run flask --app $(PACKAGE_NAME)/$(FLASK_APP) run --reload

clean:
	@echo "Cleaning up..."
	poetry env remove $(shell poetry env info --path)
	rm -rf __pycache__
	rm -f *.pyc
