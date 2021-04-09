import ast

import pytest

from pandas_dev_flaker.__main__ import Plugin


def results(s):
    return {"{}:{}: {}".format(*r) for r in Plugin(ast.parse(s)).run()}


@pytest.mark.parametrize(
    "source",
    (
        pytest.param(
            "import foo\n" "foo.filter('str')",
            id="non-builtin filter",
        ),
    ),
)
def test_noop(source):
    assert not results(source)


@pytest.mark.parametrize(
    "source, expected",
    (
        pytest.param(
            "filter('str')",
            "1:0: PDF004 builtin filter function used",
            id="builtin filter",
        ),
    ),
)
def test_violation(source, expected):
    (result,) = results(source)
    assert result == expected
