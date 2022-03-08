from nr_theses_metadata.records_ui.base_to_be_moved.resource import UIResource
from nr_theses_metadata.records_ui.searchapp import sort_config, facets_config, SearchAppConfig


class RecordTemplateProcessor:
    template_context_name = 'record_template_context'
    template_context_key = 'record_template_context_key'
    template_context_key_default = 'search_app_config'  # TODO: better name here?

    def __init__(self, resource: UIResource):
        self.resource = resource

    def search_app_context(self, template_contexts):
        app_ctx = getattr(self.resource.config, self.template_context_name)
        opts = dict(
            endpoint=app_ctx.get('endpoint', self.resource.api_config.url_prefix),
            headers={"Accept": "application/json"},
            grid_view=False,
            # do it better
            sort=sort_config(app_ctx['config_name']),
            facets=facets_config(app_ctx['config_name'], app_ctx['available_facets']),
        )
        overrides = app_ctx.get('overrides') or {}

        def wrapped(**kwargs):
            _opts = {**opts, **kwargs}
            return SearchAppConfig.generate(_opts, **overrides)

        context_key = getattr(self.resource.config, self.template_context_key, self.template_context_key_default)
        template_contexts[context_key] = wrapped
