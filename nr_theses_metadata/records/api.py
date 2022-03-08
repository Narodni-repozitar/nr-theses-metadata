from invenio_pidstore.providers.recordid_v2 import RecordIdProviderV2
from invenio_records.systemfields import ConstantField
from invenio_records_resources.records.api import Record as InvenioBaseRecord
from invenio_records_resources.records.systemfields import IndexField
from invenio_records_resources.records.systemfields.pid import PIDField, PIDFieldContext

from nr_theses_metadata.records.dumper import NrThesesMetadataDumper
from nr_theses_metadata.records.models import NrThesesMetadataMetadata
from nr_theses_metadata.records.multilingual_dumper import MultilingualDumper


class NrThesesMetadataRecord(InvenioBaseRecord):
    model_cls = NrThesesMetadataMetadata
    schema = ConstantField(
        "$schema", "http://localhost/schemas/nr-theses-metadata-1.0.0.json"
    )
    index = IndexField("nr_theses_metadata-nr-theses-metadata-1.0.0")
    pid = PIDField(
        create=True, provider=RecordIdProviderV2, context_cls=PIDFieldContext
    )
    dumper_extensions = []
    dumper = NrThesesMetadataDumper(extensions=dumper_extensions)


NrThesesMetadataRecord.dumper_extensions.append(MultilingualDumper)