from nr_theses_metadata.records_ui.resource import NrThesesMetadataRecordsUIResourceConfig, \
    NrThesesMetadataRecordsUIResource
from nr_theses_metadata.resources.config import NrThesesMetadataResourceConfig
from nr_theses_metadata.resources.resource import NrThesesMetadataResource
from nr_theses_metadata.services.config import NrThesesMetadataServiceConfig
from nr_theses_metadata.services.facets import metadata_accessRights, metadata_languages, metadata_resourceType
from nr_theses_metadata.services.service import NrThesesMetadataService
from nr_theses_metadata.theme.resource import NrThesesMetadataUIResource, NrThesesMetadataUIResourceConfig

NR_THESES_METADATA_RESOURCE_CONFIG = NrThesesMetadataResourceConfig
NR_THESES_METADATA_RESOURCE_CLASS = NrThesesMetadataResource
NR_THESES_METADATA_SERVICE_CONFIG = NrThesesMetadataServiceConfig
NR_THESES_METADATA_SERVICE_CLASS = NrThesesMetadataService
NR_THESES_METADATA_UI_RESOURCE_CONFIG = NrThesesMetadataUIResourceConfig
NR_THESES_METADATA_UI_RESOURCE_CLASS = NrThesesMetadataUIResource
NR_THESES_METADATA_RECORDS_UI_RESOURCE_CONFIG = NrThesesMetadataRecordsUIResourceConfig
NR_THESES_METADATA_RECORDS_UI_RESOURCE_CLASS = NrThesesMetadataRecordsUIResource

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
