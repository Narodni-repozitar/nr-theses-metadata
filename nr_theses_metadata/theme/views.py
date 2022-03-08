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


def create_ui_blueprint(app):
    """Create  blueprint."""
    blueprint = app.extensions["nr_theses_metadata"].ui_resource.as_blueprint()
    return blueprint
