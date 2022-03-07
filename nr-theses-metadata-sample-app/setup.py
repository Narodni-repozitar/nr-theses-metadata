# -*- coding: utf-8 -*-
# Copyright (c) 2022 """CESNET."""
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""nr-theses-metadata Sample app."""

import os

from setuptools import find_packages, setup

readme = open("README.md").read()

invenio_version = "~=3.5.0a4"
invenio_search_version = ">=1.4.2,<1.5.0"
invenio_db_version = ">=1.0.11,<1.1.0"

tests_require = [
    "pytest-invenio~=1.4.2",
]

setup_requires = [
    "Babel>=2.8,<3",
]

extras_require = {
    # Invenio-Search
    "elasticsearch7": [f"invenio-search[elasticsearch7]{invenio_search_version}"],
    # Invenio-DB
    "mysql": [f"invenio-db[mysql,versioning]{invenio_db_version}"],
    "postgresql": [f"invenio-db[postgresql,versioning]{invenio_db_version}"],
    "sqlite": [f"invenio-db[versioning]{invenio_db_version}"],
    # Storage plugins
    "s3": ["invenio-s3~=1.0.5"],
    # Extras
    "docs": [
        "Sphinx==4.2.0",
    ],
    "tests": tests_require,
}

extras_require["all"] = []
for name, reqs in extras_require.items():
    if name[0] == ":" or name in ("elasticsearch7", "mysql", "postgresql", "sqlite"):
        continue
    extras_require["all"].extend(reqs)

install_requires = [
    "pyyaml>=5.4.0",
    "CairoSVG>=2.5.2,<3.0.0",
    f"invenio[base,auth,metadata,files]{invenio_version}",
    "invenio-records-resources>=0.19.0,<0.20.0",
    "invenio-requests>=0.3.0,<0.4.0",
    "invenio-logging[sentry-sdk]>=1.3.0,<1.4.0",
]

packages = find_packages()

# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join("nr_theses_metadata_sample_app", "version.py"), "rt") as fp:
    exec(fp.read(), g)
    version = g["__version__"]

setup(
    name="nr-theses-metadata-sample-app",
    version=version,
    description=__doc__,
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords="nr-theses-metadata-sample-app OARepo Invenio",
    license="MIT",
    author="CESNET",
    author_email="info@oarepo.org",
    url="https://github.com/oarepo/nr-theses-metadata-sample-app",
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    entry_points={
        "flask.commands": [
            "rdm-records = nr_theses_metadata_sample_app.cli:rdm_records",
        ],
        "invenio_config.module": [
            "nr_theses_metadata_sample_app = nr_theses_metadata_sample_app.config",
        ],
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Development Status :: 5 - Production/Stable",
    ],
)
