# (C) Datadog, Inc. 2020-present
# All rights reserved
# Licensed under the Apache license (see LICENSE)
from typing import Iterator, List, Optional, cast, Iterable

import click

from ._exceptions import MkDocsClickException


def make_command_docs(prog_name: str, command: click.BaseCommand, level: int = 0) -> Iterator[str]:
    """Create the Markdown lines for a command and its sub-commands."""
    for line in _recursively_make_command_docs(prog_name, command, level=level):
        yield line.replace("\b", "")


def _recursively_make_command_docs(
    prog_name: str, command: click.BaseCommand, parent: click.Context = None, level: int = 0
) -> Iterator[str]:
    """Create the raw Markdown lines for a command and its sub-commands."""
    ctx = click.Context(cast(click.Command, command), parent=parent)

    yield from _make_title(prog_name, level)
    yield from _make_description(ctx)
    yield from _make_usage(ctx)
    yield from _make_options(ctx)

    subcommands = _get_sub_commands(ctx.command, ctx)

    for command in sorted(subcommands, key=lambda cmd: cmd.name):
        yield from _recursively_make_command_docs(command.name, command, parent=ctx, level=level + 1)


def _get_sub_commands(command: click.Command, ctx: click.Context) -> List[click.Command]:
    """Return subcommands of a Click command."""
    subcommands = getattr(command, "commands", {})
    if subcommands:
        return subcommands.values()

    if not isinstance(command, click.MultiCommand):
        return []

    subcommands = []

    for name in command.list_commands(ctx):
        subcommand = command.get_command(ctx, name)
        assert subcommand is not None
        subcommands.append(subcommand)

    return subcommands


def _make_title(prog_name: str, level: int) -> Iterator[str]:
    """Create the first markdown lines describing a command."""
    yield _make_header(prog_name, level)
    yield ""


def _make_header(text: str, level: int) -> str:
    """Create a markdown header at a given level"""
    return f"{'#' * (level + 1)} {text}"


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

    # Generate the full usage string based on parents if any, i.e. `root sub1 sub2 ...`.
    full_path = []
    current: Optional[click.Context] = ctx
    while current is not None:
        name = current.command.name
        if name is None:
            raise MkDocsClickException(f"command {current.command} has no `name`")
        full_path.append(name)
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

    def backquote(opts: Iterable[str]) -> List[str]:
        return [f"`{opt}`" for opt in opts]

    def format_possible_value(opt: click.Option) -> str:
        param_type = opt.type

        if isinstance(param_type, click.Choice):
            return f"{param_type.name.upper()} ({' &#x7C; '.join(backquote(param_type.choices))})"
        elif isinstance(param_type, click.DateTime):
            return f"{param_type.name.upper()} ({' &#x7C; '.join(backquote(param_type.formats))})"
        elif isinstance(param_type, (click.IntRange, click.FloatRange)):
            if param_type.min is not None and param_type.max is not None:
                return f"{param_type.name.upper()} (between `{param_type.min}` and `{param_type.max}`)"
            elif param_type.min is not None:
                return f"{param_type.name.upper()} (`{param_type.min}` and above)"
            else:
                return f"{param_type.name.upper()} (`{param_type.max}` and below)"
        else:
            return param_type.name.upper()

    params = [param for param in ctx.command.get_params(ctx) if isinstance(param, click.Option)]

    if params[0].opts[0] == "--help":
        return

    yield "**Options:**"
    yield ""
    yield "| Option | Type | Description | Required | Default |"
    yield "| ------ | ---- | ----------- | -------- | ------- |"
    for param in params[:-1]:
        options = f"{', '.join(backquote(param.opts))}{'/{}'.format(', '.join(backquote(param.secondary_opts))) if param.secondary_opts != [] else ''}"  # noqa: E501
        value_type = format_possible_value(param)
        description = param.help if param.help is not None else "No description given"
        required = "&#x2714;" if param.required else ""
        default = f"`{param.default}`" if param.default is not None else ""
        yield f"| {options} | {value_type} | {description} | {required} | {default} |"
    yield ""
