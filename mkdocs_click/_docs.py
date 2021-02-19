# (C) Datadog, Inc. 2020-present
# All rights reserved
# Licensed under the Apache license (see LICENSE)
from typing import Iterator, List, cast

import click
from markdown.extensions.toc import slugify

from ._exceptions import MkDocsClickException


def make_command_docs(
    prog_name: str,
    command: click.BaseCommand,
    depth: int = 0,
    style: str = "plain",
    has_attr_list: bool = False,
) -> Iterator[str]:
    """Create the Markdown lines for a command and its sub-commands."""
    for line in _recursively_make_command_docs(
        prog_name, command, depth=depth, style=style, has_attr_list=has_attr_list
    ):
        yield line.replace("\b", "")


def _recursively_make_command_docs(
    prog_name: str,
    command: click.BaseCommand,
    parent: click.Context = None,
    depth: int = 0,
    style: str = "plain",
    has_attr_list: bool = False,
) -> Iterator[str]:
    """Create the raw Markdown lines for a command and its sub-commands."""
    ctx = click.Context(cast(click.Command, command), info_name=prog_name, parent=parent)

    yield from _make_title(ctx, depth, has_attr_list=has_attr_list)
    yield from _make_description(ctx)
    yield from _make_usage(ctx)
    yield from _make_options(ctx, style)

    subcommands = _get_sub_commands(ctx.command, ctx)

    for command in sorted(subcommands, key=lambda cmd: cmd.name):
        yield from _recursively_make_command_docs(
            command.name, command, parent=ctx, depth=depth + 1, style=style, has_attr_list=has_attr_list
        )


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


def _make_title(ctx: click.Context, depth: int, *, has_attr_list: bool) -> Iterator[str]:
    """Create the Markdown heading for a command."""
    if has_attr_list:
        yield from _make_title_full_command_path(ctx, depth)
    else:
        yield from _make_title_basic(ctx, depth)


def _make_title_basic(ctx: click.Context, depth: int) -> Iterator[str]:
    """Create a basic Markdown heading for a command."""
    yield f"{'#' * (depth + 1)} {ctx.info_name}"
    yield ""


def _make_title_full_command_path(ctx: click.Context, depth: int) -> Iterator[str]:
    """Create the markdown heading for a command, showing the full command path.

    This style accomodates nested commands by showing:
    * The full command path for headers and permalinks (eg `# git commit` and `http://localhost:8000/#git-commit`)
    * The command leaf name only for TOC entries (eg `* commit`).

    We do this because a TOC naturally conveys the hierarchy, whereas headings and permalinks should be namespaced to
    convey the hierarchy.

    See: https://github.com/DataDog/mkdocs-click/issues/35
    """
    text = ctx.command_path  # 'git commit'
    permalink = slugify(ctx.command_path, "-")  # 'git-commit'
    toc_label = ctx.info_name  # 'commit'

    # Requires `attr_list` extension, see: https://python-markdown.github.io/extensions/toc/#custom-labels
    attributes = f"#{permalink} data-toc-label='{toc_label}'"

    yield f"{'#' * (depth + 1)} {text} {{ {attributes} }}"
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

    yield "**Usage:**"
    yield ""
    yield "```"
    yield usage
    yield "```"
    yield ""


def _make_options(ctx: click.Context, style: str = "plain") -> Iterator[str]:
    """Create the Markdown lines describing the options for the command."""

    if style == "plain":
        return _make_plain_options(ctx)
    elif style == "table":
        return _make_table_options(ctx)
    else:
        raise MkDocsClickException(f"{style} is not a valid option style, which must be either `plain` or `table`.")


def _make_plain_options(ctx: click.Context) -> Iterator[str]:
    """Create the plain style options description."""
    formatter = ctx.make_formatter()
    click.Command.format_options(ctx.command, ctx, formatter)

    option_lines = formatter.getvalue().splitlines()

    # First line is redundant "Options"
    option_lines = option_lines[1:]

    if not option_lines:  # pragma: no cover
        # We expect at least `--help` to be present.
        raise RuntimeError("Expected at least one option")

    yield "**Options:**"
    yield ""
    yield "```"
    yield from option_lines
    yield "```"
    yield ""


# Unicode "Vertical Line" character (U+007C), HTML-compatible.
# "\|" (escaped pipe) would work, too, but linters don't like it in literals.
# https://stackoverflow.com/questions/23723396/how-to-show-the-pipe-symbol-in-markdown-table
_HTML_PIPE = "&#x7C;"


def _format_table_option_type(option: click.Option) -> str:
    typename = option.type.name

    # TODO: remove "# type: ignore" comments once https://github.com/python/typeshed/pull/4813 gets merged and released.

    if isinstance(option.type, click.Choice):
        # @click.option(..., type=click.Choice(["A", "B", "C"]))
        # -> choices (`A` | `B` | `C`)
        choices = f" {_HTML_PIPE} ".join(f"`{choice}`" for choice in option.type.choices)
        return f"{typename} ({choices})"

    if isinstance(option.type, click.DateTime):
        # @click.option(..., type=click.DateTime(["A", "B", "C"]))
        # -> datetime (`%Y-%m-%d` | `%Y-%m-%dT%H:%M:%S` | `%Y-%m-%d %H:%M:%S`)
        formats = f" {_HTML_PIPE} ".join(f"`{fmt}`" for fmt in option.type.formats)  # type: ignore[attr-defined]
        return f"{typename} ({formats})"

    if isinstance(option.type, (click.IntRange, click.FloatRange)):
        if option.type.min is not None and option.type.max is not None:  # type: ignore[union-attr]
            # @click.option(..., type=click.IntRange(min=0, max=10))
            # -> integer range (between `0` and `10`)
            return f"{typename} (between `{option.type.min}` and `{option.type.max}`)"  # type: ignore[union-attr]
        elif option.type.min is not None:  # type: ignore[union-attr]
            # @click.option(..., type=click.IntRange(min=0))
            # -> integer range (`0` and above)
            return f"{typename} (`{option.type.min}` and above)"  # type: ignore[union-attr]
        else:
            # @click.option(..., type=click.IntRange(max=10))
            # -> integer range (`10` and below)
            return f"{typename} (`{option.type.max}` and below)"  # type: ignore[union-attr]

    # -> "boolean", "text", etc.
    return typename


def _format_table_option_row(option: click.Option) -> str:
    # Example: @click.option("-V, --version/--show-version", is_flag=True, help="Show version info.")

    # -> "`-V`, `--version`"
    names = ", ".join(f"`{opt}`" for opt in option.opts)

    if option.secondary_opts:
        # -> "`-V`, `--version` / `--show-info`"
        names += " / "
        names += ", ".join(f"`{opt}`" for opt in option.secondary_opts)

    # -> "boolean"
    value_type = _format_table_option_type(option)

    # -> "Show version info."
    description = option.help if option.help is not None else "N/A"

    # -> `False`
    default = f"`{option.default}`" if option.default is not None else "_required_"

    # -> "| `-V`, `--version` / `--show-version` | boolean | Show version info. | `False` |"
    return f"| {names} | {value_type} | {description} | {default} |"


def _make_table_options(ctx: click.Context) -> Iterator[str]:
    """Create the table style options description."""

    options = [param for param in ctx.command.get_params(ctx) if isinstance(param, click.Option)]
    option_rows = [_format_table_option_row(option) for option in options]

    yield "**Options:**"
    yield ""
    yield "| Name | Type | Description | Default |"
    yield "| ---- | ---- | ----------- | ------- |"
    yield from option_rows
    yield ""
