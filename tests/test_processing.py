# (C) Datadog, Inc. 2020-present
# All rights reserved
# Licensed under the Apache license (see LICENSE)
from mkdocs_click._processing import replace_blocks


def test_replace_options():
    """Replace a block with options."""

    source = """
# Some content
foo
::: target
    :option1: value1
    :optiøn2: value2
\t:option3:
    :option4:\x20
bar
""".strip()

    expected = """
# Some content
foo
{'option1': 'value1', 'optiøn2': 'value2', 'option3': '', 'option4': ''}
bar
""".strip()

    output = list(
        replace_blocks(
            source.splitlines(), title="target", replace=lambda **options: [str(options)]
        )
    )
    assert output == expected.splitlines()


def test_replace_no_options():
    """Replace a block that has no options."""

    source = """
# Some content
foo
::: target
bar
""".strip()

    expected = """
# Some content
foo
> mock
bar
""".strip()

    output = list(
        replace_blocks(source.splitlines(), title="target", replace=lambda **options: ["> mock"])
    )
    assert output == expected.splitlines()


def test_other_blocks_unchanged():
    """Blocks other than the target block are left unchanged."""

    source = """
# Some content
::: target
::: plugin1
    :option1: value1
::: target
    :option: value
::: plugin2
    :option2: value2
bar
""".strip()

    expected = """
# Some content
::: plugin1
    :option1: value1
::: plugin2
    :option2: value2
bar
""".strip()

    output = list(replace_blocks(source.splitlines(), title="target", replace=lambda **kwargs: []))
    assert output == expected.splitlines()
