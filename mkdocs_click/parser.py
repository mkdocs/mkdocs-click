import logging
import traceback

import click
from click import Command

from mkdocs_click.common import MKClickConfigException

logger = logging.getLogger(f"MARKDOWN.{__name__}")


def _load_command(module_path: str, module_name: str) -> click.BaseCommand:
    """Load the module."""
    # __import__ will fail on unicode,
    # so we ensure module path is a string here.
    module_path = str(module_path)
    module_name = str(module_name)

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


def _make_header(text: str, level: int) -> str:
    return f"{'#' * (level + 1)} {text}"


def _make_title(prog_name: str, level: int) -> [str]:
    return [_make_header(prog_name, level), ""]


def _make_description(ctx: click.Context) -> [str]:
    lines = []
    help_string = ctx.command.help or ctx.command.short_help
    if help_string:
        lines.extend([f"{l}" for l in help_string.splitlines()])
        lines.append("")

    return lines


def _make_usage(ctx: click.Context) -> [str]:
    formatter = ctx.make_formatter()
    pieces = ctx.command.collect_usage_pieces(ctx)
    formatter.write_usage(ctx.command_path, ' '.join(pieces), prefix='')
    usage = formatter.getvalue().rstrip('\n')

    full_path = []
    current = ctx
    while current is not None:
        full_path.append(current.command.name)
        current = current.parent

    full_path.reverse()

    return [
        "Usage:",
        "```",
        " ".join(full_path) + usage,
        "```"
    ]


def _make_options(ctx: click.Context) -> [str]:
    formatter = ctx.make_formatter()
    Command.format_options(ctx.command, ctx, formatter)
    # First line is redundant "Options"
    # Last line is `--help`
    option_lines = formatter.getvalue().splitlines()[1:-1]
    if not option_lines:
        return []

    return [
        "Options:",
        "```code",
        *option_lines,
        "```"
    ]


def _get_lazyload_commands(multicommand):
    commands = {}
    for command in multicommand.list_commands(multicommand):
        commands[command] = multicommand.get_command(multicommand, command)

    return commands


def _parse_recursively(prog_name: str, command: click.BaseCommand, parent: click.Context = None, level: int = 0) -> [str]:
    ctx = click.Context(command, parent=parent)
    lines = []
    lines.extend(_make_title(prog_name, level))
    lines.extend(_make_description(ctx))
    lines.extend(_make_usage(ctx))
    lines.extend(_make_options(ctx))

    # Get subcommands
    lookup = getattr(ctx.command, 'commands', {})
    if not lookup and isinstance(ctx.command, click.MultiCommand):
        lookup = _get_lazyload_commands(ctx.command)
    commands = sorted(lookup.values(), key=lambda item: item.name)

    for command in commands:
        lines.extend(_parse_recursively(command.name, command, parent=ctx, level=level+1))
    return [
        l.replace('\b', '') for l in lines
    ]


def generate_command_docs(path: str, command: str) -> [str]:
    click_command = _load_command(path, command)
    return _parse_recursively(command, click_command)

