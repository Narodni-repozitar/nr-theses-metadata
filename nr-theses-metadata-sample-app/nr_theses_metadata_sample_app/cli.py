# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2022 CERN.
# Copyright (C) 2019-2022 Northwestern University.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.


"""Command-line tools for demo module."""

import click
from flask.cli import with_appcontext
from .fixtures import FixturesEngine
from invenio_access.permissions import system_identity


@click.group()
def rdm_records():
    """Records commands."""
    # This name MUST be kept as it is called from invenio-cli in services setup


@rdm_records.command("fixtures")
@with_appcontext
def create_fixtures():
    """Create the fixtures required for record creation."""
    click.secho("Creating required fixtures...", fg="green")

    FixturesEngine(system_identity).run()

    click.secho("Created required fixtures!", fg="green")
