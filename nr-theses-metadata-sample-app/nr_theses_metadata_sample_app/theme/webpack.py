# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2022 CERN.
# Copyright (C) 2019-2022 Northwestern University.
# Copyright (C)      2022 TU Wien.
# Copyright (c) 2022 CESNET
#
# Invenio App RDM is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""JS/CSS Webpack bundles for theme."""

from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    "assets",
    default="semantic-ui",
    themes={
        "semantic-ui": dict(
            entry={
                "nr-theses-metadata-sample-app-landing-page": "./js/nr_theses_metadata_sample_app/landing_page/index.js",
                "nr-theses-metadata-sample-app-deposit": "./js/nr_theses_metadata_sample_app/deposit/index.js",
                "nr-theses-metadata-sample-app-search": "./js/nr_theses_metadata_sample_app/search/index.js",
                "nr-theses-metadata-sample-app-user-dashboard": "./js/nr_theses_metadata_sample_app/user_dashboard/index.js",
            },
            dependencies={
                "@babel/runtime": "^7.9.0",
                "@ckeditor/ckeditor5-build-classic": "^16.0.0",
                "@ckeditor/ckeditor5-react": "^2.1.0",
                "formik": "^2.1.0",
                "i18next": "^20.3.0",
                "i18next-browser-languagedetector": "^6.1.0",
                "luxon": "^1.23.0",
                "path": "^0.12.7",
                "prop-types": "^15.7.2",
                "react-copy-to-clipboard": "^5.0.0",
                "react-dnd": "^11.1.0",
                "react-dnd-html5-backend": "^11.1.0",
                "react-dropzone": "^11.0.0",
                "react-i18next": "^11.11.0",
                "react-invenio-deposit": "^0.18.0",
                "react-invenio-forms": "^0.10.0",
                "yup": "^0.32.0",
            },
            aliases={
                # Define Semantic-UI theme configuration needed by
                # Invenio-Theme in order to build Semantic UI (in theme.js
                # entry point). theme.config itself is provided by
                # cookiecutter-oarepo-app.
                "../../theme.config$": "less/theme.config",
                "themes/oarepo": "less/nr_theses_metadata_sample_app/theme",
                "@less/nr_theses_metadata_sample_app": "less/nr_theses_metadata_sample_app",
                "@translations/nr_theses_metadata_sample_app": "translations/nr_theses_metadata_sample_app",
                "@translations/invenio_app_rdm": "translations/nr_theses_metadata_sample_app",
            },
        ),
    },
)
