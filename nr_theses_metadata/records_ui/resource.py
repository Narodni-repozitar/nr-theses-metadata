from nr_theses_metadata.records_ui.base_to_be_moved import UIResourceConfig, UIResource


class NrThesesMetadataUIResourceConfig(UIResourceConfig):
    """NrThesesMetadataRecord resource config."""

    blueprint_name = "NrThesesMetadataUI"
    url_prefix = "/records/"
    template_folder = "templates"

    detail_template = "nr_theses_metadata/records/detail.html"

    record_template_context = {
        'config_name': 'RECORD_SEARCH',   # tohle pujde do kytek
        'available_facets': {},
    }


class NrThesesMetadataUIResource(UIResource):
    pass