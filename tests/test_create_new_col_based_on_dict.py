import unittest
import pandas as pd
from sampytools.pandas_utils import create_new_col_based_on_dict

class TestCreateNewColBasedOnDict(unittest.TestCase):

    def test_basic_mapping(self):
        df = pd.DataFrame({"color": ["red", "green", "blue"]})
        mapping_dict = {"red": "#FF0000", "green": "#00FF00", "blue": "#0000FF"}
        result_df = create_new_col_based_on_dict(df, "color", "hex", mapping_dict)
        expected_df = pd.DataFrame({
            "color": ["red", "green", "blue"],
            "hex": ["#FF0000", "#00FF00", "#0000FF"]
        })
        pd.testing.assert_frame_equal(result_df, expected_df)

    def test_partial_mapping(self):
        df = pd.DataFrame({"status": ["active", "inactive", "pending"]})
        mapping_dict = {"active": 1, "inactive": 0}
        result_df = create_new_col_based_on_dict(df, "status", "status_code", mapping_dict)
        expected_df = pd.DataFrame({
            "status": ["active", "inactive", "pending"],
            "status_code": [1, 0, "pending"]
        })
        pd.testing.assert_frame_equal(result_df, expected_df)

    def test_missing_values(self):
        df = pd.DataFrame({"fruit": ["apple", None, "banana"]})
        mapping_dict = {"apple": "red", "banana": "yellow"}
        result_df = create_new_col_based_on_dict(df, "fruit", "color", mapping_dict)
        expected_df = pd.DataFrame({
            "fruit": ["apple", None, "banana"],
            "color": ["red", None, "yellow"]
        })
        pd.testing.assert_frame_equal(result_df, expected_df)


if __name__ == '__main__':
    unittest.main()
