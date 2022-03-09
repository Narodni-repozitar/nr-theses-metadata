from copy import deepcopy
from typing import List, Dict

from nr_theses_metadata.records_ui.base_to_be_moved.resource import UIResource


class RecordTemplateContextComponent:
    config_context_name = 'record_template_context'
    config_context_key = 'record_template_context_key'
    config_context_key_default = 'search_app_config'  # TODO: better name here?
    config_sort_options = 'record_sort_options'
    config_sort_default = 'record_sort_default'
    config_sort_default_no_query = 'record_sort_default_no_query'
    config_facets = 'record_facets'

    def __init__(self, resource: UIResource):
        self.resource = resource

    def search_app_context(self, template_contexts):
        app_ctx = getattr(self.resource.config, self.config_context_name)
        opts = dict(
            endpoint=app_ctx.get('endpoint', f"/api{self.resource.api_config.url_prefix}"),
            headers={"Accept": "application/vnd.inveniordm.v1+json"},
            grid_view=False,
            # do it better
            sort=SortConfig(
                self.resource.service.config.search.sort_options,
                getattr(self.resource.config, self.config_sort_options),
                getattr(self.resource.config, self.config_sort_default),
                getattr(self.resource.config, self.config_sort_default_no_query)
            ),
            facets=FacetsConfig(self.resource.service.config.search.facets,
                                getattr(self.resource.config, self.config_facets)),
        )
        overrides = app_ctx.get('overrides') or {}

        def wrapped(**kwargs):
            _opts = {**opts, **kwargs}
            return SearchAppConfig.generate(_opts, **overrides)

        context_key = getattr(self.resource.config, self.config_context_key, self.config_context_key_default)
        template_contexts[context_key] = wrapped


class OptionsSelector:
    """Generic helper to select and validate facet/sort options."""

    def __init__(self, available_options, selected_options):
        """Initialize selector."""
        # Ensure all selected options are availabe.
        for o in selected_options:
            assert o in available_options, \
                f"Selected option '{o}' is undefined."
        self.available_options = available_options
        self.selected_options = selected_options

    def __iter__(self):
        """Iterate over options to produce RSK options."""
        for o in self.selected_options:
            yield self.map_option(o, self.available_options[o])

    def map_option(self, key, option):
        """Map an option."""
        # This interface is used in Invenio-App-RDM.
        return (key, option)


class SortOptionsSelector(OptionsSelector):
    """Sort options for the search configuration."""

    def __init__(self, available_options, selected_options, default=None,
                 default_no_query=None):
        """Initialize sort options."""
        super().__init__(available_options, selected_options)

        self.default = selected_options[0] if default is None else default
        self.default_no_query = selected_options[1] \
            if default_no_query is None else default_no_query

        assert self.default in self.available_options, \
            f"Default sort with query {self.default} is undefined."
        assert self.default_no_query in self.available_options, \
            f"Default sort without query {self.default_no_query} is undefined."


class SortConfig(SortOptionsSelector):
    """Sort options for the search configuration."""

    def map_option(self, key, option):
        """Generate a RSK search option."""
        return {
            "sortBy": key,
            "text": option['title']
        }


class FacetsConfig(OptionsSelector):
    """Facets options for the search configuration."""

    def map_option(self, key, option):
        """Generate an RSK aggregation option."""
        print(option)
        title = getattr(option, 'title', getattr(option, '_label'))

        ui = deepcopy(getattr(option, 'ui', {}))
        ui.update({
            'aggName': key,
            'title': title,
        })

        # Nested facets
        if 'childAgg' in ui:
            ui['childAgg'].setdefault('aggName', 'inner')
            ui['childAgg'].setdefault('title', title)

        return ui


class SearchAppConfig:
    """Configuration generator for React-SearchKit."""
    endpoint: str
    hidden_params: List
    app_id: str
    list_view: bool
    grid_view: bool
    default_size: int
    default_page: int
    initial_filters: List
    headers: List
    facets: List
    pagination_options: Dict
    sort: SortConfig

    default_options = dict(
        endpoint=None,
        hidden_params=None,
        app_id='oarepo-search',
        headers=None,
        list_view=True,
        grid_view=False,
        pagination_options=(10, 20, 50),
        default_size=10,
        default_page=1,
        facets=None,
        sort=None,
        initial_filters=[],
    )

    def __init__(self, configuration_options):
        """Initialize the search configuration.

        :param endpoint: The URL path to the REST API.
        :param hidden_params: Nested arrays containing any additional query
            parameters to be used in the search.
        :param app_id: The string ID of the Search Application.
        :param headers: Dictionary containing additional headers to be included
             in the request.
        :param list_view: Boolean enabling the list view of the results.
        :param grid_view: Boolean enabling the grid view of the results.
        :param pagination_options: An integer array providing the results per
            page options.
        :param default_size: An integer setting the default number of results
            per page.
        :param default_page: An integer setting the default page.
        """
        options = deepcopy(self.default_options)
        options.update(configuration_options)
        for key, value in options.items():
            setattr(self, key, value)

    @property
    def appId(self):
        """The React appplication id."""
        return self.app_id

    @property
    def initialQueryState(self):
        """Generate initialQueryState."""
        return {
            'hiddenParams': self.hidden_params,
            'layout': 'list' if self.list_view else 'grid',
            "size": self.default_size,
            "sortBy": self.sort.default,
            "page": self.default_page,
            "filters": self.initial_filters,
        }

    @property
    def searchApi(self):
        """Generate searchAPI configuration."""
        return {
            "axios": {
                "url": self.endpoint,
                "withCredentials": True,
                "headers": self.headers,
            },
            "invenio": {
                "requestSerializer":
                    "InvenioRecordsResourcesRequestSerializer",
            }
        }

    @property
    def layoutOptions(self):
        """Generate the Layout Options.

        :returns: A dict with the options for React-SearchKit JS.
        """
        return {
            'listView': self.list_view,
            'gridView': self.grid_view
        }

    @property
    def sortOptions(self):
        """Format sort options to be used in React-SearchKit JS.

        :returns: A list of dicts with sorting options for React-SearchKit JS.
        """
        return list(self.sort) if self.sort is not None else []

    @property
    def aggs(self):
        """Format the aggs configuration to be used in React-SearchKit JS.

        :returns: A list of dicts for React-SearchKit JS.
        """
        return list(self.facets) if self.facets is not None else []

    @property
    def paginationOptions(self):
        """Format the pagination options to be used in React-SearchKit JS."""
        if not getattr(self, 'default_size') or \
                self.default_size not in self.pagination_options:
            raise ValueError(
                'Parameter default_size should be part of pagination_options')
        return {
            "resultsPerPage": [
                {"text": str(option), "value": option}
                for option in self.pagination_options
            ],
            "defaultValue": self.default_size,
        }

    @property
    def defaultSortingOnEmptyQueryString(self):
        """Defines the default sorting options when there is no query."""
        return {
            "sortBy": self.sort.default_no_query,
        }

    @classmethod
    def generate(cls, options, **kwargs):
        """Create JSON config for React-Searchkit."""
        generator_object = cls(options)
        config = {
            "appId": generator_object.appId,
            "initialQueryState": generator_object.initialQueryState,
            "searchApi": generator_object.searchApi,
            "sortOptions": generator_object.sortOptions,
            "aggs": generator_object.aggs,
            "layoutOptions": generator_object.layoutOptions,
            "sortOrderDisabled": True,
            "paginationOptions": generator_object.paginationOptions,
            "defaultSortingOnEmptyQueryString":
                generator_object.defaultSortingOnEmptyQueryString

        }
        config.update(kwargs)
        return config
