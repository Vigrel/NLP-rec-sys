PROJECT_NAME = cocktail_recommender
DOCKER_IMAGE = $(PROJECT_NAME)_image
HOST_PORT = 9000
PYTHON = python3
PIP = pip3
VENV_DIR = venv
VENV_SCRIPTS_DIR = scripts/venvscripts
REQUIREMENTS_FILE = requirements.txt
DOCKERFILE = Dockerfile
DATA_DIR = data
MODEL_DIR = model
LOGS_DIR = logs
EXAMPLE_DIR = example

#############
# Other env #
#############
# this env exists to run scripts/get_data.py due to conflicts between
# httpx lib version when using FastAPI and googletrans at the same project
$(VENV_SCRIPTS_DIR)/bin/activate: 
	$(PYTHON) -m venv $(VENV_SCRIPTS_DIR)
	$(VENV_SCRIPTS_DIR)/bin/$(PIP) install --upgrade pip
	$(VENV_SCRIPTS_DIR)/bin/$(PIP) install -r scripts/$(REQUIREMENTS_FILE)

venv-scripts: $(VENV_SCRIPTS_DIR)/bin/activate
	@echo "Virtual environment created."

get-data: venv-scripts
	$(VENV_SCRIPTS_DIR)/bin/$(PYTHON) scripts/get_data.py

#############
# Init Repo #
#############
$(VENV_DIR)/bin/activate: 
	$(PYTHON) -m venv $(VENV_DIR)
	$(VENV_DIR)/bin/$(PIP) install --upgrade pip
	$(VENV_DIR)/bin/$(PIP) install -r $(REQUIREMENTS_FILE)


venv: $(VENV_DIR)/bin/activate
	@echo "Virtual environment created."

install: venv
	$(VENV_DIR)/bin/$(PIP) install -r $(REQUIREMENTS_FILE)

run: venv
	$(VENV_DIR)/bin/$(PYTHON) app/main.py

###################
# Maintainability #
###################
test: venv
	$(VENV_DIR)/bin/pytest test/

lint: venv
	$(VENV_DIR)/bin/flake8 app/ scripts/ test/ logs/ --count --select=E9,F63,F7,F82 --show-source --statistics
	$(VENV_DIR)/bin/flake8 app/ scripts/ test/ logs/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

format: venv
	$(VENV_DIR)/bin/black .

#########################
# Local Maintainability #
#########################
clean-venv:
	rm -rf $(VENV_DIR)
	@echo "Removed virtual environment."

clean-venv-scripts:
	rm -rf $(VENV_SCRIPTS_DIR)
	@echo "Removed scripts virtual environment."

clean-cache:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	@echo "Removed Python cache files."

clean-data:
	find $(DATA_DIR) -mindepth 1 ! -regex "$(DATA_DIR)/.gitignore" -delete
	@echo "Cleaned data directory, excluding .gitignore."

clean-model:
	find $(MODEL_DIR) -mindepth 1 ! -regex "$(MODEL_DIR)/.gitignore" -delete
	@echo "Cleaned model directory, excluding .gitignore."

clean-logs:
	find $(LOGS_DIR) -mindepth 1 ! -name "__init__.py" ! -name "logger.py" -delete
	@echo "Cleaned logs directory, excluding logger.py."

clean-all: clean-venv clean-cache clean-data clean-model clean-logs clean-venv-scripts
	@echo "Cleaned all specified directories and caches."


#################
# Build Project #
#################
docker-build:
	docker build -t $(DOCKER_IMAGE) -f $(DOCKERFILE) .

docker-run:
	docker run -it --rm -p $(HOST_PORT):8888 $(DOCKER_IMAGE)



#################
# Help #
#################
help:
	@echo "Makefile for $(PROJECT_NAME) project"
	@echo ""
	@echo "Available targets:"
	@echo "  venv               Create the primary virtual environment and install dependencies."
	@echo "  install            Install dependencies in the primary virtual environment."
	@echo "  run                Run the application locally."
	@echo "  venv-scripts       Create a separate virtual environment for script dependencies."
	@echo "  get-data           Run the data retrieval script using the separate environment."
	@echo "  test               Run unit tests with pytest."
	@echo "  lint               Lint the code with flake8."
	@echo "  format             Format the code with black."
	@echo "  clean-venv         Remove the primary virtual environment."
	@echo "  clean-venv-scripts Remove the script virtual environment."
	@echo "  clean-cache        Remove Python cache files."
	@echo "  clean-data         Clean the data directory, excluding .gitignore."
	@echo "  clean-model        Clean the model directory, excluding .gitignore."
	@echo "  clean-logs         Clean the logs directory, excluding __init__.py and logger.py."
	@echo "  clean-all          Clean all environments, caches, data, model, and logs."
	@echo "  docker-build       Build the Docker image."
	@echo "  docker-run         Run the application in a Docker container."
	@echo "  help               Show this help message."