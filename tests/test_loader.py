# (C) Datadog, Inc. 2020-present
# All rights reserved
# Licensed under the Apache license (see LICENSE)
from contextlib import nullcontext

import pytest

from mkdocs_click._exceptions import MkDocsClickException
from mkdocs_click._loader import load_command


@pytest.mark.parametrize(
    "module, command, exc, command_class",
    [
        pytest.param("tests.app.cli", "cli", None, "click.BaseCommand", id="ok"),
        pytest.param(
            "tests.app.cli",
            "doesnotexist",
            MkDocsClickException,
            "click.BaseCommand",
            id="command-does-not-exist",
        ),
        pytest.param(
            "doesnotexist", "cli", ImportError, "click.BaseCommand", id="module-does-not-exist"
        ),
        pytest.param(
            "tests.app.cli",
            "NOT_A_COMMAND",
            MkDocsClickException,
            "click.BaseCommand",
            id="not-a-command",
        ),
        pytest.param(
            "tests.app.cli",
            "cli",
            MkDocsClickException,
            "foo.Bar",
            id="bad-command-class",
        ),
        pytest.param(
            "tests.app.cli",
            "cli",
            MkDocsClickException,
            "pathlib.Path",
            id="arbitrary-command-class",
        ),
    ],
)
def test_load_command(module: str, command: str, exc, command_class: str):
    with pytest.raises(exc) if exc is not None else nullcontext():
        load_command(module, command, command_class)
