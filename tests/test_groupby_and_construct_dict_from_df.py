import unittest
import pandas as pd
from sampytools.pandas_utils import groupby_and_construct_dict_from_df

class TestGroupByAndConstructDict(unittest.TestCase):

    def test_basic_case(self):
        df = pd.DataFrame({
            'group': ['A', 'A', 'B', 'B'],
            'key_col': ['k1', 'k2', 'k1', 'k3'],
            'val_col': ['v1', 'v2', 'v3', 'v4']
        })
        result = groupby_and_construct_dict_from_df(df, 'group', 'key_col', 'val_col')
        expected = pd.DataFrame({
            'group': ['A', 'B'],
            "grouped_dict": [{'k1': 'v1', 'k2': 'v2'}, {'k1': 'v3', 'k3': 'v4'}]
        })
        pd.testing.assert_frame_equal(result, expected)

    def test_single_group(self):
        df = pd.DataFrame({
            'group': ['X', 'X'],
            'key_col': ['k5', 'k6'],
            'val_col': ['v5', 'v6']
        })
        result = groupby_and_construct_dict_from_df(df, 'group', 'key_col', 'val_col')
        expected = pd.DataFrame({
            'group': ['X'],
            "grouped_dict": [{'k5': 'v5', 'k6': 'v6'}]
        })
        pd.testing.assert_frame_equal(result, expected)


    def test_duplicate_keys_in_group(self):
        df = pd.DataFrame({
            'group': ['G1', 'G1'],
            'key_col': ['dup', 'dup'],
            'val_col': ['first', 'second']
        })
        result = groupby_and_construct_dict_from_df(df, 'group', 'key_col', 'val_col')
        expected = pd.DataFrame({
            'group': ['G1'],
            "grouped_dict": [{'dup': 'second'}]  # second value overwrites the first in a dict
        })
        pd.testing.assert_frame_equal(result, expected)

    def test_numeric_values(self):
        df = pd.DataFrame({
            'group': ['Z', 'Z'],
            'key_col': ['x', 'y'],
            'val_col': [1, 2]
        })
        result = groupby_and_construct_dict_from_df(df, 'group', 'key_col', 'val_col')
        expected = pd.DataFrame({
            'group': ['Z'],
            "grouped_dict": [{'x': 1, 'y': 2}]
        })
        pd.testing.assert_frame_equal(result, expected)

if __name__ == "__main__":
    unittest.main()
