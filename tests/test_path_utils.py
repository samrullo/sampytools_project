# tests/test_path_utils.py
import re
import logging
from pathlib import Path

import pytest

from sampytools.path_utils import locate_filename


def test_no_match(tmp_path, caplog):
    # make a file that does NOT match the pattern
    (tmp_path / "other.txt").write_text("nope")
    caplog.set_level(logging.WARNING)

    result = locate_filename(tmp_path, re.compile(r"^data.*\.csv"))
    assert result == "", "Expected empty string when no file matches"
    assert "Could not locate file matching pattern" in caplog.text


def test_single_match(tmp_path, caplog):
    # one matching file and one non-matching file
    (tmp_path / "data_2021.csv").write_text("x")
    (tmp_path / "README.md").write_text("x")
    caplog.set_level(logging.WARNING)

    result = locate_filename(tmp_path, re.compile(r"^data.*\.csv"))
    assert result == "data_2021.csv"
    # no warnings about missing or multiple files
    assert "Could not locate file matching pattern" not in caplog.text
    assert "Multiple files matching pattern" not in caplog.text


def test_multiple_matches(tmp_path, caplog):
    # create two matching files
    f1 = tmp_path / "data_a.csv"
    f2 = tmp_path / "data_b.csv"
    f1.write_text("a")
    f2.write_text("b")
    caplog.set_level(logging.WARNING)

    result = locate_filename(tmp_path, re.compile(r"^data.*\.csv"))
    # filesystem order may vary; function should return one of the matching filenames
    assert result in {"data_a.csv", "data_b.csv"}
    # a warning must be logged describing multiple matches and that the first is used
    assert "Multiple files matching pattern" in caplog.text
    assert "Using the first one" in caplog.text
    # both filenames should be mentioned in the warning message
    assert "data_a.csv" in caplog.text and "data_b.csv" in caplog.text


def test_case_insensitive_match(tmp_path, caplog):
    # filename in uppercase should still match because function lowercases names
    (tmp_path / "DATA_UPPER.CSV").write_text("x")
    caplog.set_level(logging.WARNING)

    result = locate_filename(tmp_path, re.compile(r"^data.*\.csv"))
    assert result == "DATA_UPPER.CSV"
    # no multi-match or missing warnings
    assert "Could not locate file matching pattern" not in caplog.text
    assert "Multiple files matching pattern" not in caplog.text
