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
            "from collections.abc.Generator import foo",
            "1:0: PDF001 found import from collections.abc "
            "(use 'from collections import abc')",
            id="3rd level 'from' import",
        ),
        pytest.param(
            "from collections.abc import Generator",
            "1:0: PDF001 found import from collections.abc "
            "(use 'from collections import abc')",
            id="2nd level 'from' import",
        ),
        pytest.param(
            "import collections.abc.Generator",
            "1:0: PDF001 found import from collections.abc "
            "(use 'from collections import abc')",
            id="3rd level import",
        ),
        pytest.param(
            "import collections.abc",
            "1:0: PDF001 found import from collections.abc "
            "(use 'from collections import abc')",
            id="2nd level import",
        ),
    ),
)
def test_violation(source, expected):
    (result,) = results(source)
    assert result == expected
