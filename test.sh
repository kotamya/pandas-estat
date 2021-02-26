#!/bin/sh -eu

python3 -m pytest --doctest-modules pandas_estat
python3 -m pytest --doctest-modules tests

python3 -m flake8 pandas_estat
python3 -m black --check --quiet pandas_estat || read -p "Run black? (y/n): " yn; [[ $yn = [yY] ]] && python3 -m black --quiet pandas_estat
python3 -m isort --check --force-single-line-imports pandas_estat || read -p "Run isort? (y/n): " yn; [[ $yn = [yY] ]] && python3 -m isort --force-single-line-imports --quiet pandas_estat
python3 -m black --quiet tests
python3 -m isort --force-single-line-imports --quiet tests
