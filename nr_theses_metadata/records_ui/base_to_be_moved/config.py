import inspect
from pathlib import Path

from invenio_records_resources.resources import (
    RecordResourceConfig as InvenioRecordResourceConfig, )


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

     # handled by RecordTemplateContextComponent
    record_sort_options = []
    record_sort_default = 'bestmatch'
    record_sort_default_no_query = 'newest'
    record_facets = []

    @property
    def components(self):
        # import here to break circular dependencies
        from .record_template_context_component import RecordTemplateContextComponent
        return [RecordTemplateContextComponent]
