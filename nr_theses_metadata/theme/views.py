# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2020 CERN.
# Copyright (C) 2019-2020 Northwestern University.
# Copyright (C)      2021 TU Wien.
# Copyright (c) 2022 CESNET
#
# Invenio App RDM is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Routes for general pages provided by nr-theses-metadata."""

from flask import Blueprint, current_app, render_template
from flask_babelex import get_locale
from flask_babelex import lazy_gettext as _

#
# Registration
#
def create_ui_blueprint(app):
    """Blueprint for the routes and resources provided by nr-theses-metadata."""
    routes = app.config.get("APP_UI_ROUTES")

    blueprint = Blueprint(
        "nr_theses_metadata",
        __name__,
        template_folder="templates",
        static_folder="static",
    )

    blueprint.add_url_rule(routes["index"], view_func=index)
    blueprint.add_url_rule(routes["help_search"], view_func=help_search)

    return blueprint

#
# Views
#
def index():
    """Frontpage."""
    return render_template(
        current_app.config["THEME_FRONTPAGE_TEMPLATE"],
    )


def help_search():
    """Search help guide."""
    # Default to rendering english page if locale page not found.
    locale = get_locale()
    return render_template(
        [
            f"nr_theses_metadata/help/search.{locale}.html",
            "nr_theses_metadata/help/search.en.html",
        ]
    )
