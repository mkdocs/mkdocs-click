# mkdocs-click

An MkDocs extension to generate documentation for Click command line applications.

## Installation

This package is not available on PyPI yet, but you can install it from git:

```bash
pip install git+https://github.com/DataDog/mkdocs-click.git
```

## Quickstart

Register the extension in your `mkdocs.yml` configuration:

```yaml
# mkdocs.yml
markdown_extensions:
    - mkdocs-click
```

To document a given Click command, add this in the body of a Markdown file:

```markdown
:::click module=<MODULE_PATH>:<COMMAND>:::
```

Be sure to replace `<MODULE_PATH>` and `<COMMAND>` as appropriate.

Example:

```markdown
:::click module=app.cli:build:::
```
