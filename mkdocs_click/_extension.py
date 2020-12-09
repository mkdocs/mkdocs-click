# (C) Datadog, Inc. 2020-present
# All rights reserved
# Licensed under the Apache license (see LICENSE)
from typing import Any, List, Iterator

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

from ._docs import make_command_docs
from ._exceptions import MkDocsClickException
from ._loader import load_command
from ._processing import replace_blocks


def replace_command_docs(**options: Any) -> Iterator[str]:
    for option in ("module", "command"):
        if option not in options:
            raise MkDocsClickException(f"Option {option!r} is required")

    module = options["module"]
    command = options["command"]
    depth = int(options.get("depth", 0))

    command_obj = load_command(module, command)

    return make_command_docs(prog_name=command, command=command_obj, level=depth)


class ClickProcessor(Preprocessor):
    def run(self, lines: List[str]) -> List[str]:
        return list(replace_blocks(lines, title="mkdocs-click", replace=replace_command_docs))


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
        processor = ClickProcessor(md.parser)
        md.preprocessors.register(processor, "mk_click", 141)


def makeExtension() -> Extension:
    return MKClickExtension()
