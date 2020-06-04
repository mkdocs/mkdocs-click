# (C) Datadog, Inc. 2020-present
# All rights reserved
# Licensed under the Apache license (see LICENSE)
from contextlib import nullcontext
from pathlib import Path

import pytest

from mkdocs_click.parser import _make_header, _make_title, _load_command, MKClickConfigException, _make_command_docs


def test__make_header():
    assert _make_header("foo", 0) == "# foo"
    assert _make_header("foo", 3) == "#### foo"


def test__make_title():
    assert list(_make_title("foo", 0)) == ["# foo", ""]
    assert list(_make_title("foo", 2)) == ["### foo", ""]


@pytest.mark.parametrize(
    "module, command, exc",
    [
        pytest.param("tests.click.cli", "cli", None, id="ok"),
        pytest.param("tests.click.cli", "doesnotexist", MKClickConfigException, id="command-does-not-exist"),
        pytest.param("doesnotexist", "cli", MKClickConfigException, id="module-does-not-exist"),
    ],
)
def test__load_command(module: str, command: str, exc):
    with pytest.raises(exc) if exc is not None else nullcontext():
        _load_command(module, command)


@pytest.mark.parametrize("level", range(6))
def test_parse(level: int):
    expected = (Path(__file__).parent / "click" / "docs.txt").read_text()
    expected = expected.replace("# ", f"{'#' * (level + 1)} ")
    expected = f"{expected}\n"  # Include final newline.

    click_command = _load_command("tests.click.cli", "cli")

    docs = list(_make_command_docs("cli", click_command, level=level))
    assert docs == expected.splitlines()
