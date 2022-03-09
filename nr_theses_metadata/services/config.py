from invenio_records_resources.services import RecordLink
from invenio_records_resources.services import (
    RecordServiceConfig as InvenioRecordServiceConfig,
)
from invenio_records_resources.services import pagination_links
from invenio_records_resources.services.records.components import (
    DataComponent,
    MetadataComponent,
)

from nr_theses_metadata.records.api import NrThesesMetadataRecord
from nr_theses_metadata.services.permissions import NrThesesMetadataPermissionPolicy
from nr_theses_metadata.services.schema import NrThesesMetadataSchema
from nr_theses_metadata.services.search import NrThesesMetadataSearchOptions


class NrThesesMetadataServiceConfig(InvenioRecordServiceConfig):
    """NrThesesMetadataRecord service config."""

    permission_policy_cls = NrThesesMetadataPermissionPolicy
    schema = NrThesesMetadataSchema
    search = NrThesesMetadataSearchOptions
    record_cls = NrThesesMetadataRecord

    components = [*InvenioRecordServiceConfig.components]

    model = "nr_theses_metadata"

    @property
    def links_item(self):
        return {
            "self": RecordLink("/api/nr_theses_metadata/{id}"),
        }

    links_search = pagination_links("/nr_theses_metadata/{?args*}")
