import unittest
import datetime
from sampytools.datetime_utils import get_previous_month_end_from_today


class MyTestCase(unittest.TestCase):
    def test_get_previous_month_end_from_toda(self):
        eom = get_previous_month_end_from_today()
        print(eom)
        self.assertTrue(eom.day >= 28)
        eom=get_previous_month_end_from_today(datetime.date(2025, 2, 10))
        print(eom)
        self.assertTrue(eom.day >= 28)

    def test_parse_yymmdd(self):
        from sampytools.datetime_utils import parse_yymmdd
        yymmdd = "250210"
        dt = parse_yymmdd(yymmdd)
        print(dt)
        self.assertTrue(dt.day>=10)


if __name__ == '__main__':
    unittest.main()
