import inspect
from pathlib import Path
from flask_resources import ResponseHandler, JSONSerializer

from invenio_records_resources.resources import (
    RecordResourceConfig as InvenioRecordResourceConfig, )
from nr_theses_metadata.resources.serializers_to_be_moved.ui import UIJSONSerializer


class UIResourceConfig(InvenioRecordResourceConfig):   
    components = None
    template_folder = None
    
    def get_template_folder(self):
        if not self.template_folder:
            return None

        tf = Path(self.template_folder)
        if not tf.is_absolute():
            tf = Path(inspect.getfile(type(self))).parent.absolute().joinpath(tf).absolute()
        return str(tf)


class RecordsUIResourceConfig(UIResourceConfig):
    routes = {
        "search": "",
        "detail": "/<pid_value>",
    }
    detail_template = None
    app_contexts = None

    response_handlers = {
        "application/json": ResponseHandler(JSONSerializer()),
        "application/vnd.inveniordm.v1+json": ResponseHandler(UIJSONSerializer()),
    }

     # handled by RecordTemplateContextComponent
    record_sort_options = []
    record_sort_default = 'bestmatch'
    record_sort_default_no_query = 'newest'
    record_facets = ['metadata_accessRights', 'metadata_rights', 'metadata_fundingReferences_funder']

    @property
    def components(self):
        # import here to break circular dependencies
        from .record_template_context_component import RecordTemplateContextComponent
        return [RecordTemplateContextComponent]
