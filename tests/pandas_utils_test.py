import unittest
import pathlib

from sampytools.list_utils import get_list_diff

from sampytools.pandas_utils import extract_dict_keys_to_columns
import pandas as pd


class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Setup code here
        print("Setup before any tests")
        cls.test_folder = pathlib.Path.cwd() / "test_data"

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
        names = ["Tesla corporation lakjdljf", "NVIDIA corporatation", "TOYOTA MOTORS", "something else"]
        df = pd.DataFrame({"name": names, "weight": [0.3] * len(names)})
        from sampytools.pandas_utils import filter_df_records_matching_text_patterns
        filterdf = filter_df_records_matching_text_patterns(df, "name", ["tesla", "toy[A-Za-z]ta"])
        print(filterdf)
        self.assertTrue(len(filterdf) > 0)

    def test_list_of_dict_to_dataframe(self):
        from sampytools.pandas_utils import list_of_dict_to_dataframe
        records = [{"custdim": "one", "custval": "one value"}, {"custdim": "two", "custval": "two value"}]
        df = list_of_dict_to_dataframe(records, "custdim", "custval")
        print(df)
        self.assertTrue(len(df) > 0)
        df2=list_of_dict_to_dataframe(records)
        print(df2)
        self.assertTrue(len(df2)>0)

    def test_order_merged_dataframe_cols(self):
        from sampytools.pandas_utils import order_merged_dataframe_cols
        file=self.test_folder/"pos.csv"
        onedf=pd.read_csv(file)
        twodf=pd.read_csv(file)
        twodf["quantity"]=twodf["quantity"]*2
        mrgdf=pd.merge(left=onedf,right=twodf,how="left",on=["portfolio","asset_id"],suffixes=("_one","_two"))
        print(f"mrgdf before ordering:\n{mrgdf.to_string()}")
        mrgdf=order_merged_dataframe_cols(mrgdf,["portfolio","asset_id"],get_list_diff(onedf.columns,["portfolio","asset_id"]),("_one","_two"))
        print(f"mrgdf after ordering:\n{mrgdf.to_string()}")
        self.assertTrue(len(mrgdf)==2)

    def test_print_df_header(self):
        df=pd.DataFrame({"col_one":[1,2,3],"col_two":[4,5,6]})
        from sampytools.pandas_utils import print_df_header
        print_df_header(df)
        self.assertTrue(len(df)>0)

    def test_remove_nonnumeric_chars_from_numeric_cols(self):
        from sampytools.pandas_utils import remove_nonnumeric_chars_from_numeric_cols
        df=pd.DataFrame({"mv":["123,456","234,567","345,765"]})
        df=remove_nonnumeric_chars_from_numeric_cols(df)
        print(df)
        self.assertTrue(len(df)>0)



if __name__ == '__main__':
    unittest.main()
