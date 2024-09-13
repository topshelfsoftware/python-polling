.PHONY: setup update clean \
		format lint test package

####### CONSTANTS #######
PROJ_ROOT_DIR := $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST)))))
VENV_DIR := $(PROJ_ROOT_DIR)/.venv
PYTHON3 := python3
LOCAL_PYPI_FP := $(PROJ_ROOT_DIR)/local_pypi_dir.txt
ifeq ($(wildcard $(LOCAL_PYPI_FP)),)
# file does not exist
	LOCAL_PYPI_DIR :=
else
# file exists
    LOCAL_PYPI_DIR := $(shell cat ${LOCAL_PYPI_FP})
endif
PKG_NAME := topshelfsoftware_polling
PKG_VER := 0.1.0

####### BUILD TARGETS #######

# The setup target creates a virtual env and installs packages as well as pre-commit hooks.
# It depends on the presence of two scripts: $(VENV_DIR)/bin/activate and $(VENV_DIR)/bin/pre-commit.
# If a script doesn't exist, it will trigger the targets below to create the
# virtual env, install packages, and/or install pre-commit hooks.
setup: $(VENV_DIR)/bin/activate $(VENV_DIR)/bin/pre-commit

update: setup pip-install pre-commit-install

$(VENV_DIR)/bin/activate:
	@$(MAKE) clean
	@echo "Setting up development environment using $(PYTHON3)..."
	$(PYTHON3) -m venv $(VENV_DIR)
	@$(MAKE) pip-install
	@$(MAKE) pre-commit-install
	@echo "Development environment setup complete."

$(VENV_DIR)/bin/pre-commit:
	@$(MAKE) pip-install
	@$(MAKE) pre-commit-install

pip-install:
	@echo "Upgrading pip..."
	$(VENV_DIR)/bin/pip install --upgrade pip
	@echo "Installing required Python packages..."
	@find $(PROJ_ROOT_DIR) \
		-path '*/.aws-sam' -prune -o \
		-path '*/lambda_layer' -prune -o \
		-name 'requirements.txt' -print0 | \
		xargs -0 -I {} sh -c '$(VENV_DIR)/bin/pip install -r "$$1"' _ {}

pre-commit-install:
	@echo "Installing pre-commit hooks..."
	$(VENV_DIR)/bin/pre-commit install
	$(VENV_DIR)/bin/pre-commit install --hook-type pre-push

# Clean target to remove the virtual environment
clean:
	@echo "Removing virtual environment..."
	rm -rf $(VENV_DIR)
	@echo "Clean complete."

# Format code using black, then lint using ruff
format:
	$(VENV_DIR)/bin/black $(PROJ_ROOT_DIR) && \
		$(VENV_DIR)/bin/ruff check $(PROJ_ROOT_DIR) --fix

lint:
	$(VENV_DIR)/bin/ruff check $(PROJ_ROOT_DIR)

# Run all tests
test:
	$(VENV_DIR)/bin/pytest -s -v -c $(PROJ_ROOT_DIR)/tests/pytest.ini \
		--cov --cov-report term --cov-report html --cov-report xml --cov-config $(PROJ_ROOT_DIR)/tests/.coveragerc

test-no-cov:
	$(VENV_DIR)/bin/pytest -s -v -c $(PROJ_ROOT_DIR)/tests/pytest.ini

# Python package
package:
	$(VENV_DIR)/bin/poetry build --format wheel && \
	if [ -d "$(LOCAL_PYPI_DIR)" ]; then \
		cp $(PROJ_ROOT_DIR)/dist/$(PKG_NAME)-$(PKG_VER)*.whl $(LOCAL_PYPI_DIR) && \
		echo "Copied wheel to $(LOCAL_PYPI_DIR)"; \
	fi
