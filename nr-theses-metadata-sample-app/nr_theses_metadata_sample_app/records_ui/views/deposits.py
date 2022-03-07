# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2021 CERN.
# Copyright (C) 2019-2021 Northwestern University.
# Copyright (C)      2021 TU Wien.
#
# Invenio App RDM is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Routes for record-related pages provided by Invenio-App-RDM."""

from flask import current_app, render_template
from flask_login import login_required


@login_required
def dashboard(dashboard_name=None):
    """Display user dashboard page."""
    return render_template(
        "oarepo_testing_app/dashboard.html",
        dashboard_name=dashboard_name or current_app.config[
            "_DASHBOARD_ROUTES"][0],
        searchbar_config=dict(),
    )
