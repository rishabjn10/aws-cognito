# Define directories to exclude
EXCLUDE_DIRS = .venv,__pycache__

# Define the targets for each tool
.PHONY: all flake8 isort autopep8

# Default target: run all the tools in sequence
lint: isort autopep8 flake8

# Target to run isort and skip excluded directories
isort:
	@echo "---Running isort format---"
	pdm run isort . --skip .venv --skip __pycache__

# Target to run autopep8 and exclude directories
autopep8:
	@echo "---Running autopep8 format---"
	pdm run autopep8 --in-place --recursive . --exclude $(EXCLUDE_DIRS)

# Target to run flake8 and exclude directories
flake8:
	@echo "---Running flake linting---"
	pdm run flake8 . --exclude $(EXCLUDE_DIRS) --ignore=E501,W503,E722

# Target to install dependencies
install-deps:
	@echo "---Installing project dependencies---"
	pdm install