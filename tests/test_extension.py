# (C) Datadog, Inc. 2020-present
# All rights reserved
# Licensed under the Apache license (see LICENSE)
from pathlib import Path
from textwrap import dedent

import pytest
from markdown import Markdown

import mkdocs_click

EXPECTED = (Path(__file__).parent / "app" / "expected.md").read_text()
EXPECTED_ENHANCED = (Path(__file__).parent / "app" / "expected-enhanced.md").read_text()
EXPECTED_SUB = (Path(__file__).parent / "app" / "expected-sub.md").read_text()
EXPECTED_SUB_ENHANCED = (Path(__file__).parent / "app" / "expected-sub-enhanced.md").read_text()


@pytest.mark.parametrize(
    "command, expected_name",
    [
        pytest.param("cli", "cli", id="cli-simple"),
        pytest.param("cli_named", "cli", id="cli-explicit-name"),
        pytest.param("multi_named", "multi", id="multi-explicit-name"),
        pytest.param("multi", "multi", id="no-name"),
    ],
)
def test_extension(command, expected_name):
    """
    Markdown output for a relatively complex Click application is correct.
    """
    md = Markdown(extensions=[mkdocs_click.makeExtension()])

    source = dedent(
        f"""
        ::: mkdocs-click
            :module: tests.app.cli
            :command: {command}
        """
    ).rstrip()

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


def test_enhanced_titles():
    """
    If `attr_list` extension is registered, section titles are enhanced with full command paths.

    See: https://github.com/DataDog/mkdocs-click/issues/35
    """
    md = Markdown(extensions=["attr_list"])
    # Register our extension as a second step, so that we see `attr_list`.
    # This is what MkDocs does, so there's no hidden usage constraint here.
    md.registerExtensions([mkdocs_click.makeExtension()], {})

    source = dedent(
        """
        ::: mkdocs-click
            :module: tests.app.cli
            :command: cli
        """
    )

    assert md.convert(source) == md.convert(EXPECTED_ENHANCED)


@pytest.mark.parametrize(
    "command, expected_name",
    [
        pytest.param("cli", "cli", id="cli-simple"),
        pytest.param("cli_named", "cli", id="cli-explicit-name"),
        pytest.param("multi_named", "multi", id="multi-explicit-name"),
        pytest.param("multi", "multi", id="no-name"),
    ],
)
def test_extension_with_subcommand(command, expected_name):
    """
    Markdown output for a relatively complex Click application is correct.
    """
    md = Markdown(extensions=[mkdocs_click.makeExtension()])

    source = dedent(
        f"""
        ::: mkdocs-click
            :module: tests.app.cli
            :command: {command}
            :list_subcommands: True
        """
    )

    expected = EXPECTED_SUB.replace("cli", expected_name)

    assert md.convert(source) == md.convert(expected)


@pytest.mark.parametrize(
    "command, expected_name",
    [
        pytest.param("cli", "cli", id="cli-simple"),
        pytest.param("cli_named", "cli", id="cli-explicit-name"),
        pytest.param("multi_named", "multi", id="multi-explicit-name"),
        pytest.param("multi", "multi", id="no-name"),
    ],
)
def test_enhanced_titles_with_subcommand(command, expected_name):
    """
    Markdown output for a relatively complex Click application is correct.
    """
    md = Markdown(extensions=["attr_list"])
    # Register our extension as a second step, so that we see `attr_list`.
    # This is what MkDocs does, so there's no hidden usage constraint here.
    md.registerExtensions([mkdocs_click.makeExtension()], {})

    source = dedent(
        f"""
        ::: mkdocs-click
            :module: tests.app.cli
            :command: {command}
            :list_subcommands: True
        """
    )

    expected = EXPECTED_SUB_ENHANCED.replace("cli", expected_name)

    assert md.convert(source) == md.convert(expected)
