# (C) Datadog, Inc. 2020-present
# All rights reserved
# Licensed under the Apache license (see LICENSE)
from textwrap import dedent
from typing import cast

import click
import pytest

from mkdocs_click._docs import make_command_docs, _show_options
from mkdocs_click._exceptions import MkDocsClickException


@click.command()
@click.option("-d", "--debug", help="Include debug output")
def hello():
    """Hello, world!"""


@click.command()
@click.option("-d", "--debug", help="Include debug output")
def hello_escape_marker():
    """
    \b
    Hello, world!
    """


@click.command()
@click.option("-d", "--debug", help="Include debug output")
def hello_ascii_art():
    """
    \b
      ______  __       __    ______  __  ___
     /      ||  |     |  |  /      ||  |/  /
    |  ,----'|  |     |  | |  ,----'|  '  /
    |  |     |  |     |  | |  |     |    <
    |  `----.|  `----.|  | |  `----.|  .  \\
     \\______||_______||__|  \\______||__|\\__\\

    Hello, world!
    """


HELLO_EXPECTED = dedent(
    """
    # hello

    Hello, world!

    **Usage:**

    ```text
    hello [OPTIONS]
    ```

    **Options:**

    ```text
      -d, --debug TEXT  Include debug output
      --help            Show this message and exit.
    ```
    """
).lstrip()


def test_basic():
    output = "\n".join(make_command_docs("hello", hello))
    assert output == HELLO_EXPECTED


def test_depth():
    output = "\n".join(make_command_docs("hello", hello, depth=2))
    assert output == HELLO_EXPECTED.replace("# ", "### ")


def test_prog_name():
    output = "\n".join(make_command_docs("hello-world", hello))
    assert output == HELLO_EXPECTED.replace("hello", "hello-world")


def test_style_invalid():
    with pytest.raises(
        MkDocsClickException, match="invalid is not a valid option style, which must be either `plain` or `table`."
    ):
        list(make_command_docs("hello", hello, style="invalid"))


def test_basic_escape_marker():
    output = "\n".join(make_command_docs("hello", hello_escape_marker))
    assert output == HELLO_EXPECTED


def test_basic_ascii_art():
    output = "\n".join(make_command_docs("hello", hello_ascii_art, remove_ascii_art=True))
    assert output == HELLO_EXPECTED


@click.command()
@click.option("-d", "--debug", help="Include debug output")
@click.option("--choice", type=click.Choice(["foo", "bar"]), default="foo")
@click.option("--date", type=click.DateTime(["%Y-%m-%d"]))
@click.option("--range-a", type=click.FloatRange(0, 1), default=0)
@click.option("--range-b", type=click.FloatRange(0))
@click.option("--range-c", type=click.FloatRange(None, 1), default=0)
@click.option("--flag/--no-flag")
def hello_full():
    """Hello, world!"""


HELLO_FULL_TABLE_EXPECTED = dedent(
    """
    # hello

    Hello, world!

    **Usage:**

    ```text
    hello [OPTIONS]
    ```

    **Options:**

    | Name | Type | Description | Default |
    | ---- | ---- | ----------- | ------- |
    | `-d`, `--debug` | text | Include debug output | None |
    | `--choice` | choice (`foo` &#x7C; `bar`) | N/A | `foo` |
    | `--date` | datetime (`%Y-%m-%d`) | N/A | None |
    | `--range-a` | float range (between `0` and `1`) | N/A | `0` |
    | `--range-b` | float range (`0` and above) | N/A | None |
    | `--range-c` | float range (`1` and below) | N/A | `0` |
    | `--flag` / `--no-flag` | boolean | N/A | `False` |
    | `--help` | boolean | Show this message and exit. | `False` |
    """
).lstrip()


@click.command()
def hello_minimal():
    """Hello, world!"""


HELLO_MINIMAL_TABLE_EXPECTED = dedent(
    """
    # hello

    Hello, world!

    **Usage:**

    ```text
    hello [OPTIONS]
    ```

    **Options:**

    | Name | Type | Description | Default |
    | ---- | ---- | ----------- | ------- |
    | `--help` | boolean | Show this message and exit. | `False` |
    """
).lstrip()


@pytest.mark.parametrize(
    "command, expected",
    [
        pytest.param(hello_full, HELLO_FULL_TABLE_EXPECTED, id="full"),
        pytest.param(hello_minimal, HELLO_MINIMAL_TABLE_EXPECTED, id="minimal"),
    ],
)
def test_style_table(command, expected):
    output = "\n".join(make_command_docs("hello", command, style="table"))
    assert output == expected


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
    expected = dedent(
        """
        # multi

        Multi help

        **Usage:**

        ```text
        multi [OPTIONS] COMMAND [ARGS]...
        ```

        **Options:**

        ```text
          --help  Show this message and exit.
        ```

        ## hello

        Hello, world!

        **Usage:**

        ```text
        multi hello [OPTIONS]
        ```

        **Options:**

        ```text
          -d, --debug TEXT  Include debug output
          --help            Show this message and exit.
        ```
        """
    ).lstrip()

    output = "\n".join(make_command_docs("multi", multi))
    assert output == expected


@pytest.mark.parametrize(
    "multi",
    [
        pytest.param(MultiCLI("multi", help="Multi help"), id="explicit-name"),
        pytest.param(MultiCLI(help="Multi help"), id="no-name"),
    ],
)
def test_custom_multicommand_with_list_subcommands(multi):
    """
    Custom `MultiCommand` objects are supported (i.e. not just `Group` multi-commands).
    """
    expected = dedent(
        """
        # multi

        Multi help

        **Usage:**

        ```text
        multi [OPTIONS] COMMAND [ARGS]...
        ```

        **Options:**

        ```text
          --help  Show this message and exit.
        ```

        **Subcommands**

        - *hello*: Hello, world!

        ## hello

        Hello, world!

        **Usage:**

        ```text
        multi hello [OPTIONS]
        ```

        **Options:**

        ```text
          -d, --debug TEXT  Include debug output
          --help            Show this message and exit.
        ```
        """
    ).lstrip()

    output = "\n".join(make_command_docs("multi", multi, list_subcommands=True))
    assert output == expected


@pytest.mark.parametrize("show_hidden", [True, False])
@pytest.mark.parametrize("style", ["plain", "table"])
def test_show_hidden_option(show_hidden, style):
    @click.command()
    @click.option("--hidden", hidden=True)
    def _test_cmd(hidden):
        """Test cmd."""

    output = "\n".join(make_command_docs("_test_cmd", _test_cmd, style=style, show_hidden=show_hidden))
    assert ("--hidden" in output) == show_hidden


@pytest.mark.parametrize("show_hidden", [True, False])
def test_show_hidden_command(show_hidden):
    @click.command(hidden=True)
    def _test_cmd():
        """Test cmd."""

    output = "\n".join(make_command_docs("_test_cmd", _test_cmd, show_hidden=show_hidden))
    assert (output != "") == show_hidden


@pytest.mark.parametrize("show_hidden", [True, False])
def test_show_hidden_group(show_hidden):
    @click.group(hidden=True)
    def _test_group():
        """Test group."""

    @_test_group.command(hidden=False)
    def _test_cmd():
        """Test cmd."""

    output = "\n".join(make_command_docs("_test_group", _test_group, show_hidden=show_hidden))
    assert (output != "") == show_hidden


def test_show_options():
    @click.command()
    @click.option("--hidden", hidden=True)
    @click.option("--normal", hidden=False)
    def _test_cmd(hidden, normal):
        """Test cmd."""

    ctx = click.Context(cast(click.Command, _test_cmd), info_name="_test_cmd")
    opt_hidden = cast(click.Option, ctx.command.params[0])
    opt_normal = cast(click.Option, ctx.command.params[1])

    assert opt_hidden.hidden
    assert not opt_normal.hidden

    with _show_options(ctx):
        assert not opt_hidden.hidden
        assert not opt_normal.hidden

    assert opt_hidden.hidden
    assert not opt_normal.hidden
