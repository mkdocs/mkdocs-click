# (C) Datadog, Inc. 2020-present
# All rights reserved
# Licensed under the Apache license (see LICENSE)
import mock
import pytest


@pytest.fixture
def generate_docs():
    with mock.patch("mkdocs_click.extension.generate_command_docs") as generate_docs:
        yield generate_docs
