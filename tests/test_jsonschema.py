from invenio_jsonschemas import current_jsonschemas
from invenio_records.api import _records_state


def test_json(app, base_json):
    print("\n\n\n\n\n")
    print("START")
    print(app)
    print(current_jsonschemas.list_schemas())
    _records_state.validate(base_json, "https://nusl.cz/schemas/nr_theses_metadata/nr-theses-metadata-v1.0.0.json")
