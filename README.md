# Introduction
These are python utility scripts defined by Subkhon.

Over the years I have written quite a number of python utility functions related to data analysis.

And I want to make that available to all my projects.

# What kind of utilities?

I define various utilities as functions under sampytools package.
I have pyproject.toml defined that can be used to install the package by running pip install from within the sampytools_project directory.

```bash
pip install -e .
```

- configdict.py provides powerful ConfigDict that gives you ability to access values with dot notation
- datetime_utils.py gives you various date time functions such as formatting functions to_yyyymmdd
- pandas_utils various utilities like make column names unique, strip trailing and leading spaces from column values
- text utilities such as regex matching , removing duplicate lines
- list_utils.py gives you list related utilities such as searching item in the list, flattening list of lists etc.

# To build wheel

First ensure you have ```build``` library installed

Then run

```bash
python -m build --no-isolation
```

Above command will build the project and create wheel file.
Then you can re-install the wheel in your virtual environment

```bash
pip install sampytools-1.0.0-py3-none-any.whl --force-reinstall
```