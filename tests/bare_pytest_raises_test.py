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
            "from foo import raises\n" "with foo.raises(ValueError): pass",
            id="raises import not from pytest",
        ),
        pytest.param(
            "import foo\n" "with foo.raises(ValueError): pass",
            id="raises accessed not from pytest",
        ),
        pytest.param(
            "from pytest import raises\n"
            "with raises(ValueError, match=None): pass",
            id="match=None, imported from pytest",
        ),
        pytest.param(
            "import pytest\n"
            "with pytest.raises(ValueError, match=None): pass",
            id="match=None, pytest.raises",
        ),
    ),
)
def test_noop(source):
    assert not results(source)


@pytest.mark.parametrize(
    "source, expected",
    (
        pytest.param(
            "from pytest import raises\n"
            "with raises(ValueError, qux=None): pass",
            "2:5: PDF009 'pytest.raises' used without 'match='",
            id="from pytest import raises, differenet kwarg",
        ),
        pytest.param(
            "from pytest import raises\n" "with raises(ValueError): pass",
            "2:5: PDF009 'pytest.raises' used without 'match='",
            id="from pytest import raises, no match",
        ),
        pytest.param(
            "import pytest\n"
            "with pytest.raises(ValueError, bar='qux'): pass",
            "2:5: PDF009 'pytest.raises' used without 'match='",
            id="pytest.raises, different keyword argument passed",
        ),
        pytest.param(
            "import pytest\n" "with pytest.raises(ValueError): pass",
            "2:5: PDF009 'pytest.raises' used without 'match='",
            id="pytest.raises, not match",
        ),
    ),
)
def test_violation(source, expected):
    (result,) = results(source)
    assert result == expected
