# (C) Datadog, Inc. 2020-present
# All rights reserved
# Licensed under the Apache license (see LICENSE)
from mkdocs_click.extension import ClickProcessor


click_processor = ClickProcessor()


def test_no_options(generate_docs):
    data = """
# Some content
foo
::: mkdocs-click
bar
""".splitlines()

    expected = """
# Some content
foo
> mocked_data
bar""".splitlines()

    generate_docs.return_value = ["> mocked_data"]
    processed = click_processor.run(data)
    assert processed == expected


def test_options(generate_docs):
    data = """
# Some content
foo
::: mkdocs-click
    :option1: value1
    :optiøn2: value2
\t:option3:
    :option4:\x20
bar
""".splitlines()
    expected = """
# Some content
foo
{'option1': 'value1', 'optiøn2': 'value2', 'option3': '', 'option4': ''}
bar
""".splitlines()

    generate_docs.side_effect = lambda mapping: [str(mapping)]
    processed = click_processor.run(data)
    assert processed == expected


def test_do_not_affect_other_blocks(generate_docs):
    data = """
# Some content
::: mkdocs-click
::: plugin1
    :option1: value1
::: mkdocs-click
    :option: value
::: plugin2
    :option2: value2
bar
""".splitlines()

    expected = """
# Some content
::: plugin1
    :option1: value1
::: plugin2
    :option2: value2
bar
""".splitlines()

    generate_docs.side_effect = lambda _: []
    processed = click_processor.run(data)
    assert processed == expected  # no change
