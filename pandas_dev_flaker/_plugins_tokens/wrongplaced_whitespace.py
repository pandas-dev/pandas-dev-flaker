"""
Taken from:

https://github.com/pandas-dev/pandas/blob/33fec602ffd476c8ca1cda8f2963e06623c51b20/scripts/validate_unwanted_patterns.py#L282-L404  # noqa: E501
"""

import tokenize
from typing import Iterator, Sequence, Tuple

from pandas_dev_flaker._data_tokens import register

MSG = "PDF005 leading space in concatenated strings"


def _get_literal_string_prefix_len(token_string: str) -> int:
    """
    Getting the length of the literal string prefix.

    Parameters
    ----------
    token_string : str
        String to check.

    Returns
    -------
    int
        Length of the literal string prefix.

    Examples
    --------
    >>> example_string = "'Hello world'"
    >>> _get_literal_string_prefix_len(example_string)
    0
    >>> example_string = "r'Hello world'"
    >>> _get_literal_string_prefix_len(example_string)
    1
    """
    return min(
        token_string.find(quote)
        for quote in (r"'", r'"')
        if token_string.find(quote) >= 0
    )


@register()
def visit(
    tokens: Sequence[tokenize.TokenInfo],
) -> Iterator[Tuple[int, int, str]]:
    def has_wrong_whitespace(first_line: str, second_line: str) -> bool:
        """
        Checking if the two lines are mattching the unwanted pattern.

        Parameters
        ----------
        first_line : str
            First line to check.
        second_line : str
            Second line to check.

        Returns
        -------
        bool
            True if the two recived string match, an unwanted pattern.

        Notes
        -----
        The unwanted pattern that we are trying to catch is if the spaces in
        a string that is concatenated over multiple lines are placed at the
        end of each string, unless this string is ending with a
        newline character (\n).

        For example, this is bad:

        >>> rule = (
        ...    "We want the space at the end of the line,"
        ...    " not at the beginning"
        ... )

        And what we want is:

        >>> rule = (
        ...    "We want the space at the end of the line, "
        ...    "not at the beginning"
        ... )

        And if the string is ending with a new line character (\n) we
        do not want any trailing whitespaces after it.
        """
        if first_line.endswith(r"\n"):
            return False
        return (not first_line.endswith(" ")) and second_line.startswith(" ")

    for first_token, second_token, third_token in zip(
        tokens,
        tokens[1:],
        tokens[2:],
    ):
        # Checking if we are in a block of concated string
        if (
            first_token.type == third_token.type == tokenize.STRING
            and second_token.type == tokenize.NL
        ):
            # Striping the quotes, with the string litteral prefix
            first_string: str = first_token.string[
                _get_literal_string_prefix_len(first_token.string) + 1 : -1
            ]
            second_string: str = third_token.string[
                _get_literal_string_prefix_len(third_token.string) + 1 : -1
            ]

            if has_wrong_whitespace(first_string, second_string):
                yield (
                    *third_token.start,
                    MSG,
                )
