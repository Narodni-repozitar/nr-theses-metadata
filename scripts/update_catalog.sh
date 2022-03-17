#!/bin/bash


cd `dirname $0`/..

set -e

source .venv/bin/activate

pybabel update -i nr_theses_metadata/translations/messages.pot -d nr_theses_metadata/translations/ -l $1
