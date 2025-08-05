import pandas as pd
import unittest
from sampytools.pandas_utils import combine_two_legs_into_single_row_in_dataframe

# Unit test definition
class TestCombineTwoLegs(unittest.TestCase):
    def test_basic_combination(self):
        data = {
            'portfolio_id': ['p1', 'p1'],
            'security_id': ['s1', 's1'],
            'leg_type': ['L', 'S'],
            'currency': ['USD', 'EUR'],
            'value': [100, 200]
        }
        df = pd.DataFrame(data)
        expected_columns = ['portfolio_id', 'security_id', 'currency_L', 'currency_S', 'value_L', 'value_S']
        result = combine_two_legs_into_single_row_in_dataframe(df, 'leg_type', ['portfolio_id', 'security_id'])
        self.assertEqual(set(result.columns), set(expected_columns))
        self.assertEqual(result.loc[0, 'currency_L'], 'USD')
        self.assertEqual(result.loc[0, 'currency_S'], 'EUR')
        self.assertEqual(result.loc[0, 'value_L'], 100)
        self.assertEqual(result.loc[0, 'value_S'], 200)

    def test_custom_leg_names(self):
        data = {
            'id': ['a', 'a'],
            'type': ['buy', 'sell'],
            'price': [10, 12]
        }
        df = pd.DataFrame(data)
        leg_map = {'buy': 'rec', 'sell': 'pay'}
        result = combine_two_legs_into_single_row_in_dataframe(df, 'type', ['id'], leg_names_mapping=leg_map)
        self.assertIn('price_rec', result.columns)
        self.assertIn('price_pay', result.columns)
        self.assertEqual(result.loc[0, 'price_rec'], 10)
        self.assertEqual(result.loc[0, 'price_pay'], 12)

if __name__ == "__main__":
    unittest.main()
