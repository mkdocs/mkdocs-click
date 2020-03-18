from markdown import Markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

import xml.etree.ElementTree as etree
import re

class ClickProcessor(Preprocessor):

    PATTERN = re.compile(r'^:::click module=([:a-zA-Z0-9_.]+):([:a-zA-Z0-9_.]+)::: *$')
    
    def run(self, lines: [str]) -> [str]:
        new_lines = []
        for line in lines:
            m = self.PATTERN.search(line)
            if m:
                path, command = m.groups()
                new_lines.append("Found a command:")
                new_lines.append(f" - Path={path}")
                new_lines.append(f" - Command={command}")
            else:
                new_lines.append(line)

        return new_lines

class MKClickExtension(Extension):
    def extendMarkdown(self, md: Markdown) -> None:
        md.registerExtension(self)
        processor = ClickProcessor(md.parser)
        md.preprocessors.register(processor, "mk_clik", 141)

def makeExtension():
    return MKClickExtension()