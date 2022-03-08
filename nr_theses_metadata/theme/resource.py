import inspect
from pathlib import Path

from flask import render_template
from flask_babelex import get_locale
from flask_resources import route

from nr_theses_metadata.records_ui.base_to_be_moved import UIResourceConfig, UIResource


class NrThesesMetadataUIResourceConfig(UIResourceConfig):
    """NrThesesMetadata resource config."""

    blueprint_name = "NrThesesMetadataThemeUI"
    url_prefix = "/"
    template_folder = "templates"

    frontpage_template = "nr_theses_metadata/frontpage.html"
    help_search_template = f"nr_theses_metadata/help/search.{get_locale()}.html",
    help_search_fallback_template = "nr_theses_metadata/help/search.en.html"

    routes = {
        "index": "/",
        "help_search": "/help/search",
    }


class NrThesesMetadataUIResource(UIResource):
    config: NrThesesMetadataUIResourceConfig

    def create_url_rules(self):
        """Create the URL rules for the record resource."""
        routes = self.config.routes
        return [
            route("GET", routes["index"], self.index),
            route("GET", routes["help_search"], self.help_search),
        ]

    def index(self):
        """Frontpage."""
        return render_template(
            self.config.frontpage_template
        )

    def help_search(self):
        """Search help guide."""
        # Default to rendering english page if locale page not found.
        return render_template(
            [
                self.config.help_search_template,
                self.config.help_search_fallback_template
            ]
        )
