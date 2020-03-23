import re
from typing import List

from markdown import Markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

from mkdocs_click.parser import generate_command_docs


class ClickProcessor(Preprocessor):

    PATTERN_PLUGIN_IDENTIFIER = re.compile(r'^::: mkdocs-click')
    PATTERN_PLUGIN_OPTIONS = re.compile(r'^(?:\t|\s{4}):(.+):(\s\S+|\s*)$')

    def run(self, lines: List[str]) -> List[str]:
        new_lines = []
        in_block_section = False
        block_options = {}
        for i, line in enumerate(lines):
            if in_block_section:
                m = self.PATTERN_PLUGIN_OPTIONS.search(line)
                if m:
                    option_name, option_value = m.groups()
                    block_options[option_name] = option_value.strip()
                else:
                    # Reached end of block, generate documentation
                    new_lines.extend(generate_command_docs(block_options))
                    new_lines.append(line)
                    in_block_section = False
                continue

            m = self.PATTERN_PLUGIN_IDENTIFIER.search(line)
            if m:
                # Just found the plugin identifier, start a block
                in_block_section = True
                block_options = {}
            else:
                new_lines.append(line)

        return new_lines


class MKClickExtension(Extension):
    def extendMarkdown(self, md: Markdown) -> None:
        md.registerExtension(self)
        processor = ClickProcessor(md.parser)
        md.preprocessors.register(processor, "mk_click", 141)


def makeExtension() -> Extension:
    return MKClickExtension()
