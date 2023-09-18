# mkdocs-click

![Tests](https://github.com/mkdocs/mkdocs-click/workflows/CI/badge.svg?branch=master)
![Python versions](https://img.shields.io/pypi/pyversions/mkdocs-click.svg)
[![PyPI](https://img.shields.io/pypi/v/mkdocs-click)](https://pypi.org/project/mkdocs-click/)

An MkDocs extension to generate documentation for Click command line applications.

## Installation

Install from PyPI:

```bash
pip install mkdocs-click
```

## Quickstart

Add `mkdocs-click` to Markdown extensions in your `mkdocs.yml` configuration:

```yaml
site_name: Example
theme: readthedocs

markdown_extensions:
    - mkdocs-click
```

Add a CLI application, e.g.:

```python
# app/cli.py
import click

@click.group()
def cli():
    """Main entrypoint."""

@cli.command()
@click.option("-d", "--debug", help="Include debug output.")
def build(debug):
    """Build production assets."""
```

Add a `mkdocs-click` block in your Markdown:

```markdown
# CLI Reference

This page provides documentation for our command line tools.

::: mkdocs-click
    :module: app.cli
    :command: cli
```

Start the docs server:

```bash
mkdocs serve
```

Tada! 💫

![](https://raw.githubusercontent.com/DataDog/mkdocs-click/master/docs/example.png)

## Usage

### Documenting commands

To add documentation for a command, add a `mkdocs-click` block where the documentation should be inserted.

Example:

```markdown
::: mkdocs-click
    :module: app.cli
    :command: main
```

For all available options, see the [Block syntax](#block-syntax).

### Multi-command support

When pointed at a group (or any other multi-command), `mkdocs-click` will also generate documentation for sub-commands.

This allows you to generate documentation for an entire CLI application by pointing `mkdocs-click` at the root command.

### Tweaking header levels

By default, `mkdocs-click` generates Markdown headers starting at `<h1>` for the root command section. This is generally what you want when the documentation should fill the entire page.

If you are inserting documentation within other Markdown content, you can set the `:depth:` option to tweak the initial header level. Note that this applies even if you are just adding a heading.

By default it is set to `0`, i.e. headers start at `<h1>`. If set to `1`, headers will start at `<h2>`, and so on. Note that if you insert your own first level heading and leave depth at its default value of 0, the page will have multiple `<h1>` tags, which is not compatible with themes that generate page-internal menus such as the ReadTheDocs and mkdocs-material themes.

### Full command path headers

By default, `mkdocs-click` outputs headers that contain the command name. For nested commands such as `$ cli build all`, this also means the heading would be `## all`. This might be surprising, and may be harder to navigate at a glance for highly nested CLI apps.

If you'd like to show the full command path instead, turn on the [Attribute Lists extension](https://python-markdown.github.io/extensions/attr_list/):

```yaml
# mkdocs.yaml

markdown_extensions:
    - attr_list
    - mkdocs-click
```

`mkdocs-click` will then output the full command path in headers (e.g. `## cli build all`) and permalinks (e.g. `#cli-build-all`).

Note that the table of content (TOC) will still use the command name: the TOC is naturally hierarchal, so full command paths would be redundant. (This exception is why the `attr_list` extension is required.)

## Reference

### Block syntax

The syntax for `mkdocs-click` blocks is the following:

```markdown
::: mkdocs-click
    :module: <MODULE>
    :command: <COMMAND>
    :prog_name: <PROG_NAME>
    :depth: <DEPTH>
    :style: <STYLE>
```

Options:

- `module`: Path to the module where the command object is located.
- `command`: Name of the command object.
- `prog_name`: _(Optional, default: same as `command`)_ The name to display for the command.
- `depth`: _(Optional, default: `0`)_ Offset to add when generating headers.
- `style`: _(Optional, default: `plain`)_ Style for the options section. The possible choices are `plain` and `table`.
- `remove_ascii_art`: _(Optional, default: `False`)_ When docstrings begin with the escape character `\b`, all text will be ignored until the next blank line is encountered.
- `show_hidden`: _(Optional, default: `False`)_ Show commands and options that are marked as hidden.
- `list_subcommands`: _(Optional, default: `False`)_ List subcommands of a given command. If _attr_list_ is installed,
add links to subcommands also.
