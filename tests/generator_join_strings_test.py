"""
Based on

https://github.com/asottile/pyupgrade/blob/5fb168667ae73f157dd579344708e1cdfb0c0341/pyupgrade/_plugins/generator_expressions_pep289.py
"""

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
            "''.join([str(i) for i in range(5)])",
            id="String join() with list comprehension",
        ),
        pytest.param(
            "''.join([\n"
            "        str(i) for i in range(5)\n"
            "        ]\n"
            ")\n",
            id="String join() with multiline list comprehension",
        ),
    ),
)
def test_list_comprehensions(source):
    assert not results(source)


@pytest.mark.parametrize(
    "source, expected",
    (
        pytest.param(
            "''.join(str(i) for i in range(5))",
            "1:0: PDF024 found string join() with generator expressions",
            id="String join() with generator expression",
        ),
        pytest.param(
            "''.join((str(i) for i in range(5)))",
            "1:0: PDF024 found string join() with generator expressions",
            id="String join() with parenthesised generator expression",
        ),
        pytest.param(
            "''.join((\n"
            "        str(i) for i in range(5)\n"
            "        )\n"
            ")\n",
            "1:0: PDF024 found string join() with generator expressions",
            id="String join() with multiline generator expression",
        ),
    ),
)
def test_generator_expressions(source, expected):
    (result,) = results(source)
    assert result == expected
