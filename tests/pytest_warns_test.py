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
            "import pytest\n" "warns = 'foo'",
            id="assignment to 'warns'",
        ),
    ),
)
def test_noop(source):
    assert not results(source)


@pytest.mark.parametrize(
    "source, expected",
    (
        pytest.param(
            "from pytest import warns\n",
            "1:0: PDF007 found pytest.warns "
            "(use pandas._testing.assert_produces_warning instead)",
            id="warns used, imported from pytest",
        ),
        pytest.param(
            "import pytest\n" "with pytest.warns(): pass",
            "2:5: PDF007 found pytest.warns "
            "(use pandas._testing.assert_produces_warning instead)",
            id="pytest.warns used",
        ),
    ),
)
def test_violation(source, expected):
    (result,) = results(source)
    assert result == expected
