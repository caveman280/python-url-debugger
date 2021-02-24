# URL Debugger

[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/caveman280/python-url-debugger)

This is a Python 3.8 CLI application that uses [poetry](https://python-poetry.org) for packaging and dependency management. 

# Use

This tool allows you to interrogate a URL and find out multiple types of information about given URL(s).

To use the tool, you need to supply it with URL(s) and in exchange, you will be returned a valid JSON file for that URL; including HTTP Status Codes, redirects in place for that URL, headers, remote IP addresses & ports.

This could be used in combination with [JQ](https://stedolan.github.io/jq/) to make the output more human readable.

You can use this CLI in a number of ways. You can supply a single URL:
```bash
$ poetry run python url_debugger fetch -u https://www.google.com | jq .
```

Or, give it a list of URLs in a text file:
```bash
$ echo -en "https://www.google.com\nhttps://www.bbc.co.uk" > urls.txt
$ poetry run python url_debugger fetch -f urls.txt | jq .
```

You could choose to spawn a shell within the virtual environment allowing you to drop the `poetry run`, eg:
```bash
# so vscode picks up the venv
$ poetry config virtualenvs.in-project true
# install dependencies
$ poetry install
# spawn the shell
$ poetry shell
# use at your will!
$ python url_debugger fetch -u https://www.google.com | jq .
$ python url_debugger fetch -f urls.txt | jq .
```

# Development

The easiest way to get started on this project is to use [GitPod](https://gitpod.io), as you'll be able to _"Start Fresh with Ephemeral Dev Environments"_, with dependancies automatically installed.

# Tests

Tests are managed in Poetry with [pytest](https://docs.pytest.org/en/stable/) and can be completed with:
```bash
$ poetry run test
```

To execute the tests with code coverage:

```bash
$ poetry run pytest --cov url_debugger
```

And for a HTML report of that at htmlcov/index.html

```bash
$ poetry run coverage html
```
