"""Facet definitions."""

from elasticsearch_dsl import Facet
from elasticsearch_dsl.query import Nested
from flask_babelex import lazy_gettext as _
from invenio_records_resources.services.records.facets import TermsFacet


class NestedLabeledFacet(Facet):
    agg_type = "nested"

    def __init__(self, path, nested_facet, label=""):
        self._path = path
        self._inner = nested_facet
        self._label = label
        super(NestedLabeledFacet, self).__init__(
            path=path,
            aggs={
                "inner": nested_facet.get_aggregation(),
            },
        )

    def get_values(self, data, filter_values):
        return self._inner.get_values(data.inner, filter_values)

    def add_filter(self, filter_values):
        inner_q = self._inner.add_filter(filter_values)
        if inner_q:
            return Nested(path=self._path, query=inner_q)

    def get_labelled_values(self, data, filter_values):
        """Get a labelled version of a bucket."""
        try:
            out = data["buckets"]
        except:
            out = []
        return {"buckets": out, "label": str(self._label)}


metadata_dateDefended = TermsFacet(field="metadata.dateDefended", label=_('Date defended'))

metadata_defended = TermsFacet(field="metadata.defended", label=_('Defended'))

metadata_collection = TermsFacet(field="metadata.collection", label=_('Collection'))

metadata_resourceType = TermsFacet(field="metadata.resourceType", label=_('Resource type'))

metadata_dateIssued = TermsFacet(field="metadata.dateIssued", label=_('Date issued'))

metadata_dateAvailable = TermsFacet(field="metadata.dateAvailable", label=_('Date available'))

metadata_dateModified = TermsFacet(field="metadata.dateModified", label=_('Date modified'))

metadata_abstract = TermsFacet(field="metadata.abstract", label=_('Abstract'))

metadata_methods = TermsFacet(field="metadata.methods", label=_('Methods'))

metadata_technicalInfo = TermsFacet(field="metadata.technicalInfo", label=_('Technical info'))

metadata_accessRights = TermsFacet(field="metadata.accessRights", label=_('Access rights'))

metadata_version = TermsFacet(field="metadata.version", label=_('Version'))

metadata_accessibility = TermsFacet(field="metadata.accessibility", label=_('Accessibility'))

metadata_externalLocation_externalLocationURL = TermsFacet(
    field="metadata.externalLocation.externalLocationURL",
    label=_('External location URL')
)

metadata_extent = TermsFacet(field="metadata.extent", label=_('Extent'))

metadata_originalRecord = TermsFacet(field="metadata.originalRecord", label=_('Original record'))

metadata_degreeGrantor = TermsFacet(field="metadata.degreeGrantor", label=_('Degree grantor'))

metadata_studyFields = TermsFacet(field="metadata.studyFields", label=_('Study field'))

metadata_additionalTitles_title = TermsFacet(field="metadata.additionalTitles.title", label=_('Title'))

metadata_additionalTitles_titleType = TermsFacet(
    field="metadata.additionalTitles.titleType",
    label=_('Title type')
)

metadata_additionalTitles = TermsFacet(field="metadata.additionalTitles", label=_('Additional title'))

metadata_creators_fullName = TermsFacet(field="metadata.creators.fullName", label=_('Creator'))

metadata_creators_nameType = TermsFacet(field="metadata.creators.nameType", label=_('Creator type'))

metadata_creators_authorityIdentifiers_identifier = TermsFacet(
    field="metadata.creators.authorityIdentifiers.identifier",
    label=_('Creator identifier')
)

metadata_creators_authorityIdentifiers_scheme = TermsFacet(
    field="metadata.creators.authorityIdentifiers.scheme",
    label=_('Creator identifier scheme')
)

metadata_creators_authorityIdentifiers = TermsFacet(
    field="metadata.creators.authorityIdentifiers",
    label=_('Creator identifiers')
)

metadata_creators_affiliations = TermsFacet(field="metadata.creators.affiliations", label=_('Affiliation'))

metadata_creators = TermsFacet(field="metadata.creators", label=_('Creators'))

metadata_contributors_role = TermsFacet(field="metadata.contributors.role", label=_('Contributor role'))

metadata_contributors_fullName = TermsFacet(field="metadata.contributors.fullName", label=_('Contributor'))

metadata_contributors_nameType = TermsFacet(field="metadata.contributors.nameType", label=_('Contributor type'))

metadata_contributors_authorityIdentifiers_identifier = TermsFacet(
    field="metadata.contributors.authorityIdentifiers.identifier",
    label=_('Contributor identifier')
)

metadata_contributors_authorityIdentifiers_scheme = TermsFacet(
    field="metadata.contributors.authorityIdentifiers.scheme",
    label=_('Contributor identifier scheme')
)

metadata_contributors_authorityIdentifiers = TermsFacet(
    field="metadata.contributors.authorityIdentifiers",
    label=_('Contributor identifiers')
)

metadata_contributors_affiliations = TermsFacet(
    field="metadata.contributors.affiliations",
    label=_('Contributor affiliation')
)

metadata_contributors = TermsFacet(field="metadata.contributors", label=_('Contributors'))

metadata_subjects_subjectScheme = TermsFacet(field="metadata.subjects.subjectScheme", label=_('Subject scheme'))

metadata_subjects_subject = TermsFacet(field="metadata.subjects.subject", label=_('Subject'))

metadata_subjects_valueURI = TermsFacet(field="metadata.subjects.valueURI", label=_('Subject URI'))

metadata_subjects_classificationCode = TermsFacet(
    field="metadata.subjects.classificationCode",
    label=_('Subject code')
)

metadata_subjects = TermsFacet(field="metadata.subjects", label=_('Subjects'))

metadata_subjectCategories = TermsFacet(field="metadata.subjectCategories", label=_('Subject category'))

metadata_languages = TermsFacet(field="metadata.languages", label=_('Language'))

metadata_rights = TermsFacet(field="metadata.rights", label=_('License'))

metadata_relatedItems_itemURL = TermsFacet(field="metadata.relatedItems.itemURL", label=_('Related item URL'))

metadata_relatedItems_itemYear = TermsFacet(field="metadata.relatedItems.itemYear", label=_('Related item year'))

metadata_relatedItems_itemVolume = TermsFacet(field="metadata.relatedItems.itemVolume", label=_('Related item volume'))

metadata_relatedItems_itemIssue = TermsFacet(field="metadata.relatedItems.itemIssue", label=_('Related item issue'))

metadata_relatedItems_itemStartPage = TermsFacet(
    field="metadata.relatedItems.itemStartPage",
    label=_('Related item start page')
)

metadata_relatedItems_itemEndPage = TermsFacet(
    field="metadata.relatedItems.itemEndPage",
    label=_('Related item end page')
)

metadata_relatedItems_itemPublisher = TermsFacet(
    field="metadata.relatedItems.itemPublisher",
    label=_('Related item publisher')
)

metadata_relatedItems_itemRelationType = TermsFacet(
    field="metadata.relatedItems.itemRelationType",
    label=_('Related item relation')
)

metadata_relatedItems_itemResourceType = TermsFacet(
    field="metadata.relatedItems.itemResourceType",
    label=_('Related item type')
)

metadata_relatedItems_itemCreators_fullName = TermsFacet(
    field="metadata.relatedItems.itemCreators.fullName",
    label=_('Related item creator')
)

metadata_relatedItems_itemCreators_nameType = TermsFacet(
    field="metadata.relatedItems.itemCreators.nameType",
    label=_('Related item creator type')
)

metadata_relatedItems_itemCreators_authorityIdentifiers_identifier = TermsFacet(
    field="metadata.relatedItems.itemCreators.authorityIdentifiers.identifier",
    label=_('Related item creator identifier')
)

metadata_relatedItems_itemCreators_authorityIdentifiers_scheme = TermsFacet(
    field="metadata.relatedItems.itemCreators.authorityIdentifiers.scheme",
    label=_('Related item creator identifier scheme')
)

metadata_relatedItems_itemCreators_authorityIdentifiers = TermsFacet(
    field="metadata.relatedItems.itemCreators.authorityIdentifiers",
    label=_('Related item creator identifiers')
)

metadata_relatedItems_itemCreators_affiliations = TermsFacet(
    field="metadata.relatedItems.itemCreators.affiliations",
    label=_('Related item creator identifiers')
)

metadata_relatedItems_itemCreators = TermsFacet(
    field="metadata.relatedItems.itemCreators",
    label=_('Related item creators')
)

metadata_relatedItems_itemContributors_role = TermsFacet(
    field="metadata.relatedItems.itemContributors.role",
    label=_('Related item contributor role')
)

metadata_relatedItems_itemContributors_fullName = TermsFacet(
    field="metadata.relatedItems.itemContributors.fullName",
    label=_('Related item contributor')
)

metadata_relatedItems_itemContributors_nameType = TermsFacet(
    field="metadata.relatedItems.itemContributors.nameType",
    label=_('Related item contributor type')
)

metadata_relatedItems_itemContributors_authorityIdentifiers_identifier = TermsFacet(
    field="metadata.relatedItems.itemContributors.authorityIdentifiers.identifier",
    label=_('Related item contributor identifier')
)

metadata_relatedItems_itemContributors_authorityIdentifiers_scheme = TermsFacet(
    field="metadata.relatedItems.itemContributors.authorityIdentifiers.scheme",
    label=_('Related item contributor identifier scheme')
)

metadata_relatedItems_itemContributors_authorityIdentifiers = TermsFacet(
    field="metadata.relatedItems.itemContributors.authorityIdentifiers",
    label=_('Related item contributor identifiers')
)

metadata_relatedItems_itemContributors_affiliations = TermsFacet(
    field="metadata.relatedItems.itemContributors.affiliations",
    label=_('Related item contributor affiliation')
)

metadata_relatedItems_itemContributors = TermsFacet(
    field="metadata.relatedItems.itemContributors",
    label=_('Related item contributors')
)

metadata_relatedItems_itemPIDs_identifier = TermsFacet(
    field="metadata.relatedItems.itemPIDs.identifier",
    label=_('Related item PID')
)

metadata_relatedItems_itemPIDs_scheme = TermsFacet(
    field="metadata.relatedItems.itemPIDs.scheme",
    label=_('Related item PID scheme')
)

metadata_relatedItems_itemPIDs = TermsFacet(field="metadata.relatedItems.itemPIDs",
                                            label=_('Related item PIDs'))

metadata_relatedItems = TermsFacet(field="metadata.relatedItems", label=_('Related items'))

metadata_fundingReferences_projectID = TermsFacet(
    field="metadata.fundingReferences.projectID",
    label=_('Project')
)

metadata_fundingReferences_funder = TermsFacet(
    field="metadata.fundingReferences.funder",
    label=_('Funder')
)

metadata_fundingReferences = TermsFacet(field="metadata.fundingReferences", label=_('Funding'))

metadata_geoLocations_geoLocationPlace = TermsFacet(
    field="metadata.geoLocations.geoLocationPlace",
    label=_('Location')
)

metadata_geoLocations_geoLocationPoint_pointLongitude = TermsFacet(
    field="metadata.geoLocations.geoLocationPoint.pointLongitude",
    label=_('Location (Lon)')
)

metadata_geoLocations_geoLocationPoint_pointLatitude = TermsFacet(
    field="metadata.geoLocations.geoLocationPoint.pointLatitude",
    label=_('Location (Lat)')
)

metadata_geoLocations = TermsFacet(field="metadata.geoLocations", label=_('Locations'))

metadata_series_seriesTitle = TermsFacet(field="metadata.series.seriesTitle", label=_('Series title'))

metadata_series_seriesVolume = TermsFacet(field="metadata.series.seriesVolume", label=_('Series volume'))

metadata_series = TermsFacet(field="metadata.series", label=_('Series'))

metadata_objectIdentifiers_identifier = TermsFacet(
    field="metadata.objectIdentifiers.identifier",
    label=_('Identifier')
)

metadata_objectIdentifiers_scheme = TermsFacet(
    field="metadata.objectIdentifiers.scheme",
    label=_('Identifier scheme')
)

metadata_objectIdentifiers = TermsFacet(field="metadata.objectIdentifiers", label=_('Identifiers'))

metadata_systemIdentifiers_identifier = TermsFacet(
    field="metadata.systemIdentifiers.identifier",
    label=_('System identifier')
)

metadata_systemIdentifiers_scheme = TermsFacet(
    field="metadata.systemIdentifiers.scheme",
    label=_('System identifier scheme')
)

metadata_systemIdentifiers = TermsFacet(field="metadata.systemIdentifiers",
                                        label=_('System identifiers'))

metadata_events_eventDate = TermsFacet(field="metadata.events.eventDate", label=_('Event date'))

metadata_events_eventLocation_place = TermsFacet(
    field="metadata.events.eventLocation.place",
    label=_('Event place')
)

metadata_events_eventLocation_country = TermsFacet(
    field="metadata.events.eventLocation.country",
    label=_('Event country')
)

metadata_events = TermsFacet(field="metadata.events", label=_('Events'))

metadata_collections = TermsFacet(field="metadata.collections", label=_('Collections'))

_id = TermsFacet(field="id", label=_('ID'))

created = TermsFacet(field="created", label=_('Created'))

updated = TermsFacet(field="updated", label=_('Updated'))

_schema = TermsFacet(field="$schema", label=_('Schema'))
