[![Build Status](https://github.com/MarcoGorelli/pandas-dev-flaker/workflows/tox/badge.svg)](https://github.com/MarcoGorelli/pandas-dev-flaker/actions?workflow=tox)
[![Coverage](https://codecov.io/gh/MarcoGorelli/pandas-dev-flaker/branch/main/graph/badge.svg)](https://codecov.io/gh/MarcoGorelli/pandas-dev-flaker)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/MarcoGorelli/pandas-dev-flaker/main.svg)](https://results.pre-commit.ci/latest/github/MarcoGorelli/pandas-dev-flaker/main)

pandas-dev-flaker
=================

Plugin for `flake8` used to contribute to [pandas](https://github.com/pandas-dev/pandas).

NOTE: this is not a linter meant for pandas usage, but for pandas development. If you want
a linter for pandas usage, please see [pandas-vet](https://github.com/deppen8/pandas-vet).

## installation

`pip install pandas-dev-flaker`

## flake8 codes

| Code   | Description                                                             |
|--------|-------------------------------------------------------------------------|
| PDF001 | import from collections.abc (use 'from collections import abc' instead) |
| PDF002 | pd.api.types used (import from pandas.api.types instead)                |
| PDF003 | pytest.raises used without 'match='                                     |
| PDF004 | builtin filter function used                                            |
| PDF005 | 'pytest.raises' used outside of context manager                         |
| PDF006 | builtin exec used                                                       |
| PDF007 | 'pytest.warns' used (use 'tm.assert_produces_warning' instead)          |
| PDF008 | 'foo.\_\_class\_\_' used, (use 'type(foo)' instead)                     |
| PDF009 | 'common' imported from 'pandas.core' without 'comm' alias               |
| PDF010 | import from 'conftest' found                                            |
| PDF011 | found both 'pd.foo' and 'foo' in the same file                          |
| PDF012 | line split in two unnecessarily by 'black' formatter                    |
| PDF013 | leading space in concatenated strings                                   |
| PDF014 | Found '{foo!r}' formatted value (instead, use 'repr(foo)')              |
| PDF015 | found pytest.xfail (use pytest.mark.xfail instead)                      |
| PDF016 | found private import across modules                                     |
| PDF017 | found import from 'pandas._testing' (use 'import pandas._testing as tm')|
| PDF018 | don't import from pandas.testing                                        |
| PDF019 | found 'os.remove' (use 'tm.ensure_clean' instead)                       |
## contributing

See `contributing.md` for how to get started.

Each new linting rule should be its own file inside `pandas-dev-flaker/_plugins`. Please linting rule should have two sets of tests in `pandas-dev-flaker/tests` - one for when the linting rule is expected to pass, and another for when it's expected to fail.

## credit

Several methods are simplified versions of methods from [pyupgrade](https://github/asottile/pyupgrade). Some of the checks were taken from the [pandas](https://github.com/pandas-dev/pandas) repo. Please find both their licenses in the `LICENSES` folder.

## as a pre-commit hook

See [pre-commit](https://github.com/pre-commit/pre-commit) for instructions

Sample `.pre-commit-config.yaml`:

```yaml
-   repo: https://github.com/pycqa/flake8
    rev: 3.9.0
    hooks:
    -   id: flake8
        additional_dependencies: [pandas-dev-flaker==0.0.1]
```
