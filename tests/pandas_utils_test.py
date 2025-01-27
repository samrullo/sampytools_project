import unittest
from sampytools.pandas_utils import extract_dict_keys_to_columns
import pandas as pd


class MyTestCase(unittest.TestCase):
    def test_extract_dict_keys_to_columns(self):
        df = pd.DataFrame(data={"col_one": ["lksdjf"] * 3,
                                "col_two": ["lakdsjf"] * 3,
                                "mydictcol": [{"name": "one", "price": 10}, {"name": "two", "price": 20},
                                              {"name": "three", "price": 30}],
                                "myusualcol": ["one", "two", "three"],
                                "colfour": ["lskdjf"] * 3})
        onedf = extract_dict_keys_to_columns(df.copy(), "mydictcol", remove_orig_col=False)
        print(onedf.to_string())
        self.assertTrue("name" in onedf.columns)
        twodf = extract_dict_keys_to_columns(df.copy(), "mydictcol", remove_orig_col=True)
        print(twodf.to_string())
        self.assertFalse("mydictcol" in twodf.columns)


if __name__ == '__main__':
    unittest.main()
