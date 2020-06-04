# (C) Datadog, Inc. 2020-present
# All rights reserved
# Licensed under the Apache license (see LICENSE)
import click


@click.command()
@click.option("--count", default=1, help="Number of greetings.")
@click.option("--name", prompt="Your name", help="The person to greet.")
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo("Hello %s!" % name)


@click.group()
def cli():
    """Main entrypoint for this dummy program"""
    pass


@click.command()
def foo():
    """The foo command"""
    pass


@click.group()
def bar():
    """The bar command"""
    pass


bar.add_command(hello)
cli.add_command(foo)
cli.add_command(bar)
