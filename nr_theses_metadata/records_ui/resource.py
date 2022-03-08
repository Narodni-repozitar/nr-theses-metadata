from .base_resource import UIResourceConfig, UIResource


class NrThesesMetadataUIResourceConfig(UIResourceConfig):
    """NrThesesMetadataRecord resource config."""

    blueprint_name = "NrThesesMetadataUI"
    url_prefix = "/records/"
    template_folder = "templates"

    detail_template = "nr_theses_metadata/records/detail.html"

    app_contexts = {
        'search_app_config': {
            'config_name': 'RECORD_SEARCH',   # tohle pujde do kytek
            'available_facets': {},
        }
    }


class NrThesesMetadataUIResource(UIResource):
    pass