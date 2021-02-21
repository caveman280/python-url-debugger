# Poetry Template

[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/caveman280/poetry-python-template)

This is a minimal Python 3.8 application that uses [poetry](https://python-poetry.org) for packaging and dependency management. It also provides [pre-commit](https://pre-commit.com/) hooks (for [Black](https://black.readthedocs.io/en/stable/) and [Flake8](https://flake8.pycqa.org/en/latest/)) and automated tests using [pytest](https://pytest.org/), [Coverage.py](https://coverage.readthedocs.io/) and [GitHub Actions](https://github.com/features/actions). Documentation can be generated with [Sphinx](https://www.sphinx-doc.org/en/master/), and version numbers updated with [bump2version](https://github.com/c4urself/bump2version).
To use this repository as a template for your own application:

1. [Download and install Poetry](https://python-poetry.org/docs/#installation) following the instructions for your OS.
1. Name and create your repository
1. Clone your new repository and make it your working directory
1. Replace instances of `poetry_template` with your own application name. Edit:
   - `pyproject.toml`
   - `tests/test_poetry_template.py`
   - The `poetry_template` directory name and `poetry_template/__main__.py`
   - `docs/source/conf.py`
   - `setup.cfg`
1. Set up the virtual environment:

   ```bash
   poetry install
   ```

1. Activate the virtual environment (alternatively, ensure any python-related command is preceded by `poetry run`):

   ```bash
   poetry shell
   ```

1. Run the main app:

   ```bash
   poetry run python poetry_template
   ```

1. Run the tests:

   ```bash
   poetry run pytest
   ```

1. Build the documentation:

   ```bash
   sphinx-build -b html docs/source/ docs/build/
   ```

1. Edit/replace `.py` files as required.
1. Add new requirements with `poetry add` or by manually adding them to `pyproject.toml`