import pytest
from marshmallow import ValidationError

from nr_theses_metadata.marshmallow import ThesisMetadataSchemaV2


def test_required_fields(app, db, taxonomy_tree, base_json, base_json_dereferenced):
    schema = ThesisMetadataSchemaV2()
    json = base_json
    result = schema.load(json)
    assert result == base_json_dereferenced


class TestDateDefended:
    def test_date_defended_1(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = "2020-07-01"
        field = "dateDefended"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = ThesisMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced

    def test_date_defended_2(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        # Future date is not supported
        content = "2021-12-31"
        field = "dateDefended"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = ThesisMetadataSchemaV2()
        with pytest.raises(ValidationError, match='Date cannot be in the future'):
            schema.load(base_json)

    def test_date_defended_3(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        # Future date is not supported
        content = "1699-12-31"
        field = "dateDefended"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = ThesisMetadataSchemaV2()
        with pytest.raises(ValidationError, match='Records older than from 1700 is not supported'):
            schema.load(base_json)

    def test_date_defended_4(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = "2020-07"
        field = "dateDefended"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = ThesisMetadataSchemaV2()
        with pytest.raises(ValidationError, match='Not a valid date.'):
            schema.load(base_json)

    def test_date_defended_5(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = "2020-08-23T08:50:28.585518+00:00"
        field = "dateDefended"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = ThesisMetadataSchemaV2()
        with pytest.raises(ValidationError, match='Not a valid date.'):
            schema.load(base_json)


class TestDegreeGrantor:
    def test_degree_grantor_1(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = [
            {
                "links": {
                    "self": 'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/61384984'
                }
            }
        ]
        field = "degreeGrantor"
        base_json[field] = content
        base_json_dereferenced[field] = [{
            'address': 'Malostranské náměstí 259/12, '
                       '118 00 Praha 1',
            'aliases': ['AMU'],
            'ico': '61384984',
            'is_ancestor': False,
            'level': 1,
            'links': {
                'self':
                    'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/61384984'
            },
            'provider': True,
            'related': {'rid': '51000'},
            'title': {
                'cs': 'Akademie múzických umění v Praze',
                'en': 'Academy of Performing Arts in Prague'
            },
            'type': 'veřejná VŠ',
            'url': 'https://www.amu.cz'
        }]
        schema = ThesisMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced

    def test_degree_grantor_2(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = [
            {
                "links": {
                    "self": 'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/bla'
                },
            }
        ]
        field = "degreeGrantor"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = ThesisMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)


class TestStudyField:
    def test_study_field(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = [
            {
                "links": {
                    "self": "http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/o-herectvi"
                            "-alternativniho-divadla"
                }
            }
        ]
        field = "studyField"
        base_json[field] = content
        base_json_dereferenced[field] = [{
            'AKVO': '8203R082',
            'is_ancestor': False,
            'level': 1,
            'links': {
                'self':
                    'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/o-herectvi-alternativniho'
                    '-divadla'
            },
            'title': {'cs': 'Herectví alternativního divadla'}
        }]
        schema = ThesisMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced
