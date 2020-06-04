from pathlib import Path

import pytest

from mkdocs_click.parser import _make_header, _make_title, _load_command, MKClickConfigException, _parse_recursively


def test__make_header():
    assert _make_header("foo", 0) == "# foo"
    assert _make_header("foo", 3) == "#### foo"


def test___make_title():
    assert _make_title("foo", 0) == ["# foo", ""]
    assert _make_title("foo", 2) == ["### foo", ""]


def test__load_command():
    _load_command("tests.click.cli", "cli")
    with pytest.raises(MKClickConfigException):
        _load_command("tests.click.cli", "not_a_command")
    with pytest.raises(MKClickConfigException):
        _load_command("not_a_module", "cli")


def test_parse():
    expected = (Path(__file__).parent / "click" / "docs.txt").read_text()

    click_command = _load_command("tests.click.cli", "cli")
    for i in range(6):
        docs = _parse_recursively("cli", click_command, level=i)
        assert docs == expected.splitlines()
        # Update content to go one level deeper.
        expected = expected.replace("# ", "## ")
