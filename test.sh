#!/bin/sh -eu

python3 -m pytest --doctest-modules pandas_estat
python3 -m pytest --doctest-modules tests
python3 -m black --quiet .
python3 -m isort --force-single-line-imports --quiet .
