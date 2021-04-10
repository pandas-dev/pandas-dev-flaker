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
            "from collections import abc",
            id="Imported abc from collections",
        ),
    ),
)
def test_noop(source):
    assert not results(source)


@pytest.mark.parametrize(
    "source, expected",
    (
        pytest.param(
            "from collections.abc import Generator",
            "1:0: PDF001 import from collections.abc "
            "(use 'from collections import abc' instead)",
            id="Imported from collections.abc",
        ),
        pytest.param(
            "import collections.abc",
            "1:0: PDF001 import from collections.abc "
            "(use 'from collections import abc' instead)",
            id="Imported collections.abc",
        ),
    ),
)
def test_violation(source, expected):
    (result,) = results(source)
    assert result == expected
