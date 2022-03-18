#!/bin/bash

cd `dirname $0`/..

set -e

source .venv/bin/activate

rm -f dist/*
rm -f nr-theses-metadata-sample-site/dist/*
rm -f nr-theses-metadata-sample-app/dist/*

pipenv run pip install wheel

poetry build

cp dist/nr-theses-metadata*.tar.gz nr-theses-metadata-sample-site/dist/

cd nr-theses-metadata-sample-app

pipenv run python3 setup.py sdist bdist_wheel

cp dist/nr-theses-metadata-sample-app*.tar.gz ../nr-theses-metadata-sample-site/dist/

cd ../nr-theses-metadata-sample-site

# Clear pipenv cache to avoid hash issues
pipenv --clear
pipenv lock
#invenio-cli containers build
