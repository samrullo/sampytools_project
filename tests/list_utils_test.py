import unittest
from sampytools.list_utils import add_new_values_in_certain_item_location


class MyTestCase(unittest.TestCase):
    def test_add_new_values_in_certain_item_location(self):
        orig_list = ["one", "bang", "two"]
        new_list = add_new_values_in_certain_item_location(orig_list, "bang", ["bang_one", "bang_two", "bang_three"],
                                                           include_orig_item=True)
        self.assertEqual(["one", "bang","bang_one", "bang_two", "bang_three", "two"], new_list)  # add assertion here


if __name__ == '__main__':
    unittest.main()
