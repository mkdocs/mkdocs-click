import mock
import pytest


@pytest.fixture
def generate_docs():
    with mock.patch("mkdocs_click.extension.generate_command_docs") as generate_docs:
        yield generate_docs
