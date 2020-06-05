# (C) Datadog, Inc. 2020-present
# All rights reserved
# Licensed under the Apache license (see LICENSE)
import importlib
from typing import Any

import click
from ._exceptions import MkDocsClickException


def load_command(module: str, attribute: str) -> click.BaseCommand:
    """
    Load and return the Click command object located at '<module>:<attribute>'.
    """
    command = _load_obj(module, attribute)

    if not isinstance(command, click.BaseCommand):
        raise MkDocsClickException(f"{attribute!r} must be a 'click.BaseCommand' object, got {type(command)}")

    return command


def _load_obj(module: str, attribute: str) -> Any:
    try:
        mod = importlib.import_module(module)
    except SystemExit:
        raise MkDocsClickException("the module appeared to call sys.exit()")  # pragma: no cover

    try:
        return getattr(mod, attribute)
    except AttributeError:
        raise MkDocsClickException(f"Module {module!r} has no attribute {attribute!r}")
