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
            "import numpy as np\nnp.tester",
            id="tester instead of testing",
        ),
    ),
)
def test_noop(source):
    assert not results(source)


@pytest.mark.parametrize(
    "source, expected",
    (
        pytest.param(
            "import numpy\nnumpy.testing",
            "2:0: PDF025 found 'np.testing' or 'np.array_equal' "
            "(use 'pandas._testing' instead)",
            id="access from numpy",
        ),
        pytest.param(
            "import numpy as np\nnp.testing",
            "2:0: PDF025 found 'np.testing' or 'np.array_equal' "
            "(use 'pandas._testing' instead)",
            id="access from np",
        ),
        pytest.param(
            "import numpy as np\n"
            "np.testing.assert_array_equal(result, expected)",
            "2:0: PDF025 found 'np.testing' or 'np.array_equal' "
            "(use 'pandas._testing' instead)",
            id="np.testing.assert_array_equal",
        ),
        pytest.param(
            "from numpy import testing",
            "1:0: PDF025 found 'np.testing' or 'np.array_equal' "
            "(use 'pandas._testing' instead)",
            id="import from numpy",
        ),
        pytest.param(
            "from numpy.testing import assert_array_equal",
            "1:0: PDF025 found 'np.testing' or 'np.array_equal' "
            "(use 'pandas._testing' instead)",
            id="import from numpy",
        ),
        pytest.param(
            "from numpy import array_equal",
            "1:0: PDF025 found 'np.testing' or 'np.array_equal' "
            "(use 'pandas._testing' instead)",
            id="array_equal",
        ),
    ),
)
def test_violation(source, expected):
    (result,) = results(source)
    assert result == expected
