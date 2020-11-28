#!/bin/sh

python3 -m pytest --doctest-modules pandas_estat
python3 -m pytest --doctest-modules tests

python3 -m flake8 pandas_estat
python3 -m black --check pandas_estat || read -p "Run formatter? (y/N): " yn; [[ $yn = [yY] ]] && python3 -m black pandas_estat
python3 -m isort --check --force-single-line-imports pandas_estat || read -p "Run formatter? (y/N): " yn; [[ $yn = [yY] ]] && python3 -m isort --force-single-line-imports pandas_estat
