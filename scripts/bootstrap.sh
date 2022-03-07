#!/bin/bash

cd `dirname $0`/..

set -e

python3.9 -m venv .venv
source .venv/bin/activate

pip install invenio-cli

cd nr-theses-metadata-sample-site
invenio-cli check-requirements -d
invenio-cli install
invenio-cli services setup -N -f

cd ..

# install back current app
pipenv run poetry install

# create the branch
pipenv run invenio alembic revision "Create nr_theses_metadata branch."  -b nr_theses_metadata -p dbdbc1b19cf2 --empty

# apply the branch
pipenv run invenio alembic upgrade heads

# initial revision
pipenv run invenio alembic revision "Initial revision." -b nr_theses_metadata

find nr_theses_metadata/alembic -name "*py" | while read FN; do
    echo "Fixing sqlalchemy file $FN"
    # import sqlalchemy_utils
    # remove length=16 from UUIDType(length=16)
    # replace Text() with sa.Text()
    cat "$FN" | \
        sed 's/import sqlalchemy as sa/import sqlalchemy as sa\nimport sqlalchemy_utils/' | \
        sed 's/UUIDType(length=16/UUIDType(/' | \
        sed 's/astext_type=Text()/astext_type=sa.Text()/' >"$FN".replaced
    mv "$FN".replaced "$FN"
done

# create db tables
pipenv run invenio alembic upgrade heads

pipenv run invenio index destroy --yes-i-know || true
pipenv run invenio index init --force
