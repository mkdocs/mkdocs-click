# (C) Datadog, Inc. 2020-present
# All rights reserved
# Licensed under the Apache license (see LICENSE)
import click

NOT_A_COMMAND = "not-a-command"


@click.command()
@click.option("--count", default=1, help="Number of greetings.")
@click.option("--name", prompt="Your name", help="The person to greet.")
@click.option("--hidden", hidden=True)
def hello(count, name, hidden):
    """Simple program that greets NAME for a total of COUNT times."""


@click.group()
def cli():
    """Main entrypoint for this dummy program"""


@click.group(name="cli")
def cli_named():
    """Main entrypoint for this dummy program"""


@click.command()
def foo():  # No description
    pass  # pragma: no cover


@click.group()
def bar():
    """The bar command"""


@click.command(hidden=True)
def hidden():
    """The hidden command"""


bar.add_command(hello)

cli.add_command(foo)
cli.add_command(bar)
cli.add_command(hidden)

cli_named.add_command(foo)
cli_named.add_command(bar)
cli_named.add_command(hidden)


class MultiCLI(click.MultiCommand):
    def list_commands(self, ctx):
        return ["foo", "bar"]

    def get_command(self, ctx, name):
        cmds = {"foo": foo, "bar": bar}
        return cmds.get(name)


multi_named = MultiCLI(name="multi", help="Main entrypoint for this dummy program")
multi = MultiCLI(help="Main entrypoint for this dummy program")
