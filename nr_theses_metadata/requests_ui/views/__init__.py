# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2022 CERN.
# Copyright (C) 2019-2022 Northwestern University.
# Copyright (C)      2022 TU Wien.
#
# Invenio App RDM is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""Request views module."""

from flask import Blueprint
from invenio_pidstore.errors import PIDDeletedError, PIDDoesNotExistError
from invenio_records_resources.services.errors import PermissionDeniedError
from invenio_requests.views.ui import (
    not_found_error,
    record_permission_denied_error,
    record_tombstone_error,
)

def create_ui_blueprint(app):
    """Register blueprint routes on app."""
    routes = app.config["REQUESTS_ROUTES"]

    blueprint = Blueprint(
        "nr_theses_metadata_sample_app_requests",
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )

    # Register error handlers
    blueprint.register_error_handler(
        PermissionDeniedError, record_permission_denied_error
    )
    blueprint.register_error_handler(PIDDeletedError, record_tombstone_error)
    blueprint.register_error_handler(PIDDoesNotExistError, not_found_error)

    return blueprint
