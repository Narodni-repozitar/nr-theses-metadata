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

from nr_theses_metadata.records_ui.searchapp import sort_config, facets_config, SearchAppConfig


class UIResourceConfig(InvenioRecordResourceConfig):
    routes = {
        "search": "",
        "detail": "/<pid_value>",
    }
    detail_template = None
    app_contexts = None
    components = None
    template_folder = None

    @property
    def components(self):
        # import here to break circular dependencies
        from .template_processor import RecordTemplateProcessor
        return [RecordTemplateProcessor]

    def get_template_folder(self):
        if not self.template_folder:
            return None

        tf = Path(self.template_folder)
        if not tf.is_absolute():
            tf = Path(inspect.getfile(type(self))).parent.absolute().joinpath(tf).absolute()
        return str(tf)
