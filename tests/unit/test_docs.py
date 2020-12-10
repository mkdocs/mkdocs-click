# (C) Datadog, Inc. 2020-present
# All rights reserved
# Licensed under the Apache license (see LICENSE)
from textwrap import dedent

import click
import pytest
from mkdocs_click._docs import make_command_docs


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
    assert output == HELLO_EXPECTED.replace("hello", "hello-world")


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
