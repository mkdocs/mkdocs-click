# (C) Datadog, Inc. 2020-present
# All rights reserved
# Licensed under the Apache license (see LICENSE)
"""
Inspired by the click plugin for Sphinx, see: https://github.com/click-contrib/sphinx-click

This module contains all the required functions to parse a Click command recursively.
"""
import logging
import traceback
from typing import cast, Dict, List, Optional, Iterator

import click

logger = logging.getLogger(f"MARKDOWN.{__name__}")


class MKClickConfigException(Exception):
    pass


def _load_command(module_path: str, module_name: str) -> click.BaseCommand:
    """Load a module at a given path."""
    logger.info(f"Loading module {module_path}:{module_name}")
    try:
        mod = __import__(module_path, globals(), locals(), [module_name])
    except (Exception, SystemExit) as exc:
        err_msg = f"Failed to import '{module_name}' from '{module_path}'. "
        if isinstance(exc, SystemExit):
            err_msg += "The module appeared to call sys.exit()"
        else:
            err_msg += f"The following exception was raised:\n{traceback.format_exc()}"

        raise MKClickConfigException(err_msg)

    if not hasattr(mod, module_name):
        raise MKClickConfigException(f"Module '{module_path}' has no attribute '{module_name}'")

    parser = getattr(mod, module_name)

    if not isinstance(parser, click.BaseCommand):
        raise MKClickConfigException(
            f"'{module_path}' of type '{type(parser)}' is not derived from 'click.BaseCommand'"
        )
    return parser


def _get_lazyload_commands(multicommand: click.MultiCommand, ctx: click.Context) -> Dict[str, click.Command]:
    """Obtain click.Command references to the subcommands of a given command."""
    commands = {}

    for name in multicommand.list_commands(ctx):
        command = multicommand.get_command(ctx, name)
        assert command is not None
        commands[name] = command

    return commands


def _make_header(text: str, level: int) -> str:
    """Create a markdown header at a given level"""
    return f"{'#' * (level + 1)} {text}"


def _make_title(prog_name: str, level: int) -> Iterator[str]:
    """Create the first markdown lines describing a command."""
    yield _make_header(prog_name, level)
    yield ""


def _make_description(ctx: click.Context) -> Iterator[str]:
    """Create markdown lines based on the command's own description."""
    help_string = ctx.command.help or ctx.command.short_help

    if help_string:
        yield from help_string.splitlines()
        yield ""


def _make_usage(ctx: click.Context) -> Iterator[str]:
    """Create the Markdown lines from the command usage string."""

    # Gets the usual 'Usage' string without the prefix.
    formatter = ctx.make_formatter()
    pieces = ctx.command.collect_usage_pieces(ctx)
    formatter.write_usage(ctx.command_path, " ".join(pieces), prefix="")
    usage = formatter.getvalue().rstrip("\n")

    # Generate the full usage string based on parents if any i.e. `ddev meta snmp ...`
    full_path = []
    current: Optional[click.Context] = ctx
    while current is not None:
        full_path.append(current.command.name)
        current = current.parent

    full_path.reverse()
    usage_snippet = " ".join(full_path) + usage

    yield "Usage:"
    yield ""
    yield "```"
    yield usage_snippet
    yield "```"
    yield ""


def _make_options(ctx: click.Context) -> Iterator[str]:
    """Create the Markdown lines describing the options for the command."""
    formatter = ctx.make_formatter()
    click.Command.format_options(ctx.command, ctx, formatter)
    # First line is redundant "Options"
    # Last line is `--help`
    option_lines = formatter.getvalue().splitlines()[1:-1]
    if not option_lines:
        return

    yield "Options:"
    yield ""
    yield "```code"
    yield from option_lines
    yield "```"
    yield ""


def _parse_recursively(
    prog_name: str, command: click.BaseCommand, parent: click.Context = None, level: int = 0
) -> Iterator[str]:
    ctx = click.Context(cast(click.Command, command), parent=parent)

    yield from _make_title(prog_name, level)
    yield from _make_description(ctx)
    yield from _make_usage(ctx)
    yield from _make_options(ctx)

    # Get subcommands
    lookup = getattr(ctx.command, "commands", {})
    if not lookup and isinstance(ctx.command, click.MultiCommand):
        lookup = _get_lazyload_commands(ctx.command, ctx)
    commands = sorted(lookup.values(), key=lambda item: item.name)

    for command in commands:
        yield from _parse_recursively(command.name, command, parent=ctx, level=level + 1)


def _make_command_docs(prog_name: str, command: click.BaseCommand, level: int = 0) -> Iterator[str]:
    for line in _parse_recursively(prog_name, command, level=level):
        yield line.replace("\b", "")


def generate_command_docs(block_options: Dict[str, str]) -> List[str]:
    """Entry point for generating Markdown doumentation for a given command."""

    required_options = ("module", "command")
    for option in required_options:
        if option not in block_options:
            raise MKClickConfigException(
                "Parameter {} is required for mkdocs-click. Provided configuration was {}".format(option, block_options)
            )

    module_path = block_options["module"]
    command = block_options["command"]
    depth = int(block_options.get("depth", 0))
    command_obj = _load_command(module_path, command)

    return list(_make_command_docs(command, command_obj, level=depth))
