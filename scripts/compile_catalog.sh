#!/bin/bash


cd `dirname $0`/..

set -e

source .venv/bin/activate

pybabel compile -f -d nr_theses_metadata/translations
