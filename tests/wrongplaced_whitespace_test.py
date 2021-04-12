import ast
import tokenize
from io import StringIO

import pytest

from pandas_dev_flaker.__main__ import run


def results(s):
    return {
        "{}:{}: {}".format(*r)
        for r in run(
            ast.parse(s),
            list(tokenize.generate_tokens(StringIO(s).readline)),
        )
    }


@pytest.mark.parametrize(
    "source",
    (
        pytest.param(
            "foo = (\n    'bar '\n    'qux '\n    )\n",
            id="Whitespace at end",
        ),
        pytest.param(
            "foo = (\n    'bar \\n'\n    ' qux '\n    )\n",
            id="Trailing newline",
        ),
    ),
)
def test_noop(source):
    assert not results(source)


@pytest.mark.parametrize(
    "source, expected",
    (
        pytest.param(
            "foo = (\n    'bar'\n    ' qux'\n    )\n",
            "3:4: PDF005 leading space in concatenated strings",
            id="Whitespace at start",
        ),
    ),
)
def test_violation(source, expected):
    (result,) = results(source)
    assert result == expected
