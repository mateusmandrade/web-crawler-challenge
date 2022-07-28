# Digesto-Jusbrasil Web Crawler Challenge

Web crawler to get some data from specific pages

## Instalation

There are some third dependencies in project, it is possible install through [poetry](https://python-poetry.org/) or in your preferred Python environment by `requirements.txt`.

```shell
poetry install [--dev]
```

## Execution

You can run the crawler calling `crawler` module with output arguments. The output arguments are:

- `--print`: to show output in stdout

- `--save-json FILENAME`: to save in a file with JSON format

- `--save-csv FILENAME`: to save in a file with CSV format

```shell
[poetry run] python -m crawler [--print | --save-json | --save-csv]
```
