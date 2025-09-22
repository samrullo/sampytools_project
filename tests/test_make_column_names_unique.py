import unittest
import pandas as pd
from pandas.testing import assert_frame_equal
from sampytools.pandas_utils import make_column_names_unique

class TestMakeColumnNamesUnique(unittest.TestCase):

    def test_no_duplicates(self):
        df = pd.DataFrame({
            'A': [1, 2],
            'B': [3, 4]
        })
        result = make_column_names_unique(df.copy())
        self.assertEqual(result.columns.tolist(), ['A', 'B'])

    def test_one_duplicate(self):
        df = pd.DataFrame([[1, 2, 3]], columns=['A', 'B', 'A'])
        result = make_column_names_unique(df.copy())
        print(result.columns.tolist())
        self.assertEqual(result.columns.tolist(), ['A', 'B', 'A1'])

    def test_multiple_duplicates(self):
        df = pd.DataFrame([[1, 2, 3, 4, 5]], columns=['A', 'B', 'A', 'B', 'A'])
        result = make_column_names_unique(df.copy())
        self.assertEqual(result.columns.tolist(), ['A', 'B', 'A1', 'B1', 'A2'])

    def test_all_same_column_name(self):
        df = pd.DataFrame([[1, 2, 3]], columns=['X', 'X', 'X'])
        result = make_column_names_unique(df.copy())
        self.assertEqual(result.columns.tolist(), ['X', 'X1', 'X2'])

    def test_empty_dataframe(self):
        df = pd.DataFrame()
        result = make_column_names_unique(df.copy())
        self.assertEqual(result.columns.tolist(), [])

    def test_single_column(self):
        df = pd.DataFrame([1, 2, 3], columns=['Z'])
        result = make_column_names_unique(df.copy())
        self.assertEqual(result.columns.tolist(), ['Z'])


if __name__ == '__main__':
    unittest.main()
