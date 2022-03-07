# Copyright (c) 2022 CESNET
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


"""Default configuration for nr-theses-metadata Sample app.

As a flavour extension, nr-theses-metadata Sample app doesn't define
configuration variables of its own, but rather forcefully sets other modules'
configuration variables.

Import below the configuration defined in other modules that should be
(forcefully) set in an OARepo instance, e.g.:

    from nr_theses_metadata_sample_app.config import *


The role of nr-theses-metadata Sample app is to configure other modules a specific way.
These configurations can nevertheless be overridden by either:

- Configuration file: ``<virtualenv prefix>/var/instance/invenio.cfg``
- Environment variables: ``APP_<variable name>``

WARNING: An OARepo instance should NOT install multiple flavour extensions since
         there would be no guarantee of priority anymore.
"""

from datetime import datetime, timedelta

from celery.schedules import crontab
from flask_principal import Denial
from invenio_access.permissions import any_user

# TODO: Remove when records-rest is out of communities and files
RECORDS_REST_ENDPOINTS = {}
RECORDS_UI_ENDPOINTS = {}


def _(x):
    """Identity function used to trigger string extraction."""
    return x


# Flask
# =====
# See https://flask.palletsprojects.com/en/1.1.x/config/

APP_ALLOWED_HOSTS = ["0.0.0.0", "localhost", "127.0.0.1"]
"""Allowed hosts.

Since HAProxy and Nginx route all requests no matter the host header
provided, the allowed hosts variable is set to localhost. In production it
should be set to the correct host and it is strongly recommended to only
route correct hosts to the application.
"""

MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 MiB
"""Max upload size for form data via application/multipart-formdata."""

# TODO: set
SECRET_KEY = "CHANGE_ME"
"""Flask secret key.

Each installation (dev, production, ...) needs a separate key.

SECURITY WARNING: keep the secret key used in production secret!
"""

SESSION_COOKIE_SECURE = True
"""Sets cookie with the secure flag by default."""

SESSION_COOKIE_SAMESITE = "Lax"
"""Restricts how cookies are sent with requests from external sites."""

# Flask-Limiter
# =============
# https://flask-limiter.readthedocs.io/en/stable/#configuration

RATELIMIT_STORAGE_URL = "redis://localhost:6379/3"
"""Storage for ratelimiter."""

# Increase defaults
RATELIMIT_AUTHENTICATED_USER = "25000 per hour;1000 per minute"

RATELIMIT_GUEST_USER = "5000 per hour;500 per minute"

# Flask-Babel
# ===========
# See https://pythonhosted.org/Flask-Babel/#configuration

BABEL_DEFAULT_LOCALE = "cs"
"""Default locale (language)."""

BABEL_DEFAULT_TIMEZONE = "Europe/Prague"
"""Default time zone."""

# Invenio-I18N
# ============
# See https://invenio-i18n.readthedocs.io/en/latest/configuration.html

# Other supported languages (do not include BABEL_DEFAULT_LOCALE in list).
# I18N_LANGUAGES = [
#     ('fr', _('French'))
# ]

# Invenio-Communities
# ===================

COMMUNITIES_ENABLED = False
"""Control if community views and endpoints are enabled."""


# Invenio-Files-REST
# ==================
# See https://invenio-files-rest.readthedocs.io/en/latest/configuration.html


def files_rest_permission_factory(obj, action):
    """Generate a denying permission."""
    return Denial(any_user)


FILES_REST_PERMISSION_FACTORY = files_rest_permission_factory
"""Set default files permission factory do DENY all."""

# Invenio-IIIF
# =================
# See https://invenio-iiif.readthedocs.io/en/latest/configuration.html

# IIIF_PREVIEW_TEMPLATE = "nr_theses_metadata_sample_app/records/iiif_preview.html"
# """Template for IIIF image preview."""

# IIIF_API_DECORATOR_HANDLER = None
# IIIF_IMAGE_OPENER_HANDLER = "nr_theses_metadata_sample_app.resources.iiif:image_opener"

# Invenio-Previewer
# =================
# See https://github.com/inveniosoftware/invenio-previewer/blob/master/invenio_previewer/config.py  # noqa

PREVIEWER_PREFERENCE = [
    "csv_dthreejs",
    # TODO: IIIF checks bucket-level permissions, and thus won't work
    # 'iiif_image',
    "simple_image",
    "json_prismjs",
    "xml_prismjs",
    "mistune",
    "pdfjs",
    "ipynb",
    "zip",
    "txt",
]
"""Preferred previewers."""

# Invenio-Formatter
# =================

FORMATTER_BADGES_ALLOWED_TITLES = ["DOI", "doi"]
"""List of allowed titles in badges."""

FORMATTER_BADGES_TITLE_MAPPING = {"doi": "DOI"}
"""Mapping of titles."""

# Invenio-Mail / Flask-Mail
# =========================
# See https://pythonhosted.org/Flask-Mail/#configuring-flask-mail

MAIL_SUPPRESS_SEND = True
"""Disable email sending by default."""

# Flask-Collect
# =============
# See https://github.com/klen/Flask-Collect#setup

COLLECT_STORAGE = "flask_collect.storage.file"
"""Static files collection method (defaults to copying files)."""

# Invenio-Accounts
# ================
# (Flask-Security, Flask-Login, Flask-Principal, Flask-KVSession)
# See https://invenio-accounts.readthedocs.io/en/latest/configuration.html
# See https://flask-security.readthedocs.io/en/3.0.0/configuration.html

ACCOUNTS_SESSION_REDIS_URL = "redis://localhost:6379/1"
"""Redis session storage URL."""

ACCOUNTS_USERINFO_HEADERS = True
"""Enable session/user id request tracing.

This feature will add X-Session-ID and X-User-ID headers to HTTP response. You
MUST ensure that NGINX (or other proxies) removes these headers again before
sending the response to the client. Set to False, in case of doubt.
"""

SECURITY_EMAIL_SENDER = "info@oarepo.org"
"""Email address used as sender of account registration emails."""

SECURITY_EMAIL_SUBJECT_REGISTER = _("Welcome to nr-theses-metadata Sample app!")
"""Email subject for account registration emails."""

# Invenio-Celery / Celery / Flask-Celeryext
# =========================================
# See https://invenio-celery.readthedocs.io/en/latest/configuration.html
# See docs.celeryproject.org/en/latest/userguide/configuration.html
# See https://flask-celeryext.readthedocs.io/en/latest/

BROKER_URL = "amqp://guest:guest@localhost:5672/"
"""URL of message broker for Celery 3 (default is RabbitMQ)."""

CELERY_BEAT_SCHEDULE = {
    # 'indexer': {
    #     'task': 'invenio_indexer.tasks.process_bulk_queue',
    #     'schedule': timedelta(minutes=5),
    # },
    "accounts_sessions": {
        "task": "invenio_accounts.tasks.clean_session_table",
        "schedule": timedelta(minutes=60),
    },
    "accounts_ips": {
        "task": "invenio_accounts.tasks.delete_ips",
        "schedule": timedelta(hours=6),
    },
    "draft_resources": {
        "task": ("invenio_drafts_resources.services.records.tasks.cleanup_drafts"),
        "schedule": timedelta(minutes=60),
    },
}
"""Scheduled tasks configuration (aka cronjobs)."""

CELERY_BROKER_URL = BROKER_URL
"""Same as BROKER_URL to support Celery 4."""

CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
"""URL of backend for result storage (default is Redis)."""

# Flask-SQLAlchemy
# ================
# See https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/

SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://nr-theses-metadata-sample-app: \
    nr-theses-metadata-sample-app@db/nr-theses-metadata-sample-app"
"""Database URI including user and password.

Default value is provided to make module testing easier.
"""

SQLALCHEMY_ECHO = False
"""Enable to see all SQL queries."""

SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_pre_ping": False,
    "pool_recycle": 3600,
    # set a more agressive timeout to ensure http requests don't wait for long
    "pool_timeout": 10,
}
"""SQLAlchemy engine options.

This is used to configure for instance the database connection pool.
Specifically for connection pooling the following options below are relevant.
Note, that the connection pool settings have to be aligned with:

1. your database server's max allowed connections settings, and
2. your application deployment (number of processes/threads)

**Disconnect handling**

Note, it's possible that a connection you get from the connection pool is no
longer open. This happens if e.g. the database server was restarted or the
server has a timeout that closes the connection. In these case you'll see an
error similar to::

    psycopg2.OperationalError: server closed the connection unexpectedly
        This probably means the server terminated abnormally
        before or while processing the request.

The errors can be avoided by using the ``pool_pre_ping`` option, which will
ensure the connection is open first by issuing a ``SELECT 1``. The pre-ping
feature however, comes with a performance penalty, and thus it may be better
to first try adjusting the ``pool_recyle`` to ensure connections are closed and
reopened regularly.

... code-block:: python

    SQLALCHEMY_ENGINE_OPTIONS = dict(
        # enable the connection pool “pre-ping” feature that tests connections
        # for liveness upon each checkout.
        pool_pre_ping=True,

        # the number of connections to allow in connection pool “overflow”,
        # that is connections that can be opened above and beyond the
        # pool_size setting
        max_overflow=10,

        # the number of connections to keep open inside the connection
        pool_size=5,

        # recycle connections after the given number of seconds has passed.
        pool_recycle=3600,

        # number of seconds to wait before giving up on getting a connection
        # from the pool
        pool_timeout=30,
    )

See https://docs.sqlalchemy.org/en/latest/core/engines.html.
"""

# Disable logging user information in SQLAlchemy-Continuum. This setting is not
# documented on purpose, since we don't want administrators to be aware of the
# setting.
DB_VERSIONING_USER_MODEL = None

# Invenio-JSONSchemas/Invenio-Records
# ===================================
# See https://invenio-jsonschemas.readthedocs.io/en/latest/configuration.html

JSONSCHEMAS_REGISTER_ENDPOINTS_API = False
"""Don't' register schema endpoints."""

JSONSCHEMAS_REGISTER_ENDPOINTS_UI = False
"""Don't' register schema endpoints."""

JSONSCHEMAS_HOST = "unused"
# This variable is set to something different than localhost to avoid a warning
# being issued. The value is however not used, because of the two variables
# set below.

RECORDS_REFRESOLVER_CLS = "invenio_records.resolver.InvenioRefResolver"
"""Custom JSONSchemas ref resolver class.

Note that when using a custom ref resolver class you should also set
``RECORDS_REFRESOLVER_STORE`` to point to a JSONSchema ref resolver store.
"""

RECORDS_REFRESOLVER_STORE = "invenio_jsonschemas.proxies.current_refresolver_store"
"""JSONSchemas ref resolver store.

Used together with ``RECORDS_REFRESOLVER_CLS`` to provide a specific
ref resolver store.
"""

# OAI-PMH
# =======
# See https://github.com/inveniosoftware/invenio-oaiserver/blob/master/invenio_oaiserver/config.py  # noqa
# (Using GitHub because documentation site out-of-sync at time of writing)

OAISERVER_ID_PREFIX = "oai:nr-theses-metadata-sample-app.org:"
"""The prefix that will be applied to the generated OAI-PMH ids."""

OAISERVER_REGISTER_RECORD_SIGNALS = False
OAISERVER_REGISTER_SET_SIGNALS = False
"""Before enabling OAI server signals, fully configure the server first."""

# Flask-DebugToolbar
# ==================
# See https://flask-debugtoolbar.readthedocs.io/en/latest/#configuration
# Flask-DebugToolbar is by default enabled when the application is running in
# debug mode. More configuration options are available above

DEBUG_TB_INTERCEPT_REDIRECTS = False
"""Switches off incept of redirects by Flask-DebugToolbar."""

# Flask-Caching
# =============
# See https://flask-caching.readthedocs.io/en/latest/index.html#configuring-flask-caching  # noqa

CACHE_REDIS_URL = "redis://localhost:6379/0"
"""URL to connect to Redis server."""

CACHE_TYPE = "flask_caching.backends.redis"
"""Use Redis caching object."""

ACCESS_CACHE = "invenio_cache:current_cache"
"""Use the cache for permmissions caching."""

# Invenio-Search
# ==============
# See https://invenio-search.readthedocs.io/en/latest/configuration.html

SEARCH_ELASTIC_HOSTS = [{"host": "localhost", "port": 9200}]
"""Elasticsearch hosts."""

# Invenio-Indexer
# ===============
# See https://invenio-indexer.readthedocs.io/en/latest/configuration.html

INDEXER_DEFAULT_INDEX = "-record-v1.0.0"
"""Default index to use if no schema is defined."""

# Invenio-Base
# ============
# See https://invenio-base.readthedocs.io/en/latest/api.html#invenio_base.wsgi.wsgi_proxyfix  # noqa

WSGI_PROXIES = 2
"""Correct number of proxies in front of your application."""

# Invenio-Admin
# =============

# Admin interface is deprecated and should not be used.
ADMIN_PERMISSION_FACTORY = "nr_theses_metadata_sample_app.admin.permission_factory"

# Invenio-REST
# ------------
REST_CSRF_ENABLED = True
# TODO: remove when https://github.com/inveniosoftware/invenio-rest/issues/125
# is solved
CSRF_HEADER = "X-CSRFToken"

# Invenio-Vocabularies
# =============

# VOCABULARIES_DATASTREAM_READERS = {
#     **VOCABULARIES_DATASTREAM_READERS,
#     **NAMES_READERS,
# }
# """Data Streams readers."""

# VOCABULARIES_DATASTREAM_TRANSFORMERS = {
#     **VOCABULARIES_DATASTREAM_TRANSFORMERS,
#     **NAMES_TRANSFORMERS,
# }
# """Data Streams transformers."""

# VOCABULARIES_DATASTREAM_WRITERS = {
#     **VOCABULARIES_DATASTREAM_WRITERS,
#     **NAMES_WRITERS,
# }
# """Data Streams writers."""

# nr-theses-metadata-sample-app
# ===============

_DASHBOARD_ROUTES = ["uploads", "communities", "requests"]

APP_ROUTES = {
    "index": "/",
    "help_search": "/help/search",
    "record_search": "/search2",
    "record_detail": "/records/<pid_value>",
    "record_export": "/records/<pid_value>/export/<export_format>",
    "record_file_preview": "/records/<pid_value>/preview/<path:filename>",
    "record_file_download": "/records/<pid_value>/files/<path:filename>",
    "record_from_pid": "/<any({schemes}):pid_scheme>/<path:pid_value>",
    "record_latest": "/records/<pid_value>/latest",
    "dashboard_home": "/me",
    "dashboard_item": "/me/<any({routes}):dashboard_name>".format(
        routes=",".join(_DASHBOARD_ROUTES)
    ),
    "deposit_create": "/uploads/new",
    "deposit_edit": "/uploads/<pid_value>",
}

APP_RECORD_EXPORTERS = {
    "json": {
        "name": _("JSON"),
        "serializer": ("flask_resources.serializers:JSONSerializer"),
        "content-type": "application/json",
        "filename": "{id}.json",
    }
}

APP_RECORDS_EXPORT_URL = "/records/<pid_value>/export/<export_format>"

APP_DEPOSIT_FORM_DEFAULTS = {}
"""Default values for new records in the deposit UI.

The keys denote the dot-separated path, where in the record's metadata
the values should be set (see invenio-records.dictutils).
If the value is callable, its return value will be used for the field
(e.g. lambda/function for dynamic calculation of values).
"""

APP_DEPOSIT_FORM_AUTOCOMPLETE_NAMES = "search"
"""Behavior for autocomplete names search field for creators/contributors.

Available options:

- ``search`` (default): Show search field and form always.
- ``search_only``: Only show search field. Form displayed after selection or
explicit "manual" entry.
- ``off``: Only show person form (no search field).
"""

CITATION_STYLES = [
    ("apa", _("APA")),
    ("harvard-cite-them-right", _("Harvard")),
    ("modern-language-association", _("MLA")),
    ("vancouver", _("Vancouver")),
    ("chicago-fullnote-bibliography", _("Chicago")),
    ("ieee", _("IEEE")),
]
"""List of citation style """

CITATION_STYLES_DEFAULT = "apa"
"""Default citation style"""

APP_DETAIL_SIDE_BAR_TEMPLATES = [
    # "nr_theses_metadata_sample_app/records/details/side_bar/metrics.html",
    # "nr_theses_metadata_sample_app/records/details/side_bar/versions.html",
    # "nr_theses_metadata_sample_app/records/details/side_bar/keywords_subjects.html",
    # "nr_theses_metadata_sample_app/records/details/side_bar/details.html",
    # "nr_theses_metadata_sample_app/records/details/side_bar/licenses.html",
    # "nr_theses_metadata_sample_app/records/details/side_bar/export.html",
]
"""Template names for record detail view sidebar components"""

SEARCH_USER_COMMUNITIES = {
    "facets": ["visibility", "type"],
    "sort": ["bestmatch", "newest", "oldest"],
}
"""User communities search configuration (i.e list of user communities)"""

SEARCH_USER_REQUESTS = {
    "facets": ["type", "status"],
    "sort": ["bestmatch", "newest", "oldest"],
}
"""User requests search configuration (i.e list of user requests)"""

REQUESTS_ROUTES = {
    "details": "/me/requests/<pid_value>",
    "user-dashboard-community-submission": "/me/requests/<pid_value>",
}

RECORD_SEARCH = {
    "sort": [],
    "sort_default": "newest",
    "sort_default_no_query": "newest"
}

RECORD_FACETS = {}

COMMUNITIES_FACETS = {}

RECORD_SORT_OPTIONS = {
    "bestmatch": dict(
        title=_('Best match'),
        fields=['_score'],  # ES defaults to desc on `_score` field
    ),
    "newest": dict(
        title=_('Newest'),
        fields=['-created'],
    ),
    "oldest": dict(
        title=_('Oldest'),
        fields=['created'],
    )
}
