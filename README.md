# mkdocs-click

![Tests](https://github.com/DataDog/mkdocs-click/workflows/Tests/badge.svg?branch=master)

An MkDocs extension to generate documentation for Click command line applications.

## Installation

This package is not available on PyPI yet, but you can install it from git:

```bash
pip install git+https://github.com/DataDog/mkdocs-click.git
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

If you are inserting documentation within other Markdown content, you can set the `:depth:` option to tweak the initial header level.

By default it is set to `0`, i.e. headers start at `<h1>`. If set to `1`, headers will start at `<h2>`, and so on.

## Reference

### Block syntax

The syntax for `mkdocs-click` blocks is the following:

```markdown
::: mkdocs-click
    :module: <MODULE>
    :command: <COMMAND>
    :depth: <DEPTH>
```

Options:

- `module`: path to the module where the command object is located.
- `command`: name of the command object.
- `depth`: _(Optional, default: `0`)_ Offset to add when generating headers.
