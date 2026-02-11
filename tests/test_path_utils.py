# tests/test_path_utils.py
import re
import logging
from pathlib import Path

import pytest

from sampytools.path_utils import locate_filename, locate_filename_lowercased


PATTERN = re.compile(r"^data.*\.csv$")


# ---------------------------
# Tests for locate_filename
# (case-sensitive: matches file.name exactly)
# ---------------------------

def test_locate_filename_no_match(tmp_path, caplog):
    (tmp_path / "other.txt").write_text("nope")
    caplog.set_level(logging.WARNING)

    result = locate_filename(tmp_path, PATTERN)
    assert result == "", "Expected empty string when no file matches (case-sensitive)"
    assert "Could not locate file matching pattern" in caplog.text


def test_locate_filename_single_match(tmp_path, caplog):
    (tmp_path / "data_2021.csv").write_text("x")
    (tmp_path / "README.md").write_text("x")
    caplog.set_level(logging.WARNING)

    result = locate_filename(tmp_path, PATTERN)
    assert result == "data_2021.csv"
    assert "Could not locate file matching pattern" not in caplog.text
    assert "Multiple files matching pattern" not in caplog.text


def test_locate_filename_multiple_matches_logs_warning(tmp_path, caplog):
    f1 = tmp_path / "data_a.csv"
    f2 = tmp_path / "data_b.csv"
    f1.write_text("a")
    f2.write_text("b")
    caplog.set_level(logging.WARNING)

    result = locate_filename(tmp_path, PATTERN)
    assert result in {"data_a.csv", "data_b.csv"}
    assert "Multiple files matching pattern" in caplog.text
    assert "Using the first one" in caplog.text
    # both filenames should be mentioned in the warning
    assert "data_a.csv" in caplog.text and "data_b.csv" in caplog.text


def test_locate_filename_is_case_sensitive(tmp_path, caplog):
    # Uppercase filename should NOT match for case-sensitive locate_filename
    (tmp_path / "DATA_UPPER.CSV").write_text("x")
    caplog.set_level(logging.WARNING)

    result = locate_filename(tmp_path, PATTERN)
    assert result == "", "Expected no match because locate_filename is case-sensitive"
    assert "Could not locate file matching pattern" in caplog.text


# ---------------------------
# Tests for locate_filename_lowercased
# (case-insensitive because file.name is lowercased before matching)
# ---------------------------

def test_locate_filename_lowercased_no_match(tmp_path, caplog):
    (tmp_path / "other.txt").write_text("nope")
    caplog.set_level(logging.WARNING)

    result = locate_filename_lowercased(tmp_path, PATTERN)
    assert result == "", "Expected empty string when no file matches (lowercased)"
    assert "Could not locate file matching pattern" in caplog.text


def test_locate_filename_lowercased_single_match(tmp_path, caplog):
    (tmp_path / "data_2021.csv").write_text("x")
    (tmp_path / "README.md").write_text("x")
    caplog.set_level(logging.WARNING)

    result = locate_filename_lowercased(tmp_path, PATTERN)
    assert result == "data_2021.csv"
    assert "Could not locate file matching pattern" not in caplog.text
    assert "Multiple files matching pattern" not in caplog.text


def test_locate_filename_lowercased_multiple_matches_logs_warning(tmp_path, caplog):
    f1 = tmp_path / "data_a.csv"
    f2 = tmp_path / "DATA_B.CSV"  # uppercase variant still considered a match
    f1.write_text("a")
    f2.write_text("b")
    caplog.set_level(logging.WARNING)

    result = locate_filename_lowercased(tmp_path, PATTERN)
    assert result in {"data_a.csv", "DATA_B.CSV"}
    assert "Multiple files matching pattern" in caplog.text
    assert "Using the first one" in caplog.text
    assert "data_a.csv" in caplog.text and "DATA_B.CSV" in caplog.text


def test_locate_filename_lowercased_matches_uppercase_filename(tmp_path, caplog):
    # Uppercase filename should match because locate_filename_lowercased lowercases names
    (tmp_path / "DATA_UPPER.CSV").write_text("x")
    caplog.set_level(logging.WARNING)

    result = locate_filename_lowercased(tmp_path, PATTERN)
    assert result == "DATA_UPPER.CSV"
    assert "Could not locate file matching pattern" not in caplog.text
