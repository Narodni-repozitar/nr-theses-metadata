import inspect
import os
from functools import partial

from flask import g, render_template
from flask_resources import Resource, route, resource_requestctx
from invenio_records_resources.resources import (
    RecordResourceConfig as InvenioRecordResourceConfig, RecordResourceConfig,
)
from invenio_records_resources.resources.records.resource import request_read_args, request_view_args
from pathlib import Path
from invenio_records_resources.services import RecordService

from .config import UIResourceConfig
from nr_theses_metadata.records_ui.searchapp import sort_config, facets_config, SearchAppConfig


#
# Resource
#
class UIResource(Resource):
    """Record resource."""
    config: UIResourceConfig
    api_config: RecordResourceConfig
    service: RecordService

    def __init__(self, config=None, api_config=None, service=None):
        """Constructor."""
        super(UIResource, self).__init__(config)
        self.api_config = api_config
        self.service = service

    def create_url_rules(self):
        """Create the URL rules for the record resource."""
        routes = self.config.routes
        return [
            route("GET", routes["detail"], self.detail),
        ]

    def as_blueprint(self, **options):
        if 'template_folder' not in options:
            template_folder = self.config.get_template_folder()
            if template_folder:
                options['template_folder'] = template_folder
        blueprint = super().as_blueprint(**options)
        blueprint.app_context_processor(lambda: self._search_app_context())
        return blueprint

    def _search_app_context(self):
        """function providing flask template app context processors"""
        ret = {}
        self.run_components('search_app_context', template_contexts=ret)
        return ret

    @request_read_args
    @request_view_args
    def detail(self):
        """Read an item."""
        record = self.service.read(g.identity, resource_requestctx.view_args["pid_value"])
        # TODO:
        # record_ui = UIJSONSerializer().serialize_object_to_dict(record.to_dict())
        record_ui = record.to_dict()
        record_ui['ui'] = {**record_ui}

        return render_template(
            self.config.detail_template,
            record=record_ui
        )

    #
    # Pluggable components
    #
    @property
    def components(self):
        """Return initialized service components."""
        return (c(self) for c in self.config.components or [])

    def run_components(self, action, *args, **kwargs):
        """Run components for a given action."""

        for component in self.components:
            if hasattr(component, action):
                getattr(component, action)(*args, **kwargs)
