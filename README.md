# mkdocs-ext-click
Extensions for mkdocs to read and parse click commands.

## Usage

Install the extension from the repo. At the moment there is no version of it on PyPI.

```bash
git clone https://github.com/DataDog/mkdocs-click.git
cd mkdocs-click
pip install .
```

If you use tox or a dynamic environment, you can add the following line to your requirements:
```bash
git+https://github.com/DataDog/mkdocs-click.git
```

Adds this to the `markdown_extensions` in your mkdocs.yml file:

```yaml
markdown_extensions:
    - mkdocs-click
```

And finally to document a given click method, add this to any of your markdown file:

```markdown
:::click module=<MODULE_PATH>:<CLICK_FUNCTION>:::
```

replacing `<MODULE_PATH>` and `<CLICK_METHOD>` as needed.