# SciDataContainer for Python

[![Python package](https://github.com/svenkleinert/scidatacontainer/actions/workflows/python-package.yml/badge.svg)](https://github.com/svenkleinert/scidatacontainer/actions/workflows/python-package.yml)
[![codecov](https://codecov.io/gh/svenkleinert/scidatacontainer/branch/main/graph/badge.svg?token=P3RFBHLFAN)](https://codecov.io/gh/svenkleinert/scidatacontainer)

This a Python 3 library for the container file format [SciDataContainer](https://github.com/reincas/scidatacontainer) intended to store scientific data.

## Documenation

You find the [documentation](https://scidatacontainer.readthedocs.io/en/latest/python_library) of the Python package `scidatacontainer` and more on [Read the Docs](https://readthedocs.org/).

## Installation

The easiest way to install the latest version of [`SciDataContainer`](https://pypi.org/project/scidatacontainer/) is using PIP:
```
>>> pip install SciDataContainer
```

## Tests

The tests require the [`coverage`](https://pypi.org/project/coverage/) python package. Run:
```
>>> make report
```
to get a command line coverage report. It's also possible to create a HTML report:
```
>>> make htmlreport
```

