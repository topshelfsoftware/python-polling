# python-polling

Poll a target function for status.

## Getting Started

### Prerequisites

1. Python 3.9 | 3.10 | 3.11 | 3.12 installed on system
2. Optionally, create a file named `local_pypi_dir.txt` in the project root directory (same folder as this `README`)
    - Contents of file are a single line defining the path to a local directory to be used as a local PyPI repository.

### Set Up Environment

To create the dev environment, navigate to the project root directory and run the following

```bash
make setup [PYTHON3=python3]
```

>NOTE: This command creates a virtual environment to `./.venv` and downloads all the
packages required to debug/test the source code as well as other developer tools. Specify
a minor version of Python 3 using the `PYTHON3=python3.<minor>` arg.

If the dev environment has already been setup, then the dependencies can be updated with

```bash
make update [PYTHON3=python3]
```

### Unit Tests

Unit tests are located in the `./tests` directory and are written using `pytest`.
To run all unit tests, execute the following command from the project root directory

```bash
make test
```

### Formatting and Linting

To ensure consistent style and catch potential errors, this repo formats Python code using `black` and
lints Python code using `ruff`. To format and then lint, run

```bash
make format
```

## Deployment

### Package

Build the `topshelfsoftware-polling` Python package as a wheel and copy it to the local PyPI repository

```bash
make package
```

## Versioning

This package uses Semantic Versioning 2.0.0 to describe MAJOR.MINOR.PATCH releases.

IMPORTANT❗
Search the project for the existing package version and update in the following places prior to building the package and deploying the lambda layer:

- shields.io badge in this `README`
- `PKG_VER` variable in the project `Makefile`
- `version` in the poetry `pyproject.toml`

## Available Modules

See the list of [available modules](./docs/README.md#available-modules).
