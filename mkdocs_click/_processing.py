# (C) Datadog, Inc. 2020-present
# All rights reserved
# Licensed under the Apache license (see LICENSE)
import re
from typing import Callable, Iterable, Iterator


def replace_blocks(lines: Iterable[str], title: str, replace: Callable[..., Iterable[str]]) -> Iterator[str]:
    """
    Find blocks of lines in the form of:

    ::: <title>
        :<key1>: <value>
        :<key2>:
        ...

    And replace them with the lines returned by `replace(key1="<value1>", key2="", ...)`.
    """

    options = {}
    in_block_section = False

    for line in lines:
        if in_block_section:
            match = re.search(r"^\s+:(?P<key>.+):(?:\s+(?P<value>\S+))?", line)
            if match is not None:
                # New ':key:' or ':key: value' line, ingest it.
                key = match.group("key")
                value = match.group("value") or ""
                options[key] = value
                continue

            # Block is finished, flush it.
            in_block_section = False
            yield from replace(**options)
            yield line
            continue

        match = re.search(rf"^::: {title}", line)
        if match is not None:
            # Block header, ingest it.
            in_block_section = True
            options = {}
        else:
            yield line
