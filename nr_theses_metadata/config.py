from nr_theses_metadata.records_ui.resource import NrThesesMetadataUIResourceConfig, NrThesesMetadataUIResource
from nr_theses_metadata.resources.config import NrThesesMetadataResourceConfig
from nr_theses_metadata.resources.resource import NrThesesMetadataResource
from nr_theses_metadata.services.config import NrThesesMetadataServiceConfig
from nr_theses_metadata.services.facets import metadata_accessRights, metadata_languages, metadata_resourceType
from nr_theses_metadata.services.service import NrThesesMetadataService

NR_THESES_METADATA_RESOURCE_CONFIG = NrThesesMetadataResourceConfig
NR_THESES_METADATA_RESOURCE_CLASS = NrThesesMetadataResource
NR_THESES_METADATA_SERVICE_CONFIG = NrThesesMetadataServiceConfig
NR_THESES_METADATA_SERVICE_CLASS = NrThesesMetadataService
NR_THESES_METADATA_UI_RESOURCE_CONFIG = NrThesesMetadataUIResourceConfig
NR_THESES_METADATA_UI_RESOURCE_CLASS = NrThesesMetadataUIResource

# TODO: generate UI routes from data model
APP_UI_ROUTES = {
    "index": "/",
    "help_search": "/help/search",
    "record_search": "/search",
    "record_detail": "/records/<pid_value>",
    "record_export": "/records/<pid_value>/export/<export_format>",
    "record_file_preview": "/records/<pid_value>/preview/<path:filename>",
    "record_file_download": "/records/<pid_value>/files/<path:filename>",
    "record_from_pid": "/<any({schemes}):pid_scheme>/<path:pid_value>",
    "record_latest": "/records/<pid_value>/latest",
    "deposit_create": "/uploads/new",
    "deposit_edit": "/uploads/<pid_value>",
}

# TODO: generate facet config by model builder
APP_SEARCH_FACETS = {
    'access_status': {
        'facet': metadata_accessRights,
        'ui': {
            'field': 'accessRights',
        }
    },
    
    'language': {
        'facet': metadata_languages,
        'ui': {
            'field': 'languages',
        }
    },
    'resource_type': {
        'facet': metadata_resourceType,
        'ui': {
            'field': 'resourceType.type',
            'childAgg': {
                'field': 'resourceType.subtype',
            }
        }
    }
}