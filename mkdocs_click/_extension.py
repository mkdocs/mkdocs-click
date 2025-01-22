# (C) Datadog, Inc. 2020-present
# All rights reserved
# Licensed under the Apache license (see LICENSE)
from __future__ import annotations

from typing import Any, Iterator

from markdown.extensions import Extension
from markdown.extensions.attr_list import AttrListExtension
from markdown.preprocessors import Preprocessor

from ._docs import make_command_docs
from ._exceptions import MkDocsClickException
from ._loader import load_command
from ._processing import replace_blocks


def replace_command_docs(has_attr_list: bool = False, **options: Any) -> Iterator[str]:
    for option in ("module", "command"):
        if option not in options:
            raise MkDocsClickException(f"Option {option!r} is required")

    module = options["module"]
    command = options["command"]
    prog_name = options.get("prog_name", None)
    depth = int(options.get("depth", 0))
    style = options.get("style", "plain")
    remove_ascii_art = options.get("remove_ascii_art", False)
    show_hidden = options.get("show_hidden", False)
    list_subcommands = options.get("list_subcommands", False)
    command_class = options.get("command_class", "click.BaseCommand")

    command_obj = load_command(module, command, command_class)

    prog_name = prog_name or command_obj.name or command

    return make_command_docs(
        prog_name=prog_name,
        command=command_obj,
        depth=depth,
        style=style,
        remove_ascii_art=remove_ascii_art,
        show_hidden=show_hidden,
        list_subcommands=list_subcommands,
        has_attr_list=has_attr_list,
    )


class ClickProcessor(Preprocessor):
    def __init__(self, md: Any) -> None:
        super().__init__(md)
        self._has_attr_list = any(
            isinstance(ext, AttrListExtension) for ext in md.registeredExtensions
        )

    def run(self, lines: list[str]) -> list[str]:
        return list(
            replace_blocks(
                lines,
                title="mkdocs-click",
                replace=lambda **options: replace_command_docs(
                    has_attr_list=self._has_attr_list, **options
                ),
            )
        )


class MKClickExtension(Extension):
    """
    Replace blocks like the following:

    ::: mkdocs-click
        :module: example.main
        :command: cli

    by Markdown documentation generated from the specified Click application.
    """

    def extendMarkdown(self, md: Any) -> None:
        md.registerExtension(self)
        processor = ClickProcessor(md)
        md.preprocessors.register(processor, "mk_click", 141)


def makeExtension() -> Extension:
    return MKClickExtension()
