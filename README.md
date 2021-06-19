[![Build Status](https://github.com/pandas-dev/pandas-dev-flaker/workflows/tox/badge.svg)](https://github.com/pandas-dev/pandas-dev-flaker/actions?workflow=tox)
[![Coverage](https://codecov.io/gh/pandas-dev/pandas-dev-flaker/branch/main/graph/badge.svg)](https://codecov.io/gh/pandas-dev/pandas-dev-flaker)

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
| PDF001 | found import from 'collections.abc' (use 'from collections import abc') |
| PDF002 | builtin 'filter' function used                                            |
| PDF003 | builtin 'exec' function used                                                       |
| PDF004 | 'foo.\_\_class\_\_' used, (use 'type(foo)' instead)                     |
| PDF005 | leading space in concatenated strings                                   |
| PDF006 | Found '{foo!r}' formatted value (instead, use 'repr(foo)')              |
| PDF007 | line split in two unnecessarily by 'black' formatter                    |
| PDF008 | found 'os.remove' (use 'tm.ensure_clean' instead)                       |
| PDF009 | 'pytest.raises' used without 'match='                                   |
| PDF010 | 'pytest.raises' used outside of context manager                         |
| PDF011 | found 'pytest.warns' (use 'pandas._testing.assert_produces_warning')    |
| PDF012 | found 'pytest.xfail' (use 'pytest.mark.xfail' instead)                  |
| PDF013 | import from 'conftest' found                                            |
| PDF014 | found import from 'pandas._testing' (use 'import pandas._testing as tm')|
| PDF015 | from import from 'pandas.testing' (use 'import pandas._testing as tm')  |
| PDF016 | found 'unittest.mock' (use 'pytest.monkeypatch' instead)                |
| PDF017 | 'pd.api.types' used (import from 'pandas.api.types' instead)            |
| PDF018 | 'common' imported from 'pandas.core' without 'com' alias                |
| PDF019 | found both 'pd.foo' and 'foo' in the same file                          |
| PDF020 | found private import across modules                                     |
| PDF021 | found 'np.bool' or 'np.object' (use 'np.bool_' or 'np.object_' instead) |
| PDF022 | found import from 'numpy.random'                                        |
| PDF023 | found assignment to single-letter variable                              |
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
        additional_dependencies: [pandas-dev-flaker==0.2.0]
```
