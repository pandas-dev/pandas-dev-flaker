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
            "from foo import bar\n" "bar._qux",
            id="Class private attributes are allowed",
        ),
        pytest.param(
            "from foo import Bar\n" "Bar._qux",
            id="Class private attributes are allowed",
        ),
        pytest.param(
            "from foo import bar\n" "bar.__qux__",
            id="Dunder methods are allowed",
        ),
        pytest.param(
            "import sys\n" "sys._getframe",
            id="allowlisted attribute",
        ),
    ),
)
def test_noop(source):
    assert not results(source)


@pytest.mark.parametrize(
    "source, expected",
    (
        pytest.param(
            "from foo import bar\n" "bar._qux()",
            "2:0: PDF016 found private import across modules",
            id="warns used, imported from pytest",
        ),
    ),
)
def test_violation(source, expected):
    (result,) = results(source)
    assert result == expected
