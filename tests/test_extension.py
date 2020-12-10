# (C) Datadog, Inc. 2020-present
# All rights reserved
# Licensed under the Apache license (see LICENSE)
from pathlib import Path
from textwrap import dedent

import mkdocs_click
import pytest
from markdown import Markdown

EXPECTED = (Path(__file__).parent / "app" / "expected.md").read_text()


@pytest.mark.parametrize(
    "attr",
    [
        pytest.param(("cli", "cli"), id="cli-simple"),
        pytest.param(("cli_named", "cli"), id="cli-explicit-name"),
        pytest.param(("multi_named", "multi"), id="multi-explicit-name"),
        pytest.param(("multi", "multi"), id="no-name"),
    ],
)
def test_extension(attr):
    """
    Markdown output for a relatively complex Click application is correct.
    """
    (command, expected_name) = attr

    md = Markdown(extensions=[mkdocs_click.makeExtension()])

    source = dedent(
        """
        ::: mkdocs-click
            :module: tests.app.cli
            :command: {{cli}}
        """
    )

    source = source.replace("{{cli}}", command)

    expected = EXPECTED.replace("cli", expected_name)

    assert md.convert(source) == md.convert(expected)


def test_prog_name():
    """
    The :prog_name: attribute determines the name to display for the command.
    """
    md = Markdown(extensions=[mkdocs_click.makeExtension()])

    source = dedent(
        """
        ::: mkdocs-click
            :module: tests.app.cli
            :command: cli
            :prog_name: custom
        """
    )

    expected = EXPECTED.replace("cli", "custom")

    assert md.convert(source) == md.convert(expected)


def test_depth():
    """
    The :depth: attribute increases the level of headers.
    """
    md = Markdown(extensions=[mkdocs_click.makeExtension()])

    source = dedent(
        """
        # CLI Reference

        ::: mkdocs-click
            :module: tests.app.cli
            :command: cli
            :depth: 1
        """
    )

    expected = f"# CLI Reference\n\n{EXPECTED.replace('# ', '## ')}"

    assert md.convert(source) == md.convert(expected)


@pytest.mark.parametrize("option", ["module", "command"])
def test_required_options(option):
    """
    The module and command options are required.
    """
    md = Markdown(extensions=[mkdocs_click.makeExtension()])

    source = dedent(
        """
        ::: mkdocs-click
            :module: tests.app.cli
            :command: cli
        """
    )

    source = source.replace(f":{option}:", ":somethingelse:")

    with pytest.raises(mkdocs_click.MkDocsClickException):
        md.convert(source)
