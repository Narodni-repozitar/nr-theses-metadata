#!/bin/bash


cd `dirname $0`/..

set -e

source .venv/bin/activate

# export FLASK_DEBUG=1
cd nr-theses-metadata-sample-site

invenio-cli run