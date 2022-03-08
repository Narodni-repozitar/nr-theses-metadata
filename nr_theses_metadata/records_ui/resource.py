
from nr_theses_metadata.records_ui.base_to_be_moved import RecordsUIResourceConfig
from nr_theses_metadata.records_ui.base_to_be_moved import RecordsUIResource


class NrThesesMetadataRecordsUIResourceConfig(RecordsUIResourceConfig):
    """NrThesesMetadataRecord resource config."""

    blueprint_name = "NrThesesMetadataRecordsUI"
    url_prefix = "/documents/"
    template_folder = "templates"

    detail_template = "nr_theses_metadata/records/detail.html"

    record_template_context = {
        'config_name': 'RECORD_SEARCH',   # tohle pujde do kytek
        'available_facets': {},
    }


class NrThesesMetadataRecordsUIResource(RecordsUIResource):
    pass
