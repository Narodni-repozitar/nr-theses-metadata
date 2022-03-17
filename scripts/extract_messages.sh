#!/bin/bash


cd `dirname $0`/..

set -e

source .venv/bin/activate

pybabel extract -F babel.ini --copyright-holder=CESNET --msgid-bugs-address=info@oarepo.org -o nr_theses_metadata/translations/messages.pot -c NOTE --input-dirs=nr_theses_metadata/