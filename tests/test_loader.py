# (C) Datadog, Inc. 2020-present
# All rights reserved
# Licensed under the Apache license (see LICENSE)
from contextlib import nullcontext

import pytest

from mkdocs_click._exceptions import MkDocsClickException
from mkdocs_click._loader import load_command


@pytest.mark.parametrize(
    "module, command, exc",
    [
        pytest.param("tests.app.cli", "cli", None, id="ok"),
        pytest.param(
            "tests.app.cli", "doesnotexist", MkDocsClickException, id="command-does-not-exist"
        ),
        pytest.param("doesnotexist", "cli", ImportError, id="module-does-not-exist"),
        pytest.param("tests.app.cli", "NOT_A_COMMAND", MkDocsClickException, id="not-a-command"),
    ],
)
def test_load_command(module: str, command: str, exc):
    with pytest.raises(exc) if exc is not None else nullcontext():  # type: ignore
        load_command(module, command)
