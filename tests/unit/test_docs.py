# (C) Datadog, Inc. 2020-present
# All rights reserved
# Licensed under the Apache license (see LICENSE)
from textwrap import dedent

import click
import pytest

from mkdocs_click._docs import make_command_docs
from mkdocs_click._exceptions import MkDocsClickException


@click.command()
@click.option("-d", "--debug", help="Include debug output")
def hello():
    """Hello, world!"""


HELLO_EXPECTED = dedent(
    """
    # hello

    Hello, world!

    Usage:

    ```
    hello [OPTIONS]
    ```

    Options:

    ```
      -d, --debug TEXT  Include debug output
    ```

    """
).strip()


def test_make_command_docs():
    output = "\n".join(make_command_docs("hello", hello)).strip()
    assert output == HELLO_EXPECTED


def test_depth():
    output = "\n".join(make_command_docs("hello", hello, level=2)).strip()
    assert output == HELLO_EXPECTED.replace("# ", "### ")


def test_prog_name():
    output = "\n".join(make_command_docs("hello-world", hello)).strip()
    assert output == HELLO_EXPECTED.replace("# hello", "# hello-world")


def test_make_command_docs_invalid():
    with pytest.raises(
        MkDocsClickException, match="invalid is not a valid option style, which must be either `plain` or `table`."
    ):
        "\n".join(make_command_docs("hello", hello, style="invalid")).strip()


@click.command()
@click.option("-d", "--debug", help="Include debug output")
@click.option("--choice", type=click.Choice(["foo", "bar"]), default="foo")
@click.option("--date", type=click.DateTime(["%Y-%m-%d"]))
@click.option("--range-a", type=click.FloatRange(0, 1), default=0)
@click.option("--range-b", type=click.FloatRange(0))
@click.option("--range-c", type=click.FloatRange(None, 1), default=0)
@click.option("--flag/--no-flag")
def hello_table():
    """Hello, world!"""


HELLO_TABLE_EXPECTED = dedent(
    """
    # hello

    Hello, world!

    Usage:

    ```
    hello-table [OPTIONS]
    ```

    Options:

    | Name | Type | Description | Default |
    | ------ | ---- | ----------- | ------- |
    | `-d`, `--debug` | text | Include debug output | _required_ |
    | `--choice` | choice (`foo` &#x7C; `bar`) | No description given | `foo` |
    | `--date` | datetime (`%Y-%m-%d`) | No description given | _required_ |
    | `--range-a` | float range (between `0` and `1`) | No description given | `0` |
    | `--range-b` | float range (`0` and above) | No description given | _required_ |
    | `--range-c` | float range (`1` and below) | No description given | `0` |
    | `--flag` / `--no-flag` | boolean | No description given | `False` |
    """
).strip()


def test_make_command_docs_table():
    output = "\n".join(make_command_docs("hello", hello_table, style="table")).strip()
    assert output == HELLO_TABLE_EXPECTED


@click.command()
def hello_only_help():
    """Hello, world!"""


HELLO_ONLY_HELP_EXPECTED = dedent(
    """
    # hello

    Hello, world!

    Usage:

    ```
    hello-only-help [OPTIONS]
    ```
    """
).strip()


def test_make_command_docs_only_help():
    output = "\n".join(make_command_docs("hello", hello_only_help, style="table")).strip()
    assert output == HELLO_ONLY_HELP_EXPECTED


class MultiCLI(click.MultiCommand):
    def list_commands(self, ctx):
        return ["single-command"]

    def get_command(self, ctx, name):
        return hello


def test_custom_multicommand():
    """
    Custom `MultiCommand` objects are supported (i.e. not just `Group` multi-commands).
    """

    multi = MultiCLI("multi", help="Multi help")

    expected = dedent(
        """
        # multi

        Multi help

        Usage:

        ```
        multi [OPTIONS] COMMAND [ARGS]...
        ```

        ## hello

        Hello, world!

        Usage:

        ```
        multi hello [OPTIONS]
        ```

        Options:

        ```
          -d, --debug TEXT  Include debug output
        ```
        """
    ).lstrip()

    output = "\n".join(make_command_docs("multi", multi))
    assert output == expected


def test_custom_multicommand_name():
    """Custom multi commands must be given a name."""
    multi = MultiCLI()
    with pytest.raises(MkDocsClickException):
        list(make_command_docs("multi", multi))
