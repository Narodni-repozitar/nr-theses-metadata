#!/bin/bash


cd `dirname $0`/..

set -e

source .venv/bin/activate

pybabel init -d nr_theses_metadata/translations/ -i nr_theses_metadata/translations/messages.pot -l $1