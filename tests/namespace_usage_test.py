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
            "import pandas\n"
            "\n"
            "cat1 = pandas.Categorical()\n"
            "cat2 = pandas.Categorical()\n",
            id="Both accessed from pandas",
        ),
        pytest.param(
            "from pandas import Categorical\n"
            "\n"
            "cat1 = Categorical()\n"
            "cat2 = Categorical()\n",
            id="Both are imported from pandas",
        ),
    ),
)
def test_noop(source):
    assert not results(source)


@pytest.mark.parametrize(
    "source, expected",
    (
        pytest.param(
            "from pandas import Categorical\n"
            "import pandas as pd\n"
            "\n"
            "cat1 = Categorical()\n"
            "cat2 = pd.Categorical()\n",
            "5:7: PDF019 found both 'pd.Categorical' and 'Categorical' "
            "in the same file",
            id="One is accessed from pd, the other is imported from pandas",
        ),
        pytest.param(
            "import pandas\n"
            "from pandas import Categorical\n"
            "\n"
            "cat1 = Categorical()\n"
            "cat2 = pandas.Categorical()\n",
            "5:7: PDF019 found both 'pd.Categorical' and 'Categorical' "
            "in the same file",
            id="One accessed from pandas, the other imported from pandas",
        ),
    ),
)
def test_violation(source, expected):
    (result,) = results(source)
    assert result == expected
