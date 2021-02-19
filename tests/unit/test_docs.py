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
      --help            Show this message and exit.
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
    assert output == HELLO_EXPECTED.replace("hello", "hello-world")


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
    hello [OPTIONS]
    ```

    Options:

    | Name | Type | Description | Default |
    | ---- | ---- | ----------- | ------- |
    | `-d`, `--debug` | text | Include debug output | _required_ |
    | `--choice` | choice (`foo` &#x7C; `bar`) | N/A | `foo` |
    | `--date` | datetime (`%Y-%m-%d`) | N/A | _required_ |
    | `--range-a` | float range (between `0` and `1`) | N/A | `0` |
    | `--range-b` | float range (`0` and above) | N/A | _required_ |
    | `--range-c` | float range (`1` and below) | N/A | `0` |
    | `--flag` / `--no-flag` | boolean | N/A | `False` |
    | `--help` | boolean | Show this message and exit. | `False` |
    """
).strip()


def test_make_command_docs_table():
    output = "\n".join(make_command_docs("hello", hello_table, style="table")).strip()
    assert output == HELLO_TABLE_EXPECTED


@click.command()
def hello_minimal():
    """Hello, world!"""


HELLO_TABLE_MINIMAL_EXPECTED = dedent(
    """
    # hello

    Hello, world!

    Usage:

    ```
    hello [OPTIONS]
    ```

    Options:

    | Name | Type | Description | Default |
    | ---- | ---- | ----------- | ------- |
    | `--help` | boolean | Show this message and exit. | `False` |
    """
).strip()


def test_make_command_docs_table_minimale():
    output = "\n".join(make_command_docs("hello", hello_minimal, style="table")).strip()
    assert output == HELLO_TABLE_MINIMAL_EXPECTED


class MultiCLI(click.MultiCommand):
    def list_commands(self, ctx):
        return ["single-command"]

    def get_command(self, ctx, name):
        return hello


@pytest.mark.parametrize(
    "multi",
    [
        pytest.param(MultiCLI("multi", help="Multi help"), id="explicit-name"),
        pytest.param(MultiCLI(help="Multi help"), id="no-name"),
    ],
)
def test_custom_multicommand(multi):
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

        Options:

        ```
          --help  Show this message and exit.
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
          --help            Show this message and exit.
        ```
        """
    ).lstrip()

    output = "\n".join(make_command_docs("multi", multi))
    assert output == expected
