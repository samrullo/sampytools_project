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
        threedf = extract_dict_keys_to_columns(df.copy(), "mydictcol", remove_orig_col=True, prefix="User")
        print(threedf.to_string())
        self.assertTrue("User_name" in threedf.columns)

    def test_filter_df_records_matching_text_patterns(self):
        names=["Tesla corporation lakjdljf","NVIDIA corporatation", "TOYOTA MOTORS", "something else"]
        df=pd.DataFrame({"name":names,"weight":[0.3]*len(names)})
        from sampytools.pandas_utils import filter_df_records_matching_text_patterns
        filterdf=filter_df_records_matching_text_patterns(df,"name",["tesla","toy[A-Za-z]ta"])
        print(filterdf)
        self.assertTrue(len(filterdf)>0)


if __name__ == '__main__':
    unittest.main()
