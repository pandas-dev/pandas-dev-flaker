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
            "foo = f'{3:2f}'",
            id="!r in string",
        ),
        pytest.param(
            "def bar():\n" "    foo = '!r'\n" "    global foo, foo",
            id="!r in string",
        ),
        pytest.param(
            "foo = '!r'",
            id="!r in string",
        ),
    ),
)
def test_noop(source):
    assert not results(source)


@pytest.mark.parametrize(
    "source, expected",
    (
        pytest.param(
            "foo = f'{3!r}'",
            "1:6: PDF014 Found '{foo!r}' formatted value "
            "(instead, use 'repr(foo)')",
            id="!r used as formatter",
        ),
    ),
)
def test_violation(source, expected):
    (result,) = results(source)
    assert result == expected
