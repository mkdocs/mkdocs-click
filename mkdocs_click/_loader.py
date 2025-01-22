# (C) Datadog, Inc. 2020-present
# All rights reserved
# Licensed under the Apache license (see LICENSE)
from __future__ import annotations

import importlib
from typing import Any

from ._exceptions import MkDocsClickException


def load_command(module: str, attribute: str, command_class: str = "click.BaseCommand") -> Any:
    """
    Load and return the Click command object located at '<module>:<attribute>'.
    """
    command = _load_obj(module, attribute)

    if not isinstance(command, _load_command_class(command_class)):
        raise MkDocsClickException(
            f"{attribute!r} must be a '{command_class}' object, got {type(command)}"
        )

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


def _load_command_class(command_class: str) -> Any:
    module, attribute = command_class.rsplit(".", 1)
    try:
        return _load_obj(module, attribute)
    except ModuleNotFoundError:
        raise MkDocsClickException(f"Could not import {module!r}")
