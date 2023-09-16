# Contributing guidelines

Thank you for being interested in contributing to this project! Here's how to get started.

## Setup

To start developing on this project, create a fork of this repository on GitHub, then clone your fork on your machine:

```bash
git clone https://github.com/<USERNAME>/mkdocs-click
cd mkdocs-click
```

## Example docs site

You can run the example docs site that lives in `example/` locally using:

```bash
hatch run test:mkdocs serve -f example/mkdocs.yml
```

## Testing and linting

You can run the test suite using:

```bash
hatch run test:test
```

You can run code auto-formatting and style checks using:

```bash
hatch run style:fix
```

## Releasing

_This section is for maintainers._

Before releasing a new version, create a pull request with:

- An update to the changelog.
- A version bump: see `__version__.py`.

Merge the release PR, then create a release on GitHub. A tag will be created which will trigger a GitHub action to publish the new release to PyPI.
